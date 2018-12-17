#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2018 Fridolin Pokorny
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""A Gremlin server adapter communicating via a web socket."""

import asyncio
import functools
import logging
import os
import typing
import re
from itertools import chain
from collections import ChainMap

import uvloop
from aiogremlin.process.graph_traversal import AsyncGraphTraversal
from gremlin_python.process.traversal import Order
from gremlin_python.process.traversal import without
from gremlin_python.process.traversal import gt
from gremlin_python.process.graph_traversal import inE
from gremlin_python.process.graph_traversal import id as id_
from gremlin_python.process.graph_traversal import outE
from gremlin_python.process.graph_traversal import constant
from gremlin_python.process.graph_traversal import flatMap
from goblin import Goblin

from thoth.common import datetime_str2timestamp
from thoth.common import timestamp2datetime

from ..base import StorageBase
from ..exceptions import NotFoundError
from .models import ALL_MODELS
from .models import CVE
from .models import DebDepends
from .models import DependsOn
from .models import DebPackageVersion
from .models import DebPreDepends
from .models import DebReplaces
from .models import EcosystemSolver
from .models import HasArtifact
from .models import HasVersion
from .models import HasVulnerability
from .models import IsPartOf
from .models import Package
from .models import PythonArtifact
from .models import PythonPackageVersion
from .models import Requires
from .models import RunsIn
from .models import PythonPackageIndex
from .models import RunsOn
from .models import BuildsIn
from .models import BuildsOn
from .models import BuildtimeEnvironment
from .models import RPMPackageVersion
from .models import RPMRequirement
from .models import RuntimeEnvironment
from .models import HardwareInformation
from .models import Solved
from .models import SoftwareStack
from .models import CreatesStack

# from .utils import enable_edge_cache
from .utils import enable_vertex_cache
from ..analyses import AnalysisResultsStore
from ..solvers import SolverResultsStore

_LOGGER = logging.getLogger(__name__)

# http://goblin.readthedocs.io/en/latest/performance.html#use-uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def _get_hashable_id(val):
    # https://github.com/davebshow/goblin/issues/55#issuecomment-318446037
    result = val
    if isinstance(val, dict) and "@type" in val and "@value" in val:
        if val["@type"] == "janusgraph:RelationIdentifier":
            result = val["@value"]["value"]
    return result


def requires_connection(func):  # Ignore PyDocStyleBear
    """Force implicit connection if not connected already."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.is_connected():
            self.connect()
        func(self, *args, **kwargs)

    return wrapper


class GraphDatabase(StorageBase):
    """A Gremlin server adapter communicating via a web socket."""

    ENVVAR_HOST_NAME = "JANUSGRAPH_SERVICE_HOST"
    ENVVAR_HOST_PORT = "JANUSGRAPH_SERVICE_PORT"

    DEFAULT_HOST = os.getenv(ENVVAR_HOST_NAME) or "localhost"
    DEFAULT_PORT = os.getenv(ENVVAR_HOST_PORT) or 8182

    DEFAULT_SERIALIZER = {
        "className": "org.apache.tinkerpop.gremlin.driver.ser.GryoMessageSerializerV1d0",
        "config": {"serializeResultToString": True},
    }

    def __init__(self, hosts=None, port=None, serializer=None):
        """Initialize Gremlin server database adapter."""
        super().__init__()
        self.app = None
        self.hosts = hosts or [self.DEFAULT_HOST]
        self.port = port or self.DEFAULT_PORT
        self.serializer = serializer or self.DEFAULT_SERIALIZER

    @classmethod
    def create(cls, host, port=None):
        """Create a graph adapter, only for one host (syntax sugar)."""
        return cls(hosts=[host], port=port)

    @property
    def g(self):
        """Retrieve the g object for synchronous operations."""
        return self.session.g

    @property
    def session(self):
        """Return session to the graph database."""
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.app.session())

    @staticmethod
    def normalize_python_package_name(package_name: str) -> str:
        """Normalize Pyton package name based on PEP-0503."""
        # Make sure we have normalized names in the graph database according to PEP:
        #   https://www.python.org/dev/peps/pep-0503/#normalized-names
        return re.sub(r"[-_.]+", "-", package_name).lower()

    def is_connected(self):
        """Check if we are connected to a remote Gremlin server."""
        # TODO: this will maybe require some logic to be sure that the
        # connection is healthy.
        return self.app is not None

    def connect(self):
        """Connect to a graph database via a websocket.

        Use GraphSONSerializersV2d0.
        """
        loop = asyncio.get_event_loop()
        self.app = loop.run_until_complete(
            Goblin.open(
                loop, get_hashable_id=_get_hashable_id, hosts=self.hosts, port=self.port, serializer=self.serializer
            )
        )
        self.app.register(*tuple(ALL_MODELS))

    def disconnect(self):
        """Close all connections - disconnect from remote."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.app.close())
        self.app = None

    def get_analysis_metadata(self, analysis_document_id: str) -> dict:
        """Get metadata stored for the given analysis document."""
        query = (
            self.g.E()
            .has("__label__", IsPartOf.__label__)
            .has("__type__", "edge")
            .has("analysis_document_id", analysis_document_id)
            .sample(1)
            .project("analysis_datetime", "analysis_document_id", "analyzer_name", "analyzer_version")
            .by("analysis_datetime")
            .by("analysis_document_id")
            .by("analyzer_name")
            .by("analyzer_version")
            .next()
        )

        result = asyncio.get_event_loop().run_until_complete(query)

        if not result:
            raise NotFoundError(f"Analysis with analysis document if {analysis_document_id} was not found")

        result["analysis_datetime"] = timestamp2datetime(result["analysis_datetime"])

        return result

    def register_python_package_index(
        self, url: str, *, warehouse_api_url: str = None, verify_ssl: bool = True, warehouse: bool = False
    ) -> typing.Tuple[PythonPackageIndex, bool]:
        """Return a list of available Python package indexes."""
        python_package_index = PythonPackageIndex.from_properties(
            url=url, warehouse_api_url=warehouse_api_url, verify_ssl=verify_ssl, warehouse=warehouse
        )
        existed = python_package_index.get_or_create(self.g)
        return python_package_index, existed

    def runtime_environment_listing(self, start_offset: int = 0, count: int = 100) -> list:
        """Get listing of runtime environments available."""
        query = (
            self.g.V()
            .has("__label__", RuntimeEnvironment.__label__)
            .has("__type__", "vertex")
            .values("runtime_environment_name")
            .dedup()
            .order()
            .range(start_offset, start_offset + count)
            .toList()
        )

        return asyncio.get_event_loop().run_until_complete(query)

    def runtime_environment_analyses_listing(
        self, runtime_environment_name: str, start_offset: int = 0, count: int = 100
    ) -> list:
        """Get listing of analyses available for the given environment."""
        query = (
            self.g.V()
            .has("__label__", RuntimeEnvironment.__label__)
            .has("__type__", "vertex")
            .has("runtime_environment_name", runtime_environment_name)
            .inE()
            .has("__label__", IsPartOf.__label__)
            .has("__type__", "edge")
            .order()
            .by("analysis_datetime", Order.decr)
            .project("analysis_datetime", "analysis_document_id", "analyzer_name", "analyzer_version")
            .by("analysis_datetime")
            .by("analysis_document_id")
            .by("analyzer_name")
            .by("analyzer_version")
            .dedup()
            .range(start_offset, start_offset + count)
            .toList()
        )

        entries = asyncio.get_event_loop().run_until_complete(query)

        if not entries:
            # TODO: we could optimize this into a single query
            query = (
                self.g.V()
                .has("__label__", RuntimeEnvironment.__label__)
                .has("__type__", "vertex")
                .has("runtime_environment_name", runtime_environment_name)
                .count()
                .next()
            )

            count = asyncio.get_event_loop().run_until_complete(query)
            if not count:
                raise NotFoundError(f"No analyses found for runtime environment {runtime_environment_name!r}")

        for entry in entries:
            entry["analysis_datetime"] = timestamp2datetime(entry["analysis_datetime"])

        return entries

    def get_runtime_environment(self, runtime_environment_name: str, analysis_document_id: str = None) -> tuple:
        """Get runtime environment dependencies by its name.

        Select the newest analysis if no document id is present.
        """
        loop = asyncio.get_event_loop()

        if not analysis_document_id:
            analysis_document_id = loop.run_until_complete(
                self.g.V()
                .has("__label__", RuntimeEnvironment.__label__)
                .has("__type__", "vertex")
                .has("runtime_environment_name", runtime_environment_name)
                .inE()
                .has("__label__", IsPartOf.__label__)
                .order()
                .by("analysis_datetime", Order.decr)
                .range(0, 1)
                .valueMap()
                .select("analysis_document_id")
                .next()
            )

            if not analysis_document_id:
                raise NotFoundError(f"No entries for runtime environment {runtime_environment_name!r} found")

        query = (
            self.g.V()
            .has("__label__", RuntimeEnvironment.__label__)
            .has("__type__", "vertex")
            .has("runtime_environment_name", runtime_environment_name)
            .coalesce(
                inE().has("__label__", IsPartOf.__label__).has("analysis_document_id", analysis_document_id).outV(),
                constant(False),
            )
            .toList()
        )

        result = loop.run_until_complete(query)
        if not result:
            # TODO: we are assuming that an analysis has always at
            # least some entries
            raise NotFoundError(
                f"No entries for runtime environment {runtime_environment_name!r} with "
                f"analysis document id {analysis_document_id!r} found"
            )

        if result[0] is False:
            raise NotFoundError(f"No entries for runtime environment {runtime_environment_name!r} found")

        return result, analysis_document_id

    def python_package_version_exists(self, package_name: str, package_version: str, index_url: str = None) -> bool:
        """Check if the given Python package version exists in the graph database."""
        package_name = self.normalize_python_package_name(package_name)
        loop = asyncio.get_event_loop()

        query = (
            self.g.V()
            .has("__label__", PythonPackageVersion.__label__)
            .has("ecosystem", "pypi")
            .has("package_name", package_name)
            .has("package_version", package_version)
        )

        if index_url:
            query = query.has("index_url", index_url)

        query = query.constant(True).next()

        return bool(loop.run_until_complete(query))

    def python_package_exists(self, package_name: str) -> bool:
        """Check if the given Python package exists regardless of version."""
        package_name = self.normalize_python_package_name(package_name)
        loop = asyncio.get_event_loop()

        query = (
            self.g.V()
            .has("__type__", "vertex")
            .has("__label__", Package.__label__)
            .has("ecosystem", "pypi")
            .has("package_name", package_name)
            .next()
        )

        return bool(loop.run_until_complete(query))

    def _get_stack(self, packages: typing.List[tuple]) -> AsyncGraphTraversal:
        """Get all stacks that include the given set of packages."""
        # The query starts in a package and ends first in a software stack - this
        # way we get all the software stacks where the first package is present. We
        # then traverse backwards to the second package from the stack where we
        # ended up first and continue from package to back to all software stacks
        # in which the second package is present. As we are chaining these queries
        # we get a software stack where there is the first and the second package
        # present at the same time. The query continues for all N packages giving
        # back all software stacks where all N packages are present (note there can
        # be also other packages).
        if len(packages) == 0:
            raise ValueError("Cannot query for a stack with no packages.")

        package_name, package_version, index_url = packages[0]
        query = self.g.V().has('__type__', 'vertex') \
            .has('__label__', 'python_package_version') \
            .has('ecosystem', 'pypi') \
            .has('package_version', package_version) \
            .has('package_name', package_name) \
            .has('index_url', index_url) \
            .outE() \
            .has('__type__', 'edge') \
            .has('__label__', 'creates_stack') \
            .inV().has('__type__', 'vertex').has('__label__', 'software_stack')

        for package_name, package_version, index_url in packages[1:]:
            query = query.inE() \
                .has('__type__', 'edge').has('__label__', 'creates_stack') \
                .outV() \
                .has('__type__', 'vertex') \
                .has('__label__', 'python_package_version') \
                .has('ecosystem', 'pypi') \
                .has('package_version', package_version) \
                .has('package_name', package_name) \
                .has('index_url', index_url) \
                .outE() \
                .has('__type__', 'edge') \
                .has('__label__', 'creates_stack') \
                .inV().has('__type__', 'vertex').has('__label__', 'software_stack')

        return query

    def get_software_stacks(self, packages: typing.List[tuple]) -> typing.List[SoftwareStack]:
        """Get all stacks that include the given set of packages.

        Packages in stacks returned are superset of packages in the original set of
        packages given in parameters - meaning a returned stack has packages as
        provided in the parameter, but can also have additional packages.
        """
        query = self._get_stack(packages)
        return asyncio.get_event_loop().run_until_complete(query.toList())

    @staticmethod
    def _compute_python_package_version_avg_performance_on_hw(
        query, hardware_specs: dict, runtime_environment_name: str
    ) -> float:
        """Extend the avg performance query so that there is taken into account hardware we run on."""
        query = query.inV().has("__label__", RuntimeEnvironment.__label__)

        if runtime_environment_name:
            query = query.has("runtime_environment_name", runtime_environment_name)

        query = query.outE().has("__label__", RunsOn.__label__).inV().has("__label__", HardwareInformation.__label__)

        for attribute_name, attribute_value in hardware_specs.items():
            query = query.has(attribute_name, attribute_value)

        query = query.inE().has("__label__", "runs_on").values("performance_index").mean().next()

        return asyncio.get_event_loop().run_until_complete(query)

    def compute_python_package_version_avg_performance(
        self,
        packages: tuple,
        *,
        runtime_environment_name: str = None,
        hardware_specs: dict = None,
    ) -> float:
        """Get average performance of Python packages on the given runtime environment.

        We derive this average performance based on software stacks we have
        evaluated on the given runtime environment including the given
        package in specified version. There are also included stacks that
        failed for some reason that have negative performance impact on the overall value.

        There are considered software stacks that include packages listed,
        they can however include also other packages.

        Optional parameters additionally slice results - e.g. if runtime_environment is set,
        it picks only resutls that match the given parameters criteria.
        """
        query = self._get_stack(packages)
        query = query.outE().has("__label__", RunsIn.__label__)

        if runtime_environment_name and not hardware_specs:
            query = (
                query.inV()
                .has("__label__", RuntimeEnvironment.__label__)
                .has("runtime_environment_name", runtime_environment_name)
                .inE()
                .has("__label__", RunsIn.__label__)
            )

        if hardware_specs:
            # We pass runtime environment name to optimize traversal (no need to go back).
            return self._compute_python_package_version_avg_performance_on_hw(
                query, hardware_specs, runtime_environment_name
            )

        query = query.values("performance_index").mean().next()
        return asyncio.get_event_loop().run_until_complete(query)

    def get_all_versions_python_package(self, package_name: str, index_url: str = None) -> typing.List[tuple]:
        """Get all versions available for a Python package."""
        package_name = self.normalize_python_package_name(package_name)
        query = (
            self.g.V()
            .has("__label__", "python_package_version")
            .has("__type__", "vertex")
            .has("ecosystem", "pypi")
            .has("package_name", package_name)
        )

        if index_url:
            query = query.has("index_url", index_url)

        query = query.valueMap().select("package_version", "index_url").dedup().toList()

        # TODO: we could optimize this query
        result = []
        query_result = asyncio.get_event_loop().run_until_complete(query)
        for item in query_result:
            result.append((item["package_version"][0], item["index_url"][0]))

        return result

    def retrieve_unsolved_pypi_packages(self) -> dict:
        """Retrieve a dictionary mapping package names to versions that dependencies were not yet resolved."""
        query = (
            self.g.V()
            .has("__label__", "python_package_version")
            .has("__type__", "vertex")
            .has("ecosystem", "pypi")
            .has("package_name")
            .has("package_version")
            .not_(inE().has("__label__", Solved.__label__).has("__type__", "edge"))
            .group()
            .by("package_name")
            .by("package_version")
            .next()
        )

        return asyncio.get_event_loop().run_until_complete(query)

    def retrieve_solved_pypi_packages(self) -> dict:
        """Retrieve a dictionary mapping package names to versions for dependencies that were already solved."""
        query = (
            self.g.E()
            .has("__label__", Solved.__label__)
            .has("__type__", "edge")
            .inV()
            .dedup()
            .group()
            .by("package_name")
            .by("package_version")
            .next()
        )

        return asyncio.get_event_loop().run_until_complete(query)

    def retrieve_unsolvable_pypi_packages(self) -> dict:
        """Retrieve a dictionary mapping package names to versions of packages that were marked as unsolvable."""
        query = (
            self.g.V()
            .has("__label__", "python_package_version")
            .has("__type__", "vertex")
            .has("ecosystem", "pypi")
            .has("package_name")
            .has("package_version")
            .and_(
                inE()
                .has("__label__", Solved.__label__)
                .has("__type__", "edge")
                .has("solver_error", True)
                .has("solver_error_unsolvable", True)
                .has("solver_error_unparsable", False)
            )
            .group()
            .by("package_name")
            .by("package_version")
            .next()
        )

        return asyncio.get_event_loop().run_until_complete(query)

    def retrieve_unparsable_pypi_packages(self) -> dict:
        """Retrieve a dictionary mapping package names to versions of packages that couldn't be parsed by solver."""
        query = (
            self.g.V()
            .has("__label__", "python_package_version")
            .has("__type__", "vertex")
            .has("ecosystem", "pypi")
            .has("package_name")
            .has("package_version")
            .and_(
                inE()
                .has("__label__", Solved.__label__)
                .has("__type__", "edge")
                .has("solver_error", True)
                .has("solver_error_unparsable", True)
                .has("solver_error_unpsolvable", False)
            )
            .group()
            .by("package_name")
            .by("package_version")
            .next()
        )

        return asyncio.get_event_loop().run_until_complete(query)

    def get_all_python_packages_count(self, without_error: bool = True) -> int:
        """Retrieve number of Python packages stored in the graph database."""
        if not without_error:
            query = (
                self.g.V()
                .has("__label__", PythonPackageVersion.__label__)
                .has("__type__", "vertex")
                .has("ecosystem", "pypi")
                .has("package_name")
                .has("package_version")
                .count()
                .next()
            )
        else:
            query = (
                self.g.E()
                .has("__label__", Solved.__label__)
                .has("__type__", "edge")
                .has("solver_document_id")
                .has("solver_datetime")
                .has("solver_error", False)
                .has("solver_error_unsolvable")
                .has("solver_error_unparsable")
                .inV()
                .has("__label__", PythonPackageVersion.__label__)
                .has("__type__", "vertex")
                .has("ecosystem", "pypi")
                .has("package_name")
                .has("package_version")
                .dedup()
                .count()
                .next()
            )

        return asyncio.get_event_loop().run_until_complete(query)

    def get_error_python_packages_count(self, unsolvable: bool = False, unparsable: bool = False) -> int:
        """Retrieve number of Python packages stored in the graph database with error flag."""
        if unsolvable and uparsable:
            raise ValueError("Properties unsolvable and unparsable are disjoin")

        query = (
            self.g.E()
            .has("__label__", Solved.__label__)
            .has("__type__", "edge")
            .has("solver_document_id")
            .has("solver_datetime")
            .has("solver_error", True)
            .has("solver_error_unsolvable", unsolvable)
            .has("solver_error_unparsable", unparsable)
            .inV()
            .has("__label__", PythonPackageVersion.__label__)
            .has("__type__", "vertex")
            .has("ecosystem", "pypi")
            .has("package_name")
            .has("package_version")
            .dedup()
            .count()
            .next()
        )

        return asyncio.get_event_loop().run_until_complete(query)

    def get_solver_documents_count(self) -> int:
        """Get number of solver documents synced into graph."""
        query = (
            self.g.E()
            .has("__label__", Solved.__label__)
            .has("__type__", "edge")
            .has("solver_document_id")
            .has("solver_datetime")
            .has("solver_error")
            .has("solver_error_unsolvable")
            .has("solver_error_unparsable")
            .valueMap()
            .select("solver_document_id")
            .dedup()
            .count()
            .next()
        )

        return asyncio.get_event_loop().run_until_complete(query)

    def get_analyzer_documents_count(self) -> int:
        """Get number of image analysis documents synced into graph."""
        query = (
            self.g.E()
            .has("__type__", "edge")
            .has("__type__", Requires.__label__)
            .has("analysis_datetime")
            .has("analysis_document_id")
            .has("analyzer_name")
            .has("analyzer_version")
            .valueMap()
            .select("analysis_document_id")
            .dedup()
            .count()
            .next()
        )

        return asyncio.get_event_loop().run_until_complete(query)

    def retrieve_dependent_packages(self, package_name: str) -> dict:
        """Get mapping package name to package version of packages that depend on the given package."""
        # TODO: when added __type__ Cassanda backend time outs.
        # TODO: specify index
        # This should be fixed once we move to Data Hub.
        package_name = self.normalize_python_package_name(package_name)
        query = (
            self.g.E()
            .has("__label__", "depends_on")
            .has("package_name", package_name)
            .outV()
            .dedup()
            .group()
            .by("package_name")
            .by("package_version")
            .next()
        )

        return asyncio.get_event_loop().run_until_complete(query)

    def retrieve_dependencies(self, package_name: str, package_version: str, index: str) -> dict:
        """Get mapping package name to package version of packages that are dependencies for the given pkg."""
        package_name = self.normalize_python_package_name(package_name)
        query = (
            self.g.V()
            .has("__label__", "depends_on")
            .has("package_name", package_name)
            .has("package_version", package_version)
            .has("index", index)
            .invV()
            .dedup()
            .group()
            .by("package_name")
            .by("package_version")
            .next()
        )

        return asyncio.get_event_loop().run_until_complete(query)

    async def get_python_package_tuple(self, python_package_node_id: int) -> typing.Dict[int, tuple]:
        session = await self.app.session()
        result = (
            await session.g.V(python_package_node_id).values("package_name", "package_version", "index_url").toList()
        )

        return {python_package_node_id: result}

    def get_python_package_tuples(self, python_package_node_ids: typing.Set[int]) -> typing.Dict[int, dict]:
        """Get package name, package version and index URL for each python package node.

        This query is good to be used in conjunction with query retrieving
        transitive dependencies. The main benefit of this function is that it
        performs all the queries in an event loop per each package.
        """
        if len(python_package_node_ids) == 0:
            return {}

        tasks = []
        for python_package_node_id in python_package_node_ids:
            task = asyncio.ensure_future(self.get_python_package_tuple(python_package_node_id))
            tasks.append(task)

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(asyncio.gather(*tasks))
        results_dict = list(chain(results))
        return dict(ChainMap(*results_dict))

    def retrieve_transitive_dependencies_python(self, package_name: str, package_version: str, index_url: str) -> list:
        """Get all transitive dependencies for the given package by traversing dependency graph.

        It's much faster to retieve just dependencies for the transitive
        dependencies as most of the time is otherwise spent in serialization
        and deserialization of query results.
        """
        package_name = self.normalize_python_package_name(package_name)
        query = (
            self.g.V()
            .has("__type__", "vertex")
            .has("__label__", "python_package_version")
            .has("ecosystem", "pypi")
            .has("package_version", package_version)
            .has("package_name", package_name)
            .has("index_url", index_url)
            .repeat(flatMap(outE().simplePath().has("__type__", "edge").has("__label__", "depends_on").inV()))
            .emit()
            .path()
            .by(id_())
            .toList()
        )

        return asyncio.get_event_loop().run_until_complete(query)

    def solver_records_exist(self, solver_document: dict) -> bool:
        """Check if the given solver document record exists."""
        loop = asyncio.get_event_loop()

        document_id = SolverResultsStore.get_document_id(solver_document)
        query = (
            self.g.V()
            .has("__label__", EcosystemSolver.__label__)
            .has("__type__", "vertex")
            .has("solver_name", solver_document["metadata"]["analyzer"])
            .has("solver_version", solver_document["metadata"]["analyzer_version"])
            .outE()
            .has("__type__", "edge")
            .has("__label__", Solved.__label__)
            .has("solver_document_id", document_id)
            .has("solver_datetime", datetime_str2timestamp(solver_document["metadata"]["datetime"]))
            .count()
            .next()
        )

        return loop.run_until_complete(query) > 0

    def solver_document_id_exist(self, solver_document_id: str) -> bool:
        """Check if there is a solver document record with the given id."""
        loop = asyncio.get_event_loop()

        query = self.g.E().has("solver_document_id", solver_document_id).count().is_(gt(0)).next()

        return bool(loop.run_until_complete(query))

    def analysis_records_exist(self, analysis_document: dict) -> bool:
        """Check whether the given analysis document records exist in the graph database."""
        loop = asyncio.get_event_loop()

        document_id = AnalysisResultsStore.get_document_id(analysis_document)
        query = (
            self.g.E()
            .has("__label__", IsPartOf.__label__)
            .has("__type__", "edge")
            .has("analysis_datetime", datetime_str2timestamp(analysis_document["metadata"]["datetime"]))
            .has("analysis_document_id", document_id)
            .has("analyzer_name", analysis_document["metadata"]["analyzer"])
            .has("analyzer_version", analysis_document["metadata"]["analyzer_version"])
            .count()
            .next()
        )

        return loop.run_until_complete(query) > 0

    def analysis_document_id_exist(self, analysis_document_id: str) -> bool:
        """Check if there is an analysis document record with the given id."""
        loop = asyncio.get_event_loop()

        query = self.g.E().has("solver_document_id", analysis_document_id).count().is_(gt(0)).next()

        return bool(loop.run_until_complete(query))

    def inspection_document_id_exist(self, inspection_document_id: str) -> bool:
        """Check if there is an inspection document record with the given id."""
        loop = asyncio.get_event_loop()

        query = self.g.E().has("inspection_document_id", inspection_document_id).count().is_(gt(0)).next()

        return bool(loop.run_until_complete(query))

    @staticmethod
    def _parse_cpu(cpu_spec) -> float:
        """Parse the given CPU requirement as used by OpenShift/Kubernetes."""
        if isinstance(cpu_spec, str):
            if cpu_spec.endswith("m"):
                cpu_spec = cpu_spec[:-1]
                return int(cpu_spec) / 1000

        return float(cpu_spec)

    @staticmethod
    def _parse_memory(memory_spec) -> float:
        if isinstance(memory_spec, (float, int)):
            return float(memory_spec)

        if memory_spec.endswith("E"):
            memory_spec = float(memory_spec[:-1])
            return memory_spec * 1000 ** 6
        elif memory_spec.endswith("P"):
            memory_spec = float(memory_spec[:-1])
            return memory_spec * 1000 ** 5
        elif memory_spec.endswith("T"):
            memory_spec = float(memory_spec[:-1])
            return memory_spec * 1000 ** 4
        elif memory_spec.endswith("G"):
            memory_spec = float(memory_spec[:-1])
            return memory_spec * 1000 ** 3
        elif memory_spec.endswith("M"):
            memory_spec = float(memory_spec[:-1])
            return memory_spec * 1000 ** 2
        elif memory_spec.endswith("K"):
            memory_spec = float(memory_spec[:-1])
            return memory_spec * 1000
        elif memory_spec.endswith("Ei"):
            memory_spec = float(memory_spec[:-2])
            return memory_spec * 1024 ** 6
        elif memory_spec.endswith("Pi"):
            memory_spec = float(memory_spec[:-2])
            return memory_spec * 1024 ** 5
        elif memory_spec.endswith("Ti"):
            memory_spec = float(memory_spec[:-2])
            return memory_spec * 1024 ** 4
        elif memory_spec.endswith("Gi"):
            memory_spec = float(memory_spec[:-2])
            return memory_spec * 1024 ** 3
        elif memory_spec.endswith("Mi"):
            memory_spec = float(memory_spec[:-2])
            return memory_spec * 1024 ** 2
        elif memory_spec.endswith("Ki"):
            memory_spec = float(memory_spec[:-2])
            return memory_spec * 1024

    def _get_hardware_information(self, specs: dict) -> HardwareInformation:
        """Get hardware information based on requests provided."""
        hardware = specs.get("hardware") or {}
        return HardwareInformation.from_properties(
            cpu_family=hardware.get("cpu_family"),
            cpu_model=hardware.get("cpu_model"),
            cpu_physical_cpus=hardware.get("physical_cpus"),
            cpu_model_name=hardware.get("processor"),
            cpu_cores=self._parse_cpu(specs["cpu"]) if specs.get("cpu") else None,
            ram_size=self._parse_memory(specs["memory"]) if specs.get("memory") else None,
        )

    def create_software_stack_pipfile(self, pipfile_locked: dict, software_stack_name: str) -> SoftwareStack:  # Ignore PyDocStyleBear
        """Create a software stack inside graph database from a Pipfile.lock."""

        def get_index_url(index_name: str):
            for source_index in pipfile_locked["_meta"]["sources"]:
                if source_index["name"] == index_name:
                    return source_index["url"]

            raise ValueError(f"Index with name {index_name!r} not found in Pipfile.lock metadata")

        python_packages = []
        for package_name, package_info in pipfile_locked["default"].items():
            # TODO: sync also test packages?
            if not package_info["version"].startswith("=="):
                _LOGGER.error(
                    "Package %r in version %r in the Pipfile.lock was not pinned to a specific version correctly",
                    package_name,
                    package_info["version"],
                )
                package_version = package_info["version"]
            else:
                package_version = package_info["version"][len("==") :]  # Ignore PycodestyleBear (E203)

            index_url = get_index_url(package_info["index"])

            _, v, python_package_version = self.create_pypi_package_version(
                package_name, package_version, index_url=index_url
            )
            python_packages.append(python_package_version)

        software_stack = SoftwareStack.from_properties(software_stack_name=software_stack_name)
        software_stack.get_or_create(self.g)

        for python_package_version in python_packages:
            CreatesStack.from_properties(source=python_package_version, target=software_stack).get_or_create(self.g)

        return software_stack

    def sync_inspection_result(self, document) -> None:
        """Sync the given inspection document into the graph database."""
        software_stack = None
        if document["specification"].get("python"):
            software_stack = self.create_software_stack_pipfile(
                document["specification"]["python"]["requirements_locked"],
                document["inspection_id"]
            )

        environment_name = document["inspection_id"]
        if document["job_log"] is not None:
            performance_index = None
            if document["status"]["job"]["exit_code"] != 0:
                # Negative performance index - the application does not run.
                performance_index = -1.0
            elif isinstance(document["job_log"]["stdout"], dict):
                try:
                    performance_index = float(document["job_log"]["stdout"].get("performance_index"))
                except Exception:
                    _LOGGER.error("Failed to parse performance index - not a float: %s", performance_index)

            if performance_index is None:
                _LOGGER.warning("No performance index found in document for inspection %r", document["inspection_id"])

            if not document["specification"].get("packages"):
                # Use the base image as an environment name if there were not
                # installed any native packages.
                environment_name = document["specification"]["base"]

            runtime_environment = RuntimeEnvironment.from_properties(runtime_environment_name=environment_name)
            runtime_environment.get_or_create(self.g)

            runtime_hardware = self._get_hardware_information(document["specification"]["run"]["requests"])
            runtime_hardware.get_or_create(self.g)

            run_error = document["status"]["job"]["exit_code"] == 0

            if software_stack:
                if performance_index is not None:
                    RunsIn.from_properties(
                        source=software_stack,
                        target=runtime_environment,
                        inspection_document_id=document["inspection_id"],
                        run_error=run_error,
                        performance_index=performance_index,
                    ).get_or_create(self.g)
                else:
                    # We cannot pass performance_index as None as goblin will complain.
                    RunsIn.from_properties(
                        source=software_stack,
                        target=runtime_environment,
                        inspection_document_id=document["inspection_id"],
                        run_error=run_error,
                    ).get_or_create(self.g)

            if performance_index is not None:
                RunsOn.from_properties(
                    source=runtime_environment,
                    target=runtime_hardware,
                    inspection_document_id=document["inspection_id"],
                    run_error=run_error,
                    performance_index=performance_index,
                ).get_or_create(self.g)
            else:
                RunsOn.from_properties(
                    source=runtime_environment,
                    target=runtime_hardware,
                    inspection_document_id=document["inspection_id"],
                    run_error=run_error,
                ).get_or_create(self.g)

        buildtime_environment = BuildtimeEnvironment.from_properties(buildtime_environment_name=environment_name)
        buildtime_environment.get_or_create(self.g)

        buildtime_hardware = self._get_hardware_information(document["specification"]["build"]["requests"])
        buildtime_hardware.get_or_create(self.g)

        build_error = document["status"]["build"]["exit_code"] == 0

        if software_stack:
            BuildsIn.from_properties(
                source=software_stack,
                target=buildtime_environment,
                inspection_document_id=document["inspection_id"],
                build_error=build_error,
            ).get_or_create(self.g)

        BuildsOn.from_properties(
            source=buildtime_environment,
            target=buildtime_hardware,
            inspection_document_id=document["inspection_id"],
            build_error=build_error,
        ).get_or_create(self.g)

    def create_pypi_package_version(
        self,
        package_name: str,
        package_version: str,
        index_url: typing.Optional[str],
        *,
        hashes: list = None,
        only_if_package_seen: bool = False,
    ) -> typing.Union[None, tuple]:
        """Create entries for PyPI package version."""
        package_name = self.normalize_python_package_name(package_name)

        if only_if_package_seen:
            query = (
                self.g.V()
                .has("__type__", "vertex")
                .has("__label__", Package.__label__)
                .has("ecosystem", "pypi")
                .has("package_name", package_name)
                .count()
                .next()
            )
            seen = asyncio.get_event_loop().run_until_complete(query)
            if not seen:
                return None

        python_package = Package.from_properties(ecosystem="pypi", package_name=package_name)
        python_package.get_or_create(self.g)

        python_package_version = PythonPackageVersion.from_properties(
            ecosystem="pypi", package_name=package_name, package_version=package_version, index_url=index_url
        )
        python_package_version.get_or_create(self.g)

        has_version = HasVersion.from_properties(source=python_package, target=python_package_version)
        has_version.get_or_create(self.g)

        for digest in hashes or []:
            python_artifact = PythonArtifact.from_properties(artifact_hash_sha256=digest)
            python_artifact.get_or_create(self.g)

            HasArtifact.from_properties(source=python_package_version, target=python_artifact).get_or_create(self.g)

        return python_package, has_version, python_package_version

    def unsolved_runtime_environments(self, package_name: str, package_version: str) -> list:
        """Get unsolved runtime environment which are not connected and attached to python package version."""
        package_name = self.normalize_python_package_name(package_name)
        query = (
            self.g.V()
            .has("__label__", "python_package_version")
            .has("package_name", package_name)
            .has("package_version", package_version)
            .inE()
            .has("__label__", "solved")
            .outV()
            .dedup()
            .aggregate("solvers_solved_python_package_version")
            .V()
            .has("__label__", "ecosystem_solver")
            .where(without("solvers_solved_python_package_version"))
            .dedup()
            .project("solver_name", "solver_version")
            .toList()
        )

        return asyncio.get_event_loop().run_until_complete(query)

    # @enable_edge_cache
    @enable_vertex_cache
    def sync_solver_result(self, document: dict) -> None:
        """Sync the given solver result to the graph database."""
        ecosystem_solver = EcosystemSolver.from_properties(
            solver_name=document["metadata"]["analyzer"], solver_version=document["metadata"]["analyzer_version"]
        )
        ecosystem_solver.get_or_create(self.g)

        solver_document_id = SolverResultsStore.get_document_id(document)
        solver_datetime = datetime_str2timestamp(document["metadata"]["datetime"])

        for python_package_info in document["result"]["tree"]:
            try:
                python_package, _, python_package_version = self.create_pypi_package_version(
                    python_package_info["package_name"],
                    python_package_info["package_version"],
                    python_package_info["index_url"],
                    hashes=python_package_info["sha256"],
                )

                Solved.from_properties(
                    source=ecosystem_solver,
                    target=python_package_version,
                    solver_document_id=solver_document_id,
                    solver_datetime=solver_datetime,
                    solver_error=False,
                    solver_error_unsolvable=False,
                    solver_error_unparsable=False,
                ).get_or_create(self.g)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(f"Failed to sync Python package, error is not fatal: {python_package_info!r}")
                continue

            for dependency in python_package_info["dependencies"]:
                try:
                    for index_entry in dependency["resolved_versions"]:
                        index_url = index_entry["index"]
                        for dependency_version in index_entry["versions"]:
                            python_package_dependency, _, python_package_version_dependency = self.create_pypi_package_version(  # Ignore PycodestyleBear (E501)
                                package_name=dependency["package_name"],
                                package_version=dependency_version,
                                index_url=index_url,
                            )

                            Solved.from_properties(
                                source=ecosystem_solver,
                                target=python_package_version_dependency,
                                solver_document_id=solver_document_id,
                                solver_datetime=solver_datetime,
                                solver_error=False,
                                solver_error_unsolvable=False,
                                solver_error_unparsable=False,
                            ).get_or_create(self.g)

                            # TODO: mark extras
                            DependsOn.from_properties(
                                source=python_package_version,
                                target=python_package_version_dependency,
                                package_name=python_package_version_dependency.package_name.value,
                                version_range=dependency["required_version"] or "*",
                            ).get_or_create(self.g)
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.exception(
                        f"Failed to sync Python package {python_package_version.to_dict()}" f"dependency: {dependency}"
                    )

        for error_info in document["result"]["errors"]:
            try:
                python_package, _, python_package_version = self.create_pypi_package_version(
                    package_name=error_info.get("package_name") or error_info["package"],
                    package_version=error_info["version"],
                    index_url=error_info["index"],
                )

                Solved.from_properties(
                    source=ecosystem_solver,
                    target=python_package_version,
                    solver_document_id=solver_document_id,
                    solver_datetime=solver_datetime,
                    solver_error=True,
                    solver_error_unsolvable=False,
                    solver_error_unparsable=False,
                ).get_or_create(self.g)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Failed to sync Python package, error is not fatal: %r", error_info)

        for unsolvable in document["result"]["unresolved"]:
            if not unsolvable["version_spec"].startswith("=="):
                # No resolution can be perfomed so no identifier is captured, report warning and continue.
                # We would like to capture this especially when there are
                # packages in ecosystem that we cannot find (e.g. not configured private index
                # or removed package).
                _LOGGER.warning(
                    f"Cannot sync unsolvable package {unsolvable} as package is not locked to as specific version"
                )
                continue

            package_version = unsolvable["version_spec"][len("==") :]  # Ignore PycodestyleBear (E203)
            try:
                python_package, _, python_package_version = self.create_pypi_package_version(
                    package_name=unsolvable["package_name"],
                    package_version=package_version,
                    index_url=unsolvable["index"],
                )

                Solved.from_properties(
                    source=ecosystem_solver,
                    target=python_package_version,
                    solver_document_id=solver_document_id,
                    solver_datetime=solver_datetime,
                    solver_error=True,
                    solver_error_unsolvable=True,
                    solver_error_unparsable=False,
                ).get_or_create(self.g)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Failed to sync unsolvable Python package, error is not fatal: %r", unsolvable)

        for unparsed in document["result"]["unparsed"]:
            parts = unparsed["requirement"].rsplit("==", maxsplit=1)
            if len(parts) != 2:
                # This request did not come from graph-refresh job as there is not pinned version.
                _LOGGER.warning(
                    f"Cannot sync unparsed package {unparsed} as package is not locked to as specific version"
                )
                continue

            package_name, package_version = parts
            try:
                python_package, _, python_package_version = self.create_pypi_package_version(
                    package_name=package_name, package_version=package_version, index_url=None
                )

                Solved.from_properties(
                    source=ecosystem_solver,
                    target=python_package_version,
                    solver_document_id=solver_document_id,
                    solver_datetime=solver_datetime,
                    solver_error=True,
                    solver_error_unsolvable=False,
                    solver_error_unparsable=True,
                ).get_or_create(self.g)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Failed to sync unparsed Python package, error is not fatal: %r", unparsed)

    def _deb_sync_analysis_result(
        self, document_id: str, document: dict, runtime_environment: RuntimeEnvironment
    ) -> None:
        """Sync results of deb packages found in the given container image."""
        for deb_package_info in document["result"]["deb-dependencies"]:
            try:
                deb_package_version = DebPackageVersion.from_properties(
                    ecosystem="deb",
                    package_name=deb_package_info["name"],
                    package_version=deb_package_info["version"],
                    arch=deb_package_info["arch"],
                    epoch=deb_package_info.get("epoch"),
                )
                deb_package_version.get_or_create(self.g)

                deb_package = Package.from_properties(
                    ecosystem=deb_package_version.ecosystem, package_name=deb_package_version.package_name
                )
                deb_package.get_or_create(self.g)

                HasVersion.from_properties(source=deb_package, target=deb_package_version).get_or_create(self.g)

                IsPartOf.from_properties(
                    source=deb_package_version,
                    target=runtime_environment,
                    analysis_datetime=datetime_str2timestamp(document["metadata"]["datetime"]),
                    analysis_document_id=document_id,
                    analyzer_name=document["metadata"]["analyzer"],
                    analyzer_version=document["metadata"]["analyzer_version"],
                ).get_or_create(self.g)

                # These three can be grouped with a zip, but that is not that readable...
                for pre_depends in deb_package_info.get("pre-depends") or []:
                    package = Package.from_properties(ecosystem="deb", package_name=pre_depends["name"])
                    package.get_or_create(self.g)

                    DebPreDepends.from_properties(
                        source=deb_package_version, target=package, version_range=pre_depends.get("version")
                    ).get_or_create(self.g)

                for depends in deb_package_info.get("depends") or []:
                    package = Package.from_properties(ecosystem="deb", package_name=depends["name"])
                    package.get_or_create(self.g)

                    DebDepends.from_properties(
                        source=deb_package_version, target=package, version_range=depends.get("version")
                    ).get_or_create(self.g)

                for replaces in deb_package_info.get("replaces") or []:
                    package = Package.from_properties(ecosystem="deb", package_name=replaces["name"])
                    package.get_or_create(self.g)

                    DebReplaces.from_properties(
                        source=deb_package_version, target=package, version_range=replaces.get("version")
                    ).get_or_create(self.g)
            except Exception:
                _LOGGER.exception("Failed to sync debian package, error is not fatal: %r", deb_package_info)

    def _rpm_sync_analysis_result(
        self, document_id: str, document: dict, runtime_environment: RuntimeEnvironment
    ) -> None:
        """Sync results of RPMs found in the given container image."""
        for rpm_package_info in document["result"]["rpm-dependencies"]:
            try:
                rpm_package_version = RPMPackageVersion.from_properties(
                    ecosystem="rpm",
                    package_name=rpm_package_info["name"],
                    package_version=rpm_package_info["version"],
                    release=rpm_package_info.get("release"),
                    epoch=rpm_package_info.get("epoch"),
                    arch=rpm_package_info.get("arch"),
                    src=rpm_package_info.get("src", False),
                    package_identifier=rpm_package_info.get("package_identifier", rpm_package_info["name"]),
                )
                rpm_package_version.get_or_create(self.g)

                rpm_package = Package.from_properties(
                    ecosystem=rpm_package_version.ecosystem, package_name=rpm_package_version.package_name
                )
                rpm_package.get_or_create(self.g)

                HasVersion.from_properties(source=rpm_package, target=rpm_package_version).get_or_create(self.g)

                IsPartOf.from_properties(
                    source=rpm_package_version,
                    target=runtime_environment,
                    analysis_datetime=datetime_str2timestamp(document["metadata"]["datetime"]),
                    analysis_document_id=document_id,
                    analyzer_name=document["metadata"]["analyzer"],
                    analyzer_version=document["metadata"]["analyzer_version"],
                ).get_or_create(self.g)

            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(f"Failed to sync RPM package, error is not fatal: {rpm_package_info!r}")
                continue

            for dependency in rpm_package_info["dependencies"]:
                try:
                    rpm_requirement = RPMRequirement.from_properties(rpm_requirement_name=dependency)
                    rpm_requirement.get_or_create(self.g)

                    Requires.from_properties(
                        source=rpm_package_version,
                        target=rpm_requirement,
                        analysis_datetime=datetime_str2timestamp(document["metadata"]["datetime"]),
                        analysis_document_id=document_id,
                        analyzer_name=document["metadata"]["analyzer"],
                        analyzer_version=document["metadata"]["analyzer_version"],
                    ).get_or_create(self.g)
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.exception(
                        f"Failed to sync dependencies for " f"RPM {rpm_package_version.to_dict()}: {dependency!r}"
                    )

    def _python_sync_analysis_result(
        self, document_id: str, document: dict, runtime_environment: RuntimeEnvironment
    ) -> None:
        """Sync results of Python packages found in the given container image."""
        # or [] should go to analyzer to be consistent
        for python_package_info in document["result"]["mercator"] or []:
            if python_package_info["ecosystem"] == "Python-RequirementsTXT":
                # We don't want to sync found requirement.txt artifacts as
                # they do not carry any valuable information for us.
                continue

            if "result" not in python_package_info or "error" in python_package_info["result"]:
                # Mercator was unable to process this - e.g. there was a
                # setup.py that is not distutils setup.py
                _LOGGER.info("Skipping error entry - %r", python_package_info)
                continue

            try:
                # TODO: we should run analysis on packages not to have packages
                # in the graph database triggering solver runs
                # TODO: we should check for hashes in the graph database to see
                # if we have the given package
                python_package, _, python_package_version = self.create_pypi_package_version(
                    package_name=python_package_info["result"]["name"],
                    package_version=python_package_info["result"]["version"],
                    index_url=None,
                )

                IsPartOf.from_properties(
                    source=python_package_version,
                    target=runtime_environment,
                    analysis_datetime=datetime_str2timestamp(document["metadata"]["datetime"]),
                    analysis_document_id=document_id,
                    analyzer_name=document["metadata"]["analyzer"],
                    analyzer_version=document["metadata"]["analyzer_version"],
                ).get_or_create(self.g)
            except Exception:  # pylint: disable=broad-exception
                _LOGGER.exception(f"Failed to sync Python package, error is not fatal: {python_package_info!r}")

    def create_python_cve_record(
        self,
        package_name: str,
        package_version: str,
        index_url: str,
        *,
        record_id: str,
        version_range: str,
        advisory: str,
        cve: str = None,
    ) -> typing.Tuple[CVE, bool]:
        """Store information about a CVE in the graph database for the given Python package."""
        cve_record = CVE.from_properties(cve_id=record_id, version_range=version_range, advisory=advisory, cve_name=cve)
        cve_record_existed = cve_record.get_or_create(self.g)
        _LOGGER.debug("CVE record wit id %r ", record_id, "added" if not cve_record_existed else "was already present")

        # We explicitly track vulnerable packages (only_if_package_seen=False).
        python_package, _, python_package_version = self.create_pypi_package_version(
            package_name, package_version, index_url=index_url, only_if_package_seen=False
        )

        has_vulnerability = HasVulnerability.from_properties(source=python_package_version, target=cve_record)
        has_vulnerability_existed = has_vulnerability.get_or_create(self.g)

        _LOGGER.debug(
            "CVE record %r for vulnerability of %r in version %r ",
            record_id,
            package_name,
            package_version,
            "added" if not has_vulnerability_existed else "was already present",
        )
        return cve_record, has_vulnerability_existed

    def get_python_cve_records(self, package_name: str, package_version: str) -> typing.List[CVE]:
        """Get known vulnerabilities for the given package-version."""
        package_name = self.normalize_python_package_name(package_name)
        query = (
            self.g.V()
            .has("__label__", "python_package_version")
            .has("package_name", package_name)
            .has("package_version", package_version)
            .outE()
            .has("__label__", "has_vulnerability")
            .inV()
            .toList()
        )

        return asyncio.get_event_loop().run_until_complete(query)

    def get_python_package_version_hashes_sha256(
        self, package_name: str, package_version: str, index_url: str
    ) -> typing.List[str]:
        """Get hashes for a Python package in specified version."""
        query = (
            self.g.V()
            .has("__label__", "python_package_version")
            .has("package_name", package_name)
            .has("package_version", package_version)
            .has("index_url", index_url)
            .outE()
            .has("__label__", "has_artifact")
            .inV()
            .valueMap()
            .select("artifact_hash_sha256")
            .toList()
        )

        return list(chain(*asyncio.get_event_loop().run_until_complete(query)))

    def get_all_python_package_version_hashes_sha256(self, package_name: str, package_version: str) -> list:
        """Get hashes for a Python package per index."""
        query = (
            self.g.V()
            .has("__label__", "python_package_version")
            .has("package_name", package_name)
            .has("package_version", package_version)
            .flatMap(outE().inV())
            .has("__label__", "python_artifact")
            .has("__type__", "vertex")
            .path()
            .by("index_url")
            .by("artifact_hash_sha256")
            .toList()
        )

        return asyncio.get_event_loop().run_until_complete(query)

    # @enable_edge_cache
    @enable_vertex_cache
    def sync_analysis_result(self, document: dict) -> None:
        """Sync the given analysis result to the graph database."""
        runtime_environment = RuntimeEnvironment.from_properties(
            runtime_environment_name=document["metadata"]["arguments"]["extract-image"]["image"]
        )
        runtime_environment.get_or_create(self.g)
        document_id = AnalysisResultsStore.get_document_id(document)
        self._rpm_sync_analysis_result(document_id, document, runtime_environment)
        self._deb_sync_analysis_result(document_id, document, runtime_environment)
        self._python_sync_analysis_result(document_id, document, runtime_environment)

    def register_python_package_index(self, url: str, warehouse_api_url: str = None, verify_ssl: bool = True):
        """Register the given Python package index in the graph database."""
        package_index = PythonPackageIndex.from_properties(
            url=url, warehouse_api_url=warehouse_api_url, verify_ssl=verify_ssl
        )
        package_index.get_or_create(self.g)

    def python_package_index_listing(self) -> list:
        """Get listing of Python package indexes registered in the JanusGraph database."""
        query = self.g.V().has("__label__", PythonPackageIndex.__label__).toList()

        return [item.to_dict() for item in asyncio.get_event_loop().run_until_complete(query)]

    def get_python_package_index_urls(self) -> list:
        """Retrieve all the URLs of registered Python package indexes."""
        query = self.g.V().has("__label__", PythonPackageIndex.__label__).valueMap().select("url").toList()

        return list(chain(*asyncio.get_event_loop().run_until_complete(query)))

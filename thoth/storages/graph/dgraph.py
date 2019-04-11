#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2019 Fridolin Pokorny
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

"""A Dgraph server adapter communicating via gRPC."""

import logging
import os
import re
import json
from typing import List
from typing import Set
from typing import Tuple
from typing import Optional
from typing import Dict
from typing import Iterable
from pathlib import Path
from itertools import chain

import pkg_resources
import grpc
import pydgraph

from thoth.common import datetime_str2timestamp
# from thoth.common import timestamp2datetime
from thoth.common import OpenShift

from ..base import StorageBase
from .models_base import enable_vertex_cache
from .models import Advised
from .models import AdviserSoftwareStack
# from .models import BuildObservation
from .models import BuildsIn
from .models import BuildsOn
from .models import BuildtimeEnvironment as BuildtimeEnvironmentModel
from .models import CreatesStack
from .models import CVE
from .models import DebDepends
from .models import DebPackageVersion
from .models import DebPreDepends
from .models import DebReplaces
from .models import DependsOn
from .models import EcosystemSolver
from .models import EnvironmentBase
from .models import HardwareInformation
from .models import HasArtifact
from .models import HasVersion
from .models import HasVulnerability
from .models import InspectionSoftwareStack
from .models import IsPartOf
# from .models import Observed
from .models import Package
from .models import PythonArtifact
from .models import PythonPackageIndex
from .models import PythonPackageVersion
from .models import Requires
from .models import RPMPackageVersion
from .models import RPMRequirement
from .models import RunsIn
from .models import RunsOn
from .models import RuntimeEnvironment as RuntimeEnvironmentModel
from .models import SoftwareStackBase
# from .models import SoftwareStackObservation
from .models import Solved
from .models import UserSoftwareStack

# from ..exceptions import NotFoundError
from ..exceptions import NotConnected
from ..advisers import AdvisersResultsStore
from ..analyses import AnalysisResultsStore
from ..provenance import ProvenanceResultsStore
from ..solvers import SolverResultsStore

_LOGGER = logging.getLogger(__name__)


class GraphDatabase(StorageBase):
    """A dgraph server adapter communicating via gRPC."""

    TLS_PATH = os.getenv("GRAPH_TLS_PATH")
    ENVVAR_HOST_NAME = "GRAPH_SERVICE_HOST"
    DEFAULT_HOST = os.getenv(ENVVAR_HOST_NAME) or "localhost:8080"

    def __init__(self, hosts: List[str] = None, tls_path: str = None):
        """Initialize Dgraph server database adapter."""
        self._hosts = hosts or [self.DEFAULT_HOST]
        self._tls_path = tls_path or self.TLS_PATH
        self._client = None
        self._stubs = []

    @property
    def client(self) -> pydgraph.DgraphClient:
        """Retrieve client for communicating with DGraph instance."""
        if self._client is None:
            raise NotConnected("No client established to talk to a Draph instance")

        return self._client

    def __del__(self) -> None:
        """Disconnect properly on object destruction."""
        if self.is_connected():
            self.disconnect()

    @classmethod
    def create(cls, host: str):
        """Create a graph adapter, only for one host (syntax sugar)."""
        return cls(hosts=[host])

    def is_connected(self) -> bool:
        """Check if we are connected to a remote Dgraph instance."""
        return self._client is not None

    def connect(self):
        """Connect to a Dgraph via gRPC."""
        credentials = None
        if self._tls_path:
            root_ca_cert = (Path(self._tls_path) / "./ca.crt").read_bytes()
            client_cert_key = (Path(self._tls_path) / "./client.user.key").read_bytes()
            client_cert = (Path(self._tls_path) / "./client.user.crt").read_bytes()

            credentials= grpc.ssl_channel_credentials(
                root_certificates=root_ca_cert,
                private_key=client_cert_key,
                certificate_chain=client_cert,
            )

        for address in self._hosts:
            self._stubs.append(pydgraph.DgraphClientStub(address, credentials=credentials))

        self._client = pydgraph.DgraphClient(*self._stubs)

    def disconnect(self):
        """Close all connections - disconnect from remote."""
        for stub in self._stubs:
            stub.close()

        self._stubs = []
        del self._client
        self._client = None

    def initialize_schema(self) -> None:
        """Initialize Dgraph's schema."""
        version_self = pkg_resources.get_distribution("thoth-storages").version
        _LOGGER.info("Initializing Dgraph with schema, schema version is %r", version_self)
        schema = (Path(__file__).parent / "schema.rdf").read_text()
        operation = pydgraph.Operation(schema=schema)
        self.client.alter(operation)

    def drop_all(self) -> None:
        """Drop all data present inside Dgraph instance."""
        _LOGGER.warning("Dropping all data on Dgraph's instance")
        operation = pydgraph.Operation(drop_all=True)
        self.client.alter(operation)

    @staticmethod
    def normalize_python_package_name(package_name: str) -> str:
        """Normalize Python package name based on PEP-0503."""
        # Make sure we have normalized names in the graph database according to PEP:
        #   https://www.python.org/dev/peps/pep-0503/#normalized-names
        # TODO: use compiled re
        return re.sub(r"[-_.]+", "-", package_name).lower()

    @staticmethod
    def parse_python_solver_name(solver_name: str) -> dict:
        """Parse os and Python identifiers encoded into solver name."""
        if solver_name.startswith("solver-"):
            solver_identifiers = solver_name[len("solver-"):]
        else:
            raise ValueError("Solver name has to start with 'solver-' prefix")

        parts = solver_identifiers.split("-")
        if len(parts) != 3:
            raise ValueError(
                "Solver should be in a form of 'solver-<os_name>-<os_version>-<python_version>, "
                f"solver name {solver_name} does not correspond to this naming schema"
            )

        python_version = parts[2]
        if python_version.startswith("py"):
            python_version = python_version[len("py"):]
        else:
            raise ValueError(
                f"Python version encoded into Python solver name does not start with 'py' prefix: {solver_name}"
            )

        python_version = ".".join(list(python_version))
        return {"os_name": parts[0], "os_version": parts[1], "python_version": python_version}

    def _query_raw(self, query: str, variables: dict = None, *, read_only: bool = True) -> dict:
        """Perform raw query on connected Dgraph instance."""
        assert self._client is not None, "Adapter is not connected to any Dgraph instance."
        txn = self._client.txn(read_only=read_only)

        try:
            result = txn.query(query, variables=variables)
        finally:
            # Safe after commit based on docs.
            txn.discard()

        _LOGGER.debug("Query statistics:\n%s", result.latency)
        return json.loads(result.json)

    def get_analysis_metadata(self, analysis_document_id: str) -> dict:
        """Get metadata stored for the given analysis document."""
        return {}

    def runtime_environment_listing(self, start_offset: int = 0, count: int = 100) -> list:
        """Get listing of runtime environments available."""
        return []

    def runtime_environment_analyses_listing(
        self, runtime_environment_name: str, start_offset: int = 0, count: int = 100
    ) -> list:
        """Get listing of analyses available for the given environment."""
        return []

    def get_runtime_environment(self, runtime_environment_name: str, analysis_document_id: str = None) -> tuple:
        """Get runtime environment dependencies by its name.

        Select the newest analysis if no document id is present.
        """
        return (1,)

    def python_package_version_exists(self, package_name: str, package_version: str, index_url: str = None) -> bool:
        """Check if the given Python package version exists in the graph database."""
        return True

    def python_package_exists(self, package_name: str) -> bool:
        """Check if the given Python package exists regardless of version."""
        return True

    def _get_stack(self, packages: Set[tuple]) -> str:
        """Get all stacks that include the given set of packages."""
        if len(packages) == 0:
            raise ValueError("Cannot query for a stack with no packages.")

        return ""

    def get_software_stacks(self, packages: List[Tuple[str, str, str]]) -> List[Set[Tuple[str, str, str]]]:
        """Get all stacks that include the given set of packages.

        Packages in stacks returned are superset of packages in the original set of
        packages given in parameters - meaning a returned stack has packages as
        provided in the parameter, but can also have additional packages.
        """
        return []

    def compute_python_package_version_avg_performance(
        self, packages: Set[tuple], *, runtime_environment: dict = None, hardware_specs: dict = None
    ) -> Optional[float]:
        """Get average performance of Python packages on the given runtime environment with hardware specs.

        We derive this average performance based on software stacks we have
        evaluated on the given runtime environment including the given
        package in specified version. There are also included stacks that
        failed for some reason that have negative performance impact on the overall value.

        There are considered software stacks that include packages listed,
        they can however include also other packages.

        Optional parameters additionally slice results - e.g. if runtime_environment is set,
        it picks only results that match the given parameters criteria.
        """
        return None

    def get_all_versions_python_package(
        self,
        package_name: str,
        index_url: str = None,
        *,
        os_name: str = None,
        os_version: str = None,
        python_version: str = None,
        without_error: bool = False,
    ) -> List[Tuple[str, str]]:
        """Get all versions available for a Python package."""
        return []

    def retrieve_unsolved_pypi_packages(self, solver_name: str = None) -> dict:
        """Retrieve a dictionary mapping package names to versions that dependencies were not yet resolved.

        If solver_name argument is provided the given solver, query narrows down to packages that were
        not resolved by the given solver.
        """
        return {}

    def retrieve_solved_pypi_packages(self) -> dict:
        """Retrieve a dictionary mapping package names to versions for dependencies that were already solved."""
        return {}

    def retrieve_unsolvable_pypi_packages(self) -> dict:
        """Retrieve a dictionary mapping package names to versions of packages that were marked as unsolvable."""
        return {}

    def retrieve_unparsable_pypi_packages(self) -> dict:
        """Retrieve a dictionary mapping package names to versions of packages that couldn't be parsed by solver."""
        return {}

    def get_all_python_packages_count(self, without_error: bool = True) -> int:
        """Retrieve number of Python packages stored in the graph database."""
        return -1

    def get_error_python_packages_count(self, unsolvable: bool = False, unparsable: bool = False) -> int:
        """Retrieve number of Python packages stored in the graph database with error flag."""
        return -1

    def get_solver_documents_count(self) -> int:
        """Get number of solver documents synced into graph."""
        query = """
        query q($l: string) {
            f(func: has(%s)) {
                cnt: count(uid)
            }
        }
        """ % EcosystemSolver.get_label()
        result = self._query_raw(query)
        return result["f"][0]["cnt"]

    def get_analyzer_documents_count(self) -> int:
        """Get number of image analysis documents synced into graph."""
        return -1

    def retrieve_dependent_packages(self, package_name: str) -> dict:
        """Get mapping package name to package version of packages that depend on the given package."""
        return {}

    def retrieve_dependencies(self, package_name: str, package_version: str, index: str) -> dict:
        """Get mapping package name to package version of packages that are dependencies for the given pkg."""
        package_name = self.normalize_python_package_name(package_name)
        return {}

    def unsolved_runtime_environments(self, package_name: str, package_version: str) -> list:
        """Get unsolved runtime environment which are not connected and attached to python package version."""
        return []

    def get_python_package_tuples(self, python_package_node_ids: Set[int]) -> Dict[int, tuple]:
        """Get package name, package version and index URL for each python package node.

        This query is good to be used in conjunction with query retrieving
        transitive dependencies. The main benefit of this function is that it
        performs all the queries in an event loop per each package.
        """
        return {}

    def retrieve_transitive_dependencies_python(
        self,
        package_name: str,
        package_version: str,
        index_url: str,
        *,
        os_name: str = None,
        os_version: str = None,
        python_version: str = None,
    ) -> list:
        """Get all transitive dependencies for the given package by traversing dependency graph.

        It's much faster to retrieve just dependencies for the transitive
        dependencies as most of the time is otherwise spent in serialization
        and deserialization of query results.
        """
        return []

    def solver_records_exist(self, solver_document: dict) -> bool:
        """Check if the given solver document record exists."""
        return True

    def solver_document_id_exist(self, solver_document_id: str) -> bool:
        """Check if there is a solver document record with the given id."""
        return True

    def adviser_document_id_exist(self, adviser_document_id: str) -> bool:
        """Check if there is a adviser document record with the given id."""
        return True

    def analysis_records_exist(self, analysis_document: dict) -> bool:
        """Check whether the given analysis document records exist in the graph database."""
        return True

    def analysis_document_id_exist(self, analysis_document_id: str) -> bool:
        """Check if there is an analysis document record with the given id."""
        return True

    def inspection_document_id_exist(self, inspection_document_id: str) -> bool:
        """Check if there is an inspection document record with the given id."""
        return True

    def provenance_checker_document_id_exist(self, provenance_checker_document_id: str) -> bool:
        """Check if there is a provenance-checker document record with the given id."""
        return True

    def get_python_cve_records(self, package_name: str, package_version: str) -> List[dict]:
        """Get known vulnerabilities for the given package-version."""
        return []

    def get_python_package_version_hashes_sha256(
        self, package_name: str, package_version: str, index_url: str
    ) -> List[str]:
        """Get hashes for a Python package in specified version."""
        return []

    def get_all_python_package_version_hashes_sha256(self, package_name: str, package_version: str) -> list:
        """Get hashes for a Python package per index."""
        return []

    def register_python_package_index(self, url: str, warehouse_api_url: str = None, verify_ssl: bool = True):
        """Register the given Python package index in the graph database."""
        return None

    def python_package_index_listing(self) -> list:
        """Get listing of Python package indexes registered in the JanusGraph database."""
        return []

    def get_python_package_index_urls(self) -> list:
        """Retrieve all the URLs of registered Python package indexes."""
        query = """
        query q($l: string) {
            f(func: has(%s)) {
                u: url
            }
        }
        """ % PythonPackageIndex.get_label()
        result = self._query_raw(query)
        return list(chain(item['u'] for item in result["f"]))

    def get_python_packages_for_index(self, index_url: str) -> Set[str]:
        """Retrieve listing of Python packages known to graph database instance for the given index."""
        return set()

    def get_python_packages(self) -> Set[str]:
        """Retrieve listing of all Python packages known to graph database instance."""
        return set()

    def _python_packages_create_stack(
        self, python_package_versions: Iterable[PythonPackageVersion], software_stack: SoftwareStackBase
    ) -> None:
        """Assign the given set of packages to the stack."""
        for python_package_version in python_package_versions:
            CreatesStack.from_properties(source=python_package_version, target=software_stack).get_or_create(self.client)

    def create_python_packages_pipfile(self, pipfile_locked: dict) -> List[PythonPackageVersion]:
        """Create Python packages from Pipfile.lock entries and return them."""
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

            existed, _, v, python_package_version = self.create_pypi_package_version(
                package_name, package_version, index_url=index_url
            )
            python_packages.append(python_package_version)

        return python_packages

    def create_user_software_stack_pipfile(
        self, document_id: str, pipfile_locked: dict, *, origin: str = None
    ) -> UserSoftwareStack:
        """Create a user software stack entry from Pipfile.lock."""
        python_package_versions = self.create_python_packages_pipfile(pipfile_locked)
        software_stack = UserSoftwareStack.from_properties(document_id=document_id, origin=origin)
        software_stack.get_or_create(self.client)
        self._python_packages_create_stack(python_package_versions, software_stack)
        return software_stack

    def create_inspection_software_stack_pipfile(
        self, document_id: str, pipfile_locked: dict
    ) -> InspectionSoftwareStack:
        """Create an inspection software stack entry from Pipfile.lock."""
        python_package_versions = self.create_python_packages_pipfile(pipfile_locked)
        software_stack = InspectionSoftwareStack.from_properties(document_id=document_id)
        software_stack.get_or_create(self.client)
        self._python_packages_create_stack(python_package_versions, software_stack)
        return software_stack

    def create_adviser_software_stack_pipfile(
        self, document_id: str, pipfile_locked: dict, *, adviser_stack_index: int
    ) -> AdviserSoftwareStack:
        """Create an inspection software stack entry from Pipfile.lock."""
        python_package_versions = self.create_python_packages_pipfile(pipfile_locked)
        software_stack = AdviserSoftwareStack.from_properties(
            document_id=document_id, adviser_stack_index=adviser_stack_index
        )
        software_stack.get_or_create(self.client)
        self._python_packages_create_stack(python_package_versions, software_stack)
        return software_stack

    def create_pypi_package_version(
        self,
        package_name: str,
        package_version: str,
        index_url: Optional[str],
        *,
        hashes: list = None,
        only_if_package_seen: bool = False,
    ) -> Optional[tuple]:
        """Create entries for PyPI package version.

        The return value is a tuple. The first item in tuple is a flag signalizing if the given package was newly
        added ("existed" flag). The rest 3 touples are models representing python package, has version and
        python package version. If only seen flag is set to true, the return value can be None in case of
        package was not previously seen - in that case no action is done.
        """
        package_name = self.normalize_python_package_name(package_name)

        if only_if_package_seen and not self.python_package_version_exists(package_name, package_version, index_url):
            return None

        python_package = Package.from_properties(ecosystem="pypi", package_name=package_name)
        python_package.get_or_create(self.client)

        python_package_version = PythonPackageVersion.from_properties(
            ecosystem="pypi", package_name=package_name, package_version=package_version, index_url=index_url
        )
        existed = python_package_version.get_or_create(self.client)

        has_version = HasVersion.from_properties(source=python_package, target=python_package_version)
        has_version.get_or_create(self.client)

        for digest in hashes or []:
            python_artifact = PythonArtifact.from_properties(artifact_hash_sha256=digest)
            python_artifact.get_or_create(self.client)

            HasArtifact.from_properties(source=python_package_version, target=python_artifact).get_or_create(self.client)

        return existed, python_package, has_version, python_package_version

    @enable_vertex_cache
    def sync_solver_result(self, document: dict) -> None:
        """Sync the given solver result to the graph database."""
        solver_document_id = SolverResultsStore.get_document_id(document)
        solver_name = SolverResultsStore.get_solver_name_from_document_id(solver_document_id)
        solver_info = self.parse_python_solver_name(solver_name)

        # Construct errors first so that we have flag for edges.
        errors = {}
        for error_info in document["result"]["errors"]:
            package_name = error_info.get("package_name") or error_info["package"]
            package_version = error_info["version"]
            index_url = error_info["index"]

            if package_name not in errors:
                errors[package_name] = {}

            if package_version not in errors[package_name]:
                errors[package_name][package_version] = {}

            if index_url not in errors[package_name][package_version]:
                errors[package_name][package_version][index_url] = True

        ecosystem_solver = EcosystemSolver.from_properties(
            solver_name=solver_name,
            solver_version=document["metadata"]["analyzer_version"],
            os_name=solver_info["os_name"],
            os_version=solver_info["os_version"],
            python_version=solver_info["python_version"],
        )

        ecosystem_solver.get_or_create(self.client)
        solver_datetime = datetime_str2timestamp(document["metadata"]["datetime"])
        for python_package_info in document["result"]["tree"]:
            existed, python_package, _, python_package_version = self.create_pypi_package_version(
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
                os_name=solver_info["os_name"],
                os_version=solver_info["os_version"],
                python_version=solver_info["python_version"],
            ).get_or_create(self.client)

            for dependency in python_package_info["dependencies"]:
                for index_entry in dependency["resolved_versions"]:
                    index_url = index_entry["index"]
                    for dependency_version in index_entry["versions"]:
                        existed, python_package_dependency, _, python_package_version_dependency = self.create_pypi_package_version(  # Ignore PycodestyleBear (E501)
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
                            os_name=solver_info["os_name"],
                            os_version=solver_info["os_version"],
                            python_version=solver_info["python_version"],
                        ).get_or_create(self.client)

                        solver_error = (
                            errors.get(python_package_version_dependency.package_name, {})
                            .get(python_package_version_dependency.package_version, {})
                            .get(python_package_version_dependency.index_url, False)
                        )

                        # TODO: mark extras
                        DependsOn.from_properties(
                            source=python_package_version,
                            target=python_package_version_dependency,
                            package_name=python_package_version_dependency.package_name,
                            version_range=dependency["required_version"] or "*",
                            os_name=solver_info["os_name"],
                            os_version=solver_info["os_version"],
                            python_version=solver_info["python_version"],
                            solver_error=solver_error,
                        ).get_or_create(self.client)

        for error_info in document["result"]["errors"]:
            existed, python_package, _, python_package_version = self.create_pypi_package_version(
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
                os_name=solver_info["os_name"],
                os_version=solver_info["os_version"],
                python_version=solver_info["python_version"],
            ).get_or_create(self.client)

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

            package_version = unsolvable["version_spec"][len("=="):]
            existed, python_package, _, python_package_version = self.create_pypi_package_version(
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
                os_name=solver_info["os_name"],
                os_version=solver_info["os_version"],
                python_version=solver_info["python_version"],
            ).get_or_create(self.client)

        for unparsed in document["result"]["unparsed"]:
            parts = unparsed["requirement"].rsplit("==", maxsplit=1)
            if len(parts) != 2:
                # This request did not come from graph-refresh job as there is not pinned version.
                _LOGGER.warning(
                    f"Cannot sync unparsed package {unparsed} as package is not locked to as specific version"
                )
                continue

            package_name, package_version = parts
            existed, python_package, _, python_package_version = self.create_pypi_package_version(
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
                os_name=solver_info["os_name"],
                os_version=solver_info["os_version"],
                python_version=solver_info["python_version"],
            ).get_or_create(self.client)

    @enable_vertex_cache
    def sync_adviser_result(self, document: dict) -> None:
        """Sync adviser result into graph database."""
        adviser_document_id = AdvisersResultsStore.get_document_id(document)
        origin = (document["metadata"]["arguments"]["thoth-adviser"].get("metadata") or {}).get("origin")

        if not origin:
            _LOGGER.warning("No origin stated in the adviser result %r", adviser_document_id)

        user_software_stack = None
        if document["result"]["input"]["requirements_locked"]:
            # User provided a Pipfile.lock, we can sync it.
            user_software_stack = self.create_user_software_stack_pipfile(
                adviser_document_id, document["result"]["input"]["requirements_locked"], origin=origin
            )

        runtime_info = document["result"]["parameters"]["runtime_environment"]

        hardware_info = runtime_info.pop("hardware", {})
        hardware_information = HardwareInformation.from_properties(**hardware_info)
        hardware_information.get_or_create(self.client)

        operating_system = runtime_info.pop("operating_system", {})
        # TODO: we should derive name from image sha to have exact match.
        runtime_info.pop("name", None)  # We do not rely on user's input here, it can be anything...
        runtime_environment_name = (
            operating_system.get("name", "unknown") + ":" + operating_system.get("version", "unknown")
        )
        runtime_environment = RuntimeEnvironmentModel.from_properties(
            environment_name=runtime_environment_name,
            os_name=operating_system.get("name"),
            os_version=operating_system.get("version"),
            **runtime_info,
        )
        runtime_environment.get_or_create(self.client)

        RunsOn.from_properties(
            source=runtime_environment, target=hardware_information, document_id=adviser_document_id
        ).get_or_create(self.client)

        RunsIn.from_properties(
            source=user_software_stack, target=runtime_environment, document_id=adviser_document_id
        ).get_or_create(self.client)

        adviser_datetime = datetime_str2timestamp(document["metadata"]["datetime"])
        adviser_version = document["analyzer"]["version"]
        for idx, result in enumerate(document["result"]["report"]):
            if len(result) != 2:
                _LOGGER.debug("Omitting stack as no output Pipfile.lock was provided - was the report error report?")
                continue

            # result[0] is score report
            # result[1]["requirements"] is Pipfile
            # result[1]["requirements_locked"] is Pipfile.lock
            if result[1] and result[1].get("requirements_locked"):
                adviser_software_stack = self.create_adviser_software_stack_pipfile(
                    adviser_document_id, result[1]["requirements_locked"], adviser_stack_index=idx
                )

                # The linkage to hardware information is already done when user software stack was created.
                RunsIn.from_properties(
                    source=adviser_software_stack, target=runtime_environment, document_id=adviser_document_id
                ).get_or_create(self.client)

                if user_software_stack:
                    Advised.from_properties(
                        source=user_software_stack,
                        target=adviser_software_stack,
                        adviser_document_id=adviser_document_id,
                        adviser_version=adviser_version,
                        adviser_datetime=adviser_datetime,
                    ).get_or_create(self.client)

    @enable_vertex_cache
    def sync_provenance_checker_result(self, document: dict) -> None:
        """Sync provenance checker results into graph database."""
        provenance_checker_document_id = ProvenanceResultsStore.get_document_id(document)
        origin = (document["metadata"]["arguments"]["thoth-adviser"].get("metadata") or {}).get("origin")

        if not origin:
            _LOGGER.warning("No origin stated in the provenance-checker result %r", provenance_checker_document_id)

        user_input = document["result"]["input"]
        if user_input.get("requirements_locked"):
            self.create_user_software_stack_pipfile(
                provenance_checker_document_id, user_input["requirements_locked"], origin=origin
            )

    @staticmethod
    def _get_hardware_information(specs: dict) -> HardwareInformation:
        """Get hardware information based on requests provided."""
        hardware = specs.get("hardware") or {}
        ram_size = OpenShift.parse_memory_spec(specs["memory"]) if specs.get("memory") else None
        if ram_size is not None:
            # Convert bytes to GiB, we need float number for Gremlin/JanusGraph serialization
            ram_size = ram_size / (1024 ** 3)

        return HardwareInformation.from_properties(
            cpu_family=hardware.get("cpu_family"),
            cpu_model=hardware.get("cpu_model"),
            cpu_physical_cpus=hardware.get("physical_cpus"),
            cpu_model_name=hardware.get("processor"),
            cpu_cores=OpenShift.parse_cpu_spec(specs["cpu"]) if specs.get("cpu") else None,
            ram_size=ram_size,
        )

    @enable_vertex_cache
    def sync_inspection_result(self, document) -> None:
        """Sync the given inspection document into the graph database."""
        software_stack, python_version, os_name, os_version = None, None, None, None
        if document["specification"].get("python"):
            software_stack = self.create_inspection_software_stack_pipfile(
                document["inspection_id"], document["specification"]["python"]["requirements_locked"]
            )
            python_version = (
                document["specification"]["python"]["requirements"].get("requires", {}).get("python_version")
            )

        if ":" in document["specification"]["base"]:
            # TODO: we should capture os info in inspection report directly.
            os_name, os_version = document["specification"]["base"].split(":")

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

            runtime_environment = RuntimeEnvironmentModel.from_properties(
                environment_name=environment_name, python_version=python_version, os_name=os_name, os_version=os_version
            )
            runtime_environment.get_or_create(self.client)

            runtime_hardware = self._get_hardware_information(document["specification"]["run"]["requests"])
            runtime_hardware.get_or_create(self.client)

            run_error = document["status"]["job"]["exit_code"] == 0

            if software_stack:
                if performance_index is not None:
                    RunsIn.from_properties(
                        source=software_stack,
                        target=runtime_environment,
                        document_id=document["inspection_id"],
                        run_error=run_error,
                        performance_index=performance_index,
                    ).get_or_create(self.client)
                else:
                    # We cannot pass performance_index as None as goblin will complain.
                    RunsIn.from_properties(
                        source=software_stack,
                        target=runtime_environment,
                        document_id=document["inspection_id"],
                        run_error=run_error,
                    ).get_or_create(self.client)

            if performance_index is not None:
                RunsOn.from_properties(
                    source=runtime_environment,
                    target=runtime_hardware,
                    document_id=document["inspection_id"],
                    run_error=run_error,
                    performance_index=performance_index,
                ).get_or_create(self.client)
            else:
                RunsOn.from_properties(
                    source=runtime_environment,
                    target=runtime_hardware,
                    document_id=document["inspection_id"],
                    run_error=run_error,
                ).get_or_create(self.client)

        buildtime_environment = BuildtimeEnvironmentModel.from_properties(environment_name=environment_name)
        buildtime_environment.get_or_create(self.client)

        buildtime_hardware = self._get_hardware_information(document["specification"]["build"]["requests"])
        buildtime_hardware.get_or_create(self.client)

        build_error = document["status"]["build"]["exit_code"] == 0

        if software_stack:
            BuildsIn.from_properties(
                source=software_stack,
                target=buildtime_environment,
                document_id=document["inspection_id"],
                build_error=build_error,
            ).get_or_create(self.client)

        BuildsOn.from_properties(
            source=buildtime_environment,
            target=buildtime_hardware,
            document_id=document["inspection_id"],
            build_error=build_error,
        ).get_or_create(self.client)

    def _deb_sync_analysis_result(self, document_id: str, document: dict, environment: EnvironmentBase) -> None:
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
                deb_package_version.get_or_create(self.client)

                deb_package = Package.from_properties(
                    ecosystem=deb_package_version.ecosystem, package_name=deb_package_version.package_name
                )
                deb_package.get_or_create(self.client)

                HasVersion.from_properties(source=deb_package, target=deb_package_version).get_or_create(self.client)

                IsPartOf.from_properties(
                    source=deb_package_version,
                    target=environment,
                    analysis_datetime=datetime_str2timestamp(document["metadata"]["datetime"]),
                    analysis_document_id=document_id,
                    analyzer_name=document["metadata"]["analyzer"],
                    analyzer_version=document["metadata"]["analyzer_version"],
                ).get_or_create(self.client)

                # These three can be grouped with a zip, but that is not that readable...
                for pre_depends in deb_package_info.get("pre-depends") or []:
                    package = Package.from_properties(ecosystem="deb", package_name=pre_depends["name"])
                    package.get_or_create(self.client)

                    DebPreDepends.from_properties(
                        source=deb_package_version, target=package, version_range=pre_depends.get("version")
                    ).get_or_create(self.client)

                for depends in deb_package_info.get("depends") or []:
                    package = Package.from_properties(ecosystem="deb", package_name=depends["name"])
                    package.get_or_create(self.client)

                    DebDepends.from_properties(
                        source=deb_package_version, target=package, version_range=depends.get("version")
                    ).get_or_create(self.client)

                for replaces in deb_package_info.get("replaces") or []:
                    package = Package.from_properties(ecosystem="deb", package_name=replaces["name"])
                    package.get_or_create(self.client)

                    DebReplaces.from_properties(
                        source=deb_package_version, target=package, version_range=replaces.get("version")
                    ).get_or_create(self.client)
            except Exception:
                _LOGGER.exception("Failed to sync debian package, error is not fatal: %r", deb_package_info)

    def _rpm_sync_analysis_result(self, document_id: str, document: dict, environment: EnvironmentBase) -> None:
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
                rpm_package_version.get_or_create(self.client)

                rpm_package = Package.from_properties(
                    ecosystem=rpm_package_version.ecosystem, package_name=rpm_package_version.package_name
                )
                rpm_package.get_or_create(self.client)

                HasVersion.from_properties(source=rpm_package, target=rpm_package_version).get_or_create(self.client)

                IsPartOf.from_properties(
                    source=rpm_package_version,
                    target=environment,
                    analysis_datetime=datetime_str2timestamp(document["metadata"]["datetime"]),
                    analysis_document_id=document_id,
                    analyzer_name=document["metadata"]["analyzer"],
                    analyzer_version=document["metadata"]["analyzer_version"],
                ).get_or_create(self.client)

            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(f"Failed to sync RPM package, error is not fatal: {rpm_package_info!r}")
                continue

            for dependency in rpm_package_info["dependencies"]:
                try:
                    rpm_requirement = RPMRequirement.from_properties(rpm_requirement_name=dependency)
                    rpm_requirement.get_or_create(self.client)

                    Requires.from_properties(
                        source=rpm_package_version,
                        target=rpm_requirement,
                        analysis_datetime=datetime_str2timestamp(document["metadata"]["datetime"]),
                        analysis_document_id=document_id,
                        analyzer_name=document["metadata"]["analyzer"],
                        analyzer_version=document["metadata"]["analyzer_version"],
                    ).get_or_create(self.client)
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.exception(
                        f"Failed to sync dependencies for " f"RPM {rpm_package_version.to_dict()}: {dependency!r}"
                    )

    def _python_sync_analysis_result(self, document_id: str, document: dict, environment: EnvironmentBase) -> None:
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
                existed, python_package, _, python_package_version = self.create_pypi_package_version(
                    package_name=python_package_info["result"]["name"],
                    package_version=python_package_info["result"]["version"],
                    index_url=None,
                )

                IsPartOf.from_properties(
                    source=python_package_version,
                    target=environment,
                    analysis_datetime=datetime_str2timestamp(document["metadata"]["datetime"]),
                    analysis_document_id=document_id,
                    analyzer_name=document["metadata"]["analyzer"],
                    analyzer_version=document["metadata"]["analyzer_version"],
                ).get_or_create(self.client)
            except Exception:  # pylint: disable=broad-exception
                _LOGGER.exception(f"Failed to sync Python package, error is not fatal: {python_package_info!r}")

    @enable_vertex_cache
    def sync_analysis_result(self, document: dict) -> None:
        """Sync the given analysis result to the graph database."""
        environment_type = document["metadata"]["arguments"]["thoth-package-extract"]["metadata"]["environment_type"]
        # TODO: we should sync also origin of analysed images
        if environment_type == "runtime":
            environment = RuntimeEnvironmentModel.from_properties(
                environment_name=document["metadata"]["arguments"]["extract-image"]["image"]
            )
            environment.get_or_create(self.client)
        elif environment_type == "buildtime":
            environment = BuildtimeEnvironmentModel.from_properties(
                environment_name=document["metadata"]["arguments"]["extract-image"]["image"]
            )
            environment.get_or_create(self.client)
        else:
            raise ValueError("Unknown environment type %r, should be buildtime or runtime" % environment_type)

        document_id = AnalysisResultsStore.get_document_id(document)
        self._rpm_sync_analysis_result(document_id, document, environment)
        self._deb_sync_analysis_result(document_id, document, environment)
        self._python_sync_analysis_result(document_id, document, environment)

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
    ) -> Tuple[CVE, bool]:
        """Store information about a CVE in the graph database for the given Python package."""
        cve_record = CVE.from_properties(cve_id=record_id, version_range=version_range, advisory=advisory, cve_name=cve)
        cve_record_existed = cve_record.get_or_create(self.client)
        _LOGGER.debug("CVE record wit id %r ", record_id, "added" if not cve_record_existed else "was already present")

        # We explicitly track vulnerable packages (only_if_package_seen=False).
        existed, python_package, _, python_package_version = self.create_pypi_package_version(
            package_name, package_version, index_url=index_url, only_if_package_seen=False
        )

        has_vulnerability = HasVulnerability.from_properties(source=python_package_version, target=cve_record)
        has_vulnerability_existed = has_vulnerability.get_or_create(self.client)

        _LOGGER.debug(
            "CVE record %r for vulnerability of %r in version %r ",
            record_id,
            package_name,
            package_version,
            "added" if not has_vulnerability_existed else "was already present",
        )
        return cve_record, has_vulnerability_existed

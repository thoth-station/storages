#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2019 Francesco Murdaca, Fridolin Pokorny
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

"""An SQL database for storing Thoth data."""

import logging
import os
import json
import pkg_resources
import functools
from typing import List
from typing import Set
from typing import Tuple
from typing import Optional
from typing import Dict
from typing import Iterable
from typing import Union
from contextlib import contextmanager
from pathlib import Path
from dateutil import parser
from datetime import timezone
from itertools import chain
from collections import deque
import asyncio
from math import nan

import attr
from methodtools import lru_cache
# import grpc
# import pydgraph

from thoth.common import OpenShift
from thoth.common import RuntimeEnvironment as RuntimeEnvironmentConfig
from thoth.common import HardwareInformation as HardwareInformationConfig
from thoth.python import Pipfile
from thoth.python import PipfileLock
from thoth.python import PackageVersion

from ..base import StorageBase
# from .cache import GraphCache
# from .models_base import enable_vertex_cache
# from .models_base import VertexBase
# from .models import ALL_MODELS
# from .models import AdviserRun
# from .models import AdvisedSoftwareStack
# from .models import AdviserRunSoftwareEnvironmentInput
# from .models import AdviserStackInput
# from .models import Advised
# from .models import AnalyzedBy
# from .models import BuildSoftwareEnvironment as BuildSoftwareEnvironmentModel
# from .models import CreatesStack
# from .models import CVE
# from .models import DebDepends
# from .models import DebDependency
# from .models import DebPackageVersion
# from .models import DebPreDepends
# from .models import DebReplaces
# from .models import DependencyMonkeyRun
# from .models import DependencyMonkeyRunSoftwareEnvironmentInput
# from .models import DependsOn
# from .models import EcosystemSolverRun
# from .models import EnvironmentBase
# from .models import HardwareInformation as HardwareInformationModel
# from .models import UserHardwareInformation as UserHardwareInformationModel
# from .models import HasArtifact
# from .models import Investigated
# from .models import HasVulnerability
# from .models import Identified
# from .models import InspectionBuildSoftwareEnvironmentInput
# from .models import InspectionRun
# from .models import InspectionRunSoftwareEnvironmentInput
# from .models import InspectionSoftwareStack
# from .models import InspectionStackInput
# from .models import InstalledFrom
# from .models import PackageExtractRun
# from .models import PackageAnalyzerRun
# from .models import PythonFileDigest
# from .models import FoundFile
# from .models import PackageAnalyzerInput
# from .models import IncludedFile
# from .models import ProvenanceCheckerRun
# from .models import ProvenanceCheckerStackInput
# from .models import ProvidedBy
# from .models import PythonArtifact
# from .models import PythonPackageIndex
# from .models import PythonPackageRequirement
# from .models import PythonPackageVersion
# from .models import PythonPackageVersionEntity
# from .models import RequirementsInput
# from .models import Requires
# from .models import Resolved
# from .models import RPMPackageVersion
# from .models import RPMRequirement
# from .models import RunSoftwareEnvironment as RunSoftwareEnvironmentModel
# from .models import UserRunSoftwareEnvironment as UserRunSoftwareEnvironmentModel
# from .models import Solved
# from .models import SoftwareStackBase
# from .models import UsedIn
# from .models import UsedInBuild
# from .models import UsedInJob
# from .models import UserSoftwareStack
# from .performance import ObservedPerformance, PerformanceIndicatorBase
# from .performance import PERFORMANCE_MODEL_BY_NAME, ALL_PERFORMANCE_MODELS

from sqlalchemy import create_engine
from sqlalchemy_utils.functions import create_database
from sqlalchemy_utils.functions import database_exists
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from .sql_cache import GraphCache

from .sql_models import Base
from .sql_models import PythonPackageVersion
from .sql_models import Solved
from .sql_models import DependsOn
from .sql_models import PythonPackageVersionEntity
from .sql_models import AdvisedSoftwareStack
from .sql_models import EcosystemSolver
from .sql_models import PythonPackageRequirement
from .sql_models import CVE
from .sql_models import UserRunSoftwareEnvironmentModel
from .sql_models import SoftwareStackBase
from .sql_models import InspectionSoftwareStack
from .sql_models import UserSoftwareStack
from .sql_base import SQLBase
from .models_base import get_python_package_version_filter_kwargs
from .sql_cache import CacheMiss

from ..exceptions import NotFoundError
from ..exceptions import PythonIndexNotRegistered
from ..exceptions import PerformanceIndicatorNotRegistered
from ..exceptions import NotConnected
from ..advisers import AdvisersResultsStore
from ..analyses import AnalysisResultsStore
from ..package_analyses import PackageAnalysisResultsStore
from ..inspections import InspectionResultsStore
from ..provenance import ProvenanceResultsStore
from ..dependency_monkey_reports import DependencyMonkeyReportsStore
from ..solvers import SolverResultsStore

_LOGGER = logging.getLogger(__name__)


@attr.s()
class GraphDatabase(SQLBase):
    """A SQL datatabase adapter providing graph-like operations on top of SQL queires."""

    _cache = attr.ib(type=GraphCache, default=attr.Factory(GraphCache.load))

    _DECLARATIVE_BASE = Base

    @staticmethod
    def construct_connection_string() -> str:
        """Construct a connection string needed to connect to database."""
        connection_string = f"postgresql+psycopg2://" \
            f"{os.getenv('POSTGRESQL_USER', 'postgres')}:{os.getenv('POSTGRESQL_PASSWORD', 'postgres')}" \
            f"@{os.getenv('POSTGRESQL_SERVICE_HOST', 'localhost')}:{os.getenv('POSTGRESQL_SERVICE_PORT', 5432)}" \
            f"/{os.getenv('POSTGRESQL_DATABASE', 'thoth')}"

        if bool(int(os.getenv("POSTGRESQL_SSL_DISABLED", 0))):
            connection_string += "?sslmode=disable"

        return connection_string

    @property
    def cache(self) -> GraphCache:
        return self._cache

    def connect(self):
        """Connect to the database."""
        if self.is_connected():
            raise ValueError("Cannot connect, the adapter is already connected")

        echo = bool(int(os.getenv("THOTH_STORAGES_DEBUG_QUERIES", False)))
        self._engine = create_engine(self.construct_connection_string(), echo=echo)
        self._session = sessionmaker(bind=self._engine)()

    @staticmethod
    def normalize_python_package_name(package_name: str) -> str:
        """Normalize Python package name based on PEP-0503."""
        return PackageVersion.normalize_python_package_name(package_name)

    @staticmethod
    def parse_python_solver_name(solver_name: str) -> dict:
        """Parse os and Python identifiers encoded into solver name."""
        if solver_name.startswith("solver-"):
            solver_identifiers = solver_name[len("solver-"):]
        else:
            raise ValueError(f"Solver name has to start with 'solver-' prefix: {solver_name!r}")

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

    # --------------------------------- >% --------------------------------------

    def get_analysis_metadata(self, analysis_document_id: str) -> dict:
        """Get metadata stored for the given analysis document."""

    def run_software_environment_listing(
        self, start_offset: int = 0, count: int = 100, is_user_run: bool = False
    ) -> list:
        """Get listing of software environments available for run."""

    def build_software_environment_listing(self, start_offset: int = 0, count: int = 100) -> list:
        """Get listing of software environments available for build."""

    def run_software_environment_analyses_listing(
        self,
        run_software_environment_name: str,
        start_offset: int = 0,
        count: int = 100,
        convert_datetime: bool = True,
        is_user_run: bool = False,
    ) -> list:
        """Get listing of analyses available for the given software environment for run."""

    def build_software_environment_analyses_listing(
        self,
        build_software_environment_name: str,
        start_offset: int = 0,
        count: int = 100,
        convert_datetime: bool = True,
    ) -> list:
        """Get listing of analyses available for the given software environment for build."""

    def python_package_version_exists(
            self,
            package_name: str,
            package_version: str,
            index_url: str = None,
            solver_name: str = None
    ) -> bool:
        """Check if the given Python package version exists in the graph database.

        If optional solver_name parameter is set, the call answers if the given package was solved by
        the given solver. Otherwise, any solver run is taken into account.
        """

    def python_package_exists(self, package_name: str) -> bool:
        """Check if the given Python package exists regardless of version."""

    def compute_python_package_version_avg_performance(
        self, packages: Set[tuple], *, run_software_environment: dict = None, hardware_specs: dict = None
    ) -> float:
        """Get average performance of Python packages on the given runtime environment.

        # We derive this average performance based on software stacks we have
        # evaluated on the given software environment for run including the given
        # package in specified version. There are also included stacks that
        # failed for some reason that have negative performance impact on the overall value.

        # There are considered software stacks that include packages listed,
        # they can however include also other packages.

        # Optional parameters additionally slice results - e.g. if run_software_environment is set,
        # it picks only results that match the given parameters criteria.
        # """

    def has_python_solver_error(
        self,
        package_name: str,
        package_version: str,
        index_url: str,
        *,
        os_name: str,
        os_version: str,
        python_version: str,
    ) -> bool:
        """Retrieve information whether the given package has any solver error."""

    def get_all_versions_python_package(
        self,
        package_name: str,
        index_url: str = None,
        *,
        only_known_index: bool = False,  # Respect this one.
        os_name: str = None,
        os_version: str = None,
        python_version: str = None,
        without_error: bool = True,
        only_solved: bool = False,  # TODO: Drop this one.
    ) -> List[Tuple[str, str]]:
        """Get all versions available for a Python package."""
        filter_kwargs = get_python_package_version_filter_kwargs(
            package_name=package_name,
            package_version=None,
            index_url=index_url,
            os_name=os_name,
            os_version=os_version,
            python_version=python_version,
        )

        if without_error is False:
            result = self._session.query(
                PythonPackageVersion.package_version,
                PythonPackageVersion.index_url,
            ).filter_by(**filter_kwargs).all()
        else:
            result = self._session.query(
                PythonPackageVersion.package_version, PythonPackageVersion.index_url
            ).filter_by(**filter_kwargs).join(Solved).filter(Solved.solver_error.is_(False)).all()

        return result

    def retrieve_unsolved_python_packages(self, solver_name: str) -> dict:
        """Retrieve a dictionary mapping package names to versions that dependencies were not yet resolved.

        Using solver_name argument the query narrows down to packages that were not resolved by the given solver.
        """

    def retrieve_unsolved_python_packages_count(self, solver_name: str) -> int:
        """Retrieve number of unsolved Python packages for the given solver."""

    def retrieve_solved_python_packages_count(self, solver_name: str) -> int:
        """Retrieve number of solved Python packages for the given solver."""

    def retrieve_unanalyzed_python_package_versions(self, start_offset: int = 0, count: int = 100) -> List[dict]:
        """Retrieve a list of package names, versions and index urls that were not analyzed yet by package-analyzer."""

    def retrieve_solved_python_packages(self, count: int = 10, start_offset: int = 0, solver_name: str = None) -> dict:
        """Retrieve a dictionary mapping package names to versions for dependencies that were already solved.

        Using count and start_offset is possible to change pagination.
        Using solver_name argument the query narrows down to packages that were resolved by the given solver.
        """

    def retrieve_unsolvable_python_packages(self, solver_name: str = None) -> dict:
        """Retrieve a dictionary mapping package names to versions of packages that were marked as unsolvable."""

    def retrieve_unsolvable_python_packages_per_run_software_environment(self, solver_name: str) -> dict:
        """Retrieve a dictionary mapping package names to versions of packages that were marked as unsolvable.

        The result is given for a specific run software environment (OS + python version)
        """

    def retrieve_document_list_of_unsolvable_python_packages(self) -> list:
        """Retrieve a dictionary mapping package names to versions of packages that were marked as unsolvable."""

    def retrieve_unparseable_python_packages(self) -> dict:
        """Retrieve a dictionary mapping package names to versions of packages that couldn't be parsed by solver."""

    def get_all_python_packages_count(self, without_error: bool = True) -> int:
        """Retrieve number of Python packages stored in the graph database."""

    def get_error_python_packages_count(self, *, unsolvable: bool = False, unparseable: bool = False) -> int:
        """Retrieve number of Python packages stored in the graph database with error flag."""

    def get_solver_documents_count(self) -> int:
        """Get number of solver documents synced into graph."""

    def get_analyzer_documents_count(self) -> int:
        """Get number of image analysis documents synced into graph."""

    def retrieve_dependent_packages(self, package_name: str) -> dict:
        """Get mapping package name to package version of packages that depend on the given package."""

    async def get_python_package_tuple(self, python_package_node_id: int) -> Dict[int, tuple]:
        """Get Python's package name, package version, package index tuple for the given package id."""

    def _get_python_package_version_by_uid(self, uid: int, *, without_cache: bool = False) -> Optional[dict]:
        """Get Python package version information for the given uid."""

    @lru_cache(maxsize=16384)
    def get_python_package_version_records(
        self,
        package_name: str,
        package_version: str,
        index_url: Union[str, None],
        *,
        os_name: Union[str, None],
        os_version: Union[str, None],
        python_version: Union[str, None],
        without_cache: bool = False,
    ) -> List[dict]:
        """Get records for the given package regardless of index_url."""
        if not without_cache:
            try:
                return self._cache.get_python_package_version_records(
                    package_name=package_name,
                    package_version=package_version,
                    index_url=index_url,
                    os_name=os_name,
                    os_version=os_version,
                    python_version=python_version,
                )
            except CacheMiss:
                pass

        filter_kwargs = get_python_package_version_filter_kwargs(
            package_name=package_name,
            package_version=package_version,
            index_url=index_url,
            os_name=os_name,
            os_version=os_version,
            python_version=python_version,
        )

        query_result = self._session.query(
            PythonPackageVersion.package_name,
            PythonPackageVersion.package_version,
            PythonPackageVersion.index_url,
            PythonPackageVersion.os_name,
            PythonPackageVersion.os_version,
            PythonPackageVersion.python_version,
        ).filter_by(**filter_kwargs).all()

        result = []
        for item in query_result:
            result.append({
                "package_name": item[0],
                "package_version": item[1],
                "index_url": item[2],
                "os_name": item[3],
                "os_version": item[4],
                "python_version": item[5],
            })

        return result

    def retrieve_transitive_dependencies_python(
        self,
        package_name: str,
        package_version: str,
        index_url: str,
        *,
        os_name: str = None,
        os_version: str = None,
        python_version: str = None,
        without_cache: bool = False,
    ) -> List[
        Tuple[
            Tuple[str, str, str], Tuple[str, str, str], Tuple[str, str, str],
            Tuple[str, str, str], Union[Tuple[str, str, str], None], Union[Tuple[str, str, str], None]
        ]
    ]:
        """Get all transitive dependencies for the given package by traversing dependency graph.

        It's much faster to retrieve just dependency ids for the transitive
        dependencies as most of the time is otherwise spent in serialization
        and deserialization of query results. The ids are obtained later on (kept in ids map, see bellow).

        The ids map represents a map to optimize number of retrievals - not to perform duplicate
        queries into graph instance.
        """
        package_name = self.normalize_python_package_name(package_name)
        result = []
        package_tuple = (package_name, package_version, index_url)
        stack = deque((package_tuple,))
        seen_tuples = {package_tuple}
        while stack:
            package_tuple = stack.pop()

            configurations = self.get_python_package_version_records(
                package_name=package_tuple[0],
                package_version=package_tuple[1],
                index_url=package_tuple[2],
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
                without_cache=without_cache,
            )

            for configuration in configurations:
                dependencies = self.get_depends_on(
                    package_name=configuration["package_name"],
                    package_version=configuration["package_version"],
                    index_url=configuration["index_url"],
                    os_name=configuration["os_name"],
                    os_version=configuration["os_version"],
                    python_version=configuration["python_version"],
                    without_cache=without_cache,
                )

                for dependency_name, dependency_version in dependencies:
                    records = self.get_python_package_version_records(
                        package_name=dependency_name,
                        package_version=dependency_version,
                        index_url=None,  # Do cross-index resolution...
                        os_name=configuration["os_name"],
                        os_version=configuration["os_version"],
                        python_version=configuration["python_version"],
                        without_cache=without_cache,
                    )

                    if records is None:
                        # Not resolved yet.
                        result.append((
                            package_tuple,
                            (dependency_name, dependency_version, None),
                        ))
                    else:
                        for record in records:
                            dependency_tuple = (record["package_name"], record["package_version"], record["index_url"])
                            result.append((package_tuple, dependency_tuple))

                            if dependency_tuple not in seen_tuples:
                                stack.append(dependency_tuple)
                                seen_tuples.add(dependency_tuple)

        return result

    @lru_cache(maxsize=8192)
    def get_depends_on(
        self,
        package_name: str,
        package_version: str,
        index_url: str,
        *,
        os_name: str = None,
        os_version: str = None,
        python_version: str = None,
        without_cache: bool = False,
    ) -> List[Tuple[str, str]]:
        """Get dependencies for the given Python package respecting environment.

        If no environment is provided, dependencies are returned for all environments as stored in the database.
        """
        filter_kwargs = get_python_package_version_filter_kwargs(
            package_name=package_name,
            package_version=package_version,
            index_url=index_url,
            os_name=os_name,
            os_version=os_version,
            python_version=python_version,
        )

        if not without_cache:
            try:
                return self._cache.get_depends_on(
                    package_name=package_name,
                    package_version=package_version,
                    index_url=index_url,
                    os_name=os_name,
                    os_version=os_version,
                    python_version=python_version,
                )
            except CacheMiss:
                pass

        dependencies = self._session.query(
            PythonPackageVersionEntity.package_name,
            PythonPackageVersionEntity.package_version,
        ).filter(PythonPackageVersionEntity.package_version.isnot(None)) \
            .join(DependsOn).join(PythonPackageVersion).filter_by(**filter_kwargs).all()

        if not without_cache:
            if not dependencies:
                if self._session.query(PythonPackageVersion).filter_by(**filter_kwargs).count() == 0:
                    raise ValueError("No package record for %r found", filter_kwargs)

                self._cache.add_depends_on(
                    package_name=package_name,
                    package_version=package_version,
                    index_url=index_url,
                    os_name=os_name,
                    os_version=os_version,
                    python_version=python_version,
                    dependency_name=None,
                    dependency_version=None,
                )
            else:
                for dependency in dependencies:
                    self._cache.add_depends_on(
                        package_name=package_name,
                        package_version=package_version,
                        index_url=index_url,
                        os_name=os_name,
                        os_version=os_version,
                        python_version=python_version,
                        dependency_name=dependency[0],
                        dependency_version=dependency[1],
                    )

        return dependencies

    def retrieve_transitive_dependencies_python_multi(
        self,
        *package_tuples,
        os_name: str = None,
        os_version: str = None,
        python_version: str = None,
        without_cache: bool = False,
    ) -> Dict[
        Tuple[str, str, str],
        Set[
            Tuple[
                Tuple[str, str, str], Tuple[str, str, str], Tuple[str, str, str],
                Tuple[str, str, str], Union[Tuple[str, str, str], None], Union[Tuple[str, str, str], None]
            ]
        ]
    ]:
        """Get all transitive dependencies for a given set of packages by traversing the dependency graph."""
        result = {}
        _LOGGER.warning(len(package_tuples))
        for package_tuple in package_tuples:
            _LOGGER.warning(package_tuple)
            from pprint import pprint
            pprint(self.stats())
            result[package_tuple] = self.retrieve_transitive_dependencies_python(
                *package_tuple,
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
                without_cache=without_cache,
            )

        return result

    def solver_records_exist(self, solver_document: dict) -> bool:
        """Check if the given solver document record exists."""

    def solver_document_id_exist(self, solver_document_id: str) -> bool:
        """Check if there is a solver document record with the given id."""

    def dependency_monkey_document_id_exist(self, dependency_monkey_document_id: str) -> bool:
        """Check if the given dependency monkey report record exists in the graph database."""

    def adviser_document_id_exist(self, adviser_document_id: str) -> bool:
        """Check if there is a adviser document record with the given id."""

    def analysis_records_exist(self, analysis_document: dict) -> bool:
        """Check whether the given analysis document records exist in the graph database."""

    def analysis_document_id_exist(self, analysis_document_id: str) -> bool:
        """Check if there is an analysis document record with the given id."""

    def package_analysis_document_id_exist(self, package_analysis_document_id: str) -> bool:
        """Check if there is a package analysis document record with the given id."""

    def inspection_document_id_exist(self, inspection_document_id: str) -> bool:
        """Check if there is an inspection document record with the given id."""

    def provenance_checker_document_id_exist(self, provenance_checker_document_id: str) -> bool:
        """Check if there is a provenance-checker document record with the given id."""

    def get_python_cve_records(self, package_name: str, package_version: str) -> List[dict]:
        """Get known vulnerabilities for the given package-version."""

    def get_python_package_version_hashes_sha256(
        self, package_name: str, package_version: str, index_url: str
    ) -> List[str]:
        """Get hashes for a Python package in specified version."""

    def get_all_python_package_version_hashes_sha256(self, package_name: str, package_version: str) -> list:
        """Get hashes for a Python package per index."""

    def register_python_package_index(self, url: str, warehouse_api_url: str = None, verify_ssl: bool = True) -> bool:
        """Register the given Python package index in the graph database."""

    def python_package_index_listing(self) -> list:
        """Get listing of Python package indexes registered in the graph database database."""

    def get_python_package_index_urls(self) -> set:
        """Retrieve all the URLs of registered Python package indexes."""

    def get_python_packages_for_index(self, index_url: str) -> Set[str]:
        """Retrieve listing of Python packages known to graph database instance for the given index."""

    def get_python_packages(self) -> Set[str]:
        """Retrieve listing of all Python packages known to graph database instance."""

    def _python_packages_create_stack(
        self, python_package_versions: Iterable[PythonPackageVersion], software_stack: SoftwareStackBase
    ) -> None:
        """Assign the given set of packages to the stack."""

    def _create_python_package_record(
        self, python_package_version: PythonPackageVersion, verify_index: bool = True
    ) -> None:
        """Create a record for the given Python package.

        @raises PythonIndexNotRegistered: if there is no index registered from which the Python version came.
        """

    def create_python_package_version_entity(
        self,
        package_name: str,
        package_version: str,
        index_url: str,
        *,
        only_if_package_seen: bool = False,
    ) -> Optional[Tuple[PythonPackageVersionEntity, bool]]:
        """Create a Python package version entity in the graph database."""

    def create_python_packages_pipfile(
        self, pipfile_locked: dict, run_software_environment: UserRunSoftwareEnvironmentModel = None
    ) -> List[PythonPackageVersion]:
        """Create Python packages from Pipfile.lock entries and return them."""

    def create_user_software_stack_pipfile(
        self,
        adviser_document_id: str,
        pipfile_locked: dict,
        run_software_environment: UserRunSoftwareEnvironmentModel = None,
    ) -> UserSoftwareStack:
        """Create a user software stack entry from Pipfile.lock."""

    def create_python_package_requirement(self, requirements: dict) -> List[PythonPackageRequirement]:
        """Create requirements for un-pinned Python packages."""

    def create_inspection_software_stack_pipfile(
        self, document_id: str, pipfile_locked: dict
    ) -> InspectionSoftwareStack:
        """Create an inspection software stack entry from Pipfile.lock."""

    def create_advised_software_stack_pipfile(
        self,
        adviser_document_id: str,
        pipfile_locked: dict,
        *,
        advised_stack_index: int,
        performance_score: float,
        overall_score: float,
        run_software_environment: UserRunSoftwareEnvironmentModel,
    ) -> AdvisedSoftwareStack:
        """Create an advised software stack entry from Pipfile.lock."""

    def sync_inspection_result(self, document) -> None:
        """Sync the given inspection document into the graph database."""

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

    def sync_analysis_result(self, document: dict) -> None:
        """Sync the given analysis result to the graph database."""

    def sync_package_analysis_result(self, document: dict) -> None:
        """Sync the given package analysis result to the graph database."""

    def sync_solver_result(self, document: dict) -> None:
        """Sync the given solver result to the graph database."""
        solver_document_id = SolverResultsStore.get_document_id(document)
        solver_name = SolverResultsStore.get_solver_name_from_document_id(solver_document_id)
        solver_info = self.parse_python_solver_name(solver_name)
        solver_datetime = document["metadata"]["datetime"]
        solver_version = document["metadata"]["analyzer_version"]
        os_name = solver_info["os_name"]
        os_version = solver_info["os_version"]
        python_version = solver_info["python_version"]

        try:
            with self._session.begin(subtransactions=True):
                ecosystem_solver, _ = EcosystemSolver.get_or_create(
                    self._session,
                    ecosystem="python",
                    solver_name=solver_name,
                    solver_version=solver_version,
                    os_name=os_name,
                    os_version=os_version,
                    python_version=python_version,
                )

                for python_package_info in document["result"]["tree"]:
                    package_name = python_package_info["package_name"]
                    package_version = python_package_info["package_version"]
                    index_url = python_package_info["index_url"]

                    python_package_version, _ = PythonPackageVersion.get_or_create(
                        self._session,
                        package_name=self.normalize_python_package_name(package_name),
                        package_version=package_version,
                        index_url=index_url,
                        os_name=ecosystem_solver.os_name,
                        os_version=ecosystem_solver.os_version,
                        python_version=ecosystem_solver.python_version,
                    )

                    solved, _ = Solved.get_or_create(
                        self._session,
                        datetime=solver_datetime,
                        document_id=solver_document_id,
                        version=python_package_version,
                        ecosystem_solver=ecosystem_solver,
                        duration=None,
                        solver_error=False,
                        solver_error_unparseable=False,
                        solver_error_unsolvable=False,
                    )

                    # TODO: detect and store extras
                    # TODO: detect and store markers
                    for dependency in python_package_info["dependencies"]:
                        for index_entry in dependency["resolved_versions"]:
                            for dependency_version in index_entry["versions"]:
                                dependency_entity, _ = PythonPackageVersionEntity.get_or_create(
                                    self._session,
                                    package_name=self.normalize_python_package_name(dependency["package_name"]),
                                    package_version=dependency_version,
                                )

                                DependsOn.get_or_create(
                                    self._session,
                                    version=python_package_version,
                                    entity=dependency_entity,
                                    version_range=dependency.get("required_version") or "*",
                                )

            for error_info in document["result"]["errors"]:
                package_name = error_info.get("package_name") or error_info["package"]
                package_version = error_info["version"]
                index_url = error_info["index"]

                python_package_version, _ = PythonPackageVersion.get_or_create(
                    self._session,
                    package_name=self.normalize_python_package_name(package_name),
                    package_version=package_version,
                    index_url=index_url,
                    os_name=ecosystem_solver.os_name,
                    os_version=ecosystem_solver.os_version,
                    python_version=ecosystem_solver.python_version,
                )

                solved, _ = Solved.get_or_create(
                    self._session,
                    datetime=solver_datetime,
                    document_id=solver_document_id,
                    version=python_package_version,
                    ecosystem_solver=ecosystem_solver,
                    duration=None,
                    solver_error=True,
                    solver_error_unparseable=False,
                    solver_error_unsolvable=False,
                    is_provided=error_info.get("is_provided"),
                )

            for unsolvable in document["result"]["unresolved"]:
                if not unsolvable["version_spec"].startswith("=="):
                    # No resolution can be perfomed so no identifier is captured, report warning and continue.
                    # We would like to capture this especially when there are
                    # packages in ecosystem that we cannot find (e.g. not configured private index
                    # or removed package).
                    _LOGGER.warning(
                        "Cannot sync unsolvable package %r as package is not locked to as specific version", unsolvable
                    )
                    continue

                package_name = unsolvable["package_name"]
                index_url = unsolvable["index"]
                package_version = unsolvable["version_spec"][len("=="):]

                python_package_version, _ = PythonPackageVersion.get_or_create(
                    self._session,
                    package_name=self.normalize_python_package_name(package_name),
                    package_version=package_version,
                    index_url=index_url,
                    os_name=ecosystem_solver.os_name,
                    os_version=ecosystem_solver.os_version,
                    python_version=ecosystem_solver.python_version,
                )

                solved, _ = Solved.get_or_create(
                    self._session,
                    datetime=solver_datetime,
                    document_id=solver_document_id,
                    version=python_package_version,
                    ecosystem_solver=ecosystem_solver,
                    duration=None,
                    solver_error=True,
                    solver_error_unparseable=False,
                    solver_error_unsolvable=True,
                )

            for unparsed in document["result"]["unparsed"]:
                parts = unparsed["requirement"].rsplit("==", maxsplit=1)
                if len(parts) != 2:
                    # This request did not come from graph-refresh job as there is not pinned version.
                    _LOGGER.warning(
                        "Cannot sync unparsed package %r as package is not locked to as specific version", unparsed
                    )
                    continue

                package_name, package_version = parts
                python_package_version, _ = PythonPackageVersion.get_or_create(
                    self._session,
                    package_name=self.normalize_python_package_name(package_name),
                    package_version=package_version,
                    index_url=None,
                    os_name=ecosystem_solver.os_name,
                    os_version=ecosystem_solver.os_version,
                    python_version=ecosystem_solver.python_version,
                )

                solved, _ = Solved.get_or_create(
                    self._session,
                    datetime=solver_datetime,
                    document_id=solver_document_id,
                    version=python_package_version,
                    ecosystem_solver=ecosystem_solver,
                    duration=None,
                    solver_error=True,
                    solver_error_unparseable=True,
                    solver_error_unsolvable=False,
                )
        except Exception:
            self._session.rollback()
            raise
        else:
            self._session.commit()

    def sync_adviser_result(self, document: dict) -> None:
        """Sync adviser result into graph database."""

    def sync_provenance_checker_result(self, document: dict) -> None:
        """Sync provenance checker results into graph database."""

    def sync_dependency_monkey_result(self, document: dict) -> None:
        """Sync reports of dependency monkey runs."""

    def get_number_of_each_vertex_in_graph(self) -> dict:
        """Retrieve dictionary with number of vertices per vertex label in the graph database."""

    def get_all_pi_per_framework_count(self, framework: str) -> dict:
        """Retrieve dictionary with number of Performance Indicators per ML Framework in the graph database."""

    def stats(self) -> dict:
        """Get statistics for this adapter."""
        stats = self._cache.stats()
        stats["memory_cache_info"] = {}

        # We need to provide name explicitly as wrappers do not handle it correctly.
        for method, method_name in (
            (self.get_python_package_version_records, "get_python_package_version_records"),
            (self.get_depends_on, "get_depends_on"),
        ):
            stats["memory_cache_info"][method_name] = dict(method.cache_info()._asdict())

        return stats


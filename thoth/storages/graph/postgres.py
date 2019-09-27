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
import json
import os
from typing import List
from typing import Set
from typing import Tuple
from typing import Optional
from typing import Dict
from typing import Union
from collections import deque

import attr
from methodtools import lru_cache
from alembic.config import main as alembic_main
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import tuple_
from sqlalchemy.orm import Query
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.pool import NullPool
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils.functions import create_database
from sqlalchemy_utils.functions import database_exists
from thoth.python import PackageVersion
from thoth.python import Pipfile
from thoth.python import PipfileLock
from thoth.common.helpers import format_datetime
from thoth.common.helpers import cwd
from thoth.common import OpenShift

from .cache import GraphCache
from .models import PythonPackageVersion
from .models import SoftwareEnvironment
from .models import PythonPackageIndex
from .models import PythonArtifact
from .models import Investigated
from .models import DependencyMonkeyRun
from .models import AdviserRun
from .models import HardwareInformation
from .models import HasArtifact
from .models import Solved
from .models import PythonSoftwareStack
from .models import PythonRequirements
from .models import PythonRequirementsLock
from .models import DependsOn
from .models import PythonPackageVersionEntity
from .models import HasVulnerability
from .models import PackageExtractRun
from .models import PackageAnalyzerRun
from .models import ProvenanceCheckerRun
from .models import InspectionRun
from .models import EcosystemSolver
from .models import PythonPackageRequirement
from .models import PythonDependencyMonkeyRequirements
from .models import RPMRequirement
from .models import RPMPackageVersion
from .models import DebReplaces
from .models import DebPackageVersion
from .models import FoundDeb
from .models import DebDependency
from .models import DebDepends
from .models import DebPreDepends
from .models import RPMRequires
from .models import Identified
from .models import PythonFileDigest
from .models import FoundPythonFile
from .models import FoundRPM
from .models import Advised
from .models import VersionedSymbol
from .models import RequiresSymbol
from .models import IncludedFile
from .models import InvestigatedFile
from .models import HasSymbol
from .models import DetectedSymbol
from .models import CVE
from .models import ALL_MAIN_MODELS, ALL_RELATION_MODELS
from .models_performance import PiMatmul
from .models_performance import ALL_PERFORMANCE_MODELS, PERFORMANCE_MODEL_BY_NAME
from collections import Counter

from .sql_base import SQLBase
from .models_base import Base

from ..analyses import AnalysisResultsStore
from ..dependency_monkey_reports import DependencyMonkeyReportsStore
from ..provenance import ProvenanceResultsStore
from ..inspections import InspectionResultsStore
from ..solvers import SolverResultsStore
from ..advisers import AdvisersResultsStore
from ..package_analyses import PackageAnalysisResultsStore
from ..exceptions import NotFoundError
from ..exceptions import PythonIndexNotRegistered
from ..exceptions import PerformanceIndicatorNotRegistered

_LOGGER = logging.getLogger(__name__)


@attr.s()
class GraphDatabase(SQLBase):
    """A SQL database adapter providing graph-like operations on top of SQL queries."""

    _cache = attr.ib(type=GraphCache, default=attr.Factory(GraphCache.load))

    _DECLARATIVE_BASE = Base

    def __del__(self) -> None:
        """Destruct adapter object."""
        if int(bool(os.getenv("THOTH_STORAGES_LOG_STATS", 0))):
            stats = self.stats()
            _LOGGER.info("Graph adapter statistics:\n%s", json.dumps(stats, indent=2))

        super().__del__()

    @staticmethod
    def construct_connection_string() -> str:
        """Construct a connection string needed to connect to database."""
        connection_string = (
            f"postgresql+psycopg2://"
            f"{os.getenv('KNOWLEDGE_GRAPH_USER', 'postgres')}:{os.getenv('KNOWLEDGE_GRAPH_PASSWORD', 'postgres')}"
            f"@{os.getenv('KNOWLEDGE_GRAPH_HOST', 'localhost')}:{os.getenv('KNOWLEDGE_GRAPH_PORT', 5432)}"
            f"/{os.getenv('KNOWLEDGE_GRAPH_DATABASE', 'postgres')}"
        )

        if bool(int(os.getenv("KNOWLEDGE_GRAPH_SSL_DISABLED", 0))):
            connection_string += "?sslmode=disable"

        return connection_string

    @property
    def cache(self) -> GraphCache:
        """Get cache for this instance."""
        return self._cache

    def connect(self):
        """Connect to the database."""
        if self.is_connected():
            raise ValueError("Cannot connect, the adapter is already connected")

        echo = bool(int(os.getenv("THOTH_STORAGES_DEBUG_QUERIES", 0)))
        # We do not use connection pool, but directly talk to the database.
        self._engine = create_engine(self.construct_connection_string(), echo=echo, poolclass=NullPool)
        self._session = sessionmaker(bind=self._engine)()

    def initialize_schema(self):
        """Initialize schema of database."""
        import thoth.storages
        from alembic import config
        from alembic import command

        if not self.is_connected():
            raise ValueError("Cannot initialize schema: the adapter is not connected yet")

        if not database_exists(self._engine.url):
            create_database(self._engine.url)

        # Change directory to data dir as that's where alembic configuration sits in and refers revisions.
        with cwd(os.path.join(os.path.dirname(thoth.storages.__file__), "data")):
            alembic_cfg = config.Config("alembic.ini")
            # Overwrite URL based on deployment configuration.
            alembic_cfg.set_main_option('sqlalchemy.url', self.construct_connection_string())
            command.upgrade(alembic_cfg, "head")

    def drop_all(self):
        """Drop all content stored in the database."""
        super().drop_all()
        # Drop alembic version to be able re-run alembic migrations next time.
        self._engine.execute("DROP TABLE alembic_version;")

    def is_schema_up2date(self) -> bool:
        """Check if the current schema is up2date with the one configured on database side."""
        import thoth.storages
        from alembic import config
        from alembic import script
        from alembic.runtime import migration

        if not self.is_connected():
            raise ValueError("Cannot check schema: the adapter is not connected yet")

        with cwd(os.path.join(os.path.dirname(thoth.storages.__file__), "data")):
            alembic_cfg = config.Config("alembic.ini")
            directory = script.ScriptDirectory.from_config(alembic_cfg)
            context = migration.MigrationContext.configure(self._engine)

            database_heads = set(context.get_current_heads())
            if not database_heads:
                raise ValueError("Database is not initialized yet")

            revision_heads = set(directory.get_heads())

            _LOGGER.debug("Current library revision heads: %r", revision_heads)
            _LOGGER.debug("Current database heads: %r", database_heads)
            return revision_heads == revision_heads

    @staticmethod
    def normalize_python_package_name(package_name: str) -> str:
        """Normalize Python package name based on PEP-0503."""
        return PackageVersion.normalize_python_package_name(package_name)

    @staticmethod
    def normalize_python_package_version(package_version: str) -> str:
        """Normalize Python package name based on PEP-440."""
        return PackageVersion.normalize_python_package_version(package_version)

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

    def get_analysis_metadata(self, analysis_document_id: str) -> dict:
        """Get metadata stored for the given analysis document."""
        query = (
            self._session.query(PackageExtractRun)
            .filter(PackageExtractRun.analysis_document_id == analysis_document_id)
            .with_entities(
                PackageExtractRun.datetime,
                PackageExtractRun.analysis_document_id,
                PackageExtractRun.package_extract_name,
                PackageExtractRun.package_extract_version
            )
        )
        query_result = query.fetch()

        if query_result is None:
            raise NotFoundError(f"No records found for analysis with id {analysis_document_id!r}")

        return {
            "analysis_datetime": query_result[0],
            "analysis_document_id": query_result[1],
            "package_extract_name": query_result[2],
            "package_extract_version": query_result[3],
        }

    def _do_software_environment_listing(
        self, start_offset: int, count: int, is_user_run: bool, environment_type: str
    ) -> List[str]:
        """Perform actual query to software environments."""
        query = (
            self._session.query(SoftwareEnvironment.environment_name)
            .filter(SoftwareEnvironment.is_user == is_user_run)
            .filter(SoftwareEnvironment.environment_type == environment_type)
            .offset(start_offset)
            .limit(count)
        )

        return [item[0] for item in query.all()]

    def run_software_environment_listing(
        self, start_offset: int = 0, count: int = 100, is_user_run: bool = False
    ) -> list:
        """Get listing of software environments available for run."""
        return self._do_software_environment_listing(start_offset, count, is_user_run, "RUNTIME")

    def build_software_environment_listing(self, start_offset: int = 0, count: int = 100) -> list:
        """Get listing of software environments available for build."""
        # We do not have user software environment which is build environment yet.
        return self._do_software_environment_listing(start_offset, count, False, "BUILDTIME")

    def _do_software_environment_analyses_listing(
        self,
        software_environment_name: str,
        start_offset: int,
        count: int,
        convert_datetime: bool,
        is_user_run: bool,
        environment_type: str,
    ) -> List[dict]:
        """Get listing of available software environment analyses."""
        query_result = (
            self._session.query(SoftwareEnvironment)
            .filter(SoftwareEnvironment.software_environment_type == environment_type)
            .filter(SoftwareEnvironment.environment_name == software_environment_name)
            .filter(SoftwareEnvironment.is_user_run == is_user_run)
            .join(PackageExtractRun)
            .with_entities(
                PackageExtractRun.datetime,
                PackageExtractRun.analysis_document_id,
                PackageExtractRun.package_extract_name,
                PackageExtractRun.package_extract_version,
            )
            .offset(start_offset)
            .limit(count)
            .all()
        )

        result = []
        for item in query_result:
            result.append({
                "analysis_datetime": item[0] if not convert_datetime else format_datetime(item[0]),
                "analysis_document_id": item[1],
                "package_extract_name": item[2],
                "package_extract_version": item[3]
            })

        return result

    def run_software_environment_analyses_listing(
        self,
        run_software_environment_name: str,
        start_offset: int = 0,
        count: int = 100,
        convert_datetime: bool = True,
        is_user_run: bool = False,
    ) -> List[dict]:
        """Get listing of analyses available for the given software environment for run."""
        return self._do_software_environment_analyses_listing(
            run_software_environment_name,
            start_offset=start_offset,
            count=count,
            is_user_run=is_user_run,
            convert_datetime=convert_datetime,
            environment_type="RUNTIME",
        )

    def build_software_environment_analyses_listing(
        self,
        build_software_environment_name: str,
        start_offset: int = 0,
        count: int = 100,
        convert_datetime: bool = True,
        is_user_run: bool = False,
    ) -> List[dict]:
        """Get listing of analyses available for the given software environment for build."""
        return self._do_software_environment_analyses_listing(
            build_software_environment_name,
            start_offset=start_offset,
            count=count,
            is_user_run=is_user_run,
            convert_datetime=convert_datetime,
            environment_type="BUILDTIME",
        )

    def python_package_version_exists(
        self, package_name: str, package_version: str, index_url: str = None, solver_name: str = None
    ) -> bool:
        """Check if the given Python package version exists in the graph database.

        If optional solver_name parameter is set, the call answers if the given package was solved by
        the given solver. Otherwise, any solver run is taken into account.
        """
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)
        query = (
            self._session.query(PythonPackageVersion)
            .filter(PythonPackageVersion.package_name == package_name)
            .filter(PythonPackageVersion.package_version == package_version)
        )

        if solver_name:
            solver_info = self.parse_python_solver_name(solver_name)
            os_name = solver_info["os_name"]
            os_version = solver_info["os_version"]
            python_version = solver_info["python_version"]
            query = (
                query.filter(PythonPackageVersion.os_name == os_name)
                .filter(PythonPackageVersion.os_version == os_version)
                .filter(PythonPackageVersion.python_version == python_version)
            )

        if index_url:
            query = query.join(PythonPackageIndex).filter(PythonPackageIndex.url == index_url)

        return query.count() > 0

    def python_package_exists(self, package_name: str) -> bool:
        """Check if the given Python package exists regardless of version."""
        package_name = self.normalize_python_package_name(package_name)
        return (
            self._session.query(PythonPackageVersionEntity)
            .filter(PythonPackageVersion.package_name == package_name)
            .count()
            > 0
        )

    def has_python_solver_error(
        self,
        package_name: str,
        package_version: str,
        index_url: str,
        *,
        os_name: Union[str, None],
        os_version: Union[str, None],
        python_version: Union[str, None],
    ) -> bool:
        """Retrieve information whether the given package has any solver error."""
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)
        query = (
            self._session.query(PythonPackageVersion)
            .filter(PythonPackageVersion.package_name == package_name)
            .filter(PythonPackageVersion.package_version == package_version)
        )

        if os_name is not None:
            query = query.filter(PythonPackageVersion.os_name == os_name)

        if os_version is not None:
            query = query.filter(PythonPackageVersion.os_version == os_version)

        if python_version is not None:
            query = query.filter(PythonPackageVersion.python_version == python_version)

        query = (
            query
            .join(PythonPackageIndex)
            .filter(PythonPackageIndex.url == index_url)
            .join(Solved)
            .order_by(desc(Solved.id))
            .with_entities(Solved.error)
        )

        result = query.first()

        if result is None:
            raise NotFoundError(
                f"No package record found for {package_name!r} in version {package_version!r} "
                f"from {index_url!r}, OS name is {os_name!r}:{os_version!r} with Python version {python_version!r}"
            )

        return result[0]

    def get_all_versions_python_package(
        self,
        package_name: str,
        index_url: str = None,
        *,
        index_enabled: bool = None,
        os_name: str = None,
        os_version: str = None,
        python_version: str = None,
    ) -> List[Tuple[str, str]]:
        """Get all versions available for a Python package."""
        package_name = self.normalize_python_package_name(package_name)
        query = self._session.query(PythonPackageVersion).filter(PythonPackageVersion.package_name == package_name)

        if os_name is not None:
            query = query.filter(PythonPackageVersion.os_name == os_name)

        if os_version is not None:
            query = query.filter(PythonPackageVersion.os_version == os_version)

        if python_version is not None:
            query = query.filter(PythonPackageVersion.python_version == python_version)

        query = query.join(PythonPackageIndex)

        if index_url is not None:
            query = query.filter(PythonPackageIndex.url == index_url)

        if index_enabled is not None:
            query = query.filter(PythonPackageIndex.enabled == index_enabled)

        return query.with_entities(PythonPackageVersion.package_version, PythonPackageIndex.url).all()

    def _construct_unsolved_python_packages_query(self, solver_name: str = None) -> Query:
        """Construct query for retrieving unsolved Python packages, the query is not executed."""
        subquery = self._session.query(PythonPackageVersion.package_name, PythonPackageVersion.package_version)

        if solver_name is not None:
            solver_info = self.parse_python_solver_name(solver_name)
            subquery = (
                subquery
                .filter(PythonPackageVersion.os_name == solver_info["os_name"])
                .filter(PythonPackageVersion.os_version == solver_info["os_version"])
                .filter(PythonPackageVersion.python_version == solver_info["python_version"])
            )

        subquery = subquery.distinct().subquery()
        query = (
            self._session.query(PythonPackageVersionEntity)
            .filter(
                tuple_(PythonPackageVersionEntity.package_name, PythonPackageVersionEntity.package_version).notin_(
                    subquery
                )
            )
            .with_entities(PythonPackageVersionEntity.package_name, PythonPackageVersionEntity.package_version)
            .distinct()
        )

        return query

    def retrieve_unsolved_python_packages(
        self,
        solver_name: str = None,
        randomize: bool = True
    ) -> List[Tuple[str, str]]:
        """Retrieve a list of tuples (package name, package version) of dependencies which were not yet resolved.

        Using solver_name argument the query narrows down to packages that were not resolved by the given solver.
        """
        query = self._construct_unsolved_python_packages_query(solver_name)

        if randomize:
            query = query.order_by(func.random())

        return query.all()

    def retrieve_unsolved_python_packages_count(self, solver_name: str = None) -> int:
        """Retrieve number of unsolved Python packages for the given solver."""
        query = self._construct_unsolved_python_packages_query(solver_name)
        return query.count()

    def retrieve_solved_python_packages_count(self, solver_name: str = None) -> int:
        """Retrieve number of solved Python packages for the given solver."""
        query = self._session.query(PythonPackageVersion)

        if solver_name:
            solver_info = self.parse_python_solver_name(solver_name)
            query = (
                query.filter(PythonPackageVersion.os_name == solver_info["os_name"])
                .filter(PythonPackageVersion.os_version == solver_info["os_version"])
                .filter(PythonPackageVersion.python_version == solver_info["python_version"])
            )

        return query.count()

    def retrieve_unanalyzed_python_package_versions(self, start_offset: int = 0, count: int = 100) -> List[dict]:
        """Retrieve a list of package names, versions and index urls that were not analyzed yet by package-analyzer."""
        subquery = (
            self._session.query(PackageAnalyzerRun)
            .join(PythonPackageVersionEntity)
            .join(PythonPackageIndex)
            .with_entities(
                PythonPackageVersionEntity.package_name,
                PythonPackageVersionEntity.package_version,
                PythonPackageIndex.url,
            )
            .distinct()
            .subquery()
        )

        query_result = (
            self._session.query(PythonPackageVersionEntity)
            .join(PythonPackageIndex)
            .filter(
                tuple_(
                    PythonPackageVersionEntity.package_name,
                    PythonPackageVersionEntity.package_version,
                    PythonPackageIndex.url,
                ).notin_(subquery)
            )
            .with_entities(
                PythonPackageVersionEntity.package_name,
                PythonPackageVersionEntity.package_version,
                PythonPackageIndex.url,
            )
            .distinct()
            .offset(start_offset)
            .limit(count)
            .all()
        )

        return [{"package_name": item[0], "package_version": item[1], "index_url": item[2]} for item in query_result]

    def retrieve_solved_python_packages(self, count: int = 10, start_offset: int = 0, solver_name: str = None) -> dict:
        """Retrieve a dictionary mapping package names to versions for dependencies that were already solved.

        Using count and start_offset is possible to change pagination.
        Using solver_name argument the query narrows down to packages that were resolved by the given solver.
        """
        query = self._session.query(PythonPackageVersion.package_name, PythonPackageVersion.package_version)

        if solver_name is not None:
            solver_info = self.parse_python_solver_name(solver_name)
            query = query.filter_by(
                os_name=solver_info["os_name"],
                os_version=solver_info["os_version"],
                python_version=solver_info["python_version"],
            )

        return query.offset(start_offset).limit(count).all()

    def retrieve_unsolvable_python_packages(self, solver_name: str = None) -> dict:
        """Retrieve a dictionary mapping package names to versions of packages that were marked as unsolvable."""
        query = self._session.query(PythonPackageVersion.package_name, PythonPackageVersion.package_version)

        if solver_name is not None:
            solver_info = self.parse_python_solver_name(solver_name)
            query = query.filter_by(
                os_name=solver_info["os_name"],
                os_version=solver_info["os_version"],
                python_version=solver_info["python_version"],
            )

        return query.join(Solved).filter_by(error_unsolvable=True).all()

    def retrieve_unsolvable_python_packages_per_run_software_environment(self, solver_name: str) -> dict:
        """Retrieve a dictionary mapping package names to versions of packages that were marked as unsolvable.

        The result is given for a specific run software environment (OS + python version)
        """
        # TODO: substitute this query where used
        return self.retrieve_unsolvable_python_packages(solver_name)

    def retrieve_unparseable_python_packages(self, solver_name: str = None) -> dict:
        """Retrieve a dictionary mapping package names to versions of packages that couldn't be parsed by solver."""
        query = self._session.query(PythonPackageVersion.package_name, PythonPackageVersion.package_version)

        if solver_name is not None:
            solver_info = self.parse_python_solver_name(solver_name)
            query = query.filter_by(
                os_name=solver_info["os_name"],
                os_version=solver_info["os_version"],
                python_version=solver_info["python_version"],
            )

        return query.join(Solved).filter_by(error_unparseable=True).all()

    def get_all_python_packages_count(self, without_error: bool = True) -> int:
        """Retrieve number of Solved Python packages stored in the graph database."""
        query = self._session.query(PythonPackageVersion)

        if without_error:
            query = query.join(Solved).filter_by(error=False)

        return query.count()

    def get_error_python_packages_count(self, *, unsolvable: bool = False, unparseable: bool = False) -> int:
        """Retrieve number of Python packages stored in the graph database with error flag."""
        if unsolvable is True and unparseable is True:
            raise ValueError("Cannot query for unparseable and unsolvable at the same time")

        return (
            self._session.query(PythonPackageVersion)
            .join(Solved)
            .filter_by(error=True, error_unsolvable=unsolvable, error_unparseable=unparseable)
            .count()
        )

    def get_solver_documents_count(self) -> int:
        """Get number of solver documents synced into graph."""
        return self._session.query(Solved).distinct(Solved.document_id).count()

    def get_analyzer_documents_count(self) -> int:
        """Get number of image analysis documents synced into graph."""
        return self._session.query(PackageExtractRun).distinct(PackageExtractRun.analysis_document_id).count()

    def retrieve_dependent_packages(self, package_name: str, package_version: str = None) -> dict:
        """Get mapping package name to package version of packages that depend on the given package."""
        package_name = self.normalize_python_package_name(package_name)
        query = self._session.query(PythonPackageVersionEntity).filter(
            PythonPackageVersionEntity.package_name == package_name
        )

        if package_version is not None:
            package_version = self.normalize_python_package_version(package_version)
            query = query.filter(PythonPackageVersionEntity.package_version == package_version)

        query_result = (
            query.join(DependsOn)
            .join(PythonPackageVersion)
            .with_entities(PythonPackageVersion.package_name, PythonPackageVersion.package_version)
            .distinct()
            .all()
        )

        result = {}
        for package_name, package_version in query_result:
            if package_name not in result:
                result[package_name] = []

            result[package_name].append(package_version)

        return result

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
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)
        if not without_cache:
            result = self._cache.get_python_package_version_records(
                package_name=package_name,
                package_version=package_version,
                index_url=index_url,
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
            )
            if result is not None:
                return result

        query = self._session.query(PythonPackageVersion).filter_by(
            package_name=package_name, package_version=package_version
        )

        if os_name is not None:
            query = query.filter(PythonPackageVersion.os_name == os_name)

        if os_version is not None:
            query = query.filter(PythonPackageVersion.os_version == os_version)

        if python_version is not None:
            query = query.filter(PythonPackageVersion.python_version == python_version)

        query = query.join(PythonPackageIndex)

        if index_url is not None:
            query = query.filter(PythonPackageIndex.url == index_url)

        query_result = (
            query.with_entities(
                PythonPackageVersion.package_name,
                PythonPackageVersion.package_version,
                PythonPackageIndex.url,
                PythonPackageVersion.os_name,
                PythonPackageVersion.os_version,
                PythonPackageVersion.python_version,
            )
            .distinct()
            .all()
        )

        result = []
        for item in query_result:
            result.append(
                {
                    "package_name": item[0],
                    "package_version": item[1],
                    "index_url": item[2],
                    "os_name": item[3],
                    "os_version": item[4],
                    "python_version": item[5],
                }
            )

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
            Tuple[str, str, str],
            Tuple[str, str, str],
            Tuple[str, str, str],
            Tuple[str, str, str],
            Union[Tuple[str, str, str], None],
            Union[Tuple[str, str, str], None],
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
        package_version = self.normalize_python_package_version(package_version)

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
                        result.append((package_tuple, (dependency_name, dependency_version, None)))
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
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)

        package_requested = locals()
        package_requested.pop("self")
        package_requested.pop("without_cache")

        if not without_cache:
            result = self._cache.get_depends_on(
                package_name=package_name,
                package_version=package_version,
                index_url=index_url,
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
            )

            if result is not None:
                return result

        query = (
            self._session.query(PythonPackageVersion)
            .filter(PythonPackageVersion.package_name == package_name)
            .filter(PythonPackageVersion.package_version == package_version)
        )

        if os_name is not None:
            query = query.filter(PythonPackageVersion.os_name == os_name)

        if os_version is not None:
            query = query.filter(PythonPackageVersion.os_version == os_version)

        if python_version is not None:
            query = query.filter(PythonPackageVersion.python_version == python_version)

        query = query.join(PythonPackageIndex).filter(PythonPackageIndex.url == index_url)

        package_query = query
        dependencies = (
            query
            .join(DependsOn)
            .join(PythonPackageVersionEntity)
            .with_entities(PythonPackageVersionEntity.package_name, PythonPackageVersionEntity.package_version)
            .distinct()
            .all()
        )

        if not dependencies:
            if package_query.count() == 0:
                raise ValueError(f"No package record for {package_requested!r} found")

        if not without_cache:
            if not dependencies:
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
                Tuple[str, str, str],
                Tuple[str, str, str],
                Tuple[str, str, str],
                Tuple[str, str, str],
                Union[Tuple[str, str, str], None],
                Union[Tuple[str, str, str], None],
            ]
        ],
    ]:
        """Get all transitive dependencies for a given set of packages by traversing the dependency graph."""
        result = {}
        for package_tuple in package_tuples:
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
        solver_document_id = SolverResultsStore.get_document_id(solver_document)
        return self.solver_document_id_exist(solver_document_id)

    def solver_document_id_exist(self, solver_document_id: str) -> bool:
        """Check if there is a solver document record with the given id."""
        return self._session.query(Solved).filter(Solved.document_id == solver_document_id).count() > 0

    def dependency_monkey_document_id_exist(self, dependency_monkey_document_id: str) -> bool:
        """Check if the given dependency monkey report record exists in the graph database."""
        return (
            self._session.query(DependencyMonkeyRun)
            .filter(DependencyMonkeyRun.dependency_monkey_document_id == dependency_monkey_document_id)
            .count()
            > 0
        )

    def adviser_document_id_exist(self, adviser_document_id: str) -> bool:
        """Check if there is a adviser document record with the given id."""
        return (
            self._session.query(AdviserRun).filter(AdviserRun.adviser_document_idc == adviser_document_id).count() > 0
        )

    def analysis_records_exist(self, analysis_document: dict) -> bool:
        """Check whether the given analysis document records exist in the graph database."""
        analysis_document_id = AnalysisResultsStore.get_document_id(analysis_document)
        return self.analysis_document_id_exist(analysis_document_id)

    def analysis_document_id_exist(self, analysis_document_id: str) -> bool:
        """Check if there is an analysis document record with the given id."""
        return (
            self._session.query(PackageExtractRun)
            .filter(PackageExtractRun.analysis_document_id == analysis_document_id)
            .count()
            > 0
        )

    def package_analysis_document_id_exist(self, package_analysis_document_id: str) -> bool:
        """Check if there is a package analysis document record with the given id."""
        return (
            self._session.query(PackageAnalyzerRun)
            .filter(PackageAnalyzerRun.package_analysis_document_id == package_analysis_document_id)
            .count()
            > 0
        )

    def inspection_document_id_exist(self, inspection_document_id: str) -> bool:
        """Check if there is an inspection document record with the given id."""
        return (
            self._session.query(InspectionRun)
            .filter(InspectionRun.inspection_document_id == inspection_document_id)
            .count()
            > 0
        )

    def provenance_checker_document_id_exist(self, provenance_checker_document_id: str) -> bool:
        """Check if there is a provenance-checker document record with the given id."""
        return (
            self._session.query(ProvenanceCheckerRun)
            .filter(ProvenanceCheckerRun.provenance_checker_document_id == provenance_checker_document_id)
            .count()
            > 0
        )

    def get_python_cve_records(self, package_name: str, package_version: str) -> List[dict]:
        """Get known vulnerabilities for the given package-version."""
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)

        result = (
            self._session.query(CVE)
            .join(CVE.python_package_versions)
            .filter(PythonPackageVersionEntity.package_name == package_name)
            .filter(PythonPackageVersionEntity.package_version == package_version)
            .all()
        )

        return [cve.to_dict() for cve in result]

    def get_python_package_version_hashes_sha256(
        self, package_name: str, package_version: str, index_url: str = None
    ) -> List[str]:
        """Get hashes for a Python package in a specified version."""
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)

        if index_url is not None:
            query = (
                self._session.query(PythonPackageIndex)
                .filter(PythonPackageIndex.url == index_url)
                .join(PythonPackageVersion)
            )
        else:
            query = self._session.query(PythonPackageVersion)

        query = (
            query.filter(PythonPackageVersion.package_name == package_name)
            .filter(PythonPackageVersion.package_version == package_version)
            .join((HasArtifact, PythonPackageVersion.python_artifacts))
            .join((PythonArtifact, HasArtifact.python_artifact))
            .with_entities(PythonArtifact.artifact_hash_sha256)
            .distinct()
        )
        return [item[0] for item in query.all()]

    def get_all_python_package_version_hashes_sha256(self, package_name: str, package_version: str) -> List[str]:
        """Get hashes for a Python package per index."""
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)
        # TODO: remove  this from sources and substitute it
        return self.get_python_package_version_hashes_sha256(package_name, package_version, None)

    def is_python_package_index_enabled(self, url: str) -> bool:
        """Check if the given Python package index is enabled."""
        return self._session.query(PythonPackageIndex.enabled).filter_by(url=url).one()[0]

    def set_python_package_index_state(self, url: str, *, enabled: bool) -> None:
        """Enable or disable Python package index."""
        try:
            with self._session.begin(subtransactions=True):
                python_package_index = self._session.query(PythonPackageIndex) \
                    .filter(PythonPackageIndex.url == url).first()
                if python_package_index is None:
                    raise NotFoundError(f"Python package index {url!r} not found")

                python_package_index.enabled = enabled
                self._session.add(python_package_index)
        except Exception:
            self._session.rollback()
            raise
        else:
            self._session.commit()

    def register_python_package_index(
        self, url: str, warehouse_api_url: str = None, verify_ssl: bool = True, enabled: bool = False
    ) -> bool:
        """Register the given Python package index in the graph database."""
        python_package_index = self._session.query(PythonPackageIndex).filter(PythonPackageIndex.url == url).first()
        if python_package_index is None:
            try:
                with self._session.begin(subtransactions=True):
                    python_package_index = PythonPackageIndex(
                        url=url, warehouse_api_url=warehouse_api_url, verify_ssl=verify_ssl, enabled=enabled
                    )
                    self._session.add(python_package_index)
            except Exception:
                self._session.rollback()
                raise
            else:
                self._session.commit()
                return True
        else:
            python_package_index.warehouse_api_url = warehouse_api_url
            python_package_index.verify_ssl = verify_ssl
            python_package_index.enabled = enabled

            try:
                with self._session.begin(subtransactions=True):
                    self._session.add(python_package_index)
            except Exception:
                self._session.rollback()
                raise
            else:
                self._session.commit()
                return False

    def python_package_index_listing(self, enabled: bool = None) -> list:
        """Get listing of Python package indexes registered in the graph database."""
        query = self._session.query(
            PythonPackageIndex.url, PythonPackageIndex.warehouse_api_url, PythonPackageIndex.verify_ssl
        )

        if enabled is not None:
            query = query.filter(PythonPackageIndex.enabled == enabled)

        return [{"url": item[0], "warehouse_api_url": item[1], "verify_ssl": item[2]} for item in query.all()]

    def get_python_package_index_urls(self, enabled: bool = None) -> set:
        """Retrieve all the URLs of registered Python package indexes."""
        query = self._session.query(PythonPackageIndex)

        if enabled is not None:
            query = query.filter(PythonPackageIndex.enabled == enabled)

        return set(item[0] for item in query.with_entities(PythonPackageIndex.url).distinct().all())

    def get_python_packages_for_index(self, index_url: str) -> Set[str]:
        """Retrieve listing of Python packages known to graph database instance for the given index."""
        return set(
            item[0]
            for item in self._session.query(PythonPackageVersion)
            .join(PythonPackageIndex)
            .filter(PythonPackageIndex.url == index_url)
            .with_entities(PythonPackageVersion.package_name)
            .distinct()
            .all()
        )

    def get_python_packages(self) -> Set[str]:
        """Retrieve listing of all Python packages known to graph database instance."""
        return set(item[0] for item in self._session.query(PythonPackageVersionEntity.package_name).distinct().all())

    def _create_python_package_requirement(self, requirements: dict) -> List[PythonPackageRequirement]:
        """Create requirements for un-pinned Python packages."""
        result = []
        pipfile = Pipfile.from_dict(requirements)
        for requirement in pipfile.packages.packages.values():
            index = None
            if requirement.index is not None:
                index = self._get_or_create_python_package_index(requirement.index.url, only_if_enabled=False)

            python_package_requirement, _ = PythonPackageRequirement.get_or_create(
                self._session,
                name=self.normalize_python_package_name(requirement.name),
                version_range=requirement.version,
                python_package_index_id=index.id if index else None,
                develop=requirement.develop,
            )
            result.append(python_package_requirement)

        return result

    def _create_python_packages_pipfile(
        self, pipfile_locked: dict, software_environment: SoftwareEnvironment = None,
    ) -> List[PythonPackageVersion]:
        """Create Python packages from Pipfile.lock entries and return them."""
        result = []
        pipfile_locked = PipfileLock.from_dict(pipfile_locked, pipfile=None)
        os_name = software_environment.os_name if software_environment else None
        os_version = software_environment.os_version if software_environment else None
        python_version = software_environment.python_version if software_environment else None

        for package in pipfile_locked.packages.packages.values():
            result.append(self._create_python_package_version(
                package_name=package.name,
                package_version=package.locked_version,
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
                index_url=package.index.url if package.index else None,
            ))

        return result

    def _runtime_environment_conf2models(
        self,
        runtime_environment: dict,
        environment_type: str,
        is_user: bool,
    ) -> Tuple[HardwareInformation, SoftwareEnvironment]:
        """Create models out of runtime environment configuration."""
        hardware = runtime_environment.get("hardware", {})
        hardware_information, _ = HardwareInformation.get_or_create(
            self._session,
            cpu_vendor=hardware.get("cpu_vendor"),
            cpu_model=hardware.get("cpu_model"),
            cpu_cores=hardware.get("cpu_cores"),
            cpu_model_name=hardware.get("cpu_model_name"),
            cpu_family=hardware.get("cpu_family"),
            cpu_physical_cpus=hardware.get("cpu_physical_cpus"),
            gpu_model_name=hardware.get("gpu_model_name"),
            gpu_vendor=hardware.get("gpu_vendor"),
            gpu_cores=hardware.get("gpu_cores"),
            gpu_memory_size=hardware.get("gpu_memory_size"),
            ram_size=hardware.get("ram_size"),
            is_user=True,
        )

        software_environment, _ = SoftwareEnvironment.get_or_create(
            self._session,
            environment_name=runtime_environment.get("environment_name"),
            python_version=runtime_environment.get("python_version"),
            image_name=None,
            image_sha=None,
            os_name=runtime_environment.get("os_name"),
            os_version=runtime_environment.get("os_version"),
            cuda_version=runtime_environment.get("cuda_version"),
            environment_type=environment_type,
            is_user=is_user,
        )

        return hardware_information, software_environment

    def create_python_package_version_entity(
        self,
        package_name: str,
        package_version: str = None,
        index_url: str = None,
        only_if_package_seen: bool = False,
    ) -> Optional[Tuple[PythonPackageVersionEntity, bool]]:
        """Create a Python package version entity record in the system.

        By creating this entity, the system will record and track the given package.
        """
        package_name = self.normalize_python_package_name(package_name)
        if package_version is not None:
            package_version = self.normalize_python_package_version(package_version)

        if only_if_package_seen:
            seen_count = (
                self._session.query(PythonPackageVersionEntity)
                .filter(PythonPackageVersionEntity.package_name == package_name)
                .count()
            )

            if seen_count == 0:
                return None

        try:
            with self._session.begin(subtransactions=True):
                index = None
                if index_url:
                    index = self._get_or_create_python_package_index(index_url, only_if_enabled=False)

                entity, existed = PythonPackageVersionEntity.get_or_create(
                    self._session,
                    package_name=package_name,
                    package_version=package_version,
                    python_package_index_id=index.id if index else None,
                )
        except Exception:
            self._session.rollback()
            raise
        else:
            self._session.commit()

        return entity, existed

    def _create_python_package_version(
        self,
        package_name: str,
        package_version: str,
        os_name: Union[str, None],
        os_version: Union[str, None],
        python_version: Union[str, None],
        index_url: Union[str, None],
    ) -> PythonPackageVersion:
        """Create a Python package version.

        Make sure it is properly mirrored with a Python package entity and connected to a Python package index.
        """
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)
        index = None
        if index_url is not None:
            index = self._get_or_create_python_package_index(index_url, only_if_enabled=False)

        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)

        entity, _ = PythonPackageVersionEntity.get_or_create(
            self._session,
            package_name=package_name,
            package_version=package_version,
            python_package_index_id=index.id if index else None,
        )

        python_package_version, _ = PythonPackageVersion.get_or_create(
            self._session,
            package_name=package_name,
            package_version=package_version,
            python_package_index_id=index.id if index else None,
            os_name=os_name,
            os_version=os_version,
            python_version=python_version,
            entity_id=entity.id,
        )

        return python_package_version

    def _create_python_software_stack(
        self,
        software_stack_type: str,
        requirements: dict = None,
        requirements_lock: dict = None,
        software_environment: SoftwareEnvironment = None,
        *,
        performance_score: float = None,
        overall_score: float = None,
    ) -> PythonSoftwareStack:
        """Create a Python software stack out of its JSON/dict representation."""
        software_stack, _ = PythonSoftwareStack.get_or_create(
            self._session,
            performance_score=performance_score,
            overall_score=overall_score,
            software_stack_type=software_stack_type,
        )

        if requirements is not None:
            python_package_requirements = self._create_python_package_requirement(requirements)
            for python_package_requirement in python_package_requirements:
                PythonRequirements.get_or_create(
                    self._session,
                    python_software_stack_id=software_stack.id,
                    python_package_requirement_id=python_package_requirement.id,
                )

        if requirements_lock is not None:
            python_package_versions = self._create_python_packages_pipfile(
                requirements_lock,
                software_environment=software_environment,
            )
            for python_package_version in python_package_versions:
                PythonRequirementsLock.get_or_create(
                    self._session,
                    python_software_stack_id=software_stack.id,
                    python_package_version_id=python_package_version.id,
                )

        return software_stack

    def python_software_stack_count(
        self,
        software_stack_type: str,
        unique: bool = False,
    ) -> List[str]:
        """Get number of Python software stacks available filtered by type."""
        query = (
            self._session.query(PythonSoftwareStack.software_stack_type)
            .filter(PythonSoftwareStack.software_stack_type == software_stack_type)
        )

        if unique:
            return query.distinct().count()

        return query.count()

    def sync_inspection_result(self, document) -> None:
        """Sync the given inspection document into the graph database."""
        # Check if we have such performance model before creating any other records.
        inspection_document_id = InspectionResultsStore.get_document_id(document)
        try:
            with self._session.begin(subtransactions=True):

                build_cpu = OpenShift.parse_cpu_spec(document["specification"]["build"]["requests"]["cpu"])
                build_memory = OpenShift.parse_memory_spec(document["specification"]["build"]["requests"]["memory"])
                run_cpu = OpenShift.parse_cpu_spec(document["specification"]["run"]["requests"]["cpu"])
                run_memory = OpenShift.parse_memory_spec(document["specification"]["run"]["requests"]["memory"])

                # Convert bytes to GiB, we need float number given the fixed int size.
                run_memory = run_memory / (1024 ** 3)
                build_memory = build_memory / (1024 ** 3)

                run_hardware_information, run_software_environment = self._runtime_environment_conf2models(
                    document["specification"]["run"].get("requests", {}), environment_type="RUNTIME", is_user=False
                )

                build_hardware_information, build_software_environment = self._runtime_environment_conf2models(
                    document["specification"]["build"].get("requests", {}),
                    environment_type="BUILDTIME",
                    is_user=False,
                )

                software_stack = None
                if "python" in document["specification"]:
                    # Inspection stack.
                    software_stack = self._create_python_software_stack(
                        software_stack_type="INSPECTION",
                        requirements=document["specification"]["python"].get("requirements"),
                        requirements_lock=document["specification"]["python"].get("requirements_locked"),
                        software_environment=run_software_environment,
                        performance_score=None,
                        overall_score=None,
                    )

                inspection_run = (
                    self._session.query(InspectionRun)
                    .filter(InspectionRun.inspection_document_id == inspection_document_id)
                    .first()
                )

                if inspection_run and inspection_run.dependency_monkey_run_id:
                    # If inspection was run through Dependency Monkey

                    # INSERT…ON CONFLICT (Upsert)
                    # https://docs.sqlalchemy.org/en/13/dialects/postgresql.html?highlight=conflict#insert-on-conflict-upsert
                    # https://docs.sqlalchemy.org/en/13/errors.html#sql-expression-language compile required
                    row = insert(InspectionRun).values(
                        id=inspection_run.dependency_monkey_run_id,
                        inspection_document_id=inspection_document_id,
                        dependency_monkey_run_id=inspection_run.dependency_monkey_run_id,
                        inspection_sync_state="PENDING"
                        ).on_conflict_do_update(
                            index_elements=['id'],
                            set_=dict(
                                inspection_sync_state="SYNCED",
                                inspection_document_id=inspection_document_id,
                                datetime=document.get("created"),
                                amun_version=None,  # TODO: propagate Amun version here which should match API version
                                build_requests_cpu=build_cpu,
                                build_requests_memory=build_memory,
                                run_requests_cpu=run_cpu,
                                run_requests_memory=run_memory,
                                build_software_environment_id=build_software_environment.id,
                                build_hardware_information_id=build_hardware_information.id,
                                run_software_environment_id=run_software_environment.id,
                                run_hardware_information_id=run_hardware_information.id,
                                inspection_software_stack_id=software_stack.id if software_stack else None,
                                )
                        ).compile(dialect=postgresql.dialect())

                else:
                    inspection_run, _ = InspectionRun.get_or_create(
                        self._session,
                        inspection_sync_state="SYNCED",
                        inspection_document_id=inspection_document_id,
                        datetime=document.get("created"),
                        amun_version=None,  # TODO: propagate Amun version here which should match API version
                        build_requests_cpu=build_cpu,
                        build_requests_memory=build_memory,
                        run_requests_cpu=run_cpu,
                        run_requests_memory=run_memory,
                        build_software_environment_id=build_software_environment.id,
                        build_hardware_information_id=build_hardware_information.id,
                        run_software_environment_id=run_software_environment.id,
                        run_hardware_information_id=run_hardware_information.id,
                        inspection_software_stack_id=software_stack.id if software_stack else None,
                    )

                if document["specification"].get("script"):  # We have run an inspection job.

                    if not document["job_log"]["stdout"]:
                        raise ValueError("No values provided for inspection output %r", inspection_document_id)

                    performance_indicator_name = document["job_log"]["stdout"].get("name")
                    performance_model_class = PERFORMANCE_MODEL_BY_NAME.get(performance_indicator_name)

                    if not performance_model_class:
                        raise PerformanceIndicatorNotRegistered(
                            f"No performance indicator registered for name {performance_indicator_name!r}"
                        )
                    framework = document["job_log"]["stdout"].get("framework")
                    if not framework:
                        _LOGGER.warning(
                            "No machine learning framework specified in performance indicator %r", cls.__name__
                        )

                    overall_score = document["job_log"]["stdout"].get("overall_score")
                    if overall_score is None:
                        _LOGGER.warning("No overall score detected in performance indicator %r", overall_score)

                    performance_indicator, _ = performance_model_class.create_from_report(
                        self._session,
                        document,
                        inspection_run_id=inspection_run.id
                    )

        except Exception:
            self._session.rollback()
            raise
        else:
            if inspection_run and inspection_run.dependency_monkey_run_id:
                self._engine.execute(row)
            else:
                self._session.commit()

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
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)
        try:
            with self._session.begin(subtransactions=True):
                cve, _ = CVE.get_or_create(
                    self._session, cve_id=record_id, version_range=version_range, advisory=advisory, cve_name=cve
                )
                index = self._session.query(PythonPackageIndex).filter_by(url=index_url).one()
                entity, _ = PythonPackageVersionEntity.get_or_create(
                    self._session,
                    package_name=package_name,
                    package_version=package_version,
                    python_package_index_id=index.id,
                )
                _, existed = HasVulnerability.get_or_create(
                    self._session, cve_id=cve.id, python_package_version_entity_id=entity.id
                )
        except Exception:
            self._session.rollback()
            raise
        else:
            self._session.commit()

        return cve, existed

    def _rpm_sync_analysis_result(self, package_extract_run: PackageExtractRun, document: dict) -> None:
        """Sync results of RPMs found in the given container image."""
        for rpm_package_info in document["result"]["rpm-dependencies"]:
            rpm_package_version, _ = RPMPackageVersion.get_or_create(
                self._session,
                package_name=rpm_package_info["name"],
                package_version=rpm_package_info["version"],
                release=rpm_package_info.get("release"),
                epoch=rpm_package_info.get("epoch"),
                arch=rpm_package_info.get("arch"),
                src=rpm_package_info.get("src", False),
                package_identifier=rpm_package_info.get("package_identifier", rpm_package_info["name"]),
            )
            FoundRPM.get_or_create(
                self._session,
                package_extract_run_id=package_extract_run.id,
                rpm_package_version_id=rpm_package_version.id,

            )
            for dependency in rpm_package_info["dependencies"]:
                rpm_requirement, _ = RPMRequirement.get_or_create(
                    self._session,
                    rpm_requirement_name=dependency
                )
                RPMRequires.get_or_create(
                    self._session,
                    rpm_package_version_id=rpm_package_version.id,
                    rpm_requirement_id=rpm_requirement.id,
                )

    def _deb_sync_analysis_result(self, package_extract_run: PackageExtractRun, document: dict) -> None:
        """Sync results of deb packages found in the given container image."""
        for deb_package_info in document["result"]["deb-dependencies"]:
            deb_package_version, _ = DebPackageVersion.get_or_create(
                self._session,
                package_name=deb_package_info["name"],
                package_version=deb_package_info["version"],
                epoch=deb_package_info.get("epoch"),
                arch=deb_package_info["arch"],
            )
            FoundDeb.get_or_create(
                self._session,
                deb_package_version_id=deb_package_version.id,
                package_extract_run_id=package_extract_run.id,
            )

            # These three can be grouped with a zip, but that is not that readable...
            for pre_depends in deb_package_info.get("pre-depends") or []:
                deb_dependency, _ = DebDependency.get_or_create(self._session, package_name=pre_depends["name"])
                DebPreDepends.get_or_create(
                    self._session,
                    deb_package_version_id=deb_package_version.id,
                    deb_dependency_id=deb_dependency.id,
                    version_range=pre_depends.get("version")
                )

            for depends in deb_package_info.get("depends") or []:
                deb_dependency, _ = DebDependency.get_or_create(self._session, package_name=depends["name"])
                DebDepends.get_or_create(
                    self._session,
                    deb_package_version_id=deb_package_version.id,
                    deb_dependency_id=deb_dependency.id,
                    version_range=depends.get("version"),
                )

            for replaces in deb_package_info.get("replaces") or []:
                deb_dependency, _ = DebDependency.get_or_create(self._session, package_name=replaces["name"])
                DebReplaces.from_properties(
                    deb_package_version_id=deb_package_version.id,
                    deb_dependency_id=deb_dependency.id,
                    version_range=replaces.get("version")
                )

    def _system_symbols_analysis_result(
        self,
        package_extract_run: PackageExtractRun,
        document: dict,
        software_environment: SoftwareEnvironment
    ) -> None:
        """Sync system symbols detected in a package-extract run into the database."""
        for library, symbols in document["result"]["system-symbols"].items():
            for symbol in symbols:
                versioned_symbol, _ = VersionedSymbol.get_or_create(
                    self._session,
                    library_name=library,
                    symbol=symbol,
                )

                HasSymbol.get_or_create(
                    self._session,
                    software_environment_id=software_environment.id,
                    versioned_symbol_id=versioned_symbol.id
                )

                DetectedSymbol.get_or_create(
                    self._session,
                    package_extract_run_id=package_extract_run.id,
                    versioned_symbol_id=versioned_symbol.id
                )

    def _python_sync_analysis_result(
        self, package_extract_run: PackageExtractRun, document: dict, software_environment: SoftwareEnvironment,
    ) -> None:
        """Sync results of Python packages found in the given container image."""
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

            if not python_package_info["result"].get("name"):
                analysis_document_id = AnalysisResultsStore.get_document_id(document)
                _LOGGER.warning(
                    "No package name found in entry %r when syncing document %r",
                    python_package_info,
                    analysis_document_id,
                )
                continue

            python_package_version = self._create_python_package_version(
                package_name=python_package_info["result"]["name"],
                package_version=python_package_info["result"]["version"],
                os_name=software_environment.os_name,
                os_version=software_environment.os_version,
                python_version=software_environment.python_version,
                index_url=None,
            )

            Identified.get_or_create(
                self._session,
                package_extract_run_id=package_extract_run.id,
                python_package_version_id=python_package_version.id,
            )

    def _python_file_digests_sync_analysis_result(self, package_extract_run: PackageExtractRun, document: dict) -> None:
        """Sync results of Python files found in the given container image."""
        for py_file in document["result"]["python-files"]:
            python_file_digest, _ = PythonFileDigest.get_or_create(
                self._session,
                sha256=py_file["sha256"],
            )

            FoundPythonFile.get_or_create(
                self._session,
                package_extract_run_id=package_extract_run.id,
                python_file_digest_id=python_file_digest.id,
                file=py_file["filepath"],
            )

    def sync_analysis_result(self, document: dict) -> None:
        """Sync the given analysis result to the graph database."""
        analysis_document_id = AnalysisResultsStore.get_document_id(document)
        environment_type = document["metadata"]["arguments"]["thoth-package-extract"]["metadata"]["environment_type"]
        environment_type = environment_type.upper()
        origin = document["metadata"]["arguments"]["thoth-package-extract"]["metadata"].get("origin")
        environment_name = document["metadata"]["arguments"]["extract-image"]["image"]
        os_name = document["result"]["operating-system"]["name"]
        os_version = document["result"]["operating-system"]["version_id"]

        image_tag = "latest"
        image_name = environment_name
        parts = environment_name.rsplit(":", maxsplit=1)
        if len(parts) == 2:
            image_name = parts[0]
            image_tag = parts[1]

        # TODO: capture errors on image analysis? result of package-extract should be a JSON with error flag
        try:
            with self._session.begin(subtransactions=True):
                software_environment, _ = SoftwareEnvironment.get_or_create(
                    self._session,
                    environment_name=environment_name,
                    python_version=None,  # TODO: find Python version which would be used by default
                    image_name=image_name,
                    image_sha=document["result"]["layers"][-1],
                    os_name=os_name,
                    os_version=os_version,
                    cuda_version=None,  # TODO: find CUDA version
                    environment_type=environment_type,
                    is_user=False,
                )
                package_extract_run, _ = PackageExtractRun.get_or_create(
                    self._session,
                    analysis_document_id=analysis_document_id,
                    datetime=document["metadata"]["datetime"],
                    package_extract_version=document["metadata"]["analyzer_version"],
                    package_extract_name=document["metadata"]["analyzer"],
                    environment_type=environment_type,
                    origin=origin,
                    debug=document["metadata"]["arguments"]["thoth-package-extract"]["verbose"],
                    package_extract_error=False,
                    image_tag=image_tag,
                    duration=None,  # TODO: assign duration
                    os_id=document["result"].get("operating-system", {}).get("id"),
                    os_name=os_name,
                    os_version_id=os_version,
                    software_environment_id=software_environment.id,
                )
                self._rpm_sync_analysis_result(package_extract_run, document)
                self._deb_sync_analysis_result(package_extract_run, document)
                self._python_sync_analysis_result(package_extract_run, document, software_environment)
                self._python_file_digests_sync_analysis_result(package_extract_run, document)
                self._system_symbols_analysis_result(package_extract_run, document, software_environment)
        except Exception:
            self._session.rollback()
            raise
        else:
            self._session.commit()

    def sync_package_analysis_result(self, document: dict) -> None:
        """Sync the given package analysis result to the graph database."""
        package_analysis_document_id = PackageAnalysisResultsStore.get_document_id(document)
        package_name = document["metadata"]["arguments"]["python"]["package_name"]
        package_name = self.normalize_python_package_name(package_name)
        package_version = document["metadata"]["arguments"]["python"]["package_version"]
        package_version = self.normalize_python_package_version(package_version)
        index_url = document["metadata"]["arguments"]["python"]["index_url"]

        _LOGGER.info(
            "Syncing package analysis for package %r in version %r from %r",
            package_name,
            package_version,
            index_url,
        )
        try:
            with self._session.begin(subtransactions=True):
                python_package_index, _ = PythonPackageIndex.get_or_create(
                    self._session,
                    url=index_url,
                )
                python_package_version_entity, _ = PythonPackageVersionEntity.get_or_create(
                    self._session,
                    package_name=package_name,
                    package_version=package_version,
                    python_package_index_id=python_package_index.id,
                )
                package_analyzer_run, _ = PackageAnalyzerRun.get_or_create(
                    self._session,
                    package_analyzer_name=document["metadata"]["analyzer"],
                    package_analyzer_version=document["metadata"]["analyzer_version"],
                    package_analysis_document_id=package_analysis_document_id,
                    datetime=document["metadata"]["datetime"],
                    debug=document["metadata"]["arguments"]["thoth-package-analyzer"]["verbose"],
                    package_analyzer_error=document["result"].get("error", False),
                    duration=None,  # TODO: assign duration
                    input_python_package_version_entity_id=python_package_version_entity.id,
                )

                for artifact in document["result"]["artifacts"]:
                    python_artifact, _ = PythonArtifact.get_or_create(
                        self._session,
                        artifact_hash_sha256=artifact["sha256"],
                        artifact_name=artifact["name"],
                    )
                    Investigated.get_or_create(
                        self._session,
                        package_analyzer_run_id=package_analyzer_run.id,
                        python_artifact_id=python_artifact.id,
                    )
                    for digest in artifact["digests"]:
                        file = digest["filepath"]
                        if file.endswith(".py"):
                            python_file_digest, _ = PythonFileDigest.get_or_create(
                                self._session,
                                sha256=digest["sha256"],
                            )
                            InvestigatedFile.get_or_create(
                                self._session,
                                package_analyzer_run_id=package_analyzer_run.id,
                                python_file_digest_id=python_file_digest.id,
                            )
                            IncludedFile.get_or_create(
                                self._session,
                                python_file_digest_id=python_file_digest.id,
                                python_artifact_id=python_artifact.id,
                                file=file,
                            )
                        else:
                            _LOGGER.warning("File %r found inside artifact not synced", file)

                    for library, symbols in artifact["symbols"].items():
                        for symbol in symbols:
                            versioned_symbol, _ = VersionedSymbol.get_or_create(
                                self._session,
                                library_name=library,
                                symbol=symbol,
                            )
                            RequiresSymbol.get_or_create(
                                self._session,
                                python_artifact_id=python_artifact.id,
                                versioned_symbol_id=versioned_symbol.id,
                            )
        except Exception:
            self._session.rollback()
            raise
        else:
            self._session.commit()

    def _get_or_create_python_package_index(
        self, index_url: str, only_if_enabled: bool = True
    ) -> Optional[PythonPackageIndex]:
        """Get or create Python package index entry with a check the given index is enabled."""
        python_package_index = (
            self._session.query(PythonPackageIndex).filter(PythonPackageIndex.url == index_url).first()
        )

        if python_package_index is None:
            if only_if_enabled:
                raise PythonIndexNotRegistered(f"Python package index {index_url!r} is not know to system")

            python_package_index, _ = PythonPackageIndex.get_or_create(self._session, url=index_url)
        elif not python_package_index.enabled and only_if_enabled:
            raise PythonIndexNotRegistered(f"Python package index {index_url!r} is not enabled")

        return python_package_index

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
                    # Normalized in `_create_python_package_version'.
                    package_name = python_package_info["package_name"]
                    package_version = python_package_info["package_version"]
                    index_url = python_package_info["index_url"]

                    _LOGGER.info(
                        "Syncing solver result of package %r in version %r from %r solved by %r",
                        package_name,
                        package_version,
                        index_url,
                        solver_info,
                    )
                    python_package_version = self._create_python_package_version(
                        package_name,
                        package_version,
                        os_name=ecosystem_solver.os_name,
                        os_version=ecosystem_solver.os_version,
                        python_version=ecosystem_solver.python_version,
                        index_url=index_url,
                    )

                    for sha256 in python_package_info["sha256"]:
                        artifact, _ = PythonArtifact.get_or_create(
                            self._session,
                            artifact_hash_sha256=sha256,
                            artifact_name=None,  # TODO: aggregate artifact names
                        )
                        HasArtifact.get_or_create(
                            self._session,
                            python_artifact_id=artifact.id,
                            python_package_version_id=python_package_version.id,
                        )

                    solved, _ = Solved.get_or_create(
                        self._session,
                        datetime=solver_datetime,
                        document_id=solver_document_id,
                        version=python_package_version,
                        ecosystem_solver=ecosystem_solver,
                        duration=None,
                        error=False,
                        error_unparseable=False,
                        error_unsolvable=False,
                    )

                    # TODO: detect and store extras
                    # TODO: detect and store markers
                    for dependency in python_package_info["dependencies"]:
                        for index_entry in dependency["resolved_versions"]:
                            for dependency_version in index_entry["versions"]:
                                dependency_entity, _ = PythonPackageVersionEntity.get_or_create(
                                    self._session,
                                    package_name=self.normalize_python_package_name(dependency["package_name"]),
                                    package_version=self.normalize_python_package_version(dependency_version),
                                    python_package_index_id=None,
                                )

                                DependsOn.get_or_create(
                                    self._session,
                                    version=python_package_version,
                                    entity=dependency_entity,
                                    version_range=dependency.get("required_version") or "*",
                                )

            for error_info in document["result"]["errors"]:
                # Normalized in `_create_python_package_version'.
                package_name = error_info.get("package_name") or error_info["package"]
                package_version = error_info["version"]
                index_url = error_info["index"]

                _LOGGER.info(
                    "Syncing solver errors for package %r in version %r from %r found by solver %r",
                    package_name,
                    package_version,
                    index_url,
                    solver_info,
                )
                python_package_version = self._create_python_package_version(
                    package_name,
                    package_version,
                    os_name=ecosystem_solver.os_name,
                    os_version=ecosystem_solver.os_version,
                    python_version=ecosystem_solver.python_version,
                    index_url=index_url,
                )

                solved, _ = Solved.get_or_create(
                    self._session,
                    datetime=solver_datetime,
                    document_id=solver_document_id,
                    version_id=python_package_version.id,
                    ecosystem_solver=ecosystem_solver,
                    duration=None,
                    error=True,
                    error_unparseable=False,
                    error_unsolvable=False,
                    is_provided=error_info.get("is_provided"),
                )

            for unsolvable in document["result"]["unresolved"]:
                if not unsolvable["version_spec"].startswith("=="):
                    # No resolution can be performed so no identifier is captured, report warning and continue.
                    # We would like to capture this especially when there are
                    # packages in ecosystem that we cannot find (e.g. not configured private index
                    # or removed package).
                    _LOGGER.warning(
                        "Cannot sync unsolvable package %r as package is not locked to as specific version", unsolvable
                    )
                    continue

                package_name = self.normalize_python_package_name(unsolvable["package_name"])
                index_url = unsolvable["index"]
                package_version = self.normalize_python_package_version(unsolvable["version_spec"][len("=="):])

                _LOGGER.info(
                    "Syncing unsolvable package %r in version %r from %r found by solver %r",
                    package_name,
                    package_version,
                    index_url,
                    solver_info,
                )
                python_package_version = self._create_python_package_version(
                    package_name,
                    package_version,
                    os_name=ecosystem_solver.os_name,
                    os_version=ecosystem_solver.os_version,
                    python_version=ecosystem_solver.python_version,
                    index_url=index_url,
                )

                solved, _ = Solved.get_or_create(
                    self._session,
                    datetime=solver_datetime,
                    document_id=solver_document_id,
                    version_id=python_package_version.id,
                    ecosystem_solver=ecosystem_solver,
                    duration=None,
                    error=True,
                    error_unparseable=False,
                    error_unsolvable=True,
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

                _LOGGER.info(
                    "Syncing unparsed package %r in version %r from %r",
                    package_name,
                    package_version,
                    solver_info,
                )
                python_package_version = self._create_python_package_version(
                    package_name,
                    package_version,
                    os_name=ecosystem_solver.os_name,
                    os_version=ecosystem_solver.os_version,
                    python_version=ecosystem_solver.python_version,
                    index_url=None,
                )

                solved, _ = Solved.get_or_create(
                    self._session,
                    datetime=solver_datetime,
                    document_id=solver_document_id,
                    version=python_package_version,
                    ecosystem_solver=ecosystem_solver,
                    duration=None,
                    error=True,
                    error_unparseable=True,
                    error_unsolvable=False,
                )
        except Exception:
            self._session.rollback()
            raise
        else:
            self._session.commit()

    def sync_adviser_result(self, document: dict) -> None:
        """Sync adviser result into graph database."""
        adviser_document_id = AdvisersResultsStore.get_document_id(document)
        parameters = document["result"]["parameters"]
        cli_arguments = document["metadata"]["arguments"]["thoth-adviser"]
        origin = (cli_arguments.get("metadata") or {}).get("origin")
        runtime_environment = document["result"]["parameters"]["runtime_environment"]

        if not origin:
            _LOGGER.warning("No origin stated in the adviser result %r", adviser_document_id)

        try:
            with self._session.begin(subtransactions=True):
                hardware_information, user_run_software_environment = self._runtime_environment_conf2models(
                    runtime_environment=runtime_environment,
                    environment_type="RUNTIME",
                    is_user=True,
                )

                # Input stack.
                software_stack = self._create_python_software_stack(
                    software_stack_type="USER",
                    requirements=document["result"]["input"].get("requirements"),
                    requirements_lock=document["result"]["input"].get("requirements_locked"),
                    software_environment=user_run_software_environment,
                    performance_score=None,
                    overall_score=None,
                )

                adviser_run, _ = AdviserRun.get_or_create(
                    self._session,
                    additional_stack_info=bool(document["result"].get("stack_info")),
                    advised_configuration_changes=bool(document["result"].get("advised_configuration")),
                    adviser_document_id=adviser_document_id,
                    adviser_error=document["result"]["error"],
                    adviser_name=document["metadata"]["analyzer"],
                    adviser_version=document["metadata"]["analyzer_version"],
                    count=parameters["count"],
                    datetime=document["metadata"]["datetime"],
                    debug=cli_arguments.get("verbose", False),
                    duration=None,  # TODO: assign duration
                    limit=parameters["limit"],
                    limit_latest_versions=parameters.get("limit_latest_versions"),
                    origin=origin,
                    recommendation_type=parameters["recommendation_type"].upper(),
                    requirements_format=parameters["requirements_format"].upper(),
                    hardware_information_id=hardware_information.id,
                    user_build_software_environment_id=None,
                    user_run_software_environment_id=user_run_software_environment.id,
                    user_software_stack_id=software_stack.id,
                )

                # Output stacks - advised stacks
                for idx, result in enumerate(document["result"]["report"]):
                    if len(result) != 3:
                        _LOGGER.warning("Omitting stack as no output Pipfile.lock was provided")
                        continue

                    # result[0] is score report
                    # result[1]["requirements"] is Pipfile
                    # result[1]["requirements_locked"] is Pipfile.lock
                    # result[2] is overall score
                    performance_score = None
                    overall_score = result[2]
                    for entry in result[0] or []:
                        if "performance_score" in entry:
                            if performance_score is not None:
                                _LOGGER.error(
                                    "Multiple performance score entries found in %r (index: %d)",
                                    adviser_document_id,
                                    idx
                                )
                            performance_score = entry["performance_score"]

                    if result[1] and result[1].get("requirements_locked"):
                        software_stack = self._create_python_software_stack(
                            software_stack_type="ADVISED",
                            requirements=result[1].get("requirements"),
                            requirements_lock=result[1].get("requirements_locked"),
                            software_environment=user_run_software_environment,
                            performance_score=performance_score,
                            overall_score=overall_score,
                        )

                        Advised.get_or_create(
                            self._session,
                            adviser_run_id=adviser_run.id,
                            python_software_stack_id=software_stack.id
                        )
        except Exception:
            self._session.rollback()
            raise
        else:
            self._session.commit()

    def sync_provenance_checker_result(self, document: dict) -> None:
        """Sync provenance checker results into graph database."""
        provenance_checker_document_id = ProvenanceResultsStore.get_document_id(document)
        origin = (document["metadata"]["arguments"]["thoth-adviser"].get("metadata") or {}).get("origin")

        if not origin:
            _LOGGER.warning("No origin stated in the provenance-checker result %r", provenance_checker_document_id)

        try:
            with self._session.begin(subtransactions=True):
                user_input = document["result"]["input"]
                software_stack = self._create_python_software_stack(
                    software_stack_type="USER",
                    requirements=user_input.get("requirements"),
                    requirements_lock=user_input.get("requirements_locked"),
                    software_environment=None,
                    performance_score=None,
                    overall_score=None,
                )

                provenance_checker_run, _ = ProvenanceCheckerRun.get_or_create(
                    self._session,
                    provenance_checker_document_id=provenance_checker_document_id,
                    datetime=document["metadata"]["datetime"],
                    provenance_checker_version=document["metadata"]["analyzer_version"],
                    provenance_checker_name=document["metadata"]["analyzer"],
                    origin=origin,
                    debug=document["metadata"]["arguments"]["thoth-adviser"]["verbose"],
                    provenance_checker_error=document["result"]["error"],
                    duration=None,  # TODO: assign duration
                    user_software_stack_id=software_stack.id,
                )
        except Exception:
            self._session.rollback()
            raise
        else:
            self._session.commit()

    def sync_dependency_monkey_result(self, document: dict) -> None:
        """Sync reports of dependency monkey runs."""
        try:
            with self._session.begin(subtransactions=True):
                run_hardware_information, run_software_environment = self._runtime_environment_conf2models(
                    document["result"]["parameters"].get("runtime_environment", {}),
                    environment_type="RUNTIME",
                    is_user=False,
                )
                build_hardware_information, build_software_environment = self._runtime_environment_conf2models(
                    document["result"]["parameters"].get("runtime_environment", {}),
                    environment_type="BUILDTIME",
                    is_user=False,
                )
                dependency_monkey_run, _ = DependencyMonkeyRun.get_or_create(
                    self._session,
                    dependency_monkey_document_id=DependencyMonkeyReportsStore.get_document_id(document),
                    datetime=document["metadata"]["datetime"],
                    dependency_monkey_name=document["metadata"]["analyzer"],
                    dependency_monkey_version=document["metadata"]["analyzer_version"],
                    seed=document["result"]["parameters"].get("seed"),
                    decision=document["result"]["parameters"].get("decision_type"),
                    count=document["result"]["parameters"].get("count"),
                    limit_latest_versions=document["result"]["parameters"].get("limit_latest_versions"),
                    debug=document["metadata"]["arguments"]["thoth-adviser"]["verbose"],
                    dependency_monkey_error=document["result"]["error"],
                    duration=None,  # TODO: assign duration
                    build_software_environment_id=build_software_environment.id,
                    build_hardware_information_id=build_hardware_information.id,
                    run_software_environment_id=run_software_environment.id,
                    run_hardware_information_id=run_hardware_information.id,
                )

                python_package_requirements = self._create_python_package_requirement(
                    document["result"]["parameters"]["requirements"]
                )
                for python_package_requirement in python_package_requirements:
                    PythonDependencyMonkeyRequirements.get_or_create(
                        self._session,
                        python_package_requirement_id=python_package_requirement.id,
                        dependency_monkey_run_id=dependency_monkey_run.id,
                    )

                for inspection_document_id in document["result"]["output"]:
                    inspection_run = self._session.query(InspectionRun).filter(
                        InspectionRun.inspection_document_id == inspection_document_id
                    ).first()

                    if inspection_run is None:
                        inspection_run = InspectionRun(
                            inspection_document_id=inspection_document_id,
                            inspection_sync_state="PENDING",
                            dependency_monkey_run_id=dependency_monkey_run.id,
                        )
                        self._session.add(inspection_run)

                    inspection_run.dependency_monkey_run_id = dependency_monkey_run.id
        except Exception:
            self._session.rollback()
            raise
        else:
            self._session.commit()

    def get_all_pi_per_framework_count(self, framework: str) -> dict:
        """Retrieve dictionary with number of Performance Indicators per ML Framework in the graph database."""
        result = {}
        for pi_model in ALL_PERFORMANCE_MODELS:
            result[pi_model.__tablename__] = self._session.query(pi_model).filter_by(framework=framework).count()

        return result

    def get_all_pi_count(self) -> dict:
        """Retrieve dictionary mapping framework to performance indicator count (regardless of pi type)."""
        counter = Counter()
        for pi_model in ALL_PERFORMANCE_MODELS:
            query_result = (
                self._session.query(pi_model.framework, func.count(pi_model.framework))
                .group_by(PiMatmul.framework)
                .all()
            )
            counter.update(dict(query_result))

        return dict(counter)

    def get_number_performance_tables_records(self) -> Dict[str, int]:
        """Retrieve dictionary mapping performance tables to records count."""
        result = {}

        for performance_model in ALL_PERFORMANCE_MODELS:
            result[performance_model.__tablename__] = self._session.query(performance_model).count()

        return result

    def get_number_main_tables_records(self) -> Dict[str, int]:
        """Retrieve dictionary mapping main tables to records count."""
        result = {}

        for main_model in ALL_MAIN_MODELS:
            result[main_model.__tablename__] = self._session.query(main_model).count()

        return result

    def get_number_relation_tables_records(self) -> Dict[str, int]:
        """Retrieve dictionary mapping relation tables to records count."""
        result = {}

        for relation_model in ALL_RELATION_MODELS:
            result[relation_model.__tablename__] = self._session.query(relation_model).count()

        return result

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

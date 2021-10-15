#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2019, 2020 Francesco Murdaca, Fridolin Pokorny
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

import functools
import re
import logging
import json
import os
import itertools
import weakref
import ssdeep

from decimal import Decimal
from typing import List
from typing import Set
from typing import Tuple
from typing import Optional
from typing import FrozenSet
from typing import Dict
from typing import Union
from typing import Any
from collections import deque
from contextlib import contextmanager
from datetime import datetime

import attr
from packaging.specifiers import SpecifierSet
from packaging.version import parse as parse_version
from sqlalchemy import create_engine
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import exists
from sqlalchemy import and_
from sqlalchemy import tuple_
from sqlalchemy import or_
from sqlalchemy.orm import Query
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.exc import NoResultFound

from thoth.python import PackageVersion
from thoth.python import Pipfile
from thoth.python import PipfileLock
from thoth.common.helpers import format_datetime
from thoth.common import OpenShift
from thoth.common import normalize_os_version
from thoth.common import map_os_name
from thoth.common.enums import ThothAdviserIntegrationEnum

from .models_base import BaseExtension
from .models import AdviserRun
from .models import ALL_MAIN_MODELS
from .models import CVE
from .models import DebDependency
from .models import DebPackageVersion
from .models import DependencyMonkeyRun
from .models import EcosystemSolver
from .models import ExternalHardwareInformation
from .models import ExternalPythonRequirements
from .models import ExternalPythonRequirementsLock
from .models import ExternalPythonSoftwareStack
from .models import ExternalSoftwareEnvironment
from .models import HardwareInformation
from .models import InspectionRun
from .models import ImportPackage
from .models import KebechetGithubAppInstallations
from .models import PackageExtractRun
from .models import ProvenanceCheckerRun
from .models import PythonArtifact
from .models import PythonFileDigest
from .models import PythonInterpreter
from .models import PythonPackageIndex
from .models import PythonPackageMetadata
from .models import PythonPackageMetadataClassifier
from .models import PythonPackageMetadataDistutils
from .models import PythonPackageMetadataPlatform
from .models import PythonPackageMetadataProjectUrl
from .models import PythonPackageMetadataProvidesExtra
from .models import PythonPackageMetadataRequiresExternal
from .models import PythonPackageMetadataSupportedPlatform
from .models import PythonPackageRequirement
from .models import PythonPackageVersion
from .models import PythonPackageVersionEntity
from .models import PythonPackageVersionEntityRule
from .models import PythonPackageVersionEntityRulesAssociation
from .models import PythonRequirements
from .models import PythonRequirementsLock
from .models import PythonSoftwareStack
from .models import RPMPackageVersion
from .models import RPMRequirement
from .models import SecurityIndicatorAggregatedRun
from .models import SoftwareEnvironment
from .models import VersionedSymbol

from .models import Advised
from .models import DebDepends
from .models import DebPreDepends
from .models import DebReplaces
from .models import DependsOn
from .models import DetectedSymbol
from .models import FoundDeb
from .models import FoundImportPackage
from .models import FoundPythonFile
from .models import FoundPythonInterpreter
from .models import FoundRPM
from .models import HasArtifact
from .models import HasExternalPythonRequirements
from .models import HasExternalPythonRequirementsLock
from .models import HasPythonRequirements
from .models import HasPythonRequirementsLock
from .models import HasMetadataClassifier
from .models import HasMetadataDistutils
from .models import HasMetadataPlatform
from .models import HasMetadataProjectUrl
from .models import HasMetadataProvidesExtra
from .models import HasMetadataRequiresExternal
from .models import HasMetadataSupportedPlatform
from .models import HasSymbol
from .models import HasUnresolved
from .models import HasVulnerability
from .models import Identified
from .models import PythonDependencyMonkeyRequirements
from .models import RequiresSymbol
from .models import RPMRequires
from .models import SIAggregated
from .models import Solved
from .models import ALL_RELATION_MODELS

from .models_performance import PERFORMANCE_MODEL_BY_NAME, ALL_PERFORMANCE_MODELS
from .models_performance import PERFORMANCE_MODELS_ML_FRAMEWORKS

from .sql_base import SQLBase
from .models_base import Base
from .postgres_utils import database_exists
from .postgres_utils import create_database
from .query_result_base import PythonQueryResult
from .enums import EnvironmentTypeEnum
from .enums import SoftwareStackTypeEnum
from .enums import InspectionSyncStateEnum
from .enums import MetadataDistutilsTypeEnum
from .enums import QuerySortTypeEnum
from .enums import PlatformEnum
from .enums import KebechetManagerEnum

from ..analyses import AnalysisResultsStore
from ..dependency_monkey_reports import DependencyMonkeyReportsStore
from ..provenance import ProvenanceResultsStore
from ..solvers import SolverResultsStore
from ..advisers import AdvisersResultsStore
from ..exceptions import NotFoundError
from ..exceptions import PythonIndexNotRegistered
from ..exceptions import PerformanceIndicatorNotRegistered
from ..exceptions import PythonIndexNotProvided
from ..exceptions import SolverNotRun
from ..exceptions import NotConnected
from ..exceptions import AlreadyConnected
from ..exceptions import DatabaseNotInitialized
from ..exceptions import DistutilsKeyNotKnown
from ..exceptions import SortTypeQueryError
from ..exceptions import CudaVersionDoesNotMatch


# Name of environment variables are long
# intentionally - you should adjust them only if
# you know what do you do.
_HAS_PYTHON_SOLVER_ERROR_CACHE_SIZE = int(os.getenv("THOTH_STORAGE_HAS_PYTHON_SOLVER_ERROR_CACHE_SIZE", 4096))
_GET_PYTHON_PACKAGE_VERSION_RECORDS_CACHE_SIZE = int(
    os.getenv("THOTH_STORAGE_GET_PYTHON_PACKAGE_VERSION_RECORDS_CACHE_SIZE", 16384)
)
_GET_DEPENDS_ON_CACHE_SIZE = int(os.getenv("THOTH_STORAGE_GET_DEPENDS_ON_CACHE_SIZE", 8192))
_GET_PYTHON_CVE_RECORDS_ALL_CACHE_SIZE = int(os.getenv("THOTH_STORAGE_GET_PYTHON_CVE_RECORDS_ALL_CACHE_SIZE", 4096))
_GET_PYTHON_PACKAGE_REQUIRED_SYMBOLS_CACHE_SIZE = int(
    os.getenv("THOTH_STORAGE_GET_PYTHON_PACKAGE_REQUIRED_SYMBOLS_CACHE_SIZE", 4096)
)
_GET_PYTHON_ENVIRONMENT_MARKER_CACHE_SIZE = int(os.getenv("THOTH_GET_PYTHON_ENVIRONMENT_MARKER_CACHE_SIZE", 4096))
_GET_S2I_ANALYZED_IMAGE_SYMBOLS = int(os.getenv("THOTH_S2I_ANALYZED_IMAGE_SYMBOLS_CACHE_SIZE", 1))
_GET_SI_AGGREGATED_PYTHON_PACKAGE_VERSION_CACHE_SIZE = int(
    os.getenv("THOTH_GET_PYTHON_ENVIRONMENT_MARKER_CACHE_SIZE", 4096)
)
_GET_PYTHON_PYTHON_PACKAGE_VERSION_SOLVER_RULES_CACHE_SIZE = int(
    os.getenv("THOTH_GET_PYTHON_PYTHON_PACKAGE_VERSION_SOLVER_RULES_CACHE_SIZE", 4096)
)
_GET_RPM_PACKAGE_VERSION_CACHE_SIZE = int(os.getenv("THOTH_GET_RPM_PACKAGE_VERSION_CACHE_SIZE", 1))
_GET_PYTHON_PACKAGE_VERSION_CACHE_SIZE = int(os.getenv("THOTH_GET_PYTHON_PACKAGE_VERSION_CACHE_SIZE", 1))


_LOGGER = logging.getLogger(__name__)


def lru_cache(*lru_args, **lru_kwargs):
    """Implement a cache for methods.

    Based on:
      https://stackoverflow.com/questions/33672412/python-functools-lru-cache-with-class-methods-release-object
    """
    # XXX: possibly move to another module to make it available for the whole Thoth
    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(self, *args, **kwargs):
            # We're storing the wrapped method inside the instance. If we had
            # a strong reference to self the instance would never die.
            self_weak = weakref.ref(self)

            @functools.wraps(func)
            @functools.lru_cache(*lru_args, **lru_kwargs)
            def cached_method(*args, **kwargs):
                return func(self_weak(), *args, **kwargs)

            setattr(self, func.__name__, cached_method)
            self._CACHED_METHODS.append(cached_method)
            return cached_method(*args, **kwargs)

        return wrapped_func

    return decorator


@attr.s()
class GraphDatabase(SQLBase):
    """A SQL database adapter providing graph-like operations on top of SQL queries."""

    _DECLARATIVE_BASE = Base
    DEFAULT_COUNT = 100

    _MULTI_VALUE_KEY_PYTHON_PACKAGE_METADATA_MAP = {
        "classifier": [HasMetadataClassifier, PythonPackageMetadataClassifier, "classifier"],
        "platform": [HasMetadataPlatform, PythonPackageMetadataPlatform, "platform"],
        "supported_platform": [
            HasMetadataSupportedPlatform,
            PythonPackageMetadataSupportedPlatform,
            "supported_platform",
        ],
        "requires_external": [HasMetadataRequiresExternal, PythonPackageMetadataRequiresExternal, "requires_external"],
        "project_url": [HasMetadataProjectUrl, PythonPackageMetadataProjectUrl, "project_url"],
        "provides_extra": [HasMetadataProvidesExtra, PythonPackageMetadataProvidesExtra, "optional_feature"],
    }

    _CACHED_METHODS = []

    def __del__(self) -> None:
        """Destruct adapter object."""
        if int(bool(os.getenv("THOTH_STORAGES_LOG_STATS", 0))):
            stats = self.stats()
            _LOGGER.info("Graph adapter statistics:\n%s", json.dumps(stats, indent=2))

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

    @contextmanager
    def _session_scope(self) -> Session:
        """Handle session commit and rollback."""
        session = self._sessionmaker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def connect(self):
        """Connect to the database."""
        if self.is_connected():
            raise AlreadyConnected("Cannot connect, the adapter is already connected")

        echo = bool(int(os.getenv("THOTH_STORAGES_DEBUG_QUERIES", 0)))
        try:
            self._engine = create_engine(self.construct_connection_string(), echo=echo)
            self._sessionmaker = sessionmaker(bind=self._engine)
        except Exception as engine_exc:
            _LOGGER.warning("Failed to create engine: %s", str(engine_exc))
            # Drop engine and session in case of any connection issues so is_connected behaves correctly.
            if self._engine:
                try:
                    self._engine.dispose()
                except Exception as exc:
                    _LOGGER.warning("Failed to dispose engine: %s", str(exc))
                    pass
            self._engine = None
            self._sessionmaker = None
            raise

        if not database_exists(self._engine.url):
            _LOGGER.warning("The database has not been created yet, no check for schema version is performed")
            return

        try:
            if not self.is_schema_up2date():
                _LOGGER.debug("Database adapter connected, database is initialized")
        except DatabaseNotInitialized as exc:
            _LOGGER.warning("Database is not ready to receive or query data: %s", str(exc))

    @staticmethod
    def _get_alembic_configuration():
        import thoth.storages
        from alembic import config

        alembic_cfg = config.Config(os.path.join(os.path.dirname(thoth.storages.__file__), "data", "alembic.ini"))
        alembic_cfg.attributes["configure_logger"] = False
        alembic_cfg.set_section_option(
            "alembic", "script_location", os.path.join(os.path.dirname(thoth.storages.__file__), "data", "alembic")
        )

        return alembic_cfg

    def initialize_schema(self):
        """Initialize schema of database."""
        from alembic import command

        if not self.is_connected():
            raise NotConnected("Cannot initialize schema: the adapter is not connected yet")

        if not database_exists(self._engine.url):
            _LOGGER.info("The database has not been created yet, it will be created now...")
            create_database(self._engine.url)

        alembic_cfg = self._get_alembic_configuration()

        # Overwrite URL based on deployment configuration.
        alembic_cfg.set_main_option("sqlalchemy.url", self.construct_connection_string())
        command.upgrade(alembic_cfg, "head")

    def drop_all(self):
        """Drop all content stored in the database."""
        super().drop_all()
        # Drop alembic version to be able re-run alembic migrations next time.
        self._engine.execute("DROP TABLE alembic_version;")

    def _get_script_directory_revisions(self):
        from alembic import script

        alembic_cfg = self._get_alembic_configuration()
        directory = script.ScriptDirectory.from_config(alembic_cfg)
        return directory

    def get_script_alembic_version_head(self) -> str:
        """Get alembic version head from alembic folder scripts."""
        directory = self._get_script_directory_revisions()
        head_revision = directory.get_current_head()

        return head_revision

    def get_table_alembic_version_head(self) -> str:
        """Get alembic version head from database table."""
        query = f"SELECT * FROM alembic_version"

        with self._session_scope() as session:
            result = session.execute(query).fetchone()
            return result[0]

    def is_schema_up2date(self) -> bool:
        """Check if the current schema is up2date with the one configured on database side."""
        database_head = self.get_table_alembic_version_head()
        script_head = self.get_script_alembic_version_head()

        is_up2date = database_head == script_head

        if not is_up2date:
            _LOGGER.warning(
                "The database schema is not in sync with library head revision, the current library revision "
                "head: %r, database head: %r",
                script_head,
                database_head,
            )

        return is_up2date

    def get_alembic_version_count_all(self) -> int:
        """Get number of records in alembic version table (1 expected)."""
        query = f"SELECT COUNT(*) FROM alembic_version"

        with self._session_scope() as session:
            result = session.execute(query).fetchone()
            return result[0]

    @staticmethod
    def normalize_python_package_name(package_name: str) -> str:
        """Normalize Python package name based on PEP-0503."""
        return PackageVersion.normalize_python_package_name(package_name)

    @staticmethod
    def normalize_python_package_version(package_version: str) -> str:
        """Normalize Python package name based on PEP-440."""
        return PackageVersion.normalize_python_package_version(package_version)

    @staticmethod
    def normalize_python_index_url(index_url: Optional[str]) -> Optional[str]:
        """Map python index url."""
        if index_url == "https://pypi.python.org/simple":
            return "https://pypi.org/simple"

        return index_url

    def get_analysis_metadata(self, analysis_document_id: str) -> Dict[str, Any]:
        """Get metadata stored for the given analysis document.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_analysis_metadata()
        {
            'analysis_datetime': datetime(2019, 10, 7, 18, 57, 22, 658131),
            'analysis_document_id': 'package-extract-2ef02c9cea8b1ef7',
            'package_extract_name': 'thoth-package-extract',
            'package_extract_version': '1.0.1'
            }
        """
        with self._session_scope() as session:
            query = (
                session.query(PackageExtractRun)
                .filter(PackageExtractRun.analysis_document_id == analysis_document_id)
                .with_entities(
                    PackageExtractRun.datetime,
                    PackageExtractRun.analysis_document_id,
                    PackageExtractRun.package_extract_name,
                    PackageExtractRun.package_extract_version,
                )
            )
            query_result = query.first()

            if query_result is None:
                raise NotFoundError(f"No records found for analysis with id {analysis_document_id!r}")

            return {
                "analysis_datetime": query_result[0],
                "analysis_document_id": query_result[1],
                "package_extract_name": query_result[2],
                "package_extract_version": query_result[3],
            }

    def _do_software_environment_listing(
        self, start_offset: int, count: Optional[int], is_external: bool, environment_type: str
    ) -> List[str]:
        """Perform actual query to software environments."""
        if is_external:
            class_ = ExternalSoftwareEnvironment
        else:
            class_ = SoftwareEnvironment

        with self._session_scope() as session:
            result = (
                session.query(class_.environment_name)
                .filter(class_.environment_type == environment_type)
                .offset(start_offset)
                .limit(count)
                .all()
            )

            return [item[0] for item in result]

    def get_run_software_environment_all(
        self, start_offset: int = 0, count: Optional[int] = DEFAULT_COUNT, is_external: bool = False
    ) -> List[str]:
        """Get all software environments available for run.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_run_software_environment_all()
        ['quay.io/thoth-station/thoth-pylint:v0.7.0-ubi8']
        """
        return self._do_software_environment_listing(
            start_offset, count, is_external, EnvironmentTypeEnum.RUNTIME.value
        )

    def get_build_software_environment_all(
        self, start_offset: int = 0, count: Optional[int] = DEFAULT_COUNT
    ) -> List[str]:
        """Get all software environments available for build.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_run_software_environment_all()
        ['quay.io/thoth-station/thoth-pylint:v0.7.0-ubi8']
        """
        # We do not have external/user software environment which is build environment yet.
        return self._do_software_environment_listing(start_offset, count, False, EnvironmentTypeEnum.BUILDTIME.value)

    def _do_software_environment_analyses_listing(
        self,
        software_environment_name: str,
        start_offset: int,
        count: Optional[int],
        convert_datetime: bool,
        is_external: bool,
        environment_type: str,
    ) -> List[dict]:
        """Get listing of available software environment analyses."""
        if is_external:
            class_ = ExternalSoftwareEnvironment
        else:
            class_ = SoftwareEnvironment

        with self._session_scope() as session:
            query_result = (
                session.query(class_)
                .filter(class_.environment_type == environment_type)
                .filter(class_.environment_name == software_environment_name)
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
                result.append(
                    {
                        "analysis_datetime": item[0] if not convert_datetime else format_datetime(item[0]),
                        "analysis_document_id": item[1],
                        "package_extract_name": item[2],
                        "package_extract_version": item[3],
                    }
                )

            return result

    def get_run_software_environment_analyses_all(
        self,
        run_software_environment_name: str,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        convert_datetime: bool = True,
        is_external: bool = False,
    ) -> List[dict]:
        """Get listing of analyses available for the given software environment for run.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_run_software_environment_analyses_all()
        [{
            'analysis_datetime': datetime(2019, 10, 7, 18, 57, 22, 658131),
            'analysis_document_id': 'package-extract-2ef02c9cea8b1ef7',
            'package_extract_name': 'thoth-package-extract',
            'package_extract_version': '1.0.1'
            }]
        """
        return self._do_software_environment_analyses_listing(
            run_software_environment_name,
            start_offset=start_offset,
            count=count,
            is_external=is_external,
            convert_datetime=convert_datetime,
            environment_type=EnvironmentTypeEnum.RUNTIME.value,
        )

    def get_build_software_environment_analyses_all(
        self,
        build_software_environment_name: str,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        convert_datetime: bool = True,
        is_external: bool = False,
    ) -> List[dict]:
        """Get listing of analyses available for the given software environment for build."""
        return self._do_software_environment_analyses_listing(
            build_software_environment_name,
            start_offset=start_offset,
            count=count,
            is_external=is_external,
            convert_datetime=convert_datetime,
            environment_type=EnvironmentTypeEnum.BUILDTIME.value,
        )

    def python_package_version_exists(
        self,
        package_name: str,
        package_version: str,
        index_url: Optional[str] = None,
        solver_name: Optional[str] = None,
    ) -> bool:
        """Check if the given Python package version exists in the graph database.

        If optional solver_name parameter is set, the call answers if the given package was solved by
        the given solver. Otherwise, any solver run is taken into account.
        """
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)
        index_url = self.normalize_python_index_url(index_url)

        with self._session_scope() as session:
            query = (
                session.query(PythonPackageVersion)
                .filter(PythonPackageVersion.package_name == package_name)
                .filter(PythonPackageVersion.package_version == package_version)
            )

            if solver_name:
                solver_info = OpenShift.parse_python_solver_name(solver_name)
                os_name = map_os_name(solver_info["os_name"])
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
        with self._session_scope() as session:
            return (
                session.query(PythonPackageVersionEntity)
                .filter(PythonPackageVersion.package_name == package_name)
                .count()
                > 0
            )

    def solved_software_environment_exists(self, os_name: str, os_version: str, python_version: str) -> bool:
        """Check if there are any solved packages for the given software environment."""
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            result = session.query(
                session.query(PythonPackageVersion)
                .filter(
                    PythonPackageVersion.os_name == os_name,
                    PythonPackageVersion.os_version == os_version,
                    PythonPackageVersion.python_version == python_version,
                )
                .exists()
            ).scalar()

            return result

    def get_solved_python_package_versions_software_environment_all(self) -> List[Dict[str, str]]:
        """Retrieve software environment configurations used to solve Python packages."""
        with self._session_scope() as session:
            result = (
                session.query(EcosystemSolver)
                .with_entities(EcosystemSolver.os_name, EcosystemSolver.os_version, EcosystemSolver.python_version)
                .distinct()
                .all()
            )

            return [{"os_name": i[0], "os_version": i[1], "python_version": i[2]} for i in result]

    @lru_cache(maxsize=_HAS_PYTHON_SOLVER_ERROR_CACHE_SIZE)
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
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        index_url = self.normalize_python_index_url(index_url)

        with self._session_scope() as session:
            query = (
                session.query(PythonPackageVersion)
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
                query.join(PythonPackageIndex)
                .filter(PythonPackageIndex.url == index_url)
                .join(Solved)
                .order_by(desc(Solved.datetime))
                .with_entities(Solved.error)
            )

            result = query.first()

            if result is None:
                raise NotFoundError(
                    f"No package record found for {package_name!r} in version {package_version!r} "
                    f"from {index_url!r}, OS name is {os_name!r}:{os_version!r} with Python version {python_version!r}"
                )

            return result[0]

    @staticmethod
    def _count_per_package(result: Union[List, Dict[str, Any]]) -> Dict[Tuple[str, str, str], int]:
        """Format Query result to count per package."""
        query_result = {}
        for item in result:
            if (item[0], item[1], item[2]) not in query_result:
                query_result[(item[0], item[1], item[2])] = item[3]
            else:
                query_result[(item[0], item[1], item[2])] += item[3]

        return query_result

    @staticmethod
    def _count_per_index(result: Union[List, Dict[str, Any]], index_url: str) -> Dict[str, Dict[Tuple[str, str], int]]:
        """Format Query result to count per index."""
        index_url = GraphDatabase.normalize_python_index_url(index_url)
        query_result = {index_url: {}}
        for item in result:
            if item[2] == index_url:
                if (item[0], item[1]) not in query_result[index_url].keys():
                    query_result[index_url][(item[0], item[1])] = item[3]
                else:
                    query_result[index_url][(item[0], item[1])] += item[3]

        return query_result

    @staticmethod
    def _count_per_version(
        result: Union[List, Dict[str, Any]],
    ) -> Dict[str, Dict[str, int]]:
        """Format Query result to count per version."""
        query_result = {}
        for item in result:
            if item[1] not in query_result:
                query_result[item[1]] = {}
                query_result[item[1]][item[2]] = item[3]
            else:
                if item[2] not in query_result[item[1]]:
                    query_result[item[1]][item[2]] = item[3]
                else:
                    query_result[item[1]][item[2]] += item[3]

        return query_result

    @staticmethod
    def _group_by_package_name(
        result: Union[List, Dict[str, Any]],
    ) -> Dict[str, List[Tuple[str, str]]]:
        """Format Query result to group by package name."""
        query_result = {}
        for item in result:
            if item[0] not in query_result:
                query_result[item[0]] = []
            query_result[item[0]].append((item[1], item[2]))

        return query_result

    # Solved Python Packages
    def get_solved_python_packages_all(
        self,
        *,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
    ) -> List[Tuple[str, str]]:
        """Retrieve solved Python package with index in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_solved_python_packages_all()
        [('regex', 'https://pypi.org/simple'), ('tensorflow', 'https://pypi.org/simple')]
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        return self.__class__.get_python_packages_all(**locals())

    def _construct_solved_python_packages_query(
        self,
        session: Session,
        *,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
    ) -> Query:
        """Construct query for solved Python packages functions, the query is not executed."""
        kwargs = locals()
        kwargs.pop("self", None)  # static method
        return self.__class__._construct_python_packages_query(**kwargs)

    def get_solved_python_packages_count_all(
        self,
        *,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
    ) -> int:
        """Retrieve number of solved Python package versions in Thoth Database."""
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = self._construct_solved_python_packages_query(
                session, os_name=os_name, os_version=os_version, python_version=python_version
            )

            if distinct:
                query = query.distinct()

            return query.count()

    def get_solved_python_packages_all_versions(
        self,
        *,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
    ) -> Dict[str, List[Tuple[str, str]]]:
        """Retrieve solved Python package versions per package in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_solved_python_packages_all_versions()
        {'absl-py': [('0.1.10', 'https://pypi.org/simple'), ('0.2.1', 'https://pypi.org/simple')]}
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = self._construct_solved_python_packages_query(
                session, os_name=os_name, os_version=os_version, python_version=python_version
            )

            query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            result = query.all()

            query_result = {}
            for item in result:
                if item[0] not in query_result:
                    query_result[item[0]] = []
                query_result[item[0]].append((item[1], item[2]))

            return query_result

    def get_solved_python_package_versions_count(
        self,
        *,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
    ) -> Dict[Tuple[str, str, str], int]:
        """Retrieve number of Python Package (package_name, package_version, index_url) solved in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_solved_python_package_versions_count()
        {('absl-py', '0.1.10', 'https://pypi.org/simple'): 1, ('absl-py', '0.2.1', 'https://pypi.org/simple'): 1}
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        return self.__class__.get_python_package_versions_count(**locals())

    def get_solved_python_package_versions_count_per_index(
        self,
        index_url: str,
        *,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
    ) -> Dict[str, Dict[Tuple[str, str], int]]:
        """Retrieve number of solved Python package versions per index url in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_solved_python_package_versions_count_per_index(index_url='https://pypi.org/simple')
        {'https://pypi.org/simple': {('absl-py', '0.1.10'): 1, ('absl-py', '0.2.1'): 1}}
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        index_url = self.normalize_python_index_url(index_url)
        return self.__class__.get_python_package_versions_count_per_index(**locals())

    def get_solved_python_package_versions_count_per_version(
        self,
        package_name: str,
        *,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
    ) -> Dict[str, Dict[str, int]]:
        """Retrieve number of solved Python package versions per package version in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_solved_python_package_versions_count_per_version(package_name='tensorflow')
        {'1.14.0rc0': {'https://pypi.org/simple': 1}, '1.13.0rc2': {'https://pypi.org/simple': 1}}
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        return self.__class__.get_python_package_versions_count_per_version(**locals())

    def _construct_solved_python_package_versions_query(
        self,
        session: Session,
        package_name: Optional[str] = None,
        package_version: Optional[str] = None,
        index_url: Optional[str] = None,
        *,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        is_missing: Optional[bool] = None,
    ) -> Query:
        """Construct query for solved Python packages versions functions, the query is not executed."""
        index_url = self.normalize_python_index_url(index_url)
        return self.__class__._construct_python_package_versions_query(**locals())

    def get_solved_python_package_versions_all(
        self,
        package_name: Optional[str] = None,
        package_version: Optional[str] = None,
        index_url: Optional[str] = None,
        *,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
        is_missing: Optional[bool] = None,
    ) -> List[Tuple[str, str, str]]:
        """Retrieve solved Python package versions in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_solved_python_package_versions_all()
        [('regex', '2018.11.7', 'https://pypi.org/simple'), ('tensorflow', '1.11.0', 'https://pypi.org/simple')]
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = self._construct_solved_python_package_versions_query(
                session,
                package_name=package_name,
                package_version=package_version,
                index_url=index_url,
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
                is_missing=is_missing,
            )

            query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            return query.all()

    def get_solved_python_package_versions_count_all(
        self,
        package_name: Optional[str] = None,
        package_version: Optional[str] = None,
        index_url: Optional[str] = None,
        *,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
        is_missing: Optional[bool] = None,
    ) -> int:
        """Retrieve solved Python package versions number in Thoth Database."""
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        index_url = self.normalize_python_index_url(index_url)
        with self._session_scope() as session:
            query = self._construct_solved_python_package_versions_query(
                session,
                package_name=package_name,
                package_version=package_version,
                index_url=index_url,
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
                is_missing=is_missing,
            )

            if distinct:
                query = query.distinct()

            return query.count()

    def _construct_error_solved_python_package_versions_query(
        self,
        session: Session,
        package_name: Optional[str] = None,
        package_version: Optional[str] = None,
        index_url: Optional[str] = None,
        *,
        unsolvable: bool = False,
        unparseable: bool = False,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
    ) -> Query:
        """Construct query for solved with error Python packages versions functions, the query is not executed."""
        query = session.query(PythonPackageVersion)

        if package_name is not None:
            package_name = self.normalize_python_package_name(package_name)
            query = query.filter(PythonPackageVersion.package_name == package_name)

        if package_version is not None:
            package_version = self.normalize_python_package_version(package_version)
            query = query.filter(PythonPackageVersion.package_version == package_version)

        if index_url is not None:
            index_url = self.normalize_python_index_url(index_url)
            query = query.filter(PythonPackageIndex.url == index_url)

        conditions = [Solved.version_id == PythonPackageVersion.id, Solved.error.is_(True)]

        if unsolvable:
            conditions.append(Solved.error_unsolvable.is_(True))

        if unparseable:
            conditions.append(Solved.error_unparseable.is_(True))

        if os_name:
            os_name = map_os_name(os_name)
            conditions.append(PythonPackageVersion.os_name == os_name)

        if os_version:
            os_version = normalize_os_version(os_name, os_version)
            conditions.append(PythonPackageVersion.os_version == os_version)

        if python_version:
            conditions.append(PythonPackageVersion.python_version == python_version)

        query = query.filter(exists().where(and_(*conditions)))

        return query

    def get_error_solved_python_package_versions_all(
        self,
        package_name: Optional[str] = None,
        package_version: Optional[str] = None,
        index_url: Optional[str] = None,
        *,
        unsolvable: bool = False,
        unparseable: bool = False,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
    ) -> List[Tuple[str, str, str]]:
        """Retrieve solved with error Python package versions in Thoth Database.

        if unsolvable=True -> get_unsolvable_python_package_versions
        if unparseable=True -> get_unparseable_python_package_versions

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_error_solved_python_package_versions_all()
        [('regex', '2018.11.7', 'https://pypi.org/simple'), ('tensorflow', '1.11.0', 'https://pypi.org/simple')]
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        index_url = self.normalize_python_index_url(index_url)
        if unsolvable is True and unparseable is True:
            raise ValueError("Cannot query for unparseable and unsolvable at the same time")

        with self._session_scope() as session:
            query = self._construct_error_solved_python_package_versions_query(
                session,
                package_name=package_name,
                package_version=package_version,
                index_url=index_url,
                unsolvable=unsolvable,
                unparseable=unparseable,
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
            )

            query = query.join(PythonPackageIndex).with_entities(
                PythonPackageVersion.package_name, PythonPackageVersion.package_version, PythonPackageIndex.url
            )

            query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            return query.all()

    def get_error_solved_document_id_all(
        self,
        package_name: Optional[str] = None,
        package_version: Optional[str] = None,
        index_url: Optional[str] = None,
        *,
        unsolvable: bool = False,
        unparseable: bool = False,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
        limit_results: bool = True,
    ) -> List[str]:
        """Retrieve solver document id with error Python package versions in Thoth Database.

        if unsolvable=True -> get_unsolvable_python_package_versions
        if unparseable=True -> get_unparseable_python_package_versions

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_error_solved_document_id_all()
        ['solver-fedora-32-py37-324232']
        """
        if unsolvable is True and unparseable is True:
            raise ValueError("Cannot query for unparseable and unsolvable at the same time")

        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)

        with self._session_scope() as session:
            query = self._construct_error_solved_python_package_versions_query(
                session,
                package_name=package_name,
                package_version=package_version,
                index_url=index_url,
                unsolvable=unsolvable,
                unparseable=unparseable,
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
            )

            query = query.with_entities(Solved.document_id)

            if limit_results:
                query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            return [ids[0] for ids in query.all()]

    def get_error_solved_python_package_versions_count_all(
        self,
        package_name: Optional[str] = None,
        package_version: Optional[str] = None,
        index_url: Optional[str] = None,
        *,
        unsolvable: bool = False,
        unparseable: bool = False,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
    ) -> int:
        """Retrieve solved with error Python package versions number in Thoth Database.

        if unsolvable=True -> get_unsolvable_python_package_versions_count_all
        if unparseable=True -> get_unparseable_python_package_versions_count_all
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        index_url = self.normalize_python_index_url(index_url)
        if unsolvable is True and unparseable is True:
            raise ValueError("Cannot query for unparseable and unsolvable at the same time")

        with self._session_scope() as session:
            query = self._construct_error_solved_python_package_versions_query(
                session,
                package_name=package_name,
                package_version=package_version,
                index_url=index_url,
                unsolvable=unsolvable,
                unparseable=unparseable,
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
            )

            query = query.join(PythonPackageIndex).with_entities(
                PythonPackageVersion.package_name, PythonPackageVersion.package_version, PythonPackageIndex.url
            )

            if distinct:
                query = query.distinct()

            return query.count()

    # Unsolved Python Packages

    def _construct_unsolved_python_package_versions_query(
        self,
        session: Session,
        package_name: Optional[str] = None,
        package_version: Optional[str] = None,
        index_url: Optional[str] = None,
        *,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
    ) -> Query:
        """Construct query for unsolved Python packages versions functions, the query is not executed."""
        index_url = self.normalize_python_index_url(index_url)
        query = session.query(PythonPackageVersionEntity).filter(
            PythonPackageVersionEntity.package_version.isnot(None),
            PythonPackageIndex.url.isnot(None),
            PythonPackageIndex.enabled.is_(True),
        )

        query = query.join(PythonPackageVersionEntityRulesAssociation, isouter=True).filter(
            PythonPackageVersionEntityRulesAssociation.python_package_version_entity_id.is_(None)
        )

        if package_name is not None:
            package_name = self.normalize_python_package_name(package_name)
            query = query.filter(PythonPackageVersionEntity.package_name == package_name)

        if package_version is not None:
            package_version = self.normalize_python_package_version(package_version)
            query = query.filter(PythonPackageVersionEntity.package_version == package_version)

        if index_url is not None:
            index_url = self.normalize_python_index_url(index_url)
            query = query.filter(PythonPackageIndex.url == index_url)

        conditions = [PythonPackageVersionEntity.id == PythonPackageVersion.entity_id]

        if os_name:
            conditions.append(PythonPackageVersion.os_name == os_name)

        if os_version:
            conditions.append(PythonPackageVersion.os_version == os_version)

        if python_version:
            conditions.append(PythonPackageVersion.python_version == python_version)

        return query.filter(~exists().where(and_(*conditions)))

    def get_unsolved_python_packages_all(
        self,
        *,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        distinct: bool = False,
    ) -> List[Tuple[str, Optional[str]]]:
        """Retrieve unsolved Python package with index in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_unsolved_python_packages_all()
        [('regex', 'https://pypi.org/simple'), ('tensorflow', 'https://pypi.org/simple')]
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = self._construct_unsolved_python_package_versions_query(
                session, os_name=os_name, os_version=os_version, python_version=python_version
            )

            query = query.join(PythonPackageIndex).with_entities(
                PythonPackageVersionEntity.package_name, PythonPackageIndex.url
            )

            query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            return query.all()

    def get_unsolved_python_packages_all_versions(
        self,
        *,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        distinct: bool = False,
    ) -> Dict[str, List[Tuple[str, str]]]:
        """Retrieve unsolved Python package versions per package in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_unsolved_python_packages_all_versions()
        {'absl-py': [('0.1.10', 'https://pypi.org/simple'), ('0.2.1', 'https://pypi.org/simple')]}
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = self._construct_unsolved_python_package_versions_query(
                session, os_name=os_name, os_version=os_version, python_version=python_version
            )

            query = (
                query.join(PythonPackageIndex)
                .with_entities(
                    PythonPackageVersionEntity.package_name,
                    PythonPackageVersionEntity.package_version,
                    PythonPackageIndex.url,
                )
                .group_by(
                    PythonPackageVersionEntity.package_name,
                    PythonPackageVersionEntity.package_version,
                    PythonPackageIndex.url,
                )
            )

            query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            result = query.all()

            return self._group_by_package_name(result=result)

    def get_unsolved_python_package_versions_count(
        self,
        *,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        distinct: bool = False,
    ) -> Dict[Tuple[str, str, str], int]:
        """Retrieve number of unsolved versions per Python package in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_unsolved_python_package_versions_count()
        {('absl-py', '0.1.10', 'https://pypi.org/simple'): 1, ('absl-py', '0.2.1', 'https://pypi.org/simple'): 1}
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = self._construct_unsolved_python_package_versions_query(
                session, os_name=os_name, os_version=os_version, python_version=python_version
            )

            query = (
                query.join(PythonPackageIndex)
                .with_entities(
                    PythonPackageVersionEntity.package_name,
                    PythonPackageVersionEntity.package_version,
                    PythonPackageIndex.url,
                    func.count(
                        tuple_(
                            PythonPackageVersionEntity.package_name,
                            PythonPackageVersionEntity.package_version,
                            PythonPackageIndex.url,
                        )
                    ),
                )
                .group_by(
                    PythonPackageVersionEntity.package_name,
                    PythonPackageVersionEntity.package_version,
                    PythonPackageIndex.url,
                )
            )

            query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            result = query.all()

            return self._count_per_package(result=result)

    def get_unsolved_python_package_versions_count_per_index(
        self,
        index_url: str,
        *,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        distinct: bool = False,
    ) -> Dict[str, Dict[Tuple[str, str], int]]:
        """Retrieve number of unsolved Python package versions per index url in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_unsolved_python_package_versions_count_per_index(index_url='https://pypi.org/simple')
        {'https://pypi.org/simple': {('absl-py', '0.1.10'): 1, ('absl-py', '0.2.1'): 1}}
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = self._construct_unsolved_python_package_versions_query(
                session, index_url=index_url, os_name=os_name, os_version=os_version, python_version=python_version
            )

            query = (
                query.join(PythonPackageIndex)
                .with_entities(
                    PythonPackageVersionEntity.package_name,
                    PythonPackageVersionEntity.package_version,
                    PythonPackageIndex.url,
                    func.count(
                        tuple_(
                            PythonPackageVersionEntity.package_name,
                            PythonPackageVersionEntity.package_version,
                            PythonPackageIndex.url,
                        )
                    ),
                )
                .group_by(
                    PythonPackageVersionEntity.package_name,
                    PythonPackageVersionEntity.package_version,
                    PythonPackageIndex.url,
                )
            )

            query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            result = query.all()

            return self._count_per_index(result=result, index_url=index_url)

    def get_unsolved_python_package_versions_count_per_version(
        self,
        package_name: str,
        *,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
    ) -> Dict[str, Dict[str, int]]:
        """Retrieve number of unsolved Python package versions per package version in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_unsolved_python_package_versions_count_per_version(package_name='tensorflow')
        {'1.14.0rc0': {'https://pypi.org/simple': 1}, '1.13.0rc2': {'https://pypi.org/simple': 1}}
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = self._construct_unsolved_python_package_versions_query(
                session,
                package_name=package_name,
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
            )

            query = (
                query.join(PythonPackageIndex)
                .with_entities(
                    PythonPackageVersionEntity.package_name,
                    PythonPackageVersionEntity.package_version,
                    PythonPackageIndex.url,
                    func.count(
                        tuple_(
                            PythonPackageVersionEntity.package_name,
                            PythonPackageVersionEntity.package_version,
                            PythonPackageIndex.url,
                        )
                    ),
                )
                .group_by(
                    PythonPackageVersionEntity.package_name,
                    PythonPackageVersionEntity.package_version,
                    PythonPackageIndex.url,
                )
            )

            query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            result = query.all()

            return self._count_per_version(result=result)

    def get_unsolved_python_package_versions_all(
        self,
        package_name: Optional[str] = None,
        package_version: Optional[str] = None,
        index_url: Optional[str] = None,
        *,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
        randomize: bool = True,
    ) -> List[Tuple[str, Optional[str], Optional[str]]]:
        """Retrieve unsolved Python package versions in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_unsolved_python_package_versions_all()
        [('regex', '2018.11.7', 'https://pypi.org/simple'), ('tensorflow', '1.11.0', 'https://pypi.org/simple')]
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = self._construct_unsolved_python_package_versions_query(
                session,
                package_name=package_name,
                package_version=package_version,
                index_url=index_url,
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
            )

            query = query.join(PythonPackageIndex).with_entities(
                PythonPackageVersionEntity.package_name,
                PythonPackageVersionEntity.package_version,
                PythonPackageIndex.url,
            )

            if randomize:
                query = query.order_by(func.random())

            query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            return query.all()

    def get_unsolved_python_package_versions_count_all(
        self,
        package_name: Optional[str] = None,
        package_version: Optional[str] = None,
        index_url: Optional[str] = None,
        *,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
    ) -> int:
        """Retrieve unsolved Python package versions number in Thoth Database."""
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = self._construct_unsolved_python_package_versions_query(
                session,
                package_name=package_name,
                package_version=package_version,
                index_url=index_url,
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
            )

            query = query.join(PythonPackageIndex).with_entities(
                PythonPackageVersionEntity.package_name,
                PythonPackageVersionEntity.package_version,
                PythonPackageIndex.url,
            )

            if distinct:
                query = query.distinct()

            return query.count()

    # SI Analyzed Python Packages

    def _construct_si_analyzed_python_package_versions_query(self, session: Session) -> Query:
        """Construct query for packages analyzed by solver and analyzed by SI."""
        query = session.query(SecurityIndicatorAggregatedRun)

        # We find all rows that are same in PythonPackageVersion and SIAggregated table.
        conditions = [
            SIAggregated.python_package_version_id == PythonPackageVersion.id,
            PythonPackageVersion.python_package_index_id == PythonPackageIndex.id,
        ]

        query = query.filter(exists().where(and_(*conditions)))

        return query

    def get_si_analyzed_python_package_versions_all(
        self,
        *,
        distinct: bool = False,
    ) -> List[Tuple[str, str, str]]:
        """Get SI analyzed Python package versions in Thoth Database.
        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_si_analyzed_python_package_versions_all()
        [('fbprophet', '0.4', 'https://pypi.org/simple')]
        """
        with self._session_scope() as session:
            query = self._construct_si_analyzed_python_package_versions_query(session)

            query = query.with_entities(
                PythonPackageVersion.package_name,
                PythonPackageVersion.package_version,
                PythonPackageIndex.url,
            )

            if distinct:
                query = query.distinct()

            return query.all()

    def get_si_analyzed_python_package_versions_count_all(
        self,
        *,
        distinct: bool = False,
    ) -> int:
        """Get SI analyzed Python package versions number in Thoth Database."""
        with self._session_scope() as session:
            query = self._construct_si_analyzed_python_package_versions_query(session)

            query = query.with_entities(
                PythonPackageVersion.package_name,
                PythonPackageVersion.package_version,
                PythonPackageIndex.url,
            )

            if distinct:
                query = query.distinct()

            return query.count()

    def _construct_si_unanalyzed_python_package_versions_query(
        self,
        session: Session,
        index_url: Optional[str] = None,
        provides_source_distro: bool = True,
        si_error: bool = False,
    ) -> Query:
        """Construct query for packages analyzed by solver, but unanalyzed by SI."""
        index_url = self.normalize_python_index_url(index_url)
        query = session.query(PythonPackageVersion).filter(
            PythonPackageVersion.package_version.isnot(None),
            PythonPackageIndex.url.isnot(None),
            PythonPackageIndex.enabled.is_(True),
            PythonPackageVersion.provides_source_distro.is_(provides_source_distro),
        )

        if index_url is not None:
            query = query.filter(PythonPackageIndex.url == index_url)

        # We find all rows that are same in PythonPackageVersion and SIAggregated table.
        conditions = [
            PythonPackageVersion.entity_id == SIAggregated.python_package_version_entity_id,
            SIAggregated.si_aggregated_run_id == SecurityIndicatorAggregatedRun.id,
        ]

        # Finally filter these out.
        query = query.filter(~exists().where(and_(*conditions)))
        query = query.filter(exists().where(SecurityIndicatorAggregatedRun.error.is_(si_error)))

        return query

    def get_si_unanalyzed_python_package_versions_all(
        self,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        distinct: bool = True,
        randomize: bool = True,
        provides_source_distro: bool = True,
        si_error: bool = False,
    ) -> List[Tuple[str, str, str]]:
        """Retrieve solved Python package versions in Thoth Database, that are not anaylyzed by SI.
        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_si_unanalyzed_python_package_versions_all()
        [('crossbar', '0.10.0', 'https://pypi.org/simple'), ('tensorflow', '1.11.0', 'https://pypi.org/simple')]
        """
        with self._session_scope() as session:
            query = self._construct_si_unanalyzed_python_package_versions_query(
                session,
                provides_source_distro=provides_source_distro,
                si_error=si_error,
            )

            query = query.join(PythonPackageIndex).with_entities(
                PythonPackageVersion.package_name,
                PythonPackageVersion.package_version,
                PythonPackageIndex.url,
            )

            if randomize:
                query = query.order_by(func.random())

            query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            return query.all()

    def get_si_unanalyzed_python_package_versions_count_all(
        self,
        index_url: Optional[str] = None,
        *,
        distinct: bool = False,
        provides_source_distro: bool = True,
        si_error: bool = False,
    ) -> int:
        """Get SI unanalyzed Python package versions number in Thoth Database."""
        with self._session_scope() as session:
            query = self._construct_si_unanalyzed_python_package_versions_query(
                session,
                provides_source_distro=provides_source_distro,
                si_error=si_error,
            )

            query = query.join(PythonPackageIndex).with_entities(
                PythonPackageVersion.package_name,
                PythonPackageVersion.package_version,
                PythonPackageIndex.url,
            )

            if distinct:
                query = query.distinct()

            return query.count()

    def _construct_get_solver_query(self, session: Session) -> Query:
        """Construct query to retrieve solvers."""
        query = session.query(EcosystemSolver).distinct(EcosystemSolver.solver_name)

        return query

    def get_ecosystem_solver_all(self) -> List[str]:
        """Get all solvers.
        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_ecosystem_solver_all()
        ['solver-fedora-31-py38', 'solver-fedora-32-py37', 'solver-fedora-32-py38', 'solver-ubi-8-py36']
        """
        with self._session_scope() as session:
            query = self._construct_get_solver_query(
                session,
            )
            solvers = query.with_entities(EcosystemSolver.solver_name).all()

            return [s[0] for s in solvers]

    def get_ecosystem_solver_count_all(self) -> int:
        """Get number of solvers."""
        with self._session_scope() as session:
            query = self._construct_get_solver_query(
                session,
            )
            return query.count()

    def get_solver_documents_count_all(self) -> int:
        """Get number of solver documents synced into graph."""
        with self._session_scope() as session:
            return session.query(Solved).distinct(Solved.document_id).count()

    def get_analyzer_documents_count_all(self) -> int:
        """Get number of image analysis documents synced into graph."""
        with self._session_scope() as session:
            return session.query(PackageExtractRun).distinct(PackageExtractRun.analysis_document_id).count()

    def _construct_query_get_si_aggregated_python_package_version(
        self, session: Session, package_name: Optional[str], package_version: Optional[str], index_url: Optional[str]
    ) -> Query:
        """Construct query for aggregate Security Indicators (SI) results per Python package version functions,
        the query is not executed.
        """
        query = session.query(SecurityIndicatorAggregatedRun)

        if package_name is not None:
            package_name = self.normalize_python_package_name(package_name)
            query = query.filter(PythonPackageVersion.package_name == package_name)

        if package_version is not None:
            package_version = self.normalize_python_package_version(package_version)
            query = query.filter(PythonPackageVersion.package_version == package_version)

        if index_url is not None:
            index_url = self.normalize_python_index_url(index_url)
            query = query.filter(PythonPackageIndex.url == index_url)

        query = query.with_entities(SecurityIndicatorAggregatedRun)

        query = query.filter(
            PythonPackageVersion.id == SIAggregated.python_package_version_id,
        )

        return query

    def si_aggregated_python_package_version_exists(
        self, package_name: str, package_version: str, index_url: str
    ) -> bool:
        """Check if Aggregate Security Indicators (SI) results exists for Python package version."""
        index_url = self.normalize_python_index_url(index_url)
        with self._session_scope() as session:
            query = self._construct_query_get_si_aggregated_python_package_version(
                session=session, package_name=package_name, package_version=package_version, index_url=index_url
            )

        return query.count() > 0

    @lru_cache(maxsize=_GET_SI_AGGREGATED_PYTHON_PACKAGE_VERSION_CACHE_SIZE)
    def get_si_aggregated_python_package_version(
        self, package_name: str, package_version: str, index_url: str
    ) -> Dict[str, int]:
        """Get Aggregate Security Indicators (SI) results per Python package version.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_si_aggregated_python_package_version(
            package_name='thoth-common',
            package_version='0.10.0',
            index_url='https://pypi.org/simple'
        )
            {
                'severity_high_confidence_high': 0,
                'severity_high_confidence_low': 0,
                'severity_high_confidence_medium': 0,
                'severity_high_confidence_undefined': 0,
                'severity_low_confidence_high': 0,
                'severity_low_confidence_low': 0,
                'severity_low_confidence_medium': 0,
                'severity_low_confidence_undefined': 0,
                'severity_medium_confidence_high': 0,
                'severity_medium_confidence_low': 0,
                'severity_medium_confidence_medium': 0,
                'severity_medium_confidence_undefined': 0,
                'number_of_analyzed_files': 0,
                'number_of_files_total': 0,
                'number_of_files_with_severities': 0,
                'number_of_filtered_files': 0,
                'number_of_python_files': 39,
                'number_of_lines_with_comments_in_python_files': 922,
                'number_of_blank_lines_in_python_files': 2760,
                'number_of_lines_with_code_in_python_files': 9509,
                'total_number_of_files': 75,
                'total_number_of_lines': 36856,
                'total_number_of_lines_with_comments': 2895,
                'total_number_of_blank_lines': 6737,
                'total_number_of_lines_with_code': 27224
            }
        """
        index_url = self.normalize_python_index_url(index_url)
        with self._session_scope() as session:
            query = self._construct_query_get_si_aggregated_python_package_version(
                session=session, package_name=package_name, package_version=package_version, index_url=index_url
            )
            result = query.order_by(SecurityIndicatorAggregatedRun.datetime.desc()).first()
            if result is None:
                raise NotFoundError(
                    f"No record found for {package_name!r} in version {package_version!r} from {index_url!r}"
                )
            result = result.to_dict()
            result.pop("si_aggregated_run_document_id")
            result.pop("datetime")
            return result

    def retrieve_dependent_packages(
        self, package_name: str, package_version: Optional[str] = None
    ) -> Dict[str, List[str]]:
        """Get mapping package name to package version of packages that depend on the given package."""
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)

        with self._session_scope() as session:
            query = session.query(PythonPackageVersionEntity).filter(
                PythonPackageVersionEntity.package_name == package_name
            )

            if package_version is not None:
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

    @lru_cache(maxsize=_GET_PYTHON_PACKAGE_VERSION_RECORDS_CACHE_SIZE)
    def get_python_package_version_records(
        self,
        package_name: str,
        package_version: str,
        index_url: Union[str, None],
        *,
        os_name: Union[str, None],
        os_version: Union[str, None],
        python_version: Union[str, None],
    ) -> List[dict]:
        """Get records for the given package regardless of index_url."""
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)

        with self._session_scope() as session:
            query = session.query(PythonPackageVersion).filter_by(
                package_name=package_name, package_version=package_version
            )

            if os_name is not None:
                os_name = map_os_name(os_name)
                query = query.filter(PythonPackageVersion.os_name == os_name)

            if os_version is not None:
                os_version = normalize_os_version(os_name, os_version)
                query = query.filter(PythonPackageVersion.os_version == os_version)

            if python_version is not None:
                query = query.filter(PythonPackageVersion.python_version == python_version)

            query = query.join(PythonPackageIndex)

            if index_url is not None:
                index_url = self.normalize_python_index_url(index_url)
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
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        extras: FrozenSet[Optional[str]] = None,
        marker_evaluation_result: Optional[bool] = None,
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

        Extras are taken into account only for direct dependencies. Any extras required in libraries used in
        transitive dependencies are not required as solver directly report dependencies regardless extras
        configuration - see get_depends_on docs for extras parameter values..
        """
        index_url = self.normalize_python_index_url(index_url)
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)

        result = []
        initial_stack_entry = (extras, package_name, package_version, index_url)
        stack = deque((initial_stack_entry,))
        seen_tuples = {(package_name, package_version, index_url)}
        while stack:
            (
                extras,
                package_name,
                package_version,
                index_url,
            ) = stack.pop()
            package_tuple = (package_name, package_version, index_url)

            configurations = self.get_python_package_version_records(
                package_name=package_name,
                package_version=package_version,
                index_url=index_url,
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
            )

            for configuration in configurations:
                dependencies = self.get_depends_on(
                    package_name=configuration["package_name"],
                    package_version=configuration["package_version"],
                    index_url=configuration["index_url"],
                    os_name=configuration["os_name"],
                    os_version=configuration["os_version"],
                    python_version=configuration["python_version"],
                    extras=extras,
                    marker_evaluation_result=marker_evaluation_result,
                )

                for dependency_name, dependency_version in itertools.chain(*dependencies.values()):
                    records = self.get_python_package_version_records(
                        package_name=dependency_name,
                        package_version=dependency_version,
                        index_url=None,  # Do cross-index resolution...
                        os_name=configuration["os_name"],
                        os_version=configuration["os_version"],
                        python_version=configuration["python_version"],
                    )

                    if not records:
                        # Not resolved yet.
                        result.append((package_tuple, (dependency_name, dependency_version, None)))
                    else:
                        for record in records:
                            dependency_tuple = (record["package_name"], record["package_version"], record["index_url"])
                            result.append((package_tuple, dependency_tuple))

                            if dependency_tuple not in seen_tuples:
                                # Explicitly set extras to None as we do not have direct dependency anymore.
                                stack.append((None, *dependency_tuple))
                                seen_tuples.add(dependency_tuple)

        return result

    @lru_cache(maxsize=_GET_PYTHON_ENVIRONMENT_MARKER_CACHE_SIZE)
    def get_python_environment_marker(
        self,
        package_name: str,
        package_version: str,
        index_url: str,
        *,
        dependency_name: str,
        dependency_version: str,
        os_name: str,
        os_version: str,
        python_version: str,
    ) -> Optional[str]:
        """Get Python evaluation marker as per PEP-0508.

        @raises NotFoundError: if the given package has no entry in the database
        """
        index_url = self.normalize_python_index_url(index_url)
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)

        with self._session_scope() as session:
            result = (
                session.query(PythonPackageVersion)
                .filter(PythonPackageVersion.package_name == package_name)
                .filter(PythonPackageVersion.package_version == package_version)
                .filter(PythonPackageVersion.os_name == os_name)
                .filter(PythonPackageVersion.os_version == os_version)
                .filter(PythonPackageVersion.python_version == python_version)
                .join(PythonPackageIndex)
                .filter(PythonPackageIndex.url == index_url)
                .join(DependsOn)
                .join(PythonPackageVersionEntity)
                .filter(PythonPackageVersionEntity.package_name == dependency_name)
                .filter(PythonPackageVersionEntity.package_version == dependency_version)
                .with_entities(DependsOn.marker)
                .first()
            )

            if result is None:
                raise NotFoundError(
                    f"No records found for package {(package_name, package_version, index_url)!r} with "
                    f"dependency {(dependency_name, dependency_version)!r} running on {os_name!r} in version "
                    f"{os_version!r} using Python in version {python_version!r}"
                )

            return result[0]

    def get_python_environment_marker_evaluation_result(
        self,
        package_name: str,
        package_version: str,
        index_url: str,
        *,
        dependency_name: str,
        dependency_version: str,
        os_name: str,
        os_version: str,
        python_version: str,
    ) -> bool:
        """Get result of the Python evaluation marker.

        The `extra` part of the environment marker (an exception in PEP-0508) is not taken into account and
        is substituted with a value which always defaults to True (as it would cause an error during context
        interpreting). See solver implementation for details.

        @raises NotFoundError: if the given package has no entry in the database
        """
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        index_url = self.normalize_python_index_url(index_url)

        with self._session_scope() as session:
            result = (
                session.query(PythonPackageVersion)
                .filter(PythonPackageVersion.package_name == package_name)
                .filter(PythonPackageVersion.package_version == package_version)
                .filter(PythonPackageVersion.os_name == os_name)
                .filter(PythonPackageVersion.os_version == os_version)
                .filter(PythonPackageVersion.python_version == python_version)
                .join(PythonPackageIndex)
                .filter(PythonPackageIndex.url == index_url)
                .join(DependsOn)
                .join(PythonPackageVersionEntity)
                .filter(PythonPackageVersionEntity.package_name == dependency_name)
                .filter(PythonPackageVersionEntity.package_version == dependency_version)
                .with_entities(DependsOn.marker_evaluation_result)
                .first()
            )

            if result is None:
                raise NotFoundError(
                    f"No records found for package {(package_name, package_version, index_url)!r} with "
                    f"dependency {(dependency_name, dependency_version)!r} running on {os_name!r} in version "
                    f"{os_version!r} using Python in version {python_version!r}"
                )

            return result[0]

    def get_python_package_version_dependents_all(
        self,
        package_name: str,
        *,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        start_offset: int = 0,
        count: int = DEFAULT_COUNT,
    ) -> List[Dict[str, Any]]:
        """Get dependents for the given package.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_dependents("selinon", os_name="rhel", os_version="8", python_version="3.6")
        [
          {
            "index_url": "https://pypi.org/simple",
            "package_name": "thoth-worker",
            "package_version": "0.0.2",
            "version_range": ">=1.0.0",
            "marker_evaluation_result": True,
            "marker": None,
            "extra": None,
          }
        ]
        """
        package_name = self.normalize_python_package_name(package_name)

        with self._session_scope() as session:
            query = (
                session.query(PythonPackageVersionEntity)
                .filter(PythonPackageVersionEntity.package_name == package_name)
                .join(DependsOn)
            )

            query = query.join(PythonPackageVersion)

            if os_name is not None:
                os_name = map_os_name(os_name)
                query = query.filter(PythonPackageVersion.os_name == os_name)

            if os_version is not None:
                os_version = normalize_os_version(os_name, os_version)
                query = query.filter(PythonPackageVersion.os_version == os_version)

            if python_version is not None:
                query = query.filter(PythonPackageVersion.python_version == python_version)

            query_result = (
                query.distinct()
                .join(PythonPackageIndex)
                .offset(start_offset)
                .limit(count)
                .with_entities(
                    PythonPackageVersion.package_name,
                    PythonPackageVersion.package_version,
                    PythonPackageIndex.url,
                    DependsOn.version_range,
                    DependsOn.marker_evaluation_result,
                    DependsOn.marker,
                    DependsOn.extra,
                )
                .all()
            )

            result = []
            for entry in query_result:
                result.append(
                    {
                        "package_name": entry[0],
                        "package_version": entry[1],
                        "index_url": entry[2],
                        "version_range": entry[3],
                        "marker_evaluation_result": entry[4],
                        "marker": entry[5],
                        "extra": entry[6],
                    }
                )

            return result

    @staticmethod
    def python_package_version_depends_on_platform_exists(platform: str) -> bool:
        """Check if the given platform has some records in the database."""
        return platform in (p.value for p in PlatformEnum)

    @staticmethod
    def get_python_package_version_platform_all() -> List[str]:
        """Retrieve all platforms stored in the database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_python_package_version_platform_all()
        ['linux-x86_64']
        """
        return [p.value for p in PlatformEnum]

    @lru_cache(maxsize=_GET_DEPENDS_ON_CACHE_SIZE)
    def get_depends_on(
        self,
        package_name: str,
        package_version: Optional[str] = None,
        index_url: Optional[str] = None,
        *,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        extras: FrozenSet[Optional[str]] = None,
        marker_evaluation_result: Optional[bool] = None,
        is_missing: Optional[bool] = None,
    ) -> Dict[str, List[Tuple[str, str]]]:
        """Get dependencies for the given Python package respecting environment and extras.

        If no environment is provided, dependencies are returned for all environments as stored in the database.

        Extras (as described in PEP-0508) are respected. If no extras is provided (extras=None), all dependencies are
        returned with all extras specified. A special value of None in extras listing no extra:

          * extras=frozenset((None,)) - return only dependencies which do not have any extra assigned
          * extras=frozenset((None, "postgresql")) - dependencies without extra and with extra "postgresql"
          * extras=None - return all dependencies (regardless extra)

        Environment markers are not taken into account in this query.
        """
        package_name = self.normalize_python_package_name(package_name)

        if package_version is not None:
            package_version = self.normalize_python_package_version(package_version)

        if index_url is not None:
            index_url = self.normalize_python_index_url(index_url)

        if os_name is not None:
            os_name = map_os_name(os_name)

        if os_version is not None:
            os_version = normalize_os_version(os_name, os_version)

        package_requested = locals()
        package_requested.pop("self")

        with self._session_scope() as session:
            query = session.query(PythonPackageVersion).filter(PythonPackageVersion.package_name == package_name)

            if package_version is not None:
                query = query.filter(PythonPackageVersion.package_version == package_version)

            if os_name is not None:
                query = query.filter(PythonPackageVersion.os_name == os_name)

            if os_version is not None:
                query = query.filter(PythonPackageVersion.os_version == os_version)

            if python_version is not None:
                query = query.filter(PythonPackageVersion.python_version == python_version)

            if is_missing is not None:
                query = query.filter(PythonPackageVersion.is_missing == is_missing)

            if index_url is not None:
                query = query.join(PythonPackageIndex).filter(PythonPackageIndex.url == index_url)

            # Mark the query here for later check, if we do not have any records for the given
            # package for the given environment.
            package_query = query

            query = query.join(DependsOn)

            if extras:
                # We cannot use in_ here as sqlalchemy does not support None in the list.
                query = query.filter(or_(*(DependsOn.extra == i for i in extras)))

            if marker_evaluation_result is not None:
                query = query.filter(DependsOn.marker_evaluation_result == marker_evaluation_result)

            dependencies = (
                query.join(PythonPackageVersionEntity)
                .with_entities(
                    DependsOn.extra, PythonPackageVersionEntity.package_name, PythonPackageVersionEntity.package_version
                )
                .distinct()
                .all()
            )

            if not dependencies:
                if package_query.count() == 0:
                    raise NotFoundError(f"No package record for {package_requested!r} found")

            result = {}
            for dependency in dependencies:
                extra, package_name, package_version = dependency
                if extra not in result:
                    result[extra] = []

                result[extra].append((package_name, package_version))

            return result

    def retrieve_transitive_dependencies_python_multi(
        self,
        *package_tuples,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
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
                *package_tuple, os_name=os_name, os_version=os_version, python_version=python_version
            )

        return result

    def solver_records_exist(self, solver_document: dict) -> bool:
        """Check if the given solver document record exists."""
        solver_document_id = SolverResultsStore.get_document_id(solver_document)
        return self.solver_document_id_exist(solver_document_id)

    def solver_document_id_exists(self, solver_document_id: str) -> bool:
        """Check if there is a solver document record with the given id."""
        with self._session_scope() as session:
            return session.query(Solved).filter(Solved.document_id == solver_document_id).count() > 0

    def dependency_monkey_document_id_exists(self, dependency_monkey_document_id: str) -> bool:
        """Check if the given dependency monkey report record exists in the graph database."""
        with self._session_scope() as session:
            return (
                session.query(DependencyMonkeyRun)
                .filter(DependencyMonkeyRun.dependency_monkey_document_id == dependency_monkey_document_id)
                .count()
                > 0
            )

    def si_aggregated_document_id_exists(self, si_aggregated_run_document_id: str) -> bool:
        """Check if the given security indicator aggregated report record exists in the graph database."""
        with self._session_scope() as session:
            return (
                session.query(SecurityIndicatorAggregatedRun)
                .filter(SecurityIndicatorAggregatedRun.si_aggregated_run_document_id == si_aggregated_run_document_id)
                .count()
                > 0
            )

    def inspection_document_id_result_number_exists(
        self, inspection_document_id: str, inspection_result_number: int
    ) -> bool:
        """Check if the given inspection id result number record exists in the graph database."""
        with self._session_scope() as session:
            return (
                session.query(InspectionRun)
                .filter(InspectionRun.inspection_document_id == inspection_document_id)
                .filter(InspectionRun.inspection_result_number == inspection_result_number)
                .count()
                > 0
            )

    def adviser_document_id_exist(self, adviser_document_id: str) -> bool:
        """Check if there is a adviser document record with the given id."""
        with self._session_scope() as session:
            return session.query(AdviserRun).filter(AdviserRun.adviser_document_id == adviser_document_id).count() > 0

    def analysis_records_exist(self, analysis_document: dict) -> bool:
        """Check whether the given analysis document records exist in the graph database."""
        analysis_document_id = AnalysisResultsStore.get_document_id(analysis_document)
        return self.analysis_document_id_exist(analysis_document_id)

    def analysis_document_id_exist(self, analysis_document_id: str) -> bool:
        """Check if there is an analysis document record with the given id."""
        with self._session_scope() as session:
            return (
                session.query(PackageExtractRun)
                .filter(PackageExtractRun.analysis_document_id == analysis_document_id)
                .count()
                > 0
            )

    def get_last_analysis_document_id(
        self, thoth_s2i_image_name: str, thoth_s2i_image_version: str, *, is_external: bool = False
    ) -> Optional[Dict[str, str]]:
        """Get last image analysis (if any) for the given container image."""
        model = ExternalSoftwareEnvironment if is_external else SoftwareEnvironment
        with self._session_scope() as session:
            result = (
                session.query(PackageExtractRun)
                .filter(model.thoth_s2i_image_name == thoth_s2i_image_name)
                .filter(model.thoth_s2i_image_version == thoth_s2i_image_version)
                .order_by(PackageExtractRun.datetime.desc())
                .with_entities(PackageExtractRun.analysis_document_id)
                .first()
            )

            if not result:
                return None

            return result[0]

    def inspection_document_id_exist(self, inspection_document_id: str) -> bool:
        """Check if there is an inspection document record with the given id."""
        with self._session_scope() as session:
            return (
                session.query(InspectionRun)
                .filter(InspectionRun.inspection_document_id == inspection_document_id)
                .count()
                > 0
            )

    def provenance_checker_document_id_exist(self, provenance_checker_document_id: str) -> bool:
        """Check if there is a provenance-checker document record with the given id."""
        with self._session_scope() as session:
            return (
                session.query(ProvenanceCheckerRun)
                .filter(ProvenanceCheckerRun.provenance_checker_document_id == provenance_checker_document_id)
                .count()
                > 0
            )

    @lru_cache(maxsize=_GET_PYTHON_CVE_RECORDS_ALL_CACHE_SIZE)
    def get_python_cve_records_all(self, package_name: str, package_version: Optional[str] = None) -> List[dict]:
        """Get known vulnerabilities for the given package-version."""
        package_name = self.normalize_python_package_name(package_name)
        if package_version:
            package_version = self.normalize_python_package_version(package_version)

        with self._session_scope() as session:
            query = session.query(PythonPackageVersionEntity).filter(
                PythonPackageVersionEntity.package_name == package_name
            )

            if package_version:
                query = query.filter(PythonPackageVersionEntity.package_version == package_version)

            result = query.join(HasVulnerability).join(CVE).with_entities(CVE).distinct().all()

            return [cve.to_dict() for cve in result]

    def get_python_cve_records_count(self) -> int:
        """Get number of CVE in Thoth database."""
        with self._session_scope() as session:
            return session.query(CVE.id).count()

    def get_python_package_hashes_sha256(
        self, package_name: str, package_version: str, index_url: str, *, distinct: bool = False
    ) -> List[str]:
        """Get all hashes for Python package in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_python_package_hashes_sha256()
        [
            '9d6863f6c70d034b8c34b3355cb7ba7d2ad799583947265efda41fe67127c23f',
            '8e4a1f6d89cfaadb486237acbfa24700add01da022dfcf3536e5071d21e13ee0'
        ]
        """
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)
        index_url = self.normalize_python_index_url(index_url)

        with self._session_scope() as session:
            query = (
                session.query(PythonPackageVersionEntity)
                .filter(PythonPackageVersionEntity.package_name == package_name)
                .filter(PythonPackageVersionEntity.package_version == package_version)
                .join(PythonPackageIndex)
                .filter(PythonPackageIndex.url == index_url)
                .join(HasArtifact)
                .join(PythonArtifact)
                .with_entities(PythonArtifact.artifact_hash_sha256)
            )

            if distinct:
                query = query.distinct()

            result = query.all()
            return [item[0] for item in result]

    def is_python_package_index_enabled(self, url: str) -> bool:
        """Check if the given Python package index is enabled."""
        with self._session_scope() as session:
            result = session.query(PythonPackageIndex.enabled).filter_by(url=url).first()

            if result is None:
                raise NotFoundError(f"No records for Python package index with URL {url!r} found")

            return result[0]

    def set_python_package_index_state(self, url: str, *, enabled: bool) -> None:
        """Enable or disable Python package index."""
        session = self._sessionmaker()
        try:
            with session.begin(subtransactions=True):
                python_package_index = session.query(PythonPackageIndex).filter(PythonPackageIndex.url == url).first()
                if python_package_index is None:
                    raise NotFoundError(f"Python package index {url!r} not found")

                python_package_index.enabled = enabled
                session.add(python_package_index)
        except Exception:
            session.rollback()
            raise
        else:
            session.commit()

    def register_python_package_index(
        self,
        url: str,
        warehouse_api_url: Optional[str] = None,
        verify_ssl: bool = True,
        enabled: bool = False,
        only_if_package_seen: bool = True,
    ) -> bool:
        """Register the given Python package index in the graph database."""
        with self._session_scope() as session, session.begin(subtransactions=True):
            python_package_index = session.query(PythonPackageIndex).filter(PythonPackageIndex.url == url).first()
            if python_package_index is None:
                PythonPackageIndex.get_or_create(
                    session=session,
                    url=url,
                    warehouse_api_url=warehouse_api_url,
                    verify_ssl=verify_ssl,
                    enabled=enabled,
                    only_if_package_seen=only_if_package_seen,
                )
                return True
            else:
                session.query(PythonPackageIndex).filter(PythonPackageIndex.id == python_package_index.id).update(
                    {
                        "warehouse_api_url": warehouse_api_url,
                        "verify_ssl": verify_ssl,
                        "enabled": enabled,
                        "only_if_package_seen": only_if_package_seen,
                    }
                )
                return False

    def delete_python_package_index(self, index_url: str) -> None:
        """Delete the given Python package index."""
        with self._session_scope() as session:
            return session.query(PythonPackageIndex).filter(PythonPackageIndex.url == index_url).delete()

    def get_python_package_index_all(self, enabled: bool = None) -> List[Dict[str, Any]]:
        """Get listing of Python package indexes registered in the graph database."""
        with self._session_scope() as session:
            query = session.query(
                PythonPackageIndex.url,
                PythonPackageIndex.warehouse_api_url,
                PythonPackageIndex.verify_ssl,
                PythonPackageIndex.only_if_package_seen,
            )

            if enabled is not None:
                query = query.filter(PythonPackageIndex.enabled == enabled)

            return [
                {"url": item[0], "warehouse_api_url": item[1], "verify_ssl": item[2], "only_if_package_seen": item[3]}
                for item in query.all()
            ]

    def get_hardware_environments_all(
        self,
        is_external: bool = False,
        *,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        without_id: bool = True,
    ) -> List[Dict]:
        """Get hardware environments (external or internal) registered in the graph database."""
        if is_external:
            hardware_environment = ExternalHardwareInformation
        else:
            hardware_environment = HardwareInformation

        with self._session_scope() as session:
            result = session.query(hardware_environment).offset(start_offset).limit(count).all()
            return [model.to_dict(without_id=without_id) for model in result]

    def get_software_environments_all(
        self,
        is_external: bool = False,
        *,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        env_image_name: Optional[str] = None,
        env_image_tag: Optional[str] = None,
    ) -> List[Dict]:
        """Get software environments (external or internal) registered in the graph database."""
        if is_external:
            software_environment = ExternalSoftwareEnvironment
        else:
            software_environment = SoftwareEnvironment

        with self._session_scope() as session:
            query = session.query(software_environment)

            if env_image_name:
                query = query.filter(software_environment.env_image_name == env_image_name)

            if env_image_tag:
                query = query.filter(software_environment.env_image_tag == env_image_tag)

            query = query.offset(start_offset).limit(count)
            return [model.to_dict() for model in query.all()]

    def get_python_package_index_urls_all(self, enabled: Optional[bool] = None) -> List[str]:
        """Retrieve all the URLs of registered Python package indexes."""
        with self._session_scope() as session:
            query = session.query(PythonPackageIndex)

            if enabled is not None:
                query = query.filter(PythonPackageIndex.enabled == enabled)

            return [item[0] for item in query.with_entities(PythonPackageIndex.url).distinct().all()]

    def get_python_package_versions_per_index(self, index_url: str, *, distinct: bool = False) -> Dict[str, List[str]]:
        """Retrieve listing of Python packages (solved) known to graph database instance for the given index."""
        index_url = self.normalize_python_index_url(index_url)
        with self._session_scope() as session:
            query = (
                session.query(PythonPackageVersion)
                .join(PythonPackageIndex)
                .filter(PythonPackageIndex.url == index_url)
                .with_entities(PythonPackageVersion.package_name)
            )

            if distinct:
                query = query.distinct()

            query = query.all()
            return {index_url: [item[0] for item in query]}

    def get_python_package_version_entities_count_all(self, *, distinct: bool = False) -> int:
        """Retrieve number of all Python packages in Thoth Database."""
        with self._session_scope() as session:
            query = session.query(PythonPackageVersionEntity)

            if distinct:
                query = query.distinct()

            return query.count()

    def get_python_package_version_entities_names_all(
        self,
    ) -> List[str]:
        """Retrieve names of Python package entities in the Thoth's knowledge base."""
        with self._session_scope() as session:
            query = session.query(PythonPackageVersionEntity.package_name)
            return [i[0] for i in query.distinct().all()]

    def get_python_package_version_names_all(
        self,
        *,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
    ) -> List[str]:
        """Retrieve names of Python Packages known by Thoth.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_python_packages_names_all()
        ['regex', 'tensorflow']
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = session.query(PythonPackageVersion).with_entities(PythonPackageVersion.package_name)

            if os_name is not None:
                query = query.filter(PythonPackageVersion.os_name == os_name)

            if os_version is not None:
                query = query.filter(PythonPackageVersion.os_version == os_version)

            if python_version is not None:
                query = query.filter(PythonPackageVersion.python_version == python_version)

            if distinct:
                query = query.distinct()

            result = query.all()
            return [item[0] for item in result]

    def get_python_packages_all(
        self,
        *,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
    ) -> List[Tuple[str, str]]:
        """Retrieve Python packages with index in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_python_packages_all()
        [('regex', 'https://pypi.org/simple'), ('tensorflow', 'https://pypi.org/simple')]
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = (
                session.query(PythonPackageVersion)
                .join(PythonPackageIndex)
                .with_entities(PythonPackageVersion.package_name, PythonPackageIndex.url)
            )

            if os_name is not None:
                query = query.filter(PythonPackageVersion.os_name == os_name)

            if os_version is not None:
                query = query.filter(PythonPackageVersion.os_version == os_version)

            if python_version is not None:
                query = query.filter(PythonPackageVersion.python_version == python_version)

            query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            return query.all()

    @staticmethod
    def _construct_python_packages_query(
        session: Session,
        *,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
    ) -> Query:
        """Construct query for Python packages functions, the query is not executed."""
        query = (
            session.query(PythonPackageVersion)
            .join(PythonPackageIndex)
            .group_by(PythonPackageVersion.package_name, PythonPackageVersion.package_version, PythonPackageIndex.url)
            .with_entities(
                PythonPackageVersion.package_name, PythonPackageVersion.package_version, PythonPackageIndex.url
            )
        )

        if os_name is not None:
            query = query.filter(PythonPackageVersion.os_name == os_name)

        if os_version is not None:
            query = query.filter(PythonPackageVersion.os_version == os_version)

        if python_version is not None:
            query = query.filter(PythonPackageVersion.python_version == python_version)

        return query

    def get_python_packages_count_all(
        self,
        *,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
    ) -> int:
        """Retrieve number of versions per Python package in Thoth Database."""
        with self._session_scope() as session:
            query = self._construct_python_packages_query(
                session, os_name=os_name, os_version=os_version, python_version=python_version
            )

            if distinct:
                query = query.distinct()

            return query.count()

    def get_python_packages_all_versions(
        self,
        *,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
    ) -> Dict[str, List[Tuple[str, str]]]:
        """Retrieve Python package versions per package in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_python_packages_all_versions()
        {'absl-py': [('0.1.10', 'https://pypi.org/simple'), ('0.2.1', 'https://pypi.org/simple')]}
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = self._construct_python_packages_query(
                session, os_name=os_name, os_version=os_version, python_version=python_version
            )

            query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            query_result = query.all()

            return self._group_by_package_name(result=query_result)

    def get_python_package_versions_count(
        self,
        *,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
    ) -> Dict[Tuple[str, str, str], int]:
        """Retrieve number of Python Package (package_name, package_version, index_url) in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_python_package_versions_count()
        {('absl-py', '0.1.10', 'https://pypi.org/simple'): 1, ('absl-py', '0.2.1', 'https://pypi.org/simple'): 1}
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = (
                session.query(PythonPackageVersion)
                .join(PythonPackageIndex)
                .group_by(
                    PythonPackageVersion.package_name, PythonPackageVersion.package_version, PythonPackageIndex.url
                )
                .with_entities(
                    PythonPackageVersion.package_name,
                    PythonPackageVersion.package_version,
                    PythonPackageIndex.url,
                    func.count(
                        tuple_(
                            PythonPackageVersion.package_name,
                            PythonPackageVersion.package_version,
                            PythonPackageIndex.url,
                        )
                    ),
                )
            )

            if os_name is not None:
                query = query.filter(PythonPackageVersion.os_name == os_name)

            if os_version is not None:
                query = query.filter(PythonPackageVersion.os_version == os_version)

            if python_version is not None:
                query = query.filter(PythonPackageVersion.python_version == python_version)

            query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            result = query.all()

            return self._count_per_package(result=result)

    def get_python_package_versions_all_count(
        self,
        *,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
        sort_by: QuerySortTypeEnum = None,
    ) -> PythonQueryResult:
        """Retrieve number of versions per Python package name in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_python_package_versions_all_count()
        {'setuptools': 988, 'pip': 211, 'termcolor': 14, 'six': 42}
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = (
                session.query(PythonPackageVersion)
                .join(PythonPackageIndex)
                .group_by(PythonPackageVersion.package_name)
                .with_entities(PythonPackageVersion.package_name, func.count(PythonPackageVersion.package_version))
            )

            if os_name is not None:
                query = query.filter(PythonPackageVersion.os_name == os_name)

            if os_version is not None:
                query = query.filter(PythonPackageVersion.os_version == os_version)

            if python_version is not None:
                query = query.filter(PythonPackageVersion.python_version == python_version)

            if sort_by and sort_by == QuerySortTypeEnum.PACKAGE_NAME:
                query = query.order_by(PythonPackageVersion.package_name)

            group_count = query.count()

            query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            result = query.all()

            if sort_by and sort_by == QuerySortTypeEnum.PACKAGE_VERSION:
                raise SortTypeQueryError("To be implemented.")  # TODO: To be implemented

            output = PythonQueryResult(result={item[0]: item[1] for item in result}, count=group_count)

            return output

    def get_python_package_versions_count_per_index(
        self,
        index_url: str,
        *,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
    ) -> Dict[str, Dict[Tuple[str, str], int]]:
        """Retrieve number of Python package versions per index url in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_python_package_versions_count_per_index(index_url='https://pypi.org/simple')
        {'https://pypi.org/simple': {('absl-py', '0.1.10'): 1, ('absl-py', '0.2.1'): 1}}
        """
        index_url = self.normalize_python_index_url(index_url)
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = (
                session.query(PythonPackageVersion)
                .join(PythonPackageIndex)
                .filter(PythonPackageIndex.url == index_url)
                .with_entities(
                    PythonPackageVersion.package_name,
                    PythonPackageVersion.package_version,
                    PythonPackageIndex.url,
                    func.count(tuple_(PythonPackageVersion.package_name, PythonPackageVersion.package_version)),
                )
                .group_by(
                    PythonPackageVersion.package_name, PythonPackageVersion.package_version, PythonPackageIndex.url
                )
            )

            if os_name is not None:
                query = query.filter(PythonPackageVersion.os_name == os_name)

            if os_version is not None:
                query = query.filter(PythonPackageVersion.os_version == os_version)

            if python_version is not None:
                query = query.filter(PythonPackageVersion.python_version == python_version)

            query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            result = query.all()

            return self._count_per_index(result=result, index_url=index_url)

    def get_python_package_versions_count_per_version(
        self,
        package_name: str,
        *,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
    ) -> Dict[str, Dict[str, int]]:
        """Retrieve number of Python package versions per index url in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_python_package_versions_count_per_version(package_name='tensorflow')
        {'1.14.0rc0': {'https://pypi.org/simple': 1}, '1.13.0rc2': {'https://pypi.org/simple': 1}}
        """
        package_name = self.normalize_python_package_name(package_name)
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)

        with self._session_scope() as session:
            query = (
                session.query(PythonPackageVersion)
                .join(PythonPackageIndex)
                .filter(PythonPackageVersion.package_name == package_name)
                .with_entities(
                    PythonPackageVersion.package_name,
                    PythonPackageVersion.package_version,
                    PythonPackageIndex.url,
                    func.count(
                        tuple_(
                            PythonPackageVersion.package_name,
                            PythonPackageVersion.package_version,
                            PythonPackageIndex.url,
                        )
                    ),
                )
                .group_by(
                    PythonPackageVersion.package_name, PythonPackageVersion.package_version, PythonPackageIndex.url
                )
            )

            if os_name is not None:
                query = query.filter(PythonPackageVersion.os_name == os_name)

            if os_version is not None:
                query = query.filter(PythonPackageVersion.os_version == os_version)

            if python_version is not None:
                query = query.filter(PythonPackageVersion.python_version == python_version)

            query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            result = query.all()

            return self._count_per_version(result=result)

    def _construct_python_package_versions_query(
        self,
        session: Session,
        package_name: Optional[str] = None,
        package_version: Optional[str] = None,
        index_url: Optional[str] = None,
        *,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        is_missing: Optional[bool] = None,
    ) -> Query:
        """Construct query for Python packages versions functions, the query is not executed."""
        index_url = self.normalize_python_index_url(index_url)
        query = (
            session.query(PythonPackageVersion)
            .join(PythonPackageIndex)
            .with_entities(
                PythonPackageVersion.package_name, PythonPackageVersion.package_version, PythonPackageIndex.url
            )
        )

        if package_name is not None:
            package_name = self.normalize_python_package_name(package_name)
            query = query.filter(PythonPackageVersion.package_name == package_name)

        if package_version is not None:
            package_version = self.normalize_python_package_version(package_version)
            query = query.filter(PythonPackageVersion.package_version == package_version)

        if index_url is not None:
            query = query.filter(PythonPackageIndex.url == index_url)

        if os_name is not None:
            query = query.filter(PythonPackageVersion.os_name == os_name)

        if os_version is not None:
            query = query.filter(PythonPackageVersion.os_version == os_version)

        if python_version is not None:
            query = query.filter(PythonPackageVersion.python_version == python_version)

        if is_missing is not None:
            query = query.filter(PythonPackageVersion.is_missing == is_missing)

        return query

    def get_python_package_versions_all(
        self,
        package_name: Optional[str] = None,
        package_version: Optional[str] = None,
        index_url: Optional[str] = None,
        *,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
        is_missing: Optional[bool] = None,
    ) -> List[Tuple[str, str, str]]:
        """Retrieve Python package versions in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_python_package_versions_all()
        [('regex', '2018.11.7', 'https://pypi.org/simple'), ('tensorflow', '1.11.0', 'https://pypi.org/simple')]
        """
        index_url = self.normalize_python_index_url(index_url)
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = self._construct_python_package_versions_query(
                session,
                package_name=package_name,
                package_version=package_version,
                index_url=index_url,
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
                is_missing=is_missing,
            )

            query = query.offset(start_offset).limit(count)

            if distinct:
                query = query.distinct()

            return query.all()

    def get_python_package_versions_count_all(
        self,
        package_name: Optional[str] = None,
        package_version: Optional[str] = None,
        index_url: Optional[str] = None,
        *,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        distinct: bool = False,
        is_missing: Optional[bool] = None,
    ) -> int:
        """Retrieve Python package versions number in Thoth Database."""
        index_url = self.normalize_python_index_url(index_url)
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)
        with self._session_scope() as session:
            query = self._construct_python_package_versions_query(
                session,
                package_name=package_name,
                package_version=package_version,
                index_url=index_url,
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
                is_missing=is_missing,
            )

            if distinct:
                query = query.distinct()

            return query.count()

    def _get_multi_values_key_python_package_version_metadata(
        self, python_package_metadata_id: int
    ) -> Dict[str, Optional[List[str]]]:
        """Retrieve multi values key metadata for Python package metadata."""
        with self._session_scope() as session:
            multi_value_results = {}
            for key, tables in self._MULTI_VALUE_KEY_PYTHON_PACKAGE_METADATA_MAP.items():
                query = (
                    session.query(tables[0])
                    .filter(tables[0].python_package_metadata_id == python_package_metadata_id)
                    .join(tables[1])
                ).with_entities(tables[1])
                multi_value_results[key] = [getattr(v, tables[2]) for v in query.all()]

            distutils_result = dict([(key, []) for key in ["requires_dist", "provides_dist", "obsolete_dist"]])
            multi_value_results.update(distutils_result)

            d_query = (
                session.query(HasMetadataDistutils)
                .filter(HasMetadataDistutils.python_package_metadata_id == python_package_metadata_id)
                .join(PythonPackageMetadataDistutils)
            ).with_entities(PythonPackageMetadataDistutils)

            for distutil in d_query.all():
                distutil_dict = distutil.to_dict()
                if distutil_dict["distutils_type"] == MetadataDistutilsTypeEnum.REQUIRED.value:
                    multi_value_results["requires_dist"].append(distutil_dict["distutils"])

                elif distutil_dict["distutils_type"] == MetadataDistutilsTypeEnum.PROVIDED.value:
                    multi_value_results["provides_dist"].append(distutil_dict["distutils"])

                elif distutil_dict["distutils_type"] == MetadataDistutilsTypeEnum.OBSOLETE.value:
                    multi_value_results["obsolete_dist"].append(distutil_dict["distutils"])

                else:
                    _LOGGER.warning("Distutils type not registered in Thoth.")

            return multi_value_results

    def get_python_package_version_metadata(
        self, package_name: str, package_version: str, index_url: str
    ) -> Dict[str, str]:
        """Retrieve Python package metadata."""
        index_url = self.normalize_python_index_url(index_url)
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)

        with self._session_scope() as session:
            query = (
                session.query(PythonPackageVersion)
                .filter(
                    and_(
                        PythonPackageVersion.package_name == package_name,
                        PythonPackageVersion.package_version == package_version,
                        PythonPackageVersion.python_package_metadata_id.isnot(None),
                    )
                )
                .join(PythonPackageIndex)
                .filter(PythonPackageIndex.url == index_url)
                .join(PythonPackageMetadata)
            ).with_entities(PythonPackageMetadata)

            result = query.first()

            if result is None:
                raise NotFoundError(f"No record found for {package_name!r}, {package_version!r}, {index_url!r}")

            formatted_result = result.to_dict()
            formatted_result.update(self._get_multi_values_key_python_package_version_metadata(result.id))

            return formatted_result

    def get_unsolved_python_packages_all_per_adviser_run(self, source_type: str) -> Dict[str, List[str]]:
        """Retrieve all unsolved packages for a certain Adviser Run that need to be re run.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_unsolved_python_packages_all_per_adviser_run()
        {'adviser-04ab56d6': ['black'], 'adviser-054ab56d6': ['black', 'numpy']}
        """
        with self._session_scope() as session:
            query = (
                session.query(AdviserRun)
                .filter(AdviserRun.need_re_run.is_(True))
                .filter(AdviserRun.source_type == source_type)
                .filter(AdviserRun.re_run_adviser_id.is_(None))
                .join(HasUnresolved)
                .join(PythonPackageVersionEntity)
            ).with_entities(AdviserRun.adviser_document_id, PythonPackageVersionEntity.package_name)

            query_result = query.all()

            result = {}
            for couple in query_result:
                result.setdefault(couple[0], []).append(couple[1])

            return result

    def _create_python_package_requirement(
        self, session: Session, requirements: dict
    ) -> List[PythonPackageRequirement]:
        """Create requirements for un-pinned Python packages."""
        result = []
        pipfile = Pipfile.from_dict(requirements)
        for requirement in pipfile.packages.packages.values():
            index = None
            if requirement.index is not None:
                index = self._get_or_create_python_package_index(session, requirement.index.url, only_if_enabled=False)

            python_package_requirement, _ = PythonPackageRequirement.get_or_create(
                session,
                name=self.normalize_python_package_name(requirement.name),
                version_range=requirement.version,
                python_package_index_id=index.id if index else None,
                develop=requirement.develop,
            )
            result.append(python_package_requirement)

        return result

    def _create_python_packages_pipfile(
        self,
        session: Session,
        pipfile_locked: dict,
        software_environment: SoftwareEnvironment = None,
        sync_only_entity: bool = False,
    ) -> List[PythonPackageVersion]:
        """Create Python packages from Pipfile.lock entries and return them."""
        result = []
        pipfile_locked = PipfileLock.from_dict(pipfile_locked, pipfile=None)
        os_name = software_environment.os_name if software_environment else None
        os_version = software_environment.os_version if software_environment else None
        python_version = software_environment.python_version if software_environment else None
        if sync_only_entity:
            for package in pipfile_locked.packages.packages.values():
                result.append(
                    self._create_python_package_version(
                        session,
                        package_name=package.name,
                        package_version=package.locked_version,
                        os_name=os_name,
                        os_version=os_version,
                        python_version=python_version,
                        index_url=package.index.url if package.index else None,
                        sync_only_entity=sync_only_entity,
                    )
                )

            return result
        else:
            for package in pipfile_locked.packages.packages.values():
                # Check if the package has a known index
                if package.index:
                    python_package_version = (
                        session.query(PythonPackageVersion)
                        .join(PythonPackageIndex)
                        .filter(PythonPackageVersion.package_name == package.name)
                        .filter(PythonPackageVersion.package_version == package.locked_version)
                        .filter(PythonPackageVersion.os_name == os_name)
                        .filter(PythonPackageVersion.os_version == os_version)
                        .filter(PythonPackageVersion.python_version == python_version)
                        .filter(PythonPackageIndex.url == package.index.url if package.index else None)
                        .first()
                    )
                else:
                    raise PythonIndexNotProvided(
                        f"Trying to sync package {package.name!r} in version {package.locked_version!r} "
                        "which does not have corresponding Python entity record"
                    )
                # Check if we run the solver for a specific package already
                if python_package_version:
                    result.append(
                        self._create_python_package_version(
                            session,
                            package_name=package.name,
                            package_version=package.locked_version,
                            os_name=os_name,
                            os_version=os_version,
                            python_version=python_version,
                            index_url=package.index.url if package.index else None,
                            python_package_metadata_id=python_package_version.python_package_metadata_id,
                            sync_only_entity=sync_only_entity,
                        )
                    )
                else:
                    raise SolverNotRun(
                        f"Trying to sync package {package.name!r} in version {package.locked_version!r} "
                        f"not solved by solver-{os_name}-{os_version}-{python_version}"
                    )

            return result

    def _runtime_environment_conf2models(
        self, session: Session, runtime_environment: dict, environment_type: str, is_external: bool
    ) -> Tuple[HardwareInformation, SoftwareEnvironment]:
        """Create models out of runtime environment configuration."""
        hardware = runtime_environment.get("hardware", {})
        os = runtime_environment.get("operating_system", {})

        if is_external:
            hardware_information_type = ExternalHardwareInformation
            software_environment_type = ExternalSoftwareEnvironment
        else:
            hardware_information_type = HardwareInformation
            software_environment_type = SoftwareEnvironment

        hardware_information, _ = hardware_information_type.get_or_create(
            session,
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
        )
        os_name = map_os_name(os.get("name"))
        software_environment, _ = software_environment_type.get_or_create(
            session,
            environment_name=runtime_environment.get("name"),
            python_version=runtime_environment.get("python_version"),
            image_name=None,
            image_sha=None,
            os_name=os_name,
            os_version=normalize_os_version(os_name, os.get("version")),
            cuda_version=runtime_environment.get("cuda_version"),
            environment_type=environment_type,
        )

        return hardware_information, software_environment

    def create_hardware_information(self, hardware: Dict[str, Any], is_external: bool = True) -> int:
        """Create hardware information in the database."""
        hardware_info = dict(hardware)

        hardware_information_type = ExternalHardwareInformation if is_external else HardwareInformation

        with self._session_scope() as session:
            hardware_information, _ = hardware_information_type.get_or_create(
                session,
                cpu_vendor=hardware_info.pop("cpu_vendor"),
                cpu_model=hardware_info.pop("cpu_model"),
                cpu_cores=hardware_info.pop("cpu_cores"),
                cpu_model_name=hardware_info.pop("cpu_model_name"),
                cpu_family=hardware_info.pop("cpu_family"),
                cpu_physical_cpus=hardware_info.pop("cpu_physical_cpus"),
                gpu_model_name=hardware_info.pop("gpu_model_name"),
                gpu_vendor=hardware_info.pop("gpu_vendor"),
                gpu_cores=hardware_info.pop("gpu_cores"),
                gpu_memory_size=hardware_info.pop("gpu_memory_size"),
                ram_size=hardware_info.pop("ram_size"),
            )

            hardware_information_id = hardware_information.id

        if hardware_info:
            _LOGGER.warning("Unknown parts of the hardware not synced into the database: %r", hardware_info)

        return hardware_information_id

    def delete_hardware_information(self, hardware_information_id: int, is_external: bool = True) -> None:
        """Delete hardware information entry with the given id."""
        hardware_information_type = ExternalHardwareInformation if is_external else HardwareInformation

        with self._session_scope() as session:
            session.query(hardware_information_type).filter(
                hardware_information_type.id == hardware_information_id
            ).delete()
            session.commit()

    def create_github_app_installation(self, slug: str, repo_name: str, private: bool, installation_id: str) -> bool:
        """Create a record for new installation or reactivate uninstalled installation.

        Example -
            "installation_id": "236796147",
            "repo_name": "advisor",
            "slug": "thoth-station/advisor",
            "private": False

        Accepts installation details passed down by Github.
        :rtype: True, False
        :returns True: if installation existed and was updated
        :returns False: if installation was newly added.
        """
        with self._session_scope() as session:
            instance = (
                session.query(KebechetGithubAppInstallations)
                .filter(KebechetGithubAppInstallations.slug == slug)
                .first()
            )
            if instance:
                instance.installation_id = installation_id
                instance.private = private
                instance.is_active = True
                session.commit()
                return True
            else:
                _, newly_added = KebechetGithubAppInstallations.get_or_create(
                    session,
                    slug=slug,
                    repo_name=repo_name,
                    private=private,
                    installation_id=installation_id,
                    is_active=True,
                    last_run=datetime.utcnow(),
                )
                return newly_added

    def get_kebechet_github_app_installations_all(
        self,
        *,
        id: Optional[int] = None,
        slug: Optional[str] = None,
        private: Optional[bool] = None,
        installation_id: Optional[str] = None,
        is_active: Optional[bool] = None,
        runtime_environment_name: Optional[str] = None,
        info_manager: Optional[bool] = None,
        pipfile_requirements_manager: Optional[bool] = None,
        udpate_manager: Optional[bool] = None,
        version_manager: Optional[bool] = None,
        thoth_advise_manager: Optional[bool] = None,
        thoth_provenance_manager: Optional[bool] = None,
        last_run_before: Optional[datetime] = None,
        last_run_after: Optional[datetime] = None,
        external_python_software_stack_id: Optional[int] = None,
        external_software_environment_id: Optional[int] = None,
        advised_python_software_stack_id: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """Get all github kebechet installations with optional filters on values

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_kebechet_github_installations_all()
        [
            {
                "id": 0,
                "slug": "thoth-station/storages",
                "repo_name": "storages",
                "private": False,
                "is_active": True,
                "info_manager": True,
                "pipfile_requirements_manager": True,
                ...
            },
            ...
        ]
        :rtype: List[Dict[str, Any]]
        :returns: A list of kebechet installations which match the applied filters
        """
        with self._session_scope() as session:
            query = session.query(KebechetGithubAppInstallations)
            if id is not None:
                query = query.filter(KebechetGithubAppInstallations.id == id)
            if slug is not None:
                query = query.filter(KebechetGithubAppInstallations.slug == slug)
            if private is not None:
                query = query.filter(KebechetGithubAppInstallations.private == private)
            if installation_id is not None:
                query = query.filter(KebechetGithubAppInstallations.installation_id == installation_id)
            if is_active is not None:
                query = query.filter(KebechetGithubAppInstallations.is_active == is_active)
            if runtime_environment_name is not None:
                query = query.filter(
                    KebechetGithubAppInstallations.runtime_environment_name == runtime_environment_name
                )
            if info_manager is not None:
                query = query.filter(KebechetGithubAppInstallations.info_manager == info_manager)
            if pipfile_requirements_manager is not None:
                query = query.filter(
                    KebechetGithubAppInstallations.pipfile_requirements_manager == pipfile_requirements_manager
                )
            if update_manager is not None:
                query = query.filter(KebechetGithubAppInstallations.update_manager == update_manager)
            if version_manager is not None:
                query = query.filter(KebechetGithubAppInstallations.version_manager == version_manager)
            if thoth_advise_manager is not None:
                query = query.filter(KebechetGithubAppInstallations.thoth_advise_manager == thoth_advise_manager)
            if thoth_provenance_manager is not None:
                query = query.filter(
                    KebechetGithubAppInstallations.thoth_provenance_manager == thoth_provenance_manager
                )
            if last_run_before is not None:
                query = query.filter(KebechetGithubAppInstallations.last_run <= last_run_before)
            if last_run_after is not None:
                query = query.filter(KebechetGithubAppInstallations.last_run >= last_run_after)
            if external_python_software_stack_id is not None:
                query = query.filter(
                    KebechetGithubAppInstallations.external_python_software_stack_id
                    == external_python_software_stack_id
                )
            if external_software_environment_id is not None:
                query = query.filter(
                    KebechetGithubAppInstallations.external_software_environment_id == external_software_environment_id
                )
            if advised_python_software_stack_id is not None:
                query = query.filter(
                    KebechetGithubAppInstallations.advised_python_software_stack_id == advised_python_software_stack_id
                )

            return [i.to_dict() for i in query.all()]

    def delete_kebechet_github_app_installations(
        self,
        *,
        id: Optional[int] = None,
        slug: Optional[str] = None,
        private: Optional[bool] = None,
        installation_id: Optional[str] = None,
        is_active: Optional[bool] = None,
        runtime_environment_name: Optional[str] = None,
        info_manager: Optional[bool] = None,
        pipfile_requirements_manager: Optional[bool] = None,
        udpate_manager: Optional[bool] = None,
        version_manager: Optional[bool] = None,
        thoth_advise_manager: Optional[bool] = None,
        thoth_provenance_manager: Optional[bool] = None,
        last_run_before: Optional[datetime] = None,
        last_run_after: Optional[datetime] = None,
        external_python_software_stack_id: Optional[int] = None,
        external_software_environment_id: Optional[int] = None,
        advised_python_software_stack_id: Optional[int] = None,
    ) -> int:
        """Delete github kebechet installations which match the given filters

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.delete_kebechet_github_app_installations(slug="foo/bar", runtime_environment_name="baz")
        [
            {
                "id": 0,
                "slug": "thoth-station/storages",
                "repo_name": "storages",
                "private": False,
                "is_active": True,
                "info_manager": True,
                "pipfile_requirements_manager": True,
                ...
            },
            ...
        ]
        :rtype: int
        :returns: Number of entries which have been deleted
        """
        with self._session_scope() as session:
            query = session.query(KebechetGithubAppInstallations)
            if id is not None:
                query = query.filter(KebechetGithubAppInstallations.id == id)
            if slug is not None:
                query = query.filter(KebechetGithubAppInstallations.slug == slug)
            if private is not None:
                query = query.filter(KebechetGithubAppInstallations.private == private)
            if installation_id is not None:
                query = query.filter(KebechetGithubAppInstallations.installation_id == installation_id)
            if is_active is not None:
                query = query.filter(KebechetGithubAppInstallations.is_active == is_active)
            if runtime_environment_name is not None:
                query = query.filter(
                    KebechetGithubAppInstallations.runtime_environment_name == runtime_environment_name
                )
            if info_manager is not None:
                query = query.filter(KebechetGithubAppInstallations.info_manager == info_manager)
            if pipfile_requirements_manager is not None:
                query = query.filter(
                    KebechetGithubAppInstallations.pipfile_requirements_manager == pipfile_requirements_manager
                )
            if update_manager is not None:
                query = query.filter(KebechetGithubAppInstallations.update_manager == update_manager)
            if version_manager is not None:
                query = query.filter(KebechetGithubAppInstallations.version_manager == version_manager)
            if thoth_advise_manager is not None:
                query = query.filter(KebechetGithubAppInstallations.thoth_advise_manager == thoth_advise_manager)
            if thoth_provenance_manager is not None:
                query = query.filter(
                    KebechetGithubAppInstallations.thoth_provenance_manager == thoth_provenance_manager
                )
            if last_run_before is not None:
                query = query.filter(KebechetGithubAppInstallations.last_run <= last_run_before)
            if last_run_after is not None:
                query = query.filter(KebechetGithubAppInstallations.last_run >= last_run_after)
            if external_python_software_stack_id is not None:
                query = query.filter(
                    KebechetGithubAppInstallations.external_python_software_stack_id
                    == external_python_software_stack_id
                )
            if external_software_environment_id is not None:
                query = query.filter(
                    KebechetGithubAppInstallations.external_software_environment_id == external_software_environment_id
                )
            if advised_python_software_stack_id is not None:
                query = query.filter(
                    KebechetGithubAppInstallations.advised_python_software_stack_id == advised_python_software_stack_id
                )
            count = query.count()
            query.delete()
            return count

    def update_kebechet_github_installations_on_is_active(self, slug: str) -> bool:
        """Deactivate the app on getting an uninstall event.

        Passed a slug name to be deactivated.
        Example - slug:'thoth-station/advisor'
        :rtype: True, False
        :returns True: if installation existed and was deactivated.
        :returns False: if installation was not found.
        """
        with self._session_scope() as session:
            instances = session.query(KebechetGithubAppInstallations).filter(
                KebechetGithubAppInstallations.slug == slug
            )
            if instances.all() == []:
                raise NotFoundError(f"No entries found for slug={slug}")

            instances.update({"is_active": False}, synchronize_session="fetch")

            session.commit()
            return True

    def get_active_kebechet_github_installations_repos(self) -> List[str]:
        """Get all active repositories names with active Kebechet installation.

         Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_active_kebechet_github_installations_repos()
        ['repository_foo_fullname', 'repository_bar_fullname', ...]
        """
        with self._session_scope() as session:
            active_installations = (
                session.query(KebechetGithubAppInstallations)
                .filter(KebechetGithubAppInstallations.is_active.is_(True))
                .with_entities(KebechetGithubAppInstallations.slug)
                .all()
            )

            return [obj[0] for obj in active_installations]

    def get_active_kebechet_github_installations_repos_count_all(self) -> int:
        """Return the count of active repos with Kebechet installation.

        Example:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.connect()
        >>> graph.get_active_kebechet_github_installations_repos_count_all()
        165
        """
        with self._session_scope() as session:
            count = (
                session.query(KebechetGithubAppInstallations)
                .filter(KebechetGithubAppInstallations.is_active.is_(True))
                .distinct(KebechetGithubAppInstallations.slug)  # so we only get one entry from each installation
                .count()
            )
            return count

    def get_kebechet_github_installations_active_managers(
        self, slug: str, runtime_environment_name: Optional[str] = None
    ) -> list:
        """Return the list of active managers for a particular repository.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_kebechet_github_installations_active_managers(
            slug="thoth-station/srcops-testing"
        )
        ['thoth_advise_manager']
        """
        with self._session_scope() as session:
            instance = (
                session.query(KebechetGithubAppInstallations)
                .filter(KebechetGithubAppInstallations.is_active.is_(True))
                .filter(KebechetGithubAppInstallations.slug == slug)
                .filter(KebechetGithubAppInstallations.runtime_environment_name == runtime_environment_name)
                .with_entities(
                    KebechetGithubAppInstallations.info_manager,
                    KebechetGithubAppInstallations.pipfile_requirements_manager,
                    KebechetGithubAppInstallations.update_manager,
                    KebechetGithubAppInstallations.version_manager,
                    KebechetGithubAppInstallations.thoth_advise_manager,
                    KebechetGithubAppInstallations.thoth_provenance_manager,
                )
                .first()
            )

            return [manager for manager, is_active in instance._asdict().items() if is_active == True]

    def get_kebechet_github_installations_active_managers_count_all(
        self, kebechet_manager: str, distinct: bool = False
    ) -> int:
        """Return the number of repos with specific manager active.

        :rtype: int
        :returns Number of active records for registered Kebechet manager.
        """
        if kebechet_manager not in KebechetManagerEnum._member_names_:
            raise NotFoundError(
                f"Manager {kebechet_manager!r} is not valid manager name. "
                f"Registered managers names are: {KebechetManagerEnum._member_names_!r}"
            )
        with self._session_scope() as session:
            query = (
                session.query(KebechetGithubAppInstallations)
                .filter(KebechetGithubAppInstallations.is_active.is_(True))
                .distinct(KebechetGithubAppInstallations.slug)
            )
            # we make slug distinct here so that we don't double count when the repo has multiple runtime environments

            if kebechet_manager == KebechetManagerEnum.INFO_MANAGER.name:
                query = query.filter(KebechetGithubAppInstallations.info_manager.is_(True))

            if kebechet_manager == KebechetManagerEnum.PIPFILE_REQUIREMENTS_MANAGER.name:
                query = query.filter(KebechetGithubAppInstallations.pipfile_requirements_manager.is_(True))

            if kebechet_manager == KebechetManagerEnum.UPDATE_MANAGER.name:
                query = query.filter(KebechetGithubAppInstallations.update_manager.is_(True))

            if kebechet_manager == KebechetManagerEnum.VERSION_MANAGER.name:
                query = query.filter(KebechetGithubAppInstallations.version_manager.is_(True))

            if kebechet_manager == KebechetManagerEnum.THOTH_ADVISE_MANAGER.name:
                query = query.filter(KebechetGithubAppInstallations.thoth_advise_manager.is_(True))

            if kebechet_manager == KebechetManagerEnum.THOTH_PROVENANCE_MANAGER.name:
                query = query.filter(KebechetGithubAppInstallations.thoth_provenance_manager.is_(True))

            if distinct:
                query = query.distinct()

            return query.count()

    def get_kebechet_github_installation_info_with_software_environment_all(
        self,
        *,
        python_version: Optional[str] = None,
        image_name: Optional[str] = None,
        image_sha: Optional[str] = None,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        thoth_s2i_image_name: Optional[str] = None,
        thoth_s2i_image_version: Optional[str] = None,
        env_image_name: Optional[str] = None,
        env_image_tag: Optional[str] = None,
        cuda_version: Optional[str] = None,
        environment_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get all github kebechet installations with optional filters on software environment

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_kebechet_github_installation_info_with_software_environment_all()
        [
            {
                "id": 0,
                "slug": "thoth-station/storages",
                "repo_name": "storages",
                "private": False,
                "is_active": True,
                "info_manager": True,
                "pipfile_requirements_manager": True,
                ...
            },
            ...
        ]
        :rtype: List[Dict[str, Any]]
        :returns: A list of kebechet installations which match the applied filters
        """
        with self._session_scope() as session, session.begin(subtransactions=True):
            query = (
                session.query(KebechetGithubAppInstallations)
                .filter(KebechetGithubAppInstallations.is_active.is_(True))
                .join(ExternalSoftwareEnvironment)
            )

            if python_version:
                query = query.filter(ExternalSoftwareEnvironment.python_version == python_version)
            if image_name:
                query = query.filter(ExternalSoftwareEnvironment.image_name == image_name)
            if image_sha:
                query = query.filter(ExternalSoftwareEnvironment.image_sha == image_sha)
            if os_name:
                query = query.filter(ExternalSoftwareEnvironment.os_name == map_os_name(os_name))
            if os_version:
                os_version = normalize_os_version(os_name, os_version)
                query = query.filter(ExternalSoftwareEnvironment.os_version == os_version)
            if thoth_s2i_image_name:
                query = query.filter(ExternalSoftwareEnvironment.thoth_s2i_image_name == thoth_s2i_image_name)
            if thoth_s2i_image_version:
                query = query.filter(ExternalSoftwareEnvironment.thoth_s2i_image_version == thoth_s2i_image_version)
            if env_image_name:
                query = query.filter(ExternalSoftwareEnvironment.env_image_name == env_image_name)
            if env_image_tag:
                query = query.filter(ExternalSoftwareEnvironment.cuda_version == cuda_version)
            if environment_type:
                query = query.filter(ExternalSoftwareEnvironment.environment_type == environment_type)

            return [i.to_dict() for i in query.all()]

    def get_kebechet_github_installations_info_for_python_package_version(
        self,
        package_name: str,
        *,
        package_version: Optional[str] = None,
        index_url: Optional[str] = None,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
    ) -> Dict[str, Dict[str, Any]]:
        """Return info about repo containing Python Package in the software stack.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_kebechet_github_installations_info_for_python_package_version(
            package_name='click'
            index_url="https://pypi.org/simple",
        )

        {
            'thoth-station/jupyter-nbrequirements':
                {
                    'installation_id': '193650988',
                    'private': False,
                    'package_name': 'click',
                    'package_version': '7.1.2',
                    'index_url': 'https://pypi.org/simple'}
                }
        """
        package_name = self.normalize_python_package_name(package_name)
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)

        with self._session_scope() as session, session.begin(subtransactions=True):
            query = (
                session.query(KebechetGithubAppInstallations)
                .filter(KebechetGithubAppInstallations.is_active.is_(True))
                .join(ExternalPythonSoftwareStack)
                .join(ExternalPythonRequirementsLock)
                .join(HasExternalPythonRequirementsLock)
                .join(PythonPackageVersionEntity)
                .filter(PythonPackageVersionEntity.package_name == package_name)
            )

            if index_url:
                index_url = self.normalize_python_index_url(index_url)

                conditions = [
                    PythonPackageVersionEntity.python_package_index_id == PythonPackageIndex.id,
                    PythonPackageVersionEntity.python_package_index_id.is_(None),
                ]

            if package_version:
                package_version = self.normalize_python_package_version(package_version)
                query = query.filter(PythonPackageVersionEntity.package_version == package_version)

            if any(se for se in [os_name, os_version, python_version]):
                query = query.join(ExternalSoftwareEnvironment)

            if os_name:
                query = query.filter(ExternalSoftwareEnvironment.os_name == os_name)

            if os_version:
                query = query.filter(ExternalSoftwareEnvironment.os_version == os_version)

            if python_version:
                query = query.filter(ExternalSoftwareEnvironment.python_version == python_version)

            if index_url:
                query = query.filter(exists().where(or_(*conditions)))

            query = query.with_entities(
                KebechetGithubAppInstallations.slug,
                KebechetGithubAppInstallations.installation_id,
                KebechetGithubAppInstallations.private,
                PythonPackageVersionEntity.package_name,
                PythonPackageVersionEntity.package_version,
                PythonPackageVersionEntity.python_package_index_id,
            )

            result = query.all()

        return self._group_by_slug(result)

    def update_kebechet_installation_using_files(
        self,
        slug: str,
        installation_id: str,
        requirements: Optional[dict] = None,
        requirements_lock: Optional[dict] = None,
        thoth_config: Optional[dict] = None,
        runtime_environment_name: Optional[str] = None,
        private: bool = False,
    ):
        """Update info about kebechet installation."""
        with self._session_scope() as session, session.begin(subtransactions=True):
            if "runtime_environments" in thoth_config:
                if runtime_environment_name is None:
                    env_dict = thoth_config["runtime_environments"][0]
                else:
                    for env in thoth_config["runtime_environments"]:
                        if env["name"] == runtime_environment_name:
                            env_dict = env
                    else:
                        raise ValueError(f"No environment {runtime_environment_name} found in thoth configuration")

                os_name = map_os_name(env_dict["operating_system"]["name"])
                os_version = env_dict["operating_system"]["version"]

                software_env = ExternalSoftwareEnvironment.get_or_create(
                    session=session,
                    environment_name=env_dict["name"],
                    os_name=os_name,
                    os_version=normalize_os_version(os_name, os_version),
                    python_version=env_dict.get("python_version"),
                    cuda_version=env_dict.get("cuda_version"),
                    environment_type=EnvironmentTypeEnum.RUNTIME.value,
                )[0]
            else:
                software_env = None

            python_stack = self._create_python_software_stack(
                session=session,
                requirements=requirements,
                requirements_lock=requirements_lock,
                software_environment=software_env,
                is_external=True,
            )

            manager_info = thoth_config.get("managers") or {}

            all_managers = [i["name"] for i in manager_info]
            item = (
                session.query(KebechetGithubAppInstallations)
                .filter(KebechetGithubAppInstallations.slug == slug)
                .filter(KebechetGithubAppInstallations.runtime_environment_name == runtime_environment_name)
                .first()
            )
            if item is None:
                KebechetGithubAppInstallations.get_or_create(
                    session=session,
                    slug=slug,
                    repo_name=slug.split("/")[1],
                    installation_id=installation_id,
                    private=private,
                    is_active=True,
                    runtime_environment_name=runtime_environment_name,
                    external_python_software_stack_id=python_stack.id,
                    external_software_environment_id=software_env.id,
                    info_manager="info" in all_managers,
                    pipfile_requirements_manager="pipfile-requirements" in all_managers,
                    update_manager="update" in all_managers,
                    version_manager="version" in all_managers,
                    thoth_advise_manager="thoth-advise" in all_managers,
                    thoth_provenance_manager="thoth-provenance" in all_managers,
                )
            else:
                session.query(KebechetGithubAppInstallations).filter(
                    KebechetGithubAppInstallations.id == item.id
                ).update(
                    {
                        "slug": slug,
                        "repo_name": slug.split("/")[1],
                        "installation_id": installation_id,
                        "private": private,
                        "is_active": True,
                        "runtime_environment_name": runtime_environment_name,
                        "external_python_software_stack_id": python_stack.id,
                        "external_software_environment_id": software_env.id,
                        "info_manager": "info" in all_managers,
                        "pipfile_requirements_manager": "pipfile-requirements" in all_managers,
                        "update_manager": "update" in all_managers,
                        "version_manager": "version" in all_managers,
                        "thoth_advise_manager": "thoth-advise" in all_managers,
                        "thoth_provenance_manager": "thoth-provenance" in all_managers,
                    }
                )

    def get_index_url_from_id(self, package_index_id: int) -> str:
        """Return index URL from id."""
        with self._session_scope() as session:
            output = (
                session.query(PythonPackageIndex)
                .filter(PythonPackageIndex.id == package_index_id)
                .with_entities(PythonPackageIndex.url)
                .first()
            )

        return output[0]

    def _group_by_slug(
        self,
        result: Union[List, Dict[str, Any]],
    ) -> Dict[str, List[Tuple[str, str]]]:
        """Format Query result to group by package name."""
        query_result = {}

        for item in result:
            if item[5]:
                index_url = self.get_index_url_from_id(item[5])
            else:
                index_url = item[5]

            query_result[item[0]] = {
                "installation_id": item[1],
                "private": item[2],
                "package_name": item[3],
                "package_version": item[4],
                "index_url": index_url,
            }

        return query_result

    def create_python_package_version_entity(
        self,
        package_name: str,
        package_version: Optional[str] = None,
        index_url: Optional[str] = None,
        *,
        only_if_package_seen: bool = False,
    ) -> Optional[Tuple[PythonPackageVersionEntity, bool]]:
        """Create a Python package version entity record in the system.

        By creating this entity, the system will record and track the given package.
        """
        index_url = self.normalize_python_index_url(index_url)
        package_name = self.normalize_python_package_name(package_name)
        if package_version is not None:
            package_version = self.normalize_python_package_version(package_version)

        with self._session_scope() as session:
            if only_if_package_seen:
                seen_count = (
                    session.query(PythonPackageVersionEntity)
                    .filter(PythonPackageVersionEntity.package_name == package_name)
                    .count()
                )

                if seen_count == 0:
                    return None

            index = None
            if index_url:
                index = self._get_or_create_python_package_index(session, index_url, only_if_enabled=False)

            entity, existed = PythonPackageVersionEntity.get_or_create(
                session,
                package_name=package_name,
                package_version=package_version,
                python_package_index_id=index.id if index else None,
            )
            self._refresh_rules_python_entity(session, entity)
            return entity, existed

    def _delete_python_package_version(
        self,
        *,
        package_name: str,
        package_version: str,
        index_url: str,
        os_name: str,
        os_version: str,
        python_version: str,
    ) -> int:
        """Delete the given package-version entry."""
        # We use join so raw delete() cannot be used.
        deleted_count = 0
        with self._session_scope() as session:
            for pv_id in (
                session.query(PythonPackageVersion)
                .join(PythonPackageIndex)
                .filter(
                    PythonPackageVersion.package_name == package_name,
                    PythonPackageVersion.package_version == package_version,
                    PythonPackageVersion.os_name == os_name,
                    PythonPackageVersion.os_version == os_version,
                    PythonPackageVersion.python_version == python_version,
                    PythonPackageIndex.url == index_url,
                )
                .with_entities(PythonPackageVersion.id)
                .all()
            ):
                session.query(PythonPackageVersion).filter(PythonPackageVersion.id == pv_id).delete()
                deleted_count += 1

        return deleted_count

    def _create_python_package_version(
        self,
        session: Session,
        package_name: str,
        package_version: Union[str, None],
        index_url: Union[str, None],
        *,
        os_name: Union[str, None],
        os_version: Union[str, None],
        python_version: Union[str, None],
        python_package_metadata_id: int = None,
        sync_only_entity: bool = False,
    ) -> Union[PythonPackageVersion, PythonPackageVersionEntity]:
        """Create a Python package version.

        Make sure it is properly mirrored with a Python package entity and connected to a Python package index.
        """
        package_name = self.normalize_python_package_name(package_name)
        if package_version is not None:
            package_version = self.normalize_python_package_version(package_version)

        index = None
        if index_url is not None:
            index_url = self.normalize_python_index_url(index_url)
            index = self._get_or_create_python_package_index(session, index_url, only_if_enabled=False)

        entity, _ = PythonPackageVersionEntity.get_or_create(
            session,
            package_name=package_name,
            package_version=package_version,
            python_package_index_id=index.id if index else None,
        )
        self._refresh_rules_python_entity(session, entity)

        if sync_only_entity:
            return entity

        python_package_version, _ = PythonPackageVersion.get_or_create(
            session,
            package_name=package_name,
            package_version=package_version,
            python_package_index_id=index.id if index else None,
            os_name=os_name,
            os_version=os_version,
            python_version=python_version,
            entity_id=entity.id,
            python_package_metadata_id=python_package_metadata_id,
        )

        return python_package_version

    @staticmethod
    def _create_fuzzy_hash(sorted_ids: List[int]) -> str:
        """Create fuzzy hash from sorted list of integers.

        Reference: https://pypi.org/project/python-ssdeep/
        Reference: https://docs.python.org/3/library/stdtypes.html#int.to_bytes
        """
        hash_ = ""
        for object_id in sorted_ids:
            # length of bytes required for the integer
            length = (object_id.bit_length() + 7) // 8
            # no negative ids are passed
            hash_ += ssdeep.hash(object_id.to_bytes(length=length, byteorder="big"))
        return hash_

    def _create_python_software_stack(
        self,
        session: Session,
        software_stack_type: Optional[str] = None,
        requirements: dict = None,
        requirements_lock: dict = None,
        software_environment: SoftwareEnvironment = None,
        *,
        performance_score: float = None,
        overall_score: float = None,
        is_external: bool = False,
    ) -> PythonSoftwareStack:
        """Create a Python software stack out of its JSON/dict representation."""
        if requirements is not None:
            python_package_requirements = self._create_python_package_requirement(session, requirements)
            # Create unique hash for requirements to go into PythonRequirements
            requirements_ids = [int(ppr.id) for ppr in python_package_requirements]
            requirements_ids.sort()
            requirements_hash = self._create_fuzzy_hash(requirements_ids)

            if is_external:
                python_requirements, _ = ExternalPythonRequirements.get_or_create(
                    session,
                    requirements_hash=requirements_hash,
                )

                for python_requirement in python_package_requirements:
                    HasExternalPythonRequirements.get_or_create(
                        session,
                        external_python_requirements_id=python_requirements.id,
                        python_package_requirement_id=python_requirement.id,
                    )
            else:
                python_requirements, _ = PythonRequirements.get_or_create(
                    session,
                    requirements_hash=requirements_hash,
                )

                for python_requirement in python_package_requirements:
                    HasPythonRequirements.get_or_create(
                        session,
                        python_requirements_id=python_requirements.id,
                        python_package_requirement_id=python_requirement.id,
                    )

        if requirements_lock is not None:
            python_package_versions = self._create_python_packages_pipfile(
                session, requirements_lock, software_environment=software_environment, sync_only_entity=is_external
            )
            # Create unique hash for requirements locked to go to PythonRequirementsLock
            requirements_lock_ids = [int(ppv.id) for ppv in python_package_versions]
            requirements_lock_ids.sort()
            requirements_lock_hash = self._create_fuzzy_hash(requirements_lock_ids)

            if is_external:
                external_python_requirements_lock, _ = ExternalPythonRequirementsLock.get_or_create(
                    session,
                    requirements_lock_hash=requirements_lock_hash,
                )

                for python_package_version_entity in python_package_versions:
                    HasExternalPythonRequirementsLock.get_or_create(
                        session,
                        external_python_requirements_locked_id=external_python_requirements_lock.id,
                        python_package_version_entity_id=python_package_version_entity.id,
                    )

            else:

                python_requirements_lock, _ = PythonRequirementsLock.get_or_create(
                    session,
                    requirements_lock_hash=requirements_lock_hash,
                )

                for python_package_version in python_package_versions:
                    HasPythonRequirementsLock.get_or_create(
                        session,
                        python_requirements_lock_id=python_requirements_lock.id,
                        python_package_version_id=python_package_version.id,
                    )

        if is_external:
            # User can submit software stack with only Pipfile
            if requirements_lock is None:
                external_python_requirements_lock, _ = ExternalPythonRequirementsLock.get_or_create(
                    session,
                    requirements_lock_hash=self._create_fuzzy_hash([0]),
                )

                software_stack, _ = ExternalPythonSoftwareStack.get_or_create(
                    session,
                    external_python_requirements_id=python_requirements.id,
                    external_python_requirements_lock_id=external_python_requirements_lock.id,
                )
            else:
                software_stack, _ = ExternalPythonSoftwareStack.get_or_create(
                    session,
                    external_python_requirements_id=python_requirements.id,
                    external_python_requirements_lock_id=external_python_requirements_lock.id,
                )
        else:
            software_stack, _ = PythonSoftwareStack.get_or_create(
                session,
                performance_score=performance_score,
                overall_score=overall_score,
                software_stack_type=software_stack_type,
                python_requirements_id=python_requirements.id,
                python_requirements_lock_id=python_requirements_lock.id,
            )

        return software_stack

    def get_python_software_stack_count_all(
        self, is_external: bool = False, software_stack_type: Optional[str] = None, distinct: bool = False
    ) -> int:
        """Get number of Python software stacks available filtered by type."""
        with self._session_scope() as session:
            if is_external:
                query = session.query(ExternalPythonSoftwareStack)
            else:
                query = session.query(PythonSoftwareStack.software_stack_type).filter(
                    PythonSoftwareStack.software_stack_type == software_stack_type
                )

                if distinct:
                    return query.distinct().count()

            return query.count()

    def sync_inspection_result(self, document) -> None:
        """Sync the given inspection document into the graph database."""
        # Check if we have such performance model before creating any other records.
        inspection_document_id = document["document_id"]
        inspection_result_number = document["result_number"]
        inspection_specification = document["specification"]
        inspection_result = document["result"]

        with self._session_scope() as session, session.begin(subtransactions=True):
            build_cpu = OpenShift.parse_cpu_spec(inspection_specification["build"]["requests"]["cpu"])
            build_memory = OpenShift.parse_memory_spec(inspection_specification["build"]["requests"]["memory"])
            run_cpu = OpenShift.parse_cpu_spec(inspection_specification["run"]["requests"]["cpu"])
            run_memory = OpenShift.parse_memory_spec(inspection_specification["run"]["requests"]["memory"])

            # Convert bytes to GiB, we need float number given the fixed int size.
            run_memory = run_memory / (1024 ** 3)
            build_memory = build_memory / (1024 ** 3)

            runtime_environment = inspection_result["runtime_environment"]

            run_hardware_information, run_software_environment = self._runtime_environment_conf2models(
                session, runtime_environment, environment_type=EnvironmentTypeEnum.RUNTIME.value, is_external=False
            )

            runtime_environment["hardware"] = inspection_specification["build"]["requests"]["hardware"]

            build_hardware_information, build_software_environment = self._runtime_environment_conf2models(
                session, runtime_environment, environment_type=EnvironmentTypeEnum.BUILDTIME.value, is_external=False
            )

            software_stack = None
            if "python" in inspection_specification:
                # Inspection stack.
                software_stack = self._create_python_software_stack(
                    session,
                    software_stack_type=SoftwareStackTypeEnum.INSPECTION.value,
                    requirements=inspection_specification["python"].get("requirements"),
                    requirements_lock=inspection_specification["python"].get("requirements_locked"),
                    software_environment=run_software_environment,
                    performance_score=None,
                    overall_score=None,
                )

            inspection_run = (
                session.query(InspectionRun)
                .filter(InspectionRun.inspection_document_id == inspection_document_id)
                .filter(InspectionRun.inspection_result_number == inspection_result_number)
                .first()
            )

            if inspection_run and inspection_run.dependency_monkey_run_id:
                # Inspection was run through Dependency Monkey

                # INSERT…ON CONFLICT (Upsert)
                # https://docs.sqlalchemy.org/en/13/dialects/postgresql.html?highlight=conflict#insert-on-conflict-upsert
                # https://docs.sqlalchemy.org/en/13/errors.html#sql-expression-language compile required
                insert_stmt = insert(InspectionRun).values(
                    id=inspection_run.dependency_monkey_run_id,
                    inspection_document_id=inspection_document_id,
                    inspection_result_number=inspection_result_number,
                    dependency_monkey_run_id=inspection_run.dependency_monkey_run_id,
                    inspection_sync_state=InspectionSyncStateEnum.PENDING.value,
                )
                do_update_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=["id"],
                    set_=dict(
                        inspection_sync_state=InspectionSyncStateEnum.SYNCED.value,
                        inspection_document_id=inspection_document_id,
                        inspection_result_number=inspection_result_number,
                        datetime=inspection_specification.get("@created"),
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
                    ),
                )

                session.execute(do_update_stmt)

            else:
                inspection_run, _ = InspectionRun.get_or_create(
                    session,
                    inspection_sync_state=InspectionSyncStateEnum.SYNCED.value,
                    inspection_document_id=inspection_document_id,
                    inspection_result_number=inspection_result_number,
                    datetime=inspection_specification.get("@created"),
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

            if inspection_specification.get("script"):  # We have run an inspection job.

                if not inspection_result["stdout"]:
                    raise ValueError("No values provided for inspection output %r", inspection_document_id)

                performance_indicator_name = inspection_result.get("name")
                performance_model_class = PERFORMANCE_MODEL_BY_NAME.get(performance_indicator_name)

                if not performance_model_class:
                    raise PerformanceIndicatorNotRegistered(
                        f"No performance indicator registered for name {performance_indicator_name!r}"
                    )

                performance_indicator, _ = performance_model_class.create_from_report(
                    session,
                    inspection_specification=inspection_specification,
                    inspection_result=inspection_result,
                    inspection_run_id=inspection_run.id,
                )

    def create_python_cve_record(
        self,
        package_name: str,
        package_version: str,
        index_url: str,
        *,
        cve_id: str,
        details: str,
    ) -> bool:
        """Store information about a CVE in the graph database for the given Python package."""
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)
        index_url = self.normalize_python_index_url(index_url)

        with self._session_scope() as session:
            cve = session.query(CVE).filter(CVE.cve_id == cve_id).first()
            if not cve:
                cve, _ = CVE.get_or_create(
                    session,
                    cve_id=cve_id,
                    details=details,
                    aggregated_at=datetime.utcnow(),
                )

            index = self._get_or_create_python_package_index(session, index_url, only_if_enabled=False)
            entity, e = PythonPackageVersionEntity.get_or_create(
                session,
                package_name=package_name,
                package_version=package_version,
                python_package_index_id=index.id,
            )

            self._refresh_rules_python_entity(session, entity)
            _, existed = HasVulnerability.get_or_create(
                session, cve_id=cve.id, python_package_version_entity_id=entity.id
            )

            return existed

    def update_missing_flag_package_version(
        self, package_name: str, package_version: str, index_url: str, value: bool
    ) -> None:
        """Update value of is_missing flag for PythonPackageVersion."""
        index_url = self.normalize_python_index_url(index_url)
        with self._session_scope() as session:
            subq = (
                session.query(PythonPackageVersion)
                .join(PythonPackageIndex)
                .filter(PythonPackageVersion.package_name == package_name)
                .filter(PythonPackageVersion.package_version == package_version)
                .filter(PythonPackageIndex.url == index_url)
                .with_entities(PythonPackageVersion.id)
            )
            (
                session.query(PythonPackageVersion)
                .filter(PythonPackageVersion.id.in_(subq))
                .update({"is_missing": value}, synchronize_session="fetch")
            )

    def update_provides_source_distro_package_version(
        self, package_name: str, package_version: str, index_url: str, value: bool
    ) -> None:
        """Update value of is_si_analyzable flag for PythonPackageVersion."""
        index_url = self.normalize_python_index_url(index_url)
        with self._session_scope() as session:
            subq = (
                session.query(PythonPackageVersion)
                .join(PythonPackageIndex)
                .filter(PythonPackageVersion.package_name == package_name)
                .filter(PythonPackageVersion.package_version == package_version)
                .filter(PythonPackageIndex.url == index_url)
                .with_entities(PythonPackageVersion.id)
            )
            (
                session.query(PythonPackageVersion)
                .filter(PythonPackageVersion.id.in_(subq))
                .update({"provides_source_distro": value}, synchronize_session="fetch")
            )

    def is_python_package_version_is_missing(self, package_name: str, package_version: str, index_url: str) -> bool:
        """Check whether is_missing flag is set for python package version."""
        index_url = self.normalize_python_index_url(index_url)
        with self._session_scope as session:
            query = (
                session.query(PythonPackageVersion)
                .join(PythonPackageIndex)
                .filter(PythonPackageVersion.package_name == package_name)
                .filter(PythonPackageVersion.package_version == package_version)
                .filter(PythonPackageIndex.url == index_url)
                .with_entities(PythonPackageVersion.is_missing)
            )

            if query.first() is None:
                raise NotFoundError(
                    f"The given package {package_name!r} in version {package_version!r} "
                    f"from {index_url!r} was not found"
                )

            return query.first()[0]

    def get_adviser_run_origins_all(
        self,
        package_name: Optional[str] = None,
        package_version: Optional[str] = None,
        index_url: Optional[str] = None,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        distinct: bool = False,
    ) -> List[str]:
        """Retrieve all origins (git repos URLs) in Adviser Run.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_adviser_run_origins_all()
        ['https://github.com/thoth-station/storages',
         'https://github.com/thoth-station/user-api',
         'https://github.com/thoth-station/adviser']
        """
        index_url = self.normalize_python_index_url(index_url)
        with self._session_scope() as session:
            query = session.query(AdviserRun).order_by(AdviserRun.origin).order_by(AdviserRun.datetime.desc())

            if package_name or package_version:
                query = query.join(
                    ExternalPythonRequirementsLock,
                    ExternalPythonRequirementsLock.python_software_stack_id == AdviserRun.user_software_stack_id,
                ).join(
                    PythonPackageVersion,
                    ExternalPythonRequirementsLock.python_package_version_entity_id == PythonPackageVersion.id,
                )
                if index_url is not None:
                    query = query.join(PythonPackageIndex)
                    query = query.filter(PythonPackageIndex.url == index_url)

            if package_name is not None:
                package_name = self.normalize_python_package_name(package_name)
                query = query.filter(PythonPackageVersion.package_name == package_name)

            if package_version is not None:
                package_version = self.normalize_python_package_version(package_version)
                query = query.filter(PythonPackageVersion.package_version == package_version)

            query = query.offset(start_offset).limit(count)

            query = query.with_entities(AdviserRun.origin)

            if distinct:
                query = query.distinct()

            result = [r[0] for r in query.all() if r[0]]  # We do not consider None results

            return result

    @staticmethod
    def _filter_source_type(results: List[any]) -> Dict[str, int]:
        """Filter results per source type."""
        return {
            source_result[0]: source_result[1]
            for source_result in results
            if source_result[0] in ThothAdviserIntegrationEnum._member_names_
        }

    def get_adviser_run_count_per_source_type(
        self,
    ) -> Dict[str, int]:
        """Retrieve number of Adviser run per source type in Thoth Database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_adviser_run_count_per_source_type()
        {'GITHUB_APP': 154, 'CLI': 71}
        """
        with self._session_scope() as session:
            query = session.query(AdviserRun.source_type, func.count(AdviserRun.source_type)).group_by(
                AdviserRun.source_type
            )

            results = query.all()

        return self._filter_source_type(results=results)

    @staticmethod
    def _create_date_filter(date_: str) -> datetime:
        """Create date filter.

        @params date_: DD-MM-YY
        """
        return datetime.strptime(date_, "%d-%m-%Y").date()

    def get_adviser_run_document_ids_all(
        self,
        initial_date: Optional[str] = None,
        final_date: Optional[str] = None,
        source_type: Optional[str] = None,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
    ) -> List[str]:
        """Retrieve adviser run document ids.

        @params initial_date: DD-MM-YY
        @params final_date: DD-MM-YY

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_adviser_run_document_ids_all()
        ['adviser-343231d']
        """
        with self._session_scope() as session:
            query = session.query(AdviserRun.adviser_document_id).with_entities(AdviserRun.adviser_document_id)

            if initial_date:
                date_filter = self._create_date_filter(initial_date)
                query = query.filter(AdviserRun.datetime > date_filter)

            if final_date:
                date_filter = self._create_date_filter(final_date)
                query = query.filter(AdviserRun.datetime < date_filter)

            if source_type:
                query = query.filter(AdviserRun.source_type == source_type)

            # query = query.offset(start_offset).limit(count)

            document_ids = query.all()

            return [obj[0] for obj in document_ids]

    def get_solver_run_document_ids_all(
        self,
        initial_date: Optional[str] = None,
        final_date: Optional[str] = None,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
        has_error: bool = False,
        unsolvable: bool = False,
        unparseable: bool = False,
    ) -> List[str]:
        """Retrieve solver run document ids.

        @params initial_date: DD-MM-YY
        @params final_date: DD-MM-YY

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_solver_run_document_ids_all()
        ['solver-rhel-8-py38-343231d']
        """
        os_name = map_os_name(os_name)
        os_version = normalize_os_version(os_name, os_version)

        with self._session_scope() as session:
            query = session.query(Solved.document_id).with_entities(Solved.document_id)

            conditions = []

            if os_name or os_version or python_version:
                conditions.append(EcosystemSolver.id == Solved.ecosystem_solver_id)

            if os_name:
                conditions.append(EcosystemSolver.os_name == os_name)

            if os_version:
                os_version = OpenShift.normalize_os_version(os_name, os_version)
                conditions.append(EcosystemSolver.os_version == os_version)

            if python_version:
                conditions.append(EcosystemSolver.python_version == python_version)

            if has_error:
                query = query.filter(Solved.error.is_(True))

            if unsolvable:
                conditions.append(Solved.error_unsolvable.is_(True))

            if unparseable:
                conditions.append(Solved.error_unparseable.is_(True))

            if conditions:
                query = query.filter(exists().where(and_(*conditions)))

            if initial_date:
                date_filter = self._create_date_filter(initial_date)
                query = query.filter(Solved.datetime > date_filter)

            if final_date:
                date_filter = self._create_date_filter(final_date)
                query = query.filter(Solved.datetime < date_filter)

            query = query.offset(start_offset).limit(count)

            document_ids = query.all()

            return [obj[0] for obj in document_ids]

    def get_python_package_version_trove_classifiers_all(
        self,
        package_name: str,
        package_version: str,
        index_url: str,
        *,
        os_name: str,
        os_version: str,
        python_version: str,
    ) -> List[str]:
        """Get Python trove classifiers.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_python_package_version_trove_classifiers_all( \
            "cowsay", "4.0", "https://pypi.org/simple", os_name="rhel", os_version="9", python_version="3.9")
        ["PROGRAMMING LANGUAGE :: PYTHON :: 3.9", "OPERATING SYSTEM :: OS INDEPENDENT"]
        """
        self.normalize_python_package_version(package_version)
        self.normalize_python_package_name(package_name)
        self.normalize_python_index_url(index_url)
        with self._session_scope() as session:
            query = (
                session.query(PythonPackageVersion)
                .filter(
                    PythonPackageVersion.package_name == package_name,
                    PythonPackageVersion.package_version == package_version,
                    PythonPackageVersion.os_name == os_name,
                    PythonPackageVersion.os_version == os_version,
                    PythonPackageVersion.python_version == python_version,
                )
                .join(PythonPackageIndex)
                .filter(PythonPackageIndex.url == index_url)
                .join(PythonPackageMetadata)
                .join(HasMetadataClassifier)
                .join(PythonPackageMetadataClassifier)
                .with_entities(PythonPackageMetadataClassifier.classifier)
            )

            return [i[0] for i in query.all()]

    def get_origin_count_per_source_type(
        self,
        distinct: bool = False,
    ) -> Dict[str, Dict[Tuple[str, str], int]]:
        """Retrieve number of users of adviser per source type.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_origin_count_per_source_type()
        {'KEBECHET': 48, 'JUPYTER_NOTEBOOK': 18, 'CLI': 513}
        >>> graph.get_origin_count_per_source_type(distinct=True)
        {'KEBECHET': 5, 'JUPYTER_NOTEBOOK': 2, 'CLI': 78}
        """
        with self._session_scope() as session:
            query = session.query(AdviserRun.origin)

            if distinct:
                query = query.with_entities(AdviserRun.source_type, func.count(AdviserRun.origin.distinct()))
            else:
                query = query.with_entities(AdviserRun.source_type, func.count(AdviserRun.origin))

            query = query.group_by(AdviserRun.source_type)

            results = query.all()

        return self._filter_source_type(results=results)

    def update_python_package_hash_present_flag(
        self, package_name: str, package_version: str, index_url: str, sha256_hash: str
    ):
        """Remove hash associated with python package in the graph."""
        index_url = self.normalize_python_index_url(index_url)
        with self._session_scope() as session:
            # We need to remove rows from both HasArtifact and PythonArtifact
            subq = (
                session.query(PythonPackageVersionEntity)
                .filter(PythonPackageVersionEntity.package_name == package_name)
                .filter(PythonPackageVersionEntity.package_version == package_version)
                .join(PythonPackageIndex)
                .filter(PythonPackageIndex.url == index_url)
                .join(HasArtifact)
                .join(PythonArtifact)
                .filter(PythonArtifact.artifact_hash_sha256 == sha256_hash)
                .with_entities(PythonArtifact.id)
            )
            # Can a hash be present on more than one python_version_entity?
            (session.query(PythonArtifact).filter(PythonArtifact.id.in_(subq)).update(present=False))

    @staticmethod
    def _rpm_sync_analysis_result(session: Session, package_extract_run: PackageExtractRun, document: dict) -> None:
        """Sync results of RPMs found in the given container image."""
        for rpm_package_info in document["result"]["rpm-dependencies"]:
            rpm_package_version, _ = RPMPackageVersion.get_or_create(
                session,
                package_name=rpm_package_info["name"],
                package_version=rpm_package_info["version"],
                release=rpm_package_info.get("release"),
                epoch=rpm_package_info.get("epoch"),
                arch=rpm_package_info.get("arch"),
                src=rpm_package_info.get("src", False),
                package_identifier=rpm_package_info.get("package_identifier", rpm_package_info["name"]),
            )
            FoundRPM.get_or_create(
                session, package_extract_run_id=package_extract_run.id, rpm_package_version_id=rpm_package_version.id
            )
            for dependency in rpm_package_info["dependencies"]:
                rpm_requirement, _ = RPMRequirement.get_or_create(session, rpm_requirement_name=dependency)
                RPMRequires.get_or_create(
                    session, rpm_package_version_id=rpm_package_version.id, rpm_requirement_id=rpm_requirement.id
                )

    @staticmethod
    def _deb_sync_analysis_result(session: Session, package_extract_run: PackageExtractRun, document: dict) -> None:
        """Sync results of deb packages found in the given container image."""
        for deb_package_info in document["result"]["deb-dependencies"]:
            deb_package_version, _ = DebPackageVersion.get_or_create(
                session,
                package_name=deb_package_info["name"],
                package_version=deb_package_info["version"],
                epoch=deb_package_info.get("epoch"),
                arch=deb_package_info["arch"],
            )
            FoundDeb.get_or_create(
                session, deb_package_version_id=deb_package_version.id, package_extract_run_id=package_extract_run.id
            )

            # These three can be grouped with a zip, but that is not that readable...
            for pre_depends in deb_package_info.get("pre-depends") or []:
                deb_dependency, _ = DebDependency.get_or_create(session, package_name=pre_depends["name"])
                DebPreDepends.get_or_create(
                    session,
                    deb_package_version_id=deb_package_version.id,
                    deb_dependency_id=deb_dependency.id,
                    version_range=pre_depends.get("version"),
                )

            for depends in deb_package_info.get("depends") or []:
                deb_dependency, _ = DebDependency.get_or_create(session, package_name=depends["name"])
                DebDepends.get_or_create(
                    session,
                    deb_package_version_id=deb_package_version.id,
                    deb_dependency_id=deb_dependency.id,
                    version_range=depends.get("version"),
                )

            for replaces in deb_package_info.get("replaces") or []:
                deb_dependency, _ = DebDependency.get_or_create(session, package_name=replaces["name"])
                DebReplaces.from_properties(
                    deb_package_version_id=deb_package_version.id,
                    deb_dependency_id=deb_dependency.id,
                    version_range=replaces.get("version"),
                )

    @staticmethod
    def _system_symbols_analysis_result(
        session: Session,
        package_extract_run: PackageExtractRun,
        document: dict,
        software_environment: Union[SoftwareEnvironment, ExternalSoftwareEnvironment],
        is_external: bool = False,
    ) -> None:
        """Sync system symbols detected in a package-extract run into the database."""
        for library, symbols in document["result"]["system-symbols"].items():
            for symbol in symbols:
                versioned_symbol, _ = VersionedSymbol.get_or_create(session, library_name=library, symbol=symbol)
                if is_external:
                    HasSymbol.get_or_create(
                        session,
                        external_software_environment_id=software_environment.id,
                        versioned_symbol_id=versioned_symbol.id,
                    )
                else:
                    HasSymbol.get_or_create(
                        session,
                        software_environment_id=software_environment.id,
                        versioned_symbol_id=versioned_symbol.id,
                    )

                DetectedSymbol.get_or_create(
                    session, package_extract_run_id=package_extract_run.id, versioned_symbol_id=versioned_symbol.id
                )

    def _python_sync_analysis_result(
        self,
        session: Session,
        package_extract_run: PackageExtractRun,
        document: dict,
        software_environment: Union[SoftwareEnvironment, ExternalSoftwareEnvironment],
    ) -> None:
        """Sync results of Python packages found in the given container image."""
        for python_package_info in document["result"].get("python-packages") or []:
            python_package_version_entity = self._create_python_package_version(
                session,
                package_name=python_package_info["package_name"],
                package_version=python_package_info["package_version"],
                os_name=software_environment.os_name,
                os_version=software_environment.os_version,
                python_version=software_environment.python_version,
                index_url=None,
                sync_only_entity=True,
            )

            Identified.get_or_create(
                session,
                package_extract_run_id=package_extract_run.id,
                python_package_version_entity_id=python_package_version_entity.id,
                location=python_package_info["location"],
            )

    @staticmethod
    def _python_file_digests_sync_analysis_result(
        session: Session, package_extract_run: PackageExtractRun, document: dict
    ) -> None:
        """Sync results of Python files found in the given container image."""
        for py_file in document["result"]["python-files"]:
            python_file_digest, _ = PythonFileDigest.get_or_create(session, sha256=py_file["sha256"])

            FoundPythonFile.get_or_create(
                session,
                package_extract_run_id=package_extract_run.id,
                python_file_digest_id=python_file_digest.id,
                file=py_file["filepath"],
            )

    @staticmethod
    def _python_interpreters_sync_analysis_result(
        session: Session,
        package_extract_run: PackageExtractRun,
        document: dict,
        software_environment: Union[SoftwareEnvironment, ExternalSoftwareEnvironment],
    ) -> None:
        """Sync python interpreters detected in a package-extract run into the database."""
        for py_interpreter in document["result"].get("python-interpreters"):
            python_interpreter, _ = PythonInterpreter.get_or_create(
                session,
                path=py_interpreter.get("path"),
                link=py_interpreter.get("link"),
                version=py_interpreter.get("version"),
            )

            FoundPythonInterpreter.get_or_create(
                session, python_interpreter=python_interpreter, package_extract_run=package_extract_run
            )

    @staticmethod
    def _package_extract_get_env_vars(document: Dict[str, Any]) -> Dict[str, str]:
        """Obtain Thoth specific environment variables present in the container image."""
        result = {}
        for entry in (document["result"].get("skopeo-inspect") or {}).get("Env") or []:
            if entry.startswith(("THAMOS_", "THOTH_")):
                env_name, env_val = entry.split("=", maxsplit=1)
                result[env_name] = env_val

        return result

    def sync_analysis_result(self, document: dict) -> None:
        """Sync the given analysis result to the graph database."""
        analysis_document_id = AnalysisResultsStore.get_document_id(document)
        environment_type = document["metadata"]["arguments"]["thoth-package-extract"]["metadata"]["environment_type"]
        environment_type = environment_type.upper()
        origin = document["metadata"]["arguments"]["thoth-package-extract"]["metadata"].get("origin")
        environment_name = document["metadata"]["arguments"]["extract-image"]["image"]
        os_name = map_os_name(document["result"]["operating-system"]["id"])
        os_version = normalize_os_version(os_name, document["result"]["operating-system"]["version_id"])
        cuda_nvcc_version = document["result"].get("cuda-version", {}).get("nvcc_version", None)
        cuda_found_in_file_version = document["result"].get("cuda-version", {}).get("/usr/local/cuda/version.txt", None)
        if (
            cuda_nvcc_version is not None
            and cuda_found_in_file_version is not None
            and cuda_nvcc_version != cuda_found_in_file_version
        ):
            raise CudaVersionDoesNotMatch(
                f"Cuda version detected by nvcc {cuda_nvcc_version!r} is different from the one found in "
                f"/usr/local/cuda/version.txt "
                f"{document['result'].get('cuda-version', {}).get('/usr/local/cuda/version.txt', None)!r}"
            )

        # Check if it comes from a User
        is_external = document["metadata"]["arguments"]["thoth-package-extract"]["metadata"].get("is_external", True)

        image_tag = "latest"
        image_name = environment_name
        parts = environment_name.rsplit(":", maxsplit=1)
        if len(parts) == 2:
            image_name = parts[0]
            image_tag = parts[1]

        # TODO: capture errors on image analysis? result of package-extract should be a JSON with error flag
        with self._session_scope() as session, session.begin(subtransactions=True):
            if is_external:
                sw_class = ExternalSoftwareEnvironment
                python_version = None
            else:
                sw_class = SoftwareEnvironment
                python_version = image_name.rsplit("-", maxsplit=1)[1]  # pyXX
                if not re.match(r"^py\d\d$", python_version):
                    _LOGGER.warning("No Python version information found in the the image name %r", image_name)
                    python_version = None
                else:
                    python_version = (
                        python_version[2:3] + "." + python_version[3:]
                    )  # take first digit and put . after it

            env_vars = self._package_extract_get_env_vars(document)

            software_environment, _ = sw_class.get_or_create(
                session,
                environment_name=environment_name,
                python_version=python_version,
                image_name=image_name,
                image_sha=document["result"]["layers"][-1],
                os_name=os_name,
                os_version=os_version,
                thoth_s2i_image_name=env_vars.get("THOTH_S2I_NAME"),
                thoth_s2i_image_version=env_vars.get("THOTH_S2I_VERSION"),
                env_image_name=env_vars.get("IMAGE_NAME"),
                env_image_tag=env_vars.get("IMAGE_TAG"),
                cuda_version=cuda_nvcc_version or cuda_found_in_file_version,
                environment_type=environment_type,
            )

            if is_external:
                sw_id = dict(external_software_environment_id=software_environment.id)
            else:
                sw_id = dict(software_environment_id=software_environment.id)

            package_extract_run, _ = PackageExtractRun.get_or_create(
                session,
                analysis_document_id=analysis_document_id,
                datetime=document["metadata"]["datetime"],
                package_extract_version=document["metadata"]["analyzer_version"],
                package_extract_name=document["metadata"]["analyzer"],
                environment_type=environment_type,
                origin=origin,
                debug=document["metadata"]["arguments"]["thoth-package-extract"]["verbose"],
                package_extract_error=False,
                image_tag=image_tag,
                duration=document["metadata"].get("duration"),
                os_id=document["result"].get("operating-system", {}).get("id"),
                os_name=os_name,
                os_version_id=os_version,
                image_size=document["result"].get("image_size"),
                **sw_id,
            )

            self._rpm_sync_analysis_result(session, package_extract_run, document)
            self._deb_sync_analysis_result(session, package_extract_run, document)
            self._python_sync_analysis_result(session, package_extract_run, document, software_environment)
            self._python_file_digests_sync_analysis_result(session, package_extract_run, document)
            self._system_symbols_analysis_result(
                session, package_extract_run, document, software_environment, is_external=is_external
            )
            self._python_interpreters_sync_analysis_result(session, package_extract_run, document, software_environment)

    @staticmethod
    def _get_or_create_python_package_index(
        session: Session, index_url: str, only_if_enabled: bool = True
    ) -> Optional[PythonPackageIndex]:
        """Get or create Python package index entry with a check the given index is enabled."""
        index_url = GraphDatabase.normalize_python_index_url(index_url)
        python_package_index = session.query(PythonPackageIndex).filter(PythonPackageIndex.url == index_url).first()

        if python_package_index is None:
            if only_if_enabled:
                raise PythonIndexNotRegistered(f"Python package index {index_url!r} is not know to system")
            python_package_index, _ = PythonPackageIndex.get_or_create(session, url=index_url)
        elif not python_package_index.enabled and only_if_enabled:
            raise PythonIndexNotRegistered(f"Python package index {index_url!r} is not enabled")

        return python_package_index

    @staticmethod
    def _create_multi_part_keys_metadata(
        session: Session, importlib_metadata: Dict[str, Any], package_metadata: PythonPackageMetadata
    ) -> Dict[str, Any]:
        """Sync multi-part keys from Python Package Metadata."""
        for classifier in importlib_metadata.pop("Classifier", []):
            python_package_metadata_classifier, _ = PythonPackageMetadataClassifier.get_or_create(
                session, classifier=classifier
            )
            HasMetadataClassifier.get_or_create(
                session,
                python_package_metadata_classifier_id=python_package_metadata_classifier.id,
                python_package_metadata_id=package_metadata.id,
            )

        for platform in importlib_metadata.pop("Platform", []):
            python_package_metadata_platform, _ = PythonPackageMetadataPlatform.get_or_create(
                session, platform=platform
            )
            HasMetadataPlatform.get_or_create(
                session,
                python_package_metadata_platform_id=python_package_metadata_platform.id,
                python_package_metadata_id=package_metadata.id,
            )

        for supported_platform in importlib_metadata.pop("Supported-Platform", []):
            python_package_metadata_supported_platform, _ = PythonPackageMetadataSupportedPlatform.get_or_create(
                session, supported_platform=supported_platform
            )
            HasMetadataSupportedPlatform.get_or_create(
                session,
                python_package_metadata_supported_platform_id=python_package_metadata_supported_platform.id,
                python_package_metadata_id=package_metadata.id,
            )

        for dependency in importlib_metadata.pop("Requires-External", []):
            python_package_metadata_requires_external, _ = PythonPackageMetadataRequiresExternal.get_or_create(
                session, dependency=dependency
            )
            HasMetadataRequiresExternal.get_or_create(
                session,
                python_package_metadata_requires_external_id=python_package_metadata_requires_external.id,
                python_package_metadata_id=package_metadata.id,
            )

        for project_url in importlib_metadata.pop("Project-URL", []):
            python_package_metadata_project_url, _ = PythonPackageMetadataProjectUrl.get_or_create(
                session, project_url=project_url
            )
            HasMetadataProjectUrl.get_or_create(
                session,
                python_package_metadata_project_url_id=python_package_metadata_project_url.id,
                python_package_metadata_id=package_metadata.id,
            )

        for optional_feature in importlib_metadata.pop("Provides-Extra", []):
            python_package_metadata_provides_extra, _ = PythonPackageMetadataProvidesExtra.get_or_create(
                session, optional_feature=optional_feature
            )
            HasMetadataProvidesExtra.get_or_create(
                session,
                python_package_metadata_provides_extra_id=python_package_metadata_provides_extra.id,
                python_package_metadata_id=package_metadata.id,
            )

        for dist_key in ("Requires-Dist", "Provides-Dist", "Obsoletes-Dist"):
            if dist_key == "Requires-Dist":
                distutils_type = MetadataDistutilsTypeEnum.REQUIRED.value
            elif dist_key == "Provides-Dist":
                distutils_type = MetadataDistutilsTypeEnum.PROVIDED.value
            elif dist_key == "Obsoletes-Dist":
                distutils_type = MetadataDistutilsTypeEnum.OBSOLETE.value
            else:
                raise DistutilsKeyNotKnown(f"No distutils key registered for {dist_key!r} ")

            for distutils in importlib_metadata.pop(dist_key, []):
                python_package_metadata_distutils, _ = PythonPackageMetadataDistutils.get_or_create(
                    session, distutils=distutils, distutils_type=distutils_type
                )

                HasMetadataDistutils.get_or_create(
                    session,
                    python_package_metadata_distutils_id=python_package_metadata_distutils.id,
                    python_package_metadata_id=package_metadata.id,
                )

        return importlib_metadata

    def sync_revsolver_result(self, document: Dict[str, Any]) -> None:
        """Sync results of the reverse solver.

        This updates relations for DependsOn on a new package release.
        """
        dependency_name = document["metadata"]["arguments"]["app.py"]["package_name"]
        dependency_version = document["metadata"]["arguments"]["app.py"]["package_version"]

        with self._session_scope() as session, session.begin(subtransactions=True):
            python_package_version_entity, _ = PythonPackageVersionEntity.get_or_create(
                session, package_name=dependency_name, package_version=dependency_version, python_package_index_id=None
            )
            self._refresh_rules_python_entity(session, python_package_version_entity)

            for entry in document["result"]:
                os_name = map_os_name(entry["os_name"])
                os_version = entry["os_version"]
                python_package_version = (
                    session.query(PythonPackageVersion)
                    .filter(PythonPackageVersion.package_name == entry["package_name"])
                    .filter(PythonPackageVersion.package_version == entry["package_version"])
                    .filter(PythonPackageVersion.os_name == os_name)
                    .filter(PythonPackageVersion.os_version == normalize_os_version(os_name, os_version))
                    .filter(PythonPackageVersion.python_version == entry["python_version"])
                    .join(PythonPackageIndex)
                    .filter(PythonPackageIndex.url == entry["index_url"])
                    .one()
                )

                DependsOn.get_or_create(
                    session,
                    version=python_package_version,
                    entity=python_package_version_entity,
                    version_range=entry["version_range"],
                    marker=entry["marker"],
                    extra=entry["extra"],
                    marker_evaluation_result=entry["marker_evaluation_result"],
                )

    def _check_package_solved(
        self, session: Session, package_name: str, package_version: str, package_index: str
    ) -> Tuple:
        """Check if the package has been solved before syncing SI analysis to the database."""
        # Check if a package have been solved by any of the solver
        python_package_version = (
            session.query(PythonPackageVersion)
            .join(PythonPackageIndex)
            .filter(PythonPackageVersion.package_name == package_name)
            .filter(PythonPackageVersion.package_version == package_version)
            .filter(PythonPackageIndex.url == package_index)
            .first()
        )

        if not python_package_version:
            raise SolverNotRun(
                f"Trying to sync package {package_name!r} in version {package_version!r} " f"not solved by any solver."
            )

        return python_package_version.entity_id, python_package_version.id

    def sync_security_indicator_aggregated_result(self, document: dict) -> None:
        """Sync the given security-indicator aggregated result to the graph database."""
        metadata = document["metadata"]
        document_id = metadata["document_id"]
        result = document.get("result", dict())

        package_name = metadata["arguments"]["app.py"]["package_name"]
        package_version = metadata["arguments"]["app.py"]["package_version"]
        index_url = metadata["arguments"]["app.py"]["package_index"]

        with self._session_scope() as session, session.begin(subtransactions=True):

            python_package_version_entity_id, python_package_version_id = self._check_package_solved(
                session=session, package_name=package_name, package_version=package_version, package_index=index_url
            )

            si_aggregated_run, _ = SecurityIndicatorAggregatedRun.get_or_create(
                session,
                si_aggregated_run_document_id=document_id,
                datetime=metadata["datetime"],
                error=document.get("error", False),
                severity_high_confidence_high=result.get("SEVERITY.HIGH__CONFIDENCE.HIGH") or 0,
                severity_high_confidence_low=result.get("SEVERITY.HIGH__CONFIDENCE.LOW") or 0,
                severity_high_confidence_medium=result.get("SEVERITY.HIGH__CONFIDENCE.MEDIUM") or 0,
                severity_high_confidence_undefined=result.get("SEVERITY.HIGH__CONFIDENCE.UNDEFINED") or 0,
                severity_low_confidence_high=result.get("SEVERITY.LOW__CONFIDENCE.HIGH") or 0,
                severity_low_confidence_low=result.get("SEVERITY.LOW__CONFIDENCE.LOW") or 0,
                severity_low_confidence_medium=result.get("SEVERITY.LOW__CONFIDENCE.MEDIUM") or 0,
                severity_low_confidence_undefined=result.get("SEVERITY.LOW__CONFIDENCE.UNDEFINED") or 0,
                severity_medium_confidence_high=result.get("SEVERITY.MEDIUM__CONFIDENCE.HIGH") or 0,
                severity_medium_confidence_low=result.get("SEVERITY.MEDIUM__CONFIDENCE.LOW") or 0,
                severity_medium_confidence_medium=result.get("SEVERITY.MEDIUM__CONFIDENCE.MEDIUM") or 0,
                severity_medium_confidence_undefined=result.get("SEVERITY.MEDIUM__CONFIDENCE.UNDEFINED") or 0,
                number_of_analyzed_files=result["number_of_analyzed_files"],
                number_of_files_total=result["number_of_files_total"],
                number_of_files_with_severities=result["number_of_files_with_severities"],
                number_of_filtered_files=result["number_of_filtered_files"],
                number_of_python_files=result["Python.nFiles"],
                number_of_lines_with_comments_in_python_files=result["Python.comment"],
                number_of_blank_lines_in_python_files=result["Python.blank"],
                number_of_lines_with_code_in_python_files=result["Python.code"],
                total_number_of_files=result["SUM.nFiles"],
                total_number_of_lines=result["SUM.n_lines"],
                total_number_of_lines_with_comments=result["SUM.comment"],
                total_number_of_blank_lines=result["SUM.blank"],
                total_number_of_lines_with_code=result["SUM.code"],
            )

            SIAggregated.get_or_create(
                session,
                si_aggregated_run_id=si_aggregated_run.id,
                python_package_version_entity_id=python_package_version_entity_id,
                python_package_version_id=python_package_version_id,
            )

    def sync_solver_result(self, document: dict, *, force: bool = False) -> None:
        """Sync the given solver result to the graph database."""
        solver_document_id = SolverResultsStore.get_document_id(document)
        solver_name = SolverResultsStore.get_solver_name_from_document_id(solver_document_id)
        solver_info = OpenShift.parse_python_solver_name(solver_name)
        solver_datetime = document["metadata"]["datetime"]
        solver_version = document["metadata"]["analyzer_version"]
        solver_duration = (document["metadata"].get("duration"),)
        os_name = solver_info["os_name"]
        os_version = solver_info["os_version"]
        python_version = solver_info["python_version"]
        # Older solver documents did not provide platform explictly.
        platform = document["result"].get("platform") or "linux-x86_64"

        if not self.python_package_version_depends_on_platform_exists(platform=platform):
            raise NotFoundError(f"No platform {platform!r} registered")

        with self._session_scope() as session, session.begin(subtransactions=True):
            ecosystem_solver, _ = EcosystemSolver.get_or_create(
                session,
                ecosystem="python",
                solver_name=solver_name,
                solver_version=solver_version,
                os_name=map_os_name(os_name),
                os_version=normalize_os_version(os_name, os_version),
                python_version=python_version,
            )

            for python_package_info in document["result"]["tree"]:
                # Normalized in `_create_python_package_version'.
                package_name = python_package_info["package_name"]
                package_version = python_package_info["package_version_requested"]
                index_url = python_package_info["index_url"]
                importlib_metadata = python_package_info["importlib_metadata"]["metadata"]

                _LOGGER.info(
                    "Syncing solver result of package %r in version %r from %r solved by %r",
                    package_name,
                    package_version,
                    index_url,
                    solver_info,
                )

                package_metadata, _ = PythonPackageMetadata.get_or_create(
                    session,
                    author=importlib_metadata.pop("Author", None),
                    author_email=importlib_metadata.pop("Author-email", None),
                    download_url=importlib_metadata.pop("Download-URL", None),
                    home_page=importlib_metadata.pop("Home-page", None),
                    keywords=importlib_metadata.pop("Keywords", None),
                    # package licence
                    license=importlib_metadata.pop("License", None),
                    maintainer=importlib_metadata.pop("Maintainer", None),
                    maintainer_email=importlib_metadata.pop("Maintainer-email", None),
                    metadata_version=importlib_metadata.pop("Metadata-Version", None),
                    # package name
                    name=importlib_metadata.pop("Name", None),
                    summary=importlib_metadata.pop("Summary", None),
                    # package version
                    version=importlib_metadata.pop("Version", None),
                    requires_python=importlib_metadata.pop("Requires-Python", None),
                    description=importlib_metadata.pop("Description", None),
                    description_content_type=importlib_metadata.pop("Description-Content-Type", None),
                )

                # Sync Metadata keys that are arrays
                importlib_metadata = self._create_multi_part_keys_metadata(
                    session, importlib_metadata=importlib_metadata, package_metadata=package_metadata
                )

                if importlib_metadata:
                    # There can be raised PythonPackageMetadataAttributeMissing once all metadata gathered.
                    _LOGGER.warning(
                        "Cannot sync the whole solver result: "
                        f"No related columns for {list(importlib_metadata.keys())!r} "
                        "found in PythonPackageMetadata table, the error is not fatal"
                    )
                try:
                    python_package_version = self._create_python_package_version(
                        session,
                        package_name,
                        package_version,
                        os_name=ecosystem_solver.os_name,
                        os_version=ecosystem_solver.os_version,
                        python_version=ecosystem_solver.python_version,
                        index_url=index_url,
                        python_package_metadata_id=package_metadata.id,
                    )
                except NoResultFound:
                    if not force:
                        raise

                    _LOGGER.warning(
                        "Removing old PythonPackageVersion entry based on previous results stored and "
                        "force parameter supplied"
                    )
                    # Try to delete the given package-version and continue with the sync.
                    self._delete_python_package_version(
                        package_name=package_name,
                        package_version=package_version,
                        os_name=ecosystem_solver.os_name,
                        os_version=ecosystem_solver.os_version,
                        python_version=ecosystem_solver.python_version,
                        index_url=index_url,
                    )

                    python_package_version = self._create_python_package_version(
                        session,
                        package_name,
                        package_version,
                        os_name=ecosystem_solver.os_name,
                        os_version=ecosystem_solver.os_version,
                        python_version=ecosystem_solver.python_version,
                        index_url=index_url,
                        python_package_metadata_id=package_metadata.id,
                    )

                for sha256 in python_package_info["sha256"]:
                    artifact, _ = PythonArtifact.get_or_create(
                        session, artifact_hash_sha256=sha256, artifact_name=None  # TODO: aggregate artifact names
                    )
                    HasArtifact.get_or_create(
                        session,
                        python_artifact_id=artifact.id,
                        python_package_version_entity_id=python_package_version.entity_id,
                    )

                solved, _ = Solved.get_or_create(
                    session,
                    datetime=solver_datetime,
                    document_id=solver_document_id,
                    version=python_package_version,
                    ecosystem_solver=ecosystem_solver,
                    duration=solver_duration,
                    error=False,
                    error_unparseable=False,
                    error_unsolvable=False,
                )

                # Sync imoprted package from result:tree
                _LOGGER.info(
                    "Syncing imported packages for package %r in version %r from %r found by solver %r",
                    package_name,
                    package_version,
                    index_url,
                    solver_info,
                )

                for package_call in python_package_info["packages"]:
                    import_package, _ = ImportPackage.get_or_create(
                        session,
                        import_package_name=package_call,
                    )

                    FoundImportPackage.get_or_create(
                        session,
                        python_package_version_id=python_package_version.id,
                        import_package_id=import_package.id,
                    )

                for dependency in python_package_info["dependencies"]:
                    for index_entry in dependency["resolved_versions"]:
                        for dependency_version in index_entry["versions"]:
                            dependency_entity, _ = PythonPackageVersionEntity.get_or_create(
                                session,
                                package_name=self.normalize_python_package_name(dependency["package_name"]),
                                package_version=self.normalize_python_package_version(dependency_version),
                                python_package_index_id=None,
                            )
                            self._refresh_rules_python_entity(session, dependency_entity)

                            if len(dependency.get("extra") or []) > 1:
                                # Not sure if this can happen in the ecosystem, report error
                                # if this incident happens.
                                _LOGGER.error(
                                    "Multiple extra detected for dependency %r in version %r required "
                                    "by %r in version %r from index %r with marker %r, only the "
                                    "first extra will be used: %r",
                                    dependency["package_name"],
                                    dependency_version,
                                    package_name,
                                    package_version,
                                    index_url,
                                    dependency.get("marker"),
                                    dependency.get("extra"),
                                )

                            DependsOn.get_or_create(
                                session,
                                version=python_package_version,
                                entity=dependency_entity,
                                version_range=dependency.get("required_version") or "*",
                                marker=dependency.get("marker"),
                                extra=dependency["extra"][0] if dependency.get("extra") else None,
                                marker_evaluation_result=dependency.get("marker_evaluation_result", True),
                            )

            for error_info in document["result"]["errors"]:
                # Normalized in `_create_python_package_version'.
                package_name = error_info.get("package_name") or error_info["package"]
                package_version = error_info.get("package_version") or error_info["version"]
                index_url = error_info.get("index_url") or error_info["index"]

                _LOGGER.info(
                    "Syncing solver errors for package %r in version %r from %r found by solver %r",
                    package_name,
                    package_version,
                    index_url,
                    solver_info,
                )

                # Sync to PPV table only packages that are provided, regardless solving errors. The default
                # value of True is due to legacy thoth-solver output.
                python_package_version_id = None
                if error_info.get("is_provided_package_version", True):
                    python_package_version_id = self._create_python_package_version(
                        session,
                        package_name,
                        package_version,
                        os_name=ecosystem_solver.os_name,
                        os_version=ecosystem_solver.os_version,
                        python_version=ecosystem_solver.python_version,
                        index_url=index_url,
                    ).id

                solved, _ = Solved.get_or_create(
                    session,
                    datetime=solver_datetime,
                    document_id=solver_document_id,
                    version_id=python_package_version_id,
                    ecosystem_solver=ecosystem_solver,
                    duration=solver_duration,
                    error=True,
                    error_unparseable=False,
                    error_unsolvable=False,
                    is_provided=python_package_version_id is not None,
                )

            for unsolvable in document["result"]["unresolved"]:
                if not unsolvable["version_spec"].startswith("==="):
                    # No resolution can be performed so no identifier is captured, report warning and continue.
                    # We would like to capture this especially when there are
                    # packages in ecosystem that we cannot find (e.g. not configured private index
                    # or removed package).
                    _LOGGER.warning(
                        "Cannot sync unsolvable package %r as package is not locked to as specific version", unsolvable
                    )
                    continue

                package_name = self.normalize_python_package_name(unsolvable["package_name"])
                index_url = unsolvable.get("index_url") or unsolvable["index"]
                package_version = self.normalize_python_package_version(unsolvable["version_spec"][len("===") :])

                _LOGGER.info(
                    "Syncing unsolvable package %r in version %r from %r found by solver %r",
                    package_name,
                    package_version,
                    index_url,
                    solver_info,
                )
                python_package_version = self._create_python_package_version(
                    session,
                    package_name,
                    package_version,
                    os_name=ecosystem_solver.os_name,
                    os_version=ecosystem_solver.os_version,
                    python_version=ecosystem_solver.python_version,
                    index_url=index_url,
                )

                solved, _ = Solved.get_or_create(
                    session,
                    datetime=solver_datetime,
                    document_id=solver_document_id,
                    version_id=python_package_version.id,
                    ecosystem_solver=ecosystem_solver,
                    duration=solver_duration,
                    error=True,
                    error_unparseable=False,
                    error_unsolvable=True,
                )

            for unparsed in document["result"]["unparsed"]:
                parts = unparsed["requirement"].rsplit("===", maxsplit=1)
                if len(parts) != 2:
                    # This request did not come from graph-refresh job as there is not pinned version.
                    _LOGGER.warning(
                        "Cannot sync unparsed package %r as package is not locked to as specific version", unparsed
                    )
                    continue

                package_name, package_version = parts

                _LOGGER.info(
                    "Syncing unparsed package %r in version %r from %r", package_name, package_version, solver_info
                )
                python_package_version = self._create_python_package_version(
                    session,
                    package_name,
                    package_version,
                    os_name=ecosystem_solver.os_name,
                    os_version=ecosystem_solver.os_version,
                    python_version=ecosystem_solver.python_version,
                    index_url=None,
                )

                solved, _ = Solved.get_or_create(
                    session,
                    datetime=solver_datetime,
                    document_id=solver_document_id,
                    version=python_package_version,
                    ecosystem_solver=ecosystem_solver,
                    duration=solver_duration,
                    error=True,
                    error_unparseable=True,
                    error_unsolvable=False,
                )

    def sync_adviser_result(self, document: dict) -> None:
        """Sync adviser result into graph database."""
        adviser_document_id = AdvisersResultsStore.get_document_id(document)
        parameters = document["result"]["parameters"]
        cli_arguments = document["metadata"]["arguments"]["thoth-adviser"]
        origin = (cli_arguments.get("metadata") or {}).get("origin")
        re_run_adviser_id = (cli_arguments.get("metadata") or {}).get("re_run_adviser_id")
        is_s2i = (cli_arguments.get("metadata") or {}).get("is_s2i")
        runtime_environment = parameters["project"].get("runtime_environment")
        source_type = (cli_arguments.get("metadata") or {}).get("source_type")
        source_type = source_type.upper() if source_type else None

        os = runtime_environment.get("operating_system", {})
        if os:
            os_name = runtime_environment["operating_system"].get("name")
            if os_name:
                runtime_environment["operating_system"]["name"] = map_os_name(
                    os_name=runtime_environment["operating_system"]["name"]
                )

        need_re_run = False

        if not origin:
            _LOGGER.warning("No origin stated in the adviser result %r", adviser_document_id)

        if is_s2i is None:
            _LOGGER.warning("No s2i flag stated in the adviser result %r", adviser_document_id)

        with self._session_scope() as session, session.begin(subtransactions=True):
            external_hardware_info, external_run_software_environment = self._runtime_environment_conf2models(
                session,
                runtime_environment=runtime_environment,
                environment_type=EnvironmentTypeEnum.RUNTIME.value,
                is_external=True,
            )

            # Input stack.
            external_software_stack = self._create_python_software_stack(
                session,
                requirements=parameters["project"].get("requirements"),
                requirements_lock=parameters["project"].get("requirements_locked"),
                software_environment=external_run_software_environment,
                is_external=True,
            )

            attributes = {
                "additional_stack_info": bool(document["result"].get("stack_info")),
                "advised_configuration_changes": bool(document["result"].get("advised_configuration")),
                "adviser_document_id": adviser_document_id,
                "adviser_error": document["result"]["error"],
                "adviser_name": document["metadata"]["analyzer"],
                "adviser_version": document["metadata"]["analyzer_version"],
                "count": parameters["count"],
                "datetime": document["metadata"]["datetime"],
                "debug": cli_arguments.get("verbose", False),
                "duration": document["metadata"].get("duration"),
                "limit": parameters["limit"],
                "limit_latest_versions": parameters.get("limit_latest_versions"),
                "origin": origin,
                "source_type": source_type,
                "is_s2i": is_s2i,
                "recommendation_type": parameters["recommendation_type"].upper(),
                "requirements_format": parameters["requirements_format"].upper(),
                "external_hardware_information_id": external_hardware_info.id,
                "external_build_software_environment_id": None,
                "external_run_software_environment_id": external_run_software_environment.id,
                "user_software_stack_id": external_software_stack.id,
            }

            # Output stacks - advised stacks
            if not document["result"].get("report", {}):
                _LOGGER.warning("No report found in %r", adviser_document_id)
                adviser_run, _ = AdviserRun.get_or_create(session, **attributes, need_re_run=need_re_run)
                return

            unresolved_packages = document["result"].get("report", {}).get("_ERROR_DETAILS", {}).get("unresolved", [])

            if unresolved_packages:
                need_re_run = True

            if re_run_adviser_id and unresolved_packages:
                # If adviser was re run and there are still unsolved packages.
                adviser_run, _ = AdviserRun.get_or_create(
                    session, **attributes, need_re_run=need_re_run, re_run_adviser_id=re_run_adviser_id
                )

            elif re_run_adviser_id and not unresolved_packages:
                # If adviser was re run and there are no more unsolved packages.

                # Modify initial adviser flag in order to avoid re run.
                first_adviser_run = (
                    session.query(AdviserRun).filter(AdviserRun.adviser_document_id == re_run_adviser_id).first()
                )
                # INSERT…ON CONFLICT (Upsert)
                # https://docs.sqlalchemy.org/en/13/dialects/postgresql.html?highlight=conflict#insert-on-conflict-upsert
                # https://docs.sqlalchemy.org/en/13/errors.html#sql-expression-language compile required

                if first_adviser_run and first_adviser_run.need_re_run:
                    insert_stmt = insert(AdviserRun).values(**first_adviser_run.to_dict(without_id=False))

                    do_update_stmt = insert_stmt.on_conflict_do_update(
                        index_elements=["id"], set_=dict(need_re_run=False)
                    )

                    session.execute(do_update_stmt)

                # Store current adviser run.
                adviser_run, _ = AdviserRun.get_or_create(
                    session, **attributes, need_re_run=need_re_run, re_run_adviser_id=re_run_adviser_id
                )

            else:
                # Any other case of adviser run.
                adviser_run, _ = AdviserRun.get_or_create(session, **attributes, need_re_run=need_re_run)

            advised_stacks = []

            for idx, product in enumerate(document["result"].get("report", {}).get("products", [])):
                performance_score = None
                overall_score = product["score"]
                for entry in product.get("justification", []):
                    if "performance_score" in entry:
                        if performance_score is not None:
                            _LOGGER.error(
                                "Multiple performance score entries found in %r (index: %d)", adviser_document_id, idx
                            )
                        performance_score = entry["performance_score"]

                if product.get("project", {}).get("requirements_locked"):
                    advised_software_stack = self._create_python_software_stack(
                        session,
                        software_stack_type=SoftwareStackTypeEnum.ADVISED.value,
                        requirements=product["project"]["requirements"],
                        requirements_lock=product["project"]["requirements_locked"],
                        software_environment=external_run_software_environment,
                        performance_score=performance_score,
                        overall_score=overall_score,
                    )

                    Advised.get_or_create(
                        session,
                        adviser_run_id=adviser_run.id,
                        python_software_stack_id=advised_software_stack.id,
                    )

                    advised_stacks.append(advised_software_stack)

            if source_type == "KEBECHET" and advised_stacks:
                slug = "/".join(
                    origin.split(
                        "/",
                    )[-2:]
                )
                _LOGGER.info("Kebechet reference slug is %r", slug)

                kebechet_installed = (
                    session.query(KebechetGithubAppInstallations)
                    .filter(KebechetGithubAppInstallations.slug == slug)
                    .first()
                )

                if kebechet_installed:

                    insert_stmt = insert(KebechetGithubAppInstallations).values(
                        **kebechet_installed.to_dict(without_id=False)
                    )

                    do_update_stmt = insert_stmt.on_conflict_do_update(
                        index_elements=["id"],
                        set_=dict(
                            last_run=document["metadata"]["datetime"],
                            thoth_advise_manager=True,
                            advised_python_software_stack_id=advised_stacks[0].id,
                        ),
                    )

                    session.execute(do_update_stmt)

                else:
                    _LOGGER.warning("No Kebechet installation found for %r", origin)

            # Mark down packages that were not solved if adviser run failed.
            for unresolved in unresolved_packages:
                python_package_version_entity = self._create_python_package_version(
                    session,
                    package_name=unresolved,
                    package_version=None,
                    index_url=None,
                    os_name=None,
                    os_version=None,
                    python_version=None,
                    sync_only_entity=True,
                )

                HasUnresolved.get_or_create(
                    session,
                    adviser_run_id=adviser_run.id,
                    python_package_version_entity_id=python_package_version_entity.id,
                )

    def sync_provenance_checker_result(self, document: dict) -> None:
        """Sync provenance checker results into graph database."""
        provenance_checker_document_id = ProvenanceResultsStore.get_document_id(document)
        origin = (document["metadata"]["arguments"]["thoth-adviser"].get("metadata") or {}).get("origin")

        if not origin:
            _LOGGER.warning("No origin stated in the provenance-checker result %r", provenance_checker_document_id)

        with self._session_scope() as session, session.begin(subtransactions=True):
            parameters = document["result"]["parameters"]
            software_stack = self._create_python_software_stack(
                session,
                requirements=parameters["project"].get("requirements"),
                requirements_lock=parameters["project"].get("requirements_locked"),
                software_environment=None,
                is_external=True,
            )

            provenance_checker_run, _ = ProvenanceCheckerRun.get_or_create(
                session,
                provenance_checker_document_id=provenance_checker_document_id,
                datetime=document["metadata"]["datetime"],
                provenance_checker_version=document["metadata"]["analyzer_version"],
                provenance_checker_name=document["metadata"]["analyzer"],
                origin=origin,
                debug=document["metadata"]["arguments"]["thoth-adviser"]["verbose"],
                provenance_checker_error=document["result"]["error"],
                duration=document["metadata"].get("duration"),
                user_software_stack_id=software_stack.id,
            )

            # Mark down packages that were not solved and missed in provenance checker.
            report = document["result"]["report"]

            for package in report:
                # Discover unresolved package matching the message ID
                if package["id"] == "MISSING-PACKAGE":

                    python_package_version_entity = self._create_python_package_version(
                        session,
                        package_name=package["package_name"],
                        package_version=package["package_version"].lstrip("=="),
                        index_url=package["source"]["url"],
                        os_name=None,
                        os_version=None,
                        python_version=None,
                        sync_only_entity=True,
                    )

    def sync_dependency_monkey_result(self, document: dict) -> None:
        """Sync reports of dependency monkey runs."""
        if "ERROR" in document["result"]["report"]:
            _LOGGER.warning(
                "No entries to be synced for Dependency Monkey %r as Dependency Monkey failed",
                DependencyMonkeyReportsStore.get_document_id(document),
            )
            return

        with self._session_scope() as session, session.begin(subtransactions=True):
            parameters = document["result"]["parameters"]

            run_hardware_information, run_software_environment = self._runtime_environment_conf2models(
                session,
                parameters["project"].get("runtime_environment", {}),
                environment_type=EnvironmentTypeEnum.RUNTIME.value,
                is_external=False,
            )
            build_hardware_information, build_software_environment = self._runtime_environment_conf2models(
                session,
                parameters["project"].get("runtime_environment", {}),
                environment_type=EnvironmentTypeEnum.BUILDTIME.value,
                is_external=False,
            )
            dependency_monkey_run, _ = DependencyMonkeyRun.get_or_create(
                session,
                dependency_monkey_document_id=DependencyMonkeyReportsStore.get_document_id(document),
                datetime=document["metadata"]["datetime"],
                dependency_monkey_name=document["metadata"]["analyzer"],
                dependency_monkey_version=document["metadata"]["analyzer_version"],
                seed=parameters.get("seed"),
                decision=parameters.get("decision_type"),
                count=parameters.get("count"),
                limit_latest_versions=parameters.get("limit_latest_versions"),
                debug=document["metadata"]["arguments"]["thoth-adviser"]["verbose"],
                dependency_monkey_error=document["result"]["error"],
                duration=document["metadata"].get("duration"),
                build_software_environment_id=build_software_environment.id,
                build_hardware_information_id=build_hardware_information.id,
                run_software_environment_id=run_software_environment.id,
                run_hardware_information_id=run_hardware_information.id,
            )

            python_package_requirements = self._create_python_package_requirement(
                session, parameters["project"].get("requirements")
            )
            for python_package_requirement in python_package_requirements:
                PythonDependencyMonkeyRequirements.get_or_create(
                    session,
                    python_package_requirement_id=python_package_requirement.id,
                    dependency_monkey_run_id=dependency_monkey_run.id,
                )

            # Number of times each inspection run will be run
            count = document["result"]["parameters"]["count"]

            for entry in document["result"]["report"]["responses"]:
                inspection_document_id = entry["response"]

                for inspection_result_number in range(count):
                    inspection_run = (
                        session.query(InspectionRun)
                        .filter(InspectionRun.inspection_document_id == inspection_document_id)
                        .filter(InspectionRun.inspection_result_number == inspection_result_number)
                        .filter(InspectionRun.dependency_monkey_run_id == dependency_monkey_run.id)
                        .first()
                    )

                    if inspection_run is None:
                        inspection_run = InspectionRun(
                            inspection_document_id=inspection_document_id,
                            inspection_sync_state=InspectionSyncStateEnum.PENDING.value,
                            inspection_result_number=inspection_result_number,
                            dependency_monkey_run_id=dependency_monkey_run.id,
                        )
                        session.add(inspection_run)

    @lru_cache(maxsize=_GET_PYTHON_PACKAGE_REQUIRED_SYMBOLS_CACHE_SIZE)
    def get_python_package_required_symbols(self, package_name: str, package_version: str, index_url: str) -> List[str]:
        """Get required symbols for a Python package in a specified version."""
        package_name = self.normalize_python_package_name(package_name)
        package_version = self.normalize_python_package_version(package_version)
        index_url = self.normalize_python_index_url(index_url)

        with self._session_scope() as session:
            query = (
                session.query(PythonPackageVersionEntity)
                .filter(PythonPackageVersionEntity.package_name == self.normalize_python_package_name(package_name))
                .filter(
                    PythonPackageVersionEntity.package_version == self.normalize_python_package_version(package_version)
                )
                .join(PythonPackageIndex)
                .filter(PythonPackageIndex.url == index_url)
                .join(HasArtifact)
                .join(RequiresSymbol, HasArtifact.python_artifact_id == RequiresSymbol.python_artifact_id)
                .join(VersionedSymbol)
                .with_entities(VersionedSymbol.symbol)
                .distinct(VersionedSymbol.symbol)
            )

            # Query returns list of single tuples
            # NOTE: can be empty even if request is valid
            return [i[0] for i in query.all()]

    def get_analyzed_image_symbols_all(
        self, os_name: str, os_version: str, *, python_version: Optional[str] = None, cuda_version: Optional[str] = None
    ) -> List[str]:
        """Get symbols associated with a given image."""
        os_name = map_os_name(os_name)
        with self._session_scope() as session:
            query = (
                session.query(SoftwareEnvironment)
                .filter(SoftwareEnvironment.os_name == os_name)
                .filter(SoftwareEnvironment.os_version == normalize_os_version(os_name, os_version))
                .filter(SoftwareEnvironment.cuda_version == cuda_version)
                .filter(SoftwareEnvironment.python_version == python_version)
                .join(HasSymbol)
                .join(VersionedSymbol)
                .with_entities(VersionedSymbol.symbol)
                .distinct(VersionedSymbol.symbol)
            )

            # Query returns list of single tuples (empty if bad request)
            return [i[0] for i in query.all()]

    @lru_cache(maxsize=_GET_S2I_ANALYZED_IMAGE_SYMBOLS)
    def get_thoth_s2i_analyzed_image_symbols_all(
        self, thoth_s2i_image_name: str, thoth_s2i_image_version: str, is_external: bool = False
    ) -> List[str]:
        """Get symbols associated with a given Thoth s2i container image."""
        model = ExternalSoftwareEnvironment if is_external else SoftwareEnvironment
        with self._session_scope() as session:
            query = (
                session.query(model)
                .filter(model.thoth_s2i_image_name == thoth_s2i_image_name)
                .filter(model.thoth_s2i_image_version == thoth_s2i_image_version)
                .join(HasSymbol)
                .join(VersionedSymbol)
                .with_entities(VersionedSymbol.symbol)
                .distinct(VersionedSymbol.symbol)
            )

            # Query returns list of single tuples (empty if bad request)
            return [i[0] for i in query.all()]

    def get_thoth_s2i_all(self, is_external: bool = False) -> List[Tuple[str, str]]:
        """Get all the Thoth s2i container images available."""
        model = ExternalSoftwareEnvironment if is_external else SoftwareEnvironment
        with self._session_scope() as session:
            query = (
                session.query(model)
                .with_entities(model.thoth_s2i_image_name, model.thoth_s2i_image_version)
                .distinct(model.thoth_s2i_image_name, model.thoth_s2i_image_version)
            )

            # Query returns list of single tuples (empty if bad request)
            return [tuple(i) for i in query.all()]

    def get_thoth_s2i_package_extract_analysis_document_id_all(
        self, thoth_s2i_image_name: str, thoth_s2i_image_version: str, is_external: bool = False
    ) -> List[str]:
        """Get package-extract analysis ids for the given Thoth s2i."""
        model = ExternalSoftwareEnvironment if is_external else SoftwareEnvironment
        with self._session_scope() as session:
            query = (
                session.query(PackageExtractRun)
                .join(model)
                .filter(model.thoth_s2i_image_name == thoth_s2i_image_name)
                .filter(model.thoth_s2i_image_version == thoth_s2i_image_version)
                .with_entities(PackageExtractRun.analysis_document_id)
            )

            return [i[0] for i in query.all()]

    def get_pi_count(self, component: str) -> Dict[str, int]:
        """Get dictionary with number of Performance Indicators per type for the PI component selected."""
        result = {}
        with self._session_scope() as session:
            for pi_model in PERFORMANCE_MODELS_ML_FRAMEWORKS:
                result[pi_model.__tablename__] = session.query(pi_model).filter_by(component=component).count()

        return result

    def get_entity_count(self, entity: Union[Base, BaseExtension]) -> int:
        """Get count of a specific entity in the database."""
        with self._session_scope() as session:
            result = session.query(func.count(entity.id)).scalar()

        return result

    def get_performance_table_count(self) -> Dict[str, int]:
        """Get dictionary mapping performance tables to records count."""
        result = {}

        with self._session_scope() as session:
            for performance_model in ALL_PERFORMANCE_MODELS:
                result[performance_model.__tablename__] = session.query(func.count(performance_model.id)).scalar()

        return result

    def get_main_table_count(self) -> Dict[str, int]:
        """Retrieve dictionary mapping main tables to records count."""
        result = {}

        with self._session_scope() as session:
            for main_model in ALL_MAIN_MODELS:
                result[main_model.__tablename__] = session.query(func.count(main_model.id)).scalar()

        return result

    def get_relation_table_count(self) -> Dict[str, int]:
        """Retrieve dictionary mapping relation tables to records count."""
        result = {}

        with self._session_scope() as session:
            for relation_model in ALL_RELATION_MODELS:
                result[relation_model.__tablename__] = session.query(relation_model).count()

        return result

    def get_pi_component_all(self) -> List[str]:
        """Retrieve pi components in Thoth database."""
        result = []
        with self._session_scope() as session:
            for performance_model in PERFORMANCE_MODELS_ML_FRAMEWORKS:
                query = session.query(performance_model).with_entities(performance_model.component).distinct()

                result = result + query.all()

        return list(set([r[0] for r in result]))

    def stats(self) -> dict:
        """Get statistics for this adapter."""
        stats = {}
        # We need to provide name explicitly as wrappers do not handle it correctly.
        for method in self._CACHED_METHODS:
            stats[method.__name__] = dict(method.cache_info()._asdict())

        return {"memory_cache_info": stats}

    def cache_clear(self) -> None:
        """Drop cache of records."""
        for method in self._CACHED_METHODS:
            method.cache_clear()

    def get_database_size(self) -> int:
        """Get size of the database in bytes."""
        query = (
            f"SELECT pg_database_size(pg_database.datname) AS size_in_bytes FROM "
            f"pg_database WHERE pg_database.datname='{self._engine.url.database}'"
        )

        with self._session_scope() as session:
            result = session.execute(query).fetchone()
            return result[0]

    def is_database_corrupted(self) -> bool:
        """
        Run the amcheck extension to check for DB corruption, false negatives are possible but false positives are not.

        amcheck documenation: https://www.postgresql.org/docs/10/amcheck.html

        Returns
        -------
        bool
            False: No DB corruption detected by amcheck (not definitive)
            True: Database is corrupted
        """
        check_for_ext_query = "SELECT * FROM pg_extension WHERE extname='amcheck'"
        run_amcheck_query = """SELECT bt_index_check(index => c.oid),
                    c.relname,
                    c.relpages
            FROM pg_index i
            JOIN pg_opclass op ON i.indclass[0] = op.oid
            JOIN pg_am am ON op.opcmethod = am.oid
            JOIN pg_class c ON i.indexrelid = c.oid
            WHERE am.amname = 'btree'
            -- Don't check temp tables, which may be from another session:
            AND c.relpersistence != 't'
            -- Function may throw an error when this is omitted:
            AND c.relkind = 'i' AND i.indisready AND i.indisvalid"""

        with self._session_scope() as session:
            if list(session.execute(check_for_ext_query)) == []:
                _LOGGER.error("amcheck extension not found.")
                return False  # do not want to accidentally mistake this state with the DB being corrupted

            try:
                session.execute(run_amcheck_query)
                return False
            except Exception as e:
                _LOGGER.error(e)
                return True

    def get_index_bloat_data(self) -> List[Dict[str, Any]]:
        """Get index bloat data.

        documenation: https://raw.githubusercontent.com/pgexperts/pgx_scripts/master/bloat/index_bloat_check.sql
        It returns data for each index/table present in the database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_index_bloat_data()
        [
            {
                'database_name': 'postgres',
                'schema_name': 'public',
                'table_name': 'depends_on',
                'index_name': 'depends_on_entity_id_idx',
                'bloat_pct': 11.0,
                'bloat_mb': 623.0,
                'index_mb': 5821.516,
                'table_mb': 14053.625,
                'index_scans': 2
            },
            {
                'database_name': 'postgres',
                'schema_name': 'public',
                'table_name': 'python_package_version',
                'index_name': 'python_package_version_package_name_package_version_python__key',
                'bloat_pct': 43.0,
                'bloat_mb': 35.0,
                'index_mb': 35.0,
                'table_mb': 111.344,
                'index_scans': 0
            }, ...
        ]
        """
        # btree index stats query estimates bloat for btree indexes
        btree_index_atts = """SELECT nspname,
            indexclass.relname as index_name,
            indexclass.reltuples,
            indexclass.relpages,
            indrelid, indexrelid,
            indexclass.relam,
            tableclass.relname as tablename,
            regexp_split_to_table(indkey::text, ' ')::smallint AS attnum,
            indexrelid as index_oid
        FROM pg_index
        JOIN pg_class AS indexclass ON pg_index.indexrelid = indexclass.oid
        JOIN pg_class AS tableclass ON pg_index.indrelid = tableclass.oid
        JOIN pg_namespace ON pg_namespace.oid = indexclass.relnamespace
        JOIN pg_am ON indexclass.relam = pg_am.oid
        WHERE pg_am.amname = 'btree' and indexclass.relpages > 0
            AND nspname NOT IN ('pg_catalog','information_schema')"""

        index_item_sizes = """SELECT
            ind_atts.nspname, ind_atts.index_name,
            ind_atts.reltuples, ind_atts.relpages, ind_atts.relam,
            indrelid AS table_oid, index_oid,
            current_setting('block_size')::numeric AS bs,
            8 AS maxalign,
            24 AS pagehdr,
            CASE WHEN max(coalesce(pg_stats.null_frac,0)) = 0
                THEN 2
                ELSE 6
            END AS index_tuple_hdr,
            sum( (1-coalesce(pg_stats.null_frac, 0)) * coalesce(pg_stats.avg_width, 1024) ) AS nulldatawidth
            FROM pg_attribute
            JOIN btree_index_atts AS ind_atts ON pg_attribute.attrelid = ind_atts.indexrelid AND pg_attribute.attnum = ind_atts.attnum
            JOIN pg_stats ON pg_stats.schemaname = ind_atts.nspname
                -- stats for regular index columns
                AND ( (pg_stats.tablename = ind_atts.tablename AND pg_stats.attname = pg_catalog.pg_get_indexdef(pg_attribute.attrelid, pg_attribute.attnum, TRUE))
                -- stats for functional indexes
                OR   (pg_stats.tablename = ind_atts.index_name AND pg_stats.attname = pg_attribute.attname))
            WHERE pg_attribute.attnum > 0
            GROUP BY 1, 2, 3, 4, 5, 6, 7, 8, 9"""

        index_aligned_est = """SELECT maxalign, bs, nspname, index_name, reltuples,
            relpages, relam, table_oid, index_oid,
            coalesce (
                ceil (
                    reltuples * ( 6
                        + maxalign
                        - CASE
                            WHEN index_tuple_hdr%maxalign = 0 THEN maxalign
                            ELSE index_tuple_hdr%maxalign
                        END
                        + nulldatawidth
                        + maxalign
                        - CASE /* Add padding to the data to align on MAXALIGN */
                            WHEN nulldatawidth::integer%maxalign = 0 THEN maxalign
                            ELSE nulldatawidth::integer%maxalign
                        END
                    )::numeric
                / ( bs - pagehdr::NUMERIC )
                +1 )
            , 0 )
        as expected
        FROM index_item_sizes"""

        raw_bloat = """SELECT current_database() as dbname, nspname, pg_class.relname AS table_name, index_name,
            bs*(index_aligned_est.relpages)::bigint AS totalbytes, expected,
            CASE
                WHEN index_aligned_est.relpages <= expected
                    THEN 0
                    ELSE bs*(index_aligned_est.relpages-expected)::bigint
                END AS wastedbytes,
            CASE
                WHEN index_aligned_est.relpages <= expected
                    THEN 0
                    ELSE bs*(index_aligned_est.relpages-expected)::bigint * 100 / (bs*(index_aligned_est.relpages)::bigint)
                END AS realbloat,
            pg_relation_size(index_aligned_est.table_oid) as table_bytes,
            stat.idx_scan as index_scans
            FROM index_aligned_est
            JOIN pg_class ON pg_class.oid=index_aligned_est.table_oid
            JOIN pg_stat_user_indexes AS stat ON index_aligned_est.index_oid = stat.indexrelid"""

        format_bloat = """SELECT dbname as database_name, nspname as schema_name, table_name, index_name,
            round(realbloat) as bloat_pct, round(wastedbytes/(1024^2)::NUMERIC) as bloat_mb,
            round(totalbytes/(1024^2)::NUMERIC,3) as index_mb,
            round(table_bytes/(1024^2)::NUMERIC,3) as table_mb,
            index_scans
            FROM raw_bloat"""

        with self._session_scope() as session:
            tables = session.execute(
                f"WITH btree_index_atts AS ({btree_index_atts}),\
                index_item_sizes AS ({index_item_sizes}),\
                index_aligned_est AS ({index_aligned_est}),\
                raw_bloat AS ({raw_bloat}),\
                format_bloat AS ({format_bloat})\
                SELECT *\
                FROM format_bloat\
                ORDER BY bloat_mb DESC; "
            )

        return self._process_bloat_data_results(tables=tables)

    @staticmethod
    def _process_bloat_data_results(tables: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        processed_bloat_data = []

        for table in tables:
            bloat_data = {}

            if "pct_bloat" in table.keys() or "mb_bloat" in table.keys():
                if table["pct_bloat"] is None:
                    continue

                if table["mb_bloat"] is None:
                    continue

            for column, value in table.items():
                if isinstance(value, Decimal):
                    bloat_data[column] = float(value)
                else:
                    bloat_data[column] = value

            processed_bloat_data.append(bloat_data)

        return processed_bloat_data

    def get_bloat_data(self) -> List[Dict[str, Any]]:
        """Get table bloat data.

        documenation: https://raw.githubusercontent.com/pgexperts/pgx_scripts/master/bloat/table_bloat_check.sql
        It returns data for each table present in the database.

        Examples:
        >>> from thoth.storages import GraphDatabase
        >>> graph = GraphDatabase()
        >>> graph.get_bloat_data()
        [
            {
                'databasename': 'postgres',
                'schemaname': 'public',
                'tablename': 'advised',
                'can_estimate': True,
                'table_bytes': 49152.0,
                'table_mb': 0.047,
                'expected_bytes': 49152.0,
                'expected_mb': 0.047,
                'pct_bloat': 0.0,
                'mb_bloat': 0.0,
                'est_rows': 1158.0
            },
            {
                'databasename': 'postgres',
                'schemaname': 'public',
                'tablename': 'adviser_run',
                'can_estimate': True,
                'table_bytes': 720896.0,
                'table_mb': 0.688,
                'expected_bytes': 712704.0,
                'expected_mb': 0.68,
                'pct_bloat': 1.0,
                'mb_bloat': 0.01,
                'est_rows': 3600.0
            }, ...
        ]
        """
        # define some constants for sizes of things
        # for reference down the query and easy maintenance
        constants = "SELECT current_setting('block_size')::numeric AS bs, 23 AS hdr, 8 AS ma"

        # screen out table who have attributes
        # which dont have stats, such as JSON
        no_stats = """SELECT table_schema, table_name,
                n_live_tup::numeric as est_rows,
                pg_table_size(relid)::numeric as table_size
            FROM information_schema.columns
                JOIN pg_stat_user_tables as psut
                ON table_schema = psut.schemaname
                AND table_name = psut.relname
                LEFT OUTER JOIN pg_stats
                ON table_schema = pg_stats.schemaname
                    AND table_name = pg_stats.tablename
                    AND column_name = attname
            WHERE attname IS NULL
                AND table_schema NOT IN ('pg_catalog', 'information_schema')
            GROUP BY table_schema, table_name, relid, n_live_tup"""

        # calculate null header sizes
        # omitting tables which dont have complete stats
        # and attributes which aren't visible
        null_headers = """SELECT
                hdr+1+(sum(case when null_frac <> 0 THEN 1 else 0 END)/8) as nullhdr,
                SUM((1-null_frac)*avg_width) as datawidth,
                MAX(null_frac) as maxfracsum,
                schemaname,
                tablename,
                hdr, ma, bs
            FROM pg_stats CROSS JOIN constants
                LEFT OUTER JOIN no_stats
                    ON schemaname = no_stats.table_schema
                    AND tablename = no_stats.table_name
            WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
                AND no_stats.table_name IS NULL
                AND EXISTS ( SELECT 1
                    FROM information_schema.columns
                        WHERE schemaname = columns.table_schema
                            AND tablename = columns.table_name )
            GROUP BY schemaname, tablename, hdr, ma, bs"""

        # estimate header and row size
        data_headers = """SELECT
                ma, bs, hdr, schemaname, tablename,
                (datawidth+(hdr+ma-(case when hdr%ma=0 THEN ma ELSE hdr%ma END)))::numeric AS datahdr,
                (maxfracsum*(nullhdr+ma-(case when nullhdr%ma=0 THEN ma ELSE nullhdr%ma END))) AS nullhdr2
            FROM null_headers"""

        # make estimates of how large the table should be
        # based on row and page size
        table_estimates = """SELECT schemaname, tablename, bs,
                reltuples::numeric as est_rows, relpages * bs as table_bytes,
            CEIL((reltuples*
                    (datahdr + nullhdr2 + 4 + ma -
                        (CASE WHEN datahdr%ma=0
                            THEN ma ELSE datahdr%ma END)
                        )/(bs-20))) * bs AS expected_bytes,
                reltoastrelid
            FROM data_headers
                JOIN pg_class ON tablename = relname
                JOIN pg_namespace ON relnamespace = pg_namespace.oid
                    AND schemaname = nspname
            WHERE pg_class.relkind = 'r'"""

        # add in estimated TOAST table sizes
        # estimate based on 4 toast tuples per page because we dont have
        # anything better.  also append the no_data tables
        estimates_with_toast = """SELECT schemaname, tablename,
                TRUE as can_estimate,
                est_rows,
                table_bytes + ( coalesce(toast.relpages, 0) * bs ) as table_bytes,
                expected_bytes + ( ceil( coalesce(toast.reltuples, 0) / 4 ) * bs ) as expected_bytes
            FROM table_estimates LEFT OUTER JOIN pg_class as toast
                ON table_estimates.reltoastrelid = toast.oid
                    AND toast.relkind = 't'"""

        # add some extra metadata to the table data and calculations to be reused
        # including whether we cant estimate it or whether we think it might be compressed
        table_estimates_plus = """SELECT current_database() as databasename,
                    schemaname, tablename, can_estimate,
                    est_rows,
                    CASE WHEN table_bytes > 0
                        THEN table_bytes::NUMERIC
                        ELSE NULL::NUMERIC END
                        AS table_bytes,
                    CASE WHEN expected_bytes > 0
                        THEN expected_bytes::NUMERIC
                        ELSE NULL::NUMERIC END
                            AS expected_bytes,
                    CASE WHEN expected_bytes > 0 AND table_bytes > 0
                        AND expected_bytes <= table_bytes
                        THEN (table_bytes - expected_bytes)::NUMERIC
                        ELSE 0::NUMERIC END AS bloat_bytes
            FROM estimates_with_toast
            UNION ALL
            SELECT current_database() as databasename,
                table_schema, table_name, FALSE,
                est_rows, table_size,
                NULL::NUMERIC, NULL::NUMERIC
            FROM no_stats"""

        # do final math calculations and formatting
        bloat_data = """SELECT current_database() as databasename,
            schemaname, tablename, can_estimate,
            table_bytes, round(table_bytes/(1024^2)::NUMERIC,3) as table_mb,
            expected_bytes, round(expected_bytes/(1024^2)::NUMERIC,3) as expected_mb,
            round(bloat_bytes*100/table_bytes) as pct_bloat,
            round(bloat_bytes/(1024::NUMERIC^2),2) as mb_bloat,
            table_bytes, expected_bytes, est_rows
        FROM table_estimates_plus"""

        with self._session_scope() as session:
            tables = session.execute(
                f"WITH constants AS ({constants}),\
                no_stats AS ({no_stats}),\
                null_headers AS ({null_headers}),\
                data_headers AS ({data_headers}),\
                table_estimates AS ({table_estimates}),\
                estimates_with_toast AS ({estimates_with_toast}),\
                table_estimates_plus AS ({table_estimates_plus}) "
                + bloat_data
            )

        return self._process_bloat_data_results(tables=tables)

    def delete_solved(self, *, os_name: str, os_version: str, python_version: str) -> int:
        """Delete corresponding solver data."""
        with self._session_scope() as session:
            return (
                session.query(EcosystemSolver)
                .filter(
                    EcosystemSolver.os_name == os_name,
                    EcosystemSolver.os_version == os_version,
                    EcosystemSolver.python_version == python_version,
                )
                .delete()
            )

    def delete_solver_result(self, solver_document_id: str) -> int:
        """Delete the corresponding solver result."""
        with self._session_scope() as session:
            return session.query(Solved).filter(Solved.document_id == solver_document_id).delete()

    def delete_adviser_run(
        self,
        *,
        end_datetime: Optional[datetime] = None,
        adviser_version: Optional[str] = None,
    ) -> int:
        """Delete corresponding adviser data."""
        delete_filter = []

        if end_datetime:
            delete_filter.append(AdviserRun.datetime < end_datetime)

        if adviser_version:
            delete_filter.append(AdviserRun.adviser_version == adviser_version)

        if not delete_filter:
            raise ValueError("No filter provided to delete adviser data")

        with self._session_scope() as session:
            return session.query(AdviserRun).filter(*delete_filter).delete()

    def delete_adviser_result(self, adviser_document_id: str) -> int:
        """Delete the corresponding adviser result."""
        with self._session_scope() as session:
            return session.query(AdviserRun).filter(AdviserRun.adviser_document_id == adviser_document_id).delete()

    def delete_package_extract_run(
        self,
        *,
        end_datetime: Optional[datetime] = None,
        package_extract_version: Optional[str] = None,
    ) -> int:
        """Delete corresponding container image analysis data."""
        delete_filter = []

        if end_datetime:
            delete_filter.append(PackageExtractRun.datetime < end_datetime)

        if package_extract_version:
            delete_filter.append(PackageExtractRun.package_extract_version == package_extract_version)

        if not delete_filter:
            raise ValueError("No filter provided to delete package-extract data")

        with self._session_scope() as session:
            return session.query(PackageExtractRun).filter(*delete_filter).delete()

    def delete_analysis_result(self, analysis_document_id: str) -> int:
        """Delete the given package-extract entry."""
        with self._session_scope() as session:
            return (
                session.query(PackageExtractRun)
                .filter(PackageExtractRun.analysis_document_id == analysis_document_id)
                .delete()
            )

    @staticmethod
    def _refresh_python_entities_rule(session: Session, rule: PythonPackageVersionEntityRule) -> None:
        """Assign the given rule to entities stored in the database if the rule applies."""
        query = session.query(PythonPackageVersionEntity).filter(
            PythonPackageVersionEntity.package_name == rule.package_name
        )

        if rule.index:
            query = query.join(PythonPackageIndex).filter(PythonPackageIndex.url == rule.index.url)

        specifier = None
        if rule.version_range:
            specifier = SpecifierSet(rule.version_range)
            specifier.prereleases = True

        for entity in query.all():
            if specifier is None or parse_version(entity.package_version) in specifier:
                PythonPackageVersionEntityRulesAssociation.get_or_create(
                    session, python_package_version_entity_id=entity.id, python_package_version_entity_rule_id=rule.id
                )

    def _refresh_rules_python_entity(self, session: Session, entity: PythonPackageVersionEntity) -> None:
        """Add all rules that applies to the given entity stored in the database."""
        version = parse_version(entity.package_version)

        rules = self.get_python_rule_all(package_name=entity.package_name, index_url=None, count=None)

        if entity.index:
            rules = itertools.chain(
                rules,
                self.get_python_rule_all(package_name=entity.package_name, index_url=entity.index.url, count=None),
            )

        for rule in rules:
            specifier = SpecifierSet(rule["version_range"])
            specifier.prereleases = True

            if not rule["version_range"] or version in specifier:
                PythonPackageVersionEntityRulesAssociation.get_or_create(
                    session,
                    python_package_version_entity_id=entity.id,
                    python_package_version_entity_rule_id=rule["id"],
                )

    def _rule_to_dict(self, rule: PythonPackageVersionEntityRule) -> Dict[str, Any]:
        """Convert a rule model to a dict representation."""
        rule_dict = rule.to_dict(without_id=False)
        index_id = rule_dict.pop("python_package_index_id")
        rule_dict["index_url"] = self.get_index_url_from_id(index_id) if index_id else None
        return rule_dict

    def create_python_rule(
        self,
        package_name: str,
        *,
        version_specifier: Optional[str] = None,
        index_url: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create the given Python rule."""
        package_name = self.normalize_python_package_name(package_name) if package_name is not None else None
        index_url = self.normalize_python_index_url(index_url) if index_url is not None else None
        version_specifier = version_specifier if version_specifier != "*" else ""

        with self._session_scope() as session:
            existing_rule_query = session.query(PythonPackageVersionEntityRule).filter(
                PythonPackageVersionEntityRule.package_name == package_name,
                PythonPackageVersionEntityRule.description == description,
            )

            if index_url:
                existing_rule_query = existing_rule_query.join(PythonPackageIndex).filter(
                    PythonPackageIndex.url == index_url
                )
            else:
                existing_rule_query = existing_rule_query.filter(
                    PythonPackageVersionEntityRule.python_package_index_id.is_(None)
                )

            existing_rule = existing_rule_query.first()

            if existing_rule:
                # SpecifierSet(",,,,") == SpecifierSet("")
                existing_rule.version_range = str(
                    SpecifierSet(",".join([existing_rule.version_range or "", version_specifier or ""]))
                )
                session.add(existing_rule)
                session.commit()
                self._refresh_python_entities_rule(session, existing_rule)
                return self._rule_to_dict(existing_rule)

            index = None
            if index_url:
                index = session.query(PythonPackageIndex).filter(PythonPackageIndex.url == index_url).first()
                if not index:
                    raise NotFoundError(f"No index with url {index_url!r} registered")

            rule = PythonPackageVersionEntityRule(
                package_name=package_name,
                version_range=str(SpecifierSet(version_specifier or "")),
                python_package_index_id=index.id,
                description=description,
            )
            session.add(rule)
            session.commit()
            self._refresh_python_entities_rule(session, rule)
            return self._rule_to_dict(rule)

    def delete_python_rule(self, rule_id: int) -> int:
        """Delete the given Python rule."""
        with self._session_scope() as session:
            return (
                session.query(PythonPackageVersionEntityRule)
                .filter(PythonPackageVersionEntityRule.id == rule_id)
                .delete()
            )

    def get_python_rule(self, rule_id: int) -> Dict[str, Any]:
        """Get the given Python rule."""
        with self._session_scope() as session:
            result = (
                session.query(PythonPackageVersionEntityRule)
                .filter(PythonPackageVersionEntityRule.id == rule_id)
                .first()
            )

            if not result:
                raise NotFoundError(f"No Python rule with id {rule_id!r} found")

            return self._rule_to_dict(result)

    def get_python_rule_all(
        self,
        *,
        package_name: Optional[str] = None,
        index_url: Optional[str] = None,
        start_offset: int = 0,
        count: Optional[int] = DEFAULT_COUNT,
    ) -> List[Dict[str, Any]]:
        """Get all the Python rules matching the given query criteria."""
        package_name = self.normalize_python_package_name(package_name) if package_name is not None else None
        index_url = self.normalize_python_index_url(index_url) if index_url is not None else None

        with self._session_scope() as session:
            query = session.query(PythonPackageVersionEntityRule)

            if package_name:
                query = query.filter(PythonPackageVersionEntityRule.package_name == package_name)

            if index_url:
                query = query.join(PythonPackageIndex).filter(PythonPackageIndex.url == index_url)

            query = query.order_by(desc(PythonPackageVersionEntityRule.id)).offset(start_offset)

            if count is not None:
                query = query.limit(count)

            result = []
            for rule in query.all():
                result.append(self._rule_to_dict(rule))

            return result

    @lru_cache(maxsize=_GET_PYTHON_PYTHON_PACKAGE_VERSION_SOLVER_RULES_CACHE_SIZE)
    def get_python_package_version_solver_rules_all(
        self,
        package_name: str,
        package_version: str,
        index_url: Optional[str] = None,
    ) -> List[str]:
        """Get rules assigned for the given Python package."""
        package_name = self.normalize_python_package_name(package_name)
        self.normalize_python_package_version(package_version)
        index_url = self.normalize_python_index_url(index_url) if index_url is not None else None

        with self._session_scope() as session:
            query = session.query(PythonPackageVersionEntity).filter(
                PythonPackageVersionEntity.package_name == package_name,
                PythonPackageVersionEntity.package_version == package_version,
            )

            if index_url:
                query = query.join(PythonPackageIndex).filter(PythonPackageIndex.url == index_url)

            return [
                i[0]
                for i in query.join(PythonPackageVersionEntityRulesAssociation)
                .join(PythonPackageVersionEntityRule)
                .with_entities(PythonPackageVersionEntityRule.description)
                .all()
            ]

    @lru_cache(maxsize=_GET_RPM_PACKAGE_VERSION_CACHE_SIZE)
    def get_rpm_package_version_all(self, analysis_document_id: str) -> List[Dict[str, str]]:
        """Retrieve RPM package information for the given container image analysis."""
        with self._session_scope() as session:
            query = (
                session.query(PackageExtractRun)
                .filter(PackageExtractRun.analysis_document_id == analysis_document_id)
                .join(FoundRPM)
                .join(RPMPackageVersion)
                .with_entities(RPMPackageVersion)
            )

            return [i.to_dict() for i in query.all()]

    @lru_cache(maxsize=_GET_RPM_PACKAGE_VERSION_CACHE_SIZE)
    def get_python_package_version_all(self, analysis_document_id: str) -> List[Dict[str, str]]:
        """Retrieve Python package information for the given container image analysis."""
        with self._session_scope() as session:
            query = (
                session.query(PackageExtractRun)
                .filter(PackageExtractRun.analysis_document_id == analysis_document_id)
                .join(Identified)
                .join(PythonPackageVersionEntity)
                .with_entities(
                    Identified.location,
                    PythonPackageVersionEntity.package_name,
                    PythonPackageVersionEntity.package_version,
                )
            )

            return [{"package_name": i[1], "package_version": i[2], "location": i[0]} for i in query.all()]

    def get_python_package_version_import_packages_all(self, import_name: str) -> List[str]:
        """Retrieve Python package name for the given import package name."""
        with self._session_scope() as session:
            query = (
                session.query(PythonPackageVersion)
                .join(FoundImportPackage)
                .join(ImportPackage)
                .filter(ImportPackage.import_package_name == import_name)
                .filter(PythonPackageVersion.id == FoundImportPackage.python_package_version_id)
                .join(PythonPackageIndex)
                .filter(PythonPackageVersion.python_package_index_id == PythonPackageIndex.id)
                .with_entities(
                    PythonPackageVersion.package_name, PythonPackageVersion.package_version, PythonPackageIndex.url
                )
            )
            result = [{"package_name": i[0], "package_version": i[1], "index_url": i[2]} for i in query.all()]

            if not result:
                raise NotFoundError(f"No package matching import {import_name!r} found")

            return result

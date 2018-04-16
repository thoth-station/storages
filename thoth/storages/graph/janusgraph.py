"""A Gremlin server adapter communicating via a web socket."""

import asyncio
import functools
import logging
import os

import uvloop
from goblin import Goblin

from thoth.common import datetime_str2timestamp

from ..base import StorageBase
from .models import ALL_MODELS
from .models import DependsOn
from .models import EcosystemSolver
from .models import HasVersion
from .models import IsPartOf
from .models import Package
from .models import PythonPackageVersion
from .models import Solved
from .models import Requires
from .models import RPMPackageVersion
from .models import RPMRequirement
from .models import RuntimeEnvironment
from .utils import enable_edge_cache
from .utils import enable_vertex_cache

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


def requires_connection(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.is_connected():
            self.connect()
        func(self, *args, **kwargs)

    return wrapper


class GraphDatabase(StorageBase):
    """A Gremlin server adapter communicating via a web socket."""

    ENVVAR_HOST_NAME = 'THOTH_JANUSGRAPH_HOST'
    ENVVAR_HOST_PORT = 'THOTH_JANUSGRAPH_PORT'

    DEFAULT_HOST = os.getenv(ENVVAR_HOST_NAME) or 'localhost'
    DEFAULT_PORT = os.getenv(ENVVAR_HOST_PORT) or 8182

    DEFAULT_SERIALIZER = {
        'className': 'org.apache.tinkerpop.gremlin.driver.ser.GryoMessageSerializerV1d0',
        'config': {
            'serializeResultToString': True
        }
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
        """Retrieve the g object for synchronous operations with the graph database."""
        return self.session.g

    @property
    def session(self):
        """Returns session to the graph database."""
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.app.session())

    def is_connected(self):
        """Check if we are connected to a remote Gremlin server."""
        # TODO: this will maybe require some logic to be sure that the connection is healthy.
        return self.app is not None

    def connect(self):
        """Connect to a graph database via a websocket, use GraphSONSerializersV2d0."""
        loop = asyncio.get_event_loop()
        self.app = loop.run_until_complete(Goblin.open(
            loop,
            get_hashable_id=_get_hashable_id,
            hosts=self.hosts,
            port=self.port,
            serializer=self.serializer
        ))
        self.app.register(*tuple(ALL_MODELS))

    def disconnect(self):
        """Close all connections - disconnect from remote."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.app.close())
        self.app = None

    #@enable_edge_cache
    @enable_vertex_cache
    def sync_solver_result(self, document: dict) -> None:
        ecosystem_solver = EcosystemSolver.from_properties(
            solver_name=document['metadata']['analyzer'],
            solver_version=document['metadata']['analyzer_version']
        )
        ecosystem_solver.get_or_create(self.g)

        solver_document_id = document['metadata']['hostname']
        solver_datetime = datetime_str2timestamp(document['metadata']['datetime'])

        for python_package_info in document['result']['tree']:
            try:
                python_package_version = PythonPackageVersion.from_properties(
                    ecosystem='pypi',
                    package_name=python_package_info['package_name'].lower(),
                    package_version=python_package_info['package_version']
                )
                python_package_version.get_or_create(self.g)

                Solved.from_properties(
                    source=ecosystem_solver,
                    target=python_package_version,
                    solver_document_id=solver_document_id,
                    solver_datetime=solver_datetime,
                    solver_error=False
                ).get_or_create(self.g)

                python_package = Package.from_properties(
                    ecosystem=python_package_version.ecosystem,
                    package_name=python_package_version.package_name
                )
                python_package.get_or_create(self.g)

                HasVersion.from_properties(
                    source=python_package,
                    target=python_package_version
                ).get_or_create(self.g)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(f"Failed to sync Python package, error is not fatal: {python_package_info!r}")
                continue

            for dependency in python_package_info['dependencies']:
                try:
                    for dependency_version in dependency['resolved_versions']:
                        python_package_version_dependency = PythonPackageVersion.from_properties(
                            package_name=dependency['package_name'],
                            package_version=dependency_version,
                            ecosystem='pypi'
                        )
                        python_package_version_dependency.get_or_create(self.g)

                        Solved.from_properties(
                            source=ecosystem_solver,
                            target=python_package_version_dependency,
                            solver_document_id=solver_document_id,
                            solver_datetime=solver_datetime,
                            solver_error=False
                        ).get_or_create(self.g)

                        python_package_dependency = Package.from_properties(
                            ecosystem=python_package_version_dependency.ecosystem,
                            package_name=python_package_version_dependency.package_name
                        )
                        python_package_dependency.get_or_create(self.g)

                        HasVersion.from_properties(
                            source=python_package_dependency,
                            target=python_package_version_dependency
                        ).get_or_create(self.g)

                        # TODO: mark extras
                        DependsOn.from_properties(
                            source=python_package_version,
                            target=python_package_version_dependency,
                            version_range=dependency['required_version']
                        ).get_or_create(self.g)
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.exception(f"Failed to sync Python package {python_package_version.to_dict()} "
                                      f"dependency: {dependency}")

        for error_info in document['result']['errors']:
            try:
                python_package_version = PythonPackageVersion.from_properties(
                    package_name=error_info.get('package_name') or error_info['package'],   # Check this inconsistency.
                    package_version=error_info['version'],
                    ecosystem='pypi'
                )
                python_package_version.get_or_create(self.g)

                Solved.from_properties(
                    source=ecosystem_solver,
                    target=python_package_version,
                    solver_document_id=solver_document_id,
                    solver_datetime=solver_datetime,
                    solver_error=True
                ).get_or_create(self.g)

                python_package = Package.from_properties(
                    ecosystem=python_package_version.ecosystem,
                    package_name=python_package_version.package_name
                )
                python_package.get_or_create(self.g)

                HasVersion.from_properties(
                    source=python_package,
                    target=python_package_version
                ).get_or_create(self.g)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(f"Failed to sync Python package, error is not fatal: {error_info!r}")

    #@enable_edge_cache
    @enable_vertex_cache
    def sync_analysis_result(self, document: dict) -> None:
        runtime_environment = RuntimeEnvironment.from_properties(
            runtime_environment_name=document['metadata']['arguments']['extract-image']['image'],
        )
        runtime_environment.get_or_create(self.g)

        # RPM packages
        for rpm_package_info in document['result']['rpm-dependencies']:
            try:
                rpm_package_version = RPMPackageVersion.from_properties(
                    ecosystem='rpm',
                    package_name=rpm_package_info['name'],
                    package_version=rpm_package_info['version'],
                    release=rpm_package_info.get('release'),
                    epoch=rpm_package_info.get('epoch'),
                    arch=rpm_package_info.get('arch'),
                    src=rpm_package_info.get('src', False),
                    package_identifier=rpm_package_info.get('package_identifier', rpm_package_info['name'])
                )
                rpm_package_version.get_or_create(self.g)

                rpm_package = Package.from_properties(
                    ecosystem=rpm_package_version.ecosystem,
                    package_name=rpm_package_version.package_name,
                )
                rpm_package.get_or_create(self.g)

                HasVersion.from_properties(
                    source=rpm_package,
                    target=rpm_package_version
                ).get_or_create(self.g)

                IsPartOf.from_properties(
                    source=rpm_package_version,
                    target=runtime_environment,
                    analysis_datetime= datetime_str2timestamp(document['metadata']['datetime']),
                    analysis_document_id=document['metadata']['hostname'],
                    analyzer_name=document['metadata']['analyzer'],
                    analyzer_version=document['metadata']['analyzer_version']
                ).get_or_create(self.g)

            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(f"Failed to sync RPM package, error is not fatal: {rpm_package_info!r}")
                continue

            for dependency in rpm_package_info['dependencies']:
                try:
                    rpm_requirement = RPMRequirement.from_properties(rpm_requirement_name=dependency)
                    rpm_requirement.get_or_create(self.g)

                    Requires.from_properties(
                        source=rpm_package_version,
                        target=rpm_requirement,
                        analysis_datetime= datetime_str2timestamp(document['metadata']['datetime']),
                        analysis_document_id=document['metadata']['hostname'],
                        analyzer_name=document['metadata']['analyzer'],
                        analyzer_version=document['metadata']['analyzer_version']
                    ).get_or_create(self.g)
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.exception(f"Failed to sync dependencies for "
                                      f"RPM {rpm_package_version.to_dict()}: {dependency!r}")

        # Python packages
        for python_package_info in document['result']['mercator'] or []:  # or [] should go to analyzer to be consistent
            try:
                python_package_version = PythonPackageVersion.from_properties(
                    ecosystem='pypi',
                    package_name=python_package_info['result']['name'].lower(),
                    package_version=python_package_info['result']['version']
                )
                python_package_version.get_or_create(self.g)

                python_package = Package.from_properties(
                    ecosystem=python_package_version.ecosystem,
                    package_name=python_package_version.package_name
                )
                python_package.get_or_create(self.g)

                HasVersion.from_properties(
                    source=python_package,
                    target=python_package_version
                ).get_or_create(self.g)

                IsPartOf.from_properties(
                    source=python_package_version,
                    target=runtime_environment,
                    analysis_datetime=datetime_str2timestamp(document['metadata']['datetime']),
                    analysis_document_id=document['metadata']['hostname'],
                    analyzer_name=document['metadata']['analyzer'],
                    analyzer_version=document['metadata']['analyzer_version']
                ).get_or_create(self.g)
            except Exception:  # pylint: disable=broad-exception
                _LOGGER.exception(f"Failed to sync Python package, error is not fatal: {python_package_info!r}")

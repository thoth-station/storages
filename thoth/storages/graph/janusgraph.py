"""A Gremlin server adapter communicating via a web socket."""

import asyncio
import functools
import logging
import os
import typing

import uvloop
from gremlin_python.process.graph_traversal import inE
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
#from .utils import enable_edge_cache
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

    def python_package_version_exists(self, package_name: str, package_version: str) -> bool:
        """Check if the given Python package version exists in the graph database."""
        loop = asyncio.get_event_loop()

        query = self.g.V() \
            .has('package_name', package_name) \
            .has('package_version', package_version) \
            .has('__label__', PythonPackageVersion.__label__).constant(True) \
            .next()

        return bool(loop.run_until_complete(query))

    def retrieve_unsolved_pypi_packages(self) -> dict:
        """Retrieve a dictionary mapping package names to versions that dependencies were not yet resolved."""
        query = self.g.V() \
            .has('__label__', 'python_package_version') \
            .has('__type__', 'vertex') \
            .has('ecosystem', 'pypi') \
            .has('package_name') \
            .has('package_version') \
            .not_(
                inE()
                .has('__label__', Solved.__label__)
                .has('__type__', 'edge')
            ).group().by('package_name').by('package_version') \
            .next()

        return asyncio.get_event_loop().run_until_complete(query)

    def retrieve_dependent_packages(self, package_name: str) -> dict:
        """Get mapping package name to package version of packages that depend on the given package."""
        # TODO: when added __type__ Cassanda backend time outs. This should be fixed once we move to Data Hub.
        query = self.g.E() \
            .has('__label__', 'depends_on') \
            .has('package_name', package_name) \
            .outV() \
            .dedup() \
            .group().by('package_name').by('package_version') \
            .next()

        return asyncio.get_event_loop().run_until_complete(query)

    def solver_records_exist(self, solver_document: dict) -> bool:
        """Check whether the given solver document record exists in the graph database."""
        loop = asyncio.get_event_loop()

        query = self.g.V() \
            .has('__label__', EcosystemSolver.__label__) \
            .has('__type__', 'vertex') \
            .has('solver_name', solver_document['metadata']['analyzer']) \
            .has('solver_version', solver_document['metadata']['analyzer_version']) \
            .outE() \
            .has('__type__', 'edge') \
            .has('__label__', Solved.__label__) \
            .has('solver_document_id', solver_document['metadata']['hostname']) \
            .has('solver_datetime', datetime_str2timestamp(solver_document['metadata']['datetime'])) \
            .count().next()

        return loop.run_until_complete(query) > 0

    def analysis_records_exist(self, analysis_document: dict) -> bool:
        """Check whether the given analysis document records exist in the graph database."""
        loop = asyncio.get_event_loop()

        query = self.g.E() \
            .has('__label__', IsPartOf.__label__) \
            .has('__type__', 'edge') \
            .has('analysis_datetime', datetime_str2timestamp(analysis_document['metadata']['datetime'])) \
            .has('analysis_document_id', analysis_document['metadata']['hostname']) \
            .has('analyzer_name', analysis_document['metadata']['analyzer']) \
            .has('analyzer_version', analysis_document['metadata']['analyzer_version'])\
            .count().next()

        return loop.run_until_complete(query) > 0

    def create_pypi_package_version(self, package_name: str, package_version: str, *,
                                    only_if_package_seen: bool=False) -> typing.Union[None, tuple]:
        """Create entries for PyPI package version."""
        package_name = package_name.lower()

        if only_if_package_seen:
            query = self.g.V() \
                .has('__type__', 'vertex') \
                .has('__label__', Package.__label__) \
                .has('ecosystem', 'pypi') \
                .has('package_name', package_name) \
                .count().next()
            seen = asyncio.get_event_loop().run_until_complete(query)
            if not seen:
                return None

        python_package = Package.from_properties(
            ecosystem='pypi',
            package_name=package_name
        )
        python_package.get_or_create(self.g)

        python_package_version = PythonPackageVersion.from_properties(
            ecosystem='pypi',
            package_name=package_name,
            package_version=package_version
        )
        python_package_version.get_or_create(self.g)

        has_version = HasVersion.from_properties(
            source=python_package,
            target=python_package_version
        )
        has_version.get_or_create(self.g)

        return python_package, has_version, python_package_version

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
                python_package, _, python_package_version = self.create_pypi_package_version(
                    python_package_info['package_name'].lower(),
                    python_package_info['package_version']
                )

                Solved.from_properties(
                    source=ecosystem_solver,
                    target=python_package_version,
                    solver_document_id=solver_document_id,
                    solver_datetime=solver_datetime,
                    solver_error=False
                ).get_or_create(self.g)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception(f"Failed to sync Python package, error is not fatal: {python_package_info!r}")
                continue

            for dependency in python_package_info['dependencies']:
                try:
                    for dependency_version in dependency['resolved_versions']:
                        python_package_dependency, _, python_package_version_dependency = \
                            self.create_pypi_package_version(
                                package_name=dependency['package_name'],
                                package_version=dependency_version
                            )

                        Solved.from_properties(
                            source=ecosystem_solver,
                            target=python_package_version_dependency,
                            solver_document_id=solver_document_id,
                            solver_datetime=solver_datetime,
                            solver_error=False
                        ).get_or_create(self.g)

                        # TODO: mark extras
                        DependsOn.from_properties(
                            source=python_package_version,
                            target=python_package_version_dependency,
                            package_name=python_package_version_dependency.package_name.value,
                            version_range=dependency['required_version'] or '*'
                        ).get_or_create(self.g)
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.exception(f"Failed to sync Python package {python_package_version.to_dict()} "
                                      f"dependency: {dependency}")

        for error_info in document['result']['errors']:
            try:
                python_package, _, python_package_version = self.create_pypi_package_version(
                    package_name=error_info.get('package_name') or error_info['package'],
                    package_version=error_info['version'],
                )

                Solved.from_properties(
                    source=ecosystem_solver,
                    target=python_package_version,
                    solver_document_id=solver_document_id,
                    solver_datetime=solver_datetime,
                    solver_error=True
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
                    analysis_datetime=datetime_str2timestamp(document['metadata']['datetime']),
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
                        analysis_datetime=datetime_str2timestamp(document['metadata']['datetime']),
                        analysis_document_id=document['metadata']['hostname'],
                        analyzer_name=document['metadata']['analyzer'],
                        analyzer_version=document['metadata']['analyzer_version']
                    ).get_or_create(self.g)
                except Exception:  # pylint: disable=broad-except
                    _LOGGER.exception(f"Failed to sync dependencies for "
                                      f"RPM {rpm_package_version.to_dict()}: {dependency!r}")

        # Python packages
        for python_package_info in document['result']['mercator'] or []:  # or [] should go to analyzer to be consistent
            if python_package_info['ecosystem'] == 'Python-RequirementsTXT':
                # We don't want to sync found requirement.txt artifacts as they do not carry any
                # valuable information for us.
                continue

            try:
                python_package, _, python_package_version = self.create_pypi_package_version(
                    package_name=python_package_info['result']['name'].lower(),
                    package_version=python_package_info['result']['version']
                )

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

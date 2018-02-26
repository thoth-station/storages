"""A Gremlin server adapter communicating via a web socket."""

import asyncio
import functools
import logging
import os

from goblin import Goblin

from .models import DependsOn
from .models import PackageVersion


_LOGGER = logging.getLogger(__name__)


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


class JanusGraphDatabase(object):
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
        self.app.register(DependsOn, PackageVersion)

    def disconnect(self):
        """Close all connections - disconnect from remote."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.app.close())
        self.app = None

    async def _get_or_create_node(self, ecosystem: str, package_name: str, package_version: str) \
            -> (PackageVersion, bool):
        """Create a node if not exists, otherwise return id of an existing one."""
        session = await self.app.session()

        package = await session.traversal(PackageVersion).\
            has(PackageVersion.name, package_name).\
            has(PackageVersion.ecosystem, ecosystem).\
            has(PackageVersion.version, package_version).toList()

        if package:
            _LOGGER.debug(f"Package {ecosystem}/{package_name}/{package_version} already exists: "
                          f"{package[0].to_dict()}")
            if len(package) > 1:
                _LOGGER.error("Multiple nodes for same package found, package %r, version %r, nodes: %s",
                              package_name, package_version, [p.to_dict() for p in package])
            return package[0], True

        package = PackageVersion()
        package.ecosystem = ecosystem
        package.name = package_name
        package.version = package_version

        session.add(package)
        _LOGGER.debug(f"Package {ecosystem}/{package_name}/{package_version} added: {package.to_dict()}")
        await session.flush()

        return package, False

    async def _get_or_create_edge_depends_on(self, from_node, to_node, edge):
        """Create the given edge."""
        session = await self.app.session()

        # TODO: create a generic way how to accomplish this
        existing_edge = await session.g.V(from_node.id).\
            outE().\
            as_('e').\
            has(edge.__class__.version_range, edge.version_range).\
            inV().\
            hasId(to_node.id).\
            select('e').\
            toList()

        if existing_edge:
            _LOGGER.debug(f"DependsOn edge between nodes {from_node.to_dict()} and {to_node.to_dict()} "
                          f"already exists: {existing_edge[0].to_dict()}")
            if len(existing_edge) > 1:
                _LOGGER.error("Multiple edges found, from node %r to node %r, edges: %s",
                              from_node.to_dict(), to_node.to_dict(), [p.to_dict() for p in existing_edge])
            return existing_edge[0], True

        edge.source = from_node
        edge.target = to_node
        session.add(edge)
        _LOGGER.debug(f"DependsOn edge between nodes {from_node.to_dict()} and {to_node.to_dict()} added: "
                      f"{edge.to_dict()}")
        await session.flush()

        return edge, False

    async def _async_store_pypi_package(self, package_name: str, package_version: str, dependencies: list) -> None:
        """Store the given PyPI package into the graph database and construct dependency graph based on dependencies."""
        # TODO: we assume that all of these queries succeed
        package_node, _ = await self._get_or_create_node('pypi', package_name, package_version)

        for dependency in dependencies:
            dependency_name = dependency['package_name']
            for dependency_version in dependency['resolved_versions']:
                dependency_node, _ = await self._get_or_create_node(
                    'pypi',
                    dependency_name,
                    dependency_version
                )

                version_range = dependency['required_version'] or '*'
                edge = DependsOn()
                edge.version_range = version_range
                await self._get_or_create_edge_depends_on(package_node, dependency_node, edge)

    @requires_connection
    def store_pypi_package(self, package_name: str, package_version: str, dependencies: list) -> None:
        """Store the given PyPI package into the graph database and construct dependency graph based on dependencies."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._async_store_pypi_package(package_name, package_version, dependencies))

    @requires_connection
    def store_pypi_solver_result(self, document_id, solver_result):
        """Store results of Thoth's PyPI dependency solver."""
        # TODO: use document_id to keep result traceable
        for entry in solver_result['result']['tree']:
            self.store_pypi_package(entry['package_name'], entry['package_version'], entry['dependencies'])

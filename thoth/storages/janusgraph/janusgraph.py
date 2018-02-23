"""A Gremlin server adapter communicating via a web socket."""

import logging
import asyncio

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


class JanusGraphDatabase(object):
    """A Gremlin server adapter communicating via a web socket."""

    def __init__(self, hosts=None, port=8182, serializer=None):
        """Initialize Gremlin server database adapter."""
        super().__init__()
        self.app = None
        #self.hosts = hosts or ['thoth-janusgraph-hostname-thoth-middleend.127.0.0.1.nip.io']
        self.hosts = hosts or ['localhost']
        self.port = port
        self.serializer = serializer or {
            'className': 'org.apache.tinkerpop.gremlin.driver.ser.GryoMessageSerializerV1d0',
            'config': {
                'serializeResultToString': True
            }
        }

    def is_connected(self):
        """Check if we are connected to a remote Gremlin server."""
        # TODO: this will require some logic to be sure that the connection is healthy.
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

    async def _get_or_create_node(self, ecosystem: str, package_name: str, package_version: str) \
            -> (PackageVersion, bool):
        """Create a node if not exists, otherwise return id of an existing one."""
        session = await self.app.session()

        package = await session.traversal(PackageVersion).\
            has(PackageVersion.name, package_name).\
            has(PackageVersion.ecosystem, ecosystem).\
            has(PackageVersion.version, package_version).toList()

        if package:
            if len(package) > 1:
                _LOGGER.error("Multiple nodes for same package found, package %r, version %r, nodes: %s",
                              package_name, package_version, [p.to_dict() for p in package])
            return package[0], True

        package = PackageVersion()
        package.ecosystem = ecosystem
        package.name = package_name
        package.version = package_version

        session.add(package)
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
            if len(existing_edge) > 1:
                _LOGGER.error("Multiple edges found, from node %r to node %r, edges: %s",
                              from_node.to_dict(), to_node.to_dict(), [p.to_dict() for p in existing_edge])
            return existing_edge[0], True

        edge.source = from_node
        edge.target = to_node
        session.add(edge)
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

    def store_pypi_package(self, package_name: str, package_version: str, dependencies: list) -> None:
        """Store the given PyPI package into the graph database and construct dependency graph based on dependencies."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._async_store_pypi_package(package_name, package_version, dependencies))

    def store_pypi_solver_result(self, solver_result):
        """Store results of Thoth's PyPI dependency solver."""
        for entry in solver_result['tree']:
            self.store_pypi_package(entry['package_name'], entry['package_version'], entry['dependencies'])

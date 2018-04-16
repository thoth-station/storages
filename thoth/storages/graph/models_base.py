"""A base classes for model representation."""

import asyncio

from goblin import Vertex
from goblin import Edge

from aiogremlin.process.graph_traversal import AsyncGraphTraversalSource


class VertexBase(Vertex):
    """A base class for edges that extends Goblin's vertex implementation."""

    # Vertex cache to be used.
    cache = None

    def __repr__(self):
        values = ''
        for key, value in self.to_dict().items():
            if key.startswith('__'):
                continue
            values += '{}={}, '.format(key, repr(value) if isinstance(value, str) else value)

        return f'{self.__class__.__name__}({values[:-2]})'

    def get_or_create(self, g: AsyncGraphTraversalSource) -> bool:
        """Get or create this vertex."""
        # Avoid cyclic imports due to typing.
        from .utils import get_or_create_vertex

        loop = asyncio.get_event_loop()
        _, existed = loop.run_until_complete(get_or_create_vertex(g, self))
        return existed

    @classmethod
    def from_properties(cls, **vertex_properties):
        """Create a vertex based on its properties."""
        instance = cls()

        for attr, value in vertex_properties.items():
            # Ensure that the instance has the given attribute.
            getattr(instance, attr)
            setattr(instance, attr, value)

        return instance


class EdgeBase(Edge):
    """A base class for edges that extends Goblin's edge implementation."""

    # Edge cache to be used.
    cache = None

    def __repr__(self):
        values = ''
        for key, value in self.to_dict().items():
            if key.startswith('__'):
                continue
            values += '{}={}, '.format(key, repr(value) if isinstance(value, str) else value)

        return f'{self.__class__.__name__}({values[:-2]})'

    def get_or_create(self, g: AsyncGraphTraversalSource) -> bool:
        """Get or create a this edge."""
        # Avoid cyclic imports due to typing.
        from .utils import get_or_create_edge

        loop = asyncio.get_event_loop()
        _, existed = loop.run_until_complete(get_or_create_edge(g, self))

        return existed

    @classmethod
    def from_properties(cls, **edge_properties):
        """Create edge based on its properties.

        >>> source_node = PackageVersion.from_properties(ecosystem='pypi', name='selinon', version='1.0.0rc1')
        >>> target_node = PackageVersion.from_properties(ecosystem='pypi', name='pyyaml', version='1.0.0')
        >>> edge = DependsOn.from_properties(version_range='>=10', source=source_node, target=target_node)
        """
        instance = cls()

        for attr, value in edge_properties.items():
            setattr(instance, attr, value)

        return instance

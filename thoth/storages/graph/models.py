"""Graph database schema."""

from goblin.element import Vertex
from goblin.element import Edge
from goblin import properties


class VertexBase(Vertex):
    """A base class for edges that extends Goblin's vertex implementation."""

    @classmethod
    def create(cls, **vertex_properties):
        """Create vertex based on its properties.

        See :meth:`thoth.storages.graph.models.EdgeBase.create`.
        """
        instance = cls()

        for attr, value in vertex_properties.items():
            setattr(instance, attr, value)

        return instance


class EdgeBase(Edge):
    """A base class for edges that extends Goblin's edge implementation."""

    @classmethod
    def create(cls, **edge_properties):
        """Create edge based on its properties.

        >>> source_node = PackageVersion.create(ecosystem='pypi', name='selinon', version='1.0.0rc1')
        >>> target_node = PackageVersion.create(ecosystem='pypi', name='pyyaml', version='1.0.0')
        >>> edge = DependsOn.create(version_range='>=10', source=source_node, target=target_node)
        """
        instance = cls()

        for attr, value in edge_properties.items():
            setattr(instance, attr, value)

        return instance


class Package(VertexBase):
    """Package node in graph representing a package without version."""
    ecosystem = properties.Property(properties.String)
    name = properties.Property(properties.String)
    # TODO: adjust sync


class PackageVersion(VertexBase):
    """Package-version node in graph representing any versioned package."""
    ecosystem = properties.Property(properties.String)
    name = properties.Property(properties.String)
    version = properties.Property(properties.String)


class DependsOn(EdgeBase):
    """Dependency between packages modeling."""
    version_range = properties.Property(properties.String, default='*')
    document_id = properties.Property(properties.String)

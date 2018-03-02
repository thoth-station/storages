"""Graph database schema."""

from goblin import element
from goblin import properties


class PackageVersion(element.Vertex):
    """Package-version node in graph representing any versioned package."""
    ecosystem = properties.Property(properties.String)
    name = properties.Property(properties.String)
    version = properties.Property(properties.String)


class DependsOn(element.Edge):
    """Dependency between packages modeling."""
    version_range = properties.Property(properties.String, default='*')
    document_id = properties.Property(properties.String)

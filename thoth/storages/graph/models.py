"""Graph database schema."""

from goblin import Property
from goblin import VertexProperty
import goblin.properties as properties

from .models_base import VertexBase
from .models_base import EdgeBase


class Package(VertexBase):
    """Package vertex in the graph representing a package without version."""

    ecosystem = VertexProperty(properties.String)
    package_name = VertexProperty(properties.String)


class RPMRequirement(VertexBase):
    """Requirement of an RPM as stated in a spec file."""

    rpm_requirement_name = VertexProperty(properties.String)


class PackageVersionBase(VertexBase):
    """Package-version vertex in the graph representing any versioned package."""

    ecosystem = VertexProperty(properties.String)
    package_name = VertexProperty(properties.String)
    package_version = VertexProperty(properties.String)


class RPMPackageVersion(PackageVersionBase):
    """RPM-specific package version."""

    release = VertexProperty(properties.String)
    epoch = VertexProperty(properties.String)
    arch = VertexProperty(properties.String)
    src = VertexProperty(properties.Boolean)
    package_identifier = VertexProperty(properties.String)


class PythonPackageVersion(PackageVersionBase):
    """Python package version vertex."""


class RuntimeEnvironment(VertexBase):
    """Environment such as container image which consists of various packages."""

    runtime_environment_name = VertexProperty(properties.String)
    # TODO: capture hashes of layers


class SoftwareStack(VertexBase):
    """Observations we have about the given stack."""

    # TODO: add observation info and info about origin


class EcosystemSolver(VertexBase):
    """Solver used to resolve dependencies within ecosystem."""

    solver_name = VertexProperty(properties.String)
    solver_version = VertexProperty(properties.String)


class DependsOn(EdgeBase):
    """Dependency between packages modeling based on ecosystem specification."""

    version_range = Property(properties.String, default='*')
    package_name = Property(properties.String)
    extras = Property(properties.String)


class IsPartOf(EdgeBase):
    """Connection to environment."""

    analysis_datetime = Property(properties.Integer)
    analysis_document_id = Property(properties.String)
    analyzer_name = Property(properties.String)
    analyzer_version = Property(properties.String)


class Solved(EdgeBase):
    """Stores information about which EcosystemSolver solved/introduced package."""

    solver_document_id = Property(properties.String)
    solver_datetime = Property(properties.Integer)
    solver_error = Property(properties.Boolean)


class Requires(EdgeBase):
    """Requirement edge of an RPM package."""

    analysis_document_id = Property(properties.String)
    analysis_datetime = Property(properties.Integer)
    analyzer_name = Property(properties.String)
    analyzer_version = Property(properties.String)


class CreatesStack(EdgeBase):
    """The given set of packages create a stack."""


class HasVersion(EdgeBase):
    """The given package has a specific version."""


class RunsIn(EdgeBase):
    """The given software stack runs in a runtime environment."""


ALL_MODELS = frozenset((
    CreatesStack,
    DependsOn,
    EcosystemSolver,
    HasVersion,
    IsPartOf,
    Package,
    PythonPackageVersion,
    Requires,
    RPMPackageVersion,
    RPMRequirement,
    RuntimeEnvironment,
    SoftwareStack,
    Solved,
))

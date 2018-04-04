"""Graph database schema."""

from goblin import properties

from thoth.common import datetime_str2timestamp

from .models_base import VertexBase
from .models_base import EdgeBase


class Package(VertexBase):
    """Package vertex in the graph representing a package without version."""

    ecosystem = properties.Property(properties.String)
    name = properties.Property(properties.String)


class RPMRequirement(VertexBase):
    """Requirement of an RPM as stated in a spec file."""

    name = properties.Property(properties.String)


class PackageVersionBase(VertexBase):
    """Package-version vertex in the graph representing any versioned package."""

    ecosystem = properties.Property(properties.String)
    name = properties.Property(properties.String)
    version = properties.Property(properties.String)

    @classmethod
    def construct(cls, *args, **kwargs):
        raise NotImplementedError


class RPMPackageVersion(PackageVersionBase):
    """RPM-specific package version."""

    release = properties.Property(properties.String)
    epoch = properties.Property(properties.String)
    arch = properties.Property(properties.String)
    src = properties.Property(properties.Boolean)
    package_identifier = properties.Property(properties.String)

    @classmethod
    def construct(cls, package_info: dict):
        """Construct an RPM package-version vertex based on analyzer result entry."""
        return cls.from_properties(
            ecosystem='rpm',
            name=package_info['name'],
            version=package_info['version'],
            release=package_info.get('release'),
            epoch=package_info.get('epoch'),
            arch=package_info.get('arch'),
            src=package_info.get('src', False),
            package_identifier=package_info.get('package_identifier', package_info['name'])
        )


class PythonPackageVersion(PackageVersionBase):
    """Python package version vertex."""

    @classmethod
    def construct(cls, package_info):
        """Construct a Python package-version vertex based on analyzer result entry."""
        return cls.from_properties(
            ecosystem=package_info['ecosystem'],
            name=package_info['result']['name'],
            version=package_info['result']['version'],
        )


class RuntimeEnvironment(VertexBase):
    """Environment such as container image which consists of various packages."""

    image = properties.Property(properties.String)
    # TODO: capture hashes of layers

    analysis_datetime = properties.Property(properties.Integer)
    analysis_document_id = properties.Property(properties.String)
    analyzer = properties.Property(properties.String)
    analyzer_version = properties.Property(properties.String)

    @classmethod
    def from_document(cls, analysis_document: dict):
        return cls.from_properties(
            image=analysis_document['metadata']['arguments']['extract-image']['image'],
            analysis_datetime=datetime_str2timestamp(analysis_document['metadata']['datetime']),
            analysis_document_id=analysis_document['metadata']['hostname'],
            analyzer=analysis_document['metadata']['analyzer'],
            analyzer_version=analysis_document['metadata']['analyzer_version']
        )


class SoftwareStack(VertexBase):
    """Observations we have about the given stack."""

    # TODO: add observation info

    analysis_document_id = properties.Property(properties.String)
    analysis_datetime = properties.Property(properties.Integer)
    analyzer = properties.Property(properties.String)
    analyzer_version = properties.Property(properties.String)

    @classmethod
    def from_document(cls, analysis_document: dict):
        return cls.from_properties(
            analysis_datetime=datetime_str2timestamp(analysis_document['metadata']['datetime']),
            analysis_document_id=analysis_document['metadata']['hostname'],
            analyzer=analysis_document['metadata']['analyzer'],
            analyzer_version=analysis_document['metadata']['analyzer_version']
        )


class DependsOn(EdgeBase):
    """Dependency between packages modeling based on ecosystem specification."""

    version_range = properties.Property(properties.String, default='*')
    package_name = properties.Property(properties.String)
    extras = properties.Property(properties.String)


class IsPartOf(EdgeBase):
    """Connection to environment."""


class IsSolvedBy(EdgeBase):
    """Connection whether the given package is installable into environment."""

    solver_document_id = properties.Property(properties.String)
    solver = properties.Property(properties.String)
    solver_version = properties.Property(properties.String)
    solver_datetime = properties.Property(properties.Integer)

    installable = properties.Property(properties.Boolean)

    @classmethod
    def from_document(cls, solver_document: dict):
        return cls.from_properties(
            solver_datetime=datetime_str2timestamp(solver_document['metadata']['datetime']),
            solver_document_id=solver_document['metadata']['hostname'],
            solver=solver_document['metadata']['analyzer'],
            solver_version=solver_document['metadata']['analyzer_version']
        )


class Requires(EdgeBase):
    """Requirement edge of an RPM package."""

    analysis_document_id = properties.Property(properties.String)
    analysis_datetime = properties.Property(properties.Integer)
    analyzer = properties.Property(properties.String)
    analyzer_version = properties.Property(properties.String)

    @classmethod
    def from_document(cls, source, target, analysis_document):
        return cls.from_properties(
            source=source,
            target=target,
            analysis_datetime=datetime_str2timestamp(analysis_document['metadata']['datetime']),
            analysis_document_id=analysis_document['metadata']['hostname'],
            analyzer=analysis_document['metadata']['analyzer'],
            analyzer_version=analysis_document['metadata']['analyzer_version']
        )


class CreatesStack(EdgeBase):
    """The given set of packages create a stack."""


class HasVersion(EdgeBase):
    """The given package has a specific version."""


ALL_MODELS = frozenset((
    CreatesStack,
    DependsOn,
    HasVersion,
    IsPartOf,
    IsSolvedBy,
    Package,
    PythonPackageVersion,
    Requires,
    RPMPackageVersion,
    RPMRequirement,
    RuntimeEnvironment,
    SoftwareStack,
))

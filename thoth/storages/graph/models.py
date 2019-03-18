#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2018, 2019 Fridolin Pokorny
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
    index_url = VertexProperty(properties.String)


class RPMPackageVersion(PackageVersionBase):
    """RPM-specific package version."""

    release = VertexProperty(properties.String)
    epoch = VertexProperty(properties.String)
    arch = VertexProperty(properties.String)
    src = VertexProperty(properties.Boolean)
    package_identifier = VertexProperty(properties.String)


class DebPackageVersion(PackageVersionBase):
    """Debian-specific package version."""

    epoch = VertexProperty(properties.String)
    arch = VertexProperty(properties.String)


class CVE(VertexBase):
    """Information about a CVE."""

    advisory = VertexProperty(properties.String)
    cve_name = VertexProperty(properties.String, default='-')
    cve_id = VertexProperty(properties.String)
    version_range = VertexProperty(properties.String)


class PythonPackageIndex(VertexBase):
    """Representation of a Python package Index.

    Fields are compatible with Thoth's Source class (the implicit ones are omitted).
    """

    url = VertexProperty(properties.String)
    warehouse_api_url = VertexProperty(properties.String, default=None)
    verify_ssl = VertexProperty(properties.Boolean, default=True)


class PythonPackageVersion(PackageVersionBase):
    """Python package version vertex."""


class PythonArtifact(VertexBase):
    """A Python artifact as placed on a source package index."""

    # artifact_name = VertexProperty(properties.String)
    artifact_hash_sha256 = VertexProperty(properties.String)


class EnvironmentBase(VertexBase):
    """A base class for environment types."""

    environment_name = VertexProperty(properties.String)
    python_version = VertexProperty(properties.String, default=None)

    # TODO: capture hashes of layers to be precise?


class RuntimeEnvironment(EnvironmentBase):
    """Environment such as container image which consists of various packages."""

    os_name = VertexProperty(properties.String, default=None)
    os_version = VertexProperty(properties.String, default=None)
    python_version = VertexProperty(properties.String, default=None)
    cuda_version = VertexProperty(properties.String, default=None)


class BuildtimeEnvironment(EnvironmentBase):
    """Environment such as container image which consists of various packages."""


class SoftwareStackBase(VertexBase):
    """A software stack crated by packages in specific versions.

    This is just a base class for creating software stack instances inside graph database.
    See specific software stack types for specific software stacks we are interested in.
    """

    # If a user stack, document id points to adviser document that introduced the stack.
    # If an adviser stack, document_id points to adviser document that introduced the stack.
    # If an inspection stack, document_id points to inspection document that introduced the stack.

    document_id = VertexProperty(properties.String)


class AdviserSoftwareStack(SoftwareStackBase):
    """A software stack as produced by adviser (the output of recommendation engine)."""

    # As adviser can output multiple stacks, this property states the index in
    # the resulting adviser document if is_adviser stack is set to True.

    adviser_stack_index = VertexProperty(properties.Integer, default=None)


class UserSoftwareStack(SoftwareStackBase):
    """A software stack as used by a user (input for the recommendation engine)."""

    # Origin of the software stack.
    origin = VertexProperty(properties.String, default=None)
    # Holds True/False if there was an error during advises in adviser.
    # Holds None if user stack came from provenance-checks.
    adviser_error = VertexProperty(properties.Boolean, default=None)


class InspectionSoftwareStack(SoftwareStackBase):
    """A software stack which was used on Amun during inspection runs (e.g. as produced by dependency-monkey)."""


class Advised(EdgeBase):
    """A relationship between user software stack and the advised software stack by Thoth's adviser."""

    adviser_version = Property(properties.String)
    adviser_document_id = Property(properties.String)
    adviser_datetime = Property(properties.Integer)
    recommendation_type = Property(properties.String)


class SoftwareStackObservation(VertexBase):
    """Observations we have about the given stack based on run on a specific hardware."""

    performance_index = VertexProperty(properties.Float)
    inspection_document_id = VertexProperty(properties.String, db_name="document_id")


class BuildObservation(VertexBase):
    """Observations we have about the given stack on runtime on some specific hardware."""

    inspection_document_id = VertexProperty(properties.String, db_name="document_id")


class HardwareInformation(VertexBase):
    """Hardware specification and propertires."""

    # cpu_vendor = VertexProperty(properties.String)
    cpu_model_name = VertexProperty(properties.String)
    cpu_model = VertexProperty(properties.Integer)
    cpu_family = VertexProperty(properties.Integer)
    cpu_cores = VertexProperty(properties.Integer)
    cpu_physical_cpus = VertexProperty(properties.Integer)

    # TODO: provide once we will have them available from Amun.
    # gpu_vendor = VertexProperty(properties.String)
    # gpu_model_name = VertexProperty(properties.String)
    # gpu_cores = VertexProperty(properties.Integer)
    # gpu_memory_size = VertexProperty(properties.Integer)

    # We use float here as using Integer can lead to serialization/deserialization
    # issues on Graph database side. JanusGraph treats Integer in fixed size of int32.
    ram_size = VertexProperty(properties.Float)


class EcosystemSolver(VertexBase):
    """Solver used to resolve dependencies within ecosystem."""

    solver_name = VertexProperty(properties.String)
    solver_version = VertexProperty(properties.String)

    # These properties could be derived from solver name, but make them properties so that they are queryable.
    os_name = VertexProperty(properties.String)
    os_version = VertexProperty(properties.String)
    python_version = VertexProperty(properties.String)


class DependsOn(EdgeBase):
    """Dependency between packages modeling based on ecosystem specification."""

    version_range = Property(properties.String, default="*")
    package_name = Property(properties.String)
    extras = Property(properties.String)

    os_name = Property(properties.String)
    os_version = Property(properties.String)
    python_version = Property(properties.String)
    solver_error = Property(properties.Boolean, default=False)


class Observed(EdgeBase):
    """Information about observations gathered on run."""

    inspection_document_id = Property(properties.String)


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
    # A flag signalizing any issues in solver.
    # If no other error flag is set, it signalizes issues during installation of the given
    # package in the given version (e.g. no native dependency that is needed,
    # issues with setup.py,, ...).
    solver_error = Property(properties.Boolean, default=False)
    # Issues when solving the given package (e.g. the given package does not
    # exist or the given version does not exist.)
    # This flag is an addition to solver_error, meaning if solver_error_unsolvable is
    # set to True, solver_error is True as well. But NOT vice versa.
    # This behaviour is to simplify queries during recommendations.
    solver_error_unsolvable = Property(properties.Boolean, default=False)
    # Issues when parsing package names (package name does not conform to PEP - e.g. spaces in name).
    # This flag is an addition to solver_error, meaning if solver_error_unparsable is
    # set to True, solver_error is True as well. But NOT vice versa.
    # This behaviour is to simplify queries during recommendations.
    solver_error_unparsable = Property(properties.Boolean, default=False)

    # Properties derived from solver name, used in queries to gather platform specific features.
    os_name = Property(properties.String)
    os_version = Property(properties.String)
    python_version = Property(properties.String)


class PackageExtractNativeBase(EdgeBase):
    """An edge that was captured when analyzing native dependencies (RPM or Debian-based)."""

    analysis_document_id = Property(properties.String)
    analysis_datetime = Property(properties.Integer)
    analyzer_name = Property(properties.String)
    analyzer_version = Property(properties.String)


class CreatesStack(EdgeBase):
    """The given set of packages create a stack."""


class HasArtifact(EdgeBase):
    """The given package has the given artifact."""


class HasVersion(EdgeBase):
    """The given package has a specific version."""


class RunsIn(EdgeBase):
    """The given software stack runs in a runtime environment."""

    document_id = Property(properties.String)
    run_error = Property(properties.Boolean, default=None)
    performance_index = Property(properties.Float, default=None)


class RunsOn(EdgeBase):
    """The given software stack runs on the given hardware."""

    document_id = Property(properties.String)
    run_error = Property(properties.Boolean, default=None)
    performance_index = Property(properties.Float, default=None)


class BuildsIn(EdgeBase):
    """The given software stack builds in a build environment."""

    document_id = Property(properties.String)
    build_error = Property(properties.Boolean)


class BuildsOn(EdgeBase):
    """The given software stack builds on the given hardware."""

    document_id = Property(properties.String)
    build_error = Property(properties.Boolean)


class HasVulnerability(EdgeBase):
    """The given package version has a vulnerability."""


class Requires(PackageExtractNativeBase):
    """Requirement edge of an RPM package."""


class DebDepends(PackageExtractNativeBase):
    """Depending edge of a deb package."""

    version_range = Property(properties.String, default="*")


class DebPreDepends(PackageExtractNativeBase):
    """Pre-depending edge of a deb package."""

    version_range = Property(properties.String, default="*")


class DebReplaces(PackageExtractNativeBase):
    """An edge of a deb package capturing package replacement.."""

    version_range = Property(properties.String, default="*")


ALL_MODELS = frozenset(
    (
        BuildsIn,
        BuildsOn,
        BuildtimeEnvironment,
        BuildObservation,
        CreatesStack,
        CVE,
        DebDepends,
        DebPackageVersion,
        DebPreDepends,
        DebReplaces,
        DependsOn,
        EcosystemSolver,
        HasArtifact,
        HasVersion,
        HasVulnerability,
        IsPartOf,
        Package,
        PythonArtifact,
        PythonPackageIndex,
        PythonPackageVersion,
        Requires,
        RPMPackageVersion,
        RPMRequirement,
        RunsIn,
        RunsOn,
        RuntimeEnvironment,
        AdviserSoftwareStack,
        UserSoftwareStack,
        InspectionSoftwareStack,
        Solved,
        Observed,
        HardwareInformation,
        SoftwareStackObservation,
    )
)

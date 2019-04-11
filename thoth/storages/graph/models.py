#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2019 Fridolin Pokorny
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


from datetime import datetime

import attr

from .models_base import VertexBase
from .models_base import ReverseEdgeBase
from .models_base import model_property


@attr.s(slots=True)
class Package(VertexBase):
    """Package vertex in the graph representing a package without version."""

    ecosystem = model_property(type=str, index="exact")
    package_name = model_property(type=str, index="exact")


@attr.s(slots=True)
class RPMRequirement(VertexBase):
    """Requirement of an RPM as stated in a spec file."""

    ELEMENT_NAME = "rpm_requirement"

    rpm_requirement_name = model_property(type=str, index="exact")


@attr.s(slots=True)
class PackageVersionBase(VertexBase):
    """Package-version vertex in the graph representing any versioned package."""

    ecosystem = model_property(type=str, index="exact")
    package_name = model_property(type=str, index="exact")
    package_version = model_property(type=str, index="exact")
    index_url = model_property(type=str, index="exact")


@attr.s(slots=True)
class RPMPackageVersion(PackageVersionBase):
    """RPM-specific package version."""

    ELEMENT_NAME = "rpm_package_version"

    release = model_property(type=str, index="exact")
    epoch = model_property(type=str, index="exact")
    arch = model_property(type=str, index="exact")
    src = model_property(type=bool)
    package_identifier = model_property(type=str, index="exact")


@attr.s(slots=True)
class DebPackageVersion(PackageVersionBase):
    """Debian-specific package version."""

    epoch = model_property(type=str, index="exact")
    arch = model_property(type=str, index="exact")


@attr.s(slots=True)
class CVE(VertexBase):
    """Information about a CVE."""

    ELEMENT_NAME = "cve"

    advisory = model_property(type=str, index="exact")
    cve_name = model_property(type=str, index="exact", default='-')
    cve_id = model_property(type=str, index="exact")
    version_range = model_property(type=str, index="exact")


@attr.s(slots=True)
class PythonPackageIndex(VertexBase):
    """Representation of a Python package Index.

    Fields are compatible with Thoth's Source class (the implicit ones are omitted).
    """

    url = model_property(type=str, index="exact")
    warehouse_api_url = model_property(type=str, index="exact", default=None)
    verify_ssl = model_property(type=bool, default=True)


@attr.s(slots=True)
class PythonPackageVersion(PackageVersionBase):
    """Python package version vertex."""


@attr.s(slots=True)
class PythonArtifact(VertexBase):
    """A Python artifact as placed on a source package index."""

    # artifact_name = model_property(type=str, index="exact")
    artifact_hash_sha256 = model_property(type=str, index="exact")


@attr.s(slots=True)
class EnvironmentBase(VertexBase):
    """A base class for environment types."""

    environment_name = model_property(type=str, index="exact")
    python_version = model_property(type=str, index="exact", default=None)

    # TODO: capture hashes of layers to be precise?


@attr.s(slots=True)
class RuntimeEnvironment(EnvironmentBase):
    """Environment such as container image which consists of various packages."""

    os_name = model_property(type=str, index="exact", default=None)
    os_version = model_property(type=str, index="exact", default=None)
    python_version = model_property(type=str, index="exact", default=None)
    cuda_version = model_property(type=str, index="exact", default=None)


@attr.s(slots=True)
class BuildtimeEnvironment(EnvironmentBase):
    """Environment such as container image which consists of various packages."""


@attr.s(slots=True)
class SoftwareStackBase(VertexBase):
    """A software stack crated by packages in specific versions.

    This is just a base class for creating software stack instances inside graph database.
    See specific software stack types for specific software stacks we are interested in.
    """

    # If a user stack, document id points to adviser document that introduced the stack.
    # If an adviser stack, document_id points to adviser document that introduced the stack.
    # If an inspection stack, document_id points to inspection document that introduced the stack.

    document_id = model_property(type=str, index="exact")


@attr.s(slots=True)
class AdviserSoftwareStack(SoftwareStackBase):
    """A software stack as produced by adviser (the output of recommendation engine)."""

    # As adviser can output multiple stacks, this property states the index in
    # the resulting adviser document if is_adviser stack is set to True.

    adviser_stack_index = model_property(type=int, default=None)


@attr.s(slots=True)
class UserSoftwareStack(SoftwareStackBase):
    """A software stack as used by a user (input for the recommendation engine)."""

    # Origin of the software stack.
    origin = model_property(type=str, index="exact", default=None)
    # Holds True/False if there was an error during advises in adviser.
    # Holds None if user stack came from provenance-checks.
    adviser_error = model_property(type=bool, default=None)


@attr.s(slots=True)
class InspectionSoftwareStack(SoftwareStackBase):
    """A software stack which was used on Amun during inspection runs (e.g. as produced by dependency-monkey)."""


@attr.s(slots=True)
class Advised(ReverseEdgeBase):
    """A relationship between user software stack and the advised software stack by Thoth's adviser."""

    adviser_version = model_property(type=str, index="exact")
    adviser_document_id = model_property(type=str, index="exact")
    adviser_datetime = model_property(type=datetime, index="hour")
    recommendation_type = model_property(type=str, index="exact")


@attr.s(slots=True)
class SoftwareStackObservation(VertexBase):
    """Observations we have about the given stack based on run on a specific hardware."""

    performance_index = model_property(type=float)
    inspection_document_id = model_property(type=str, index="exact")


@attr.s(slots=True)
class BuildObservation(VertexBase):
    """Observations we have about the given stack on runtime on some specific hardware."""

    inspection_document_id = model_property(type=str, index="exact")


@attr.s(slots=True)
class HardwareInformation(VertexBase):
    """Hardware specification and properties."""

    # cpu_vendor = model_property(type=str, index="exact")
    cpu_model_name = model_property(type=str, index="exact")
    cpu_model = model_property(type=int)
    cpu_family = model_property(type=int)
    cpu_cores = model_property(type=int)
    cpu_physical_cpus = model_property(type=int)

    # TODO: provide once we will have them available from Amun.
    # gpu_vendor = model_property(type=str, index="exact")
    # gpu_model_name = model_property(type=str, index="exact")
    # gpu_cores = model_property(type=int)
    # gpu_memory_size = model_property(type=int)

    # We use float here as using Integer can lead to serialization/deserialization
    # issues on Graph database side. JanusGraph treats Integer in fixed size of int32.
    ram_size = model_property(type=float)


@attr.s(slots=True)
class EcosystemSolver(VertexBase):
    """Solver used to resolve dependencies within ecosystem."""

    solver_name = model_property(type=str, index="exact")
    solver_version = model_property(type=str, index="exact")

    # These properties could be derived from solver name, but make them properties so that they are queryable.
    os_name = model_property(type=str, index="exact")
    os_version = model_property(type=str, index="exact")
    python_version = model_property(type=str, index="exact")


@attr.s(slots=True)
class DependsOn(ReverseEdgeBase):
    """Dependency between packages modeling based on ecosystem specification."""

    version_range = model_property(type=str, index="exact", default="*")
    package_name = model_property(type=str, index="exact")

    os_name = model_property(type=str, index="exact")
    os_version = model_property(type=str, index="exact")
    python_version = model_property(type=str, index="exact")
    solver_error = model_property(type=bool, default=False)


@attr.s(slots=True)
class Observed(ReverseEdgeBase):
    """Information about observations gathered on run."""

    inspection_document_id = model_property(type=str, index="exact")


@attr.s(slots=True)
class IsPartOf(ReverseEdgeBase):
    """Connection to environment."""

    analysis_datetime = model_property(type=datetime)
    analysis_document_id = model_property(type=str, index="exact")
    analyzer_name = model_property(type=str, index="exact")
    analyzer_version = model_property(type=str, index="exact")


@attr.s(slots=True)
class Solved(ReverseEdgeBase):
    """Stores information about which EcosystemSolver solved/introduced package."""

    solver_document_id = model_property(type=str, index="exact")
    solver_datetime = model_property(type=datetime)
    # A flag signalizing any issues in solver.
    # If no other error flag is set, it signalizes issues during installation of the given
    # package in the given version (e.g. no native dependency that is needed,
    # issues with setup.py,, ...).
    solver_error = model_property(type=bool, default=False)
    # Issues when solving the given package (e.g. the given package does not
    # exist or the given version does not exist.)
    # This flag is an addition to solver_error, meaning if solver_error_unsolvable is
    # set to True, solver_error is True as well. But NOT vice versa.
    # This behaviour is to simplify queries during recommendations.
    solver_error_unsolvable = model_property(type=bool, default=False)
    # Issues when parsing package names (package name does not conform to PEP - e.g. spaces in name).
    # This flag is an addition to solver_error, meaning if solver_error_unparsable is
    # set to True, solver_error is True as well. But NOT vice versa.
    # This behaviour is to simplify queries during recommendations.
    solver_error_unparsable = model_property(type=bool, default=False)

    # Properties derived from solver name, used in queries to gather platform specific features.
    os_name = model_property(type=str, index="exact")
    os_version = model_property(type=str, index="exact")
    python_version = model_property(type=str, index="exact")


@attr.s(slots=True)
class PackageExtractNativeBase(ReverseEdgeBase):
    """An edge that was captured when analyzing native dependencies (RPM or Debian-based)."""

    analysis_document_id = model_property(type=str, index="exact")
    analysis_datetime = model_property(type=datetime)
    analyzer_name = model_property(type=str, index="exact")
    analyzer_version = model_property(type=str, index="exact")


@attr.s(slots=True)
class CreatesStack(ReverseEdgeBase):
    """The given set of packages create a stack."""


@attr.s(slots=True)
class HasArtifact(ReverseEdgeBase):
    """The given package has the given artifact."""


@attr.s(slots=True)
class HasVersion(ReverseEdgeBase):
    """The given package has a specific version."""


@attr.s(slots=True)
class RunsIn(ReverseEdgeBase):
    """The given software stack runs in a runtime environment."""

    document_id = model_property(type=str, index="exact")
    run_error = model_property(type=bool, default=None)
    performance_index = model_property(type=float, default=None)


@attr.s(slots=True)
class RunsOn(ReverseEdgeBase):
    """The given software stack runs on the given hardware."""

    document_id = model_property(type=str, index="exact")
    run_error = model_property(type=bool, default=None)
    performance_index = model_property(type=float, default=None)


@attr.s(slots=True)
class BuildsIn(ReverseEdgeBase):
    """The given software stack builds in a build environment."""

    document_id = model_property(type=str, index="exact")
    build_error = model_property(type=bool)


@attr.s(slots=True)
class BuildsOn(ReverseEdgeBase):
    """The given software stack builds on the given hardware."""

    document_id = model_property(type=str, index="exact")
    build_error = model_property(type=bool)


@attr.s(slots=True)
class HasVulnerability(ReverseEdgeBase):
    """The given package version has a vulnerability."""


@attr.s(slots=True)
class Requires(PackageExtractNativeBase):
    """Requirement edge of an RPM package."""


@attr.s(slots=True)
class DebDepends(PackageExtractNativeBase):
    """Depending edge of a deb package."""

    version_range = model_property(type=str, index="exact", default="*")


@attr.s(slots=True)
class DebPreDepends(PackageExtractNativeBase):
    """Pre-depending edge of a deb package."""

    version_range = model_property(type=str, index="exact", default="*")


@attr.s(slots=True)
class DebReplaces(PackageExtractNativeBase):
    """An edge of a deb package capturing package replacement.."""

    version_range = model_property(type=str, index="exact", default="*")


class HasIndex(EdgeBase):
    """The given package version has an index."""


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
        HasIndex,
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

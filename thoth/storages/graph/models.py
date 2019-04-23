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


################################################################################
#                         Workload representatives.
################################################################################


@attr.s(slots=True)
class PackageExtractRun(VertexBase):
    """A class representing a single package-extract (image analysis) run."""

    analysis_document_id = model_property(type=str, index="exact")
    analysis_datetime = model_property(type=datetime, index="hour")
    package_extract_version = model_property(type=str, index="exact")
    package_extract_name = model_property(type=str, index="exact")
    environment_type = model_property(type=str, index="exact")
    origin = model_property(type=str, index="exact")
    debug = model_property(type=bool)
    package_extract_error = model_property(type=bool)
    # An image tag which was used during image analysis. As this tag can change (e.g. latest is always changing
    # on new builds), it's part of this class instead of Runtime/Buildtime environment to keep correct
    # linkage for same container images.
    image_tag = model_property(type=str, index="exact")
    # Duration in seconds.
    duration = model_property(type=int)


@attr.s(slots=True)
class Identified(ReverseEdgeBase):
    """An edge representing a package identified by a package-extract run."""


@attr.s(slots=True)
class AnalyzedBy(ReverseEdgeBase):
    """An edge representing an image analysis."""


@attr.s(slots=True)
class InspectionRun(VertexBase):
    """A class representing a single inspection run."""

    inspection_document_id = model_property(type=str, index="exact")
    inspection_datetime = model_property(type=datetime, index="hour")
    amun_version = model_property(type=str, index="exact")
    build_requests_cpu = model_property(type=float)
    build_requests_memory = model_property(type=float)
    run_requests_cpu = model_property(type=float)
    run_requests_memory = model_property(type=float)


@attr.s(slots=True)
class EcosystemSolverRun(VertexBase):
    """A class representing a single solver run."""

    ecosystem = model_property(type=str, index="exact")
    solver_document_id = model_property(type=str, index="exact")
    solver_datetime = model_property(type=datetime, index="hour")
    solver_name = model_property(type=str, index="exact")
    solver_version = model_property(type=str, index="exact")
    os_name = model_property(type=str, index="exact")
    os_version = model_property(type=str, index="exact")
    python_version = model_property(type=str, index="exact")
    # Duration in seconds.
    duration = model_property(type=int)


@attr.s(slots=True)
class Solved(ReverseEdgeBase):
    """The given ecosystem solver solved a stack."""


@attr.s(slots=True)
class DependencyMonkeyRun(VertexBase):
    """A class representing a single dependency-monkey run."""

    dependency_monkey_document_id = model_property(type=str, index="exact")
    dependency_monkey_datetime = model_property(type=datetime, index="hour")
    dependency_monkey_name = model_property(type=str, index="exact")
    dependency_monkey_version = model_property(type=str, index="exact")
    seed = model_property(type=int)
    decision = model_property(type=str, index="exact")
    count = model_property(type=int)
    limit_latest_versions = model_property(type=bool)
    debug = model_property(type=bool)
    dependency_monkey_error = model_property(type=bool)
    # Duration in seconds.
    duration = model_property(type=int)


@attr.s(slots=True)
class DependencyMonkeyEnvironmentInput(ReverseEdgeBase):
    """A class representing runtime environment used during stack resolution on a dependency monkey run."""


@attr.s(slots=True)
class Resolved(ReverseEdgeBase):
    """The given dependency monkey run resolved an inspection software stack which was sent to inspection run."""


@attr.s(slots=True)
class AdviserRun(VertexBase):
    """A class representing a single adviser run."""

    adviser_document_id = model_property(type=str, index="exact")
    adviser_datetime = model_property(type=datetime, index="hour")
    adviser_version = model_property(type=str, index="exact")
    adviser_name = model_property(type=str, index="exact")
    count = model_property(type=int)
    limit = model_property(type=int)
    origin = model_property(type=str, index="exact")
    debug = model_property(type=bool)
    limit_latest_versions = model_property(type=int)
    adviser_error = model_property(type=bool)
    recommendation_type = model_property(type=str, index="exact")
    requirements_format = model_property(type=str, index="exact")
    # Duration in seconds.
    duration = model_property(type=int)
    advised_configuration_changes = model_property(type=bool)
    additional_stack_info = model_property(type=bool)


@attr.s(slots=True)
class ProvenanceCheckerRun(VertexBase):
    """A class representing a single provenance-checker run."""

    provenance_checker_document_id = model_property(type=str, index="exact")
    provenance_checker_datetime = model_property(type=datetime, index="hour")
    provenance_checker_version = model_property(type=str, index="exact")
    provenance_checker_name = model_property(type=str, index="exact")
    origin = model_property(type=str, index="exact")
    debug = model_property(type=bool)
    provenance_checker_error = model_property(type=bool)
    # Duration in seconds.
    duration = model_property(type=int)


@attr.s(slots=True)
class ProvenanceCheckerStackInput(ReverseEdgeBase):
    """A stack input to a provenance checker run."""


################################################################################
#                             Packages.
################################################################################


@attr.s(slots=True)
class RPMPackageVersion(VertexBase):
    """RPM-specific package version."""

    ELEMENT_NAME = "rpm_package_version"

    ecosystem = model_property(type=str, index="exact")
    package_name = model_property(type=str, index="exact")
    package_version = model_property(type=str, index="exact")
    release = model_property(type=str, index="exact")
    epoch = model_property(type=str, index="exact")
    arch = model_property(type=str, index="exact")
    src = model_property(type=bool)
    package_identifier = model_property(type=str, index="exact")


@attr.s(slots=True)
class Requires(ReverseEdgeBase):
    """Requirement edge of an RPM package."""


@attr.s(slots=True)
class RPMRequirement(VertexBase):
    """Requirement of an RPM as stated in a spec file."""

    ELEMENT_NAME = "rpm_requirement"

    rpm_requirement_name = model_property(type=str, index="exact")


@attr.s(slots=True)
class DebPackageVersion(VertexBase):
    """Debian-specific package version."""

    ecosystem = model_property(type=str, index="exact")
    package_name = model_property(type=str, index="exact")
    package_version = model_property(type=str, index="exact")
    epoch = model_property(type=str, index="exact")
    arch = model_property(type=str, index="exact")


@attr.s(slots=True)
class DebDepends(ReverseEdgeBase):
    """Depending edge of a deb package."""

    version_range = model_property(type=str, index="exact", default="*")


@attr.s(slots=True)
class DebPreDepends(ReverseEdgeBase):
    """Pre-depending edge of a deb package."""

    version_range = model_property(type=str, index="exact", default="*")


@attr.s(slots=True)
class DebReplaces(ReverseEdgeBase):
    """An edge of a deb package capturing package replacement.."""

    version_range = model_property(type=str, index="exact", default="*")


@attr.s(slots=True)
class DebDependency(VertexBase):
    """A Debian dependency."""

    ecosystem = model_property(type=str, index="exact")
    package_name = model_property(type=str, index="exact")


@attr.s(slots=True)
class PythonPackageVersionEntity(VertexBase):
    """A representative for a Python package version vertex without being installed."""

    ecosystem = model_property(type=str, index="exact")
    package_name = model_property(type=str, index="exact")
    package_version = model_property(type=str, index="exact")
    index_url = model_property(type=str, index="exact")


@attr.s(slots=True)
class PythonPackageVersion(VertexBase):
    """Python package version vertex."""

    ecosystem = model_property(type=str, index="exact")
    package_name = model_property(type=str, index="exact")
    package_version = model_property(type=str, index="exact")
    index_url = model_property(type=str, index="exact")
    extras = model_property(type=str, index="exact")
    os_name = model_property(type=str, index="exact")
    os_version = model_property(type=str, index="exact")
    python_version = model_property(type=str, index="exact")
    solver_error = model_property(type=bool, index="bool")
    solver_error_unparseable = model_property(type=bool, index="bool")
    solver_error_unsolvable = model_property(type=bool, index="bool")


@attr.s(slots=True)
class DependsOn(ReverseEdgeBase):
    """Dependency between packages modeling based on ecosystem specification."""

    version_range = model_property(type=str)


@attr.s(slots=True)
class PythonPackageRequirement(VertexBase):
    """Python package requirement vertex."""

    ecosystem = model_property(type=str, index="exact")
    package_name = model_property(type=str, index="exact")
    version_range = model_property(type=str, index="exact")
    develop = model_property(type=bool)
    index_url = model_property(type=str, index="exact")
    extras = model_property(type=str, index="exact")
    markers = model_property(type=str)


@attr.s(slots=True)
class RequirementsInput(ReverseEdgeBase):
    """Requirement input - Python package requirements."""


@attr.s(slots=True)
class HasArtifact(ReverseEdgeBase):
    """The given package has the given artifact."""


@attr.s(slots=True)
class PythonArtifact(VertexBase):
    """An artifact for a python package in a specific version."""

    artifact_hash_sha256 = model_property(type=str, index="exact")
    artifact_name = model_property(type=str, index="exact")
    # TODO: parse wheel specific tags to make them queryable?


@attr.s(slots=True)
class CreatesStack(ReverseEdgeBase):
    """The given set of packages create a stack."""


@attr.s(slots=True)
class ProvidedBy(ReverseEdgeBase):
    """The given PythonPackageVersion is provided by a Python index."""


@attr.s(slots=True)
class InstalledFrom(ReverseEdgeBase):
    """The given PythonPackageVersion installed from the given Python entity."""


@attr.s(slots=True)
class PythonPackageIndex(VertexBase):
    """Representation of a Python package Index."""

    url = model_property(type=str, index="exact")
    warehouse_api_url = model_property(type=str, index="exact")
    verify_ssl = model_property(type=bool)


################################################################################
#                          Environments and hardware.
################################################################################


@attr.s(slots=True)
class EnvironmentBase(VertexBase):
    """A base class for environment types."""

    environment_name = model_property(type=str, index="exact")
    python_version = model_property(type=str, index="exact", default=None)
    image_name = model_property(type=str, index="exact")
    image_sha = model_property(type=str, index="exact")
    os_name = model_property(type=str, index="exact", default=None)
    os_version = model_property(type=str, index="exact", default=None)


@attr.s(slots=True)
class BuildtimeEnvironment(EnvironmentBase):
    """Environment - container image which consists of various packages used during build."""


@attr.s(slots=True)
class InspectionBuildtimeEnvironmentInput(ReverseEdgeBase):
    """Buildtime environment in inspections."""


@attr.s(slots=True)
class RuntimeEnvironment(EnvironmentBase):
    """Environment - container image which consists of various packages used in a deployment."""

    cuda_version = model_property(type=str, index="exact", default=None)


@attr.s(slots=True)
class InspectionRuntimeEnvironmentInput(ReverseEdgeBase):
    """Runtime environment in inspections."""


@attr.s(slots=True)
class SoftwareStackBase(VertexBase):
    """A software stack crated by packages in specific versions.

    This is just a base class for creating software stack instances inside graph database.
    See specific software stack types for specific software stacks we are interested in.
    """


@attr.s(slots=True)
class Advised(ReverseEdgeBase):
    """A relation stating advised software stack in an adviser run."""


@attr.s(slots=True)
class AdviserStackInput(ReverseEdgeBase):
    """A relation stating user's software stack coming in to the recommendation engine."""


@attr.s(slots=True)
class AdviserRuntimeEnvironmentInput(ReverseEdgeBase):
    """A relation capturing runtime environment used in advises."""


@attr.s(slots=True)
class AdvisedSoftwareStack(SoftwareStackBase):
    """A software stack as produced by adviser (the output of recommendation engine)."""

    adviser_document_id = model_property(type=str, index="exact")
    # As adviser can output multiple stacks, this property states the index.
    advised_stack_index = model_property(type=int)
    performance_score = model_property(type=float)
    overall_score = model_property(type=float)


@attr.s(slots=True)
class UserSoftwareStack(SoftwareStackBase):
    """A software stack as used by a user (input for the recommendation engine)."""

    # Keeps adviser_document_id in case of advises, provenance_checker_document_id in case of provenance checks.
    document_id = model_property(type=str, index="exact")


@attr.s(slots=True)
class InspectionSoftwareStack(SoftwareStackBase):
    """A software stack which was used on Amun during inspection runs (e.g. as produced by dependency-monkey)."""

    inspection_document_id = model_property(type=str, index="exact")


@attr.s(slots=True)
class InspectionStackInput(ReverseEdgeBase):
    """An input stack for an inspection run."""


@attr.s(slots=True)
class HardwareInformation(VertexBase):
    """Hardware specification and properties."""

    cpu_vendor = model_property(type=str, index="exact")
    cpu_model = model_property(type=int)
    cpu_cores = model_property(type=int)
    cpu_model_name = model_property(type=str)
    cpu_family = model_property(type=int)
    cpu_physical_cpus = model_property(type=int)

    gpu_model_name = model_property(type=str, index="exact")
    gpu_vendor = model_property(type=str)
    gpu_cores = model_property(type=int)
    gpu_memory_size = model_property(type=float)

    ram_size = model_property(type=float)


@attr.s(slots=True)
class UsedIn(ReverseEdgeBase):
    """Information about hardware used when running/checking a stack."""


@attr.s(slots=True)
class UsedInBuild(ReverseEdgeBase):
    """Information about hardware used when building a stack on Amun."""


@attr.s(slots=True)
class UsedInJob(ReverseEdgeBase):
    """Information about hardware used when running a stack on Amun."""


################################################################################
#                             Performance indicators.
################################################################################


@attr.s(slots=True)
class ObservedPerformance(ReverseEdgeBase):
    """A class for representing connection to performance indicators."""

    performance_indicator_index = model_property(type=int)


@attr.s(slots=True)
class PerformanceIndicatorBase(VertexBase):
    """A base class for implementing performance indicators."""

    # Origin from where the performance indicator was obtained. In case of Git repo,
    # it holds Git repo URL, in case of URL it holds URL to the script.
    origin = model_property(type=str, index="exact")
    # Reference of the script, in case of Git repo it holds commit SHA, in case of URL it caries
    # SHA256 of the script which was used to test the performance with (performance indicator script).
    reference = model_property(type=str, index="exact")
    # This one is used later on in queries in adviser, all the relevant performance indicators should
    # respect this property and place resutls in there.
    overall_score = model_property(type=float)


@attr.s(slots=True)
class PiMatmul(PerformanceIndicatorBase):
    """A class for representing a matrix multiplication micro-performance test."""

    matrix_size = model_property(type=int)


################################################################################
#                           Security.
################################################################################


@attr.s(slots=True)
class HasVulnerability(ReverseEdgeBase):
    """The given package version has a vulnerability."""


@attr.s(slots=True)
class CVE(VertexBase):
    """Information about a CVE."""

    ELEMENT_NAME = "cve"

    advisory = model_property(type=str, index="exact")
    cve_name = model_property(type=str, index="exact", default='-')
    cve_id = model_property(type=str, index="exact")
    version_range = model_property(type=str, index="exact")


ALL_MODELS = frozenset(
    (
        AdviserRun,
        AdvisedSoftwareStack,
        AdviserRuntimeEnvironmentInput,
        AdviserStackInput,
        Advised,
        AnalyzedBy,
        BuildtimeEnvironment,
        CreatesStack,
        CVE,
        DebDepends,
        DebPackageVersion,
        DebPreDepends,
        DebReplaces,
        DependencyMonkeyRun,
        DependencyMonkeyEnvironmentInput,
        DependsOn,
        EcosystemSolverRun,
        HardwareInformation,
        HasArtifact,
        HasVulnerability,
        Identified,
        InspectionBuildtimeEnvironmentInput,
        InspectionRun,
        InspectionRuntimeEnvironmentInput,
        InspectionStackInput,
        InspectionSoftwareStack,
        ObservedPerformance,
        PackageExtractRun,
        PiMatmul,
        ProvenanceCheckerRun,
        ProvenanceCheckerStackInput,
        ProvidedBy,
        PythonArtifact,
        PythonPackageIndex,
        PythonPackageRequirement,
        PythonPackageVersion,
        PythonPackageVersionEntity,
        Resolved,
        RequirementsInput,
        Requires,
        RPMPackageVersion,
        RPMRequirement,
        RuntimeEnvironment,
        Solved,
        InstalledFrom,
        UsedIn,
        UsedInBuild,
        UsedInJob,
        UserSoftwareStack,
    )
)

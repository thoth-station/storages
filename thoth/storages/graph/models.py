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

"""Graph database schema.

This module contains just "core" parts of the graph database schema. Other modules present in this package
capture standalone parts - see for example performance indicators.
"""


from datetime import datetime

import attr

from .models_base import model_property
from .models_base import ReverseEdgeBase
from .models_base import VertexBase
from .performance import ALL_PERFORMANCE_MODELS


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
    # Entries parsed from /etc/os-release
    os_name = model_property(type=str, index="exact")
    os_id = model_property(type=str, index="exact")
    os_version_id = model_property(type=str, index="exact")


@attr.s(slots=True)
class PackageAnalyzerRun(VertexBase):
    """A class representing a single package-analyzer (package analysis) run."""

    package_analysis_document_id = model_property(type=str, index="exact")
    package_analysis_datetime = model_property(type=datetime, index="hour")
    package_analyzer_version = model_property(type=str, index="exact")
    package_analyzer_name = model_property(type=str, index="exact")
    debug = model_property(type=bool)
    package_analyzer_error = model_property(type=bool, index="bool")
    duration = model_property(type=int)


@attr.s(slots=True)
class PythonFileDigest(VertexBase):
    """A class representing a single file digests."""

    sha256 = model_property(type=str, index="exact")


@attr.s(slots=True)
class FoundFile(ReverseEdgeBase):
    """An edge representing a filepath to the python file found in an image."""

    file_path = model_property(type=str, index="exact")


@attr.s(slots=True)
class PackageAnalyzerInput(ReverseEdgeBase):
    """An input python-package-version entity for a package analyzer run."""


@attr.s(slots=True)
class IncludedFile(ReverseEdgeBase):
    """An edge representing file found in the given artifact."""

    package_analysis_document_id = model_property(type=str, index="exact")


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
class DependencyMonkeyRunSoftwareEnvironmentInput(ReverseEdgeBase):
    """A class representing software environment for run used during stack resolution on a dependency monkey run."""


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
class Investigated(ReverseEdgeBase):
    """The given artifact is investigated by the package analyzer."""


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
class BuildSoftwareEnvironment(EnvironmentBase):
    """Software Environment for build - container image which consists of various packages used during build."""


@attr.s(slots=True)
class InspectionBuildSoftwareEnvironmentInput(ReverseEdgeBase):
    """Software environment for build in inspections."""


@attr.s(slots=True)
class RunSoftwareEnvironment(EnvironmentBase):
    """Software Environment for run - container image which consists of various packages used in a deployment."""

    cuda_version = model_property(type=str, index="exact", default=None)


@attr.s(slots=True)
class UserRunSoftwareEnvironment(RunSoftwareEnvironment):
    """Software Environment for run - container image which consists of various packages used in a deployment.

    As used by a user (input for the recommendation engine).
    """


@attr.s(slots=True)
class InspectionRunSoftwareEnvironmentInput(ReverseEdgeBase):
    """Software environment for run in inspections."""


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
class AdviserRunSoftwareEnvironmentInput(ReverseEdgeBase):
    """A relation capturing software environment for run used in advises."""


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
    cpu_model = model_property(type=int, index="int")
    cpu_cores = model_property(type=int, index="int")
    cpu_model_name = model_property(type=str, index="exact")
    cpu_family = model_property(type=int, index="int")
    cpu_physical_cpus = model_property(type=int, index="int")

    gpu_model_name = model_property(type=str, index="exact")
    gpu_vendor = model_property(type=str, index="exact")
    gpu_cores = model_property(type=int, index="int")
    gpu_memory_size = model_property(type=float, index="float")

    ram_size = model_property(type=float, index="float")


@attr.s(slots=True)
class UserHardwareInformation(HardwareInformation):
    """Hardware specification and properties as used by a user (input for the recommendation engine)."""


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
    cve_name = model_property(type=str, index="exact", default="-")
    cve_id = model_property(type=str, index="exact")
    version_range = model_property(type=str, index="exact")


ALL_CORE_MODELS = frozenset(
    (
        AdviserRun,
        AdvisedSoftwareStack,
        AdviserRunSoftwareEnvironmentInput,
        AdviserStackInput,
        Advised,
        AnalyzedBy,
        BuildSoftwareEnvironment,
        CreatesStack,
        CVE,
        DebDepends,
        DebPackageVersion,
        DebPreDepends,
        DebReplaces,
        DependencyMonkeyRun,
        DependencyMonkeyRunSoftwareEnvironmentInput,
        DependsOn,
        EcosystemSolverRun,
        HardwareInformation,
        HasArtifact,
        Investigated,
        HasVulnerability,
        Identified,
        InspectionBuildSoftwareEnvironmentInput,
        InspectionRun,
        InspectionRunSoftwareEnvironmentInput,
        InspectionStackInput,
        InspectionSoftwareStack,
        PackageExtractRun,
        PackageAnalyzerRun,
        PythonFileDigest,
        FoundFile,
        PackageAnalyzerInput,
        IncludedFile,
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
        RunSoftwareEnvironment,
        UserRunSoftwareEnvironment,
        Solved,
        InstalledFrom,
        UsedIn,
        UsedInBuild,
        UsedInJob,
        UserSoftwareStack,
        UserHardwareInformation,
    )
)


ALL_MODELS = ALL_CORE_MODELS | ALL_PERFORMANCE_MODELS

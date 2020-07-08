#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2019, 2020 Fridolin Pokorny
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

"""Models for SQL based database."""

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM

from sqlalchemy import UniqueConstraint
from sqlalchemy import Index

from .models_base import BaseExtension
from .models_base import Base
from .models_base import get_python_package_version_index_combinations

from .enums import EnvironmentTypeEnum
from .enums import SoftwareStackTypeEnum
from .enums import RecommendationTypeEnum
from .enums import RequirementsFormatEnum
from .enums import InspectionSyncStateEnum
from .enums import MetadataDistutilsTypeEnum
from .enums import ThothAdviserIntegrationEnum

# Environment type used in package-extract as a flag as well as in software environment records.
_ENVIRONMENT_TYPE_ENUM = ENUM(
    EnvironmentTypeEnum.RUNTIME.value, EnvironmentTypeEnum.BUILDTIME.value, name="environment_type", create_type=True
)


class PythonPackageVersion(Base, BaseExtension):
    """Representation of a Python package version running on a specific software environment."""

    __tablename__ = "python_package_version"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    package_name = Column(Text, nullable=False)
    package_version = Column(Text, nullable=True)
    # Only solved packages can be synced.
    os_name = Column(Text, nullable=False)
    os_version = Column(Text, nullable=False)
    python_version = Column(Text, nullable=False)
    entity_id = Column(Integer, ForeignKey("python_package_version_entity.id", ondelete="CASCADE"), nullable=False)
    # Null if package is unparseable.
    python_package_index_id = Column(Integer, ForeignKey("python_package_index.id", ondelete="CASCADE"), nullable=True)
    python_package_metadata_id = Column(
        Integer, ForeignKey("python_package_metadata.id", ondelete="CASCADE"), nullable=True
    )
    is_missing = Column(Boolean, nullable=False, default=False)

    dependencies = relationship("DependsOn", back_populates="version")
    solvers = relationship("Solved", back_populates="version")
    entity = relationship("PythonPackageVersionEntity", back_populates="python_package_versions")
    index = relationship("PythonPackageIndex", back_populates="python_package_versions")
    python_package_metadata = relationship("PythonPackageMetadata", back_populates="python_package_versions")

    python_software_stacks = relationship("PythonRequirementsLock", back_populates="python_package_version")

    __table_args__ = tuple(
        get_python_package_version_index_combinations()
        + [
            UniqueConstraint(
                "package_name", "package_version", "python_package_index_id", "os_name", "os_version", "python_version"
            ),
            Index("python_package_version_environment_idx", "os_name", "os_version", "python_version"),
        ]
    )


class HasArtifact(Base, BaseExtension):
    """The given package has the given artifact."""

    __tablename__ = "has_artifact"

    python_package_version_entity_id = Column(
        Integer, ForeignKey("python_package_version_entity.id", ondelete="CASCADE"), primary_key=True
    )
    python_artifact_id = Column(Integer, ForeignKey("python_artifact.id", ondelete="CASCADE"), primary_key=True)

    python_package_version_entity = relationship("PythonPackageVersionEntity", back_populates="python_artifacts")
    python_artifact = relationship("PythonArtifact", back_populates="python_package_version_entities")

    __table_args__ = (
        Index("has_artifact_python_package_version_entity_id", "python_package_version_entity_id"),
        Index("has_artifact_python_artifact_id", "python_artifact_id"),
    )


class Solved(Base, BaseExtension):
    """A solver solved a package-version."""

    __tablename__ = "solved"

    datetime = Column(DateTime(timezone=False), nullable=False)
    document_id = Column(Text, nullable=False)
    duration = Column(Integer, nullable=True)  # nullable for now...

    error = Column(Boolean, default=False, nullable=False)
    error_unparseable = Column(Boolean, default=False, nullable=False)
    error_unsolvable = Column(Boolean, default=False, nullable=False)
    is_provided = Column(Boolean)

    ecosystem_solver_id = Column(Integer, ForeignKey("ecosystem_solver.id", ondelete="CASCADE"), primary_key=True)
    version_id = Column(Integer, ForeignKey("python_package_version.id", ondelete="CASCADE"), primary_key=True)

    ecosystem_solver = relationship("EcosystemSolver", back_populates="versions")
    version = relationship("PythonPackageVersion", back_populates="solvers")

    __table_args__ = (Index("solver_document_id_idx", "document_id"), Index("solved_version_id_idx", "version_id"))


class PythonPackageVersionEntity(Base, BaseExtension):
    """Representation of a Python package not running in any environment."""

    __tablename__ = "python_package_version_entity"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)

    package_name = Column(Text, nullable=False)
    # Nullable if we cannot resolve.
    package_version = Column(Text, nullable=True)
    # Nullable if coming from user or cross-index resolution.
    python_package_index_id = Column(Integer, ForeignKey("python_package_index.id", ondelete="CASCADE"), nullable=True)

    versions = relationship("DependsOn", back_populates="entity")
    adviser_runs = relationship("HasUnresolved", back_populates="python_package_version_entity")
    package_extract_runs = relationship("Identified", back_populates="python_package_version_entity")
    si_aggregated_runs = relationship("SIAggregated", back_populates="python_package_version_entity")
    build_log_analyzer_runs = relationship("BuildLogAnalyzerRun", back_populates="input_python_package_version_entity")
    package_analyzer_runs = relationship("PackageAnalyzerRun", back_populates="input_python_package_version_entity")
    cves = relationship("HasVulnerability", back_populates="python_package_version_entity")
    # inspection_software_stacks = relationship("PythonSoftwareStack", back_populates="python_package_version_entity")
    # user_software_stacks = relationship("PythonSoftwareStack", back_populates="python_package_version_entity")
    index = relationship("PythonPackageIndex", back_populates="python_package_version_entities")
    python_package_versions = relationship("PythonPackageVersion", back_populates="entity")
    python_artifacts = relationship("HasArtifact", back_populates="python_package_version_entity")
    python_software_stacks = relationship(
        "ExternalPythonRequirementsLock", back_populates="python_package_version_entity"
    )

    __table_args__ = (
        UniqueConstraint("package_name", "package_version", "python_package_index_id"),
        Index(
            "python_package_version_entity_idx",
            "package_name",
            "package_version",
            "python_package_index_id",
            unique=True,
        ),
        Index("python_package_version_entity_id_idx", "id", unique=True),
        Index("python_package_version_entity_package_name_idx", "package_name"),
    )


class DependsOn(Base, BaseExtension):
    """Dependency of a Python package version."""

    __tablename__ = "depends_on"

    entity_id = Column(Integer, ForeignKey("python_package_version_entity.id", ondelete="CASCADE"), primary_key=True)
    version_id = Column(Integer, ForeignKey("python_package_version.id", ondelete="CASCADE"), primary_key=True)

    version_range = Column(Text)
    marker = Column(Text, nullable=True)
    extra = Column(Text, nullable=True)
    marker_evaluation_result = Column(Boolean, nullable=False)
    platform = Column(Text, nullable=False)

    entity = relationship("PythonPackageVersionEntity", back_populates="versions")
    version = relationship("PythonPackageVersion", back_populates="dependencies")

    __table_args__ = (
        Index("depends_on_version_id_idx", "version_id"),
        Index("depends_on_entity_id_idx", "entity_id"),
        Index("depends_on_platform", "platform"),
    )


class EcosystemSolver(Base, BaseExtension):
    """Record for an ecosystem solver."""

    __tablename__ = "ecosystem_solver"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ecosystem = Column(Text, nullable=False)
    solver_name = Column(Text, nullable=False)
    solver_version = Column(Text, nullable=False)
    os_name = Column(Text, nullable=False)
    os_version = Column(Text, nullable=False)
    python_version = Column(Text, nullable=False)

    versions = relationship("Solved", back_populates="ecosystem_solver")

    __table_args__ = (
        UniqueConstraint("ecosystem", "solver_name", "solver_version", "os_name", "os_version", "python_version"),
        Index(
            "ecosystem_solver_idx",
            "ecosystem",
            "solver_name",
            "solver_version",
            "os_name",
            "os_version",
            "python_version",
            unique=True,
        ),
    )


class PackageExtractRun(Base, BaseExtension):
    """A class representing a single package-extract (image analysis) run."""

    __tablename__ = "package_extract_run"

    id = Column(Integer, primary_key=True, autoincrement=True)

    package_extract_name = Column(Text, nullable=False)
    package_extract_version = Column(Text, nullable=False)
    analysis_document_id = Column(Text, nullable=False)
    datetime = Column(DateTime, nullable=False)
    environment_type = Column(_ENVIRONMENT_TYPE_ENUM, nullable=False)
    origin = Column(Text, nullable=True)
    debug = Column(Boolean, nullable=False, default=False)
    package_extract_error = Column(Boolean, nullable=False, default=False)
    image_size = Column(Integer, nullable=True)
    # An image tag which was used during image analysis. As this tag can change (e.g. latest is always changing
    # on new builds), it's part of this class instead of Runtime/Buildtime environment to keep correct
    # linkage for same container images.
    image_tag = Column(Text, nullable=False)
    # Duration in seconds.
    duration = Column(Integer, nullable=True)
    # Entries parsed from /etc/os-release
    os_name = Column(Text, nullable=False)
    os_id = Column(Text, nullable=False)
    os_version_id = Column(Text, nullable=False)
    software_environment_id = Column(Integer, ForeignKey("software_environment.id", ondelete="CASCADE"), nullable=True)

    external_software_environment_id = Column(
        Integer, ForeignKey("external_software_environment.id", ondelete="CASCADE"), nullable=True
    )

    found_python_files = relationship("FoundPythonFile", back_populates="package_extract_run")
    found_python_interpreters = relationship("FoundPythonInterpreter", back_populates="package_extract_run")
    found_rpms = relationship("FoundRPM", back_populates="package_extract_run")
    found_debs = relationship("FoundDeb", back_populates="package_extract_run")
    python_package_version_entities = relationship("Identified", back_populates="package_extract_run")
    software_environment = relationship("SoftwareEnvironment", back_populates="package_extract_runs")
    versioned_symbols = relationship("DetectedSymbol", back_populates="package_extract_run")

    external_software_environment = relationship(
        "ExternalSoftwareEnvironment", back_populates="external_package_extract_runs"
    )


class FoundPythonFile(Base, BaseExtension):
    """State a package extract run found a Python file."""

    __tablename__ = "found_python_file"

    file = Column(Text, nullable=False)

    python_file_digest_id = Column(Integer, ForeignKey("python_file_digest.id", ondelete="CASCADE"), primary_key=True)
    package_extract_run_id = Column(Integer, ForeignKey("package_extract_run.id", ondelete="CASCADE"), primary_key=True)

    python_file_digest = relationship("PythonFileDigest", back_populates="package_extract_runs")
    package_extract_run = relationship("PackageExtractRun", back_populates="found_python_files")


class PythonInterpreter(Base, BaseExtension):
    """A class representing a single python interpreter."""

    __tablename__ = "python_interpreter"

    id = Column(Integer, primary_key=True, autoincrement=True)

    path = Column(Text, nullable=False)
    link = Column(Text, nullable=True)
    version = Column(Text, nullable=True)

    package_extract_runs = relationship("FoundPythonInterpreter", back_populates="python_interpreter")


class FoundPythonInterpreter(Base, BaseExtension):
    """State a package extract run found a Python interpreter."""

    __tablename__ = "found_python_interpreter"

    python_interpreter_id = Column(Integer, ForeignKey("python_interpreter.id", ondelete="CASCADE"), primary_key=True)
    package_extract_run_id = Column(Integer, ForeignKey("package_extract_run.id", ondelete="CASCADE"), primary_key=True)

    python_interpreter = relationship("PythonInterpreter", back_populates="package_extract_runs")
    package_extract_run = relationship("PackageExtractRun", back_populates="found_python_interpreters")


class FoundRPM(Base, BaseExtension):
    """State a package extract run found an RPM package."""

    __tablename__ = "found_rpm"

    rpm_package_version_id = Column(Integer, ForeignKey("rpm_package_version.id", ondelete="CASCADE"), primary_key=True)
    package_extract_run_id = Column(Integer, ForeignKey("package_extract_run.id", ondelete="CASCADE"), primary_key=True)

    rpm_package_version = relationship("RPMPackageVersion", back_populates="package_extract_runs")
    package_extract_run = relationship("PackageExtractRun", back_populates="found_rpms")


class FoundDeb(Base, BaseExtension):
    """State a package extract run found a Debian package."""

    __tablename__ = "found_deb"

    deb_package_version_id = Column(Integer, ForeignKey("deb_package_version.id", ondelete="CASCADE"), primary_key=True)
    package_extract_run_id = Column(Integer, ForeignKey("package_extract_run.id", ondelete="CASCADE"), primary_key=True)

    deb_package_version = relationship("DebPackageVersion", back_populates="package_extract_runs")
    package_extract_run = relationship("PackageExtractRun", back_populates="found_debs")


class PythonPackageRequirement(Base, BaseExtension):
    """A requirement as stated by a software stack."""

    __tablename__ = "python_package_requirement"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(Text, nullable=False)
    version_range = Column(Text, nullable=False)
    develop = Column(Boolean, nullable=False)
    python_package_index_id = Column(Integer, ForeignKey("python_package_index.id", ondelete="CASCADE"), nullable=True)

    index = relationship("PythonPackageIndex", back_populates="python_package_requirements")
    python_software_stacks = relationship("PythonRequirements", back_populates="python_package_requirement")
    dependency_monkey_runs = relationship(
        "PythonDependencyMonkeyRequirements", back_populates="python_package_requirement"
    )


class CVE(Base, BaseExtension):
    """Information about a CVE."""

    __tablename__ = "cve"

    id = Column(Integer, primary_key=True, autoincrement=True)

    advisory = Column(Text, nullable=True)
    cve_name = Column(Text, nullable=True)
    cve_id = Column(Text, nullable=False, unique=True)
    version_range = Column(Text, nullable=True)
    aggregated_at = Column(DateTime, nullable=True)

    python_package_version_entities = relationship("HasVulnerability", back_populates="cve")


class BuildLogAnalyzerRun(Base, BaseExtension):
    """A class representing a single buildlogs-analyzer (build log analysis) run."""

    __tablename__ = "build_log_analyzer_run"

    id = Column(Integer, primary_key=True, autoincrement=True)
    build_log_analyzer_name = Column(Text, nullable=True)
    build_log_analyzer_version = Column(Text, nullable=True)
    build_log_analysis_document_id = Column(Text, nullable=False)
    datetime = Column(DateTime, nullable=False)
    debug = Column(Boolean, nullable=False, default=False)
    build_log_analyzer_error_reason = Column(Text, nullable=True)
    duration = Column(Integer, nullable=True)
    input_python_package_version_entity_id = Column(
        Integer, ForeignKey("python_package_version_entity.id", ondelete="CASCADE")
    )

    input_python_package_version_entity = relationship(
        "PythonPackageVersionEntity", back_populates="build_log_analyzer_runs"
    )


class PackageAnalyzerRun(Base, BaseExtension):
    """A class representing a single package-analyzer (package analysis) run."""

    __tablename__ = "package_analyzer_run"

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_analyzer_name = Column(Text, nullable=True)
    package_analyzer_version = Column(Text, nullable=True)
    package_analysis_document_id = Column(Text, nullable=False)
    datetime = Column(DateTime, nullable=False)
    debug = Column(Boolean, nullable=False, default=False)
    package_analyzer_error = Column(Boolean, nullable=False, default=False)
    duration = Column(Integer, nullable=True)
    input_python_package_version_entity_id = Column(
        Integer, ForeignKey("python_package_version_entity.id", ondelete="CASCADE")
    )

    input_python_package_version_entity = relationship(
        "PythonPackageVersionEntity", back_populates="package_analyzer_runs"
    )
    python_artifacts = relationship("Investigated", back_populates="package_analyzer_run")
    python_files = relationship("InvestigatedFile", back_populates="package_analyzer_run")


class PythonArtifact(Base, BaseExtension):
    """An artifact for a python package in a specific version."""

    __tablename__ = "python_artifact"

    id = Column(Integer, primary_key=True, autoincrement=True)

    artifact_hash_sha256 = Column(Text, nullable=False)
    artifact_name = Column(Text, nullable=True)
    present = Column(Boolean, nullable=False, default=True)
    # TODO: parse wheel specific tags to make them queryable?

    python_files = relationship("IncludedFile", back_populates="python_artifact")
    python_package_version_entities = relationship("HasArtifact", back_populates="python_artifact")
    package_analyzer_runs = relationship("Investigated", back_populates="python_artifact")
    versioned_symbols = relationship("RequiresSymbol", back_populates="python_artifact")


class InvestigatedFile(Base, BaseExtension):
    """A record about found file by package analyzer."""

    __tablename__ = "investigated_file"

    package_analyzer_run_id = Column(
        Integer, ForeignKey("package_analyzer_run.id", ondelete="CASCADE"), primary_key=True
    )
    python_file_digest_id = Column(Integer, ForeignKey("python_file_digest.id", ondelete="CASCADE"), primary_key=True)

    package_analyzer_run = relationship("PackageAnalyzerRun", back_populates="python_files")
    python_file_digest = relationship("PythonFileDigest", back_populates="package_analyzer_runs")


class Investigated(Base, BaseExtension):
    """A record about investigated Python artifact by a package analyzer."""

    __tablename__ = "investigated"

    package_analyzer_run_id = Column(
        Integer, ForeignKey("package_analyzer_run.id", ondelete="CASCADE"), primary_key=True
    )
    python_artifact_id = Column(Integer, ForeignKey("python_artifact.id", ondelete="CASCADE"), primary_key=True)

    package_analyzer_run = relationship("PackageAnalyzerRun", back_populates="python_artifacts")
    python_artifact = relationship("PythonArtifact", back_populates="package_analyzer_runs")


class PythonFileDigest(Base, BaseExtension):
    """A class representing a single file digests."""

    __tablename__ = "python_file_digest"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sha256 = Column(Text, nullable=False)

    package_extract_runs = relationship("FoundPythonFile", back_populates="python_file_digest")
    package_analyzer_runs = relationship("InvestigatedFile", back_populates="python_file_digest")
    python_artifacts = relationship("IncludedFile", back_populates="python_file_digest")

    __table_args__ = (UniqueConstraint("sha256"), Index("sha256_idx", "sha256", unique=True))


class InspectionRun(Base, BaseExtension):
    """A class representing a single inspection."""

    __tablename__ = "inspection_run"

    id = Column(Integer, primary_key=True, autoincrement=True)

    inspection_document_id = Column(Text, nullable=False)
    inspection_result_number = Column(Integer, nullable=False)
    datetime = Column(DateTime, nullable=True)
    amun_version = Column(Text, nullable=True)
    build_requests_cpu = Column(Float, nullable=True)
    build_requests_memory = Column(Float, nullable=True)
    run_requests_cpu = Column(Float, nullable=True)
    run_requests_memory = Column(Float, nullable=True)
    inspection_sync_state = Column(
        ENUM(
            InspectionSyncStateEnum.PENDING.value,
            InspectionSyncStateEnum.SYNCED.value,
            name="inspection_sync_state",
            create_type=True,
        ),
        nullable=False,
    )

    build_hardware_information_id = Column(Integer, ForeignKey("hardware_information.id", ondelete="CASCADE"))
    run_hardware_information_id = Column(Integer, ForeignKey("hardware_information.id", ondelete="CASCADE"))
    build_software_environment_id = Column(Integer, ForeignKey("software_environment.id", ondelete="CASCADE"))
    run_software_environment_id = Column(Integer, ForeignKey("software_environment.id", ondelete="CASCADE"))
    dependency_monkey_run_id = Column(
        Integer, ForeignKey("dependency_monkey_run.id", ondelete="CASCADE"), nullable=True
    )

    build_hardware_information = relationship(
        "HardwareInformation", back_populates="inspection_runs_build", foreign_keys=[build_hardware_information_id]
    )
    run_hardware_information = relationship(
        "HardwareInformation", back_populates="inspection_runs_run", foreign_keys=[run_hardware_information_id]
    )

    build_software_environment = relationship(
        "SoftwareEnvironment", back_populates="inspection_runs_build", foreign_keys=[build_software_environment_id]
    )
    run_software_environment = relationship(
        "SoftwareEnvironment", back_populates="inspection_runs_run", foreign_keys=[run_software_environment_id]
    )

    dependency_monkey_run = relationship("DependencyMonkeyRun", back_populates="inspection_runs")

    inspection_software_stack_id = Column(Integer, ForeignKey("python_software_stack.id", ondelete="CASCADE"))
    inspection_software_stack = relationship("PythonSoftwareStack", back_populates="inspection_runs")

    matmul_perf_indicators = relationship("PiMatmul", back_populates="inspection_run")
    conv1d_perf_indicators = relationship("PiConv1D", back_populates="inspection_run")
    conv2d_perf_indicators = relationship("PiConv2D", back_populates="inspection_run")
    pybench_perf_indicators = relationship("PiPyBench", back_populates="inspection_run")


class AdviserRun(Base, BaseExtension):
    """A class representing a single adviser run."""

    __tablename__ = "adviser_run"

    id = Column(Integer, primary_key=True, autoincrement=True)

    adviser_document_id = Column(Text, nullable=False)
    datetime = Column(DateTime, nullable=False)
    adviser_version = Column(Text, nullable=False)
    adviser_name = Column(Text, nullable=False)
    count = Column(Integer, nullable=True)
    limit = Column(Integer, nullable=True)
    origin = Column(Text, nullable=True)
    source_type = Column(
        ENUM(
            *(e.name for e in ThothAdviserIntegrationEnum),
            name="source_type",
            create_type=True,
        ),
        nullable=True,
    )
    is_s2i = Column(Boolean, nullable=True)
    debug = Column(Boolean, nullable=False)
    need_re_run = Column(Boolean, nullable=True)
    re_run_adviser_id = Column(Text, nullable=True)
    limit_latest_versions = Column(Integer, nullable=True)
    adviser_error = Column(Boolean, nullable=False, default=False)
    recommendation_type = Column(
        ENUM(
            RecommendationTypeEnum.STABLE.value,
            RecommendationTypeEnum.TESTING.value,
            RecommendationTypeEnum.LATEST.value,
            name="recommendation_type",
            create_type=True,
        ),
        nullable=False,
    )
    requirements_format = Column(
        ENUM(RequirementsFormatEnum.PIPENV.value, name="requirements_format", create_type=True), nullable=False
    )

    # Duration in seconds.
    duration = Column(Integer, nullable=True)  # XXX: nullable for now.
    advised_configuration_changes = Column(Boolean, nullable=False, default=False)
    additional_stack_info = Column(Boolean, nullable=False, default=False)

    user_software_stack_id = Column(Integer, ForeignKey("python_software_stack.id", ondelete="CASCADE"))
    user_software_stack = relationship(
        "PythonSoftwareStack", back_populates="adviser_runs", foreign_keys=[user_software_stack_id]
    )

    advised_software_stacks = relationship("Advised", back_populates="adviser_run")

    python_package_version_entities = relationship("HasUnresolved", back_populates="adviser_run")

    external_run_software_environment_id = Column(
        Integer, ForeignKey("external_software_environment.id", ondelete="CASCADE")
    )

    external_run_software_environment = relationship(
        "ExternalSoftwareEnvironment",
        back_populates="adviser_inputs_run",
        foreign_keys=[external_run_software_environment_id],
    )

    external_build_software_environment_id = Column(
        Integer, ForeignKey("external_software_environment.id", ondelete="CASCADE")
    )

    external_build_software_environment = relationship(
        "ExternalSoftwareEnvironment",
        back_populates="adviser_inputs_build",
        foreign_keys=[external_build_software_environment_id],
    )

    external_hardware_information_id = Column(
        Integer, ForeignKey("external_hardware_information.id", ondelete="CASCADE")
    )
    external_hardware_information = relationship(
        "ExternalHardwareInformation", back_populates="adviser_runs", foreign_keys=[external_hardware_information_id]
    )


class Advised(Base, BaseExtension):
    """A relation stating advised software stack."""

    __tablename__ = "advised"

    adviser_run_id = Column(Integer, ForeignKey("adviser_run.id", ondelete="CASCADE"), primary_key=True)
    python_software_stack_id = Column(
        Integer, ForeignKey("python_software_stack.id", ondelete="CASCADE"), primary_key=True
    )

    adviser_run = relationship("AdviserRun", back_populates="advised_software_stacks")
    python_software_stack = relationship("PythonSoftwareStack", back_populates="advised_by")


class HasUnresolved(Base, BaseExtension):
    """A relation representing a Python package version entity unresolved identified in adviser run."""

    __tablename__ = "has_unresolved"

    adviser_run_id = Column(Integer, ForeignKey("adviser_run.id", ondelete="CASCADE"), primary_key=True)
    python_package_version_entity_id = Column(
        Integer, ForeignKey("python_package_version_entity.id", ondelete="CASCADE"), primary_key=True
    )

    adviser_run = relationship("AdviserRun", back_populates="python_package_version_entities")
    python_package_version_entity = relationship("PythonPackageVersionEntity", back_populates="adviser_runs")


class DependencyMonkeyRun(Base, BaseExtension):
    """A class representing a single dependency-monkey run."""

    __tablename__ = "dependency_monkey_run"

    id = Column(Integer, primary_key=True, autoincrement=True)

    dependency_monkey_document_id = Column(Text, nullable=False)
    datetime = Column(DateTime, nullable=False)
    dependency_monkey_name = Column(Text, nullable=False)
    dependency_monkey_version = Column(Text, nullable=False)
    seed = Column(Integer, nullable=True)
    decision = Column(Text, nullable=False)
    count = Column(Integer, nullable=True)
    limit_latest_versions = Column(Integer, nullable=True)
    debug = Column(Boolean, default=False)
    dependency_monkey_error = Column(Boolean, default=False)
    duration = Column(Integer, nullable=True)  # XXX: nullable for now

    run_software_environment_id = Column(Integer, ForeignKey("software_environment.id", ondelete="CASCADE"))
    build_software_environment_id = Column(Integer, ForeignKey("software_environment.id", ondelete="CASCADE"))
    run_hardware_information_id = Column(Integer, ForeignKey("hardware_information.id", ondelete="CASCADE"))
    build_hardware_information_id = Column(Integer, ForeignKey("hardware_information.id", ondelete="CASCADE"))

    inspection_runs = relationship("InspectionRun", back_populates="dependency_monkey_run")
    python_package_requirements = relationship(
        "PythonDependencyMonkeyRequirements", back_populates="dependency_monkey_run"
    )
    run_software_environment = relationship(
        "SoftwareEnvironment", back_populates="dependency_monkey_runs_run", foreign_keys=[run_software_environment_id]
    )
    build_software_environment = relationship(
        "SoftwareEnvironment",
        back_populates="dependency_monkey_runs_build",
        foreign_keys=[build_software_environment_id],
    )
    run_hardware_information = relationship(
        "HardwareInformation", back_populates="dependency_monkey_runs_run", foreign_keys=[run_hardware_information_id]
    )
    build_hardware_information = relationship(
        "HardwareInformation",
        back_populates="dependency_monkey_runs_build",
        foreign_keys=[build_hardware_information_id],
    )


class HardwareInformation(Base, BaseExtension):
    """Hardware information base class to derive for specific HW environments."""

    __tablename__ = "hardware_information"

    id = Column(Integer, primary_key=True, autoincrement=True)

    cpu_vendor = Column(Integer, nullable=True)
    cpu_model = Column(Integer, nullable=True)
    cpu_cores = Column(Integer, nullable=True)
    cpu_model_name = Column(Text, nullable=True)
    cpu_family = Column(Integer, nullable=True)
    cpu_physical_cpus = Column(Integer, nullable=True)

    gpu_model_name = Column(Text, nullable=True)
    gpu_vendor = Column(Text, nullable=True)
    gpu_cores = Column(Integer, nullable=True)
    gpu_memory_size = Column(Integer, nullable=True)

    ram_size = Column(Integer, nullable=True)

    inspection_runs_run = relationship(
        "InspectionRun",
        back_populates="run_hardware_information",
        foreign_keys="InspectionRun.run_hardware_information_id",
    )
    inspection_runs_build = relationship(
        "InspectionRun",
        back_populates="build_hardware_information",
        foreign_keys="InspectionRun.build_hardware_information_id",
    )
    dependency_monkey_runs_run = relationship(
        "DependencyMonkeyRun",
        back_populates="run_hardware_information",
        foreign_keys="DependencyMonkeyRun.run_hardware_information_id",
    )
    dependency_monkey_runs_build = relationship(
        "DependencyMonkeyRun",
        back_populates="build_hardware_information",
        foreign_keys="DependencyMonkeyRun.build_hardware_information_id",
    )


class ExternalHardwareInformation(Base, BaseExtension):
    """External Hardware information base class to derive for specific HW environments."""

    __tablename__ = "external_hardware_information"

    id = Column(Integer, primary_key=True, autoincrement=True)

    cpu_vendor = Column(Integer, nullable=True)
    cpu_model = Column(Integer, nullable=True)
    cpu_cores = Column(Integer, nullable=True)
    cpu_model_name = Column(Text, nullable=True)
    cpu_family = Column(Integer, nullable=True)
    cpu_physical_cpus = Column(Integer, nullable=True)

    gpu_model_name = Column(Text, nullable=True)
    gpu_vendor = Column(Text, nullable=True)
    gpu_cores = Column(Integer, nullable=True)
    gpu_memory_size = Column(Integer, nullable=True)

    ram_size = Column(Integer, nullable=True)

    adviser_runs = relationship("AdviserRun", back_populates="external_hardware_information")


class ProvenanceCheckerRun(Base, BaseExtension):
    """A class representing a single provenance-checker run."""

    __tablename__ = "provenance_checker_run"

    id = Column(Integer, primary_key=True, autoincrement=True)

    provenance_checker_document_id = Column(Text, nullable=False)
    datetime = Column(DateTime, nullable=False)
    provenance_checker_version = Column(Text, nullable=False)
    provenance_checker_name = Column(Text, nullable=False)
    origin = Column(Text, nullable=True)
    debug = Column(Boolean, nullable=False)
    provenance_checker_error = Column(Boolean, nullable=False, default=False)
    # Duration in seconds.
    duration = Column(Integer, nullable=True)  # nullable for now.

    user_software_stack_id = Column(
        Integer, ForeignKey("python_software_stack.id", ondelete="CASCADE"), primary_key=True
    )
    user_software_stack = relationship("PythonSoftwareStack", back_populates="provenance_checker_runs")


class PythonPackageIndex(Base, BaseExtension):
    """Representation of a Python package Index."""

    __tablename__ = "python_package_index"

    id = Column(Integer, primary_key=True, autoincrement=True)

    url = Column(Text, nullable=False)
    warehouse_api_url = Column(Text, nullable=True, default=None)
    verify_ssl = Column(Boolean, nullable=False, default=True)
    enabled = Column(Boolean, default=False)

    python_package_versions = relationship("PythonPackageVersion", back_populates="index")
    python_package_requirements = relationship("PythonPackageRequirement", back_populates="index")
    python_package_version_entities = relationship("PythonPackageVersionEntity", back_populates="index")

    __table_args__ = (UniqueConstraint("url"), Index("url_idx", "url", unique=True))


class RPMPackageVersion(Base, BaseExtension):
    """RPM-specific package version."""

    __tablename__ = "rpm_package_version"

    id = Column(Integer, primary_key=True, autoincrement=True)

    package_name = Column(Text, nullable=False)
    package_version = Column(Text, nullable=False)
    release = Column(Text, nullable=True)
    epoch = Column(Text, nullable=True)
    arch = Column(Text, nullable=True)
    src = Column(Boolean, nullable=True, default=True)
    package_identifier = Column(Text, nullable=False)

    rpm_requirements = relationship("RPMRequires", back_populates="rpm_package_version")
    package_extract_runs = relationship("FoundRPM", back_populates="rpm_package_version")


class RPMRequires(Base, BaseExtension):
    """RPM requirement mapping."""

    __tablename__ = "rpm_requires"

    rpm_package_version_id = Column(Integer, ForeignKey("rpm_package_version.id", ondelete="CASCADE"), primary_key=True)
    rpm_requirement_id = Column(Integer, ForeignKey("rpm_requirement.id", ondelete="CASCADE"), primary_key=True)

    rpm_package_version = relationship("RPMPackageVersion", back_populates="rpm_requirements")
    rpm_requirement = relationship("RPMRequirement", back_populates="rpm_package_versions")


class RPMRequirement(Base, BaseExtension):
    """Requirement of an RPM as stated in a spec file."""

    __tablename__ = "rpm_requirement"

    id = Column(Integer, primary_key=True, autoincrement=True)

    rpm_requirement_name = Column(Text, nullable=False)
    rpm_package_versions = relationship("RPMRequires", back_populates="rpm_requirement")


class SoftwareEnvironment(Base, BaseExtension):
    """A base class for environment types."""

    __tablename__ = "software_environment"

    id = Column(Integer, primary_key=True, autoincrement=True)

    environment_name = Column(Text, nullable=True)
    python_version = Column(Text, nullable=True)
    image_name = Column(Text, nullable=True)
    image_sha = Column(Text, nullable=True)
    os_name = Column(Text, nullable=True)
    os_version = Column(Text, nullable=True)
    cuda_version = Column(Text, nullable=True)
    environment_type = Column(_ENVIRONMENT_TYPE_ENUM, nullable=False)

    dependency_monkey_runs_run = relationship(
        "DependencyMonkeyRun",
        back_populates="run_software_environment",
        foreign_keys="DependencyMonkeyRun.run_software_environment_id",
    )
    dependency_monkey_runs_build = relationship(
        "DependencyMonkeyRun",
        back_populates="build_software_environment",
        foreign_keys="DependencyMonkeyRun.build_software_environment_id",
    )
    inspection_runs_run = relationship(
        "InspectionRun",
        back_populates="run_software_environment",
        foreign_keys="InspectionRun.build_software_environment_id",
    )
    inspection_runs_build = relationship(
        "InspectionRun",
        back_populates="build_software_environment",
        foreign_keys="InspectionRun.run_software_environment_id",
    )

    package_extract_runs = relationship("PackageExtractRun", back_populates="software_environment")
    versioned_symbols = relationship("HasSymbol", back_populates="software_environment")


class ExternalSoftwareEnvironment(Base, BaseExtension):
    """A base class for environment types."""

    __tablename__ = "external_software_environment"

    id = Column(Integer, primary_key=True, autoincrement=True)

    environment_name = Column(Text, nullable=True)
    python_version = Column(Text, nullable=True)
    image_name = Column(Text, nullable=True)
    image_sha = Column(Text, nullable=True)
    os_name = Column(Text, nullable=True)
    os_version = Column(Text, nullable=True)
    cuda_version = Column(Text, nullable=True)
    environment_type = Column(_ENVIRONMENT_TYPE_ENUM, nullable=False)

    adviser_inputs_run = relationship(
        "AdviserRun",
        back_populates="external_run_software_environment",
        foreign_keys="AdviserRun.external_run_software_environment_id",
    )
    adviser_inputs_build = relationship(
        "AdviserRun",
        back_populates="external_build_software_environment",
        foreign_keys="AdviserRun.external_build_software_environment_id",
    )

    external_package_extract_runs = relationship("PackageExtractRun", back_populates="external_software_environment")
    versioned_symbols = relationship("HasSymbol", back_populates="external_software_environment")


class IncludedFile(Base, BaseExtension):
    """A relation representing file found in the given artifact."""

    __tablename__ = "included_file"

    file = Column(Text, nullable=False)

    python_file_digest_id = Column(Integer, ForeignKey("python_file_digest.id", ondelete="CASCADE"), primary_key=True)
    python_artifact_id = Column(Integer, ForeignKey("python_artifact.id", ondelete="CASCADE"), primary_key=True)

    python_file_digest = relationship("PythonFileDigest", back_populates="python_artifacts")
    python_artifact = relationship("PythonArtifact", back_populates="python_files")


class Identified(Base, BaseExtension):
    """A relation representing a Python package version identified by a package-extract run."""

    __tablename__ = "identified"

    package_extract_run_id = Column(Integer, ForeignKey("package_extract_run.id", ondelete="CASCADE"), primary_key=True)
    python_package_version_entity_id = Column(
        Integer, ForeignKey("python_package_version_entity.id", ondelete="CASCADE"), primary_key=True
    )

    package_extract_run = relationship("PackageExtractRun", back_populates="python_package_version_entities")
    python_package_version_entity = relationship("PythonPackageVersionEntity", back_populates="package_extract_runs")


class HasVulnerability(Base, BaseExtension):
    """The given package version has a vulnerability."""

    __tablename__ = "has_vulnerability"

    python_package_version_entity_id = Column(
        Integer, ForeignKey("python_package_version_entity.id", ondelete="CASCADE"), primary_key=True
    )
    cve_id = Column(Integer, ForeignKey("cve.id", ondelete="CASCADE"), primary_key=True)

    python_package_version_entity = relationship("PythonPackageVersionEntity", back_populates="cves")
    cve = relationship("CVE", back_populates="python_package_version_entities")

    __table_args__ = (
        Index("has_vulnerability_python_package_version_entity_idx", "python_package_version_entity_id"),
    )


class PythonSoftwareStack(Base, BaseExtension):
    """A Python software stack definition."""

    __tablename__ = "python_software_stack"

    id = Column(Integer, primary_key=True, autoincrement=True)

    inspection_runs = relationship("InspectionRun", back_populates="inspection_software_stack")
    adviser_runs = relationship("AdviserRun", back_populates="user_software_stack")
    advised_by = relationship("Advised", back_populates="python_software_stack")
    provenance_checker_runs = relationship("ProvenanceCheckerRun", back_populates="user_software_stack")
    software_stack_type = Column(
        ENUM(
            SoftwareStackTypeEnum.USER.value,
            SoftwareStackTypeEnum.INSPECTION.value,
            SoftwareStackTypeEnum.ADVISED.value,
            name="software_stack_type",
            create_type=True,
        )
    )

    performance_score = Column(Float, nullable=True)
    overall_score = Column(Float, nullable=True)

    python_package_requirements = relationship("PythonRequirements", back_populates="python_software_stack")
    python_package_versions = relationship("PythonRequirementsLock", back_populates="python_software_stack")
    python_package_versions_entities = relationship(
        "ExternalPythonRequirementsLock", back_populates="python_software_stack"
    )


class PythonRequirements(Base, BaseExtension):
    """Requirements for a software stack."""

    __tablename__ = "python_requirements"

    id = Column(Integer, primary_key=True, autoincrement=True)

    python_package_requirement_id = Column(
        Integer, ForeignKey("python_package_requirement.id", ondelete="CASCADE"), primary_key=True
    )
    python_software_stack_id = Column(
        Integer, ForeignKey("python_software_stack.id", ondelete="CASCADE"), primary_key=True
    )

    python_package_requirement = relationship("PythonPackageRequirement", back_populates="python_software_stacks")
    python_software_stack = relationship("PythonSoftwareStack", back_populates="python_package_requirements")


class PythonDependencyMonkeyRequirements(Base, BaseExtension):
    """Requirements for a software stack as run on Dependency Monkey."""

    __tablename__ = "python_dependency_monkey_requirements"

    id = Column(Integer, primary_key=True, autoincrement=True)

    python_package_requirement_id = Column(
        Integer, ForeignKey("python_package_requirement.id", ondelete="CASCADE"), primary_key=True
    )
    dependency_monkey_run_id = Column(
        Integer, ForeignKey("dependency_monkey_run.id", ondelete="CASCADE"), primary_key=True
    )

    python_package_requirement = relationship("PythonPackageRequirement", back_populates="dependency_monkey_runs")
    dependency_monkey_run = relationship("DependencyMonkeyRun", back_populates="python_package_requirements")


class PythonRequirementsLock(Base, BaseExtension):
    """A pinned down requirements for an application."""

    __tablename__ = "python_requirements_lock"

    id = Column(Integer, primary_key=True, autoincrement=True)

    python_package_version_id = Column(
        Integer, ForeignKey("python_package_version.id", ondelete="CASCADE"), primary_key=True
    )
    python_software_stack_id = Column(
        Integer, ForeignKey("python_software_stack.id", ondelete="CASCADE"), primary_key=True
    )

    python_package_version = relationship("PythonPackageVersion", back_populates="python_software_stacks")
    python_software_stack = relationship("PythonSoftwareStack", back_populates="python_package_versions")


class ExternalPythonRequirementsLock(Base, BaseExtension):
    """An External pinned down requirements for an application."""

    __tablename__ = "external_python_requirements_lock"

    id = Column(Integer, primary_key=True, autoincrement=True)

    python_package_version_entity_id = Column(
        Integer, ForeignKey("python_package_version_entity.id", ondelete="CASCADE"), primary_key=True
    )
    python_software_stack_id = Column(
        Integer, ForeignKey("python_software_stack.id", ondelete="CASCADE"), primary_key=True
    )

    python_package_version_entity = relationship("PythonPackageVersionEntity", back_populates="python_software_stacks")
    python_software_stack = relationship("PythonSoftwareStack", back_populates="python_package_versions_entities")


class DebPackageVersion(Base, BaseExtension):
    """Debian-specific package version."""

    __tablename__ = "deb_package_version"

    id = Column(Integer, primary_key=True, autoincrement=True)

    package_name = Column(Text, nullable=False)
    package_version = Column(Text, nullable=False)
    epoch = Column(Text, nullable=True)
    arch = Column(Text, nullable=True)

    depends = relationship("DebDepends", back_populates="deb_package_version")
    replaces = relationship("DebReplaces", back_populates="deb_package_version")
    pre_depends = relationship("DebPreDepends", back_populates="deb_package_version")
    package_extract_runs = relationship("FoundDeb", back_populates="deb_package_version")


class DebDepends(Base, BaseExtension):
    """Depending relation of a deb package."""

    __tablename__ = "deb_depends"

    id = Column(Integer, primary_key=True, autoincrement=True)

    version_range = Column(Text, nullable=False)

    deb_dependency_id = Column(Integer, ForeignKey("deb_dependency.id", ondelete="CASCADE"), primary_key=True)
    deb_package_version_id = Column(Integer, ForeignKey("deb_package_version.id", ondelete="CASCADE"), primary_key=True)

    deb_package_version = relationship("DebPackageVersion", back_populates="depends")
    deb_dependency = relationship("DebDependency", back_populates="deb_package_versions_depends")


class DebPreDepends(Base, BaseExtension):
    """Pre-depending relation of a deb package."""

    __tablename__ = "deb_pre_depends"

    deb_dependency_id = Column(Integer, ForeignKey("deb_dependency.id", ondelete="CASCADE"), primary_key=True)
    deb_package_version_id = Column(Integer, ForeignKey("deb_package_version.id", ondelete="CASCADE"), primary_key=True)

    version_range = Column(Text, nullable=True)
    deb_package_version = relationship("DebPackageVersion", back_populates="pre_depends")
    deb_dependency = relationship("DebDependency", back_populates="deb_package_versions_pre_depends")


class DebReplaces(Base, BaseExtension):
    """A relation of a deb package capturing package replacement.."""

    __tablename__ = "deb_replaces"

    deb_dependency_id = Column(Integer, ForeignKey("deb_dependency.id", ondelete="CASCADE"), primary_key=True)
    deb_package_version_id = Column(Integer, ForeignKey("deb_package_version.id", ondelete="CASCADE"), primary_key=True)

    version_range = Column(Text, nullable=False)
    deb_package_version = relationship("DebPackageVersion", back_populates="replaces")
    deb_dependency = relationship("DebDependency", back_populates="deb_package_versions_replaces")


class DebDependency(Base, BaseExtension):
    """A Debian dependency."""

    __tablename__ = "deb_dependency"

    id = Column(Integer, primary_key=True, autoincrement=True)

    package_name = Column(Text, nullable=False)

    deb_package_versions_depends = relationship("DebDepends", back_populates="deb_dependency")
    deb_package_versions_pre_depends = relationship("DebPreDepends", back_populates="deb_dependency")
    deb_package_versions_replaces = relationship("DebReplaces", back_populates="deb_dependency")


class VersionedSymbol(Base, BaseExtension):
    """A system symbol."""

    __tablename__ = "versioned_symbol"

    id = Column(Integer, primary_key=True, autoincrement=True)

    library_name = Column(Text, nullable=False)
    symbol = Column(Text, nullable=False)

    package_extract_runs = relationship("DetectedSymbol", back_populates="versioned_symbol")
    software_environments = relationship("HasSymbol", back_populates="versioned_symbol")
    python_artifacts = relationship("RequiresSymbol", back_populates="versioned_symbol")

    __table_args__ = (
        Index("versioned_symbol_id_idx", "id", unique=True,),
    )


class HasSymbol(Base, BaseExtension):
    """A relation stating a software environment has a symbol."""

    __tablename__ = "has_symbol"

    software_environment_id = Column(
        Integer, ForeignKey("software_environment.id", ondelete="CASCADE"), primary_key=True
    )
    versioned_symbol_id = Column(Integer, ForeignKey("versioned_symbol.id", ondelete="CASCADE"), primary_key=True)

    software_environment = relationship("SoftwareEnvironment", back_populates="versioned_symbols")
    versioned_symbol = relationship("VersionedSymbol", back_populates="software_environments")

    external_software_environment_id = Column(
        Integer, ForeignKey("external_software_environment.id", ondelete="CASCADE")
    )

    external_software_environment = relationship("ExternalSoftwareEnvironment", back_populates="versioned_symbols")


class RequiresSymbol(Base, BaseExtension):
    """A relation stating a software environment requires a symbol."""

    __tablename__ = "requires_symbol"

    python_artifact_id = Column(Integer, ForeignKey("python_artifact.id", ondelete="CASCADE"), primary_key=True)
    versioned_symbol_id = Column(Integer, ForeignKey("versioned_symbol.id", ondelete="CASCADE"), primary_key=True)

    python_artifact = relationship("PythonArtifact", back_populates="versioned_symbols")
    versioned_symbol = relationship("VersionedSymbol", back_populates="python_artifacts")

    __table_args__ = (
        Index("requires_symbol_python_artifact_id_idx", "python_artifact_id"),
    )


class DetectedSymbol(Base, BaseExtension):
    """A relation stating a package extract run detected a symbol."""

    __tablename__ = "detected_symbol"

    package_extract_run_id = Column(Integer, ForeignKey("package_extract_run.id", ondelete="CASCADE"), primary_key=True)
    versioned_symbol_id = Column(Integer, ForeignKey("versioned_symbol.id", ondelete="CASCADE"), primary_key=True)

    package_extract_run = relationship("PackageExtractRun", back_populates="versioned_symbols")
    versioned_symbol = relationship("VersionedSymbol", back_populates="package_extract_runs")


class PythonPackageMetadata(Base, BaseExtension):
    """Metadata extracted for a Python Package.

    Source: https://packaging.python.org/specifications/core-metadata/
    """

    __tablename__ = "python_package_metadata"

    id = Column(Integer, primary_key=True, autoincrement=True)

    author = Column(Text, nullable=True)
    author_email = Column(Text, nullable=True)
    download_url = Column(Text, nullable=True)
    home_page = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)
    # package licence
    license = Column(Text, nullable=True)
    maintainer = Column(Text, nullable=True)
    maintainer_email = Column(Text, nullable=True)
    metadata_version = Column(Text, nullable=True)
    # package name
    name = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    # package version
    version = Column(Text, nullable=True)
    requires_python = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    description_content_type = Column(Text, nullable=True)

    python_package_versions = relationship("PythonPackageVersion", back_populates="python_package_metadata")

    # multi-part kyes metadata
    classifiers = relationship("HasMetadataClassifier", back_populates="python_package_metadata")
    platforms = relationship("HasMetadataPlatform", back_populates="python_package_metadata")
    supported_platforms = relationship("HasMetadataSupportedPlatform", back_populates="python_package_metadata")
    requires_externals = relationship("HasMetadataRequiresExternal", back_populates="python_package_metadata")
    project_urls = relationship("HasMetadataProjectUrl", back_populates="python_package_metadata")
    provides_extras = relationship("HasMetadataProvidesExtra", back_populates="python_package_metadata")
    # distutils (REQUIRED, PROVIDED, OBSOLETE)
    distutils = relationship("HasMetadataDistutils", back_populates="python_package_metadata")


class HasMetadataClassifier(Base, BaseExtension):
    """The Python package has the given classifier in the metadata."""

    __tablename__ = "has_metadata_classifier"

    python_package_metadata_id = Column(
        Integer, ForeignKey("python_package_metadata.id", ondelete="CASCADE"), primary_key=True
    )
    python_package_metadata_classifier_id = Column(
        Integer, ForeignKey("python_package_metadata_classifier.id", ondelete="CASCADE"), primary_key=True
    )
    python_package_metadata = relationship("PythonPackageMetadata", back_populates="classifiers")
    python_package_metadata_classifiers = relationship(
        "PythonPackageMetadataClassifier", back_populates="python_packages_metadata"
    )


class PythonPackageMetadataClassifier(Base, BaseExtension):
    """Classification value (part of metadata) for the Python Package."""

    __tablename__ = "python_package_metadata_classifier"

    id = Column(Integer, primary_key=True, autoincrement=True)
    classifier = Column(Text, nullable=True)

    python_packages_metadata = relationship(
        "HasMetadataClassifier", back_populates="python_package_metadata_classifiers"
    )


class HasMetadataPlatform(Base, BaseExtension):
    """The Python package has the given platform in the metadata."""

    __tablename__ = "has_metadata_platform"

    python_package_metadata_id = Column(
        Integer, ForeignKey("python_package_metadata.id", ondelete="CASCADE"), primary_key=True
    )
    python_package_metadata_platform_id = Column(
        Integer, ForeignKey("python_package_metadata_platform.id", ondelete="CASCADE"), primary_key=True
    )
    python_package_metadata = relationship("PythonPackageMetadata", back_populates="platforms")
    python_package_metadata_platforms = relationship(
        "PythonPackageMetadataPlatform", back_populates="python_packages_metadata"
    )


class PythonPackageMetadataPlatform(Base, BaseExtension):
    """Platform (part of metadata) describing an operating system supported by the Python Package."""

    __tablename__ = "python_package_metadata_platform"

    id = Column(Integer, primary_key=True, autoincrement=True)
    platform = Column(Text, nullable=True)

    python_packages_metadata = relationship("HasMetadataPlatform", back_populates="python_package_metadata_platforms")


class HasMetadataSupportedPlatform(Base, BaseExtension):
    """The Python package has the given supported platform in the metadata."""

    __tablename__ = "has_metadata_supported_platform"

    python_package_metadata_id = Column(
        Integer, ForeignKey("python_package_metadata.id", ondelete="CASCADE"), primary_key=True
    )
    python_package_metadata_supported_platform_id = Column(
        Integer, ForeignKey("python_package_metadata_supported_platform.id", ondelete="CASCADE"), primary_key=True
    )
    python_package_metadata = relationship("PythonPackageMetadata", back_populates="supported_platforms")
    python_package_metadata_supported_platforms = relationship(
        "PythonPackageMetadataSupportedPlatform", back_populates="python_packages_metadata"
    )


class PythonPackageMetadataSupportedPlatform(Base, BaseExtension):
    """Supported-Platform field (part of metadata) used in binary distributions containing a PKG-INFO file.

    It is used to specify the OS and CPU for which the binary distribution was compiled.
    """

    __tablename__ = "python_package_metadata_supported_platform"

    id = Column(Integer, primary_key=True, autoincrement=True)
    supported_platform = Column(Text, nullable=True)

    python_packages_metadata = relationship(
        "HasMetadataSupportedPlatform", back_populates="python_package_metadata_supported_platforms"
    )


class HasMetadataRequiresExternal(Base, BaseExtension):
    """The Python package has the given dependency in the metadata."""

    __tablename__ = "has_metadata_requires_external"

    python_package_metadata_id = Column(
        Integer, ForeignKey("python_package_metadata.id", ondelete="CASCADE"), primary_key=True
    )
    python_package_metadata_requires_external_id = Column(
        Integer, ForeignKey("python_package_metadata_requires_external.id", ondelete="CASCADE"), primary_key=True
    )
    python_package_metadata = relationship("PythonPackageMetadata", back_populates="requires_externals")
    python_package_metadata_requires_externals = relationship(
        "PythonPackageMetadataRequiresExternal", back_populates="python_packages_metadata"
    )


class PythonPackageMetadataRequiresExternal(Base, BaseExtension):
    """Dependency field (part of metadata) in the system that the distribution (Python package) is to be used.

    This field is intended to serve as a hint to downstream project maintainers,
    and has no semantics which are meaningful to the distutils distribution.
    """

    __tablename__ = "python_package_metadata_requires_external"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dependency = Column(Text, nullable=True)

    python_packages_metadata = relationship(
        "HasMetadataRequiresExternal", back_populates="python_package_metadata_requires_externals"
    )


class HasMetadataProjectUrl(Base, BaseExtension):
    """The Python package has the given project URL in the metadata."""

    __tablename__ = "has_metadata_project_url"

    python_package_metadata_id = Column(
        Integer, ForeignKey("python_package_metadata.id", ondelete="CASCADE"), primary_key=True
    )
    python_package_metadata_project_url_id = Column(
        Integer, ForeignKey("python_package_metadata_project_url.id", ondelete="CASCADE"), primary_key=True
    )
    python_package_metadata = relationship("PythonPackageMetadata", back_populates="project_urls")
    python_package_metadata_project_urls = relationship(
        "PythonPackageMetadataProjectUrl", back_populates="python_packages_metadata"
    )


class PythonPackageMetadataProjectUrl(Base, BaseExtension):
    """Browsable URL (part of metadata) for the project of the Python Package and a label for it."""

    __tablename__ = "python_package_metadata_project_url"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_url = Column(Text, nullable=True)

    python_packages_metadata = relationship(
        "HasMetadataProjectUrl", back_populates="python_package_metadata_project_urls"
    )


class HasMetadataProvidesExtra(Base, BaseExtension):
    """The Python package has the given optional feature in the metadata."""

    __tablename__ = "has_metadata_provides_extra"

    python_package_metadata_id = Column(
        Integer, ForeignKey("python_package_metadata.id", ondelete="CASCADE"), primary_key=True
    )
    python_package_metadata_provides_extra_id = Column(
        Integer, ForeignKey("python_package_metadata_provides_extra.id", ondelete="CASCADE"), primary_key=True
    )
    python_package_metadata = relationship("PythonPackageMetadata", back_populates="provides_extras")
    python_package_metadata_provides_extras = relationship(
        "PythonPackageMetadataProvidesExtra", back_populates="python_packages_metadata"
    )


class PythonPackageMetadataProvidesExtra(Base, BaseExtension):
    """Optional feature (part of metadata) for the Python Package.

    May be used to make a dependency conditional on whether the optional feature has been requested.
    """

    __tablename__ = "python_package_metadata_provides_extra"

    id = Column(Integer, primary_key=True, autoincrement=True)
    optional_feature = Column(Text, nullable=True)

    python_packages_metadata = relationship(
        "HasMetadataProvidesExtra", back_populates="python_package_metadata_provides_extras"
    )


class HasMetadataDistutils(Base, BaseExtension):
    """The Python package has the given distutils in the metadata."""

    __tablename__ = "has_metadata_distutils"

    python_package_metadata_id = Column(
        Integer, ForeignKey("python_package_metadata.id", ondelete="CASCADE"), primary_key=True
    )
    python_package_metadata_distutils_id = Column(
        Integer, ForeignKey("python_package_metadata_distutils.id", ondelete="CASCADE"), primary_key=True
    )

    python_package_metadata = relationship("PythonPackageMetadata", back_populates="distutils")
    python_package_metadata_distutils = relationship(
        "PythonPackageMetadataDistutils", back_populates="python_packages_metadata"
    )


class PythonPackageMetadataDistutils(Base, BaseExtension):
    """Distutils (part of metadata).

    REQUIRED: it means that the distribution (Python package) requires it.

    PROVIDED: it means that the distribution (Python package) has it.

    OBSOLETE: it means that the distribution (Python package) renders obsolete.
    This means that the two projects should not be installed at the same time.
    """

    __tablename__ = "python_package_metadata_distutils"

    id = Column(Integer, primary_key=True, autoincrement=True)
    distutils = Column(Text, nullable=True)
    distutils_type = Column(
        ENUM(
            MetadataDistutilsTypeEnum.REQUIRED.value,
            MetadataDistutilsTypeEnum.PROVIDED.value,
            MetadataDistutilsTypeEnum.OBSOLETE.value,
            name="distutils_type",
            create_type=True,
        )
    )

    python_packages_metadata = relationship("HasMetadataDistutils", back_populates="python_package_metadata_distutils")


class KebechetGithubAppInstallations(Base, BaseExtension):
    """Kebechet Github App Installations.

    slug = namespace/repository (ex - thoth-station/advisor)
    repo_name = repository (ex - advisor)
    private = True or False
    installation_id = provided by github (ex - 236821515)
    """

    __tablename__ = "kebechet_github_installations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(Text, nullable=False, unique=True)
    repo_name = Column(Text, nullable=False)
    private = Column(Boolean, nullable=False)
    installation_id = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False)


class SecurityIndicatorAggregatedRun(Base, BaseExtension):
    """SecurityIndicatorAggregatedRun."""

    __tablename__ = "si_aggregated_run"

    id = Column(Integer, primary_key=True, autoincrement=True)
    si_aggregated_run_document_id = Column(Text, nullable=False)
    datetime = Column(DateTime(timezone=False), nullable=False)

    # SI bandit
    severity_high_confidence_high = Column(Integer, nullable=False)
    severity_high_confidence_low = Column(Integer, nullable=False)
    severity_high_confidence_medium = Column(Integer, nullable=False)
    severity_high_confidence_undefined = Column(Integer, nullable=False)
    severity_low_confidence_high = Column(Integer, nullable=False)
    severity_low_confidence_low = Column(Integer, nullable=False)
    severity_low_confidence_medium = Column(Integer, nullable=False)
    severity_low_confidence_undefined = Column(Integer, nullable=False)
    severity_medium_confidence_high = Column(Integer, nullable=False)
    severity_medium_confidence_low = Column(Integer, nullable=False)
    severity_medium_confidence_medium = Column(Integer, nullable=False)
    severity_medium_confidence_undefined = Column(Integer, nullable=False)
    number_of_analyzed_files = Column(Integer, nullable=False)
    number_of_files_total = Column(Integer, nullable=False)
    number_of_files_with_severities = Column(Integer, nullable=False)
    number_of_filtered_files = Column(Integer, nullable=False)

    # SI cloc

    ## Python files
    number_of_python_files = Column(Integer, nullable=False)
    number_of_lines_with_comments_in_python_files = Column(Integer, nullable=False)
    number_of_blank_lines_in_python_files = Column(Integer, nullable=False)
    number_of_lines_with_code_in_python_files = Column(Integer, nullable=False)

    ## All files
    total_number_of_files = Column(Integer, nullable=False)
    total_number_of_lines = Column(Integer, nullable=False)
    total_number_of_lines_with_comments = Column(Integer, nullable=False)
    total_number_of_blank_lines = Column(Integer, nullable=False)
    total_number_of_lines_with_code = Column(Integer, nullable=False)

    python_package_version_entities = relationship("SIAggregated", back_populates="si_aggregated_run")


class SIAggregated(Base, BaseExtension):
    """A relation representing a Python package version entity analyzed by a si_aggregated_run."""

    __tablename__ = "si_aggregated"

    si_aggregated_run_id = Column(Integer, ForeignKey("si_aggregated_run.id", ondelete="CASCADE"), primary_key=True)
    python_package_version_entity_id = Column(
        Integer, ForeignKey("python_package_version_entity.id", ondelete="CASCADE"), primary_key=True
    )

    si_aggregated_run = relationship("SecurityIndicatorAggregatedRun", back_populates="python_package_version_entities")
    python_package_version_entity = relationship("PythonPackageVersionEntity", back_populates="si_aggregated_runs")


ALL_MAIN_MODELS = frozenset(
    (
        AdviserRun,
        BuildLogAnalyzerRun,
        CVE,
        DebDependency,
        DebPackageVersion,
        DependencyMonkeyRun,
        EcosystemSolver,
        ExternalHardwareInformation,
        ExternalPythonRequirementsLock,
        ExternalSoftwareEnvironment,
        HardwareInformation,
        InspectionRun,
        KebechetGithubAppInstallations,
        PackageAnalyzerRun,
        PackageExtractRun,
        ProvenanceCheckerRun,
        PythonArtifact,
        PythonFileDigest,
        PythonInterpreter,
        PythonPackageIndex,
        PythonPackageMetadata,
        PythonPackageMetadataClassifier,
        PythonPackageMetadataDistutils,
        PythonPackageMetadataPlatform,
        PythonPackageMetadataProjectUrl,
        PythonPackageMetadataProvidesExtra,
        PythonPackageMetadataRequiresExternal,
        PythonPackageMetadataSupportedPlatform,
        PythonPackageRequirement,
        PythonPackageVersion,
        PythonPackageVersionEntity,
        PythonRequirements,
        PythonRequirementsLock,
        PythonSoftwareStack,
        RPMPackageVersion,
        RPMRequirement,
        SecurityIndicatorAggregatedRun,
        SoftwareEnvironment,
        VersionedSymbol
    )
)

ALL_RELATION_MODELS = frozenset(
    (
        Advised,
        DebDepends,
        DebPreDepends,
        DebReplaces,
        DependsOn,
        DetectedSymbol,
        FoundDeb,
        FoundPythonFile,
        FoundPythonInterpreter,
        FoundRPM,
        HasArtifact,
        HasMetadataClassifier,
        HasMetadataDistutils,
        HasMetadataPlatform,
        HasMetadataProjectUrl,
        HasMetadataProvidesExtra,
        HasMetadataRequiresExternal,
        HasMetadataSupportedPlatform,
        HasSymbol,
        HasUnresolved,
        HasVulnerability,
        Identified,
        IncludedFile,
        Investigated,
        InvestigatedFile,
        PythonDependencyMonkeyRequirements,
        RequiresSymbol,
        RPMRequires,
        SIAggregated,
        Solved,
    )
)

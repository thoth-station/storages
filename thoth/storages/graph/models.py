#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# thoth-storages
# Copyright(C) 2018 Fridolin Pokorny
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
    index = VertexProperty(properties.String)


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
    cve_name = VertexProperty(properties.String, default=None)
    cve_id = VertexProperty(properties.String)
    version_range = VertexProperty(properties.String)


class PythonPackageVersion(PackageVersionBase):
    """Python package version vertex."""


class RuntimeEnvironment(VertexBase):
    """Environment such as container image which consists of various packages."""

    runtime_environment_name = VertexProperty(properties.String)
    # TODO: capture hashes of layers


class SoftwareStack(VertexBase):
    """A software stack crated by packages in specific versions."""

    installable = VertexProperty(properties.Boolean, default=True)


class SoftwareStackObservation(VertexBase):
    """Observations we have about the given stack based on run on a specific hardware."""

    performance_index = VertexProperty(properties.Float)
    observation_document_id = VertexProperty(properties.String, db_name='document_id')


class HardwareInformation(VertexBase):
    """Hardware specification and propertires."""

    cpu_vendor = VertexProperty(properties.String)
    cpu_model_name = VertexProperty(properties.String)
    cpu_model = VertexProperty(properties.Integer)
    cpu_family = VertexProperty(properties.Integer)
    cpu_cores = VertexProperty(properties.Integer)

    gpu_vendor = VertexProperty(properties.String)
    gpu_model_name = VertexProperty(properties.String)
    gpu_cores = VertexProperty(properties.Integer)
    gpu_memory_size = VertexProperty(properties.Integer)

    ram_size = VertexProperty(properties.Integer)


class EcosystemSolver(VertexBase):
    """Solver used to resolve dependencies within ecosystem."""

    solver_name = VertexProperty(properties.String)
    solver_version = VertexProperty(properties.String)


class DependsOn(EdgeBase):
    """Dependency between packages modeling based on ecosystem specification."""

    version_range = Property(properties.String, default='*')
    package_name = Property(properties.String)
    extras = Property(properties.String)


class Observed(EdgeBase):
    """Information about observations gathered on run."""

    observation_document_id = Property(properties.String)


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
    # Issues during installation of the given package in the given version
    # (e.g. no native dependency that is needed, issues with setup.py,, ...)
    solver_error = Property(properties.Boolean, default=False)
    # Issues when solving the given package (e.g. the given package does not
    # exist or the given version does not exist.)
    # This flag is an addition to solver_error, meaning if solver_unsolvable is
    # set to True, solver_error is True as well. But NOT vice versa.
    # This behaviour is to simplify queries during recommendations.
    solver_unsolvable = Property(properties.Boolean, default=False)


class PackageExtractNativeBase(EdgeBase):
    """An edge that was captured when analyzing native dependencies (RPM or Debian-based)."""

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


class HasVulnerability(EdgeBase):
    """The given package-v version has a vulnerability."""


class Requires(PackageExtractNativeBase):
    """Requirement edge of an RPM package."""


class DebDepends(PackageExtractNativeBase):
    """Depending edge of a deb package."""

    version_range = Property(properties.String, default='*')


class DebPreDepends(PackageExtractNativeBase):
    """Pre-depending edge of a deb package."""

    version_range = Property(properties.String, default='*')


class DebReplaces(PackageExtractNativeBase):
    """An edge of a deb package capturing package replacement.."""

    version_range = Property(properties.String, default='*')


ALL_MODELS = frozenset((
    CreatesStack,
    CVE,
    DebDepends,
    DebPackageVersion,
    DebPreDepends,
    DebReplaces,
    DependsOn,
    EcosystemSolver,
    HasVersion,
    HasVulnerability,
    IsPartOf,
    Package,
    PythonPackageVersion,
    Requires,
    RPMPackageVersion,
    RPMRequirement,
    RuntimeEnvironment,
    SoftwareStack,
    Solved,
    Observed,
    HardwareInformation,
    SoftwareStackObservation,
))

#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2019, 2020 Francesco Murdaca
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

"""Enum types used in thoth-storages code."""

from enum import Enum


class EnvironmentTypeEnum(Enum):
    """Class for the environment types."""

    RUNTIME = "RUNTIME"
    BUILDTIME = "BUILDTIME"


class SoftwareStackTypeEnum(Enum):
    """Class for the software stack types."""

    USER = "USER"
    INSPECTION = "INSPECTION"
    ADVISED = "ADVISED"


class InspectionSyncStateEnum(Enum):
    """Class for the inspection syncs state."""

    PENDING = "PENDING"
    SYNCED = "SYNCED"


class RecommendationTypeEnum(Enum):
    """Class for the reccomendation type."""

    STABLE = "STABLE"
    TESTING = "TESTING"
    LATEST = "LATEST"
    PERFORMANCE = "PERFORMANCE"
    SECURITY = "SECURITY"


class RequirementsFormatEnum(Enum):
    """Class for the requirements format."""

    PIPENV = "PIPENV"


class MetadataDistutilsTypeEnum(Enum):
    """Class for the requirements format."""

    REQUIRED = "REQUIRED"
    # rarely used fields
    PROVIDED = "PROVIDED"
    OBSOLETE = "OBSOLETE"


class QuerySortTypeEnum(Enum):
    """Class for the requirements format."""

    PACKAGE_NAME = "package_name"
    PACKAGE_VERSION = "package_version"


class PlatformEnum(Enum):
    """Class for platform enum."""

    LINUX_X86_64 = "linux-x86_64"


class KebechetManagerEnum(Enum):
    """Class for Kebechet manager enum."""

    INFO_MANAGER = 1
    PIPFILE_REQUIREMENTS_MANAGER = 2
    UPDATE_MANAGER = 3
    VERSION_MANAGER = 4
    THOTH_ADVISE_MANAGER = 5
    THOTH_PROVENANCE_MANAGER = 6

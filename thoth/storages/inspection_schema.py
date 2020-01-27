#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2019, 2020 Fridolin Pokorny, Francesco Murdaca
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

"""Schema definition for inspection results."""

from voluptuous import Required, Optional
from voluptuous import Schema
from .result_schema import Datetime


# Metadata about specifications produced by inspections.
INSPECTION_SPECIFICATION_SCHEMA = Schema(
    {
        Required("base"): str,
        Optional("build"): dict,
        Optional("environment"): list,
        Optional("files"): list,
        Optional("identifier"): str,
        Optional("packages"): list,
        Optional("python"): dict,
        Optional("python_packages"): list,
        Optional("run"): dict,
        Optional("script"): str,
        Optional("update"): bool,
    }
)


# Metadata about job_log produced by inspections.
INSPECTION_JOB_LOG_SCHEMA = Schema(
    {
        Required("exit_code"): int,
        Required("hwinfo"): dict,
        Required("script_sha256"): str,
        Required("stderr"): str,
        Required("stdout"): dict,
        Required("usage"): dict,
        Required("os_release"): dict,
        Optional("runtime_environment"): dict,
    }
)


# Metadata about status produced by inspections.
INSPECTION_STATUS_SCHEMA = Schema(
    {
        Required("build"): dict,
        Required("job"): dict,
    }
)


# Metadata inspections.
INSPECTION_SCHEMA = Schema(
    {
        Required("specification"): INSPECTION_SPECIFICATION_SCHEMA,
        Required("created"): str,
        Required("build_log"): str,
        Required("job_log"): INSPECTION_JOB_LOG_SCHEMA,
        Required("inspection_id"): str,
        Required("status"): INSPECTION_STATUS_SCHEMA,
    }
)

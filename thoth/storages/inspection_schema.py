#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2019 Fridolin Pokorny, Francesco Murdaca
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

from voluptuous import Required
from voluptuous import Schema
from .result_schema import Datetime


# Metadata about specifications produced by inspections.
INSPECTION_SPECIFICATION_SCHEMA = Schema(
    {
        Required("specification"): list,
    }
)


# Metadata about created produced by inspections.
INSPECTION_CREATED_SCHEMA = Schema(
    {
        Required("created"): Datetime(),
    }
)


# Metadata about build_log produced by inspections.
INSPECTION_BUILD_LOG_SCHEMA = Schema(
    {
        Required("build_log"): str,
    }
)


# Metadata about job_log produced by inspections.
INSPECTION_JOB_LOG_SCHEMA = Schema(
    {
        Required("job_log"): list,
    }
)


# Metadata about inspection_id produced by inspections.
INSPECTION_INSPECTION_ID_SCHEMA = Schema(
    {
        Required("inspection_id"): str,
    }
)


# Metadata about status produced by inspections.
INSPECTION_STATUS_SCHEMA = Schema(
    {
        Required("status"): list,
    }
)


# Metadata inspections.
INSPECTION_SCHEMA = Schema(
    {
        Required("specification"): INSPECTION_SPECIFICATION_SCHEMA,
        Required("created"): INSPECTION_CREATED_SCHEMA,
        Required("build_log"): INSPECTION_BUILD_LOG_SCHEMA,
        Required("job_log"): INSPECTION_JOB_LOG_SCHEMA,
        Required("inspection_id"): INSPECTION_INSPECTION_ID_SCHEMA,
        Required("status"): INSPECTION_STATUS_SCHEMA,
    }
)

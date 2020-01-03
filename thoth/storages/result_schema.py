#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2018, 2019, 2020 Fridolin Pokorny
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

"""Schema definition for analyzer results."""

from voluptuous import Required
from voluptuous import Optional
from voluptuous import Schema

from thoth.common import parse_datetime


class Datetime(object):
    """Check datetime fields against ISO format."""

    def __call__(self, dt):
        """Make check for datetime fields against ISO format."""
        return parse_datetime(dt)


# Describe Python version used by the analyzer image.
PYTHON_SCHEMA = Schema(
    {
        Required("api_version"): int,
        Required("implementation_name"): str,  # e.g. cpython
        Required("major"): int,
        Required("micro"): int,
        Required("minor"): int,
        Required("releaselevel"): str,
        Required("serial"): int,
    }
)


# Describe Linux distribution details that was run in the analyzer image.
DISTRIBUTION_SCHEMA = Schema(
    {
        Required("codename"): str,  # e.g. "Twenty Seven"
        Required("id"): str,  # e.g. "fedora"
        Required("like"): str,
        Required("version"): str,
        Required("version_parts"): {Required("build_number"): str, Required("major"): str, Required("minor"): str},
    }
)

OS_RELEASE_SCHEMA = Schema(
    {
        Optional("redhat_bugzilla_product"): str,
        Optional("redhat_bugzilla_product_version"): str,
        Optional("redhat_support_product"): str,
        Optional("redhat_support_product_version"): str,
        Optional("variant_id"): str,
        Required("id"): str,
        Required("name"): str,
        Required("platform_id"): str,
        Required("version_id"): str,
        Required("version"): str,
    }
)


# Metadata about results produced by analyzers.
METADATA_SCHEMA = Schema(
    {
        Required("analyzer"): str,
        Required("analyzer_version"): str,
        Required("arguments"): dict,
        Required("datetime"): Datetime(),
        Required("distribution"): DISTRIBUTION_SCHEMA,
        Required("document_id"): str,
        Required("duration"): int,
        Required("hostname"): str,
        Required("os_release"): OS_RELEASE_SCHEMA,
        Required("python"): PYTHON_SCHEMA,
        Required("thoth_deployment_name"): str,
        Required("timestamp"): int,
    }
)


# Top level schema for analyzer results.
RESULT_SCHEMA = Schema({Required("metadata"): METADATA_SCHEMA, Required("result"): object})

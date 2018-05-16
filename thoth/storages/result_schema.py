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

"""Schema definition for analyzer results."""

import datetime

from voluptuous import Required
from voluptuous import Schema


class Datetime(object):
    """Check datetime fields against ISO format."""

    def __call__(self, dt):
        """Make check for datetime fields against ISO format."""
        dt, _, us = dt.partition(".")
        dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
        us = int(us.rstrip("Z"), 10)
        return dt + datetime.timedelta(microseconds=us)


# Describe Python version used by the analyzer image.
PYTHON_SCHEMA = Schema({
    Required("api_version"): int,
    Required("implementation_name"): str,   # e.g. cpython
    Required("major"): int,
    Required("micro"): int,
    Required("minor"): int,
    Required("releaselevel"): str,
    Required("serial"): int
})


# Describe Linux distribution details that was run in the analyzer image.
DISTRIBUTION_SCHEMA = Schema({
    Required("codename"): str,  # e.g. "Twenty Seven"
    Required("id"): str,  # e.g. "fedora"
    Required("like"): str,
    Required("version"): str,
    Required("version_parts"): {
        Required("build_number"): str,
        Required("major"): str,
        Required("minor"): str
    }
})


# Metadata about results produced by analyzers.
METADATA_SCHEMA = Schema({
    Required("analyzer"): str,
    Required("analyzer_version"): str,
    Required("arguments"): dict,
    Required("datetime"): Datetime(),
    Required("distribution"): DISTRIBUTION_SCHEMA,
    Required("hostname"): str,
    Required("python"): PYTHON_SCHEMA
})


# Top level schema for analyzer results.
RESULT_SCHEMA = Schema({
    Required("metadata"): METADATA_SCHEMA,
    Required("result"): object
})

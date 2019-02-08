#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2018, 2019 Fridolin Pokorny
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

"""This is the tests."""

import os
import json

import pytest
from voluptuous.error import Error

from .base import ThothStoragesTest

from thoth.storages.result_schema import METADATA_SCHEMA
from thoth.storages.result_schema import RESULT_SCHEMA


def get_metadata(fail):
    """Retrieve all files that store metadata dictionary as a test input."""
    path = os.path.join(ThothStoragesTest.DATA_DIR, 'schema')
    for metadata_file in os.listdir(path):
        if fail and not metadata_file.startswith('metadata_fail_'):
            continue
        elif not fail and not metadata_file.startswith('metadata_ok_'):
            continue

        with open(os.path.join(path, metadata_file)) as mf:
            yield pytest.param(json.load(mf), id=metadata_file)


def get_results(fail):
    """Retrieve all files that store metadata dictionary as a test input."""
    path = os.path.join(ThothStoragesTest.DATA_DIR, 'schema')
    for result_file in os.listdir(path):
        if fail and not result_file.startswith('result_fail_'):
            continue
        elif not fail and not result_file.startswith('result_ok_'):
            continue

        with open(os.path.join(path, result_file)) as mf:
            yield pytest.param(json.load(mf), id=result_file)


@pytest.mark.parametrize("metadata", get_metadata(fail=False))
def test_metadata_schema_ok(metadata):
    """Test correct result schema."""
    METADATA_SCHEMA(metadata)


@pytest.mark.parametrize("metadata", get_metadata(fail=True))
def test_metadata_schema_fail(metadata):
    """Test invalid metadata schema raises an error."""
    with pytest.raises(Error):
        METADATA_SCHEMA(metadata)


@pytest.mark.parametrize("result", get_results(fail=False))
def test_result_schema_ok(result):
    """Test valid result schema matches result schema."""
    RESULT_SCHEMA(result)


@pytest.mark.parametrize("result", get_results(fail=True))
def test_result_schema_fail(result):
    """Test invalid result schema raises an error."""
    with pytest.raises(Error):
        RESULT_SCHEMA(result)

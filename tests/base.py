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
# type: ignore

"""This is the tests."""

import os
import json

import pytest
from flexmock import flexmock


class ThothStoragesTest(object):
    """A main class for testing thoth-storages package."""

    DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")

    @classmethod
    def get_all_results(cls):
        """Retrieve all files that store JSON results as a test input."""
        yield from cls.get_solver_results()
        yield from cls.get_analyzer_results()

    @classmethod
    def get_solver_results(cls):
        return cls._get_result_type("solver")

    @classmethod
    def get_analyzer_results(cls):
        return cls._get_result_type("analyzer")

    @classmethod
    def _get_result_type(cls, result_type):
        path = os.path.join(cls.DATA_DIR, "result", result_type)
        for document_id in os.listdir(path):
            with open(os.path.join(path, document_id)) as document_file:
                yield pytest.param(json.load(document_file), document_id, id=document_id)


class StorageBaseTest(ThothStoragesTest):
    def test_connect(self, adapter):
        """Test lazy connection to Ceph."""
        assert not adapter.is_connected()

        flexmock(adapter.ceph).should_receive("connect").with_args().and_return(None).once()
        flexmock(adapter.ceph).should_receive("is_connected").with_args().and_return(True).once()
        adapter.connect()

        assert adapter.is_connected()

    def test_is_connected(self, adapter):
        assert not adapter.is_connected()
        adapter.connect()
        assert adapter.is_connected()

    def test_retrieve_document(self, adapter):
        """Test proper document retrieval."""
        document = {"foo": "bar"}
        document_id = "<document_id>"
        flexmock(adapter.ceph).should_receive("retrieve_document").with_args(document_id).and_return(document).once()
        assert adapter.ceph.retrieve_document(document_id) == document

    def test_iterate_results(self, adapter):
        """Test iterating over results for build logs stored on Ceph."""
        # Just check that the request is properly propagated.
        flexmock(adapter.ceph).should_receive("iterate_results").with_args().and_yield().once()
        assert list(adapter.iterate_results()) == []

    def test_get_document_listing(self, adapter):
        """Test document listing for build logs stored on Ceph."""
        # Just check that the request is properly propagated.
        flexmock(adapter.ceph).should_receive("get_document_listing").with_args().and_return([]).once()
        assert list(adapter.get_document_listing()) == []

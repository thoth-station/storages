#!/usr/bin/env python3
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

"""This is the tests."""

import flexmock
import pytest

from thoth.storages.result_base import ResultStorageBase

from .base import StorageBaseTest
from .test_ceph import CEPH_INIT_ENV
from .test_ceph import CEPH_INIT_KWARGS
from .utils import connected_ceph_adapter

_DEPLOYMENT_NAME = 'my-deployment'
_RESULT_TYPE = 'TEST'
_BUCKET_PREFIX = 'prefix'

_ENV = {'THOTH_DEPLOYMENT_NAME': _DEPLOYMENT_NAME, **CEPH_INIT_ENV}


class MyResultStorage(ResultStorageBase):
    """A derived class used in tests with mandatory RESULT_TYPE set."""

    RESULT_TYPE = _RESULT_TYPE


@pytest.fixture(name='adapter')
def _fixture_adapter():
    """Retrieve an adapter to build logs."""
    return MyResultStorage(deployment_name=_DEPLOYMENT_NAME,
                           prefix=_BUCKET_PREFIX, **CEPH_INIT_KWARGS)


class ResultBaseTest(StorageBaseTest):  # Ignore PyDocStyleBear
    """The Base Class for Result Tests."""
  # Ignore PycodestyleBear (W293)
    def test_get_document_id(self):  # Ignore PyDocStyleBear
        # Make sure we pick document id from right place.
        document = {'metadata': {'hostname': 'localhost'}}
        assert ResultStorageBase.get_document_id(document) == 'localhost'

    @pytest.mark.parametrize('document,document_id',
                             StorageBaseTest.get_all_results())
    # Ignore PyDocStyleBear
    def test_store_document(self, document, document_id):
        # pytest does not support fixtures and parameters at the same time
        adapter = _fixture_adapter()
        adapter.ceph = flexmock(
            get_document_id=ResultStorageBase.get_document_id)
        adapter.ceph. \
            should_receive('store_document'). \
            with_args(document, document_id). \
            and_return(document_id). \
            once()
        assert adapter.store_document(document) == document_id

    def test_assertion_error(self):
        """Test assertion error if a developer does not provide RESULT_TYPE."""
        with pytest.raises(AssertionError):
            ResultStorageBase(deployment_name=_DEPLOYMENT_NAME,
                              prefix=_BUCKET_PREFIX, **CEPH_INIT_KWARGS)

    @staticmethod
    def store_retrieve_document_test(adapter, document, document_id):
        """Some logic common to Ceph storing/retrieval wrappers.

        Call it with appropriate adapter.
        """
        with connected_ceph_adapter(adapter) as connected_adapter:
            stored_document_id = connected_adapter.store_document(document)
            assert stored_document_id == document_id
            assert connected_adapter.retrieve_document(
                stored_document_id) == document


class TestResultBase(ResultBaseTest):
    """Test base class for result types.

    We need to rename class to rename the class so it starts with Test prefix and is correctly picked by pytest.  # Ignore PycodestyleBear (E501)
    We cannot directly use this class to derive from in result-specific adapters as pytest will run tests multiple  # Ignore PycodestyleBear (E501)
    times for it due to Test prefix. This is a simple workaround to avoid running tests multiple times.  # Ignore PycodestyleBear (E501)
    """

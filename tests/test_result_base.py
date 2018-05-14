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

import os
import json

import flexmock
import pytest

from thoth.storages.result_base import ResultStorageBase

from .base import StorageBaseTest
from .base import ThothStoragesTest
from .test_ceph import CEPH_INIT_ENV
from .test_ceph import CEPH_INIT_KWARGS

_DEPLOYMENT_NAME = 'my-deployment'
_RESULT_TYPE = 'TEST'
_BUCKET_PREFIX = 'prefix'

_ENV = {'THOTH_DEPLOYMENT_NAME': _DEPLOYMENT_NAME, **CEPH_INIT_ENV}


def _get_results():
    """Retrieve all result files that store JSON results as a test input."""
    path = os.path.join(ThothStoragesTest.DATA_DIR, 'result')
    for document_id in os.listdir(path):
        with open(os.path.join(path, document_id)) as document_file:
            # pytest does not allow fixture and parameters at the same time, call fixture explicitly.
            yield pytest.param(_fixture_adapter(), json.load(document_file), document_id, id=document_id)


class MyResultStorage(ResultStorageBase):
    """A derived class used in tests with mandatory RESULT_TYPE set."""
    RESULT_TYPE = _RESULT_TYPE


@pytest.fixture(name='adapter')
def _fixture_adapter():
    """Retrieve an adapter to build logs."""
    return MyResultStorage(deployment_name=_DEPLOYMENT_NAME, prefix=_BUCKET_PREFIX, **CEPH_INIT_KWARGS)


class TestResultBase(StorageBaseTest):
    def test_get_document_id(self):
        # Make sure we pick document id from right place.
        document = {'metadata': {'hostname': 'localhost'}}
        assert ResultStorageBase.get_document_id(document) == 'localhost'

    @pytest.mark.parametrize('adapter,document,document_id', _get_results())
    def test_store_document(self, adapter, document, document_id):
        adapter.ceph = flexmock(get_document_id=ResultStorageBase.get_document_id)
        adapter.ceph. \
            should_receive('store_document'). \
            with_args(document, document_id). \
            and_return(document_id). \
            once()
        assert adapter.store_document(document) == document_id

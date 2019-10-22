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
# type: ignore

"""This is the tests."""

import flexmock
import pytest

from thoth.storages import BuildLogsStore

from .base import StorageBaseTest
from .test_ceph import CEPH_ENV_MAP
from .test_ceph import CEPH_INIT_ENV
from .test_ceph import CEPH_INIT_KWARGS
from .utils import with_adjusted_env

_BUILDLOGS_INIT_KWARGS = {
    'deployment_name': 'testenv',
}

_BUILDLOGS_INIT_KWARGS_EXP = {
    'bucket_prefix': 'thoth-test'
}


_BUILDLOGS_INIT_ENV = {
    'THOTH_DEPLOYMENT_NAME': 'testenv',
}


_BUILDLOGS_INIT_ENV_EXP = {
    'THOTH_CEPH_BUCKET_PREFIX': 'thoth-test'
}


_ENV = {**CEPH_INIT_ENV, **_BUILDLOGS_INIT_ENV, **_BUILDLOGS_INIT_ENV_EXP}


@pytest.fixture(name='adapter')
@with_adjusted_env(_ENV)
def _fixture_adapter():
    """Retrieve an adapter to build logs."""
    return BuildLogsStore()


class TestBuildLogsStore(StorageBaseTest):
    """Test operations on build logs."""

    def test_init_kwargs(self):
        """Test adapter initialization from explicit arguments supplied to constructor."""
        adapter = BuildLogsStore(
            **_BUILDLOGS_INIT_KWARGS, **CEPH_INIT_KWARGS, **_BUILDLOGS_INIT_KWARGS_EXP)
        assert not adapter.is_connected()
        for key, value in _BUILDLOGS_INIT_KWARGS.items():
            assert getattr(adapter, key) == value, \
                f"Build log's adapter attribute {key!r} should have value {value!r} but " \
                f"got {getattr(adapter, key)!r} instead"

        assert adapter.ceph is not None
        assert not adapter.ceph.is_connected()

        for key, value in CEPH_INIT_KWARGS.items():
            assert getattr(adapter.ceph, key) == value, \
                f"Ceph's adapter key {key!r} should have value {value!r} but " \
                f"got {getattr(adapter.ceph, key)!r} instead"

        bucket_prefix = _BUILDLOGS_INIT_KWARGS_EXP['bucket_prefix']
        assert adapter.prefix == f"{bucket_prefix}/{adapter.deployment_name}/buildlogs/"
        assert adapter.ceph.prefix == adapter.prefix

    def test_init_env(self, adapter):
        """Test initialization from env variables."""
        assert not adapter.is_connected()
        assert adapter.ceph is not None
        assert not adapter.ceph.is_connected()

        assert adapter.deployment_name == _BUILDLOGS_INIT_ENV['THOTH_DEPLOYMENT_NAME']

        bucket_prefix = _BUILDLOGS_INIT_ENV_EXP['THOTH_CEPH_BUCKET_PREFIX']
        assert adapter.prefix == f"{bucket_prefix}/{adapter.deployment_name}/buildlogs/"
        assert adapter.ceph.prefix == adapter.prefix

        for key, value in CEPH_INIT_ENV.items():
            attribute = CEPH_ENV_MAP[key]
            assert getattr(adapter.ceph, attribute) == value, \
                f"Ceph's adapter attribute {attribute!r} should have value {value!r} but " \
                f"got {getattr(adapter.ceph, key)!r} instead (env: {key})"

    def test_store_document(self, adapter):
        """Test storing results on Ceph."""
        # This method handling is different from store_document() of result base as we use hashes as ids.
        document = b'{\n  "foo": "bar"\n}'
        document_id = 'bbe8e9a86be651f9efc8e8df7fb76999d8e9a4a9674df9be8de24f4fb3d872a2'
        adapter.ceph = flexmock(dict2blob=lambda _: document)
        adapter.ceph. \
            should_receive('store_blob'). \
            with_args(document, document_id). \
            and_return(document_id). \
            once()
        assert adapter.store_document(document) == document_id

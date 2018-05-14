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

import flexmock
import pytest

from thoth.storages import BuildLogsStore

from .base import ThothStoragesTest
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


class TestBuildLogsStore(ThothStoragesTest):
    """Test operations on build logs."""

    def test_init_kwargs(self):
        """Test adapter initialization from explicit arguments supplied to constructor."""
        adapter = BuildLogsStore(**_BUILDLOGS_INIT_KWARGS, **CEPH_INIT_KWARGS, **_BUILDLOGS_INIT_KWARGS_EXP)
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
        assert adapter.prefix == f"{bucket_prefix}/{adapter.deployment_name}/buildlogs"
        assert adapter.ceph.prefix == adapter.prefix

    def test_init_env(self, adapter):
        """Test initialization from env variables."""
        assert not adapter.is_connected()
        assert adapter.ceph is not None
        assert not adapter.ceph.is_connected()

        assert adapter.deployment_name == _BUILDLOGS_INIT_ENV['THOTH_DEPLOYMENT_NAME']

        bucket_prefix = _BUILDLOGS_INIT_ENV_EXP['THOTH_CEPH_BUCKET_PREFIX']
        assert adapter.prefix == f"{bucket_prefix}/{adapter.deployment_name}/buildlogs"
        assert adapter.ceph.prefix == adapter.prefix

        for key, value in CEPH_INIT_ENV.items():
            attribute = CEPH_ENV_MAP[key]
            assert getattr(adapter.ceph, attribute) == value, \
                f"Ceph's adapter attribute {attribute!r} should have value {value!r} but " \
                f"got {getattr(adapter.ceph, key)!r} instead (env: {key})"

    def test_connect(self, adapter):
        """Test lazy connection to Ceph."""
        assert not adapter.is_connected()

        flexmock(adapter.ceph). \
            should_receive('connect'). \
            with_args(). \
            and_return(None). \
            once()
        flexmock(adapter.ceph).should_receive('is_connected').with_args().and_return(True).once()
        adapter.connect()

        assert adapter.is_connected()

    def test_store_document(self, adapter):
        """Test storing results on Ceph."""
        document = b'{\n  "foo": "bar"\n}'
        document_id = 'bbe8e9a86be651f9efc8e8df7fb76999d8e9a4a9674df9be8de24f4fb3d872a2'
        adapter.ceph = flexmock(dict2blob=lambda _: document)
        adapter.ceph.should_receive('store_blob'). \
            with_args(document, document_id). \
            and_return(document_id). \
            once()
        assert adapter.store_document(document) == document_id

    def test_retrieve_document(self, adapter):
        """Test proper document retrieval."""
        document = {'foo': 'bar'}
        document_id = '<document_id>'
        flexmock(adapter.ceph). \
            should_receive('retrieve_document'). \
            with_args(document_id). \
            and_return(document). \
            once()
        assert adapter.ceph.retrieve_document(document_id) == document

    def test_iterate_results(self, adapter):
        """Test iterating over results for build logs stored on Ceph."""
        # Just check that the request is properly propagated.
        flexmock(adapter.ceph). \
            should_receive('iterate_results'). \
            with_args(). \
            and_return(None). \
            once()
        assert adapter.iterate_results() is None

    def test_get_document_listing(self, adapter):
        """Test document listing for build logs stored on Ceph."""
        # Just check that the request is properly propagated.
        flexmock(adapter.ceph). \
            should_receive('get_document_listing'). \
            with_args(). \
            and_return(None). \
            once()
        assert adapter.get_document_listing() is None

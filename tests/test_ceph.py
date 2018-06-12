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

import pytest
from moto import mock_s3

from thoth.storages import CephStore
from thoth.storages.exceptions import NotFoundError

from .base import ThothStoragesTest
from .utils import with_adjusted_env
from .utils import connected_ceph_adapter


CEPH_INIT_ENV = {
    'THOTH_S3_ENDPOINT_URL ': None,
    'THOTH_CEPH_KEY_ID': 'THOTHISGREATTHOTHISG',
    'THOTH_CEPH_SECRET_KEY': 'THOTHISGREAT+THOTHISGREAT/THOTHISGREAT+S',
    'THOTH_CEPH_BUCKET': 'test-bucket',
    'THOTH_CEPH_REGION': 'us-east-1'
}


CEPH_INIT_KWARGS = {
    'host': 'https://s3.ap-southeast-1.amazonaws.com',  # This host is needed by moto that mocks calls to it.
    'key_id': 'THOTHISGREATTHOTHISG',
    'secret_key': 'THOTHISGREAT+THOTHISGREAT/THOTHISGREAT+S',
    'bucket': 'test-bucket',
    'region': 'us-east-1'
}


# A mapping of env variables to actual properties.
CEPH_ENV_MAP = {
    'THOTH_S3_ENDPOINT_URL ': 'host',
    'THOTH_CEPH_KEY_ID': 'key_id',
    'THOTH_CEPH_SECRET_KEY': 'secret_key',
    'THOTH_CEPH_BUCKET': 'bucket',
    'THOTH_CEPH_REGION': 'region'
}

_ENV = {**CEPH_INIT_ENV}
_BUCKET_PREFIX = 'some-prefix'


@pytest.fixture(name='adapter')
def _fixture_adapter():
    """Retrieve an adapter to Ceph."""
    mock_s3().start()
    try:
        yield CephStore(_BUCKET_PREFIX, **CEPH_INIT_KWARGS)
    finally:
        mock_s3().stop()


@pytest.fixture(name='connected_adapter')
def _fixture_connected_adapter():
    """Retrieve a connected adapter to Ceph."""
    adapter = CephStore(_BUCKET_PREFIX, **CEPH_INIT_KWARGS)
    with connected_ceph_adapter(adapter, raw_ceph=True) as connected_adapter:
        yield connected_adapter


class TestCephStore(ThothStoragesTest):
    def test_init_kwargs(self):
        """Test initialization of Ceph based on arguments."""
        adapter = CephStore(_BUCKET_PREFIX, **CEPH_INIT_KWARGS)

        for key, value in CEPH_INIT_KWARGS.items():
            assert getattr(adapter, key) == value, \
                f"Ceph attribute {key!r} has value {getattr(adapter, key)!r} but expected is {value!r}"

        assert adapter.prefix == _BUCKET_PREFIX
        assert not adapter.is_connected()

    @with_adjusted_env(_ENV)
    def test_init_env(self):
        """Test initialization of Ceph adapter based on env variables."""
        adapter = CephStore(_BUCKET_PREFIX)

        assert adapter.prefix == _BUCKET_PREFIX

        for key, value in CEPH_INIT_ENV.items():
            attribute = CEPH_ENV_MAP[key]
            assert getattr(adapter, attribute) == value, \
                f"Ceph attribute {attribute!r} has value {getattr(adapter, attribute)!r} but expected is " \
                f"{value!r} (env: {key!r})"

    def test_is_connected(self, adapter):
        """Test connection handling."""
        assert not adapter.is_connected()
        adapter.connect()
        assert adapter.is_connected()

    def test_get_document_listing_empty(self, connected_adapter):
        """Test listing of documents stored on Ceph."""
        assert list(connected_adapter.get_document_listing()) == []

    def test_get_document_listing(self, connected_adapter):
        """Test listing of documents stored on Ceph."""
        assert list(connected_adapter.get_document_listing()) == []

        document1, document1_id = {'foo': 'bar'}, '666'
        document2, document2_id = {'foo': 'baz'}, '42'

        connected_adapter.store_document(document1, document1_id)
        connected_adapter.store_document(document2, document2_id)
        document_listing = list(connected_adapter.get_document_listing())

        assert len(document_listing) == 2
        assert document1_id in document_listing
        assert document2_id in document_listing

    def test_test_store_blob(self, connected_adapter):
        """Test storing binary objects onto Ceph."""
        blob = b'foo'
        key = 'some-key'
        connected_adapter.store_blob(blob, key)
        assert connected_adapter.retrieve_blob(key) == blob

    def test_store_document(self, connected_adapter):
        """Test storing document on Ceph."""
        document, key = {'thoth': 'is awesome! ;-)'}, 'my-key'
        assert not connected_adapter.document_exists(key)

        connected_adapter.store_document(document, key)
        assert connected_adapter.retrieve_document(key) == document

    def test_iterate_results_empty(self, connected_adapter):
        assert list(connected_adapter.iterate_results()) == []

    def test_iterate_results(self, connected_adapter):
        """Test iterating over stored documents on Ceph."""
        document1, key1 = {'thoth': 'document'}, 'key-1'
        document2, key2 = {'just': 'dict'}, 'key-2'

        for document_id, document in connected_adapter.iterate_results():
            if document_id == key1:
                assert document == document1
            elif document_id == key2:
                assert document == document2
            else:
                assert False, "The retrieved document was not previously stored."

    def test_retrieve_document_not_exist(self, connected_adapter):
        """Check that retrieving document that does not exists raises an exception."""
        with pytest.raises(NotFoundError):
            connected_adapter.retrieve_document('some-document-that-really-does-not-exist')

    def test_document_exists(self, connected_adapter):
        """Test document presents on Ceph."""
        assert connected_adapter.document_exists('foo') is False
        connected_adapter.store_document({'Hello': 'Thoth'}, 'foo')
        assert connected_adapter.document_exists('foo') is True

    def connect(self, adapter):
        """Test connecting to Ceph."""
        assert not adapter.is_connected()
        adapter.connect()
        assert adapter.is_connected()

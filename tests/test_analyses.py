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

from thoth.storages import AnalysisResultsStore

from .test_result_base import ResultBaseTest
from .test_ceph import CEPH_INIT_KWARGS


_DEPLOYMENT_NAME = 'thoth-my-deployment'
_BUCKET_PREFIX = 'some-analyses'


@pytest.fixture(name='adapter')
def _fixture_adapter():
    """Retrieve an adapter to build logs."""
    return AnalysisResultsStore(deployment_name=_DEPLOYMENT_NAME, prefix=_BUCKET_PREFIX, **CEPH_INIT_KWARGS)


class TestAnalysisResultsStore(ResultBaseTest):
    def test_prefix(self, adapter):
        """Test that results stored on Ceph are correctly prefixed."""
        assert adapter.ceph.prefix == f"{_BUCKET_PREFIX}/{_DEPLOYMENT_NAME}/{adapter.RESULT_TYPE}"

    @pytest.mark.parametrize('document,document_id', ResultBaseTest.get_analyzer_results())
    def test_store_document(self, adapter, document, document_id):
        self.store_retrieve_document_test(adapter, document, document_id)

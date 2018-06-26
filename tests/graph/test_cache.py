#!/usr/bin/env python3  # Ignore PyDocStyleBear
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

from ..base import ThothStoragesTest

from thoth.storages.graph.cache import CacheMiss
from thoth.storages.graph.cache import Cache


@pytest.fixture(name='cache')
def _fixture_adapter():
    """Retrieve a cache instance."""
    return Cache()


class TestCache(ThothStoragesTest):  # Ignore PyDocStyleBear
    def test_wipe(self, cache):  # Ignore PyDocStyleBear
        item, value = {'foo': '<id>'}, 'value'
        cache.put(item, value)

        assert cache.get(item) == value
        cache.wipe()

        with pytest.raises(CacheMiss):
            cache.get(item)

    def test_get_nonexistent(self, cache):  # Ignore PyDocStyleBear
        item, value = {'foo': '<id>'}, 'value'

        cache.put(item, value)

        with pytest.raises(CacheMiss):
            cache.get({'foo': 'some-non-existing-item'})

    def test_get(self, cache):  # Ignore PyDocStyleBear
        item1, value1 = {'foo': '<id1>'}, 'value1'
        item2, value2 = {'bar': '<id2>'}, 'value2'

        cache.put(item1, value1)
        cache.put(item2, value2)

        assert cache.get(item1) == value1
        assert cache.get(item2) == value2

    def test_get_empty(self, cache):  # Ignore PyDocStyleBear
        with pytest.raises(CacheMiss):
            cache.get({'<id>': '<value>'})

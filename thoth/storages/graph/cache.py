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

"""A cache to optimize syncs to JanusGraph database."""

from collections import deque


class CacheMiss(Exception):
    """Exception raised when the given item is not present inside cache."""


class Cache(object):
    """A generic cache for non-hashable item-value pairs."""

    def __init__(self):
        """Initialize cache."""
        # Let's implement cache as a linked list now.
        self._cache = deque()

    def wipe(self):
        """Clear the cache."""
        self._cache.clear()

    def get(self, item):
        """Get the given item from cache."""
        item.pop('id', None)
        for entry in self._cache:
            if entry[0] == item:
                return entry[1]

        raise CacheMiss

    def put(self, item, value):
        """Store the given item with the given value into a cache."""
        item.pop('id', None)  # Do not store ids as they are the actual value.
        self._cache.appendleft((item, value))

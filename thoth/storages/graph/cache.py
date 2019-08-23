#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2019 Fridolin Pokorny
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

"""A cache for Dgraph.

This cache is pre-computed dump of memory to speed up resolutions of popular packages.

There are two main purposes of using this cache:

1. One is reducing number of queries to the graph database for packages which
share dependency sub-graphs.

2. Use this cache to reduce number queries to graph database of "popular" or
"monitored" packages - the cache will be pre-initialized in a form of memory
dump on disk in that cases and loaded in the GraphDatabase adapter on inital
instantiation.
"""

import logging
import os
import pickle
from typing import Set
from typing import Tuple
from typing import Optional

import attr

_LOGGER = logging.getLogger(__name__)


@attr.s(slots=True)
class GraphCache:
    """A Dgraph database cache to speed up resolution of popular packages and packages with overlapping dependencies."""

    # This is a default graph cache - the location is primarily picked for OpenShift's s2i process.
    DEFAULT_CACHE_PATH = "/opt/app-root/src/graph_cache.pickle"
    ENV_CACHE_PATH = "THOTH_STORAGES_GRAPH_CACHE_PATH"

    _uid_map = attr.ib(type=dict, default=attr.Factory(dict))
    _dependencies_map = attr.ib(type=dict, default=attr.Factory(dict))

    def add_uid_record(self, uid: int, package_tuple: Tuple[str, str, str]) -> bool:
        """Add a uid record to the graph cache."""
        recorded_item = self._uid_map.get(uid)
        if recorded_item is not None and package_tuple != recorded_item:
            raise ValueError(
                f"Cache already keeps record for {uid!r} but for different "
                f"item; present {recorded_item}, to insert {package_tuple}"
            )

        if recorded_item:
            return True

        self._uid_map[uid] = package_tuple
        return False

    def get_all_stored_uids(self) -> Set[int]:
        """Retrieve all uids stored in the cache."""
        return set(self._uid_map.keys())

    def add_dependencies(self, package_uid: int, *dependency: int) -> bool:
        """Add a dependency information record."""
        dependencies_set: Set[Tuple[str, str, str]] = self._dependencies_map.get(package_uid)
        if dependencies_set and dependency in dependencies_set:
            return True

        if dependencies_set is None:
            self._dependencies_map[package_uid] = set()

        self._dependencies_map[package_uid].update(dependency)
        return False

    def get_uid_record(self, uid: int) -> Optional[Tuple[str, str, str]]:
        """Retrieve package tuple for the given uid of package tuple."""
        result = self._uid_map.get(uid)
        _LOGGER.debug("Cache hit/miss for uid: %r -> %r", uid, result)
        return result

    def get_dependencies(self, package_uid: int) -> Optional[Set[int]]:
        """Get dependencies for the given uid from cache."""
        result = self._dependencies_map.get(package_uid)
        _LOGGER.debug("Cache hit/miss for package uid dependency: %r -> %r", package_uid, result)
        return result

    @classmethod
    def load(cls, cache_path: str = None) -> "GraphCache":
        """Load graph database if present on filesystem."""
        if not cache_path:
            cache_path = os.getenv(cls.ENV_CACHE_PATH, cls.DEFAULT_CACHE_PATH)

        try:
            with open(cache_path, "rb") as cache_file:
                return pickle.load(cache_file)
        except Exception as exc:
            _LOGGER.warning("Creating empty cache, failed to load cache from %r: %s", cache_path, str(exc))
            return cls()

    def dump(self, cache_path: str = None) -> str:
        """Dump the current state of cache to a pickle specified by path."""
        if not cache_path:
            cache_path = os.getenv(self.ENV_CACHE_PATH, self.DEFAULT_CACHE_PATH)

        _LOGGER.debug("Dumping graph cache to %r", cache_path)
        with open(cache_path, "wb") as cache_file:
            pickle.dump(self, cache_file)

        return cache_path

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

"""Tests related to graph database cache."""

from pathlib import Path

from thoth.storages.graph import GraphCache

from ..base import ThothStoragesTest


class TestCache(ThothStoragesTest):
    """Test graph database cache."""

    def test_dump_and_load(self, tmp_path: Path) -> None:
        """Test creating cache, adding data into it and dumping it with restore."""
        tmp_path = tmp_path / "graph_cache.pickle"
        cache = GraphCache()
        package_tuple = ("tensorflow", "1.9.0", "https://pypi.org/simple")
        dependencies = (2, 3, 4)

        cache.add_uid_record(1, package_tuple)
        cache.add_dependencies(1, *dependencies)
        cache.dump(str(tmp_path))
        del cache

        cache = GraphCache.load(str(tmp_path))

        retrieved_dependencies = cache.get_dependencies(1)
        assert set(dependencies) == retrieved_dependencies

        assert cache.get_uid_record(1) == package_tuple
        assert cache.get_uid_record(0) is None

        assert cache.get_dependencies(1) == set(dependencies)
        assert cache.get_dependencies(0) is None

    def test_add_uid_record(self) -> None:
        """Test adding records to the cache."""
        cache = GraphCache()
        package_tuples = (
            ("tensorflow", "1.9.0", "https://pypi.org/simple"),
            ("flask", "0.12.1", "https://pypi.org/simple"),
            ("numpy", "1.17.0", "https://pypi.org/simple"),
        )

        for i, package_tuple in enumerate(package_tuples):
            cache.add_uid_record(i, package_tuple)

        for i, package_tuple in enumerate(package_tuples):
            assert cache.get_uid_record(i) == package_tuple

        assert cache.get_uid_record(0xDeadBeef) is None

    def test_add_dependencies(self) -> None:
        """Test adding dependencies to cache."""
        cache = GraphCache()
        dependencies = (
            (2, 3, 4, 5),
            (3, 2, 1),
        )

        for i, dep_item in enumerate(dependencies):
            cache.add_dependencies(i, *dep_item)

        for i, dep_item in enumerate(dependencies):
            assert cache.get_dependencies(i) == set(dependencies[i])

        assert cache.get_uid_record(0xDeadBeef) is None

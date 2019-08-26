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

"""Test graph cache."""

from pathlib import Path

import pytest

from thoth.storages.graph import GraphCache

from ..base import ThothStoragesTest


class TestCache(ThothStoragesTest):

    def test_add_python_package_version_entity_uid_record(self, tmp_path: Path) -> None:
        """Test adding records of Python package version entities to the cache."""
        cache = GraphCache.load(str(tmp_path / 'db.sqlite3'))
        package_records = (
            dict(
                package_name="tensorflow",
                package_version="1.9.0"
            ),
            dict(
                package_name="flask",
                package_version="0.12.1",
            )
        )

        for i, package_record in enumerate(package_records):
            cache.add_python_package_version_entity_uid_record(**package_record, uid=i)

        for i, package_record in enumerate(package_records):
            expected = (package_record["package_name"], package_record["package_version"])
            assert cache.get_python_package_version_entity_uid_record(i) == expected

        assert cache.get_python_package_version_entity_uid_record(0xDeadBeef) is None

    def test_get_python_package_version_records(self, tmp_path: Path) -> None:
        """Test retrieval of Python package version records."""
        cache = GraphCache.load(str(tmp_path / 'db.sqlite3'))
        package_records = (
            dict(
                package_name="tensorflow",
                package_version="1.9.0",
                index_url="https://pypi.org/simple",
                os_name="fedora",
                os_version="28",
                python_version="3.6",
            ),
            dict(
                package_name="tensorflow",
                package_version="1.9.0",
                index_url="https://pypi.thoth-station.org/simple",
                os_name="fedora",
                os_version="28",
                python_version="3.6",
            ),
            dict(
                package_name="tensorflow",
                package_version="1.9.0",
                index_url="https://pypi.org/simple",
                os_name="fedora",
                os_version="29",
                python_version="3.7",
            ),
            dict(
                package_name="tensorflow",
                package_version="1.9.0",
                index_url="https://pypi.org/simple",
                os_name="ubi",
                os_version="8",
                python_version="3.6",
            ),
            # This one is duplicate with the previous one to test this.
            dict(
                package_name="tensorflow",
                package_version="1.9.0",
                index_url="https://pypi.org/simple",
                os_name="fedora",
                os_version="29",
                python_version="3.7",
            ),
        )

        for i, package_record in enumerate(package_records):
            cache.add_python_package_version_uid_record(**package_record, uid=i)

        records = cache.get_python_package_version_records(
            package_name="tensorflow",
            package_version="1.9.0",
            os_name=None,
            os_version=None,
            python_version=None,
        )

        assert len(records) == 4
        assert set(tuple(item.items()) for item in records) == set(tuple(item.items()) for item in package_records[:4])

        records = cache.get_python_package_version_records(
            package_name="tensorflow",
            package_version="1.9.0",
            os_name="fedora",
            os_version=None,
            python_version=None,
        )

        assert len(records) == 3
        assert set(tuple(item.items()) for item in records) == set(tuple(item.items()) for item in package_records[:3])

        records = cache.get_python_package_version_records(
            package_name="tensorflow",
            package_version="1.9.0",
            os_name="fedora",
            os_version="28",
            python_version="3.6",
        )

        assert len(records) == 2
        assert set(tuple(item.items()) for item in records) == set(tuple(item.items()) for item in package_records[:2])

    def test_add_python_package_version_uid_record(self, tmp_path: Path) -> None:
        """Test adding records for Python package versions to the cache."""
        cache = GraphCache.load(str(tmp_path / 'db.sqlite3'))
        package_records = (
            dict(
                package_name="tensorflow",
                package_version="1.9.0",
                index_url="https://pypi.org/simple",
                os_name="fedora",
                os_version="28",
                python_version="3.6",
            ),
            dict(
                package_name="flask",
                package_version="0.12.1",
                index_url="https://pypi.org/simple",
                os_name="fedora",
                os_version="29",
                python_version="3.6",
            ),
            dict(
                package_name="numpy",
                package_version="1.17.0",
                index_url="https://pypi.org/simple",
                os_name="fedora",
                os_version="30",
                python_version="3.7",
            ),
        )

        for i, package_record in enumerate(package_records):
            cache.add_python_package_version_uid_record(**package_record, uid=i)

        for i, package_record in enumerate(package_records):
            assert cache.get_python_package_version_uid_record(i) == package_record

        assert cache.get_python_package_version_uid_record(0xDeadBeef) is None

    def test_add_depends_on_simple(self, tmp_path: Path) -> None:
        """Test adding dependencies to cache."""
        cache = GraphCache.load(str(tmp_path / "db.sqlite3"))
        package_records = (
            dict(
                package_name="tensorflow",
                package_version="1.9.0",
                index_url="https://pypi.org/simple",
                os_name="fedora",
                os_version="28",
                python_version="3.6",
                dependency_name="numpy",
                dependency_version="1.17.0",
            ),
            dict(
                package_name="flask",
                package_version="0.12.1",
                index_url="https://pypi.org/simple",
                os_name="fedora",
                os_version="29",
                python_version="3.6",
                dependency_name="werkzeug",
                dependency_version="0.15.5",
            ),
        )

        for record in package_records:
            cache.add_depends_on(**record)

        for item in package_records:
            dependency_name, dependency_version = item.pop("dependency_name"), item.pop("dependency_version")
            assert {(dependency_name, dependency_version)} == cache.get_depends_on(**item)

    def test_add_depends_on_no_deps(self, tmp_path: Path) -> None:
        """Test if no dependencies are present for the given package."""
        cache = GraphCache.load(str(tmp_path / "db.sqlite3"))
        record = dict(
            package_name="flask",
            package_version="0.12.1",
            index_url="https://pypi.org/simple",
            os_name="fedora",
            os_version="29",
            python_version="3.6",
            dependency_name=None,
            dependency_version=None,
        )

        cache.add_depends_on(**record)
        record.pop("dependency_name")
        record.pop("dependency_version")
        assert cache.get_depends_on(**record) == set()

    def test_add_depends_on_no_deps_error(self, tmp_path: Path) -> None:
        """Test error if wrong parameters are supplied"""
        cache = GraphCache.load(str(tmp_path / "db.sqlite3"))

        with pytest.raises(ValueError):
            cache.add_depends_on(
                package_name="flask",
                package_version="0.12.1",
                index_url="https://pypi.org/simple",
                os_name="fedora",
                os_version="29",
                python_version="3.6",
                dependency_name="foo",
                dependency_version=None,
            )

        with pytest.raises(ValueError):
            cache.add_depends_on(
                package_name="flask",
                package_version="0.12.1",
                index_url="https://pypi.org/simple",
                os_name="fedora",
                os_version="29",
                python_version="3.6",
                dependency_name=None,
                dependency_version="bar",
            )

    def test_get_depends_on_no_record(self, tmp_path: Path) -> None:
        """Test return value of not cached item yet."""
        cache = GraphCache.load(str(tmp_path / "db.sqlite3"))

        assert cache.get_depends_on(
            package_name="flask",
            package_version="0.12.1",
            index_url="https://pypi.org/simple",
            os_name="fedora",
            os_version="29",
            python_version="3.6",
        ) is None

    def test_multiple_match(self, tmp_path: Path) -> None:
        """Test retrieval of multiple records from the database."""
        cache = GraphCache.load(str(tmp_path / "db.sqlite3"))

        package_records = (
            dict(
                package_name="tensorflow",
                package_version="1.9.0",
                index_url="https://pypi.org/simple",
                os_name="fedora",
                os_version="28",
                python_version="3.6",
                dependency_name="numpy",
                dependency_version="1.17.0",
            ),
            dict(
                package_name="tensorflow",
                package_version="1.9.0",
                index_url="https://pypi.org/simple",
                os_name="fedora",
                os_version="29",
                python_version="3.6",
                dependency_name="numpy",
                dependency_version="1.17.0",
            ),
            dict(
                package_name="tensorflow",
                package_version="1.9.0",
                index_url="https://pypi.org/simple",
                os_name="fedora",
                os_version="29",
                python_version="3.6",
                dependency_name="numpy",
                dependency_version="1.16.0",
            ),
        )

        for record in package_records:
            cache.add_depends_on(**record)

        result = cache.get_depends_on(
            package_name="tensorflow",
            package_version="1.9.0",
            index_url="https://pypi.org/simple"
        )
        assert result == {("numpy", "1.16.0"), ("numpy", "1.17.0")}

    def test_stats(self, tmp_path: Path):
        """Test gathering statistics about cache."""
        cache = GraphCache.load(str(tmp_path / "db.sqlite3"))
        cache.add_depends_on(
            package_name="flask",
            package_version="0.12.1",
            index_url="https://pypi.org/simple",
            os_name="fedora",
            os_version="29",
            python_version="3.6",
            dependency_name="selinon",
            dependency_version="1.0.0",
        )
        assert cache.stats() == {
            'depends_on': 1,
            'python_package_version_entity_uid': 0,
            'python_package_version_uid': 0,
        }

        cache.add_python_package_version_uid_record(
            package_name="tensorflow",
            package_version="1.9.0",
            index_url="https://pypi.org/simple",
            os_name="fedora",
            os_version="29",
            python_version="3.7",
            uid=2,
        )
        assert cache.stats() == {
            'depends_on': 1,
            'python_package_version_entity_uid': 0,
            'python_package_version_uid': 1,
        }

        cache.add_python_package_version_entity_uid_record(
            package_name="tensorflow",
            package_version="1.9.0",
            uid=3,
        )
        assert cache.stats() == {
            'depends_on': 1,
            'python_package_version_entity_uid': 1,
            'python_package_version_uid': 1,
        }

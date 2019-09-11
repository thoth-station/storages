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
    """Test manipulation with graph cache."""

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
            assert {(dependency_name, dependency_version)} == set(cache.get_depends_on(**item))

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
        assert cache.get_depends_on(**record) == []

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

        result = set(cache.get_depends_on(
            package_name="tensorflow",
            package_version="1.9.0",
            index_url="https://pypi.org/simple"
        ))
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
            'sqlite_cache_info': {
                'get_depends_on': {
                    'hits': 0,
                    'misses': 0
                },
                'get_python_package_version_records': {
                    'hits': 0,
                    'misses': 0
                }
            },
            'table_size': {
                'depends_on': 1,
                'python_package_version': 1,
                'python_package_version_entity': 1
            }
        }

        cache.get_depends_on(
            package_name="flask",
            package_version="0.12.1",
            index_url="https://pypi.org/simple",
            os_name="fedora",
            os_version="29",
            python_version="3.6",
        )

        assert cache.stats() == {
            'sqlite_cache_info': {
                'get_depends_on': {
                    'hits': 1,
                    'misses': 0
                },
                'get_python_package_version_records': {
                    'hits': 0,
                    'misses': 0
                }
            },
            'table_size': {
                'depends_on': 1,
                'python_package_version': 1,
                'python_package_version_entity': 1
            }
        }

        cache.get_depends_on(
            package_name="nonexistingpackage",
            package_version="0.0.0",
            index_url="https://pypi.org/simple",
            os_name="fedora",
            os_version="29",
            python_version="3.6",
        )

        assert cache.stats() == {
            'sqlite_cache_info': {
                'get_depends_on': {
                    'hits': 1,
                    'misses': 1
                },
                'get_python_package_version_records': {
                    'hits': 0,
                    'misses': 0
                }
            },
            'table_size': {
                'depends_on': 1,
                'python_package_version': 1,
                'python_package_version_entity': 1
            }
        }

        cache.get_python_package_version_records(
            package_name="nonexistingpackage",
            package_version="0.0.0",
            index_url="https://pypi.org/simple",
            os_name="fedora",
            os_version="29",
            python_version="3.6",
        )

        assert cache.stats() == {
            'sqlite_cache_info': {
                'get_depends_on': {
                    'hits': 1,
                    'misses': 1
                },
                'get_python_package_version_records': {
                    'hits': 0,
                    'misses': 1
                }
            },
            'table_size': {
                'depends_on': 1,
                'python_package_version': 1,
                'python_package_version_entity': 1
            }
        }

        cache.get_python_package_version_records(
            package_name="flask",
            package_version="0.12.1",
            index_url="https://pypi.org/simple",
            os_name="fedora",
            os_version="29",
            python_version=None,
        )

        assert cache.stats() == {
            'sqlite_cache_info': {
                'get_depends_on': {
                    'hits': 1,
                    'misses': 1
                },
                'get_python_package_version_records': {
                    'hits': 1,
                    'misses': 1
                }
            },
            'table_size': {
                'depends_on': 1,
                'python_package_version': 1,
                'python_package_version_entity': 1
            }
        }

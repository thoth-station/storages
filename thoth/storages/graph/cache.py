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

"""A graph database cache implementation to speed up queries.

The implementation uses actually two caches - one in-memory for LRU based on
method calls and another one which is build on top of SQLite3.
"""

import os
import logging
import sqlite3
import functools
from methodtools import lru_cache
from itertools import combinations
from typing import Set
from typing import Tuple
from typing import List
from typing import Optional
from typing import Union

import attr

_LOGGER = logging.getLogger(__name__)


def _only_if_enabled(func):
    """A decorator to make sure the graph database cache is used only if enabled."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not args[0].is_enabled():
            return None

        return func(*args, **kwargs)

    return wrapper


def _only_if_inserts_enabled(func):
    """Decorator to make sure inserts are noop on production systems to reduce cache building overhead."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not args[0].is_insert_enabled():
            return None

        return func(*args, **kwargs)

    return wrapper


@attr.s(slots=True)
class GraphCache:
    """A Dgraph database cache to speed up resolution of popular packages and packages with overlapping dependencies."""

    # This is a default graph cache - using in-memory. In a deployment we point to a path on disk.
    DEFAULT_CACHE_PATH = ":memory:"
    ENV_CACHE_PATH = "THOTH_STORAGES_GRAPH_CACHE"

    _CREATE_DEPENDS_ON_DATABASE = """CREATE TABLE depends_on ( \
 package_name TEXT NOT NULL, \
 package_version TEXT NOT NULL, \
 index_url TEXT NOT NULL, \
 os_name TEXT NOT NULL, \
 os_version TEXT NOT NULL, \
 python_version TEXT NOT NULL, \
 dependency_name TEXT, \
 dependency_version TEXT, \
 UNIQUE( \
  package_name, \
  package_version, \
  index_url, \
  os_name, \
  os_version, \
  python_version, \
  dependency_name, \
  dependency_version \
 )
)"""

    _CREATE_PYTHON_PACKAGE_VERSION_UID_DATABASE = """CREATE TABLE python_package_version_uid ( \
 package_name TEXT NOT NULL, \
 package_version TEXT NOT NULL, \
 index_url TEXT NOT NULL, \
 os_name TEXT NOT NULL, \
 os_version TEXT NOT NULL, \
 python_version TEXT NOT NULL, \
 uid int PRIMARY KEY, \
 UNIQUE(
  package_name, \
  package_version, \
  index_url, \
  os_name, \
  os_version, \
  python_version \
 )
)"""

    _CREATE_PYTHON_PACKAGE_VERSION_ENTITY_UID_DATABASE = """CREATE TABLE python_package_version_entity_uid ( \
 package_name TEXT NOT NULL, \
 package_version TEXT NOT NULL, \
 uid int PRIMARY KEY, \
 UNIQUE(
  package_name, \
  package_version \
 )
)"""

    _SELECT_DEPENDS_ON_BASE = """SELECT dependency_name, dependency_version FROM depends_on WHERE \
 package_name=:package_name AND \
 package_version=:package_version AND \
 index_url=:index_url \
"""

    _SELECT_PYTHON_PACKAGE_VERSIONS_BASE = """SELECT \
 package_name, \
 package_version, \
 index_url, \
 os_name, \
 os_version, \
 python_version FROM python_package_version_uid WHERE package_name=:package_name AND package_version=:package_version
"""

    _SELECT_PYTHON_PACKAGE_VERSION_UID = """SELECT \
 package_name, \
 package_version, \
 index_url, \
 os_name, \
 os_version, \
 python_version FROM python_package_version_uid WHERE uid=:uid
"""

    _SELECT_PYTHON_PACKAGE_VERSION_ENTITY_UID = """SELECT \
 package_name, \
 package_version FROM python_package_version_entity_uid WHERE uid=:uid
"""

    _QUERY_TABLE_EXISTS = """SELECT CASE WHEN name = :table THEN 1 ELSE 0 END FROM sqlite_master WHERE \
  name = :table AND type = 'table'
"""

    _TABLES = {
        "depends_on": _CREATE_DEPENDS_ON_DATABASE,
        "python_package_version_uid": _CREATE_PYTHON_PACKAGE_VERSION_UID_DATABASE,
        "python_package_version_entity_uid": _CREATE_PYTHON_PACKAGE_VERSION_ENTITY_UID_DATABASE,
    }

    sqlite_connection = attr.ib(type=sqlite3.Connection)

    @classmethod
    def load(cls, db_file: str = None) -> "GraphCache":
        """Prepare graph cache by loading an already existing one or a new one."""
        if not db_file:
            db_file = os.getenv(cls.ENV_CACHE_PATH, cls.DEFAULT_CACHE_PATH)

        if db_file == ":memory:":
            _LOGGER.info("Using in-memory graph database cache")
        else:
            _LOGGER.info("Using graph database cache from %r", db_file)

        instance = cls(sqlite_connection=sqlite3.connect(db_file))
        instance.initialize()
        return instance

    @staticmethod
    def is_enabled():
        """Check if this cache is enabled."""
        return not bool(int(os.getenv("THOTH_STORAGES_GRAPH_CACHE_DISABLED", 0)))

    @staticmethod
    def is_insert_enabled():
        """Check if inserts to this cache are enabled."""
        return not bool(int(os.getenv("THOTH_STORAGES_GRAPH_CACHE_INSERTS_DISABLED", 0)))

    @_only_if_enabled
    def _create_indexes_depends_on(self):
        """Create indexes for depends_on table to optimize look-ups."""
        cursor = self.sqlite_connection.cursor()

        _LOGGER.debug("Creating index depends_on_all")
        cursor.execute(
            """CREATE INDEX IF NOT EXISTS depends_on_all ON depends_on \
 (package_name, package_version, index_url, os_name, os_version, python_version)
"""
        )

        _LOGGER.debug("Creating index python_package_version_uid_all")
        cursor.execute(
            """CREATE UNIQUE INDEX IF NOT EXISTS python_package_version_uid_all ON python_package_version_uid \
 (package_name, package_version, index_url, os_name, os_version, python_version)
"""
        )

        columns_to_variate = ("index_url", "os_name", "os_version", "python_version")
        for i in range(1, len(columns_to_variate)):
            for j, variation in enumerate(combinations(columns_to_variate, i)):
                _LOGGER.debug("Creating index depends_on_%d%d: %s", i, j, variation)
                cursor.execute(
                    """CREATE INDEX IF NOT EXISTS depends_on_%d%d ON depends_on \
     (package_name, package_version, index_url, %s)
    """
                    % (i, j, ",".join(variation))
                )

                _LOGGER.debug("Creating index python_package_version_uid_%d%d: %s", i, j, variation)
                cursor.execute(
                    """CREATE INDEX IF NOT EXISTS python_package_version_uid_%d%d ON depends_on \
     (package_name, package_version, index_url, %s)
    """
                    % (i, j, ",".join(variation))
                )

        self.sqlite_connection.commit()
        cursor.close()

    @_only_if_enabled
    def initialize(self):
        """Initialize database if not already initialized."""
        cursor = self.sqlite_connection.cursor()

        for table_name, create_query in self._TABLES.items():
            cursor.execute(self._QUERY_TABLE_EXISTS, {"table": table_name})
            if not cursor.fetchone():
                _LOGGER.debug("Creating database %r", table_name)
                cursor.execute(create_query)
            else:
                _LOGGER.debug("Database %r is already present", table_name)

        cursor.close()
        self.sqlite_connection.commit()
        self._create_indexes_depends_on()

    @staticmethod
    def _get_params_ext(
        package_name: str,
        package_version: str,
        index_url: str = None,
        *,
        os_name: str = None,
        os_version: str = None,
        python_version: str = None,
    ) -> Tuple[str, dict]:
        """Get parameters and extension to query."""
        query_ext = ""
        query_params = {"package_name": package_name, "package_version": package_version}

        if index_url:
            query_params["index_url"] = index_url

        if os_name:
            query_ext += " AND os_name=:os_name "
            query_params["os_name"] = os_name

        if os_version:
            query_ext += " AND os_version=:os_version "
            query_params["os_version"] = os_version

        if python_version:
            query_ext += " AND python_version=:python_version "
            query_params["python_version"] = python_version

        return query_ext, query_params

    @lru_cache(maxsize=2048)
    @_only_if_enabled
    def get_depends_on(
        self,
        package_name: str,
        package_version: str,
        index_url: str,
        *,
        os_name: str = None,
        os_version: str = None,
        python_version: str = None,
    ) -> Optional[Set[Tuple[str, str]]]:
        """Retrieve dependencies for the given packages."""
        query_ext, query_params = self._get_params_ext(
            package_name=package_name,
            package_version=package_version,
            index_url=index_url,
            os_name=os_name,
            os_version=os_version,
            python_version=python_version,
        )
        query = self._SELECT_DEPENDS_ON_BASE + query_ext

        cursor = self.sqlite_connection.cursor()
        try:
            cursor.execute(query, query_params)
            query_result = cursor.fetchall()
            if not query_result:
                # No records in the database.
                return None

            result = set()
            for item in query_result:
                dependency_name, dependency_version = item[0], item[1]
                if dependency_name is None and dependency_version is None:
                    # If we have a record that any of the given do not
                    # match criteria, we return any result computed so far.
                    # An example could be flask==1.0.0 depending only on werkzeug on fedora:31, but no
                    # dependency for flask==1.0.0 on fedora:30 (assuming no operating system was
                    # specified). Then we return werkzeug as we do "generic"/platform independent resolution.
                    continue

                result.add((dependency_name, dependency_version))

            return result
        finally:
            cursor.close()

    @lru_cache(maxsize=2048)
    @_only_if_enabled
    def get_python_package_version_records(
        self,
        package_name: str,
        package_version: str,
        index_url: Union[str, None],
        os_name: Union[str, None],
        os_version: Union[str, None],
        python_version: Union[str, None],
    ) -> Optional[List[dict]]:
        """Get records for Python packages matching the given criteria for environment."""
        query_ext, query_params = self._get_params_ext(
            package_name=package_name,
            package_version=package_version,
            index_url=index_url,
            os_name=os_name,
            os_version=os_version,
            python_version=python_version,
        )

        query = self._SELECT_PYTHON_PACKAGE_VERSIONS_BASE + query_ext
        cursor = self.sqlite_connection.cursor()
        try:
            cursor.execute(query, query_params)
            result = cursor.fetchall()

            if not result:
                return None

            return [
                dict(
                    package_name=item[0],
                    package_version=item[1],
                    index_url=item[2],
                    os_name=item[3],
                    os_version=item[4],
                    python_version=item[5],
                )
                for item in result
            ]
        finally:
            cursor.close()

    @lru_cache(maxsize=256)
    @_only_if_enabled
    def get_python_package_version_uid_record(self, uid: int) -> Optional[dict]:
        """Get uid for the give Python package version."""
        cursor = self.sqlite_connection.cursor()
        try:
            cursor.execute(self._SELECT_PYTHON_PACKAGE_VERSION_UID, dict(uid=uid))
            result = cursor.fetchone()
            if not result:
                return None

            return dict(
                package_name=result[0],
                package_version=result[1],
                index_url=result[2],
                os_name=result[3],
                os_version=result[4],
                python_version=result[5],
            )
        finally:
            cursor.close()

    @lru_cache(maxsize=256)
    @_only_if_enabled
    def get_python_package_version_entity_uid_record(self, uid: int) -> Optional[Tuple[str, str]]:
        """Get uid for the give Python package version entity."""
        params = locals()
        params.pop("self")

        cursor = self.sqlite_connection.cursor()
        try:
            cursor.execute(self._SELECT_PYTHON_PACKAGE_VERSION_ENTITY_UID, dict(uid=uid))
            result = cursor.fetchone()
            if not result:
                return None

            return result[0], result[1]
        finally:
            cursor.close()

    @_only_if_enabled
    @_only_if_inserts_enabled
    def add_depends_on(
        self,
        package_name: str,
        package_version: str,
        index_url: str,
        *,
        os_name: str,
        os_version: str,
        python_version: str,
        dependency_name: str,
        dependency_version: str,
    ) -> None:
        """Add a new entry of depends on for a Python package."""
        if (
            dependency_name is None
            and dependency_version is not None
            or dependency_name is not None
            and dependency_version is None
        ):
            raise ValueError(f"Integrity error - cannot insert {dependency_name} in version {dependency_version}")

        values = (
            package_name,
            package_version,
            index_url,
            os_name,
            os_version,
            python_version,
            dependency_name,
            dependency_version,
        )
        cursor = self.sqlite_connection.cursor()
        try:
            cursor.execute("INSERT INTO depends_on VALUES (?, ?, ?, ?, ?, ?, ?, ?)", values)
            self.sqlite_connection.commit()
        except sqlite3.IntegrityError as exc:
            _LOGGER.debug("Cannot insert depends_on entry %r: %s", values, str(exc))
        finally:
            cursor.close()

    @_only_if_enabled
    @_only_if_inserts_enabled
    def add_python_package_version_uid_record(
        self,
        package_name: str,
        package_version: str,
        index_url: str,
        *,
        os_name: Union[str, None],
        os_version: Union[str, None],
        python_version: Union[str, None],
        uid: int,
    ) -> None:
        """Add a new record to Python package version uid database."""
        values = (package_name, package_version, index_url, os_name, os_version, python_version, uid)

        cursor = self.sqlite_connection.cursor()
        try:
            cursor.execute("INSERT INTO python_package_version_uid VALUES (?, ?, ?, ?, ?, ?, ?)", values)
            self.sqlite_connection.commit()
        except sqlite3.IntegrityError as exc:
            _LOGGER.debug("Cannot insert python_package_version_uid entry %r: %s", values, str(exc))
        finally:
            cursor.close()

    @_only_if_enabled
    @_only_if_inserts_enabled
    def add_python_package_version_entity_uid_record(self, package_name: str, package_version: str, uid: int) -> None:
        """Add a new record to Python package version entity uid database."""
        values = (package_name, package_version, uid)

        cursor = self.sqlite_connection.cursor()
        try:
            cursor.execute("INSERT INTO python_package_version_entity_uid VALUES (?, ?, ?)", values)
            self.sqlite_connection.commit()
        except sqlite3.IntegrityError as exc:
            _LOGGER.debug("Cannot insert python_package_version_entity_uid entry %r: %s", values, str(exc))
        finally:
            cursor.close()

    def stats(self) -> dict:
        """Get statistics for the graph cache."""
        result = {
            "table_size": {},
            "cache_info": {},
        }
        cursor = self.sqlite_connection.cursor()
        try:
            for table_name in self._TABLES:
                cursor.execute(f"SELECT COUNT() FROM {table_name!r}")
                result["table_size"][table_name] = cursor.fetchone()[0]
        finally:
            cursor.close()

        # We need to provide name explicitly as wrappers do not handle it correctly.
        for method, method_name in (
            (self.get_python_package_version_records, "get_python_package_version_records"),
            (self.get_depends_on, "get_depends_on"),
            (self.get_python_package_version_uid_record, "get_python_package_version_uid_record"),
            (self.get_python_package_version_entity_uid_record, "get_python_package_version_entity_uid_record"),
        ):
            result["cache_info"][method_name] = dict(method.cache_info()._asdict())

        return result

    def __del__(self):
        """Make sure the sqlite database gets written to disk."""
        self.sqlite_connection.close()

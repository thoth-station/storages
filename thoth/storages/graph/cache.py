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
import functools
from sqlite3 import dbapi2 as sqlite
from typing import Tuple
from typing import List
from typing import Optional
from typing import Union

import attr

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import create_database
from sqlalchemy_utils.functions import database_exists

from .sql_base import SQLBase
from .models_cache import CacheBase as Base
from .models_cache import DependsOn
from .models_cache import PythonPackageVersion
from .models_cache import PythonPackageVersionEntity

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
        if not args[0].is_inserts_enabled():
            return None

        return func(*args, **kwargs)

    return wrapper


def _get_python_package_version_filter_kwargs(
    package_name: str,
    package_version: Union[str, None],
    index_url: Union[str, None],
    *,
    os_name: Union[str, None],
    os_version: Union[str, None],
    python_version: Union[str, None],
) -> dict:
    """Get filter kwargs to query PythonPackageVersion records."""
    filter_kwargs = {"package_name": package_name}
    if package_version is not None:
        filter_kwargs["package_version"] = package_version
    if index_url is not None:
        filter_kwargs["index_url"] = index_url
    if os_name is not None:
        filter_kwargs["os_name"] = os_name
    if os_version is not None:
        filter_kwargs["os_version"] = os_version
    if python_version is not None:
        filter_kwargs["python_version"] = python_version

    return filter_kwargs


@attr.s()  # Do not use slots here as methodtools will fail.
class GraphCache(SQLBase):
    """A Dgraph database cache to speed up resolution of popular packages and packages with overlapping dependencies."""

    # This is a default graph cache - using in-memory. In a deployment we point to a path on disk.
    DEFAULT_CACHE_PATH = ":memory:"
    ENV_CACHE_PATH = "THOTH_STORAGES_GRAPH_CACHE"
    _DECLARATIVE_BASE = Base

    sqlite_cache_stats = attr.ib(type=dict)
    cache = attr.ib(type=str, default=None, kw_only=True)

    @sqlite_cache_stats.default
    def _sqlite_cache_stats_default(self):
        return {
            "get_python_package_version_records": dict.fromkeys(("misses", "hits"), 0),
            "get_depends_on": dict.fromkeys(("misses", "hits"), 0),
        }

    @staticmethod
    def is_enabled():
        """Check if this cache is enabled."""
        return not bool(int(os.getenv("THOTH_STORAGES_GRAPH_CACHE_DISABLED", 0)))

    @staticmethod
    def is_inserts_enabled():
        """Check if inserts to this cache are enabled."""
        return not bool(int(os.getenv("THOTH_STORAGES_GRAPH_CACHE_INSERTS_DISABLED", 1)))

    @classmethod
    def load(cls, cache: str = None) -> "GraphCache":
        """Prepare graph cache by loading an already existing one or a new one."""
        if not cache:
            cache = os.getenv(cls.ENV_CACHE_PATH, cls.DEFAULT_CACHE_PATH)

        if cache == ":memory:":
            cache = "sqlite://"
        else:
            cache = f"sqlite:///{cache if cache.startswith('/') else os.path.join(os.getcwd(), cache)}"

        instance = cls(cache=cache)
        instance.connect()

        if instance.is_enabled():
            instance.initialize_schema()

            if cache != "sqlite://":
                _LOGGER.info("Using database cache from %r", cache)
            else:
                _LOGGER.info("Using in-memory database cache")
        else:
            _LOGGER.info("Database cache is disabled")

        if not instance.is_inserts_enabled():
            _LOGGER.info(
                "Inserts into database cache are disabled, cache will be used only for reading pre-cached data"
            )

        return instance

    def connect(self):
        """Connect to the database."""
        if self.is_connected():
            raise ValueError("Cannot connect, the adapter is already connected")

        echo = bool(int(os.getenv("THOTH_STORAGES_DEBUG_QUERIES", 0)))
        # self._engine = create_engine(f"sqlite+pysqlite:///{self.cache}", echo=echo, module=sqlite)
        self._engine = create_engine(self.cache, echo=echo, module=sqlite)
        self._session = sessionmaker(bind=self._engine)()

    def initialize_schema(self):
        """Initialize schema of database."""
        if not self.is_connected():
            raise ValueError("Cannot initialize schema: the adapter is not connected yet")

        if not database_exists(self._engine.url):
            create_database(self._engine.url)

        self._DECLARATIVE_BASE.metadata.create_all(self._engine)

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
    ) -> Optional[List[Tuple[str, str]]]:
        """Retrieve dependencies for the given packages."""
        filter_kwargs = _get_python_package_version_filter_kwargs(
            package_name=package_name,
            package_version=package_version,
            index_url=index_url,
            os_name=os_name,
            os_version=os_version,
            python_version=python_version,
        )

        dependencies = (
            self._session.query(PythonPackageVersion)
            .filter_by(**filter_kwargs)
            .join(DependsOn)
            .join(PythonPackageVersionEntity)
            .with_entities(PythonPackageVersionEntity.package_name, PythonPackageVersionEntity.package_version)
            .all()
        )

        if not dependencies:
            # No record in the cache - for packages which do not depend on anything, we have (None, None) record.
            self.sqlite_cache_stats["get_depends_on"]["misses"] += 1
            return None

        result = []
        for dependency_name, dependency_version in dependencies:
            if dependency_name is not None and dependency_version is not None:
                result.append((dependency_name, dependency_version))

        self.sqlite_cache_stats["get_depends_on"]["hits"] += 1
        return result

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
        filter_kwargs = _get_python_package_version_filter_kwargs(
            package_name=package_name,
            package_version=package_version,
            index_url=index_url,
            os_name=os_name,
            os_version=os_version,
            python_version=python_version,
        )

        result = (
            self._session.query(
                PythonPackageVersion.package_name,
                PythonPackageVersion.package_version,
                PythonPackageVersion.index_url,
                PythonPackageVersion.os_name,
                PythonPackageVersion.os_version,
                PythonPackageVersion.python_version,
            )
            .filter_by(**filter_kwargs)
            .all()
        )

        if result:
            self.sqlite_cache_stats["get_python_package_version_records"]["hits"] += 1
            return [
                {
                    "package_name": item[0],
                    "package_version": item[1],
                    "index_url": item[2],
                    "os_name": item[3],
                    "os_version": item[4],
                    "python_version": item[5],
                }
                for item in result
            ]

        self.sqlite_cache_stats["get_python_package_version_records"]["misses"] += 1
        return None

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
        dependency_name: Union[str, None],
        dependency_version: Union[str, None],
    ) -> None:
        """Add a new entry of depends on for a Python package."""
        if (
            dependency_name is None
            and dependency_version is not None
            or dependency_name is not None
            and dependency_version is None
        ):
            raise ValueError(f"Integrity error - cannot insert {dependency_name} in version {dependency_version}")

        try:
            with self._session.begin(subtransactions=True):
                python_package_version, _ = PythonPackageVersion.get_or_create(
                    self._session,
                    package_name=package_name,
                    package_version=package_version,
                    index_url=index_url,
                    os_name=os_name,
                    os_version=os_version,
                    python_version=python_version,
                )
                entity, _ = PythonPackageVersionEntity.get_or_create(
                    self._session, package_name=dependency_name, package_version=dependency_version
                )
                DependsOn.get_or_create(self._session, entity_id=entity.id, version_id=python_package_version.id)
        except Exception:
            self._session.rollback()
            raise
        else:
            self._session.commit()

    def stats(self) -> dict:
        """Get statistics for the graph cache."""
        result = {"table_size": {}}

        if not self.is_enabled():
            return result

        for table_name in self._engine.table_names():
            table_object = self._DECLARATIVE_BASE.metadata.tables.get(table_name)
            result["table_size"][table_name] = self._session.query(table_object).count()

        result["sqlite_cache_info"] = self.sqlite_cache_stats
        return result

    def clear_in_memory_cache(self) -> None:
        """Clear in-memory cache."""
        for method in (self.get_python_package_version_records, self.get_depends_on):
            method.cache_clear()

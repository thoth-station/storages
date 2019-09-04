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

"""SQL database based model."""

import os
import attr

from sqlalchemy import create_engine
from sqlalchemy_utils.functions import create_database
from sqlalchemy_utils.functions import database_exists

from .sql_models import Base
from .sql_models import PythonPackageVersion
from .sql_models import PythonPackageVersionEntity

from ..base import StorageBase
from ..solvers import SolverResultsStore


@attr.s(slots=True)
class GraphDatabase(StorageBase):
    _engine = attr.ib(default=None)
    # cache = attr.ib(type=GraphCache, default=attr.Factory(GraphCache.load), kw_only=True)

    @staticmethod
    def construct_connection_string() -> str:
        """Construct a connection string needed to connect to database."""
        return f"postgresql+psycopg2://" \
            f"{os.getenv('POSTGRES_DB_USER', 'postgres')}:{os.getenv('POSTGRES_DB_PASS', 'postgres')}" \
            f"@{os.getenv('POSTGRES_SERVICE_HOST', 'localhost')}:{os.getenv('POSTGRES_SERVICE_PORT', 5432)}" \
            f"/{os.getenv('POSTGRES_DB_NAME', 'thoth')}"

    def connect(self):
        if self.is_connected():
            raise ValueError("Cannot connect, the adapter is already connected")

        self._engine = create_engine(self.construct_connection_string())

    def __del__(self) -> None:
        """Disconnect properly on object destruction."""
        if self.is_connected():
            self.disconnect()

    def is_connected(self) -> bool:
        """Check if we are connected to a remote Dgraph instance."""
        return self._engine is not None

    def disconnect(self):
        """Disconnect from the connected database."""
        if not self.is_connected():
            raise ValueError("Cannot disconnect, the adapter is not connected")

        del self._engine
        self._engine = None

    def initialize_schema(self) -> None:
        """Initialize schema in the database."""
        if not self.is_connected():
            raise ValueError("Cannot initialize schema: the adapter is not connected yet")

        if not database_exists(self._engine.url):
            create_database(self._engine.url)

        Base.metadata.create_all(self._engine)

    def drop_all(self) -> None:
        """Drop all content stored in the database."""
        if not self.is_connected():
            raise ValueError("Cannot initialize schema: the adapter is not connected yet")

        Base.metadata.drop_all(self._engine)

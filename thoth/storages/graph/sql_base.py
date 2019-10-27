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

"""A base class for implementing SQL based databases."""

import attr
import abc

from sqlalchemy.engine import Engine

from ..exceptions import NotConnected


@attr.s(slots=True)
class SQLBase:
    """A base class for implementing SQL based databases using SQLAlchemy."""

    _engine = attr.ib(type=Engine, default=None)
    _session = attr.ib(default=None)

    _DECLARATIVE_BASE = None

    @abc.abstractmethod
    def connect(self):
        """Connect to the database."""

    def is_connected(self):
        """Check if the database is connected."""
        return self._engine is not None

    def disconnect(self):
        """Disconnect from the connected database."""
        if not self.is_connected():
            raise NotConnected("Cannot disconnect, the adapter is not connected")

        if self._session is not None:
            self._session = None

        # self._engine.dispose()
        self._engine = None

    @abc.abstractmethod
    def initialize_schema(self) -> None:
        """Initialize schema in the database."""

    def drop_all(self) -> None:
        """Drop all content stored in the database."""
        if not self.is_connected():
            raise NotConnected("Cannot initialize schema: the adapter is not connected yet")

        self._DECLARATIVE_BASE.metadata.drop_all(self._engine)

    def __del__(self) -> None:
        """Disconnect properly on object destruction."""
        if self.is_connected():
            self.disconnect()

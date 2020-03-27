#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2019, 2020 Fridolin Pokorny
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

"""A base and utilities for implementing SQLAlchemy based models."""

import logging
import datetime
from itertools import combinations
from typing import List

from sqlalchemy import Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm import ColumnProperty
from sqlalchemy.exc import IntegrityError


Base = declarative_base()


_LOGGER = logging.getLogger(__name__)


class BaseExtension:
    """Extend base class with additional functionality."""

    @classmethod
    def get_or_create(cls, session, **kwargs):
        """Query for the given entity, create if it does not exist yet."""
        instance = session.query(cls).filter_by(**kwargs).first()
        if instance:
            return instance, True
        else:
            try:
                session.begin_nested()
                instance = cls(**kwargs)
                session.add(instance)
                session.commit()
                return instance, False
            except IntegrityError as exc:
                session.rollback()
                _LOGGER.warning(
                    "Integrity error on creating a new record; this can be due to "
                    "concurrent writes to database, recovering (attributes: %r): %s",
                    kwargs,
                    str(exc),
                )
                return session.query(cls).filter_by(**kwargs).one(), True

    @classmethod
    def attribute_names(cls):
        """Get names of attributes for the given model declaration."""
        return [prop.key for prop in class_mapper(cls).iterate_properties if isinstance(prop, ColumnProperty)]

    def to_dict(self, without_id: bool = True) -> dict:
        """Convert model to a dictionary representation keeping just rows as attributes."""
        result = {}
        for column in self.__table__.columns:
            if without_id and column.name == "id":
                continue

            if getattr(self, column.name) is None:
                result[column.name] = None
            else:
                value = getattr(self, column.name)
                if isinstance(value, (datetime.datetime, datetime.date)):
                    result[column.name] = str(value)
                else:
                    result[column.name] = value

        return result


def get_python_package_version_index_combinations() -> List[Index]:
    """Create index for all possible combinations which we can query."""
    result = []
    _columns_to_variate = (
        "os_name",
        "os_version",
        "python_version",
    )
    for i in range(0, len(_columns_to_variate) + 1):
        for j, variation in enumerate(combinations(_columns_to_variate, i)):
            result.append(
                Index(
                    f"python_package_version_index_idx_{i}{j}",
                    "package_name",
                    "package_version",
                    *variation,
                )
            )

    return result

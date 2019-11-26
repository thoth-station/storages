#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2019 Francesco Murdaca
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

"""Utilities for SQLAlchemy query results."""

import logging

from typing import List, Dict, Any, Optional, Union, Tuple

_LOGGER = logging.getLogger(__name__)


class PythonQueryResult:
    """Class for managing queries' results for Python Packages."""

    def __init__(
        self,
        result: Union[List, Dict[str, Any]],
        count: Optional[int] = None
    ):
        """Query result initialization."""
        self._result = result
        self._count = count

    @property
    def result(self):
        """Query result."""
        return self._result

    @property
    def count(self):
        """Query count result."""
        return self._count

    def count_per_package(self) -> Dict[Tuple[str, str, str], int]:
        """Query result count per package."""
        query_result = {}
        for item in self._result:
            if (item[0], item[1], item[2]) not in query_result:
                query_result[(item[0], item[1], item[2])] = item[3]
            else:
                query_result[(item[0], item[1], item[2])] += item[3]

        return query_result

    def count_per_index(self, index_url) -> Dict[str, Dict[Tuple[str, str], int]]:
        """Query result count per index."""
        query_result = {
            index_url: {}
            }
        for item in self._result:
            if item[2] == index_url:
                if (item[0], item[1]) not in query_result[index_url].keys():
                    query_result[index_url][(item[0], item[1])] = item[3]
                else:
                    query_result[index_url][(item[0], item[1])] += item[3]

        return query_result

    def count_per_version(self) -> Dict[str, Dict[str, int]]:
        """Query result count per version."""
        query_result = {}
        for item in self._result:
            if item[1] not in query_result:
                query_result[item[1]] = {}
                query_result[item[1]][item[2]] = item[3]
            else:
                if item[2] not in query_result[item[1]]:
                    query_result[item[1]][item[2]] = item[3]
                else:
                    query_result[item[1]][item[2]] += item[3]

        return query_result

    def group_by_package_name(self) -> Dict[str, List[Tuple[str, str]]]:
        """Query result group by package name."""
        query_result = {}
        for item in self._result:
            if item[0] not in query_result:
                query_result[item[0]] = []
            query_result[item[0]].append((item[1], item[2]))

        return query_result

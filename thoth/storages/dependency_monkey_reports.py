#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2018, 2019, 2020 Fridolin Pokorny
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

"""Adapter for persisting reports from Dependency Monkey runs."""

from .result_base import ResultStorageBase


class DependencyMonkeyReportsStore(ResultStorageBase):
    """Adapter for persisting reports from Dependency Monkey runs."""

    RESULT_TYPE = "dependency-monkey-reports"

    def iterate_inspection_ids(self) -> str:
        """Iterate over all inspection ids that were run."""
        for _, report in self.iterate_results():
            # Yield inspections.
            yield from report["result"]["output"]

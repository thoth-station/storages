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

"""Adapter for storing solver results onto a persistence remote store."""

from datetime import date
from typing import Optional
from typing import Generator, TypedDict

from .result_base import ResultStorageBase


class _SolverInfo(TypedDict):
    os_name: str
    os_version: str
    python_version: str


class SolverResultsStore(ResultStorageBase):
    """Adapter for persisting solver results."""

    RESULT_TYPE = "solver"

    @staticmethod
    def get_solver_name_from_document_id(solver_document_id: str) -> str:
        """Retrieve solver name from solver's document id."""
        return solver_document_id.rsplit("-", maxsplit=2)[0]

    def get_document_listing(
        self,
        *,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        include_end_date: bool = False,
        only_requests: bool = False,
        solver_info: Optional[_SolverInfo] = None,
    ) -> Generator[str, None, None]:
        """Get listing of documents available in Ceph as a generator.

        Additional parameters can filter results. If start_date is supplied
        and no end_date is supplied explicitly, the current date is
        considered as end_date (inclusively).
        """
        if solver_info is None and start_date is not None:
            raise ValueError("Date filter can be used only when specific solvers are requested")
        if solver_info:
            _s = solver_info
            prefix_solver = f"-{_s['os_name']}-{_s['os_version']}-py{_s['python_version'].replace('.', '')}"

        if start_date is not None:
            for prefix_date in self._iter_dates_prefix_addition(
                start_date=start_date, end_date=end_date, include_end_date=include_end_date
            ):
                yield from self.ceph.get_document_listing(prefix_solver + prefix_date)
        elif solver_info is not None:
            yield from self.ceph.get_document_listing(prefix_solver)
        else:
            yield from self.ceph.get_document_listing()

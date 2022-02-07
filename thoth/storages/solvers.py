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
from typing import Generator

from .result_base import ResultStorageBase


class SolverResultsStore(ResultStorageBase):
    """Adapter for persisting solver results."""

    RESULT_TYPE = "solver"

    @staticmethod
    def get_solver_name_from_document_id(solver_document_id: str) -> str:
        """Retrieve solver name from solver's document id."""
        return solver_document_id.rsplit("-", maxsplit=2)[0]

    def get_document_listing(
        self,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        *,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        include_end_date: bool = False,
    ) -> Generator[str, None, None]:
        """Get listing of documents available in Ceph as a generator.

        Additional parameters can filter results. If start_date is supplied
        and no end_date is supplied explicitly, the current date is
        considered as end_date (inclusively).
        """
        if start_date:
            if os_name is None or os_version is None or python_version is None:
                raise ValueError("Date filter can be used only when specific solvers are requested")

            prefix = f"solver-{os_name}-{os_version}-py{python_version.replace('.', '')}"
            for prefix_addition in self._iter_dates_prefix_addition(
                prefix=prefix, start_date=start_date, end_date=end_date, include_end_date=include_end_date
            ):
                for document_id in self.ceph.get_document_listing(prefix_addition):
                    yield document_id
        else:
            if all(i is not None for i in (os_name, os_version, python_version)):
                prefix = f"solver-{os_name}-{os_version}-py{python_version.replace('.', '')}"
                for document_id in self.ceph.get_document_listing(prefix):
                    yield document_id
            elif all(i is None for i in (os_name, os_version, python_version)):
                for document_id in self.ceph.get_document_listing():
                    yield document_id
            else:
                raise ValueError("None or all parameters for os_name, os_version, python_version have to be supplied")

    def get_document_count(
        self,
        os_name: Optional[str] = None,
        os_version: Optional[str] = None,
        python_version: Optional[str] = None,
        *,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        include_end_date: bool = False,
    ) -> int:
        """Get number of documents present."""
        return sum(
            1
            for _ in self.get_document_listing(
                os_name=os_name,
                os_version=os_version,
                python_version=python_version,
                start_date=start_date,
                end_date=end_date,
                include_end_date=include_end_date,
            )
        )

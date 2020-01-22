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

"""Adapter for persisting Amun inspection results."""


import typing
from typing import List, Dict

from .result_base import ResultStorageBase
from .inspection_schema import INSPECTION_SCHEMA


class InspectionResultsStore(ResultStorageBase):
    """Adapter for persisting Amun inspection results."""

    RESULT_TYPE = "inspection"
    SCHEMA = INSPECTION_SCHEMA

    @classmethod
    def get_document_id(cls, document: dict) -> str:
        """Get id under which the given document will be stored."""
        return document["inspection_id"]

    def filter_document_ids(cls, inspection_identifiers: List[str]) -> Dict[str, List]:
        """Filter inspection document ids list according to the inspection identifiers selected.

        :param inspection_identifiers: list of identifier/s to filter inspection ids
        """
        inspection_document_ids = list(cls.get_document_listing())
        filtered_inspection_document_ids = dict((i, []) for i in inspection_identifiers)

        for sid in inspection_document_ids:
            inspection_filter = "-".join(sid.split("-")[1:(len(sid.split("-")) - 1)])

            if inspection_filter and inspection_filter in inspection_identifiers:
                filtered_inspection_document_ids[inspection_filter].append(sid)

        return filtered_inspection_document_ids

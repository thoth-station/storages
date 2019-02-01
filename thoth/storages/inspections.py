#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2018, 2019 Fridolin Pokorny
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

from .result_base import ResultStorageBase


class InspectionResultsStore(ResultStorageBase):
    """Adapter for persisting Amun inspection results."""

    RESULT_TYPE = "inspection"
    SCHEMA = None

    @classmethod
    def get_document_id(cls, document: dict) -> str:
        """Get id under which the given document will be stored."""
        return document["inspection_id"]

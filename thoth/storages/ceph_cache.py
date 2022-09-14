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

"""A base class for implementing caches based on Ceph."""

from datetime import datetime

from .exceptions import CacheMiss
from .exceptions import NotFoundError
from .result_base import ResultStorageBase


class CephCache(ResultStorageBase):
    """A base class implementing cache interface."""

    def retrieve_document_record(self, document_id: str) -> dict:
        """Check whether the given record exists in the cache for the requested document."""
        try:
            return self.retrieve_document(document_id)
        except NotFoundError as exc:
            raise CacheMiss(f"There was no record found in the cache for {document_id!r}") from exc

    def store_document_record(self, document_id: str, document: dict) -> str:
        """Store the given document record in the cache."""
        self.ceph.store_document(document, document_id)

    def retrieve_document_ttl(self, document_id: str) -> float:
        """Retrieve the TTL for a cached document."""
        # Verify if the document is present in the cache
        self.retrieve_document_record(document_id)

        # Uses UTC time to be environment agnostic (no timezone)
        time_lived = (
            datetime.now()
            - self.ceph.retrieve_document_attr(object_key=document_id, attr="LastModified").replace(
                tzinfo=datetime.timezone.utc
            )
        ).total_seconds()

        if time_lived <= 14400.0:
            return time_lived

        return 0.0

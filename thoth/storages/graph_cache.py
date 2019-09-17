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

"""Graph cache backup for incremental cache builds."""

import os
import logging

from .ceph import CephStore
from .exceptions import NotFoundError

_LOGGER = logging.getLogger(__name__)


class GraphCacheStore:
    """A graph cache store for storing and restoring graph cache."""

    _OBJECT_NAME = "graph_cache.sqlite3"

    def __init__(self, prefix: str = None):
        """Initialize graph cache store."""
        self.prefix = prefix or "{}/{}/{}".format(
            os.environ["THOTH_CEPH_BUCKET_PREFIX"], os.environ["THOTH_DEPLOYMENT_NAME"], "graph-cache"
        )
        self._ceph = CephStore(prefix=self.prefix)

    def connect(self) -> None:
        """Connect to the remote store."""
        self._ceph.connect()

    def retrieve(self, cache_file: str) -> None:
        """Retrieve a cache from remote Ceph."""
        _LOGGER.debug("Restoring %r from %r to %r", self._OBJECT_NAME, self.prefix, cache_file)
        with open(cache_file, "wb") as blob_file:
            blob_file.write(self._ceph.retrieve_blob(self._OBJECT_NAME))

    def store(self, cache_file: str) -> None:
        """Store the given cache onto remote Ceph."""
        _LOGGER.debug("Storing %r to %r, object name is %r", cache_file, self.prefix, self._OBJECT_NAME)
        try:
            with open(cache_file, "rb") as blob_file:
                self._ceph.store_blob(blob_file.read(), self._OBJECT_NAME)
        except FileNotFoundError as exc:
            raise NotFoundError(f"File {cache_file!r} was not found: {str(exc)}") from exc

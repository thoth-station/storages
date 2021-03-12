#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2019, 2020 Harshad Reddy Nalla, Fridolin Pokorny
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

"""Adapter for storing graph database backups."""

import logging
from typing import Tuple
from typing import List
import os
from datetime import datetime
import operator


from .result_base import ResultStorageBase

_LOGGER = logging.getLogger(__name__)


class GraphBackupStore(ResultStorageBase):
    """Adapter for storing graph database backups."""

    RESULT_TYPE = "graph-backup"

    # Keep 21 backups by default.
    GRAPH_BACKUP_STORE_ROTATE = int(os.getenv("GRAPH_BACKUP_STORE_ROTATE", 21))
    _BACKUP_FILE_DATETIME_FORMAT = "%y-%m-%d-%H-%M-%S"

    def _rotate_backups(self) -> None:
        """Rotate backups stored by deleting old once."""
        backup_files_maintained: List[Tuple[datetime, str]] = []

        # Perform a basic check for file name correctness.
        for backup_file in self.get_document_listing():
            if not backup_file.startswith("pg_dump-"):
                _LOGGER.error(
                    "Unknown backup file name %r - the file name does not start with "
                    "'pg_dump-' prefix, skipping maintaining this file",
                    backup_file,
                )
                continue

            try:
                datetime_obj = datetime.strptime(backup_file[len("pg_dump-") :], self._BACKUP_FILE_DATETIME_FORMAT)
            except Exception as exc:
                _LOGGER.exception(
                    "Failed to parse datetime from the backup file name %r, skipping maintaining this file: %s",
                    backup_file,
                    str(exc),
                )
                continue

            backup_files_maintained.append((datetime_obj, backup_file))

        backup_files_maintained.sort(key=operator.itemgetter(0), reverse=True)
        for backup_file in backup_files_maintained[self.GRAPH_BACKUP_STORE_ROTATE :]:
            _LOGGER.info(
                "Removing backup file %r based on rotation configuration (keeping %d dumps)",
                backup_file[1],
                self.GRAPH_BACKUP_STORE_ROTATE,
            )
            self.ceph.delete(backup_file[1])

    def store_dump(self, dump_file_path: str) -> str:
        """Store the given dump, maintain a fixed set of dumps ."""
        backup_file_name = f"pg_dump-{datetime.utcnow().strftime(self._BACKUP_FILE_DATETIME_FORMAT)}"
        self.store_file(dump_file_path, backup_file_name)
        self._rotate_backups()
        return backup_file_name

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

import os
import logging
from typing import Any
from typing import Dict
from typing import Generator
from typing import Optional

from .ceph import CephStore

_LOGGER = logging.getLogger(__name__)


def _get_inspection_prefix(inspection_id: Optional[str] = None) -> str:
    """Get prefix where inspections store data.

    This configuration matches Amun configmap.
    """
    bucket_prefix = os.environ["THOTH_CEPH_BUCKET_PREFIX"]
    deployment_name = os.environ["THOTH_DEPLOYMENT_NAME"]

    if inspection_id is None:
        return f"{bucket_prefix}/{deployment_name}/inspections"

    return f"{bucket_prefix}/{deployment_name}/inspections/{inspection_id}"


class _InspectionBase:
    """A base class for inspection builds and results."""

    __slots__ = ["ceph", "inspection_id"]

    def connect(self) -> None:
        """Connect this adapter to Ceph."""
        self.ceph.connect()

    def is_connected(self) -> bool:
        """Check if this adapter is connected."""
        return self.ceph.is_connected()

    def check_connection(self) -> None:
        """Check connection of this adapter."""
        return self.ceph.check_connection()


class InspectionBuildsStore(_InspectionBase):
    """An adapter for manipulating with inspection builds."""

    def __init__(self, inspection_id: str) -> None:
        """Constructor."""
        prefix = f"{_get_inspection_prefix(inspection_id)}/build/"
        self.ceph = CephStore(prefix=prefix)
        self.inspection_id = inspection_id

    def retrieve_dockerfile(self) -> str:
        """Retrieve Dockerfile used during the build."""
        return self.ceph.retrieve_blob("Dockerfile").decode()

    def retrieve_log(self) -> str:
        """Retrieve logs (stdout together with stderr) reported during the build."""
        return self.ceph.retrieve_blob("log").decode()

    def retrieve_specification(self) -> Dict[str, Any]:
        """Retrieve specification used for the build, captures also run specification."""
        return self.ceph.retrieve_document("specification")


class InspectionResultsStore(_InspectionBase):
    """An adapter for manipulating with inspection results."""

    def __init__(self, inspection_id: str) -> None:
        """Constructor."""
        prefix = f"{_get_inspection_prefix(inspection_id)}/results/"
        self.ceph = CephStore(prefix=prefix)
        self.ceph.connect()
        self.inspection_id = inspection_id

    @classmethod
    def get_document_id(cls, document: Dict[str, Any]) -> str:
        """Get id under which the given document will be stored."""
        return document["inspection_id"]

    def get_results_count(self) -> int:
        """Obtain number of results produced during inspection run."""
        items = []
        items_set = set()
        for object_key in self.ceph.get_document_listing():
            item, _ = object_key.split("/", maxsplit=1)
            item_int = int(item)
            if item_int not in items_set:
                items_set.add(item_int)
                items.append(item_int)

        del items_set

        if len(items) == 0:
            return 0

        items.sort(reverse=False)

        if len(items) != items[-1] + 1:
            _LOGGER.warning("Some of the inspection results are missing")

        return items[-1] + 1

    def retrieve_hwinfo(self, item: int) -> Dict[str, Any]:
        """Obtain hardware information for the given inspection run."""
        return self.ceph.retrieve_document(f"{item}/hwinfo")

    def retrieve_log(self, item: int) -> str:
        """Obtain log for the given inspection run."""
        return self.ceph.retrieve_blob(f"{item}/log").decode()

    def retrieve_result(self, item: int) -> Dict[str, Any]:
        """Obtain the actual result for the given inspection run."""
        return self.ceph.retrieve_document(f"{item}/result")

    def iter_inspection_results(self) -> Generator[Dict[str, Any], None, None]:
        """Iterate over inspection results."""
        for item in range(self.get_results_count()):
            yield self.retrieve_result(item)


class InspectionStore:
    """Adapter for manipulating with Amun inspections."""

    __slots__ = ["build", "results", "inspection_id"]

    def __init__(self, inspection_id: str) -> None:
        """A representation of an inspection."""
        self.inspection_id = inspection_id
        self.build = InspectionBuildsStore(inspection_id)
        self.results = InspectionResultsStore(inspection_id)

    def retrieve_specification(self) -> Dict[str, Any]:
        """Retrieve specification used for this inspection."""
        return self.build.retrieve_specification()

    def connect(self) -> None:
        """Connect this adapter."""
        self.build.connect()
        self.results.connect()

    def is_connected(self) -> bool:
        """Check if this adapter is connected."""
        return self.build.is_connected() and self.results.is_connected()

    def check_connection(self):
        """Check connections of this adapter."""
        self.build.check_connection()
        self.results.check_connection()

    def exists(self) -> bool:
        """Check if the given inspection exists."""
        # Specification is stored as one of the very first inspection results.
        return self.build.ceph.document_exists("specification")

    @classmethod
    def iter_inspections(cls) -> Generator[str, None, None]:
        """Iterate over inspection ids stored."""
        ceph = CephStore(prefix=_get_inspection_prefix())
        ceph.connect()

        last_id = None
        for item in ceph.get_document_listing():
            inspection_id = item.split("/", maxsplit=1)[0]
            if last_id == inspection_id:
                # Return only unique inspection ids, discard any results placed under the given prefix.
                continue

            last_id = inspection_id
            yield inspection_id

    @classmethod
    def get_inspection_count(cls) -> int:
        """Get number of inspection stored."""
        return sum(1 for _ in cls.iter_inspections())

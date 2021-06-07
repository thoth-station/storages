#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2021 Fridolin Pokorny
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

"""Adapter for accessing Argo Workflow logs."""

import os
from typing import Optional

from thoth.storages.base import StorageBase
from thoth.storages.ceph import CephStore
from thoth.storages.exceptions import MultipleFoundError
from thoth.storages.exceptions import NotFoundError


class WorkflowLogsStore(StorageBase):
    """Access logs stored by Argo Workflows."""

    def __init__(
        self,
        deployment_name: Optional[str] = None,
        *,
        host: Optional[str] = None,
        key_id: Optional[str] = None,
        secret_key: Optional[str] = None,
        bucket: Optional[str] = None,
        region: Optional[str] = None,
        prefix: Optional[str] = None,
    ):
        """Initialize the adapter."""
        self.deployment_name = deployment_name or os.environ["THOTH_DEPLOYMENT_NAME"]
        self.prefix = "{}/{}/argo/artifacts".format(
            prefix or os.environ["THOTH_CEPH_BUCKET_PREFIX"],
            self.deployment_name,
        )
        self.ceph = CephStore(
            self.prefix, host=host, key_id=key_id, secret_key=secret_key, bucket=bucket, region=region
        )

    def get_log(self, workflow_id: str) -> str:
        """Obtain log from the given workflow."""
        results = list(self.ceph.get_document_listing(workflow_id))
        if len(results) > 1:
            raise MultipleFoundError(
                f"Multiple results match the given workflow_id ({workflow_id!r}) provided: {results!r}"
            )

        # Make sure users do not use workflow id prefix.
        if not results or not results[0].startswith(f"{workflow_id}/"):
            raise NotFoundError(f"No log entry found for {workflow_id!r}")

        return self.ceph.retrieve_blob(results[0]).decode()

    def connect(self) -> None:
        """Connect to Ceph."""
        self.ceph.connect()

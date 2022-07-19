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

"""Adapter for storing build logs."""

import hashlib
import os
import typing

from .s3 import S3store
from .base import StorageBase


class BuildLogsStore(StorageBase):
    """Adapter for storing build logs."""

    RESULT_TYPE = "buildlogs"

    def __init__(
        self,
        deployment_name=None,
        *,
        bucket_prefix: str = None,
        host: str = None,
        key_id: str = None,
        secret_key: str = None,
        bucket: str = None,
        region: str = None,
    ):
        """Initialize adapter for storing build logs.

        Parameters not explicitly provided will be picked from env variables.
        """
        self.deployment_name = deployment_name or os.environ["THOTH_DEPLOYMENT_NAME"]
        self.prefix = "{}/{}/{}/".format(
            bucket_prefix or os.environ["THOTH_CEPH_BUCKET_PREFIX"], self.deployment_name, self.RESULT_TYPE
        )
        self.s3 = S3store(self.prefix, host=host, key_id=key_id, secret_key=secret_key, bucket=bucket, region=region)

    def is_connected(self) -> bool:
        """Check if the given database adapter is in connected state."""
        return self.s3.is_connected()

    def connect(self) -> None:
        """Connect the given storage adapter."""
        self.s3.connect()

    def store_document(self, document: dict) -> str:
        """Store the given document in Ceph."""
        blob = self.s3.dict2blob(document)
        document_id = "buildlog-" + hashlib.sha256(blob).hexdigest()
        self.s3.store_blob(blob, document_id)
        return document_id

    def retrieve_document(self, document_id: str) -> dict:
        """Retrieve a document from Ceph by its id."""
        return self.s3.retrieve_document(document_id)

    def iterate_results(self) -> typing.Generator[tuple, None, None]:
        """Iterate over results available in the Ceph."""
        return self.s3.iterate_results()

    def get_document_listing(self) -> typing.Generator[str, None, None]:
        """Get listing of documents stored on the Ceph."""
        return self.s3.get_document_listing()

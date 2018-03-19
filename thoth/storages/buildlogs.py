"""Adapter for storing build logs."""

import hashlib
import os
import typing

from .ceph import CephStore
from .base import StorageBase


class BuildLogsStore(StorageBase):
    RESULT_TYPE = 'buildlogs'

    def __init__(self, deployment_name=None, *,
                 host: str=None, key_id: str=None, secret_key: str=None, bucket: str=None, region: str=None):
        self.deployment_name = deployment_name or os.environ['THOTH_DEPLOYMENT_NAME']
        self.prefix = "{}/{}".format(self.deployment_name, self.RESULT_TYPE)
        self.ceph = CephStore(
            self.prefix,
            host=host,
            key_id=key_id,
            secret_key=secret_key,
            bucket=bucket,
            region=region
        )

    def is_connected(self) -> bool:
        """Check if the given database adapter is in connected state."""
        return self.ceph is not None

    def connect(self) -> None:
        """Connect the given storage adapter."""
        self.ceph.connect()

    def store_document(self, document: dict) -> str:
        """Store the given document in Ceph."""
        blob = self.ceph.dict2blob(document)
        document_id = hashlib.sha256(blob).hexdigest()
        self.ceph.store_blob(blob, document_id)
        return document_id

    def retrieve_document(self, document_id: str) -> dict:
        """Retrieve a document from Ceph by its id."""
        return self.ceph.retrieve_document(document_id)

    def iterate_results(self) -> typing.Generator[tuple, None, None]:
        """Iterate over results available in the Ceph."""
        return self.ceph.iterate_results()

    def get_document_listing(self) -> typing.Generator[str, None, None]:
        """Get listing of documents stored on the Ceph."""
        return self.ceph.get_document_listing()

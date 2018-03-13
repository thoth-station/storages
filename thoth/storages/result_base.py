"""Adapter for storing analysis results onto a persistence remote store."""

import os
import typing

from .base import StorageBase
from .ceph import CephStore


class ResultStorageBase(StorageBase):
    """Adapter base for storing results."""

    PATH_ENV_VAR = None

    def __init__(self, *, host: str=None, key_id: str=None, secret_key: str=None, bucket: str=None,
                 path: str=None, region: str=None):
        assert self.PATH_ENV_VAR is not None, "Make sure you define PATH_ENV_VAR in derived classes " \
                                              "to distinguish between adapter type instances."
        path = path or os.getenv(self.PATH_ENV_VAR)
        self.ceph = CephStore(
            host=host,
            key_id=key_id,
            secret_key=secret_key,
            bucket=bucket,
            path=path,
            region=region
        )

    def is_connected(self) -> bool:
        """Check if the given database adapter is in connected state."""
        return self.ceph.is_connected()

    def connect(self) -> None:
        """Connect the given storage adapter."""
        self.ceph.connect()

    def get_document_listing(self) -> typing.Generator[str, None, None]:
        yield from self.ceph.get_document_listing()

    def store_document(self, document: dict) -> dict:
        document_id = document['metadata']['hostname']
        return self.ceph.store_document(document, document_id)

    def retrieve_document(self, document_id: str) -> dict:
        return self.ceph.retrieve_document(document_id)

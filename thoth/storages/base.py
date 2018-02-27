"""A base class for implementing storage adapters."""

import abc


class StorageBase(metaclass=abc.ABCMeta):
    """A base class for implementing storage adapters."""

    def is_connected(self) -> bool:
        """Check if the given database adapter is in connected state."""

    def connect(self) -> None:
        """Connect the given storage adapter."""

"""Exceptions for storage adapters and storage handling."""


class ThothStorageException(Exception):
    """A base exception for Thoth storage exception hierarchy."""


class NotFoundError(ThothStorageException):
    """Raised if the given artifact cannot be found."""


class SchemaError(ThothStorageException):
    """Raised if trying to store document with invalid schema."""

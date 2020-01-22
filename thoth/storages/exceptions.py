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

"""Exceptions for storage adapters and storage handling."""


class ThothStorageException(Exception):
    """A base exception for Thoth storage exception hierarchy."""


class NotFoundError(ThothStorageException):
    """Raised if the given artifact cannot be found."""


class SchemaError(ThothStorageException):
    """Raised if trying to store document with invalid schema."""


class CacheMiss(ThothStorageException):
    """Raised if the requested document was not found in the cache."""


class NotConnected(ThothStorageException):
    """Raised if there was no connection established when communicating with a storage."""


class AlreadyConnected(ThothStorageException):
    """Raised if trying to connect on already connected adapter."""


class DatabaseNotInitialized(ThothStorageException):
    """Raised if trying to perform operations on un-initialized database schema."""


class SolverNameParseError(ThothStorageException):
    """Raised if unable to determine solver information out of solver name run."""


class MultipleFoundError(ThothStorageException):
    """Raised if there are multiple entities in the graph database when querying for a single one."""


class PythonIndexNotRegistered(ThothStorageException):
    """Raised if an attempt to insert a Python package with an index not being registered to the system."""


class UnboundModel(ThothStorageException):
    """Raised if there are done operations on models which do not link to objects stored inside database."""


class PerformanceIndicatorNotRegistered(ThothStorageException):
    """Raised if a performance indicator model which is about to be synced was not found."""


class PythonIndexNotProvided(ThothStorageException):
    """Raised if an attempt to insert a package without an index."""


class SolverNotRun(ThothStorageException):
    """Raised if an attempt to insert a package which was not solved."""


class PythonPackageMetadataAttributeMissing(ThothStorageException):
    """Raised if a Python Package metadata attribute is not included in the class attributes."""


class DistutilsKeyNotKnown(ThothStorageException):
    """Raised if a distutils in Python Package metadata is not known."""


class SortTypeQueryError(ThothStorageException):
    """Raised if a sort key used in a query is not known."""


class NoDocumentIdError(ThothStorageException):
    """Raised if document id is not found in the document."""


class CudaVersionDoesNotMatch(ThothStorageException):
    """Raised if the cuda versions from txt file and nvcc command is different."""

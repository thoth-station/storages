#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2019 Fridolin Pokorny
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

"""Models for cache."""

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import UniqueConstraint
from sqlalchemy import Index

from .models_base import BaseExtension
from .models_base import get_python_package_version_index_combinations

CacheBase = declarative_base()


class PythonPackageVersion(CacheBase, BaseExtension):
    """A Python package version in the given environment."""

    __tablename__ = "python_package_version"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    package_name = Column(String(256), nullable=False)
    package_version = Column(String(256), nullable=False)
    index_url = Column(String(256), nullable=False)
    os_name = Column(String(256), nullable=False)
    os_version = Column(String(256), nullable=False)
    python_version = Column(String(256), nullable=False)

    entities = relationship("DependsOn", back_populates="version")

    __table_args__ = tuple(
        get_python_package_version_index_combinations()
        + [
            UniqueConstraint("package_name", "package_version", "index_url", "os_name", "os_version", "python_version"),
            Index("python_package_version_idx", "package_name", "package_version", "index_url"),
        ]
    )


class PythonPackageVersionEntity(CacheBase, BaseExtension):
    """A Python package version entity."""

    __tablename__ = "python_package_version_entity"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    package_name = Column(String(256), nullable=True)
    package_version = Column(String(256), nullable=True)

    versions = relationship("DependsOn", back_populates="entity")

    __table_args__ = (
        UniqueConstraint("package_name", "package_version"),
        Index("python_package_version_entity_idx", "package_name", "package_version", unique=True),
    )


class DependsOn(CacheBase, BaseExtension):
    """Dependency relationship capturing."""

    __tablename__ = "depends_on"

    entity_id = Column(Integer, ForeignKey("python_package_version_entity.id"), primary_key=True)
    version_id = Column(Integer, ForeignKey("python_package_version.id"), primary_key=True)
    version_range = Column(String(128))

    entity = relationship("PythonPackageVersionEntity", back_populates="versions")
    version = relationship("PythonPackageVersion", back_populates="entities")

    __table_args__ = (
        UniqueConstraint("entity_id", "version_id"),
        Index("depends_on_idx", "entity_id", "version_id", unique=True),
    )

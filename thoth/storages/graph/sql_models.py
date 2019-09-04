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

"""Models for SQL based database."""

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import UniqueConstraint
from sqlalchemy import Index

from .models_base import BaseExtension
from .models_base import get_python_package_version_index_combinations

Base = declarative_base()


class PythonPackageVersion(Base, BaseExtension):

    __tablename__ = "python_package_version"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    package_name = Column(String(256), nullable=False)
    package_version = Column(String(256), nullable=False)
    # Nullable if we have unparseable entries.
    index_url = Column(String(256), nullable=True)
    os_name = Column(String(256), nullable=False)
    os_version = Column(String(256), nullable=False)
    python_version = Column(String(256), nullable=False)

    entities = relationship("DependsOn", back_populates="version")
    solvers = relationship("Solved", back_populates="version")

    __table_args__ = tuple(
        get_python_package_version_index_combinations() + [
            UniqueConstraint(
                "package_name",
                "package_version",
                "index_url",
                "os_name",
                "os_version",
                "python_version",
            ),
            Index(
                "python_package_version_idx",
                "package_name",
                "package_version",
                "index_url",
            )
        ],
    )


class Solved(Base, BaseExtension):
    """A solver solved a package-version."""

    __tablename__ = "solved"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    datetime = Column(DateTime(timezone=False), nullable=False)
    document_id = Column(String(128), nullable=False)
    duration = Column(Integer)

    solver_error = Column(Boolean, default=False, nullable=False)
    solver_error_unparseable = Column(Boolean, default=False, nullable=False)
    solver_error_unsolvable = Column(Boolean, default=False, nullable=False)
    is_provided = Column(Boolean)

    ecosystem_solver_id = Column(Integer, ForeignKey('ecosystem_solver.id'), primary_key=True)
    version_id = Column(Integer, ForeignKey('python_package_version.id'), primary_key=True)

    ecosystem_solver = relationship("EcosystemSolver", back_populates="versions")
    version = relationship("PythonPackageVersion", back_populates="solvers")

    __table_args__ = (
        UniqueConstraint(
            "ecosystem_solver_id",
            "version_id",
            "document_id",
        ),
    )


class PythonPackageVersionEntity(Base, BaseExtension):

    __tablename__ = "python_package_version_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    package_name = Column(String(256), nullable=False)
    # Nullable if we cannot resolve.
    package_version = Column(String(256), nullable=True)
    # Nullable if coming from user or cross-index resolution.
    index_url = Column(String(256), nullable=True)

    versions = relationship("DependsOn", back_populates="entity")

    __table_args__ = (
        UniqueConstraint(
            "package_name",
            "package_version",
            "index_url",
        ),
        Index(
            "python_package_version_entity_idx",
            "package_name",
            "package_version",
            "index_url",
            unique=True,
        ),
    )


class DependsOn(Base, BaseExtension):

    __tablename__ = 'depends_on'

    id = Column(Integer, primary_key=True, autoincrement=True)

    entity_id = Column(Integer, ForeignKey('python_package_version_entity.id'), primary_key=True)
    version_id = Column(Integer, ForeignKey('python_package_version.id'), primary_key=True)

    version_range = Column(String(128))

    entity = relationship("PythonPackageVersionEntity", back_populates="versions")
    version = relationship("PythonPackageVersion", back_populates="entities")

    __table_args__ = (
        UniqueConstraint(
            "entity_id",
            "version_id",
        ),
        Index(
            "depends_on_idx",
            "entity_id",
            "version_id",
            unique=True,
        ),
    )


class EcosystemSolver(Base, BaseExtension):

    __tablename__ = "ecosystem_solver"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ecosystem = Column(String(256))
    solver_name = Column(String(256))
    solver_version = Column(String(16))
    os_name = Column(String(128))
    os_version = Column(String(8))
    python_version = Column(String(8))

    versions = relationship("Solved", back_populates="ecosystem_solver")

    __table_args__ = (
        UniqueConstraint(
            "ecosystem",
            "solver_name",
            "solver_version",
            "os_name",
            "os_version",
            "python_version",
        ),
        Index(
            "ecosystem_solver_idx",
            "ecosystem",
            "solver_name",
            "solver_version",
            "os_name",
            "os_version",
            "python_version",
            unique=True,
        ),
    )


class UserRunSoftwareEnvironmentModel(Base, BaseExtension):

    __tablename__ = "user_run_software_environment"

    id = Column(Integer, primary_key=True, autoincrement=True)


class CVE(Base, BaseExtension):

    __tablename__ = "cve"

    id = Column(Integer, primary_key=True, autoincrement=True)


class PythonPackageRequirement(Base, BaseExtension):

    __tablename__ = "python_package_requirement"

    id = Column(Integer, primary_key=True, autoincrement=True)


class SoftwareStackBase:
    pass


class UserSoftwareStack(Base, BaseExtension, SoftwareStackBase):

    __tablename__ = "user_software_stack"

    id = Column(Integer, primary_key=True, autoincrement=True)


class AdvisedSoftwareStack(Base, BaseExtension, SoftwareStackBase):

    __tablename__ = "advised_software_stack"

    id = Column(Integer, primary_key=True, autoincrement=True)


class InspectionSoftwareStack(Base, BaseExtension, SoftwareStackBase):

    __tablename__ = "inspection_software_stack"

    id = Column(Integer, primary_key=True, autoincrement=True)

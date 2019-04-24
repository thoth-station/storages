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

"""Base operations on top of Dgraph's models."""

import re
import os
from typing import Optional
from typing import Callable
from typing import Tuple
from typing import List
import logging
import json
from functools import wraps

from hashlib import sha1

from pydgraph import DgraphClient
from pydgraph import AbortedError

import attr

from ..exceptions import MultipleFoundError
from ..exceptions import NotFoundError


_LOGGER = logging.getLogger(__name__)


def model_property(type, default=None, index=None, reverse=None, count=None):
    """Define a property with its attributes.

    Make sure metadata get stored for later automatic schema generation.
    """
    metadata = {"dgraph": ""}

    if index:
        if isinstance(index, str):
            metadata["dgraph"] += f"@index({index}) "
        elif isinstance(index, bool) and index is True:
            metadata["dgraph"] += f"@index "

    if reverse:
        metadata["dgraph"] += f"@reverse "

    if count:
        metadata["count"] += f"@count"

    return attr.ib(kw_only=True, type=type, default=default, metadata=metadata)


@attr.s(slots=True)
class Element:
    """An abstract class with common methods for vertex and edge."""

    _RE_CAMEL2SNAKE = re.compile("(?!^)([A-Z]+)")
    ELEMENT_NAME = None

    # Dgraph uses uint64_t for UID.
    uid = attr.ib(type=int, default=None)

    @staticmethod
    def compute_label_hash(data) -> str:
        """Get hash of this element."""
        content = json.dumps(data, sort_keys=True)
        return sha1(content.encode()).hexdigest()

    @classmethod
    def get_label(cls) -> str:
        """Retrieve label of the given vertex or edge."""
        return cls.get_name() + '_label'

    @classmethod
    def get_name(cls) -> str:
        """Get name of edge."""
        return cls.ELEMENT_NAME or cls._RE_CAMEL2SNAKE.sub(r"_\1", cls.__name__).lower()

    def to_dict(self, *, without_uid: bool = False) -> dict:
        """Covert an edge or vertex representation to a dict."""
        result = attr.asdict(self)
        if without_uid:
            result.pop("uid")

        return result

    def get_or_create(self, client: DgraphClient) -> bool:
        """Get or create the given entity."""
        raise NotImplementedError

    @classmethod
    def get_properties(cls) -> dict:
        """Get all properties with their corresponding type."""
        result = {}
        for attribute in cls.__attrs_attrs__:
            if attribute.name in ("source", "target", "uid"):
                # Edge attributes for storing source and target vertex or uid which is automatically generated.
                continue

            result[attribute.name] = attribute.type

        return result

    @staticmethod
    def _do_upsert(client: DgraphClient, label: str, label_hash: str, data: dict) -> Tuple[int, bool]:
        """Perform upsert operation."""
        upsert_query = """
        {
            all(func: eq(%s, "%s")) {
                uid
                %s
            }
        }""" % (label, label_hash, label)
        transaction = client.txn(read_only=False)
        try:
            res = transaction.query(upsert_query)
            entries = json.loads(res.json)

            if len(entries["all"]) != 0:
                if len(entries["all"]) > 1:
                    _LOGGER.error(f"Found multiple entities with label {label!r} with hash {label_hash!r}")

                uid = entries["all"][0]["uid"]
                _LOGGER.debug("Using entity %r with uid %r", data, uid)
                transaction.commit()
                return uid, True

            res = transaction.mutate(set_obj=data)
            transaction.commit()
        except AbortedError:
            _LOGGER.exception(
                f"Transaction has been aborted - concurrent upsert writes for {label!r} with hash {label_hash}?"
            )
            raise
        finally:
            transaction.discard()
        # If JSON is sent as an input, Dgraph assigns "blank-0" for the blank node being
        # synced. We use it as a key to obtain assigned UID from the graph.
        uid = res.uids["blank-0"]
        _LOGGER.debug("Created a new entity %r with uid %r", data, uid)
        return uid, False

    @classmethod
    def _do_query(cls, client: DgraphClient, keys: dict) -> List["Element"]:
        """Perform the actual query to the Dgraph instance."""
        label = cls.get_label()

        filter_str = ""
        for key, value in keys.items():
            if filter_str:
                filter_str += " AND "
            if isinstance(value, str):
                filter_str += f'eq({key}, "{value}")'
            else:
                filter_str += f'eq({key}, {value})'

        query = """
        {
            q(func: has(%s)) @filter(%s) {
                uid
                %s
            }
        }
        """ % (label, filter_str, "\n".join(cls.get_properties().keys()))
        query_result = client.txn(read_only=True).query(query)
        query_result = json.loads(query_result.json)["q"]

        result = []
        for attrs in query_result:
            instance = cls(**attrs)
            result.append(instance)

        return result

    @classmethod
    def query_all(cls, client: DgraphClient, *, raise_on_not_found: bool = False, **keys) -> List["Element"]:
        """Query graph database for entity with the given set of parameters."""
        result = cls._do_query(client, keys)
        if not result and raise_on_not_found:
            raise NotFoundError(
                f"Entity with label {cls.get_label()!r} not found in the database with: {keys!r}"
            )

        return result

    @classmethod
    def query_one(cls, client: DgraphClient, *, raise_on_not_found: bool = False, **keys) -> "Element":
        """Query graph database for entity with the given set of parameters for an entity."""
        result = cls._do_query(client, keys)
        if not result and raise_on_not_found:
            raise NotFoundError(
                f"Entity with label {cls.get_label()!r} not found in the database with properties: {keys!r}"
            )

        if len(result) > 1:
            raise MultipleFoundError(
                f"Multiple entities with label {cls.get_label()!r} found with properties: {keys!r}"
            )

        return result[0] if len(result) > 0 else None

    @classmethod
    def _do_modify(
            cls,
            client: DgraphClient,
            *,
            keys: dict,
            properties: dict,
            raise_on_not_found: bool = False,
            only_one: bool = False
    ) -> List["Element"]:
        """Perform modification of an entity matching the given keys."""
        label = cls.get_label()

        filter_str = ""
        for key, value in keys.items():
            if filter_str:
                filter_str += " AND "
            if isinstance(value, str):
                filter_str += f'eq({key}, "{value}")'
            else:
                filter_str += f'eq({key}, {value})'

        if not keys:
            raise ValueError(f"No keys supplied to perform modification on {label}")

        if not properties:
            raise ValueError(f"No properties supplied to perform modification on {label}")

        query = """
        {
            q(func: has(%s)) @filter(%s) {
                uid
                %s
            }
        }
        """ % (label, filter_str, "\n".join(cls.get_properties().keys()))

        instances = []
        transaction = client.txn(read_only=False)
        try:
            result = transaction.query(query)
            result = json.loads(result.json)["q"]

            if raise_on_not_found and not result:
                raise NotFoundError(
                    f"No entities {label} found for modification with filter criteria {filter_str}"
                )

            if only_one and len(result) > 1:
                raise MultipleFoundError(
                    f"Multiple entities {label} found for modification with filter criteria {filter_str}"
                )

            for original_properties in result:
                instance = cls(**original_properties)
                for property_key, property_value in properties.items():
                    setattr(instance, property_key, property_value)
                    transaction.mutate(set_obj=instance.to_dict(without_uid=False))
                    instances.append(instance)

            transaction.commit()
        finally:
            transaction.discard()

        return instances

    @classmethod
    def modify_all(
            cls,
            client: DgraphClient,
            *,
            properties: dict,
            raise_on_not_found: bool = False,
            **keys,
    ) -> List["Element"]:
        """Modify all properties of models stored inside graph database matching the given keys."""
        return cls._do_modify(
            client,
            keys=keys,
            raise_on_not_found=raise_on_not_found,
            properties=properties,
            only_one=False,
        )

    @classmethod
    def modify_one(
            cls,
            client: DgraphClient,
            *,
            properties: dict,
            raise_on_not_found: bool = False,
            **keys,
    ) -> "Element":
        """Modify all properties of models stored inside graph database matching the given keys."""
        result = cls._do_modify(
            client,
            keys=keys,
            raise_on_not_found=raise_on_not_found,
            properties=properties,
            only_one=False,
        )
        return result[0] if len(result) > 0 else []


@attr.s(slots=True)
class VertexBase(Element):
    """A base class for implementing vertexes."""

    _CACHE = None

    @classmethod
    def from_properties(cls, **properties):
        """Instantiate a vertex from properties."""
        return cls(**properties)

    def get_or_create(self, client: DgraphClient) -> bool:
        """Get or create the given vertex.

        This is implementation of the upsert procedure.
        """
        data = self.to_dict(without_uid=True)
        label = self.get_label()
        label_hash = self.compute_label_hash(data)
        data[label] = label_hash

        if self._CACHE and label_hash in self._CACHE:
            _LOGGER.debug("Vertex with label %r found in vertex cache %r", label, label_hash)
            self.uid = self._CACHE[label_hash]
            return True

        self.uid, existed = self._do_upsert(client, label, label_hash, data)
        return existed


@attr.s(slots=True)
class EdgeBase(Element):
    """A base class for implementing edges."""

    source = attr.ib(type=VertexBase, default=None, kw_only=True)
    target = attr.ib(type=VertexBase, default=None, kw_only=True)

    @classmethod
    def from_properties(cls, *, source, target, **properties):
        """Instantiate a vertex from properties."""
        return cls(source=source, target=target, **properties)

    def get_or_create(self, client: DgraphClient) -> bool:
        """Get or create the given edge."""
        assert self.source is not None, "No source vertex provided"
        assert self.target is not None, "No target vertex provided"

        if self.source.uid is None:
            raise ValueError(
                "Source vertex not mapped to any entity in graph database, was get_or_create() called?"
            )

        if self.target.uid is None:
            raise ValueError(
                "Target vertex not mapped to any entity in graph database, was get_or_create() called?"
            )

        edge_name = self.get_name()
        data = self.to_dict(without_uid=True)
        data.pop("target")
        data.pop("source")
        edge_def = {
            "uid": self.source.uid,
            # Respect Facets syntax in JSON.
            edge_name: {f"{edge_name}|{k}": v for k, v in data.items() if k != "uid"},
        }
        label = self.get_label()
        label_hash = self.compute_label_hash(edge_def)
        edge_def[edge_name][label] = label_hash
        edge_def[edge_name]["uid"] = self.target.uid
        # Edges have no relevant uid, do not assign it.
        _, existed = self._do_upsert(client, label, label_hash, edge_def)
        return existed


@attr.s(slots=True)
class ReverseEdgeBase(EdgeBase):
    """An edge which stores also reverse direction."""


def enable_vertex_cache(func: Callable):  # Ignore PyDocStyleBear
    """Enable vertex caching."""

    @wraps(func)
    def wrapped(*args, **kwargs):
        if bool(int(os.getenv("THOTH_STORAGES_DISABLE_CACHE", "0"))):
            _LOGGER.debug("Disabling vertex graph cache")
            # We could just return directly function call here, but
            # this version works as expected in Jupyter notebooks.
            return func(*args, **kwargs)

        _LOGGER.debug("Enabling vertex graph cache")
        VertexBase._CACHE = {}

        try:
            result = func(*args, **kwargs)
        finally:
            # We delete cache once sync is done.
            VertexBase._CACHE = None

        return result

    return wrapped

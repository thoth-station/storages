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
import logging
import json
from functools import wraps

from hashlib import sha1


from pydgraph import DgraphClient
from pydgraph import AbortedError


import attr


_LOGGER = logging.getLogger(__name__)


def model_property(type, default=None, index=None, reverse=None, count=None):
    """Define a property with its attributes.

    Make sure metadata get stored for later automatic schema generation.
    """
    metadata = {"dgraph": ""}

    if index:
        metadata["dgraph"] += f"@index({index}) "

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
    _uid = attr.ib(type=int, default=None)

    @property
    def uid(self) -> Optional[int]:
        """Return uid for the given element (vertex or edge).

        If uid is set to None, the given model is not mapped to any database representative.
        """
        return self._uid

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
            result.pop("_uid")

        return result

    def _do_upsert(self, client: DgraphClient, label: str, label_hash: str, data: dict):
        transaction = client.txn(read_only=False)
        upsert_query = """
        query q($label: string) {
            all(func: eq(%s, $label)) {
                uid
            }   
        }""" % label
        try:
            res = client.query(upsert_query, variables={"$label": label_hash})
            entries = json.loads(res.json)

            if len(entries["all"]) != 0:
                if len(entries["all"]) > 1:
                    _LOGGER.error(f"Found multiple entities with label {label!r} with hash {label_hash!r}")

                self._uid = entries["all"][0]["uid"]
                _LOGGER.debug("Using entity %r with uid %r", data, self._uid)
                transaction.commit()
                return

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
        self._uid = res.uids["blank-0"]
        _LOGGER.debug("Created a new entity %r with uid %r", data, self._uid)


@attr.s(slots=True)
class VertexBase(Element):
    """A base class for implementing vertexes."""

    _CACHE = None

    @classmethod
    def from_properties(cls, **properties):
        """Instantiate a vertex from properties."""
        return cls(**properties)

    def get_or_create(self, client: DgraphClient):
        """Get or create the given vertex.

        This is implementation of the upsert procedure.
        """
        data = self.to_dict(without_uid=True)
        label = self.get_label()
        label_hash = self.compute_label_hash(data)
        data[label] = label_hash

        if self._CACHE and label_hash in self._CACHE:
            _LOGGER.debug("Vertex with label %r found in vertex cache %r", label, label_hash)
            self._uid = self._CACHE[label_hash]

        self._do_upsert(client, label, label_hash, data)


@attr.s(slots=True)
class EdgeBase(Element):
    """A base class for implementing edges."""

    source = attr.ib(type=VertexBase, default=None, kw_only=True)
    target = attr.ib(type=VertexBase, default=None, kw_only=True)

    @classmethod
    def from_properties(cls, *, source, target, **properties):
        """Instantiate a vertex from properties."""
        return cls(source=source, target=target, **properties)

    def get_or_create(self, client: DgraphClient):
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
            edge_name: data,
        }
        edge_def[edge_name]["uid"] = self.target.uid
        label = self.get_label()
        label_hash = self.compute_label_hash(data)
        edge_def[edge_name][label] = label_hash
        self._do_upsert(client, label, label_hash, edge_def)


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

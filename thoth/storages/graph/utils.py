#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# thoth-storages
# Copyright(C) 2018 Fridolin Pokorny
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

"""Various utilities and helper methods for the Graph database."""

import os
import typing
import logging

from aiogremlin.process.graph_traversal import AsyncGraphTraversalSource
from gremlin_python.process.graph_traversal import addV
from gremlin_python.process.graph_traversal import unfold

from .cache import Cache
from .cache import CacheMiss
from .models_base import VertexBase
from .models_base import EdgeBase

_LOGGER = logging.getLogger(__name__)


def enable_vertex_cache(func: typing.Callable):
    """Enable vertex caching."""
    def wrapped(*args, **kwargs):
        if bool(int(os.getenv('THOTH_STORAGES_DISABLE_CACHE', '0'))):
            _LOGGER.debug("Disabling vertex graph cache")
            # We could just return directly function call here, but
            # this version works as expected in Jupyter notebooks.
            return func(*args, **kwargs)

        _LOGGER.debug("Enabling vertex graph cache")
        VertexBase.cache = Cache()

        try:
            result = func(*args, **kwargs)
        finally:
            VertexBase.cache.wipe()
            VertexBase.cache = None

        return result

    return wrapped


def enable_edge_cache(func: typing.Callable):
    """Enable caching for edge handling."""
    def wrapped(*args, **kwargs):
        if bool(int(os.getenv('THOTH_STORAGES_DISABLE_CACHE', '0'))):
            _LOGGER.debug("Disabling edge graph cache")
            # We could just return directly function call instead of wrapper
            # here, but this version works as expected in Jupyter notebooks.
            return func(*args, **kwargs)

        _LOGGER.debug("Enabling edge graph cache")
        EdgeBase.cache = Cache()

        try:
            result = func(*args, **kwargs)
        finally:
            EdgeBase.cache.wipe()
            EdgeBase.cache = None

        return result

    return wrapped


# Ignore PycodestyleBear (E501)
async def get_or_create_vertex(g: AsyncGraphTraversalSource, vertex: VertexBase) -> tuple:
    """Create a vertex if not existes.

    If the Vertex does not exists, it is created, if the given vertex
    already exists, it's ID is returned.
    """
    if VertexBase.cache:
        try:
            cached_id = VertexBase.cache.get(vertex.to_dict())
            vertex.id = cached_id
            return cached_id, True
        except CacheMiss:
            pass

    query = g.V()
    creation = addV(vertex.__label__)

    for key, value in vertex.to_dict().items():
        # Goblin's to_dict() calls to_dict() on properties. If there is
        # such case, get actual value from property.
        if isinstance(value, dict) and '__value__' in value:
            value = value['__value__']
        if value is not None:
            query = query.has(key, value)
            creation = creation.property(key, value)
        else:
            query = query.hasNot(key)

    result = await query.fold().coalesce(
        unfold().id().as_('id').constant(True).as_('existed')
        .select('id', 'existed'),
        creation.id().as_('id').constant(False).as_('existed')
        .select('id', 'existed')
    ).next()

    if VertexBase.cache:
        VertexBase.cache.put(vertex.to_dict(), result['id'])

    # Assign to instance so instance has the id associated correctly
    # for later queries.
    vertex.id = result['id']

    return result['id'], result['existed']


async def get_or_create_edge(g: AsyncGraphTraversalSource, edge: EdgeBase,
                             source_id: int = None,
                             target_id: int = None) -> tuple:
    """Create an edge if not existed.

    If the given edge already exists, return its id.

    Optional parameters source_id and target_id are present for optimizations.
    """
    # If source_id/target_id are not provided explicitly and
    # edge.source/edge.target are not set, this will raise
    # an exception. Provide at least one based on your usage.
    source_id = source_id or edge.source.id
    target_id = target_id or edge.target.id

    if EdgeBase.cache:
        item = edge.to_dict()
        item['source'] = source_id
        item['target'] = target_id
        try:
            cached_id = EdgeBase.cache.get(item)
            edge.id = cached_id
            return cached_id, True
        except CacheMiss:
            pass

    query = g.V(source_id).outE()
    creation = g.V(source_id).addE(edge.__label__)

    for key, value in edge.to_dict().items():
        if key in ('source', 'target', 'id'):
            continue

        # Goblin's to_dict() calls to_dict() on properties. If there is
        # such case, get actual value from property.
        if isinstance(value, dict) and '__value__' in value:
            value = value['__value__']

        if value is not None:
            query = query.has(key, value)
            creation = creation.property(key, value)
        else:
            query = query.hasNot(key)

    result = await query.as_('e').inV().hasId(target_id).select('e').fold().coalesce(
        unfold().id().as_('id').constant(True).as_('existed').select('id', 'existed'),
        creation.as_('e').to(g.V(target_id)).select('e').id().as_('id')
        .constant(False).as_('existed').select('id', 'existed')
    ).next()

    if EdgeBase.cache:
        item = edge.to_dict()
        # Overwrite source and target dict with actual id.
        item['source'] = source_id
        item['target'] = target_id
        EdgeBase.cache.put(item, result['id'])

    # Assign to instance so instance has the id associated correctly for
    # later queries.
    edge.id = result['id']

    return result['id'], result['existed']

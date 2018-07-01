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

"""A base classes for model representation."""

import asyncio

from goblin import Vertex
from goblin import VertexProperty
from goblin import Edge

from aiogremlin.process.graph_traversal import AsyncGraphTraversalSource


class VertexBase(Vertex):
    """A base class for edges that extends Goblin's vertex implementation."""

    # Vertex cache to be used.
    cache = None

    def __repr__(self):
        """Show vertex representation."""
        values = ''
        for key, value in self.to_dict().items():
            if key.startswith('__'):
                continue
            values += '{}={}, '.format(key, repr(value)
                                       if isinstance(value, str) else value)

        return f'{self.__class__.__name__}({values[:-2]})'

    def to_pretty_dict(self) -> dict:
        """Return a dict representation of this object.

        It can be exposed on API endpoints directly.
        """
        result = {}

        for property_name, property_value in self.__properties__.items():
            if isinstance(property_value, VertexProperty):
                prop = getattr(self, property_name, None)
                result[property_name] = prop.value if prop else None

        return result

    def get_or_create(self, g: AsyncGraphTraversalSource) -> bool:
        """Get or create this vertex."""
        # Avoid cyclic imports due to typing.
        from .utils import get_or_create_vertex

        loop = asyncio.get_event_loop()
        _, existed = loop.run_until_complete(get_or_create_vertex(g, self))
        return existed

    @classmethod
    def from_properties(cls, **vertex_properties):
        """Create a vertex based on its properties."""
        instance = cls()

        for attr, value in vertex_properties.items():
            # Ensure that the instance has the given attribute.
            getattr(instance, attr)
            setattr(instance, attr, value)

        return instance


class EdgeBase(Edge):
    """A base class for edges that extends Goblin's edge implementation."""

    # Edge cache to be used.
    cache = None

    def __repr__(self):  # Ignore PyDocStyleBear
        values = ''
        for key, value in self.to_dict().items():
            if key.startswith('__'):
                continue
            values += '{}={}, '.format(key, repr(value)
                                       if isinstance(value, str) else value)

        return f'{self.__class__.__name__}({values[:-2]})'

    def get_or_create(self, g: AsyncGraphTraversalSource) -> bool:
        """Get or create a this edge."""
        # Avoid cyclic imports due to typing.
        from .utils import get_or_create_edge

        loop = asyncio.get_event_loop()
        _, existed = loop.run_until_complete(get_or_create_edge(g, self))

        return existed

    @classmethod
    def from_properties(cls, **edge_properties):
        """Create edge based on its properties.

        >>> source_node = PackageVersion.from_properties(ecosystem='pypi', name='selinon', version='1.0.0rc1')
        >>> target_node = PackageVersion.from_properties(ecosystem='pypi', name='pyyaml', version='1.0.0')
        >>> edge = DependsOn.from_properties(version_range='>=10', source=source_node, target=target_node)
        """
        instance = cls()

        for attr, value in edge_properties.items():
            setattr(instance, attr, value)

        return instance

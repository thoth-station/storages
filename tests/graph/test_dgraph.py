#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2018, 2019 Fridolin Pokorny
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

"""Test related to graph database.

As most of the queries directly prepare results using graphql, there are
stated just tests which require some additional post-processing logic.
"""

from pydgraph import DgraphClientStub

from thoth.storages import GraphDatabase


class TestGraphDatabase:
    """Test graph database adapter."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = DgraphClientStub("localhost:9080")

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

"""Implementation of chained query for submitting items in a burst mode."""

import asyncio


class ChainedQueryBase:
    cache = None

    def __init__(self, g, cache):
        self.query = g
        self.cache = cache

    def execute(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.query.next())

    def __del__(self):
        self.cache.wipe()


class ChainedVertexQuery(ChainedQueryBase):
    pass


class ChainedEdgeQuery(ChainedQueryBase):
    pass

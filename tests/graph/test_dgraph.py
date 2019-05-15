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

from itertools import chain

import flexmock

from thoth.storages import GraphDatabase


class TestGraphDatabase:
    """Test graph database adapter."""

    _TRANSITIVE_SUBRESULT_1 = {
        "q": [{
            'depends_on': [
                {
                    'uid': '0x2',
                },
            ],
            'uid': '0x1',
        }]
    }

    _TRANSITIVE_SUBRESULT_2 = {
        "q": [{
            'depends_on': [
                {
                    'uid': '0x3',
                    'depends_on': [
                        {'uid': '0x2'}
                    ]
                },
            ],
            'uid': '0x2',
        }],
    }

    _TRANSITIVE_RESULT = {"0x1": ("a", "b", "c"), "0x2": ("A", "B", "C"), "0x3": ("X", "Y", "Z")}

    def test_transitive_query_cycles(self):
        flexmock(GraphDatabase)
        GraphDatabase.should_receive("_query_raw") \
            .and_return(self._TRANSITIVE_SUBRESULT_1)\
            .ordered()
        GraphDatabase.should_receive("_query_raw") \
            .and_return(self._TRANSITIVE_SUBRESULT_2)\
            .ordered()
        GraphDatabase.should_receive("get_python_package_tuples") \
            .with_args({"0x1", "0x2", "0x3"}) \
            .and_return(self._TRANSITIVE_RESULT) \
            .ordered()

        old_depth = GraphDatabase._TRANSITIVE_QUERY_DEPTH
        try:
            GraphDatabase._TRANSITIVE_QUERY_DEPTH = 2
            # Explicitly set recirsive limit to lower number not to create complex tests.
            graph = GraphDatabase()
            result = graph.retrieve_transitive_dependencies_python(
                package_name="flask",
                package_version="1.0.2",
                index_url="https://pypi.org/simple",
                os_name="fedora",
                os_version="29",
                python_version="3.6",
            )
            # 0x3 links back to 0x2, but that one was already checked.
            assert result == [[('a', 'b', 'c'), ('A', 'B', 'C'), ('X', 'Y', 'Z'), ('A', 'B', 'C')]]
        finally:
            GraphDatabase._TRANSITIVE_QUERY_DEPTH = old_depth

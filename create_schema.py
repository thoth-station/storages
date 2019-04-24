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

"""Create schema out of Thoth's graph models."""

import sys
from datetime import datetime
from pathlib import Path

import click

from thoth.storages.graph.models import ALL_MODELS
from thoth.storages.graph.models_base import ReverseEdgeBase
from thoth.storages.graph.models_base import EdgeBase
from thoth.storages.graph.models_base import VertexBase


_DGRAPH_TYPES_NAME_MAP = {
    str.__name__: "string",
    int.__name__: "int",
    bool.__name__: "bool",
    float.__name__: "float",
    datetime.__name__: "dateTime"
}


def create_schema(models: frozenset):
    """Create schema based on models defined."""
    schema = ""
    properties_seen = set()
    for model in sorted(models, key=lambda x: x.__name__):
        # Used to guarantee a node exists exactly once.
        schema += f"{model.get_label()}: string @count @upsert @index(exact) .\n"
        if issubclass(model, ReverseEdgeBase):
            schema += f"{model.get_name()}: uid @reverse @count .\n"
        elif issubclass(model, EdgeBase):
            schema += f"{model.get_name()}: uid @count .\n"
        elif not issubclass(model, VertexBase):
            raise ValueError(f"Unknown entity - not derived from vertex nor edge: {model}")

        for attribute in model.__attrs_attrs__:
            if attribute.name in ("source", "target", "uid"):
                # Edge attributes for storing source and target vertex or uid which is automatically generated.
                continue

            if attribute.name in properties_seen:
                continue

            definition = f"{attribute.name}: {_DGRAPH_TYPES_NAME_MAP[attribute.type.__name__]} "

            if "dgraph" in attribute.metadata:
                definition += attribute.metadata["dgraph"]

            schema += definition + ".\n"
            properties_seen.add(attribute.name)

    if not schema:
        raise ValueError("No entities found, no schema generated")

    return schema


@click.command()
@click.option(
    "--output", "-o",
    type=click.Path(exists=False, dir_okay=False, writable=True),
    required=False,
    help="Output file where the generated schema should be stored to."
)
def cli(output):
    """Tool for Thoth - automated creation of RDF schema out of models."""
    schema = create_schema(ALL_MODELS)

    if output:
        with open(output, "w") as output_file:
            output_file.write(schema)
    else:
        click.echo(schema)


if __name__ == "__main__":
    sys.exit(cli())

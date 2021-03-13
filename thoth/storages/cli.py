#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2019, 2020 Fridolin Pokorny
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

"""A CLI client to thoth-storages library."""

import logging
import re

import click
import daiquiri

from thoth.storages import __version__ as thoth_storages_version

daiquiri.setup(level=logging.INFO)
_LOGGER = logging.getLogger("thoth.storages")


def _print_version(ctx, _, value):
    """Print thoth-storages version and exit."""
    if not value or ctx.resilient_parsing:
        return

    click.echo(thoth_storages_version)
    ctx.exit()


@click.group()
@click.pass_context
@click.option(
    "-v", "--verbose", is_flag=True, envvar="THOTH_STORAGES_VERBOSE", help="Be verbose about what's going on."
)
@click.option(
    "--version",
    is_flag=True,
    is_eager=True,
    callback=_print_version,
    expose_value=False,
    help="Print version and exit.",
)
def cli(ctx=None, verbose: bool = False):
    """CLI tool for interacting with Thoth."""
    if ctx:
        ctx.auto_envvar_prefix = "THOTH_STORAGES"

    if verbose:
        _LOGGER.setLevel(logging.DEBUG)
        _LOGGER.debug("Debug mode is on")


@cli.command("generate-schema")
@click.option(
    "-i",
    "--include",
    multiple=True,
    type=str,
    help=(
        "Models to be included in the generated schema. Accepts regular expression. "
        "If not provided, all models will be included."
    ),
)
@click.option(
    "--include_performance_models", default=True, help="Whether to include performance models in the generated schema."
)
@click.argument("schema_file", type=str, required=False, default="schema.png", metavar="schema.png")
def generate_schema(schema_file: str, include=None, include_performance_models=True):
    """Generate an image out of the current schema."""
    try:
        import sadisplay
        import pydot
    except ImportError:
        _LOGGER.error("Failed to import required libraries to perform schema generation")
        raise

    import thoth.storages.graph.models_performance as performance_models

    from thoth.storages.graph.models import ALL_MAIN_MODELS
    from thoth.storages.graph.models import ALL_RELATION_MODELS

    all_models = list(ALL_MAIN_MODELS.union(ALL_RELATION_MODELS))

    if include:
        desc_models = [m for m in all_models if any(re.fullmatch(p, m.__name__) for p in include)]
    else:
        desc_models = all_models

    if include_performance_models:
        desc_models += list(vars(performance_models).values())

    desc = sadisplay.describe(
        desc_models,
        show_methods=True,
        show_properties=True,
        show_indexes=False,
        show_simple_indexes=False,
        show_columns_of_indexes=False,
    )
    dot_data = sadisplay.dot(desc)
    (graph,) = pydot.graph_from_dot_data(dot_data)
    _LOGGER.info("Writing schema to %r...", schema_file)
    graph.write_png(schema_file)


if __name__ == "__main__":
    cli()

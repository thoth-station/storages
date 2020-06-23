#!/usr/bin/env python
# Methods from SQLAlchemy utils modified.
# TODO: remove once https://github.com/kvesteri/sqlalchemy-utils/pull/372 is merged
#
###################################################################
#  SQLAlchemy utils methods
# Copyright (c) 2012, Konsta Vesterinen
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# * The names of the contributors may not be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  See https://github.com/kvesteri/sqlalchemy-utils/blob/master/LICENSE.
####################################################################
#
# Additional changes for project Thoth by Thoth team.
#

"""Utils for postgresql database."""

import os
import logging
from copy import copy

from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import OperationalError, ProgrammingError

_LOGGER = logging.getLogger(__name__)


def database_exists(url):
    """Check if a database exists.
    :param url: A SQLAlchemy engine URL.
    Performs backend-specific testing to quickly determine if a database
    exists on the server. ::
        database_exists('postgres://postgres@localhost/name')  #=> False
        create_database('postgres://postgres@localhost/name')
        database_exists('postgres://postgres@localhost/name')  #=> True
    Supports checking against a constructed URL as well. ::
        engine = create_engine('postgres://postgres@localhost/name')
        database_exists(engine.url)  #=> False
        create_database(engine.url)
        database_exists(engine.url)  #=> True

    Modified version from sqlalchemy_utils to take care of one issue.
    """

    def get_scalar_result(engine, sql):
        result_proxy = engine.execute(sql)
        result = result_proxy.scalar()
        result_proxy.close()
        engine.dispose()
        return result

    url = copy(make_url(url))
    database, url.database = url.database, os.getenv('KNOWLEDGE_GRAPH_DATABASE')
    engine = create_engine(url)

    if engine.dialect.name == "postgresql":
        text = "SELECT 1 FROM pg_database WHERE datname='%s'" % database
        return bool(get_scalar_result(engine, text))

    else:
        _LOGGER.exception("This implementation is valid only for postgresql dialects")


def create_database(url, encoding="utf8", template=None):
    """Issue the appropriate CREATE DATABASE statement.
    :param url: A SQLAlchemy engine URL.
    :param encoding: The encoding to create the database as.
    :param template:
        The name of the template from which to create the new database. At the
        moment only supported by PostgreSQL driver.
    To create a database, you can pass a simple URL that would have
    been passed to ``create_engine``. ::
        create_database('postgres://postgres@localhost/name')
    You may also pass the url from an existing engine. ::
        create_database(engine.url)
    Has full support for mysql, postgres, and sqlite. In theory,
    other database engines should be supported.

    Modified version from sqlalchemy_utils to take care of one issue.
    """

    url = copy(make_url(url))

    database, url.database = url.database, os.getenv('KNOWLEDGE_GRAPH_DATABASE')
    engine = create_engine(url)
    result_proxy = None

    if engine.dialect.name == "postgresql":
        if engine.driver == "psycopg2":
            from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

            engine.raw_connection().set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        if not template:
            template = "template1"

        text = "CREATE DATABASE {0} ENCODING '{1}' TEMPLATE {2}".format(
            quote(engine, database), encoding, quote(engine, template)
        )
        result_proxy = engine.execute(text)

    else:
        _LOGGER.exception("This implementation is valid only for postgresql dialects")

    if result_proxy is not None:
        result_proxy.close()
    engine.dispose()

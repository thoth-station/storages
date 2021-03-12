#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2018, 2019, 2020 Fridolin Pokorny
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
# type: ignore

"""This is the tests."""

import os
from contextlib import contextmanager

from moto import mock_s3


def with_adjusted_env(env_dict: dict):
    """Adjust environment variables on function/method run."""

    def wrapper(func):
        def wrapped(*args, **kwargs):
            old_env, os.environ = os.environ, env_dict
            try:
                return func(*args, **kwargs)
            finally:
                os.environ = old_env

        return wrapped

    return wrapper


@contextmanager
def connected_ceph_adapter(adapter, raw_ceph=False):
    """Retrieve a connected adapter to Ceph results."""
    mock_s3().start()

    try:
        adapter.connect()
        # FIXME: We need to call this explicitly since we use moto/boto3
        # instead of raw Ceph which has slightly different behaviour if
        # a bucket is already present.
        if not raw_ceph:
            adapter.ceph._create_bucket_if_needed()
        else:
            adapter._create_bucket_if_needed()
        assert adapter.is_connected()
        yield adapter
    finally:
        mock_s3().stop()

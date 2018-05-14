#!/usr/bin/env python3
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

import os


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

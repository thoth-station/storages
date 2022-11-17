#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2020 Kevin Postlethwait, Francesco Murdaca
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

"""Adapter for persisting Security Indicator results."""

import os
import logging
from typing import Any
from typing import Dict
from typing import Optional
from typing import Iterator
from abc import abstractmethod
from itertools import groupby

from .ceph import CephStore

_LOGGER = logging.getLogger(__name__)


def _get_security_indicators_prefix(security_indicator_id: Optional[str] = None) -> str:
    """Get prefix where security indicators are stored."""
    bucket_prefix = os.environ["THOTH_CEPH_BUCKET_PREFIX"]
    deployment_name = os.environ["THOTH_DEPLOYMENT_NAME"]

    if security_indicator_id is None:
        return f"{bucket_prefix}/{deployment_name}/security-indicators"

    return f"{bucket_prefix}/{deployment_name}/security-indicators/{security_indicator_id}"


class _SecurityIndicatorBase:
    """A base class for security-indicators analyzers results."""

    @property
    @abstractmethod
    def security_indicator_type(self) -> str:
        raise NotImplementedError

    def __init__(self, security_indicator_id: str) -> None:
        """Set ceph prefix from security_indicator_id."""
        prefix = f"{_get_security_indicators_prefix(security_indicator_id)}/"
        self.ceph = CephStore(prefix=prefix)
        self.security_indicator_id = security_indicator_id

    def retrieve_document(self) -> Dict[str, Any]:
        """Retrieve security indicator document."""
        return self.ceph.retrieve_document(self.security_indicator_type)

    def document_exists(self) -> bool:
        """Check if the there is an object with the given key in bucket."""
        return self.ceph.document_exists(self.security_indicator_type)

    def connect(self) -> None:
        """Connect this adapter to Ceph."""
        self.ceph.connect()

    def is_connected(self) -> bool:
        """Check if this adapter is connected."""
        return self.ceph.is_connected()

    def check_connection(self) -> None:
        """Check connection of this adapter."""
        return self.ceph.check_connection()


class SIBanditStore(_SecurityIndicatorBase):
    """An adapter for manipulating security-indicators bandit."""

    security_indicator_type = "bandit"


class SIClocStore(_SecurityIndicatorBase):
    """An adapter for manipulating with security-indicators cloc."""

    security_indicator_type = "cloc"


class SIAggregatedStore(_SecurityIndicatorBase):
    """An adapter for manipulating security-indicators aggregated."""

    security_indicator_type = "aggregated"


class SecurityIndicatorsResultsStore:
    """Adapter for manipulating Security Indicators."""

    __slots__ = ["bandit", "cloc", "aggregated", "security_indicator_id"]

    def __init__(self, security_indicator_id: str) -> None:
        """Init sub stores for each security indicator type."""
        self.security_indicator_id = security_indicator_id
        self.bandit = SIBanditStore(security_indicator_id)
        self.cloc = SIClocStore(security_indicator_id)
        self.aggregated = SIAggregatedStore(security_indicator_id)

    def connect(self) -> None:
        """Connect this adapter."""
        self.bandit.connect()
        self.cloc.connect()
        self.aggregated.connect()

    def is_connected(self) -> bool:
        """Check if this adapter is connected."""
        return self.bandit.is_connected() and self.cloc.is_connected() and self.aggregated.is_connected()

    def check_connection(self):
        """Check connections of this adapter."""
        self.bandit.check_connection()
        self.cloc.check_connection()
        self.aggregated.check_connection()

    @classmethod
    def iter_security_indicators(cls) -> Iterator[str]:
        """Iterate over security_indicators ids stored."""
        ceph = CephStore(prefix=_get_security_indicators_prefix())
        ceph.connect()

        def _key_id(key: str) -> str:
            return key[: key.find("/")]

        # Return only unique si ids, discard any results placed under the given prefix.
        yield from (k for k, _ in groupby(ceph.get_document_listing(), _key_id))

    @classmethod
    def get_security_indicators_count(cls) -> int:
        """Get number of security_indicators stored."""
        return sum(1 for _ in cls.iter_security_indicators())

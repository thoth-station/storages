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
from typing import Generator

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

    __slots__ = ["ceph", "security_indicator_id"]

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
    """An adapter for manipulating with security-indicators bandit."""

    def __init__(self, security_indicator_id: str) -> None:
        """Constructor."""
        prefix = f"{_get_security_indicators_prefix(security_indicator_id)}/"
        self.ceph = CephStore(prefix=prefix)
        self.security_indicator_id = security_indicator_id

    def retrieve_document(self) -> Dict[str, Any]:
        """Retrieve SI bandit document."""
        return self.ceph.retrieve_document("bandit")

    def document_exists(self) -> bool:
        """Check if the there is an object with the given key in bucket."""
        return self.ceph.document_exists("bandit")


class SIClocStore(_SecurityIndicatorBase):
    """An adapter for manipulating with security-indicators cloc."""

    def __init__(self, security_indicator_id: str) -> None:
        """Constructor."""
        prefix = f"{_get_security_indicators_prefix(security_indicator_id)}/"
        self.ceph = CephStore(prefix=prefix)
        self.security_indicator_id = security_indicator_id

    def retrieve_document(self) -> Dict[str, Any]:
        """Retrieve SI cloc document."""
        return self.ceph.retrieve_document("cloc")

    def document_exists(self) -> bool:
        """Check if the there is an object with the given key in bucket."""
        return self.ceph.document_exists("cloc")


class SIAggregatedStore(_SecurityIndicatorBase):
    """An adapter for manipulating with security-indicators aggregated."""

    def __init__(self, security_indicator_id: str) -> None:
        """Constructor."""
        prefix = f"{_get_security_indicators_prefix(security_indicator_id)}/"
        self.ceph = CephStore(prefix=prefix)
        self.security_indicator_id = security_indicator_id

    def retrieve_document(self) -> Dict[str, Any]:
        """Retrieve SI aggregated document."""
        return self.ceph.retrieve_document("aggregated")

    def document_exists(self) -> bool:
        """Check if the there is an object with the given key in bucket."""
        return self.ceph.document_exists("aggregated")


class SecurityIndicatorsResultsStore:
    """Adapter for manipulating with Security Indicators."""

    __slots__ = ["bandit", "cloc", "aggregated", "security_indicator_id"]

    def __init__(self, security_indicator_id: str) -> None:
        """A representation of a Security Indicator."""
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
    def iter_security_indicators(cls) -> Generator[str, None, None]:
        """Iterate over security_indicators ids stored."""
        ceph = CephStore(prefix=_get_security_indicators_prefix())
        ceph.connect()

        last_id = None
        for item in ceph.get_document_listing():
            security_indicator_id = item.split("/", maxsplit=1)[0]
            if last_id == security_indicator_id:
                # Return only unique si ids, discard any results placed under the given prefix.
                continue

            last_id = security_indicator_id
            yield security_indicator_id

    @classmethod
    def get_security_indicators_count(cls) -> int:
        """Get number of security_indicators stored."""
        return sum(1 for _ in cls.iter_security_indicators())

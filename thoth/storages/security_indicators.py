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
from typing import Generator

from .ceph import CephStore

_LOGGER = logging.getLogger(__name__)


def _get_security_indicators_prefix(security_indicator_id: str) -> str:
    """Get prefix where security indicators for this id are stored."""
    bucket_prefix = os.environ["THOTH_CEPH_BUCKET_PREFIX"]
    deployment_name = os.environ["THOTH_DEPLOYMENT_NAME"]
    return f'{bucket_prefix}/{deployment_name}/security-indicators/{security_indicator_id}'

class SecurityIndicatorStore:
    """An adapter for working with security indicator results."""

    def __init__(self, security_indicator_id: str) -> None:
        """Constructor."""
        prefix = f"{_get_security_indicators_prefix(security_indicator_id)}"
        self.ceph = CephStore(prefix=prefix)
        self.security_indicator_id = security_indicator_id

    def retrieve_si_bandit_document(self) -> Dict[str, Any]:
        """Retrieve SI bandit document."""
        return self.ceph.retrieve_document("bandit")

    def retrieve_si_cloc_document(self) -> Dict[str, Any]:
        """Retrieve SI cloc document."""
        return self.ceph.retrieve_document("cloc")

    def retrieve_si_aggregated_document(self) -> Dict[str, Any]:
        """Retrieve SI aggregated document."""
        return self.ceph.retrieve_document("aggregated")

    def si_aggregated_document_exists(self) -> bool:
        """Check if the there is an object with the given key in bucket."""
        return self.ceph.document_exists("aggregated")

    def connect(self) -> None:
        """Connect this adapter."""
        self.ceph.connect()

    def is_connected(self) -> bool:
        """Check if this adapter is connected."""
        return self.ceph.is_connected()

    def check_connection(self):
        """Check connections of this adapter."""
        self.ceph.check_connection()


class SecurityIndicatorsResultsStore:
    """An adapter for working with security indicators results."""

    def __init__(self) -> None:
        """Constructor."""
        bucket_prefix = os.environ["THOTH_CEPH_BUCKET_PREFIX"]
        deployment_name = os.environ["THOTH_DEPLOYMENT_NAME"]
        prefix = f'{bucket_prefix}/{deployment_name}/security-indicators'
        self.ceph = CephStore(prefix=prefix)

    def connect(self) -> None:
        """Connect this adapter."""
        self.ceph.connect()

    def is_connected(self) -> bool:
        """Check if this adapter is connected."""
        return self.ceph.is_connected()

    def check_connection(self):
        """Check connections of this adapter."""
        self.ceph.check_connection()

    def get_listing(self) -> Generator[str, None, None]:
        """Get listing of documents available in Ceph as a generator."""
        return self.ceph.get_document_listing()

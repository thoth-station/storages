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

"""Storage and database adapters for Thoth."""

from .advisers import AdvisersResultsStore
from .advisers_cache import AdvisersCacheStore
from .analyses import AnalysisResultsStore
from .analyses_by_digest import AnalysisByDigest
from .analyses_cache import AnalysesCacheStore
from .buildlogs import BuildLogsStore
from .buildlogs_parsed import BuildLogsParsedResultsStore
from .buildlogs_analyses_cache import BuildLogsAnalysesCacheStore
from .ceph import CephStore
from .dependency_monkey_reports import DependencyMonkeyReportsStore
from .dependency_monkey_requests import DependencyMonkeyRequestsStore
from .graph import GraphDatabase
from .graph_backup import GraphBackupStore
from .inspections import InspectionResultsStore
from .inspections import InspectionBuildsStore
from .inspections import InspectionStore
from .logs import WorkflowLogsStore
from .provenance import ProvenanceResultsStore
from .provenance_cache import ProvenanceCacheStore
from .result_schema import RESULT_SCHEMA
from .security_indicators import SIAggregatedStore, SIBanditStore, SIClocStore
from .security_indicators import SecurityIndicatorsResultsStore
from .solvers import SolverResultsStore
from .sync import sync_adviser_documents
from .sync import sync_analysis_documents
from .sync import sync_dependency_monkey_documents
from .sync import sync_documents
from .sync import sync_inspection_documents
from .sync import sync_provenance_checker_documents
from .sync import sync_security_indicators_documents
from .sync import sync_solver_documents
from .sync import HANDLERS_MAPPING


__name__ = "thoth-storages"
__version__ = "0.62.1"

__all__ = [
    AdvisersCacheStore.__name__,
    AdvisersResultsStore.__name__,
    AnalysesCacheStore.__name__,
    AnalysisByDigest.__name__,
    AnalysisResultsStore.__name__,
    BuildLogsAnalysesCacheStore.__name__,
    BuildLogsParsedResultsStore.__name__,
    BuildLogsStore.__name__,
    CephStore.__name__,
    DependencyMonkeyReportsStore.__name__,
    DependencyMonkeyRequestsStore.__name__,
    GraphBackupStore.__name__,
    GraphDatabase.__name__,
    InspectionBuildsStore.__name__,
    InspectionResultsStore.__name__,
    InspectionStore.__name__,
    ProvenanceCacheStore.__name__,
    ProvenanceResultsStore.__name__,
    SecurityIndicatorsResultsStore.__name__,
    SIAggregatedStore.__name__,
    SIBanditStore.__name__,
    SIClocStore.__name__,
    SolverResultsStore.__name__,
    sync_adviser_documents.__name__,
    sync_analysis_documents.__name__,
    sync_dependency_monkey_documents.__name__,
    sync_documents.__name__,
    sync_inspection_documents.__name__,
    sync_provenance_checker_documents.__name__,
    sync_security_indicators_documents.__name__,
    sync_solver_documents.__name__,
    WorkflowLogsStore.__name__,
    "HANDLERS_MAPPING",
    "RESULT_SCHEMA",
]

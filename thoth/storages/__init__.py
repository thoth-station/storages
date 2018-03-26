"""Storage and database adapters for Thoth."""

__name__ = 'thoth-storages'
__version__ = '0.0.12'

from .analyses import AnalysisResultsStore
from .buildlogs import BuildLogsStore
from .ceph import CephStore
from .graph import GraphDatabase
from .result_schema import RESULT_SCHEMA
from .solvers import SolverResultsStore


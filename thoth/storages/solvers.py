"""Adapter for storing solver results onto a persistence remote store."""

from .result_base import ResultStorageBase


class SolverResultsStore(ResultStorageBase):
    PATH_ENV_VAR = 'THOTH_CEPH_SOLVER_PATH'

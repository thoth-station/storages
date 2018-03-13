"""Adapter for storing solver results onto a persistence remote store."""

from .result_base import ResultStorageBase


class SolverResultsStore(ResultStorageBase):
    RESULT_TYPE = 'solver'

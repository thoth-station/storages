"""Adapter for storing analysis results onto a persistence remote store."""

from .result_base import ResultStorageBase


class AnalysisResultsStore(ResultStorageBase):
    RESULT_TYPE = 'analysis'

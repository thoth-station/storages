"""Adapter for storing analysis results onto a persistence remote store."""

from .result_base import ResultStorageBase


class AnalysisResultsStore(ResultStorageBase):
    PATH_ENV_VAR = 'THOTH_CEPH_ANALYSIS_PATH'

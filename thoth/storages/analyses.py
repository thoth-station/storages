"""Adapter for storing analysis results onto a persistence remote store."""

import os

import requests


class AnalysisResultsStore(object):
    """Adapter for storing analysis results."""

    def __init__(self, host: str=None):
        super().__init__()
        self.host = host or os.environ['THOTH_ANALYSIS_RESULTS_STORE_HOST']

    def retrieve_by_document_id(self, document_id: str) -> dict:
        """Retrieve document stored in analysis results store by its ID."""
        assert document_id.startswith('analysis-'), \
            "Please make sure you are calling right adapter to retrieve results."
        response = requests.get('{}/api/v1/result/{}'.format(self.host, document_id))
        response.raise_for_status()
        return response.json()

    def store_document(self, content: dict) -> str:
        """Store the given document content, return an ID of the stored document."""
        response = requests.post('{}/api/v1/analysis-result'.format(self.host), json=content)
        response.raise_for_status()
        return response.json()['document_id']

    def get_result_listing(self):
        """List all available analysis results stored."""
        response = requests.get('{}/api/v1/result?type=analysis'.format(self.host))
        response.raise_for_status()
        return response.json()['files']

    def is_connected(self) -> bool:
        return True

    def connect(self):
        return True

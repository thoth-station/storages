"""Adapter for storing solver results onto a persistence remote store."""

import os

import requests


class SolverResultsStore(object):
    """Adapter for storing solver results."""

    ENVVAR_HOST = 'THOTH_SOLVER_RESULTS_STORE_HOST'
    DEFAULT_HOST = os.getenv(ENVVAR_HOST) or 'http://localhost:8080'

    def __init__(self, host: str=None):
        super().__init__()
        self.host = host or self.DEFAULT_HOST

    def retrieve_by_document_id(self, document_id: str) -> dict:
        """Retrieve document stored in solver results store by its ID."""
        assert document_id.startswith('solver-'), "Please make sure you are calling right adapter to retrieve results."
        response = requests.get('{}/api/v1/result/{}'.format(self.host, document_id))
        response.raise_for_status()
        return response.json()

    def store_document(self, content: dict) -> str:
        """Store the given document content, return an ID of the stored document."""
        response = requests.post('{}/api/v1/solver-result'.format(self.host), json=content)
        response.raise_for_status()
        return response.json()['document_id']

    def get_result_listing(self):
        """List all available solver results stored."""
        response = requests.get('{}/api/v1/result?type=solver'.format(self.host))
        response.raise_for_status()
        return response.json()['files']

    def iterate_results(self):
        """Iterate over available solver results, yielding one document at the time."""
        for document_id in self.get_result_listing():
            document = self.retrieve_by_document_id(document_id)
            yield document_id, document

    def is_connected(self) -> bool:
        return True

    def connect(self):
        return True

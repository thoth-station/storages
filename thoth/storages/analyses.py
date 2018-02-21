"""Adapter for storing analysis results onto a persistence remote store."""

from selinon import DataStorage


class AnalysisResultsStore(DataStorage):
    """Adapter for storing analysis results."""

    def __init__(self, host: str):
        super().__init__()
        self.host = host

    def retrieve_by_document_id(self, document_id: str) -> dict:
        # TODO: implement
        pass

    def store_document(self, content: dict) -> str:
        # TODO: implement
        pass

    def is_connected(self) -> bool:
        return True

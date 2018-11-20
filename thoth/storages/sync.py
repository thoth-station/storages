#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2018 Fridolin Pokorny
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

"""Routines for syncing data from Ceph into graph database."""

import logging

from .solvers import SolverResultsStore
from .analyses import AnalysisResultsStore
from .graph import GraphDatabase

_LOGGER = logging.getLogger(__name__)


def sync_solver_documents(document_ids: list = None, force: bool = False,
                          graceful: bool = False) -> tuple:
    """Sync solver documents into graph."""
    graph = GraphDatabase()
    graph.connect()

    solver_store = SolverResultsStore()
    solver_store.connect()

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in document_ids or solver_store.get_document_listing():
        processed += 1
        if force or not graph.solver_document_id_exist(document_id):
            _LOGGER.info(
                f"Syncing solver document from {solver_store.ceph.host} "
                f"with id {document_id!r} to graph {graph.hosts}"
            )

            try:
                document = solver_store.retrieve_document(document_id)
                graph.sync_solver_result(document)
                synced += 1
            except Exception:
                if not graceful:
                    raise

                _LOGGER.exception("Failed to sync solver result with document id %r", document_id)
                failed += 1
        else:
            _LOGGER.info(f"Sync of solver document with id {document_id!r} skipped - already synced")
            skipped += 1

    return processed, synced, skipped, failed


def sync_analysis_documents(document_ids: list = None, force: bool = False,
                            graceful: bool = False) -> tuple:
    """Sync image analysis documents into graph."""
    graph = GraphDatabase()
    graph.connect()

    analysis_store = AnalysisResultsStore()
    analysis_store.connect()

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in document_ids or analysis_store.get_document_listing():
        processed += 1

        if force or not graph.analysis_document_id_exist(document_id):
            _LOGGER.info(
                f"Syncing analysis document from {analysis_store.ceph.host} "
                f"with id {document_id!r} to graph {graph.hosts}"
            )

            try:
                document = analysis_store.retrieve_document(document_id)
                graph.sync_analysis_result(document)
                synced += 1
            except Exception:
                if not graceful:
                    raise

                _LOGGER.exception("Failed to sync analysis result with document id %r", document_id)
                failed += 1
        else:
            _LOGGER.info(f"Sync of analysis document with id {document_id!r} skipped - already synced")
            skipped += 1

    return processed, synced, skipped, failed

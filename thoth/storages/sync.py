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

from amun import get_inspection_build_log
from amun import get_inspection_job_log
from amun import get_inspection_specification
from amun import get_inspection_status
from amun import is_inspection_finished
from amun import has_inspection_job

from .solvers import SolverResultsStore
from .analyses import AnalysisResultsStore
from .inspections import InspectionResultsStore
from .dependency_monkey_reports import DependencyMonkeyReportsStore
from .graph import GraphDatabase

_LOGGER = logging.getLogger(__name__)


def sync_solver_documents(document_ids: list = None, force: bool = False, graceful: bool = False) -> tuple:
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


def sync_analysis_documents(document_ids: list = None, force: bool = False, graceful: bool = False) -> tuple:
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


def sync_inspection_documents(
    amun_api_url: str, document_ids: list = None, force_sync: bool = False, graceful: bool = False
) -> tuple:
    """Sync observations made on Amun into graph databaes."""
    inspection_store = InspectionResultsStore()
    inspection_store.connect()

    dependency_mokey_reports_store = DependencyMonkeyReportsStore()
    dependency_mokey_reports_store.connect()

    graph = GraphDatabase()
    graph.connect()

    processed, synced, skipped, failed = 0, 0, 0, 0
    for inspection_id in document_ids or dependency_mokey_reports_store.iterate_inspection_ids():
        processed += 1
        if force_sync or not inspection_store.document_exists(inspection_id):
            finished = is_inspection_finished(amun_api_url, inspection_id)

            if finished:
                _LOGGER.info("Obtaining results from Amun API for inspection %r", inspection_id)
                try:
                    specification = get_inspection_specification(amun_api_url, inspection_id)
                    build_log = get_inspection_build_log(amun_api_url, inspection_id)
                    status = get_inspection_status(amun_api_url, inspection_id)
                    job_log = None
                    if has_inspection_job(amun_api_url, inspection_id):
                        job_log = get_inspection_job_log(amun_api_url, inspection_id)

                    document = {
                        "specification": specification,
                        "build_log": build_log,
                        "job_log": job_log,
                        "inspection_id": inspection_id,
                        "status": status,
                    }

                    # First we store results into graph database and then onto
                    # Ceph. This way in the next run we can sync documents that
                    # failed to sync to graph - see if statement that is asking
                    # for Ceph document presents first.
                    _LOGGER.info(f"Syncing inspection {inspection_id!r} to {graph.hosts}")
                    graph.sync_inspection_result(document)
                    _LOGGER.info(f"Syncing inspection {inspection_id!r} to {inspection_store.ceph.host}")
                    inspection_store.store_document(document)
                    synced += 1
                except Exception as exc:
                    if not graceful:
                        raise

                    _LOGGER.exception(f"Failed to sync inspection %r: %s", inspection_id, str(exc))
                    failed += 1
            else:
                _LOGGER.info(f"Skipping inspection {inspection_id!r} - not finised yet")
                skipped += 1
        else:
            _LOGGER.info(f"Skipping inspection {inspection_id!r} - the given inspection is already synced")
            skipped += 1

    return processed, synced, skipped, failed

#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2018, 2019 Fridolin Pokorny
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
from .advisers import AdvisersResultsStore
from .inspections import InspectionResultsStore
from .provenance import ProvenanceResultsStore
from .dependency_monkey_reports import DependencyMonkeyReportsStore
from .graph import GraphDatabase

_LOGGER = logging.getLogger(__name__)


def sync_adviser_documents(
        document_ids: list = None,
        force: bool = False,
        graceful: bool = False,
        graph: GraphDatabase = None,
) -> tuple:
    """Sync adviser documents into graph."""
    if not graph:
        graph = GraphDatabase()
        graph.connect()

    adviser_store = AdvisersResultsStore()
    adviser_store.connect()

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in document_ids or adviser_store.get_document_listing():
        processed += 1

        if force or not graph.adviser_document_id_exist(document_id):
            _LOGGER.info(
                f"Syncing adviser document from {adviser_store.ceph.host} "
                f"with id {document_id!r} to graph {graph.hosts}"
            )

            try:
                document = adviser_store.retrieve_document(document_id)
                graph.sync_adviser_result(document)
                synced += 1
            except Exception:
                if not graceful:
                    raise

                _LOGGER.exception("Failed to sync adviser result with document id %r", document_id)
                failed += 1
        else:
            _LOGGER.info(f"Sync of adviser document with id {document_id!r} skipped - already synced")
            skipped += 1

    return processed, synced, skipped, failed


def sync_solver_documents(
        document_ids: list = None,
        force: bool = False,
        graceful: bool = False,
        graph: GraphDatabase = None,
) -> tuple:
    """Sync solver documents into graph."""
    if not graph:
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


def sync_analysis_documents(
        document_ids: list = None,
        force: bool = False,
        graceful: bool = False,
        graph: GraphDatabase = None,
) -> tuple:
    """Sync image analysis documents into graph."""
    if not graph:
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


def sync_provenance_checker_documents(
        document_ids: list = None,
        force: bool = False,
        graceful: bool = False,
        graph: GraphDatabase = None,
) -> tuple:
    """Sync provenance check documents into graph."""
    if not graph:
        graph = GraphDatabase()
        graph.connect()

    provenance_check_store = ProvenanceResultsStore()
    provenance_check_store.connect()

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in document_ids or provenance_check_store.get_document_listing():
        processed += 1

        if force or not graph.provenance_checker_document_id_exist(document_id):
            _LOGGER.info(
                f"Syncing provenance-checker document from {provenance_check_store.ceph.host} "
                f"with id {document_id!r} to graph {graph.hosts}"
            )

            try:
                document = provenance_check_store.retrieve_document(document_id)
                graph.sync_provenance_checker_result(document)
                synced += 1
            except Exception:
                if not graceful:
                    raise

                _LOGGER.exception("Failed to sync provenance-checker result with document id %r", document_id)
                failed += 1
        else:
            _LOGGER.info(f"Sync of provenance-checker document with id {document_id!r} skipped - already synced")
            skipped += 1

    return processed, synced, skipped, failed


def sync_dependency_monkey_documents(
        document_ids: list = None,
        force: bool = False,
        graceful: bool = False,
        graph: GraphDatabase = None,
) -> tuple:
    """Sync dependency monkey reports into graph database."""
    if not graph:
        graph = GraphDatabase()
        graph.connect()

    dependency_monkey_reports_store = DependencyMonkeyReportsStore()
    dependency_monkey_reports_store.connect()

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in document_ids or dependency_monkey_reports_store.get_document_listing():
        processed += 1

        if force or not graph.dependency_monkey_document_id_exist(document_id):
            _LOGGER.info(
                f"Syncing dependency monkey report document from {dependency_monkey_reports_store.ceph.host} "
                f"with id {document_id!r} to graph {graph.hosts}"
            )

            try:
                document = dependency_monkey_reports_store.retrieve_document(document_id)
                graph.sync_dependency_monkey_result(document)
                synced += 1
            except Exception:
                if not graceful:
                    raise

                _LOGGER.exception("Failed to sync dependency-monkey result with document id %r", document_id)
                failed += 1
        else:
            _LOGGER.info(f"Sync of dependency-monkey document with id {document_id!r} skipped - already synced")
            skipped += 1

    return processed, synced, skipped, failed


def sync_inspection_documents(
    amun_api_url: str,
    document_ids: list = None,
    *,
    force_sync: bool = False,
    graceful: bool = False,
    only_graph_sync: bool = False,
    only_ceph_sync: bool = False,
    graph: GraphDatabase = None,
) -> tuple:
    """Sync observations made on Amun into graph databaes."""
    if only_graph_sync and only_ceph_sync:
        raise ValueError("At least one of Ceph or Graph should be performed")

    inspection_store = InspectionResultsStore()
    inspection_store.connect()

    dependency_monkey_reports_store = DependencyMonkeyReportsStore()
    dependency_monkey_reports_store.connect()

    if not graph:
        graph = GraphDatabase()
        graph.connect()

    processed, synced, skipped, failed = 0, 0, 0, 0
    for inspection_id in document_ids or dependency_monkey_reports_store.iterate_inspection_ids():
        processed += 1
        if force_sync or not inspection_store.document_exists(inspection_id):
            finished = is_inspection_finished(amun_api_url, inspection_id)

            if finished:
                _LOGGER.info("Obtaining results from Amun API for inspection %r", inspection_id)
                try:
                    specification, created = get_inspection_specification(amun_api_url, inspection_id)
                    build_log = get_inspection_build_log(amun_api_url, inspection_id)
                    status = get_inspection_status(amun_api_url, inspection_id)
                    job_log = None
                    if has_inspection_job(amun_api_url, inspection_id):
                        job_log = get_inspection_job_log(amun_api_url, inspection_id)

                    document = {
                        "specification": specification,
                        "created": created,
                        "build_log": build_log,
                        "job_log": job_log,
                        "inspection_id": inspection_id,
                        "status": status,
                    }

                    # First we store results into graph database and then onto
                    # Ceph. This way in the next run we can sync documents that
                    # failed to sync to graph - see if statement that is asking
                    # for Ceph document presents first.
                    if not only_ceph_sync:
                        _LOGGER.info(f"Syncing inspection {inspection_id!r} to {graph.hosts}")
                        graph.sync_inspection_result(document)

                    if not only_graph_sync:
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

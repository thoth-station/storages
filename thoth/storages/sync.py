#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2018, 2019, 2020 Fridolin Pokorny
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
import json
import os
from typing import Dict
from typing import Tuple
from typing import List
from typing import Optional

from amun import get_inspection_build_log
from amun import get_inspection_specification
from amun import get_inspection_status
from amun import is_inspection_finished
from amun import has_inspection_job

from .solvers import SolverResultsStore
from .revsolvers import RevSolverResultsStore
from .analyses import AnalysisResultsStore
from .buildlogs_analyses import BuildLogsAnalysisResultsStore
from .package_analyses import PackageAnalysisResultsStore
from .advisers import AdvisersResultsStore
from .inspections import InspectionResultsStore
from .provenance import ProvenanceResultsStore
from .dependency_monkey_reports import DependencyMonkeyReportsStore
from .graph import GraphDatabase

_LOGGER = logging.getLogger(__name__)


def sync_adviser_documents(
    document_ids: Optional[List[str]] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    is_local: bool = False,
) -> tuple:
    """Sync adviser documents into graph."""
    if is_local and not document_ids:
        raise ValueError(
            "Cannot sync documents from local directory without explicitly specifying a list of documents to be synced"
        )

    if not graph:
        graph = GraphDatabase()
        graph.connect()

    if not is_local:
        adviser_store = AdvisersResultsStore()
        adviser_store.connect()

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in document_ids or adviser_store.get_document_listing():
        processed += 1

        if force or not graph.adviser_document_id_exist(os.path.basename(document_id)):
            try:
                if is_local:
                    _LOGGER.debug("Loading document from a local file: %r", document_id)
                    with open(document_id, "r") as document_file:
                        document = json.loads(document_file.read())
                else:
                    _LOGGER.info(
                        "Syncing adviser document from %r with id %r to graph", adviser_store.ceph.host, document_id
                    )
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
    document_ids: Optional[List[str]] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    is_local: bool = False,
) -> tuple:
    """Sync solver documents into graph."""
    if is_local and not document_ids:
        raise ValueError(
            "Cannot sync documents from local directory without explicitly specifying a list of documents to be synced"
        )

    if not graph:
        graph = GraphDatabase()
        graph.connect()

    if not is_local:
        solver_store = SolverResultsStore()
        solver_store.connect()

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in document_ids or solver_store.get_document_listing():
        processed += 1
        if force or not graph.solver_document_id_exist(os.path.basename(document_id)):
            try:
                if is_local:
                    _LOGGER.debug("Loading document from a local file: %r", document_id)
                    with open(document_id, "r") as document_file:
                        document = json.loads(document_file.read())
                else:
                    _LOGGER.info(
                        "Syncing solver document from %r with id %r to graph", solver_store.ceph.host, document_id
                    )
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


def sync_revsolver_documents(
    document_ids: Optional[List[str]] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    is_local: bool = False,
) -> tuple:
    """Sync reverse solver documents into graph."""
    if is_local and not document_ids:
        raise ValueError(
            "Cannot sync documents from local directory without explicitly specifying a list of documents to be synced"
        )

    if not graph:
        graph = GraphDatabase()
        graph.connect()

    if not is_local:
        revsolver_store = RevSolverResultsStore()
        revsolver_store.connect()

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in document_ids or revsolver_store.get_document_listing():
        processed += 1
        try:
            if is_local:
                _LOGGER.debug("Loading document from a local file: %r", document_id)
                with open(document_id, "r") as document_file:
                    document = json.loads(document_file.read())
            else:
                _LOGGER.info(
                    "Syncing reverse solver document from %r with id %r to graph",
                    revsolver_store.ceph.host,
                    document_id
                )
                document = revsolver_store.retrieve_document(document_id)

            graph.sync_revsolver_result(document)
            synced += 1
        except Exception:
            if not graceful:
                raise

            _LOGGER.exception("Failed to sync reverse solver result with document id %r", document_id)
            failed += 1

    return processed, synced, skipped, failed


def sync_analysis_documents(
    document_ids: Optional[List[str]] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    is_local: bool = False,
) -> tuple:
    """Sync image analysis documents into graph."""
    if is_local and not document_ids:
        raise ValueError(
            "Cannot sync documents from local directory without explicitly specifying a list of documents to be synced"
        )

    if not graph:
        graph = GraphDatabase()
        graph.connect()

    if not is_local:
        analysis_store = AnalysisResultsStore()
        analysis_store.connect()

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in document_ids or analysis_store.get_document_listing():
        processed += 1

        if force or not graph.analysis_document_id_exist(os.path.basename(document_id)):
            try:
                if is_local:
                    _LOGGER.debug("Loading document from a local file: %r", document_id)
                    with open(document_id, "r") as document_file:
                        document = json.loads(document_file.read())
                else:
                    _LOGGER.info(
                        "Syncing analysis document from %r with id %r to graph", analysis_store.ceph.host, document_id
                    )
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


def sync_build_log_analysis_documents(
    document_ids: Optional[List[str]] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    is_local: bool = False,
) -> tuple:
    """Sync build log analysis documents into graph."""
    if is_local and not document_ids:
        raise ValueError(
            "Cannot sync documents from local directory without explicitly specifying a list of documents to be synced"
        )

    if not graph:
        graph = GraphDatabase()
        graph.connect()

    if not is_local:
        build_log_analysis_store = BuildLogsAnalysisResultsStore()
        build_log_analysis_store.connect()

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in document_ids or buildlog_analysis_store.get_document_listing():
        processed += 1

        if force or not graph.build_log_analysis_document_id_exist(os.path.basename(document_id)):
            try:
                if is_local:
                    _LOGGER.debug("Loading document from a local file: %r", document_id)
                    with open(document_id, "r") as document_file:
                        document = json.loads(document_file.read())
                else:
                    _LOGGER.info(
                        "Syncing build log analysis document from %r with id %r to graph",
                        build_log_analysis_store.ceph.host,
                        document_id,
                    )
                    document = build_log_analysis_store.retrieve_document(document_id)
                # Analysis results with no information are not required
                if document["result"]["build_breaker"]:
                    graph.sync_build_log_analysis_result(document)
                    synced += 1
            except Exception:
                if not graceful:
                    raise

                _LOGGER.exception("Failed to sync build log analysis result with document id %r", document_id)
                failed += 1
        else:
            _LOGGER.info("Sync of build log analysis document with id %r skipped - already synced", document_id)
            skipped += 1

    return processed, synced, skipped, failed


def sync_package_analysis_documents(
    document_ids: Optional[List[str]] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    is_local: bool = False,
) -> tuple:
    """Sync package analysis documents into graph."""
    if is_local and not document_ids:
        raise ValueError(
            "Cannot sync documents from local directory without explicitly specifying a list of documents to be synced"
        )

    if not graph:
        graph = GraphDatabase()
        graph.connect()

    if not is_local:
        package_analysis_store = PackageAnalysisResultsStore()
        package_analysis_store.connect()

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in document_ids or package_analysis_store.get_document_listing():
        processed += 1

        if force or not graph.package_analysis_document_id_exist(os.path.basename(document_id)):
            try:
                if is_local:
                    _LOGGER.debug("Loading document from a local file: %r", document_id)
                    with open(document_id, "r") as document_file:
                        document = json.loads(document_file.read())
                else:
                    _LOGGER.info(
                        "Syncing package analysis document from %r with id %r to graph",
                        package_analysis_store.ceph.host,
                        document_id,
                    )
                    document = package_analysis_store.retrieve_document(document_id)

                graph.sync_package_analysis_result(document)
                synced += 1
            except Exception:
                if not graceful:
                    raise

                _LOGGER.exception("Failed to sync package analysis result with document id %r", document_id)
                failed += 1
        else:
            _LOGGER.info(f"Sync of package analysis document with id {document_id!r} skipped - already synced")
            skipped += 1

    return processed, synced, skipped, failed


def sync_provenance_checker_documents(
    document_ids: Optional[List[str]] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    is_local: bool = False,
) -> tuple:
    """Sync provenance check documents into graph."""
    if is_local and not document_ids:
        raise ValueError(
            "Cannot sync documents from local directory without explicitly specifying a list of documents to be synced"
        )

    if not graph:
        graph = GraphDatabase()
        graph.connect()

    if not is_local:
        provenance_check_store = ProvenanceResultsStore()
        provenance_check_store.connect()

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in document_ids or provenance_check_store.get_document_listing():
        processed += 1

        if force or not graph.provenance_checker_document_id_exist(os.path.basename(document_id)):
            try:
                if is_local:
                    _LOGGER.debug("Loading document from a local file: %r", document_id)
                    with open(document_id, "r") as document_file:
                        document = json.loads(document_file.read())
                else:
                    _LOGGER.info(
                        "Syncing provenance-checker document from %r with id %r to graph",
                        provenance_check_store.ceph.host,
                        document_id,
                    )
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
    document_ids: Optional[List[str]] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    is_local: bool = False,
) -> tuple:
    """Sync dependency monkey reports into graph database."""
    if is_local and not document_ids:
        raise ValueError(
            "Cannot sync documents from local directory without explicitly specifying a list of documents to be synced"
        )

    if not graph:
        graph = GraphDatabase()
        graph.connect()

    if not is_local:
        dependency_monkey_reports_store = DependencyMonkeyReportsStore()
        dependency_monkey_reports_store.connect()

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in document_ids or dependency_monkey_reports_store.get_document_listing():
        processed += 1

        if force or not graph.dependency_monkey_document_id_exist(os.path.basename(document_id)):
            try:
                if is_local:
                    _LOGGER.debug("Loading document from a local file: %r", document_id)
                    with open(document_id, "r") as document_file:
                        document = json.loads(document_file.read())
                else:
                    _LOGGER.info(
                        f"Syncing dependency monkey report document from %r with id %r to graph",
                        dependency_monkey_reports_store.ceph.host,
                        document_id,
                    )
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
    document_ids: Optional[List[str]] = None,
    *,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    amun_api_url: str,
    only_ceph_sync: bool = False,
    only_graph_sync: bool = False,
    is_local: bool = False,
) -> tuple:
    """Sync observations made on Amun into graph database."""
    from amun import get_inspection_job_log

    if is_local:
        raise NotImplementedError("Cannot sync inspection documents from a local file")

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
        if force or not inspection_store.document_exists(inspection_id):
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
                        _LOGGER.info(f"Syncing inspection {inspection_id!r} to graph")
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


# Corresponding mapping of document prefix (before the actual unique document identifier part) to
# functions which can handle the given document sync.

_HANDLERS_MAPPING = {
    "adviser": sync_adviser_documents,
    "build-report": sync_build_log_analysis_documents,
    "dependency-monkey": sync_dependency_monkey_documents,
    "inspection": sync_inspection_documents,
    "package-analyzer": sync_package_analysis_documents,
    "package-extract": sync_analysis_documents,
    "provenance-checker": sync_provenance_checker_documents,
    "solver": sync_solver_documents,
    "revsolver": sync_revsolver_documents,
}


def sync_documents(
    document_ids: Optional[List[str]] = None,
    *,
    amun_api_url: Optional[str] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    inspection_only_graph_sync: bool = False,
    inspection_only_ceph_sync: bool = False,
    is_local: bool = False,
) -> Dict[str, Tuple[int, int, int, int]]:
    """Sync documents based on document type.

    If no list of document ids is provided, all documents will be synced.
    >>> from thoth.storages.sync import sync_documents
    >>> sync_documents(["adviser-efa7213babd12911", "package-extract-f8e354d9597a1203"])
    """
    stats = dict.fromkeys(_HANDLERS_MAPPING, (0, 0, 0, 0))

    if inspection_only_ceph_sync and inspection_only_graph_sync:
        raise ValueError("Parameters `inspection_only_ceph_sync' and `inspection_only_graph_sync' are disjoint")

    for document_id in document_ids or [None] * len(_HANDLERS_MAPPING):
        for document_prefix, handler in _HANDLERS_MAPPING.items():
            # Basename for local syncs, document_id should not have slash otherwise.
            if document_id is None or os.path.basename(document_id).startswith(document_prefix):
                to_sync_document_id = [document_id] if document_id is not None else None
                if handler == sync_inspection_documents:
                    # A special case with additional arguments to obtain results from Amun API.
                    if amun_api_url is None:
                        error_msg = f"Cannot sync document with id {document_id!r} without specifying Amun API URL"
                        if not graceful:
                            raise ValueError(error_msg)

                        _LOGGER.error(error_msg)

                    stats_change = handler(
                        to_sync_document_id,
                        amun_api_url=amun_api_url,
                        force=force,
                        graceful=graceful,
                        graph=graph,
                        only_ceph_sync=inspection_only_ceph_sync,
                        only_graph_sync=inspection_only_graph_sync,
                        is_local=is_local,
                    )
                else:
                    stats_change = handler(
                        to_sync_document_id, force=force, graceful=graceful, graph=graph, is_local=is_local
                    )

                stats[document_prefix] = tuple(map(sum, zip(stats[document_prefix], stats_change)))
                if document_id is not None:
                    break
        else:
            if document_id is not None:
                error_msg = f"No handler defined for document identifier {document_id!r}"
                if not graceful:
                    raise ValueError(error_msg)

                _LOGGER.error(error_msg)

    return stats

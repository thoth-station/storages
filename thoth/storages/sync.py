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
import random
from typing import Dict
from typing import List
from typing import Iterable
from typing import Optional
from typing import Tuple
from pathlib import Path

from .analyses import AnalysisResultsStore
from .advisers import AdvisersResultsStore
from .dependency_monkey_reports import DependencyMonkeyReportsStore
from .inspections import InspectionStore
from .provenance import ProvenanceResultsStore
from .revsolvers import RevSolverResultsStore
from .security_indicators import SIAggregatedStore, SecurityIndicatorsResultsStore
from .solvers import SolverResultsStore

from .graph import GraphDatabase

_LOGGER = logging.getLogger(__name__)
_RANDOMIZE_LISTING = bool(int(os.getenv("THOTH_STORAGES_RANDOMIZE_LISTING", 0)))


def sync_adviser_documents(
    document_ids: Optional[Iterable[str]] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    is_local: bool = False,
) -> Tuple[int, int, int, int]:
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

    listing = document_ids or adviser_store.get_document_listing()

    if _RANDOMIZE_LISTING:
        random.shuffle(list(listing))

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in listing:
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
    document_ids: Optional[Iterable[str]] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    is_local: bool = False,
) -> Tuple[int, int, int, int]:
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

    listing = document_ids or solver_store.get_document_listing()

    if _RANDOMIZE_LISTING:
        random.shuffle(list(listing))

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in listing:
        processed += 1
        if force or not graph.solver_document_id_exists(os.path.basename(document_id)):
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

                graph.sync_solver_result(document, force=force)
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
    document_ids: Optional[Iterable[str]] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    is_local: bool = False,
) -> Tuple[int, int, int, int]:
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

    listing = document_ids or revsolver_store.get_document_listing()

    if _RANDOMIZE_LISTING:
        random.shuffle(list(listing))

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in listing:
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
                    document_id,
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
    document_ids: Optional[Iterable[str]] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    is_local: bool = False,
) -> Tuple[int, int, int, int]:
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

    listing = document_ids or analysis_store.get_document_listing()

    if _RANDOMIZE_LISTING:
        random.shuffle(list(listing))

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in listing:
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


def sync_provenance_checker_documents(
    document_ids: Optional[Iterable[str]] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    is_local: bool = False,
) -> Tuple[int, int, int, int]:
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

    listing = document_ids or provenance_check_store.get_document_listing()

    if _RANDOMIZE_LISTING:
        random.shuffle(list(listing))

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in listing:
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
    document_ids: Optional[Iterable[str]] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    is_local: bool = False,
) -> Tuple[int, int, int, int]:
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

    listing = document_ids or dependency_monkey_reports_store.get_document_listing()

    if _RANDOMIZE_LISTING:
        random.shuffle(list(listing))

    processed, synced, skipped, failed = 0, 0, 0, 0
    for document_id in listing:
        processed += 1

        if force or not graph.dependency_monkey_document_id_exists(os.path.basename(document_id)):
            try:
                if is_local:
                    _LOGGER.debug("Loading document from a local file: %r", document_id)
                    with open(document_id, "r") as document_file:
                        document = json.loads(document_file.read())
                else:
                    _LOGGER.info(
                        f"Syncing dependency monkey report document from "
                        f"{dependency_monkey_reports_store.ceph.host} with id "
                        f"{document_id}, to graph"
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
    document_ids: Optional[Iterable[str]] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    is_local: bool = False,
) -> Tuple[int, int, int, int]:
    """Sync observations made on Amun into graph database."""
    if is_local and not document_ids:
        raise ValueError(
            "Cannot sync documents from local directory without explicitly specifying a list of documents to be synced"
        )

    if not graph:
        graph = GraphDatabase()
        graph.connect()

    listing = document_ids or InspectionStore.iter_inspections()

    if _RANDOMIZE_LISTING:
        random.shuffle(list(listing))

    processed, synced, skipped, failed = 0, 0, 0, 0
    for inspection_document_id in listing:

        if not is_local:
            results = []
            inspection_store = InspectionStore(inspection_id=inspection_document_id)
            inspection_store.connect()

            number_results = inspection_store.results.get_results_count()
        else:
            main_repo = Path(f"{inspection_document_id}/results")
            results = [int(repo.name) for repo in main_repo.iterdir()]
            # dir entry should be numbers

        if number_results > 0:

            for inspection_result_number in results or range(number_results):

                processed += 1
                try:
                    if force or not graph.inspection_document_id_result_number_exists(
                        inspection_document_id=inspection_document_id, inspection_result_number=inspection_result_number
                    ):
                        if is_local:

                            inspection_specification_path = f"{inspection_document_id}/build/specification"
                            _LOGGER.debug(
                                "Loading specification document from a local file: %r", inspection_specification_path
                            )

                            inspection_result_path = (
                                f"{inspection_document_id}/results/{inspection_result_number}/result"
                            )
                            _LOGGER.debug("Loading result document from a local file: %r", inspection_result_path)

                            with open(inspection_specification_path, "r") as document_file:
                                inspection_specification_document = json.loads(document_file.read())

                            with open(inspection_result_path, "r") as document_file:
                                inspection_result_document = json.loads(document_file.read())
                        else:
                            _LOGGER.info(
                                "Syncing analysis document from %r with id %r and number %r to graph",
                                inspection_store.results.ceph.host,
                                inspection_document_id,
                                inspection_result_number,
                            )

                            inspection_specification_document = inspection_store.retrieve_specification()
                            inspection_result_document = inspection_store.results.retrieve_result(
                                inspection_result_number
                            )

                        inspection_document = {
                            "document_id": inspection_document_id,
                            "result_number": inspection_result_number,
                            "specification": inspection_specification_document,
                            "result": inspection_result_document,
                        }

                        graph.sync_inspection_result(inspection_document)
                        synced += 1

                    else:
                        _LOGGER.info(
                            f"Sync of results n.{inspection_result_number!r}"
                            f" from inspection id {inspection_document_id!r} skipped - already synced"
                        )
                        skipped += 1

                except Exception:
                    if not graceful:
                        raise

                    _LOGGER.exception(
                        f"Failed to sync results n.{inspection_result_number!r}"
                        f" from inspection id {inspection_document_id!r}"
                    )
                    failed += 1

        else:
            _LOGGER.info(f"inspection_document_id: {inspection_document_id!r} - does not have any results.")

    return processed, synced, skipped, failed


def sync_security_indicators_documents(
    document_ids: Optional[Iterable[str]] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    is_local: bool = False,
) -> Tuple[int, int, int, int]:
    """Sync security indicators results into graph."""
    if is_local and not document_ids:
        raise ValueError(
            "Cannot sync documents from local directory without explicitly specifying a list of documents to be synced"
        )

    if not graph:
        graph = GraphDatabase()
        graph.connect()

    listing = document_ids or SecurityIndicatorsResultsStore.iter_security_indicators()

    if _RANDOMIZE_LISTING:
        random.shuffle(list(listing))

    processed, synced, skipped, failed = 0, 0, 0, 0
    for security_indicator_id in listing:

        processed += 1

        if force or not graph.si_aggregated_document_id_exists(security_indicator_id):
            try:
                if is_local:
                    _LOGGER.debug("Loading document from a local file: %r", security_indicator_id)
                    with open(security_indicator_id, "r") as document_file:
                        aggregated_document = json.loads(document_file.read())
                else:
                    si_aggregated_store = SIAggregatedStore(security_indicator_id=security_indicator_id)
                    si_aggregated_store.connect()
                    _LOGGER.info(
                        "Syncing analysis document from %r with id %r to graph",
                        si_aggregated_store.ceph.host,
                        security_indicator_id,
                    )

                    aggregated_document = si_aggregated_store.retrieve_document()

                graph.sync_security_indicator_aggregated_result(aggregated_document)
                synced += 1
            except Exception:
                if not graceful:
                    raise

                _LOGGER.exception("Failed to sync analysis result with document id %r", security_indicator_id)
                failed += 1
        else:
            _LOGGER.info(f"Sync of analysis document with id {security_indicator_id!r} skipped - already synced")
            skipped += 1

    return processed, synced, skipped, failed


# Corresponding mapping of document prefix (before the actual unique document identifier part) to
# functions which can handle the given document sync.

HANDLERS_MAPPING = {
    "adviser": sync_adviser_documents,
    "dependency": sync_dependency_monkey_documents,
    "inspection": sync_inspection_documents,
    "package": sync_analysis_documents,
    "provenance": sync_provenance_checker_documents,
    "solver": sync_solver_documents,
    "revsolver": sync_revsolver_documents,
    "security": sync_security_indicators_documents,
}


def sync_documents(
    document_ids: Optional[Iterable[str]] = None,
    force: bool = False,
    graceful: bool = False,
    graph: Optional[GraphDatabase] = None,
    is_local: bool = False,
) -> Dict[str, Tuple[int, int, int, int]]:
    """Sync documents based on document type.

    If no list of document ids is provided, all documents will be synced.
    >>> from thoth.storages.sync import sync_documents
    >>> sync_documents(["adviser-efa7213babd12911", "package-extract-f8e354d9597a1203"])
    """
    handlers: Dict[str, List[str]] = dict()
    if document_ids:
        handlers = {key: [] for key in HANDLERS_MAPPING.keys()}
        assert handlers is not None
        for doc in document_ids:
            try:
                handlers[doc[doc.rfind("/") + 1 : doc.find("-")]].append(doc)
                # Basename for local syncs, document_id should not have slash otherwise.
            except KeyError:
                error_msg = f"No handler defined for document identifier {doc}"
                if not graceful:
                    raise ValueError(error_msg)
                _LOGGER.error(error_msg)

    else:
        static_handlers = dict.fromkeys(HANDLERS_MAPPING, None)

    stats = dict.fromkeys(HANDLERS_MAPPING, (0, 0, 0, 0))
    for handler, documents in (handlers or static_handlers).items():
        if documents != []:
            stats[handler] = HANDLERS_MAPPING[handler](
                documents, force=force, graceful=graceful, graph=graph, is_local=is_local
            )

    return stats

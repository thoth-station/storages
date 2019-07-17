#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2019 Fridolin Pokorny
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

"""Performance indicators (models) used in Thoth with their schemas."""

from functools import partial
import logging

import attr

from voluptuous import Required
from voluptuous import Schema

from .models_base import VertexBase
from .models_base import ReverseEdgeBase
from .models_base import model_property


_LOGGER = logging.getLogger(__name__)


@attr.s(slots=True)
class ObservedPerformance(ReverseEdgeBase):
    """A class for representing connection to performance indicators."""

    # We can have multiple performance indicators, index them.
    performance_indicator_index = model_property(type=int)


@attr.s(slots=True)
class PerformanceIndicatorBase(VertexBase):
    """A base class for implementing performance indicators."""

    SCHEMA_PARAMETERS = None
    SCHEMA_RESULT = None

    # ML framework used for the performance indicator.
    framework = model_property(type=str, index="exact")

    # Origin from where the performance indicator was obtained. In case of Git repo,
    # it holds Git repo URL, in case of URL it holds URL to the script.
    origin = model_property(type=str, index="exact")

    # Reference of the script, in case of Git repo it holds commit SHA, in case of URL it carries
    # SHA256 of the script which was used to test the performance with (performance indicator script).
    version = model_property(type=str, index="exact")

    # This one is used later on in queries in adviser, all the relevant performance indicators should
    # respect this property and place results in there.
    overall_score = model_property(type=float)

    # The actual exit code of the performance indicator.
    exit_code = model_property(type=int)

    # Time spent on CPU.
    cpu_utime = model_property(type=float)
    cpu_stime = model_property(type=float)
    cpu_cutime = model_property(type=float)
    cpu_cstime = model_property(type=float)
    cpu_total_time = model_property(type=float)

    @classmethod
    def create_from_report(cls, inspection_document: dict) -> "PerformanceIndicatorBase":
        """Create performance indicator record together with related observed performance edge based on inspection."""
        # Place core parts of the base class into the model.
        framework = inspection_document["job_log"]["stdout"].get("framework")
        if not framework:
            _LOGGER.warning("No machine learning framework specified in performance indicator %r", cls.__name__)

        overall_score = inspection_document["job_log"]["stdout"].get("overall_score")
        if overall_score is None:
            _LOGGER.warning("No overall score detected in performance indicator %r", overall_score)

        partial_model = partial(
            cls.from_properties,
            framework=framework,
            origin=inspection_document["specification"]["script"],
            version=inspection_document["job_log"]["stdout"].get("version")
            or inspection_document["job_log"]["script_sha256"],
            overall_score=overall_score,
            exit_code=inspection_document["job_log"].get("exit_code"),
            cpu_utime=inspection_document["job_log"].get("utime"),
            cpu_stime=inspection_document["job_log"].get("stime"),
            cpu_cutime=inspection_document["job_log"].get("cutime"),
            cpu_cstime=inspection_document["job_log"].get("cstime"),
            cpu_total_time=inspection_document["job_log"].get("total_time"),
        )

        if cls.SCHEMA_PARAMETERS:
            cls.SCHEMA_PARAMETERS(inspection_document["job_log"]["stdout"]["@parameters"])

        if cls.SCHEMA_RESULT:
            cls.SCHEMA_RESULT(inspection_document["job_log"]["stdout"]["@result"])

        return cls.from_report(inspection_document, partial_model)

    @classmethod
    def from_report(cls, inspection_document: dict, partial_model: type(partial)) -> "PerformanceIndicatorBase":
        """Create model from the inspection report respecting parameters and result reported by the indicator."""
        kwargs = {}
        for parameter, parameter_value in inspection_document["job_log"]["stdout"]["@parameters"].items():
            kwargs[parameter] = parameter_value

        for result_name, result_value in inspection_document["job_log"]["stdout"]["@result"].items():
            if result_name in kwargs:
                raise ValueError("Collision in result name and parameter name")

            kwargs[result_name] = result_value

        return partial_model(**kwargs)


@attr.s(slots=True)
class PiMatmul(PerformanceIndicatorBase):
    """A class for representing a matrix multiplication micro-performance test."""

    SCHEMA_PARAMETERS = Schema(
        {Required("matrix_size"): int, Required("dtype"): str, Required("reps"): int, Required("device"): str}
    )

    SCHEMA_RESULT = Schema({Required("elapsed"): float, Required("rate"): float})

    # Device used during performance indicator run - CPU/GPU/TPU/...
    device = model_property(type=str, index="exact")

    # Size of the metrix tested.
    matrix_size = model_property(type=int, index="int")

    # Type of item in the metrix.
    dtype = model_property(type=str, index="exact")

    # Number of repetitions of matrix multiplication performed.
    reps = model_property(type=int, index="int")

    # Elapsed seconds.
    elapsed = model_property(type=float)

    # Final rate gflops/s.
    rate = model_property(type=float)


ALL_PERFORMANCE_MODELS = frozenset((ObservedPerformance, PiMatmul))


PERFORMANCE_MODEL_BY_NAME = {model_class.__name__: model_class for model_class in ALL_PERFORMANCE_MODELS}

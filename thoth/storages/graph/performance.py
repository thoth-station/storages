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

    # Process statistics:
    #   https://docs.python.org/3/library/resource.html#resource.getrusage
    ru_utime = model_property(type=float)
    ru_stime = model_property(type=float)
    ru_maxrss = model_property(type=int)
    ru_ixrss = model_property(type=int)
    ru_idrss = model_property(type=int)
    ru_isrss = model_property(type=int)
    ru_minflt = model_property(type=int)
    ru_majflt = model_property(type=int)
    ru_nswap = model_property(type=int)
    ru_inblock = model_property(type=int)
    ru_oublock = model_property(type=int)
    ru_msgsnd = model_property(type=int)
    ru_msgrcv = model_property(type=int)
    ru_nsignals = model_property(type=int)
    ru_nvcsw = model_property(type=int)
    ru_nivcsw = model_property(type=int)

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
            ru_utime=inspection_document["job_log"].get("usage", {}).get("ru_utime"),
            ru_stime=inspection_document["job_log"].get("usage", {}).get("ru_stime"),
            ru_maxrss=inspection_document["job_log"].get("usage", {}).get("ru_maxrss"),
            ru_ixrss=inspection_document["job_log"].get("usage", {}).get("ru_ixrss"),
            ru_idrss=inspection_document["job_log"].get("usage", {}).get("ru_idrss"),
            ru_isrss=inspection_document["job_log"].get("usage", {}).get("ru_isrss"),
            ru_minflt=inspection_document["job_log"].get("usage", {}).get("ru_minflt"),
            ru_majflt=inspection_document["job_log"].get("usage", {}).get("ru_majflt"),
            ru_nswap=inspection_document["job_log"].get("usage", {}).get("ru_nswap"),
            ru_inblock=inspection_document["job_log"].get("usage", {}).get("ru_inblock"),
            ru_oublock=inspection_document["job_log"].get("usage", {}).get("ru_oublock"),
            ru_msgsnd=inspection_document["job_log"].get("usage", {}).get("ru_msgsnd"),
            ru_msgrcv=inspection_document["job_log"].get("usage", {}).get("ru_msgrcv"),
            ru_nsignals=inspection_document["job_log"].get("usage", {}).get("ru_nsignals"),
            ru_nvcsw=inspection_document["job_log"].get("usage", {}).get("ru_nvcsw"),
            ru_nivcsw=inspection_document["job_log"].get("usage", {}).get("ru_nivcsw"),
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

    # Size of the matrix tested.
    matrix_size = model_property(type=int, index="int")

    # Type of item in the matrix.
    dtype = model_property(type=str, index="exact")

    # Number of repetitions of matrix multiplication performed.
    reps = model_property(type=int, index="int")

    # Elapsed seconds.
    elapsed = model_property(type=float)

    # Final rate gflops/s.
    rate = model_property(type=float)


@attr.s(slots=True)
class PiConv1D(PerformanceIndicatorBase):
    """A class for representing a conv1D micro-performance test."""

    SCHEMA_PARAMETERS = Schema(
        {
            Required("dtype"): str,
            Required("reps"): int,
            Required("device"): str,
            Required("data_format"): str,
            Required("batch"): int,
            Required("input_width"): int,
            Required("input_channels"): int,
            Required("filter_width"): int,
            Required("output_channels"): int,
            Required("strides"): int,
            Required("padding"): int,
        }
    )

    SCHEMA_RESULT = Schema({Required("elapsed"): float, Required("rate"): float})

    # Device used during performance indicator run - CPU/GPU/TPU/...
    device = model_property(type=str, index="exact")

    # Type of item in the tensor.
    dtype = model_property(type=str, index="exact")

    # Number of repetitions of conv2d performed.
    reps = model_property(type=int, index="int")

    # Data format NHWC Channel_last or NCHW Channel_first
    data_format = model_property(type=str, index="exact")

    # INPUT TENSOR
    batch = model_property(type=int, index="int")
    input_width = model_property(type=int, index="int")
    input_channels = model_property(type=int, index="int")

    # FILTER
    filter_width = model_property(type=int, index="int")
    output_channels = model_property(type=int, index="int")

    # Stride, the speed by which the filter moves across the image
    strides = model_property(type=int, index="int")

    # Padding
    padding = model_property(type=int, index="int")

    # Elapsed seconds.
    elapsed = model_property(type=float)

    # Final rate gflops/s.
    rate = model_property(type=float)


@attr.s(slots=True)
class PiConv2D(PerformanceIndicatorBase):
    """A class for representing a conv2D micro-performance test."""

    SCHEMA_PARAMETERS = Schema(
        {
            Required("dtype"): str,
            Required("reps"): int,
            Required("device"): str,
            Required("data_format"): str,
            Required("batch"): int,
            Required("input_height"): int,
            Required("input_width"): int,
            Required("input_channels"): int,
            Required("filter_height"): int,
            Required("filter_width"): int,
            Required("output_channels"): int,
            Required("strides"): int,
            Required("padding"): int,
        }
    )

    SCHEMA_RESULT = Schema({Required("elapsed"): float, Required("rate"): float})

    # Device used during performance indicator run - CPU/GPU/TPU/...
    device = model_property(type=str, index="exact")

    # Type of item in the tensor.
    dtype = model_property(type=str, index="exact")

    # Number of repetitions of conv2d performed.
    reps = model_property(type=int, index="int")

    # Data format NHWC Channel_last or NCHW Channel_first
    data_format = model_property(type=str, index="exact")

    # INPUT TENSOR
    batch = model_property(type=int, index="int")
    input_height = model_property(type=int, index="int")
    input_width = model_property(type=int, index="int")
    input_channels = model_property(type=int, index="int")

    # FILTER
    filter_height = model_property(type=int, index="int")
    filter_width = model_property(type=int, index="int")
    output_channels = model_property(type=int, index="int")

    # Stride, the speed by which the filter moves across the image
    strides = model_property(type=int, index="int")

    # Padding
    padding = model_property(type=int, index="int")

    # Elapsed seconds.
    elapsed = model_property(type=float)

    # Final rate gflops/s.
    rate = model_property(type=float)


ALL_PERFORMANCE_MODELS = frozenset((ObservedPerformance, PiMatmul, PiConv1D, PiConv2D))


PERFORMANCE_MODEL_BY_NAME = {model_class.__name__: model_class for model_class in ALL_PERFORMANCE_MODELS}

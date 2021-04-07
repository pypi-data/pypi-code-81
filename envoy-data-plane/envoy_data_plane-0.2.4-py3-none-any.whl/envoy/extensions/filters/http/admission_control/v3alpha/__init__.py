# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/filters/http/admission_control/v3alpha/admission_control.proto
# plugin: python-betterproto
from dataclasses import dataclass
from datetime import timedelta
from typing import List

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class AdmissionControl(betterproto.Message):
    """[#next-free-field: 6]"""

    # If set to false, the admission control filter will operate as a pass-
    # through filter. If the message is unspecified, the filter will be enabled.
    enabled: "_____config_core_v3__.RuntimeFeatureFlag" = betterproto.message_field(1)
    success_criteria: "AdmissionControlSuccessCriteria" = betterproto.message_field(
        2, group="evaluation_criteria"
    )
    # The sliding time window over which the success rate is calculated. The
    # window is rounded to the nearest second. Defaults to 30s.
    sampling_window: timedelta = betterproto.message_field(3)
    # Rejection probability is defined by the formula::     max(0, (rq_count -
    # rq_success_count / sr_threshold) / (rq_count + 1)) ^ (1 / aggression) The
    # aggression dictates how heavily the admission controller will throttle
    # requests upon SR dropping at or below the threshold. A value of 1 will
    # result in a linear increase in rejection probability as SR drops. Any
    # values less than 1.0, will be set to 1.0. If the message is unspecified,
    # the aggression is 1.0. See `the admission control documentation <https://ww
    # w.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/admission
    # _control_filter.html>`_ for a diagram illustrating this.
    aggression: "_____config_core_v3__.RuntimeDouble" = betterproto.message_field(4)
    # Dictates the success rate at which the rejection probability is non-zero.
    # As success rate drops below this threshold, rejection probability will
    # increase. Any success rate above the threshold results in a rejection
    # probability of 0. Defaults to 95%.
    sr_threshold: "_____config_core_v3__.RuntimePercent" = betterproto.message_field(5)


@dataclass(eq=False, repr=False)
class AdmissionControlSuccessCriteria(betterproto.Message):
    """
    Default method of specifying what constitutes a successful request. All
    status codes that indicate a successful request must be explicitly
    specified if not relying on the default values.
    """

    # If HTTP criteria are unspecified, all HTTP status codes below 500 are
    # treated as successful responses. .. note::    The default HTTP codes
    # considered successful by the admission controller are done so due    to the
    # unlikelihood that sending fewer requests would change their behavior (for
    # example:    redirects, unauthorized access, or bad requests won't be
    # alleviated by sending less    traffic).
    http_criteria: "AdmissionControlSuccessCriteriaHttpCriteria" = (
        betterproto.message_field(1)
    )
    # GRPC status codes to consider as request successes. If unspecified,
    # defaults to: Ok, Cancelled, Unknown, InvalidArgument, NotFound,
    # AlreadyExists, Unauthenticated, FailedPrecondition, OutOfRange,
    # PermissionDenied, and Unimplemented. .. note::    The default gRPC codes
    # that are considered successful by the admission controller are    chosen
    # because of the unlikelihood that sending fewer requests will change the
    # behavior.
    grpc_criteria: "AdmissionControlSuccessCriteriaGrpcCriteria" = (
        betterproto.message_field(2)
    )


@dataclass(eq=False, repr=False)
class AdmissionControlSuccessCriteriaHttpCriteria(betterproto.Message):
    # Status code ranges that constitute a successful request. Configurable codes
    # are in the range [100, 600).
    http_success_status: List["_____type_v3__.Int32Range"] = betterproto.message_field(
        1
    )


@dataclass(eq=False, repr=False)
class AdmissionControlSuccessCriteriaGrpcCriteria(betterproto.Message):
    # Status codes that constitute a successful request. Mappings can be found
    # at: https://github.com/grpc/grpc/blob/master/doc/statuscodes.md.
    grpc_success_status: List[int] = betterproto.uint32_field(1)


from ......config.core import v3 as _____config_core_v3__
from ......type import v3 as _____type_v3__

# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/config/filter/http/health_check/v2/health_check.proto
# plugin: python-betterproto
from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, List, Optional

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class HealthCheck(betterproto.Message):
    """[#next-free-field: 6]"""

    # Specifies whether the filter operates in pass through mode or not.
    pass_through_mode: Optional[bool] = betterproto.message_field(
        1, wraps=betterproto.TYPE_BOOL
    )
    # If operating in pass through mode, the amount of time in milliseconds that
    # the filter should cache the upstream response.
    cache_time: timedelta = betterproto.message_field(3)
    # If operating in non-pass-through mode, specifies a set of upstream cluster
    # names and the minimum percentage of servers in each of those clusters that
    # must be healthy or degraded in order for the filter to return a 200. ..
    # note::    This value is interpreted as an integer by truncating, so 12.50%
    # will be calculated    as if it were 12%.
    cluster_min_healthy_percentages: Dict[
        str, "_____type__.Percent"
    ] = betterproto.map_field(4, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE)
    # Specifies a set of health check request headers to match on. The health
    # check filter will check a request’s headers against all the specified
    # headers. To specify the health check endpoint, set the ``:path`` header to
    # match on.
    headers: List["_____api_v2_route__.HeaderMatcher"] = betterproto.message_field(5)


from ...... import type as _____type__
from ......api.v2 import route as _____api_v2_route__

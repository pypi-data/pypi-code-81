# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/filters/http/local_ratelimit/v3/local_rate_limit.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class LocalRateLimit(betterproto.Message):
    """[#next-free-field: 7]"""

    # The human readable prefix to use when emitting stats.
    stat_prefix: str = betterproto.string_field(1)
    # This field allows for a custom HTTP response status code to the downstream
    # client when the request has been rate limited. Defaults to 429
    # (TooManyRequests). .. note::   If this is set to < 400, 429 will be used
    # instead.
    status: "_____type_v3__.HttpStatus" = betterproto.message_field(2)
    # The token bucket configuration to use for rate limiting requests that are
    # processed by this filter. Each request processed by the filter consumes a
    # single token. If the token is available, the request will be allowed. If no
    # tokens are available, the request will receive the configured rate limit
    # status. .. note::   It's fine for the token bucket to be unset for the
    # global configuration since the rate limit   can be applied at a the virtual
    # host or route level. Thus, the token bucket must be set   for the per route
    # configuration otherwise the config will be rejected. .. note::   When using
    # per route configuration, the bucket becomes unique to that route. .. note::
    # In the current implementation the token bucket's :ref:`fill_interval
    # <envoy_api_field_type.v3.TokenBucket.fill_interval>` must be >= 50ms to
    # avoid too aggressive   refills.
    token_bucket: "_____type_v3__.TokenBucket" = betterproto.message_field(3)
    # If set, this will enable -- but not necessarily enforce -- the rate limit
    # for the given fraction of requests. Defaults to 0% of requests for safety.
    filter_enabled: "_____config_core_v3__.RuntimeFractionalPercent" = (
        betterproto.message_field(4)
    )
    # If set, this will enforce the rate limit decisions for the given fraction
    # of requests. Note: this only applies to the fraction of enabled requests.
    # Defaults to 0% of requests for safety.
    filter_enforced: "_____config_core_v3__.RuntimeFractionalPercent" = (
        betterproto.message_field(5)
    )
    # Specifies a list of HTTP headers that should be added to each response for
    # requests that have been rate limited.
    response_headers_to_add: List[
        "_____config_core_v3__.HeaderValueOption"
    ] = betterproto.message_field(6)


from ......config.core import v3 as _____config_core_v3__
from ......type import v3 as _____type_v3__

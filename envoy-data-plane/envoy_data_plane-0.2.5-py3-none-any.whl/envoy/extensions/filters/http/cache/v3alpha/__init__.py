# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/filters/http/cache/v3alpha/cache.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class CacheConfig(betterproto.Message):
    # Config specific to the cache storage implementation.
    typed_config: "betterproto_lib_google_protobuf.Any" = betterproto.message_field(1)
    # List of matching rules that defines allowed *Vary* headers. The *vary*
    # response header holds a list of header names that affect the contents of a
    # response, as described by
    # https://httpwg.org/specs/rfc7234.html#caching.negotiated.responses. During
    # insertion, *allowed_vary_headers* acts as a allowlist: if a response's
    # *vary* header mentions any header names that aren't matched by any rules in
    # *allowed_vary_headers*, that response will not be cached. During lookup,
    # *allowed_vary_headers* controls what request headers will be sent to the
    # cache storage implementation.
    allowed_vary_headers: List[
        "_____type_matcher_v3__.StringMatcher"
    ] = betterproto.message_field(2)
    # [#not-implemented-hide:] <TODO(toddmgreer) implement key customization>
    # Modifies cache key creation by restricting which parts of the URL are
    # included.
    key_creator_params: "CacheConfigKeyCreatorParams" = betterproto.message_field(3)
    # [#not-implemented-hide:] <TODO(toddmgreer) implement size limit> Max body
    # size the cache filter will insert into a cache. 0 means unlimited (though
    # the cache storage implementation may have its own limit beyond which it
    # will reject insertions).
    max_body_bytes: int = betterproto.uint32_field(4)


@dataclass(eq=False, repr=False)
class CacheConfigKeyCreatorParams(betterproto.Message):
    """
    [#not-implemented-hide:] Modifies cache key creation by restricting which
    parts of the URL are included.
    """

    # If true, exclude the URL scheme from the cache key. Set to true if your
    # origins always produce the same response for http and https requests.
    exclude_scheme: bool = betterproto.bool_field(1)
    # If true, exclude the host from the cache key. Set to true if your origins'
    # responses don't ever depend on host.
    exclude_host: bool = betterproto.bool_field(2)
    # If *query_parameters_included* is nonempty, only query parameters matched
    # by one or more of its matchers are included in the cache key. Any other
    # query params will not affect cache lookup.
    query_parameters_included: List[
        "_____config_route_v3__.QueryParameterMatcher"
    ] = betterproto.message_field(3)
    # If *query_parameters_excluded* is nonempty, query parameters matched by one
    # or more of its matchers are excluded from the cache key (even if also
    # matched by *query_parameters_included*), and will not affect cache lookup.
    query_parameters_excluded: List[
        "_____config_route_v3__.QueryParameterMatcher"
    ] = betterproto.message_field(4)


from ......config.route import v3 as _____config_route_v3__
from ......type.matcher import v3 as _____type_matcher_v3__
import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf

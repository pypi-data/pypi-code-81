# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/config/filter/http/original_src/v2alpha1/original_src.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class OriginalSrc(betterproto.Message):
    """
    The Original Src filter binds upstream connections to the original source
    address determined for the request. This address could come from something
    like the Proxy Protocol filter, or it could come from trusted http headers.
    [#extension: envoy.filters.http.original_src]
    """

    # Sets the SO_MARK option on the upstream connection's socket to the provided
    # value. Used to ensure that non-local addresses may be routed back through
    # envoy when binding to the original source address. The option will not be
    # applied if the mark is 0.
    mark: int = betterproto.uint32_field(1)

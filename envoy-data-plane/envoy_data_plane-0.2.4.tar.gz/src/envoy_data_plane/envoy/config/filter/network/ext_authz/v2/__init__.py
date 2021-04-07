# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/config/filter/network/ext_authz/v2/ext_authz.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class ExtAuthz(betterproto.Message):
    """
    External Authorization filter calls out to an external service over the
    gRPC Authorization API defined by :ref:`CheckRequest
    <envoy_api_msg_service.auth.v2.CheckRequest>`. A failed check will cause
    this filter to close the TCP connection.
    """

    # The prefix to use when emitting statistics.
    stat_prefix: str = betterproto.string_field(1)
    # The external authorization gRPC service configuration. The default timeout
    # is set to 200ms by this filter.
    grpc_service: "_____api_v2_core__.GrpcService" = betterproto.message_field(2)
    # The filter's behaviour in case the external authorization service does not
    # respond back. When it is set to true, Envoy will also allow traffic in case
    # of communication failure between authorization service and the proxy.
    # Defaults to false.
    failure_mode_allow: bool = betterproto.bool_field(3)
    # Specifies if the peer certificate is sent to the external service. When
    # this field is true, Envoy will include the peer X.509 certificate, if
    # available, in the :ref:`certificate<envoy_api_field_service.auth.v2.Attribu
    # teContext.Peer.certificate>`.
    include_peer_certificate: bool = betterproto.bool_field(4)


from ......api.v2 import core as _____api_v2_core__

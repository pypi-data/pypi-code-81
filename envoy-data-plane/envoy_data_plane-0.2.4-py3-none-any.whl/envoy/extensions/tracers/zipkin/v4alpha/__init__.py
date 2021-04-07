# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/tracers/zipkin/v4alpha/zipkin.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import Optional

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


class ZipkinConfigCollectorEndpointVersion(betterproto.Enum):
    DEPRECATED_AND_UNAVAILABLE_DO_NOT_USE = 0
    HTTP_JSON = 1
    HTTP_PROTO = 2
    GRPC = 3


@dataclass(eq=False, repr=False)
class ZipkinConfig(betterproto.Message):
    """
    Configuration for the Zipkin tracer. [#extension: envoy.tracers.zipkin]
    [#next-free-field: 6]
    """

    # The cluster manager cluster that hosts the Zipkin collectors. Note that the
    # Zipkin cluster must be defined in the :ref:`Bootstrap static cluster
    # resources <envoy_api_field_config.bootstrap.v4alpha.Bootstrap.StaticResourc
    # es.clusters>`.
    collector_cluster: str = betterproto.string_field(1)
    # The API endpoint of the Zipkin service where the spans will be sent. When
    # using a standard Zipkin installation, the API endpoint is typically
    # /api/v1/spans, which is the default value.
    collector_endpoint: str = betterproto.string_field(2)
    # Determines whether a 128bit trace id will be used when creating a new trace
    # instance. The default value is false, which will result in a 64 bit trace
    # id being used.
    trace_id_128_bit: bool = betterproto.bool_field(3)
    # Determines whether client and server spans will share the same span
    # context. The default value is true.
    shared_span_context: Optional[bool] = betterproto.message_field(
        4, wraps=betterproto.TYPE_BOOL
    )
    # Determines the selected collector endpoint version. By default, the
    # ``HTTP_JSON_V1`` will be used.
    collector_endpoint_version: "ZipkinConfigCollectorEndpointVersion" = (
        betterproto.enum_field(5)
    )

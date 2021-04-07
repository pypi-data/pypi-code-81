# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/filters/network/dubbo_proxy/v4alpha/dubbo_proxy.proto, envoy/extensions/filters/network/dubbo_proxy/v4alpha/route.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import Dict, List

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


class ProtocolType(betterproto.Enum):
    """Dubbo Protocol types supported by Envoy."""

    # the default protocol.
    Dubbo = 0


class SerializationType(betterproto.Enum):
    """Dubbo Serialization types supported by Envoy."""

    # the default serialization protocol.
    Hessian2 = 0


@dataclass(eq=False, repr=False)
class RouteConfiguration(betterproto.Message):
    """[#next-free-field: 6]"""

    # The name of the route configuration. Reserved for future use in
    # asynchronous route discovery.
    name: str = betterproto.string_field(1)
    # The interface name of the service.
    interface: str = betterproto.string_field(2)
    # Which group does the interface belong to.
    group: str = betterproto.string_field(3)
    # The version number of the interface.
    version: str = betterproto.string_field(4)
    # The list of routes that will be matched, in order, against incoming
    # requests. The first route that matches will be used.
    routes: List["Route"] = betterproto.message_field(5)


@dataclass(eq=False, repr=False)
class Route(betterproto.Message):
    # Route matching parameters.
    match: "RouteMatch" = betterproto.message_field(1)
    # Route request to some upstream cluster.
    route: "RouteAction" = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class RouteMatch(betterproto.Message):
    # Method level routing matching.
    method: "MethodMatch" = betterproto.message_field(1)
    # Specifies a set of headers that the route should match on. The router will
    # check the request’s headers against all the specified headers in the route
    # config. A match will happen if all the headers in the route are present in
    # the request with the same values (or based on presence if the value field
    # is not in the config).
    headers: List[
        "_____config_route_v4_alpha__.HeaderMatcher"
    ] = betterproto.message_field(2)


@dataclass(eq=False, repr=False)
class RouteAction(betterproto.Message):
    # Indicates the upstream cluster to which the request should be routed.
    cluster: str = betterproto.string_field(1, group="cluster_specifier")
    # Multiple upstream clusters can be specified for a given route. The request
    # is routed to one of the upstream clusters based on weights assigned to each
    # cluster. Currently ClusterWeight only supports the name and weight fields.
    weighted_clusters: "_____config_route_v4_alpha__.WeightedCluster" = (
        betterproto.message_field(2, group="cluster_specifier")
    )


@dataclass(eq=False, repr=False)
class MethodMatch(betterproto.Message):
    # The name of the method.
    name: "_____type_matcher_v4_alpha__.StringMatcher" = betterproto.message_field(1)
    # Method parameter definition. The key is the parameter index, starting from
    # 0. The value is the parameter matching type.
    params_match: Dict[
        int, "MethodMatchParameterMatchSpecifier"
    ] = betterproto.map_field(2, betterproto.TYPE_UINT32, betterproto.TYPE_MESSAGE)


@dataclass(eq=False, repr=False)
class MethodMatchParameterMatchSpecifier(betterproto.Message):
    """The parameter matching type."""

    # If specified, header match will be performed based on the value of the
    # header.
    exact_match: str = betterproto.string_field(3, group="parameter_match_specifier")
    # If specified, header match will be performed based on range. The rule will
    # match if the request header value is within this range. The entire request
    # header value must represent an integer in base 10 notation: consisting of
    # an optional plus or minus sign followed by a sequence of digits. The rule
    # will not match if the header value does not represent an integer. Match
    # will fail for empty values, floating point numbers or if only a subsequence
    # of the header value is an integer. Examples: * For range [-10,0), route
    # will match for header value -1, but not for 0,   "somestring", 10.9,
    # "-1somestring"
    range_match: "_____type_v3__.Int64Range" = betterproto.message_field(
        4, group="parameter_match_specifier"
    )


@dataclass(eq=False, repr=False)
class DubboProxy(betterproto.Message):
    """[#next-free-field: 6]"""

    # The human readable prefix to use when emitting statistics.
    stat_prefix: str = betterproto.string_field(1)
    # Configure the protocol used.
    protocol_type: "ProtocolType" = betterproto.enum_field(2)
    # Configure the serialization protocol used.
    serialization_type: "SerializationType" = betterproto.enum_field(3)
    # The route table for the connection manager is static and is specified in
    # this property.
    route_config: List["RouteConfiguration"] = betterproto.message_field(4)
    # A list of individual Dubbo filters that make up the filter chain for
    # requests made to the Dubbo proxy. Order matters as the filters are
    # processed sequentially. For backwards compatibility, if no dubbo_filters
    # are specified, a default Dubbo router filter (`envoy.filters.dubbo.router`)
    # is used.
    dubbo_filters: List["DubboFilter"] = betterproto.message_field(5)


@dataclass(eq=False, repr=False)
class DubboFilter(betterproto.Message):
    """DubboFilter configures a Dubbo filter."""

    # The name of the filter to instantiate. The name must match a supported
    # filter.
    name: str = betterproto.string_field(1)
    # Filter specific configuration which depends on the filter being
    # instantiated. See the supported filters for further documentation.
    config: "betterproto_lib_google_protobuf.Any" = betterproto.message_field(2)


from ......config.route import v4alpha as _____config_route_v4_alpha__
from ......type import v3 as _____type_v3__
from ......type.matcher import v4alpha as _____type_matcher_v4_alpha__
import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf

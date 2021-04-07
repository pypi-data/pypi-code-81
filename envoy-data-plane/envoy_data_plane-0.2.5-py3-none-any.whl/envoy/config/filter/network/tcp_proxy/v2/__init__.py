# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/config/filter/network/tcp_proxy/v2/tcp_proxy.proto
# plugin: python-betterproto
import warnings
from dataclasses import dataclass
from datetime import timedelta
from typing import List, Optional

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class TcpProxy(betterproto.Message):
    """[#next-free-field: 13]"""

    # The prefix to use when emitting :ref:`statistics
    # <config_network_filters_tcp_proxy_stats>`.
    stat_prefix: str = betterproto.string_field(1)
    # The upstream cluster to connect to.
    cluster: str = betterproto.string_field(2, group="cluster_specifier")
    # Multiple upstream clusters can be specified for a given route. The request
    # is routed to one of the upstream clusters based on weights assigned to each
    # cluster.
    weighted_clusters: "TcpProxyWeightedCluster" = betterproto.message_field(
        10, group="cluster_specifier"
    )
    # Optional endpoint metadata match criteria. Only endpoints in the upstream
    # cluster with metadata matching that set in metadata_match will be
    # considered. The filter name should be specified as *envoy.lb*.
    metadata_match: "_____api_v2_core__.Metadata" = betterproto.message_field(9)
    # The idle timeout for connections managed by the TCP proxy filter. The idle
    # timeout is defined as the period in which there are no bytes sent or
    # received on either the upstream or downstream connection. If not set, the
    # default idle timeout is 1 hour. If set to 0s, the timeout will be disabled.
    # .. warning::   Disabling this timeout has a highly likelihood of yielding
    # connection leaks due to lost TCP   FIN packets, etc.
    idle_timeout: timedelta = betterproto.message_field(8)
    # [#not-implemented-hide:] The idle timeout for connections managed by the
    # TCP proxy filter. The idle timeout is defined as the period in which there
    # is no active traffic. If not set, there is no idle timeout. When the idle
    # timeout is reached the connection will be closed. The distinction between
    # downstream_idle_timeout/upstream_idle_timeout provides a means to set
    # timeout based on the last byte sent on the downstream/upstream connection.
    downstream_idle_timeout: timedelta = betterproto.message_field(3)
    # [#not-implemented-hide:]
    upstream_idle_timeout: timedelta = betterproto.message_field(4)
    # Configuration for :ref:`access logs <arch_overview_access_logs>` emitted by
    # the this tcp_proxy.
    access_log: List["___accesslog_v2__.AccessLog"] = betterproto.message_field(5)
    # [#not-implemented-hide:] Deprecated.
    deprecated_v1: "TcpProxyDeprecatedV1" = betterproto.message_field(6)
    # The maximum number of unsuccessful connection attempts that will be made
    # before giving up. If the parameter is not specified, 1 connection attempt
    # will be made.
    max_connect_attempts: Optional[int] = betterproto.message_field(
        7, wraps=betterproto.TYPE_UINT32
    )
    # Optional configuration for TCP proxy hash policy. If hash_policy is not
    # set, the hash-based load balancing algorithms will select a host randomly.
    # Currently the number of hash policies is limited to 1.
    hash_policy: List["_____type__.HashPolicy"] = betterproto.message_field(11)
    # [#not-implemented-hide:] feature in progress If set, this configures
    # tunneling, e.g. configuration options to tunnel multiple TCP payloads over
    # a shared HTTP/2 tunnel. If this message is absent, the payload will be
    # proxied upstream as per usual.
    tunneling_config: "TcpProxyTunnelingConfig" = betterproto.message_field(12)

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.deprecated_v1:
            warnings.warn("TcpProxy.deprecated_v1 is deprecated", DeprecationWarning)


@dataclass(eq=False, repr=False)
class TcpProxyDeprecatedV1(betterproto.Message):
    """
    [#not-implemented-hide:] Deprecated. TCP Proxy filter configuration using
    V1 format.
    """

    # The route table for the filter. All filter instances must have a route
    # table, even if it is empty.
    routes: List["TcpProxyDeprecatedV1TcpRoute"] = betterproto.message_field(1)

    def __post_init__(self) -> None:
        warnings.warn("TcpProxyDeprecatedV1 is deprecated", DeprecationWarning)
        super().__post_init__()


@dataclass(eq=False, repr=False)
class TcpProxyDeprecatedV1TcpRoute(betterproto.Message):
    """
    A TCP proxy route consists of a set of optional L4 criteria and the name of
    a cluster. If a downstream connection matches all the specified criteria,
    the cluster in the route is used for the corresponding upstream connection.
    Routes are tried in the order specified until a match is found. If no match
    is found, the connection is closed. A route with no criteria is valid and
    always produces a match. [#next-free-field: 6]
    """

    # The cluster to connect to when a the downstream network connection matches
    # the specified criteria.
    cluster: str = betterproto.string_field(1)
    # An optional list of IP address subnets in the form “ip_address/xx”. The
    # criteria is satisfied if the destination IP address of the downstream
    # connection is contained in at least one of the specified subnets. If the
    # parameter is not specified or the list is empty, the destination IP address
    # is ignored. The destination IP address of the downstream connection might
    # be different from the addresses on which the proxy is listening if the
    # connection has been redirected.
    destination_ip_list: List[
        "_____api_v2_core__.CidrRange"
    ] = betterproto.message_field(2)
    # An optional string containing a comma-separated list of port numbers or
    # ranges. The criteria is satisfied if the destination port of the downstream
    # connection is contained in at least one of the specified ranges. If the
    # parameter is not specified, the destination port is ignored. The
    # destination port address of the downstream connection might be different
    # from the port on which the proxy is listening if the connection has been
    # redirected.
    destination_ports: str = betterproto.string_field(3)
    # An optional list of IP address subnets in the form “ip_address/xx”. The
    # criteria is satisfied if the source IP address of the downstream connection
    # is contained in at least one of the specified subnets. If the parameter is
    # not specified or the list is empty, the source IP address is ignored.
    source_ip_list: List["_____api_v2_core__.CidrRange"] = betterproto.message_field(4)
    # An optional string containing a comma-separated list of port numbers or
    # ranges. The criteria is satisfied if the source port of the downstream
    # connection is contained in at least one of the specified ranges. If the
    # parameter is not specified, the source port is ignored.
    source_ports: str = betterproto.string_field(5)


@dataclass(eq=False, repr=False)
class TcpProxyWeightedCluster(betterproto.Message):
    """
    Allows for specification of multiple upstream clusters along with weights
    that indicate the percentage of traffic to be forwarded to each cluster.
    The router selects an upstream cluster based on these weights.
    """

    # Specifies one or more upstream clusters associated with the route.
    clusters: List["TcpProxyWeightedClusterClusterWeight"] = betterproto.message_field(
        1
    )


@dataclass(eq=False, repr=False)
class TcpProxyWeightedClusterClusterWeight(betterproto.Message):
    # Name of the upstream cluster.
    name: str = betterproto.string_field(1)
    # When a request matches the route, the choice of an upstream cluster is
    # determined by its weight. The sum of weights across all entries in the
    # clusters array determines the total weight.
    weight: int = betterproto.uint32_field(2)
    # Optional endpoint metadata match criteria used by the subset load balancer.
    # Only endpoints in the upstream cluster with metadata matching what is set
    # in this field will be considered for load balancing. Note that this will be
    # merged with what's provided in :ref:`TcpProxy.metadata_match <envoy_api_fie
    # ld_config.filter.network.tcp_proxy.v2.TcpProxy.metadata_match>`, with
    # values here taking precedence. The filter name should be specified as
    # *envoy.lb*.
    metadata_match: "_____api_v2_core__.Metadata" = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class TcpProxyTunnelingConfig(betterproto.Message):
    """
    Configuration for tunneling TCP over other transports or application
    layers. Currently, only HTTP/2 is supported. When other options exist,
    HTTP/2 will remain the default.
    """

    # The hostname to send in the synthesized CONNECT headers to the upstream
    # proxy.
    hostname: str = betterproto.string_field(1)


from ...... import type as _____type__
from ......api.v2 import core as _____api_v2_core__
from ....accesslog import v2 as ___accesslog_v2__

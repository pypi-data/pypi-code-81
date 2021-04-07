# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/config/filter/network/redis_proxy/v2/redis_proxy.proto
# plugin: python-betterproto
import warnings
from dataclasses import dataclass
from datetime import timedelta
from typing import List, Optional

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


class RedisProxyConnPoolSettingsReadPolicy(betterproto.Enum):
    MASTER = 0
    PREFER_MASTER = 1
    REPLICA = 2
    PREFER_REPLICA = 3
    ANY = 4


@dataclass(eq=False, repr=False)
class RedisProxy(betterproto.Message):
    """[#next-free-field: 7]"""

    # The prefix to use when emitting :ref:`statistics
    # <config_network_filters_redis_proxy_stats>`.
    stat_prefix: str = betterproto.string_field(1)
    # Name of cluster from cluster manager. See the :ref:`configuration section
    # <arch_overview_redis_configuration>` of the architecture overview for
    # recommendations on configuring the backing cluster. .. attention::   This
    # field is deprecated. Use a :ref:`catch_all   route<envoy_api_field_config.f
    # ilter.network.redis_proxy.v2.RedisProxy.PrefixRoutes.catch_all_route>`
    # instead.
    cluster: str = betterproto.string_field(2)
    # Network settings for the connection pool to the upstream clusters.
    settings: "RedisProxyConnPoolSettings" = betterproto.message_field(3)
    # Indicates that latency stat should be computed in microseconds. By default
    # it is computed in milliseconds.
    latency_in_micros: bool = betterproto.bool_field(4)
    # List of **unique** prefixes used to separate keys from different workloads
    # to different clusters. Envoy will always favor the longest match first in
    # case of overlap. A catch-all cluster can be used to forward commands when
    # there is no match. Time complexity of the lookups are in O(min(longest key
    # prefix, key length)). Example: .. code-block:: yaml    prefix_routes:
    # routes:        - prefix: "ab"          cluster: "cluster_a"        -
    # prefix: "abc"          cluster: "cluster_b" When using the above routes,
    # the following prefixes would be sent to: * ``get abc:users`` would retrieve
    # the key 'abc:users' from cluster_b. * ``get ab:users`` would retrieve the
    # key 'ab:users' from cluster_a. * ``get z:users`` would return a
    # NoUpstreamHost error. A :ref:`catch-all   route<envoy_api_field_config.filt
    # er.network.redis_proxy.v2.RedisProxy.PrefixRoutes.catch_all_route>`   would
    # have retrieved the key from that cluster instead. See the
    # :ref:`configuration section <arch_overview_redis_configuration>` of the
    # architecture overview for recommendations on configuring the backing
    # clusters.
    prefix_routes: "RedisProxyPrefixRoutes" = betterproto.message_field(5)
    # Authenticate Redis client connections locally by forcing downstream clients
    # to issue a `Redis AUTH command <https://redis.io/commands/auth>`_ with this
    # password before enabling any other command. If an AUTH command's password
    # matches this password, an "OK" response will be returned to the client. If
    # the AUTH command password does not match this password, then an "ERR
    # invalid password" error will be returned. If any other command is received
    # before AUTH when this password is set, then a "NOAUTH Authentication
    # required." error response will be sent to the client. If an AUTH command is
    # received when the password is not set, then an "ERR Client sent AUTH, but
    # no password is set" error will be returned.
    downstream_auth_password: "_____api_v2_core__.DataSource" = (
        betterproto.message_field(6)
    )

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.cluster:
            warnings.warn("RedisProxy.cluster is deprecated", DeprecationWarning)


@dataclass(eq=False, repr=False)
class RedisProxyConnPoolSettings(betterproto.Message):
    """Redis connection pool settings. [#next-free-field: 9]"""

    # Per-operation timeout in milliseconds. The timer starts when the first
    # command of a pipeline is written to the backend connection. Each response
    # received from Redis resets the timer since it signifies that the next
    # command is being processed by the backend. The only exception to this
    # behavior is when a connection to a backend is not yet established. In that
    # case, the connect timeout on the cluster will govern the timeout until the
    # connection is ready.
    op_timeout: timedelta = betterproto.message_field(1)
    # Use hash tagging on every redis key to guarantee that keys with the same
    # hash tag will be forwarded to the same upstream. The hash key used for
    # determining the upstream in a consistent hash ring configuration will be
    # computed from the hash tagged key instead of the whole key. The algorithm
    # used to compute the hash tag is identical to the `redis-cluster
    # implementation <https://redis.io/topics/cluster-spec#keys-hash-tags>`_.
    # Examples: * '{user1000}.following' and '{user1000}.followers' **will** be
    # sent to the same upstream * '{user1000}.following' and
    # '{user1001}.following' **might** be sent to the same upstream
    enable_hashtagging: bool = betterproto.bool_field(2)
    # Accept `moved and ask redirection <https://redis.io/topics/cluster-
    # spec#redirection-and-resharding>`_ errors from upstream redis servers, and
    # retry commands to the specified target server. The target server does not
    # need to be known to the cluster manager. If the command cannot be
    # redirected, then the original error is passed downstream unchanged. By
    # default, this support is not enabled.
    enable_redirection: bool = betterproto.bool_field(3)
    # Maximum size of encoded request buffer before flush is triggered and
    # encoded requests are sent upstream. If this is unset, the buffer flushes
    # whenever it receives data and performs no batching. This feature makes it
    # possible for multiple clients to send requests to Envoy and have them
    # batched- for example if one is running several worker processes, each with
    # its own Redis connection. There is no benefit to using this with a single
    # downstream process. Recommended size (if enabled) is 1024 bytes.
    max_buffer_size_before_flush: int = betterproto.uint32_field(4)
    # The encoded request buffer is flushed N milliseconds after the first
    # request has been encoded, unless the buffer size has already exceeded
    # `max_buffer_size_before_flush`. If `max_buffer_size_before_flush` is not
    # set, this flush timer is not used. Otherwise, the timer should be set
    # according to the number of clients, overall request rate and desired
    # maximum latency for a single command. For example, if there are many
    # requests being batched together at a high rate, the buffer will likely be
    # filled before the timer fires. Alternatively, if the request rate is lower
    # the buffer will not be filled as often before the timer fires. If
    # `max_buffer_size_before_flush` is set, but `buffer_flush_timeout` is not,
    # the latter defaults to 3ms.
    buffer_flush_timeout: timedelta = betterproto.message_field(5)
    # `max_upstream_unknown_connections` controls how many upstream connections
    # to unknown hosts can be created at any given time by any given worker
    # thread (see `enable_redirection` for more details). If the host is unknown
    # and a connection cannot be created due to enforcing this limit, then
    # redirection will fail and the original redirection error will be passed
    # downstream unchanged. This limit defaults to 100.
    max_upstream_unknown_connections: Optional[int] = betterproto.message_field(
        6, wraps=betterproto.TYPE_UINT32
    )
    # Enable per-command statistics per upstream cluster, in addition to the
    # filter level aggregate count.
    enable_command_stats: bool = betterproto.bool_field(8)
    # Read policy. The default is to read from the primary.
    read_policy: "RedisProxyConnPoolSettingsReadPolicy" = betterproto.enum_field(7)


@dataclass(eq=False, repr=False)
class RedisProxyPrefixRoutes(betterproto.Message):
    # List of prefix routes.
    routes: List["RedisProxyPrefixRoutesRoute"] = betterproto.message_field(1)
    # Indicates that prefix matching should be case insensitive.
    case_insensitive: bool = betterproto.bool_field(2)
    # Optional catch-all route to forward commands that doesn't match any of the
    # routes. The catch-all route becomes required when no routes are specified.
    # .. attention::   This field is deprecated. Use a :ref:`catch_all   route<en
    # voy_api_field_config.filter.network.redis_proxy.v2.RedisProxy.PrefixRoutes.
    # catch_all_route>`   instead.
    catch_all_cluster: str = betterproto.string_field(3)
    # Optional catch-all route to forward commands that doesn't match any of the
    # routes. The catch-all route becomes required when no routes are specified.
    catch_all_route: "RedisProxyPrefixRoutesRoute" = betterproto.message_field(4)

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.catch_all_cluster:
            warnings.warn(
                "RedisProxyPrefixRoutes.catch_all_cluster is deprecated",
                DeprecationWarning,
            )


@dataclass(eq=False, repr=False)
class RedisProxyPrefixRoutesRoute(betterproto.Message):
    # String prefix that must match the beginning of the keys. Envoy will always
    # favor the longest match.
    prefix: str = betterproto.string_field(1)
    # Indicates if the prefix needs to be removed from the key when forwarded.
    remove_prefix: bool = betterproto.bool_field(2)
    # Upstream cluster to forward the command to.
    cluster: str = betterproto.string_field(3)
    # Indicates that the route has a request mirroring policy.
    request_mirror_policy: List[
        "RedisProxyPrefixRoutesRouteRequestMirrorPolicy"
    ] = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class RedisProxyPrefixRoutesRouteRequestMirrorPolicy(betterproto.Message):
    """
    The router is capable of shadowing traffic from one cluster to another. The
    current implementation is "fire and forget," meaning Envoy will not wait
    for the shadow cluster to respond before returning the response from the
    primary cluster. All normal statistics are collected for the shadow cluster
    making this feature useful for testing.
    """

    # Specifies the cluster that requests will be mirrored to. The cluster must
    # exist in the cluster manager configuration.
    cluster: str = betterproto.string_field(1)
    # If not specified or the runtime key is not present, all requests to the
    # target cluster will be mirrored. If specified, Envoy will lookup the
    # runtime key to get the percentage of requests to the mirror.
    runtime_fraction: "_____api_v2_core__.RuntimeFractionalPercent" = (
        betterproto.message_field(2)
    )
    # Set this to TRUE to only mirror write commands, this is effectively
    # replicating the writes in a "fire and forget" manner.
    exclude_read_commands: bool = betterproto.bool_field(3)


@dataclass(eq=False, repr=False)
class RedisProtocolOptions(betterproto.Message):
    """
    RedisProtocolOptions specifies Redis upstream protocol options. This object
    is used in :ref:`typed_extension_protocol_options<envoy_api_field_Cluster.t
    yped_extension_protocol_options>`, keyed by the name
    `envoy.filters.network.redis_proxy`.
    """

    # Upstream server password as defined by the `requirepass` directive
    # <https://redis.io/topics/config>`_ in the server's configuration file.
    auth_password: "_____api_v2_core__.DataSource" = betterproto.message_field(1)


from ......api.v2 import core as _____api_v2_core__

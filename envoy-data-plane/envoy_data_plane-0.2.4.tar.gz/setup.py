# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['envoy_data_plane',
 'envoy_data_plane.envoy',
 'envoy_data_plane.envoy.admin',
 'envoy_data_plane.envoy.admin.v3',
 'envoy_data_plane.envoy.annotations',
 'envoy_data_plane.envoy.api',
 'envoy_data_plane.envoy.api.v2',
 'envoy_data_plane.envoy.api.v2.auth',
 'envoy_data_plane.envoy.api.v2.cluster',
 'envoy_data_plane.envoy.api.v2.core',
 'envoy_data_plane.envoy.api.v2.endpoint',
 'envoy_data_plane.envoy.api.v2.listener',
 'envoy_data_plane.envoy.api.v2.ratelimit',
 'envoy_data_plane.envoy.api.v2.route',
 'envoy_data_plane.envoy.config',
 'envoy_data_plane.envoy.config.accesslog',
 'envoy_data_plane.envoy.config.accesslog.v2',
 'envoy_data_plane.envoy.config.accesslog.v3',
 'envoy_data_plane.envoy.config.accesslog.v4alpha',
 'envoy_data_plane.envoy.config.bootstrap',
 'envoy_data_plane.envoy.config.bootstrap.v2',
 'envoy_data_plane.envoy.config.bootstrap.v3',
 'envoy_data_plane.envoy.config.bootstrap.v4alpha',
 'envoy_data_plane.envoy.config.cluster',
 'envoy_data_plane.envoy.config.cluster.v3',
 'envoy_data_plane.envoy.config.cluster.v4alpha',
 'envoy_data_plane.envoy.config.common',
 'envoy_data_plane.envoy.config.common.dynamic_forward_proxy',
 'envoy_data_plane.envoy.config.common.dynamic_forward_proxy.v2alpha',
 'envoy_data_plane.envoy.config.common.matcher',
 'envoy_data_plane.envoy.config.common.matcher.v3',
 'envoy_data_plane.envoy.config.common.matcher.v4alpha',
 'envoy_data_plane.envoy.config.common.tap',
 'envoy_data_plane.envoy.config.common.tap.v2alpha',
 'envoy_data_plane.envoy.config.core',
 'envoy_data_plane.envoy.config.core.v3',
 'envoy_data_plane.envoy.config.core.v4alpha',
 'envoy_data_plane.envoy.config.endpoint',
 'envoy_data_plane.envoy.config.endpoint.v3',
 'envoy_data_plane.envoy.config.filter',
 'envoy_data_plane.envoy.config.filter.accesslog',
 'envoy_data_plane.envoy.config.filter.accesslog.v2',
 'envoy_data_plane.envoy.config.filter.dubbo',
 'envoy_data_plane.envoy.config.filter.dubbo.router',
 'envoy_data_plane.envoy.config.filter.dubbo.router.v2alpha1',
 'envoy_data_plane.envoy.config.filter.fault',
 'envoy_data_plane.envoy.config.filter.fault.v2',
 'envoy_data_plane.envoy.config.filter.http',
 'envoy_data_plane.envoy.config.filter.http.adaptive_concurrency',
 'envoy_data_plane.envoy.config.filter.http.adaptive_concurrency.v2alpha',
 'envoy_data_plane.envoy.config.filter.http.aws_lambda',
 'envoy_data_plane.envoy.config.filter.http.aws_lambda.v2alpha',
 'envoy_data_plane.envoy.config.filter.http.aws_request_signing',
 'envoy_data_plane.envoy.config.filter.http.aws_request_signing.v2alpha',
 'envoy_data_plane.envoy.config.filter.http.buffer',
 'envoy_data_plane.envoy.config.filter.http.buffer.v2',
 'envoy_data_plane.envoy.config.filter.http.cache',
 'envoy_data_plane.envoy.config.filter.http.cache.v2alpha',
 'envoy_data_plane.envoy.config.filter.http.compressor',
 'envoy_data_plane.envoy.config.filter.http.compressor.v2',
 'envoy_data_plane.envoy.config.filter.http.cors',
 'envoy_data_plane.envoy.config.filter.http.cors.v2',
 'envoy_data_plane.envoy.config.filter.http.csrf',
 'envoy_data_plane.envoy.config.filter.http.csrf.v2',
 'envoy_data_plane.envoy.config.filter.http.dynamic_forward_proxy',
 'envoy_data_plane.envoy.config.filter.http.dynamic_forward_proxy.v2alpha',
 'envoy_data_plane.envoy.config.filter.http.dynamo',
 'envoy_data_plane.envoy.config.filter.http.dynamo.v2',
 'envoy_data_plane.envoy.config.filter.http.ext_authz',
 'envoy_data_plane.envoy.config.filter.http.ext_authz.v2',
 'envoy_data_plane.envoy.config.filter.http.fault',
 'envoy_data_plane.envoy.config.filter.http.fault.v2',
 'envoy_data_plane.envoy.config.filter.http.grpc_http1_bridge',
 'envoy_data_plane.envoy.config.filter.http.grpc_http1_bridge.v2',
 'envoy_data_plane.envoy.config.filter.http.grpc_http1_reverse_bridge',
 'envoy_data_plane.envoy.config.filter.http.grpc_http1_reverse_bridge.v2alpha1',
 'envoy_data_plane.envoy.config.filter.http.grpc_stats',
 'envoy_data_plane.envoy.config.filter.http.grpc_stats.v2alpha',
 'envoy_data_plane.envoy.config.filter.http.grpc_web',
 'envoy_data_plane.envoy.config.filter.http.grpc_web.v2',
 'envoy_data_plane.envoy.config.filter.http.gzip',
 'envoy_data_plane.envoy.config.filter.http.gzip.v2',
 'envoy_data_plane.envoy.config.filter.http.header_to_metadata',
 'envoy_data_plane.envoy.config.filter.http.header_to_metadata.v2',
 'envoy_data_plane.envoy.config.filter.http.health_check',
 'envoy_data_plane.envoy.config.filter.http.health_check.v2',
 'envoy_data_plane.envoy.config.filter.http.ip_tagging',
 'envoy_data_plane.envoy.config.filter.http.ip_tagging.v2',
 'envoy_data_plane.envoy.config.filter.http.jwt_authn',
 'envoy_data_plane.envoy.config.filter.http.jwt_authn.v2alpha',
 'envoy_data_plane.envoy.config.filter.http.lua',
 'envoy_data_plane.envoy.config.filter.http.lua.v2',
 'envoy_data_plane.envoy.config.filter.http.on_demand',
 'envoy_data_plane.envoy.config.filter.http.on_demand.v2',
 'envoy_data_plane.envoy.config.filter.http.original_src',
 'envoy_data_plane.envoy.config.filter.http.original_src.v2alpha1',
 'envoy_data_plane.envoy.config.filter.http.rate_limit',
 'envoy_data_plane.envoy.config.filter.http.rate_limit.v2',
 'envoy_data_plane.envoy.config.filter.http.rbac',
 'envoy_data_plane.envoy.config.filter.http.rbac.v2',
 'envoy_data_plane.envoy.config.filter.http.router',
 'envoy_data_plane.envoy.config.filter.http.router.v2',
 'envoy_data_plane.envoy.config.filter.http.squash',
 'envoy_data_plane.envoy.config.filter.http.squash.v2',
 'envoy_data_plane.envoy.config.filter.http.tap',
 'envoy_data_plane.envoy.config.filter.http.tap.v2alpha',
 'envoy_data_plane.envoy.config.filter.http.transcoder',
 'envoy_data_plane.envoy.config.filter.http.transcoder.v2',
 'envoy_data_plane.envoy.config.filter.listener',
 'envoy_data_plane.envoy.config.filter.listener.http_inspector',
 'envoy_data_plane.envoy.config.filter.listener.http_inspector.v2',
 'envoy_data_plane.envoy.config.filter.listener.original_dst',
 'envoy_data_plane.envoy.config.filter.listener.original_dst.v2',
 'envoy_data_plane.envoy.config.filter.listener.original_src',
 'envoy_data_plane.envoy.config.filter.listener.original_src.v2alpha1',
 'envoy_data_plane.envoy.config.filter.listener.proxy_protocol',
 'envoy_data_plane.envoy.config.filter.listener.proxy_protocol.v2',
 'envoy_data_plane.envoy.config.filter.listener.tls_inspector',
 'envoy_data_plane.envoy.config.filter.listener.tls_inspector.v2',
 'envoy_data_plane.envoy.config.filter.network',
 'envoy_data_plane.envoy.config.filter.network.client_ssl_auth',
 'envoy_data_plane.envoy.config.filter.network.client_ssl_auth.v2',
 'envoy_data_plane.envoy.config.filter.network.direct_response',
 'envoy_data_plane.envoy.config.filter.network.direct_response.v2',
 'envoy_data_plane.envoy.config.filter.network.dubbo_proxy',
 'envoy_data_plane.envoy.config.filter.network.dubbo_proxy.v2alpha1',
 'envoy_data_plane.envoy.config.filter.network.echo',
 'envoy_data_plane.envoy.config.filter.network.echo.v2',
 'envoy_data_plane.envoy.config.filter.network.ext_authz',
 'envoy_data_plane.envoy.config.filter.network.ext_authz.v2',
 'envoy_data_plane.envoy.config.filter.network.http_connection_manager',
 'envoy_data_plane.envoy.config.filter.network.http_connection_manager.v2',
 'envoy_data_plane.envoy.config.filter.network.kafka_broker',
 'envoy_data_plane.envoy.config.filter.network.kafka_broker.v2alpha1',
 'envoy_data_plane.envoy.config.filter.network.local_rate_limit',
 'envoy_data_plane.envoy.config.filter.network.local_rate_limit.v2alpha',
 'envoy_data_plane.envoy.config.filter.network.mongo_proxy',
 'envoy_data_plane.envoy.config.filter.network.mongo_proxy.v2',
 'envoy_data_plane.envoy.config.filter.network.mysql_proxy',
 'envoy_data_plane.envoy.config.filter.network.mysql_proxy.v1alpha1',
 'envoy_data_plane.envoy.config.filter.network.rate_limit',
 'envoy_data_plane.envoy.config.filter.network.rate_limit.v2',
 'envoy_data_plane.envoy.config.filter.network.rbac',
 'envoy_data_plane.envoy.config.filter.network.rbac.v2',
 'envoy_data_plane.envoy.config.filter.network.redis_proxy',
 'envoy_data_plane.envoy.config.filter.network.redis_proxy.v2',
 'envoy_data_plane.envoy.config.filter.network.sni_cluster',
 'envoy_data_plane.envoy.config.filter.network.sni_cluster.v2',
 'envoy_data_plane.envoy.config.filter.network.tcp_proxy',
 'envoy_data_plane.envoy.config.filter.network.tcp_proxy.v2',
 'envoy_data_plane.envoy.config.filter.network.thrift_proxy',
 'envoy_data_plane.envoy.config.filter.network.thrift_proxy.v2alpha1',
 'envoy_data_plane.envoy.config.filter.network.zookeeper_proxy',
 'envoy_data_plane.envoy.config.filter.network.zookeeper_proxy.v1alpha1',
 'envoy_data_plane.envoy.config.filter.thrift',
 'envoy_data_plane.envoy.config.filter.thrift.rate_limit',
 'envoy_data_plane.envoy.config.filter.thrift.rate_limit.v2alpha1',
 'envoy_data_plane.envoy.config.filter.thrift.router',
 'envoy_data_plane.envoy.config.filter.thrift.router.v2alpha1',
 'envoy_data_plane.envoy.config.filter.udp',
 'envoy_data_plane.envoy.config.filter.udp.udp_proxy',
 'envoy_data_plane.envoy.config.filter.udp.udp_proxy.v2alpha',
 'envoy_data_plane.envoy.config.grpc_credential',
 'envoy_data_plane.envoy.config.grpc_credential.v2alpha',
 'envoy_data_plane.envoy.config.grpc_credential.v3',
 'envoy_data_plane.envoy.config.health_checker',
 'envoy_data_plane.envoy.config.health_checker.redis',
 'envoy_data_plane.envoy.config.health_checker.redis.v2',
 'envoy_data_plane.envoy.config.listener',
 'envoy_data_plane.envoy.config.listener.v2',
 'envoy_data_plane.envoy.config.listener.v3',
 'envoy_data_plane.envoy.config.listener.v4alpha',
 'envoy_data_plane.envoy.config.metrics',
 'envoy_data_plane.envoy.config.metrics.v2',
 'envoy_data_plane.envoy.config.metrics.v3',
 'envoy_data_plane.envoy.config.metrics.v4alpha',
 'envoy_data_plane.envoy.config.overload',
 'envoy_data_plane.envoy.config.overload.v2alpha',
 'envoy_data_plane.envoy.config.overload.v3',
 'envoy_data_plane.envoy.config.ratelimit',
 'envoy_data_plane.envoy.config.ratelimit.v2',
 'envoy_data_plane.envoy.config.ratelimit.v3',
 'envoy_data_plane.envoy.config.rbac',
 'envoy_data_plane.envoy.config.rbac.v2',
 'envoy_data_plane.envoy.config.rbac.v3',
 'envoy_data_plane.envoy.config.rbac.v4alpha',
 'envoy_data_plane.envoy.config.resource_monitor',
 'envoy_data_plane.envoy.config.resource_monitor.fixed_heap',
 'envoy_data_plane.envoy.config.resource_monitor.fixed_heap.v2alpha',
 'envoy_data_plane.envoy.config.resource_monitor.injected_resource',
 'envoy_data_plane.envoy.config.resource_monitor.injected_resource.v2alpha',
 'envoy_data_plane.envoy.config.retry',
 'envoy_data_plane.envoy.config.retry.omit_canary_hosts',
 'envoy_data_plane.envoy.config.retry.omit_canary_hosts.v2',
 'envoy_data_plane.envoy.config.retry.omit_host_metadata',
 'envoy_data_plane.envoy.config.retry.omit_host_metadata.v2',
 'envoy_data_plane.envoy.config.retry.previous_hosts',
 'envoy_data_plane.envoy.config.retry.previous_hosts.v2',
 'envoy_data_plane.envoy.config.retry.previous_priorities',
 'envoy_data_plane.envoy.config.route',
 'envoy_data_plane.envoy.config.route.v3',
 'envoy_data_plane.envoy.config.route.v4alpha',
 'envoy_data_plane.envoy.config.tap',
 'envoy_data_plane.envoy.config.tap.v3',
 'envoy_data_plane.envoy.config.tap.v4alpha',
 'envoy_data_plane.envoy.config.trace',
 'envoy_data_plane.envoy.config.trace.v2',
 'envoy_data_plane.envoy.config.trace.v2alpha',
 'envoy_data_plane.envoy.config.trace.v3',
 'envoy_data_plane.envoy.config.trace.v4alpha',
 'envoy_data_plane.envoy.config.transport_socket',
 'envoy_data_plane.envoy.config.transport_socket.alts',
 'envoy_data_plane.envoy.config.transport_socket.alts.v2alpha',
 'envoy_data_plane.envoy.config.transport_socket.raw_buffer',
 'envoy_data_plane.envoy.config.transport_socket.raw_buffer.v2',
 'envoy_data_plane.envoy.config.transport_socket.tap',
 'envoy_data_plane.envoy.config.transport_socket.tap.v2alpha',
 'envoy_data_plane.envoy.data',
 'envoy_data_plane.envoy.data.accesslog',
 'envoy_data_plane.envoy.data.accesslog.v2',
 'envoy_data_plane.envoy.data.accesslog.v3',
 'envoy_data_plane.envoy.data.cluster',
 'envoy_data_plane.envoy.data.cluster.v2alpha',
 'envoy_data_plane.envoy.data.cluster.v3',
 'envoy_data_plane.envoy.data.core',
 'envoy_data_plane.envoy.data.core.v2alpha',
 'envoy_data_plane.envoy.data.core.v3',
 'envoy_data_plane.envoy.data.dns',
 'envoy_data_plane.envoy.data.dns.v2alpha',
 'envoy_data_plane.envoy.data.dns.v3',
 'envoy_data_plane.envoy.data.dns.v4alpha',
 'envoy_data_plane.envoy.data.tap',
 'envoy_data_plane.envoy.data.tap.v2alpha',
 'envoy_data_plane.envoy.data.tap.v3',
 'envoy_data_plane.envoy.extensions',
 'envoy_data_plane.envoy.extensions.access_loggers',
 'envoy_data_plane.envoy.extensions.access_loggers.file',
 'envoy_data_plane.envoy.extensions.access_loggers.file.v3',
 'envoy_data_plane.envoy.extensions.access_loggers.file.v4alpha',
 'envoy_data_plane.envoy.extensions.access_loggers.grpc',
 'envoy_data_plane.envoy.extensions.access_loggers.grpc.v3',
 'envoy_data_plane.envoy.extensions.access_loggers.wasm',
 'envoy_data_plane.envoy.extensions.access_loggers.wasm.v3',
 'envoy_data_plane.envoy.extensions.clusters',
 'envoy_data_plane.envoy.extensions.clusters.aggregate',
 'envoy_data_plane.envoy.extensions.clusters.aggregate.v3',
 'envoy_data_plane.envoy.extensions.clusters.dynamic_forward_proxy',
 'envoy_data_plane.envoy.extensions.clusters.dynamic_forward_proxy.v3',
 'envoy_data_plane.envoy.extensions.clusters.redis',
 'envoy_data_plane.envoy.extensions.clusters.redis.v3',
 'envoy_data_plane.envoy.extensions.common',
 'envoy_data_plane.envoy.extensions.common.dynamic_forward_proxy',
 'envoy_data_plane.envoy.extensions.common.dynamic_forward_proxy.v3',
 'envoy_data_plane.envoy.extensions.common.ratelimit',
 'envoy_data_plane.envoy.extensions.common.ratelimit.v3',
 'envoy_data_plane.envoy.extensions.common.tap',
 'envoy_data_plane.envoy.extensions.common.tap.v3',
 'envoy_data_plane.envoy.extensions.common.tap.v4alpha',
 'envoy_data_plane.envoy.extensions.compression',
 'envoy_data_plane.envoy.extensions.compression.gzip',
 'envoy_data_plane.envoy.extensions.compression.gzip.compressor',
 'envoy_data_plane.envoy.extensions.compression.gzip.compressor.v3',
 'envoy_data_plane.envoy.extensions.compression.gzip.decompressor',
 'envoy_data_plane.envoy.extensions.compression.gzip.decompressor.v3',
 'envoy_data_plane.envoy.extensions.filters',
 'envoy_data_plane.envoy.extensions.filters.common',
 'envoy_data_plane.envoy.extensions.filters.common.fault',
 'envoy_data_plane.envoy.extensions.filters.common.fault.v3',
 'envoy_data_plane.envoy.extensions.filters.http',
 'envoy_data_plane.envoy.extensions.filters.http.adaptive_concurrency',
 'envoy_data_plane.envoy.extensions.filters.http.adaptive_concurrency.v3',
 'envoy_data_plane.envoy.extensions.filters.http.admission_control',
 'envoy_data_plane.envoy.extensions.filters.http.admission_control.v3alpha',
 'envoy_data_plane.envoy.extensions.filters.http.aws_lambda',
 'envoy_data_plane.envoy.extensions.filters.http.aws_lambda.v3',
 'envoy_data_plane.envoy.extensions.filters.http.aws_request_signing',
 'envoy_data_plane.envoy.extensions.filters.http.aws_request_signing.v3',
 'envoy_data_plane.envoy.extensions.filters.http.buffer',
 'envoy_data_plane.envoy.extensions.filters.http.buffer.v3',
 'envoy_data_plane.envoy.extensions.filters.http.cache',
 'envoy_data_plane.envoy.extensions.filters.http.cache.v3alpha',
 'envoy_data_plane.envoy.extensions.filters.http.cache.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.http.cdn_loop',
 'envoy_data_plane.envoy.extensions.filters.http.cdn_loop.v3alpha',
 'envoy_data_plane.envoy.extensions.filters.http.compressor',
 'envoy_data_plane.envoy.extensions.filters.http.compressor.v3',
 'envoy_data_plane.envoy.extensions.filters.http.cors',
 'envoy_data_plane.envoy.extensions.filters.http.cors.v3',
 'envoy_data_plane.envoy.extensions.filters.http.csrf',
 'envoy_data_plane.envoy.extensions.filters.http.csrf.v3',
 'envoy_data_plane.envoy.extensions.filters.http.csrf.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.http.decompressor',
 'envoy_data_plane.envoy.extensions.filters.http.decompressor.v3',
 'envoy_data_plane.envoy.extensions.filters.http.dynamic_forward_proxy',
 'envoy_data_plane.envoy.extensions.filters.http.dynamic_forward_proxy.v3',
 'envoy_data_plane.envoy.extensions.filters.http.dynamo',
 'envoy_data_plane.envoy.extensions.filters.http.dynamo.v3',
 'envoy_data_plane.envoy.extensions.filters.http.ext_authz',
 'envoy_data_plane.envoy.extensions.filters.http.ext_authz.v3',
 'envoy_data_plane.envoy.extensions.filters.http.ext_authz.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.http.fault',
 'envoy_data_plane.envoy.extensions.filters.http.fault.v3',
 'envoy_data_plane.envoy.extensions.filters.http.fault.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.http.grpc_http1_bridge',
 'envoy_data_plane.envoy.extensions.filters.http.grpc_http1_bridge.v3',
 'envoy_data_plane.envoy.extensions.filters.http.grpc_http1_reverse_bridge',
 'envoy_data_plane.envoy.extensions.filters.http.grpc_http1_reverse_bridge.v3',
 'envoy_data_plane.envoy.extensions.filters.http.grpc_json_transcoder',
 'envoy_data_plane.envoy.extensions.filters.http.grpc_json_transcoder.v3',
 'envoy_data_plane.envoy.extensions.filters.http.grpc_stats',
 'envoy_data_plane.envoy.extensions.filters.http.grpc_stats.v3',
 'envoy_data_plane.envoy.extensions.filters.http.grpc_web',
 'envoy_data_plane.envoy.extensions.filters.http.grpc_web.v3',
 'envoy_data_plane.envoy.extensions.filters.http.gzip',
 'envoy_data_plane.envoy.extensions.filters.http.gzip.v3',
 'envoy_data_plane.envoy.extensions.filters.http.header_to_metadata',
 'envoy_data_plane.envoy.extensions.filters.http.header_to_metadata.v3',
 'envoy_data_plane.envoy.extensions.filters.http.header_to_metadata.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.http.health_check',
 'envoy_data_plane.envoy.extensions.filters.http.health_check.v3',
 'envoy_data_plane.envoy.extensions.filters.http.health_check.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.http.ip_tagging',
 'envoy_data_plane.envoy.extensions.filters.http.ip_tagging.v3',
 'envoy_data_plane.envoy.extensions.filters.http.jwt_authn',
 'envoy_data_plane.envoy.extensions.filters.http.jwt_authn.v3',
 'envoy_data_plane.envoy.extensions.filters.http.jwt_authn.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.http.local_ratelimit',
 'envoy_data_plane.envoy.extensions.filters.http.local_ratelimit.v3',
 'envoy_data_plane.envoy.extensions.filters.http.lua',
 'envoy_data_plane.envoy.extensions.filters.http.lua.v3',
 'envoy_data_plane.envoy.extensions.filters.http.oauth2',
 'envoy_data_plane.envoy.extensions.filters.http.oauth2.v3alpha',
 'envoy_data_plane.envoy.extensions.filters.http.oauth2.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.http.on_demand',
 'envoy_data_plane.envoy.extensions.filters.http.on_demand.v3',
 'envoy_data_plane.envoy.extensions.filters.http.original_src',
 'envoy_data_plane.envoy.extensions.filters.http.original_src.v3',
 'envoy_data_plane.envoy.extensions.filters.http.ratelimit',
 'envoy_data_plane.envoy.extensions.filters.http.ratelimit.v3',
 'envoy_data_plane.envoy.extensions.filters.http.rbac',
 'envoy_data_plane.envoy.extensions.filters.http.rbac.v3',
 'envoy_data_plane.envoy.extensions.filters.http.rbac.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.http.router',
 'envoy_data_plane.envoy.extensions.filters.http.router.v3',
 'envoy_data_plane.envoy.extensions.filters.http.router.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.http.squash',
 'envoy_data_plane.envoy.extensions.filters.http.squash.v3',
 'envoy_data_plane.envoy.extensions.filters.http.tap',
 'envoy_data_plane.envoy.extensions.filters.http.tap.v3',
 'envoy_data_plane.envoy.extensions.filters.http.tap.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.http.wasm',
 'envoy_data_plane.envoy.extensions.filters.http.wasm.v3',
 'envoy_data_plane.envoy.extensions.filters.listener',
 'envoy_data_plane.envoy.extensions.filters.listener.http_inspector',
 'envoy_data_plane.envoy.extensions.filters.listener.http_inspector.v3',
 'envoy_data_plane.envoy.extensions.filters.listener.original_dst',
 'envoy_data_plane.envoy.extensions.filters.listener.original_dst.v3',
 'envoy_data_plane.envoy.extensions.filters.listener.original_src',
 'envoy_data_plane.envoy.extensions.filters.listener.original_src.v3',
 'envoy_data_plane.envoy.extensions.filters.listener.proxy_protocol',
 'envoy_data_plane.envoy.extensions.filters.listener.proxy_protocol.v3',
 'envoy_data_plane.envoy.extensions.filters.listener.tls_inspector',
 'envoy_data_plane.envoy.extensions.filters.listener.tls_inspector.v3',
 'envoy_data_plane.envoy.extensions.filters.network',
 'envoy_data_plane.envoy.extensions.filters.network.client_ssl_auth',
 'envoy_data_plane.envoy.extensions.filters.network.client_ssl_auth.v3',
 'envoy_data_plane.envoy.extensions.filters.network.direct_response',
 'envoy_data_plane.envoy.extensions.filters.network.direct_response.v3',
 'envoy_data_plane.envoy.extensions.filters.network.dubbo_proxy',
 'envoy_data_plane.envoy.extensions.filters.network.dubbo_proxy.router',
 'envoy_data_plane.envoy.extensions.filters.network.dubbo_proxy.router.v3',
 'envoy_data_plane.envoy.extensions.filters.network.dubbo_proxy.v3',
 'envoy_data_plane.envoy.extensions.filters.network.dubbo_proxy.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.network.echo',
 'envoy_data_plane.envoy.extensions.filters.network.echo.v3',
 'envoy_data_plane.envoy.extensions.filters.network.ext_authz',
 'envoy_data_plane.envoy.extensions.filters.network.ext_authz.v3',
 'envoy_data_plane.envoy.extensions.filters.network.ext_authz.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.network.http_connection_manager',
 'envoy_data_plane.envoy.extensions.filters.network.http_connection_manager.v3',
 'envoy_data_plane.envoy.extensions.filters.network.http_connection_manager.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.network.kafka_broker',
 'envoy_data_plane.envoy.extensions.filters.network.kafka_broker.v3',
 'envoy_data_plane.envoy.extensions.filters.network.local_ratelimit',
 'envoy_data_plane.envoy.extensions.filters.network.local_ratelimit.v3',
 'envoy_data_plane.envoy.extensions.filters.network.mongo_proxy',
 'envoy_data_plane.envoy.extensions.filters.network.mongo_proxy.v3',
 'envoy_data_plane.envoy.extensions.filters.network.mysql_proxy',
 'envoy_data_plane.envoy.extensions.filters.network.mysql_proxy.v3',
 'envoy_data_plane.envoy.extensions.filters.network.postgres_proxy',
 'envoy_data_plane.envoy.extensions.filters.network.postgres_proxy.v3alpha',
 'envoy_data_plane.envoy.extensions.filters.network.ratelimit',
 'envoy_data_plane.envoy.extensions.filters.network.ratelimit.v3',
 'envoy_data_plane.envoy.extensions.filters.network.rbac',
 'envoy_data_plane.envoy.extensions.filters.network.rbac.v3',
 'envoy_data_plane.envoy.extensions.filters.network.rbac.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.network.redis_proxy',
 'envoy_data_plane.envoy.extensions.filters.network.redis_proxy.v3',
 'envoy_data_plane.envoy.extensions.filters.network.rocketmq_proxy',
 'envoy_data_plane.envoy.extensions.filters.network.rocketmq_proxy.v3',
 'envoy_data_plane.envoy.extensions.filters.network.rocketmq_proxy.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.network.sni_cluster',
 'envoy_data_plane.envoy.extensions.filters.network.sni_cluster.v3',
 'envoy_data_plane.envoy.extensions.filters.network.sni_dynamic_forward_proxy',
 'envoy_data_plane.envoy.extensions.filters.network.sni_dynamic_forward_proxy.v3alpha',
 'envoy_data_plane.envoy.extensions.filters.network.tcp_proxy',
 'envoy_data_plane.envoy.extensions.filters.network.tcp_proxy.v3',
 'envoy_data_plane.envoy.extensions.filters.network.tcp_proxy.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.network.thrift_proxy',
 'envoy_data_plane.envoy.extensions.filters.network.thrift_proxy.filters',
 'envoy_data_plane.envoy.extensions.filters.network.thrift_proxy.filters.ratelimit',
 'envoy_data_plane.envoy.extensions.filters.network.thrift_proxy.filters.ratelimit.v3',
 'envoy_data_plane.envoy.extensions.filters.network.thrift_proxy.v3',
 'envoy_data_plane.envoy.extensions.filters.network.thrift_proxy.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.network.wasm',
 'envoy_data_plane.envoy.extensions.filters.network.wasm.v3',
 'envoy_data_plane.envoy.extensions.filters.network.zookeeper_proxy',
 'envoy_data_plane.envoy.extensions.filters.network.zookeeper_proxy.v3',
 'envoy_data_plane.envoy.extensions.filters.udp',
 'envoy_data_plane.envoy.extensions.filters.udp.dns_filter',
 'envoy_data_plane.envoy.extensions.filters.udp.dns_filter.v3alpha',
 'envoy_data_plane.envoy.extensions.filters.udp.dns_filter.v4alpha',
 'envoy_data_plane.envoy.extensions.filters.udp.udp_proxy',
 'envoy_data_plane.envoy.extensions.filters.udp.udp_proxy.v3',
 'envoy_data_plane.envoy.extensions.internal_redirect',
 'envoy_data_plane.envoy.extensions.internal_redirect.allow_listed_routes',
 'envoy_data_plane.envoy.extensions.internal_redirect.allow_listed_routes.v3',
 'envoy_data_plane.envoy.extensions.internal_redirect.previous_routes',
 'envoy_data_plane.envoy.extensions.internal_redirect.previous_routes.v3',
 'envoy_data_plane.envoy.extensions.internal_redirect.safe_cross_scheme',
 'envoy_data_plane.envoy.extensions.internal_redirect.safe_cross_scheme.v3',
 'envoy_data_plane.envoy.extensions.network',
 'envoy_data_plane.envoy.extensions.network.socket_interface',
 'envoy_data_plane.envoy.extensions.network.socket_interface.v3',
 'envoy_data_plane.envoy.extensions.retry',
 'envoy_data_plane.envoy.extensions.retry.host',
 'envoy_data_plane.envoy.extensions.retry.host.omit_host_metadata',
 'envoy_data_plane.envoy.extensions.retry.host.omit_host_metadata.v3',
 'envoy_data_plane.envoy.extensions.retry.priority',
 'envoy_data_plane.envoy.extensions.retry.priority.previous_priorities',
 'envoy_data_plane.envoy.extensions.retry.priority.previous_priorities.v3',
 'envoy_data_plane.envoy.extensions.tracers',
 'envoy_data_plane.envoy.extensions.tracers.datadog',
 'envoy_data_plane.envoy.extensions.tracers.datadog.v4alpha',
 'envoy_data_plane.envoy.extensions.tracers.dynamic_ot',
 'envoy_data_plane.envoy.extensions.tracers.dynamic_ot.v4alpha',
 'envoy_data_plane.envoy.extensions.tracers.lightstep',
 'envoy_data_plane.envoy.extensions.tracers.lightstep.v4alpha',
 'envoy_data_plane.envoy.extensions.tracers.opencensus',
 'envoy_data_plane.envoy.extensions.tracers.opencensus.v4alpha',
 'envoy_data_plane.envoy.extensions.tracers.xray',
 'envoy_data_plane.envoy.extensions.tracers.xray.v4alpha',
 'envoy_data_plane.envoy.extensions.tracers.zipkin',
 'envoy_data_plane.envoy.extensions.tracers.zipkin.v4alpha',
 'envoy_data_plane.envoy.extensions.transport_sockets',
 'envoy_data_plane.envoy.extensions.transport_sockets.alts',
 'envoy_data_plane.envoy.extensions.transport_sockets.alts.v3',
 'envoy_data_plane.envoy.extensions.transport_sockets.proxy_protocol',
 'envoy_data_plane.envoy.extensions.transport_sockets.proxy_protocol.v3',
 'envoy_data_plane.envoy.extensions.transport_sockets.quic',
 'envoy_data_plane.envoy.extensions.transport_sockets.quic.v3',
 'envoy_data_plane.envoy.extensions.transport_sockets.quic.v4alpha',
 'envoy_data_plane.envoy.extensions.transport_sockets.raw_buffer',
 'envoy_data_plane.envoy.extensions.transport_sockets.raw_buffer.v3',
 'envoy_data_plane.envoy.extensions.transport_sockets.tap',
 'envoy_data_plane.envoy.extensions.transport_sockets.tap.v3',
 'envoy_data_plane.envoy.extensions.transport_sockets.tap.v4alpha',
 'envoy_data_plane.envoy.extensions.transport_sockets.tls',
 'envoy_data_plane.envoy.extensions.transport_sockets.tls.v3',
 'envoy_data_plane.envoy.extensions.transport_sockets.tls.v4alpha',
 'envoy_data_plane.envoy.extensions.upstreams',
 'envoy_data_plane.envoy.extensions.upstreams.http',
 'envoy_data_plane.envoy.extensions.upstreams.http.generic',
 'envoy_data_plane.envoy.extensions.upstreams.http.generic.v3',
 'envoy_data_plane.envoy.extensions.upstreams.http.http',
 'envoy_data_plane.envoy.extensions.upstreams.http.http.v3',
 'envoy_data_plane.envoy.extensions.upstreams.http.tcp',
 'envoy_data_plane.envoy.extensions.upstreams.http.tcp.v3',
 'envoy_data_plane.envoy.extensions.wasm',
 'envoy_data_plane.envoy.extensions.wasm.v3',
 'envoy_data_plane.envoy.extensions.watchdog',
 'envoy_data_plane.envoy.extensions.watchdog.abort_action',
 'envoy_data_plane.envoy.extensions.watchdog.abort_action.v3alpha',
 'envoy_data_plane.envoy.extensions.watchdog.profile_action',
 'envoy_data_plane.envoy.extensions.watchdog.profile_action.v3alpha',
 'envoy_data_plane.envoy.service',
 'envoy_data_plane.envoy.service.tap',
 'envoy_data_plane.envoy.service.tap.v2alpha',
 'envoy_data_plane.envoy.type',
 'envoy_data_plane.envoy.type.matcher',
 'envoy_data_plane.envoy.type.matcher.v3',
 'envoy_data_plane.envoy.type.matcher.v4alpha',
 'envoy_data_plane.envoy.type.metadata',
 'envoy_data_plane.envoy.type.metadata.v2',
 'envoy_data_plane.envoy.type.metadata.v3',
 'envoy_data_plane.envoy.type.tracing',
 'envoy_data_plane.envoy.type.tracing.v2',
 'envoy_data_plane.envoy.type.tracing.v3',
 'envoy_data_plane.envoy.type.v3',
 'envoy_data_plane.google',
 'envoy_data_plane.google.api',
 'envoy_data_plane.google.api.expr',
 'envoy_data_plane.google.api.expr.v1alpha1',
 'envoy_data_plane.google.rpc',
 'envoy_data_plane.opencensus',
 'envoy_data_plane.opencensus.proto',
 'envoy_data_plane.opencensus.proto.trace',
 'envoy_data_plane.opencensus.proto.trace.v1',
 'envoy_data_plane.udpa',
 'envoy_data_plane.udpa.annotations',
 'envoy_data_plane.udpa.core',
 'envoy_data_plane.udpa.core.v1',
 'envoy_data_plane.validate']

package_data = \
{'': ['*']}

install_requires = \
['betterproto>=2.0.0b2,<3.0.0']

setup_kwargs = {
    'name': 'envoy-data-plane',
    'version': '0.2.4',
    'description': 'Python dataclasses for the Envoy Data-Plane-API',
    'long_description': '[![Build Status](https://travis-ci.org/cetanu/envoy_data_plane.svg?branch=master)](https://travis-ci.org/cetanu/envoy_data_plane) \n[![PyPI version](https://badge.fury.io/py/envoy-data-plane.svg)](https://badge.fury.io/py/envoy-data-plane)\n\n# envoy_data_plane\n\nA conversion of envoyproxy/data-plane-api protocol buffers into Python dataclasses using betterproto\n\n## Intended usage\n\nThis is a helper library that allows importing every type available in the envoy API.\n\nOne use-case might be generating Envoy configuration using a Python script.\n\nIn my case, I will use this library in my custom built control-plane, \nso that I have autocompletion in my IDE, and a basic form of validation.\n\nIn future, this may also help with building an idiomatic GRPC control-plane in Python.\n\n## Installation\n\nThis package is published to PyPI:\n\n```shell script\npython -m pip install envoy_data_plane\n```\n\n## Example\n\n```python\nimport stringcase\nimport json\nimport envoy_data_plane.envoy.api.v2 as envoy\n\nroute_config = envoy.RouteConfiguration(\n    name=\'MyRouteConfig\',\n    virtual_hosts=[\n        envoy.route.VirtualHost(\n            name=\'SomeWebsite\',\n            domains=[\'foobar.com\'],\n            routes=[\n                envoy.route.Route(\n                    name=\'catchall\',\n                    match=envoy.route.RouteMatch(\n                        prefix=\'/\'\n                    ),\n                    direct_response=envoy.route.DirectResponseAction(\n                        status=200,\n                        body=envoy.core.DataSource(\n                            inline_string=\'Hello there\'\n                        )\n                    )\n                )\n            ]\n        )\n    ]\n)\n\nresponse = envoy.DiscoveryResponse(\n    version_info=\'0\',\n    resources=[\n        route_config\n    ],\n)\n\nprint(\n    json.dumps(response.to_dict(casing=stringcase.snakecase), indent=2)\n)\n```\n\nResult:\n```\n{\n  "version_info": "0",\n  "resources": [\n    {\n      "name": "MyRouteConfig",\n      "virtual_hosts": [\n        {\n          "name": "SomeWebsite",\n          "domains": [\n            "foobar.com"\n          ],\n          "routes": [\n            {\n              "name": "catchall",\n              "match": {\n                "prefix": "/",\n                "headers": [],\n                "query_parameters": []\n              },\n              "direct_response": {\n                "status": 200,\n                "body": {\n                  "inline_string": "Hello there"\n                }\n              },\n              "request_headers_to_add": [],\n              "response_headers_to_add": []\n            }\n          ],\n          "virtual_clusters": [],\n          "rate_limits": [],\n          "request_headers_to_add": [],\n          "response_headers_to_add": []\n        }\n      ],\n      "response_headers_to_add": [],\n      "request_headers_to_add": []\n    }\n  ]\n}\n\n```\n',
    'author': 'Vasili Syrakis',
    'author_email': 'vsyrakis@atlassian.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

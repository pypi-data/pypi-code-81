# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/access_loggers/wasm/v3/wasm.proto
# plugin: python-betterproto
from dataclasses import dataclass

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class WasmAccessLog(betterproto.Message):
    """
    [[#not-implemented-hide:] Custom configuration for an :ref:`AccessLog
    <envoy_api_msg_config.accesslog.v3.AccessLog>` that calls into a WASM VM.
    """

    config: "___wasm_v3__.PluginConfig" = betterproto.message_field(1)


from ....wasm import v3 as ___wasm_v3__

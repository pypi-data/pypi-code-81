# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/filters/listener/proxy_protocol/v3/proxy_protocol.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class ProxyProtocol(betterproto.Message):
    # The list of rules to apply to requests.
    rules: List["ProxyProtocolRule"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class ProxyProtocolKeyValuePair(betterproto.Message):
    # The namespace — if this is empty, the filter's namespace will be used.
    metadata_namespace: str = betterproto.string_field(1)
    # The key to use within the namespace.
    key: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class ProxyProtocolRule(betterproto.Message):
    """
    A Rule defines what metadata to apply when a header is present or missing.
    """

    # The type that triggers the rule - required TLV type is defined as uint8_t
    # in proxy protocol. See `the spec
    # <https://www.haproxy.org/download/2.1/doc/proxy-protocol.txt>`_ for
    # details.
    tlv_type: int = betterproto.uint32_field(1)
    # If the TLV type is present, apply this metadata KeyValuePair.
    on_tlv_present: "ProxyProtocolKeyValuePair" = betterproto.message_field(2)

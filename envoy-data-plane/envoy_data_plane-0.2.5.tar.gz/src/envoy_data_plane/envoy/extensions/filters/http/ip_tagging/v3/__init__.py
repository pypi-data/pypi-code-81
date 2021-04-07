# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/filters/http/ip_tagging/v3/ip_tagging.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


class IpTaggingRequestType(betterproto.Enum):
    BOTH = 0
    INTERNAL = 1
    EXTERNAL = 2


@dataclass(eq=False, repr=False)
class IpTagging(betterproto.Message):
    # The type of request the filter should apply to.
    request_type: "IpTaggingRequestType" = betterproto.enum_field(1)
    # [#comment:TODO(ccaraman): Extend functionality to load IP tags from file
    # system. Tracked by issue https://github.com/envoyproxy/envoy/issues/2695]
    # The set of IP tags for the filter.
    ip_tags: List["IpTaggingIpTag"] = betterproto.message_field(4)


@dataclass(eq=False, repr=False)
class IpTaggingIpTag(betterproto.Message):
    """Supplies the IP tag name and the IP address subnets."""

    # Specifies the IP tag name to apply.
    ip_tag_name: str = betterproto.string_field(1)
    # A list of IP address subnets that will be tagged with ip_tag_name. Both
    # IPv4 and IPv6 are supported.
    ip_list: List["_____config_core_v3__.CidrRange"] = betterproto.message_field(2)


from ......config.core import v3 as _____config_core_v3__

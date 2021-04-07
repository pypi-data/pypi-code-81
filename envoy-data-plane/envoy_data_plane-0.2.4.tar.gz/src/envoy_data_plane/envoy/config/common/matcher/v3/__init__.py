# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/config/common/matcher/v3/matcher.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class MatchPredicate(betterproto.Message):
    """
    Match configuration. This is a recursive structure which allows complex
    nested match configurations to be built using various logical operators.
    [#next-free-field: 11]
    """

    # A set that describes a logical OR. If any member of the set matches, the
    # match configuration matches.
    or_match: "MatchPredicateMatchSet" = betterproto.message_field(1, group="rule")
    # A set that describes a logical AND. If all members of the set match, the
    # match configuration matches.
    and_match: "MatchPredicateMatchSet" = betterproto.message_field(2, group="rule")
    # A negation match. The match configuration will match if the negated match
    # condition matches.
    not_match: "MatchPredicate" = betterproto.message_field(3, group="rule")
    # The match configuration will always match.
    any_match: bool = betterproto.bool_field(4, group="rule")
    # HTTP request headers match configuration.
    http_request_headers_match: "HttpHeadersMatch" = betterproto.message_field(
        5, group="rule"
    )
    # HTTP request trailers match configuration.
    http_request_trailers_match: "HttpHeadersMatch" = betterproto.message_field(
        6, group="rule"
    )
    # HTTP response headers match configuration.
    http_response_headers_match: "HttpHeadersMatch" = betterproto.message_field(
        7, group="rule"
    )
    # HTTP response trailers match configuration.
    http_response_trailers_match: "HttpHeadersMatch" = betterproto.message_field(
        8, group="rule"
    )
    # HTTP request generic body match configuration.
    http_request_generic_body_match: "HttpGenericBodyMatch" = betterproto.message_field(
        9, group="rule"
    )
    # HTTP response generic body match configuration.
    http_response_generic_body_match: "HttpGenericBodyMatch" = (
        betterproto.message_field(10, group="rule")
    )


@dataclass(eq=False, repr=False)
class MatchPredicateMatchSet(betterproto.Message):
    """A set of match configurations used for logical operations."""

    # The list of rules that make up the set.
    rules: List["MatchPredicate"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class HttpHeadersMatch(betterproto.Message):
    """HTTP headers match configuration."""

    # HTTP headers to match.
    headers: List["___route_v3__.HeaderMatcher"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class HttpGenericBodyMatch(betterproto.Message):
    """
    HTTP generic body match configuration. List of text strings and hex strings
    to be located in HTTP body. All specified strings must be found in the HTTP
    body for positive match. The search may be limited to specified number of
    bytes from the body start. .. attention::   Searching for patterns in HTTP
    body is potentially cpu intensive. For each specified pattern, http body is
    scanned byte by byte to find a match.   If multiple patterns are specified,
    the process is repeated for each pattern. If location of a pattern is
    known, ``bytes_limit`` should be specified   to scan only part of the http
    body.
    """

    # Limits search to specified number of bytes - default zero (no limit - match
    # entire captured buffer).
    bytes_limit: int = betterproto.uint32_field(1)
    # List of patterns to match.
    patterns: List["HttpGenericBodyMatchGenericTextMatch"] = betterproto.message_field(
        2
    )


@dataclass(eq=False, repr=False)
class HttpGenericBodyMatchGenericTextMatch(betterproto.Message):
    # Text string to be located in HTTP body.
    string_match: str = betterproto.string_field(1, group="rule")
    # Sequence of bytes to be located in HTTP body.
    binary_match: bytes = betterproto.bytes_field(2, group="rule")


from ....route import v3 as ___route_v3__

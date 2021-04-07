# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/filters/http/gzip/v3/gzip.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import Optional

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


class GzipCompressionStrategy(betterproto.Enum):
    DEFAULT = 0
    FILTERED = 1
    HUFFMAN = 2
    RLE = 3


class GzipCompressionLevelEnum(betterproto.Enum):
    DEFAULT = 0
    BEST = 1
    SPEED = 2


@dataclass(eq=False, repr=False)
class Gzip(betterproto.Message):
    """[#next-free-field: 12]"""

    # Value from 1 to 9 that controls the amount of internal memory used by zlib.
    # Higher values use more memory, but are faster and produce better
    # compression results. The default value is 5.
    memory_level: Optional[int] = betterproto.message_field(
        1, wraps=betterproto.TYPE_UINT32
    )
    # A value used for selecting the zlib compression level. This setting will
    # affect speed and amount of compression applied to the content. "BEST"
    # provides higher compression at the cost of higher latency, "SPEED" provides
    # lower compression with minimum impact on response time. "DEFAULT" provides
    # an optimal result between speed and compression. This field will be set to
    # "DEFAULT" if not specified.
    compression_level: "GzipCompressionLevelEnum" = betterproto.enum_field(3)
    # A value used for selecting the zlib compression strategy which is directly
    # related to the characteristics of the content. Most of the time "DEFAULT"
    # will be the best choice, though there are situations which changing this
    # parameter might produce better results. For example, run-length encoding
    # (RLE) is typically used when the content is known for having sequences
    # which same data occurs many consecutive times. For more information about
    # each strategy, please refer to zlib manual.
    compression_strategy: "GzipCompressionStrategy" = betterproto.enum_field(4)
    # Value from 9 to 15 that represents the base two logarithmic of the
    # compressor's window size. Larger window results in better compression at
    # the expense of memory usage. The default is 12 which will produce a 4096
    # bytes window. For more details about this parameter, please refer to zlib
    # manual > deflateInit2.
    window_bits: Optional[int] = betterproto.message_field(
        9, wraps=betterproto.TYPE_UINT32
    )
    # Set of configuration parameters common for all compression filters. If this
    # field is set then the fields `content_length`, `content_type`,
    # `disable_on_etag_header` and `remove_accept_encoding_header` are ignored.
    compressor: "__compressor_v3__.Compressor" = betterproto.message_field(10)
    # Value for Zlib's next output buffer. If not set, defaults to 4096. See
    # https://www.zlib.net/manual.html for more details. Also see
    # https://github.com/envoyproxy/envoy/issues/8448 for context on this
    # filter's performance.
    chunk_size: Optional[int] = betterproto.message_field(
        11, wraps=betterproto.TYPE_UINT32
    )


@dataclass(eq=False, repr=False)
class GzipCompressionLevel(betterproto.Message):
    pass


from ...compressor import v3 as __compressor_v3__

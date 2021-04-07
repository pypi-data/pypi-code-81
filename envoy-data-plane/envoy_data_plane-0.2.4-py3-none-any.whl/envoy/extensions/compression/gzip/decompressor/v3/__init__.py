# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: envoy/extensions/compression/gzip/decompressor/v3/gzip.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import Optional

import betterproto
from betterproto.grpc.grpclib_server import ServiceBase


@dataclass(eq=False, repr=False)
class Gzip(betterproto.Message):
    # Value from 9 to 15 that represents the base two logarithmic of the
    # decompressor's window size. The decompression window size needs to be equal
    # or larger than the compression window size. The default is 12 to match the
    # default in the :ref:`gzip compressor <envoy_api_field_extensions.compressio
    # n.gzip.compressor.v3.Gzip.window_bits>`. For more details about this
    # parameter, please refer to `zlib manual
    # <https://www.zlib.net/manual.html>`_ > inflateInit2.
    window_bits: Optional[int] = betterproto.message_field(
        1, wraps=betterproto.TYPE_UINT32
    )
    # Value for zlib's decompressor output buffer. If not set, defaults to 4096.
    # See https://www.zlib.net/manual.html for more details.
    chunk_size: Optional[int] = betterproto.message_field(
        2, wraps=betterproto.TYPE_UINT32
    )

# -*- coding: UTF-8 -*-
# BSD 3-Clause License
#
# Copyright (c) 2021, InterlockLedger
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import io
import struct


def read_bytes(n: int, reader: io.IOBase) -> bytes:
    """
    Reads the specified number of bytes from the reader. It raises an 
    `EOFError` if the specified number of bytes is not available.

    Parameters:
    - `n`: The number of bytes to read;
    - `reader`: The reader;

    Returns the bytes read.
    """
    buff = reader.read(n)
    if not isinstance(buff, bytes):
        raise ValueError('The reader is expected to return bytes.')
    if len(buff) != n:
        raise EOFError(f'Unable to read {n} bytes from the stream.')
    return buff


def read_binary32(reader: io.IOBase) -> float:
    """
    Reads a binary32 floating point value from the reader. It must be
    encoded using IEEE 754-2008 in big endian value. It may raise `EOFError`
    if it is not able to read the specified number of bytes.
    """
    return struct.unpack('>f', read_bytes(4, reader))[0]


def read_binary64(reader: io.IOBase) -> float:
    """
    Reads a binary64 floating point value from the reader. It must be
    encoded using IEEE 754-2008 in big endian value. It may raise `EOFError`
    if it is not able to read the specified number of bytes.
    """
    return struct.unpack('>d', read_bytes(8, reader))[0]


def read_binary128(reader: io.IOBase) -> bytes:
    """
    Reads a binary128 floating point value from the reader. It must be
    encoded using IEEE 754-2008 in big endian value. It may raise `EOFError`
    if it is not able to read the specified number of bytes.

    Note: binary128 is not supported by Python, it will return its bytes
    instead.
    """
    return read_bytes(16, reader)


def write_binary32(value: float, writer: io.IOBase) -> None:
    """
    Writes a binary32 floating point value to the writer. It will be
    encoded using IEEE 754-2008 in big endian value.
    """
    writer.write(struct.pack('>f', value))


def write_binary64(value: float, writer: io.IOBase) -> None:
    """
    Writes a binary64 floating point value to the writer. It will be
    encoded using IEEE 754-2008 in big endian value.
    """
    writer.write(struct.pack('>d', value))


def write_binary128(value: bytes, writer: io.IOBase) -> None:
    """
    Writes a binary128 floating point value to the writer. It will be
    encoded using IEEE 754-2008 in big endian value.
    """
    if len(value) != 16:
        raise ValueError('Invalid binary128.')
    writer.write(value)


def read_int(size: int, signed: bool, reader: io.IOBase) -> int:
    """
    Reads an integer from the reader. It is always threated as a big endian
    value.

    Parameters:
    - `size`: The size of the value in bytes;
    - `signed`: A flag that determines if the encoding is signed or not;
    - `reader`: The reader;

    Returns the value read.
    """
    return int.from_bytes(read_bytes(size, reader), byteorder='big', signed=signed)


def write_int(value: int, size: int, signed: bool, writer: io.IOBase):
    """
    Writes an integer into the writer. It is always encoded as a big endian
    value.

    Parameters:
    - `value`: The value to be written;
    - `size`: The size of the value in bytes;
    - `signed`: A flag that determines if the encoding is signed or not;
    - `writer`: The writer;

    It may raise `OverflowError` if the `value` cannot be represented using
    the specfied size.
    """
    writer.write(value.to_bytes(size, byteorder='big', signed=signed))


class LimitedReaderWrapper(io.IOBase):
    """
    This class implements a wrapper over an io.IOBase instance that limits
    the amount of values that can be read from it.
    """

    def __init__(self, reader: io.IOBase, remaining: int, skip_close: bool = True) -> None:
        """
        Creates a new instance of this class.

        Parameters:
        - `reader`: The inner reader to wrap;
        - `remaining`: The number of bytes remaining;
        - `skip_close`: If True, closing this instance will not close the inner reader, otherwise,
          it will do so.
        """
        self.reader = reader
        self.remaining = remaining
        self.skip_close = skip_close

    def close(self):
        """
        If `skip_close` is set to True, the inner close will not be called otherwise
        it will call the inner reader close() method.
        """
        if not self.skip_close:
            self.reader.close()

    @property
    def closed(self) -> bool:
        """
        Just a proxy to the inner reader property.
        """
        return self.reader.closed

    def flush(self) -> None:
        """
        Just a proxy to the inner reader method.
        """
        self.reader.flush()

    def isatty(self) -> bool:
        """
        Just a proxy to the inner reader method.
        """
        return self.reader.isatty()

    def readable(self) -> bool:
        """
        Just a proxy to the inner reader method.
        """
        return self.reader.readable()

    def tell(self) -> int:
        """
        Just a proxy to the inner reader method.
        """
        return self.reader.tell()

    def read(self, size: int = -1) -> bytes:
        if self.remaining == 0:
            return b''
        else:
            if size == -1:
                r = self.remaining
                self.remaining = 0
            else:
                r = min(self.remaining, size)
                self.remaining -= r
            return self.reader.read(r)

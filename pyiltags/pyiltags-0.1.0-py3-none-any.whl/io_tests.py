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
import unittest
from unittest.mock import MagicMock, PropertyMock
import math
from .io import *


class TestIO(unittest.TestCase):

    def generate_bytes(self, size: int) -> bytes:
        buff = bytearray()
        for i in range(size):
            buff.append(i & 0xFF)
        return bytes(buff)

    def test_read_bytes(self):

        for size in range(0, 33):
            sample = self.generate_bytes(size)
            r = read_bytes(size, io.BytesIO(sample))
            self.assertEqual(r, sample)

        for size in range(0, 33):
            sample = self.generate_bytes(size)
            self.assertRaises(EOFError, read_bytes,
                              size + 1, io.BytesIO(sample))

    def test_read_binary32(self):
        # Examples extracted from https://en.wikipedia.org/wiki/Single-precision_floating-point_format
        src = io.BytesIO(bytes.fromhex('3f800000'))
        f = read_binary32(src)
        self.assertEqual(1.0, f)

        src = io.BytesIO(bytes.fromhex('3e800000'))
        f = read_binary32(src)
        self.assertEqual(0.25, f)

        src = io.BytesIO(bytes.fromhex('3ec00000'))
        f = read_binary32(src)
        self.assertEqual(0.375, f)

        src = io.BytesIO(bytes.fromhex('00000001'))
        f = read_binary32(src)
        self.assertEqual(1.401298464324817e-45, f)

        src = io.BytesIO(bytes.fromhex('007fffff'))
        f = read_binary32(src)
        self.assertEqual(1.1754942106924411e-38, f)

        src = io.BytesIO(bytes.fromhex('40490fdb'))
        f = read_binary32(src)
        self.assertEqual(3.1415927410125732, f)

        src = io.BytesIO(bytes.fromhex('ff800000'))
        f = read_binary32(src)
        self.assertEqual(-math.inf, f)

        src = io.BytesIO(bytes.fromhex('ff8000'))
        self.assertRaises(EOFError, read_binary32, src)

    def test_read_binary64(self):
        # Examples extracted from https://en.wikipedia.org/wiki/Double-precision_floating-point_format
        src = io.BytesIO(bytes.fromhex('3FF0000000000000'))
        f = read_binary64(src)
        self.assertEqual(1.0, f)

        src = io.BytesIO(bytes.fromhex('3FF0000000000001'))
        f = read_binary64(src)
        self.assertEqual(1.0000000000000002, f)

        src = io.BytesIO(bytes.fromhex('C000000000000000'))
        f = read_binary64(src)
        self.assertEqual(-2.0, f)

        src = io.BytesIO(bytes.fromhex('0000000000000001'))
        f = read_binary64(src)
        self.assertEqual(5e-324, f)

        src = io.BytesIO(bytes.fromhex('7FEFFFFFFFFFFFFF'))
        f = read_binary64(src)
        self.assertEqual(1.7976931348623157e+308, f)

        src = io.BytesIO(bytes.fromhex('400921FB54442D18'))
        f = read_binary64(src)
        self.assertEqual(3.141592653589793, f)

        src = io.BytesIO(bytes.fromhex('FFF0000000000000'))
        f = read_binary64(src)
        self.assertEqual(-math.inf, f)

        src = io.BytesIO(bytes.fromhex('FFF00000000000'))
        self.assertRaises(EOFError, read_binary64, src)

    def test_read_binary128(self):
        bin = self.generate_bytes(16)
        src = io.BytesIO(bin)
        f = read_binary128(src)
        self.assertTrue(isinstance(f, bytes))
        self.assertEqual(bin, f)

    def test_write_binary32(self):
        writer = io.BytesIO()
        write_binary32(3.1415927410125732, writer)
        exp = bytes.fromhex('40490fdb')
        writer.seek(0)
        self.assertEqual(exp, writer.read())

    def test_write_binary64(self):
        writer = io.BytesIO()
        write_binary64(3.141592653589793, writer)
        exp = bytes.fromhex('400921FB54442D18')
        writer.seek(0)
        self.assertEqual(exp, writer.read())

    def test_write_binary128(self):
        exp = self.generate_bytes(16)
        writer = io.BytesIO()
        write_binary128(exp, writer)
        writer.seek(0)
        self.assertEqual(exp, writer.read())
        self.assertRaises(ValueError, write_binary128,
                          self.generate_bytes(15), writer)
        self.assertRaises(ValueError, write_binary128,
                          self.generate_bytes(17), writer)

    def test_read_int(self):
        sample = bytes.fromhex('FEDCBA9876543210')

        for size in [1, 2, 4, 8]:
            s = sample[:size]
            for signed in [False, True]:
                exp = int.from_bytes(s, byteorder='big', signed=signed)
                reader = io.BytesIO(s)
                self.assertEqual(exp, read_int(size, signed, reader))

        for size in [1, 2, 4, 8]:
            s = sample[:size - 1]
            for signed in [False, True]:
                reader = io.BytesIO(s)
                self.assertRaises(EOFError, read_int, size, signed, reader)

    def test_write_int(self):
        sample = bytes.fromhex('FEDCBA9876543210')

        for size in [1, 2, 4, 8]:
            s = sample[:size]
            for signed in [False, True]:
                value = int.from_bytes(s, byteorder='big', signed=signed)
                writer = io.BytesIO()
                write_int(value, size, signed, writer)
                writer.seek(0)
                self.assertEqual(s, writer.read())

        writer = io.BytesIO()
        for size in [1, 2, 4, 8]:
            write_int(0, size, False, writer)
            write_int(2**(size * 8) - 1, size, False, writer)
            self.assertRaises(OverflowError, write_int,
                              -1, size, False, writer)
            self.assertRaises(OverflowError, write_int,
                              2**(size * 8), size, False, writer)

            base = 2**(size * 8 - 1)
            write_int(-base, size, True, writer)
            write_int(base - 1, size, True, writer)
            self.assertRaises(OverflowError, write_int,
                              -(base + 1), size, True, writer)
            self.assertRaises(OverflowError, write_int,
                              base, size, True, writer)


class TestLimitedReaderWrapper(unittest.TestCase):

    def sample_bytes(self, count: int) -> bytes:
        ret = bytearray()
        for i in range(count):
            ret.append(i & 0xFF)
        return bytes(ret)

    def test_constructor(self):
        reader = io.BytesIO(self.sample_bytes(16))
        r = LimitedReaderWrapper(reader, 10)
        self.assertEqual(reader, r.reader)
        self.assertEqual(10, r.remaining)
        self.assertTrue(r.skip_close)

        r = LimitedReaderWrapper(reader, 10, False)
        self.assertEqual(reader, r.reader)
        self.assertEqual(10, r.remaining)
        self.assertFalse(r.skip_close)

    def test_close(self):
        reader = io.BytesIO()
        reader.close = MagicMock()
        r = LimitedReaderWrapper(reader, 10)
        r.close()
        reader.close.assert_not_called()

        r = LimitedReaderWrapper(reader, 10, False)
        r.close()
        reader.close.assert_called_once()

    def test_closed(self):
        reader = io.BytesIO()
        r = LimitedReaderWrapper(reader, 10)
        self.assertFalse(r.closed)
        reader.close()
        self.assertTrue(r.closed)

    def test_flush(self):
        reader = io.BytesIO()
        reader.flush = MagicMock()
        r = LimitedReaderWrapper(reader, 10)
        r.flush()
        reader.flush.assert_called_once()

    def test_isatty(self):
        reader = io.BytesIO()
        reader.isatty = MagicMock()
        r = LimitedReaderWrapper(reader, 10)
        r.isatty()
        reader.isatty.assert_called_once()

    def test_readable(self):
        reader = io.BytesIO()
        reader.readable = MagicMock()
        r = LimitedReaderWrapper(reader, 10)
        r.readable()
        reader.readable.assert_called_once()

    def test_read(self):
        sample = self.sample_bytes(16)

        reader = io.BytesIO(sample)
        r = LimitedReaderWrapper(reader, 10)
        b = r.read()
        self.assertEqual(sample[:10], b)
        self.assertEqual(b'', r.read())

        reader = io.BytesIO(sample)
        r = LimitedReaderWrapper(reader, 10)
        b = r.read(128)
        self.assertEqual(sample[:10], b)
        self.assertEqual(b'', r.read())

        for chunck_size in range(1, 16):
            r = LimitedReaderWrapper(reader, 10)
            ret = b''
            used = 0
            while used < 10:
                ret += r.read(chunck_size)
                used += chunck_size
            self.assertEqual(0, r.remaining)
            self.assertEqual(sample[:10], b)

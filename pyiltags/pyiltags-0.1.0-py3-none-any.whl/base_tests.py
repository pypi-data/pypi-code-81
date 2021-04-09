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
from unittest import mock
from unittest.mock import MagicMock

from pyilint import ilint_encode_to_stream, ilint_size
from .base import *


class TestBaseFunctions(unittest.TestCase):

    def test_iltags_assert_valid_id(self):
        iltags_assert_valid_id(0)
        iltags_assert_valid_id(2**64 - 1)
        self.assertRaises(ValueError, iltags_assert_valid_id, -1)
        self.assertRaises(ValueError, iltags_assert_valid_id, 2**64)

    def test_iltags_is_implicit(self):
        self.assertRaises(ValueError, iltags_is_implicit, -1)
        self.assertRaises(ValueError, iltags_is_implicit, 2**64)
        for id in range(16):
            self.assertTrue(iltags_is_implicit(id))
        self.assertFalse(iltags_is_implicit(16))
        self.assertFalse(iltags_is_implicit(32))
        self.assertFalse(iltags_is_implicit(64))

    def test_iltags_is_standard(self):
        self.assertRaises(ValueError, iltags_is_standard, -1)
        self.assertRaises(ValueError, iltags_is_standard, 2**64)
        for id in range(32):
            self.assertTrue(iltags_is_standard(id))
        self.assertFalse(iltags_is_standard(32))
        self.assertFalse(iltags_is_standard(64))


class TestILTagFactory(unittest.TestCase):

    def test_constructor(self):
        c = ILTagFactory()
        self.assertFalse(c.strict)
        self.assertRaises(NotImplementedError, c.create, 10)
        self.assertRaises(NotImplementedError, c.deserialize, io.BytesIO())

        c = ILTagFactory(True)
        self.assertTrue(c.strict)
        self.assertRaises(NotImplementedError, c.create, 10)
        self.assertRaises(NotImplementedError, c.deserialize, io.BytesIO())

        c = ILTagFactory(False)
        self.assertFalse(c.strict)
        self.assertRaises(NotImplementedError, c.create, 10)
        self.assertRaises(NotImplementedError, c.deserialize, io.BytesIO())


class TestILTag(unittest.TestCase):

    def test_constructor(self):
        t = ILTag(0, True)
        self.assertEqual(t.id, 0)

        t = ILTag(2**64 - 1)
        self.assertEqual(t.id, 2**64 - 1)

        for id in range(16):
            self.assertRaises(ValueError, ILTag, id, False)
        self.assertRaises(ValueError, ILTag, -1)
        self.assertRaises(ValueError, ILTag, 2**64)

    def test_implicit(self):
        for id in range(16):
            t = ILTag(id, True)
            self.assertTrue(t.implicit)
        t = ILTag(16)
        self.assertFalse(t.implicit)

    def test_standard(self):
        for id in range(32):
            t = ILTag(id, True)
            self.assertTrue(t.standard)
        t = ILTag(32)
        self.assertFalse(t.standard)

    def test_value_size(self):
        t = ILTag(123)
        self.assertRaises(NotImplementedError, t.value_size)

    def test_tag_size(self):
        for id in range(16):
            t = ILTag(id, True)
            t.value_size = MagicMock(return_value=id)
            size = ilint_size(id) + id
            self.assertEqual(t.tag_size(), size)
            t.value_size.assert_called_once()

        for id in [16, 256, 1231231]:
            t = ILTag(id)
            t.value_size = MagicMock(return_value=id)
            size = ilint_size(id) + ilint_size(id) + id
            self.assertEqual(t.tag_size(), size)
            t.value_size.assert_called_once()

    def test_deserialize_value(self):
        t = ILTag(123)
        self.assertRaises(NotImplementedError, t.deserialize_value,
                          ILTagFactory(), 0, io.BytesIO())

    def test_serialize_value(self):
        t = ILTag(123)
        self.assertRaises(NotImplementedError, t.serialize_value, io.BytesIO())

    def test_serialize(self):
        class DummyILTag(ILTag):
            def value_size(self) -> int:
                return 4

            def serialize_value(self, writer: io.IOBase) -> None:
                writer.write(b'1234')

        # Normal tag with no payload
        t = DummyILTag(65535)
        writer = io.BytesIO()
        t.serialize(writer)

        exp = io.BytesIO()
        ilint_encode_to_stream(65535, exp)
        ilint_encode_to_stream(4, exp)
        exp.write(b'1234')
        exp.seek(0)
        writer.seek(0)
        self.assertEqual(exp.read(), writer.read())

        # Implicit
        t = DummyILTag(1, True)
        writer = io.BytesIO()
        t.serialize(writer)

        exp = io.BytesIO()
        ilint_encode_to_stream(1, exp)
        exp.write(b'1234')
        exp.seek(0)
        writer.seek(0)
        self.assertEqual(exp.read(), writer.read())

    def test_compute_tag_size(self):

        for value_size in [0, 15, 16, 0xFFFF, 0xFFFFFFFFFFFFFFFF]:
            for id in range(16):
                exp = pyilint.ilint_size(id) + value_size
                self.assertEqual(exp, ILTag.compute_tag_size(id, value_size))

            for id in [16, 0xFFFF, 0xFFFFFFFFFFFFFFFF]:
                exp = pyilint.ilint_size(
                    id) + pyilint.ilint_size(value_size) + value_size
                self.assertEqual(exp, ILTag.compute_tag_size(id, value_size))


class TestILRawTag(unittest.TestCase):

    def test_constructor(self):
        t = ILRawTag(16)

        t.value = b'1234'
        self.assertEqual(b'1234', t.value)

        t.value = bytearray(b'1234')
        self.assertEqual(b'1234', t.value)

        t.value = None
        self.assertIsNone(t.value)

        for v in ['', '1234', 1, 15, 1.0, []]:
            with self.assertRaises(TypeError):
                t.value = v

    def test_default_value(self):
        class ILRawTagNewDefault(ILRawTag):
            DEFAULT_VALUE = b''

        t = ILRawTag(16)
        self.assertEqual(None, t.default_value)

        t = ILRawTagNewDefault(16)
        self.assertEqual(b'', t.default_value)

    def test_assert_value_valid(self):
        t = ILRawTag(16)

        t.assert_value_valid(b'')

    def test_value(self):
        class ILRawTagNewDefault(ILRawTag):
            DEFAULT_VALUE = b''

        t = ILRawTag(16, b'1234')

        self.assertEqual(b'1234', t.value)
        self.assertFalse(isinstance(t.value, bytearray))
        self.assertTrue(isinstance(t.value, bytes))

        t.value = None
        self.assertEqual(None, t.value)

        t.value = bytearray(b'5678')
        self.assertEqual(b'5678', t.value)
        self.assertFalse(isinstance(t.value, bytearray))
        self.assertTrue(isinstance(t.value, bytes))

        t = ILRawTagNewDefault(16)
        t.value = None
        self.assertEqual(b'', t.value)

        t = ILRawTag(16, b'1234')
        t.assert_value_valid = mock.MagicMock()
        t.value = None
        t.assert_value_valid.assert_not_called()
        t.value = b''
        t.assert_value_valid.assert_called()
        t.assert_value_valid.reset_mock()
        t.value = bytearray(b'')
        t.assert_value_valid.assert_called()

        t.value = b'1234'
        t.assert_value_valid = mock.MagicMock(side_effect=ValueError)
        with self.assertRaises(ValueError):
            t.value = b''
        self.assertEqual(b'1234', t.value)

    def test_deserialize_value(self):
        t = ILRawTag(16)
        reader = io.BytesIO(b'1234')
        t.deserialize_value(None, 0, reader)
        self.assertEqual(0, reader.tell())
        self.assertEqual(b'', t.value)
        self.assertEqual(0, t.value_size())

        t = ILRawTag(16)
        reader = io.BytesIO(b'1234')
        t.deserialize_value(None, 3, reader)
        self.assertEqual(3, reader.tell())
        self.assertEqual(b'123', t.value)
        self.assertEqual(3, t.value_size())

        t = ILRawTag(16)
        reader = io.BytesIO(b'1234')
        self.assertRaises(EOFError, t.deserialize_value, None, 5, reader)

    def test_serialize(self):
        t = ILRawTag(16)
        writer = io.BytesIO()
        t.serialize(writer)
        exp = io.BytesIO()
        ilint_encode_to_stream(16, exp)
        ilint_encode_to_stream(0, exp)
        writer.seek(0)
        exp.seek(0)
        self.assertEqual(exp.read(), writer.read())

        t = ILRawTag(256, b'')
        writer = io.BytesIO()
        t.serialize(writer)
        exp = io.BytesIO()
        ilint_encode_to_stream(256, exp)
        ilint_encode_to_stream(0, exp)
        writer.seek(0)
        exp.seek(0)
        self.assertEqual(exp.read(), writer.read())

        t = ILRawTag(12312312, b'0123456789')
        writer = io.BytesIO()
        t.serialize(writer)
        exp = io.BytesIO()
        ilint_encode_to_stream(12312312, exp)
        ilint_encode_to_stream(10, exp)
        exp.write(b'0123456789')
        writer.seek(0)
        exp.seek(0)
        self.assertEqual(exp.read(), writer.read())


class TestILFixedSizeTag(unittest.TestCase):

    def test_constructor(self):
        t = ILFixedSizeTag(0, 0, True)
        self.assertEqual(0, t.id)
        self.assertEqual(0, t.value_size())

        t = ILFixedSizeTag(16, 12)
        self.assertEqual(16, t.id)
        self.assertEqual(12, t.value_size())


class TestILBaseIntTag(unittest.TestCase):

    def constructor_test_core(self, value_size: int):
        bits = value_size * 8
        for v in [0, 2**bits - 1]:
            t = ILBaseIntTag(12, value_size, False, v, True)
            self.assertEqual(12, t.id)
            self.assertEqual(value_size, t.value_size())
            self.assertEqual(v, t.value)
            self.assertFalse(t.signed)
        self.assertRaises(ValueError, ILBaseIntTag, 0, value_size, False, -1)
        self.assertRaises(ValueError, ILBaseIntTag, 0,
                          value_size, False, 2**bits)
        bits -= 1
        for v in [-(2**bits), (2**bits) - 1]:
            t = ILBaseIntTag(13, value_size, True, v, True)
            self.assertEqual(13, t.id)
            self.assertEqual(value_size, t.value_size())
            self.assertEqual(v, t.value)
            self.assertTrue(t.signed)
        self.assertRaises(ValueError, ILBaseIntTag, 0,
                          value_size, True, -(2**bits + 1))
        self.assertRaises(ValueError, ILBaseIntTag, 0,
                          value_size, True, 2**bits)

    def test_constructor(self):
        self.constructor_test_core(1)
        self.constructor_test_core(2)
        self.constructor_test_core(4)
        self.constructor_test_core(8)
        for value_size in [0, 3, 5, 6, 7, 9]:
            self.assertRaises(ValueError, ILBaseIntTag, 0,
                              value_size, False, 0)
            self.assertRaises(ValueError, ILBaseIntTag, 0,
                              value_size, True, 0)

    def value_core(self, value_size: int):
        bits = value_size * 8
        for v in [0, 2**bits - 1]:
            t = ILBaseIntTag(12, value_size, False, 0, True)
            t.value = v
            self.assertEqual(v, t.value)
        for v in [-1, 2**bits]:
            t = ILBaseIntTag(12, value_size, False, 0, True)
            with self.assertRaises(ValueError):
                t.value = v
        bits -= 1
        for v in [-(2**bits), (2**bits) - 1]:
            t = ILBaseIntTag(12, value_size, True, 0, True)
            t.value = v
            self.assertEqual(v, t.value)
        for v in [-(2 ** bits + 1), 2**bits]:
            t = ILBaseIntTag(12, value_size, True, 0, True)
            with self.assertRaises(ValueError):
                t.value = v

    def test_value(self):
        self.value_core(1)
        self.value_core(2)
        self.value_core(4)
        self.value_core(8)

    def deserialize_value_core(self, value_size: int, signed: bool):
        sample = b'FEDCBA9876543210'

        t = ILBaseIntTag(0, value_size, signed, 0, True)
        reader = io.BytesIO(sample[:value_size])
        t.deserialize_value(None, value_size, reader)
        exp = int.from_bytes(sample[:value_size],
                             byteorder='big', signed=signed)
        self.assertEqual(exp, t.value)
        self.assertRaises(EOFError, t.deserialize_value,
                          None, value_size, reader)
        self.assertRaises(EOFError, t.deserialize_value,
                          None, value_size - 1, reader)

    def test_deserialize_value(self):
        self.deserialize_value_core(1, False)
        self.deserialize_value_core(1, True)
        self.deserialize_value_core(2, False)
        self.deserialize_value_core(2, True)
        self.deserialize_value_core(4, False)
        self.deserialize_value_core(4, True)
        self.deserialize_value_core(8, False)
        self.deserialize_value_core(8, True)

    def serialize_value_core(self, value_size: int, signed: bool):
        sample = b'FEDCBA9876543210'

        val = int.from_bytes(sample[:value_size],
                             byteorder='big', signed=signed)
        t = ILBaseIntTag(0, value_size, signed, val, True)
        writer = io.BytesIO()
        t.serialize_value(writer)
        self.assertEqual(value_size, writer.tell())
        writer.seek(0)
        self.assertEqual(sample[:value_size], writer.read())

    def test_serialize_value(self):
        self.serialize_value_core(1, False)
        self.serialize_value_core(1, True)
        self.serialize_value_core(2, False)
        self.serialize_value_core(2, True)
        self.serialize_value_core(4, False)
        self.serialize_value_core(4, True)
        self.serialize_value_core(8, False)
        self.serialize_value_core(8, True)


class TestILBaseFloatTag(unittest.TestCase):

    def test_constructor(self):
        t = ILBaseFloatTag(1, 4, allow_implicit=True)
        self.assertEqual(1, t.id)
        self.assertEqual(4, t.value_size())
        self.assertEqual(0, t.value)

        t = ILBaseFloatTag(1, 4, 1.0, allow_implicit=True)
        self.assertEqual(1, t.id)
        self.assertEqual(4, t.value_size())
        self.assertEqual(1.0, t.value)

        t = ILBaseFloatTag(1, 8, allow_implicit=True)
        self.assertEqual(1, t.id)
        self.assertEqual(8, t.value_size())
        self.assertEqual(0, t.value)

        t = ILBaseFloatTag(1, 8, 1.0, allow_implicit=True)
        self.assertEqual(1, t.id)
        self.assertEqual(8, t.value_size())
        self.assertEqual(1.0, t.value)

        self.assertRaises(ValueError, ILBaseFloatTag, 1, 3, 0.0)
        self.assertRaises(ValueError, ILBaseFloatTag, 1, 5, 0.0)
        self.assertRaises(ValueError, ILBaseFloatTag, 1, 7, 0.0)
        self.assertRaises(ValueError, ILBaseFloatTag, 1, 9, 0.0)

    def test_value(self):
        t = ILBaseFloatTag(1, 4, allow_implicit=True)
        self.assertEqual(0, t.value)
        self.assertTrue(isinstance(t.value, float))
        t.value = 1
        self.assertEqual(1.0, t.value)
        self.assertTrue(isinstance(t.value, float))

        t = ILBaseFloatTag(1, 8, allow_implicit=True)
        self.assertEqual(0, t.value)
        self.assertTrue(isinstance(t.value, float))
        t.value = 1
        self.assertEqual(1.0, t.value)
        self.assertTrue(isinstance(t.value, float))

    def test_deserialize_value(self):
        val = 3.1415927410125732
        serialized = struct.pack('>f', val)
        t = ILBaseFloatTag(1, 4, allow_implicit=True)
        t.deserialize_value(None, 4, io.BytesIO(serialized))
        self.assertEqual(val, t.value)
        self.assertRaises(EOFError, t.deserialize_value,
                          None, 3, io.BytesIO(serialized))
        self.assertRaises(EOFError, t.deserialize_value,
                          None, 4, io.BytesIO(serialized[:-1]))

        val = 3.141592653589793
        serialized = struct.pack('>d', val)
        t = ILBaseFloatTag(1, 8, allow_implicit=True)
        t.deserialize_value(None, 8, io.BytesIO(serialized))
        self.assertEqual(val, t.value)
        self.assertRaises(EOFError, t.deserialize_value,
                          None, 7, io.BytesIO(serialized))
        self.assertRaises(EOFError, t.deserialize_value,
                          None, 8, io.BytesIO(serialized[:-1]))

    def test_serialize_value(self):
        val = 3.1415927410125732
        serialized = struct.pack('>f', val)
        t = ILBaseFloatTag(1, 4, val, True)
        writer = io.BytesIO()
        t.serialize_value(writer)
        self.assertEqual(4, writer.tell())
        writer.seek(0)
        self.assertEqual(serialized, writer.read())

        val = 3.141592653589793
        serialized = struct.pack('>d', val)
        t = ILBaseFloatTag(1, 8, val, True)
        writer = io.BytesIO()
        t.serialize_value(writer)
        self.assertEqual(8, writer.tell())
        writer.seek(0)
        self.assertEqual(serialized, writer.read())

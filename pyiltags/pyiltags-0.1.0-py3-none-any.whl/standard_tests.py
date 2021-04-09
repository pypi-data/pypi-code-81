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
from io import SEEK_END
from typing import Callable, Type
import codecs
import unittest
import random
from .standard import *

# Text example extracted from O Alienista by Machado de Assis.
STRING_SAMPLES = """
As crônicas da vila de Itaguaí dizem que em tempos remotos vivera ali um certo
médico, o Dr. Simão Bacamarte, filho da nobreza da terra e o maior dos médicos
do Brasil, de Portugal e das Espanhas. Estudara em Coimbra e Pádua. Aos trinta
e quatro anos regressou ao Brasil, não podendo el-rei alcançar dele que ficasse
em Coimbra, regendo a universidade, ou em Lisboa, expedindo os negócios da monarquia.
""".split()

# Unique words extracted from STRING_SAMPLES
STRING_KEY_SAMPLES = \
    ['trinta', 'regendo', 'Simão', 'ficasse', 'terra', 'que', 'de', 'remotos',
     'Portugal', 'um', 'da', 'anos', 'universidade,', 'a', 'vila', 'quatro',
     'Coimbra,', 'vivera', 'alcançar', 'certo', 'dizem', 'Lisboa,', 'expedindo',
     'os', 'Dr.', 'regressou', 'das', 'dele', 'filho', 'Bacamarte,', 'e', 'dos',
     'não', 'el-rei', 'Brasil,', 'Aos', 'médico,', 'médicos', 'do', 'nobreza',
     'ali', 'maior', 'As', 'crônicas', 'em', 'Espanhas.', 'Estudara', 'Pádua.',
     'o', 'ou', 'Coimbra', 'ao', 'Itaguaí', 'negócios', 'monarquia.', 'tempos',
     'podendo']


def generate_random_tag(id: int = None) -> ILTag:
    if id is None:
        id = random.randrange(0, 2**64)
    size = random.randrange(0, 1024)
    payload = bytearray()
    for i in range(size):
        payload.append(random.randrange(0, 256))
    return ILRawTag(id, payload)


SAMPLE_ILINT_VALUES = [
    0,
    0xFE,
    0xFEDC,
    0xFEDCBA,
    0xFEDCBA98,
    0xFEDCBA9876,
    0xFEDCBA987654,
    0xFEDCBA98765432,
    0xFEDCBA9876543210,
]

BASIC_TAG_SAMPLES = [
    ILNullTag(),
    ILBoolTag(),
    ILInt8Tag(1),
    ILUInt8Tag(2),
    ILInt16Tag(3),
    ILUInt16Tag(4),
    ILInt32Tag(5),
    ILUInt32Tag(6),
    ILInt64Tag(7),
    ILUInt64Tag(8),
    ILILInt64Tag(0),
    ILILInt64Tag(0xFE),
    ILILInt64Tag(0xFEDC),
    ILILInt64Tag(0xFEDCBA),
    ILILInt64Tag(0xFEDCBA98),
    ILILInt64Tag(0xFEDCBA9876),
    ILILInt64Tag(0xFEDCBA987654),
    ILILInt64Tag(0xFEDCBA98765432),
    ILILInt64Tag(0xFEDCBA9876543210),
    ILBinary32Tag(1.0),
    ILBinary64Tag(2.0),
    ILBinary128Tag(),
    ILByteArrayTag(b'1234567890'),
    ILStringTag('1234567890'),
    ILBigIntegerTag(b'1234567890'),
    ILBigDecimalTag(b'1234567890', -1),
    ILIntArrayTag([0xFE, 0xFEDCBA9876543210]),
    ILTagArrayTag(),
    ILTagSequenceTag(),
    ILRangeTag(123, 456),
    ILVersionTag(1, 2, 3, 4),
    ILOIDTag([1, 2, 3, 4]),
    ILDictionaryTag(),
    ILStringDictionaryTag()
]


def __create_sample_dict():
    n = min(len(BASIC_TAG_SAMPLES), len(STRING_KEY_SAMPLES))
    ret = []
    for i in range(n):
        ret.append((STRING_KEY_SAMPLES[i], BASIC_TAG_SAMPLES[i]))
    return ret


SAMPLE_DICT = __create_sample_dict()


class TestILTagIds(unittest.TestCase):

    def test_standard_ids(self):
        self.assertEqual(ILTAG_NULL_ID, 0)
        self.assertEqual(ILTAG_BOOL_ID, 1)
        self.assertEqual(ILTAG_INT8_ID, 2)
        self.assertEqual(ILTAG_UINT8_ID, 3)
        self.assertEqual(ILTAG_INT16_ID, 4)
        self.assertEqual(ILTAG_UINT16_ID, 5)
        self.assertEqual(ILTAG_INT32_ID, 6)
        self.assertEqual(ILTAG_UINT32_ID, 7)
        self.assertEqual(ILTAG_INT64_ID, 8)
        self.assertEqual(ILTAG_UINT64_ID, 9)
        self.assertEqual(ILTAG_ILINT64_ID, 10)
        self.assertEqual(ILTAG_BINARY32_ID, 11)
        self.assertEqual(ILTAG_BINARY64_ID, 12)
        self.assertEqual(ILTAG_BINARY128_ID, 13)
        self.assertEqual(ILTAG_BYTE_ARRAY_ID, 16)
        self.assertEqual(ILTAG_STRING_ID, 17)
        self.assertEqual(ILTAG_BINT_ID, 18)
        self.assertEqual(ILTAG_BDEC_ID, 19)
        self.assertEqual(ILTAG_ILINT64_ARRAY_ID, 20)
        self.assertEqual(ILTAG_ILTAG_ARRAY_ID, 21)
        self.assertEqual(ILTAG_ILTAG_SEQ_ID, 22)
        self.assertEqual(ILTAG_RANGE_ID, 23)
        self.assertEqual(ILTAG_VERSION_ID, 24)
        self.assertEqual(ILTAG_OID_ID, 25)
        self.assertEqual(ILTAG_DICT_ID, 30)
        self.assertEqual(ILTAG_STRDICT_ID, 31)


class TestILNullTag(unittest.TestCase):

    def test_contructor(self):
        t = ILNullTag()
        self.assertEqual(ILTAG_NULL_ID, t.id)
        self.assertEqual(0, t.value_size())

        t = ILNullTag(123)
        self.assertEqual(123, t.id)
        self.assertEqual(0, t.value_size())

    def test_deserialize_value(self):
        t = ILNullTag()
        reader = io.BytesIO(b'123456')
        t.deserialize_value(None, 0, reader)
        self.assertEqual(0, reader.tell())
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 1, reader)

    def test_serialize_value(self):
        t = ILNullTag()
        writer = io.BytesIO()
        t.serialize_value(writer)
        self.assertEqual(0, writer.tell())


class TestILBoolTag(unittest.TestCase):

    def test_contructor(self):
        t = ILBoolTag()
        self.assertEqual(ILTAG_BOOL_ID, t.id)
        self.assertEqual(1, t.value_size())
        self.assertFalse(t.value)

        t = ILBoolTag(False)
        self.assertEqual(ILTAG_BOOL_ID, t.id)
        self.assertEqual(1, t.value_size())
        self.assertFalse(t.value)

        t = ILBoolTag(True)
        self.assertEqual(ILTAG_BOOL_ID, t.id)
        self.assertEqual(1, t.value_size())
        self.assertTrue(t.value)

        t = ILBoolTag(False, 123123)
        self.assertEqual(123123, t.id)
        self.assertEqual(1, t.value_size())
        self.assertFalse(t.value)

        t = ILBoolTag(True, 123123)
        self.assertEqual(123123, t.id)
        self.assertEqual(1, t.value_size())
        self.assertTrue(t.value)

    def test_value(self):
        t = ILBoolTag()

        for v in [False, 0, None, b'', '', []]:
            t.value = v
            self.assertFalse(t.value)
        for v in [True, 1, 1.0, b'x', 'z', [1]]:
            t.value = v
            self.assertTrue(t.value)

    def test_deserialize_value(self):
        t = ILBoolTag(True)

        t.deserialize_value(None, 1, io.BytesIO(b'\x00'))
        self.assertFalse(t.value)

        t.deserialize_value(None, 1, io.BytesIO(b'\x01'))
        self.assertTrue(t.value)

        self.assertRaises(EOFError,
                          t.deserialize_value, None, 0, io.BytesIO(b'\x00'))
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 2, io.BytesIO(b'\x0001'))
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 1, io.BytesIO(b'\x02'))

    def test_serialize_value(self):
        t = ILBoolTag()

        writer = io.BytesIO()
        t.serialize_value(writer)
        self.assertEqual(1, writer.tell())
        writer.seek(0)
        self.assertEqual(b'\x00', writer.read())

        t.value = True
        writer = io.BytesIO()
        t.serialize_value(writer)
        self.assertEqual(1, writer.tell())
        writer.seek(0)
        self.assertEqual(b'\x01', writer.read())


class BaseTestILIntTag(unittest.TestCase):
    def constructor_core(self, tag_class: Callable, exp_size: int, default_id: int, signed: bool):
        t = tag_class()
        self.assertEqual(default_id, t.id)
        self.assertEqual(exp_size, t.value_size())
        self.assertEqual(0, t.value)
        self.assertEqual(signed, t.signed)

        t = tag_class(123)
        self.assertEqual(default_id, t.id)
        self.assertEqual(exp_size, t.value_size())
        self.assertEqual(123, t.value)
        self.assertEqual(signed, t.signed)

        t = tag_class(123, 456)
        self.assertEqual(456, t.id)
        self.assertEqual(exp_size, t.value_size())
        self.assertEqual(123, t.value)
        self.assertEqual(signed, t.signed)

    def test_constructor(self):
        self.constructor_core(ILInt8Tag, 1, ILTAG_INT8_ID, True)
        self.constructor_core(ILUInt8Tag, 1, ILTAG_UINT8_ID, False)
        self.constructor_core(ILInt16Tag, 2, ILTAG_INT16_ID, True)
        self.constructor_core(ILUInt16Tag, 2, ILTAG_UINT16_ID, False)
        self.constructor_core(ILInt32Tag, 4, ILTAG_INT32_ID, True)
        self.constructor_core(ILUInt32Tag, 4, ILTAG_UINT32_ID, False)
        self.constructor_core(ILInt64Tag, 8, ILTAG_INT64_ID, True)
        self.constructor_core(ILUInt64Tag, 8, ILTAG_UINT64_ID, False)


class TestILILInt64Tag(unittest.TestCase):

    def test_constructor(self):
        t = ILILInt64Tag()
        self.assertEqual(ILTAG_ILINT64_ID, t.id)
        self.assertEqual(0, t.value)

        t = ILILInt64Tag(123)
        self.assertEqual(ILTAG_ILINT64_ID, t.id)
        self.assertEqual(123, t.value)

        t = ILILInt64Tag(123, 456)
        self.assertEqual(456, t.id)
        self.assertEqual(123, t.value)

        self.assertRaises(ValueError, ILILInt64Tag, -1)
        self.assertRaises(ValueError, ILILInt64Tag, 2**64)
        self.assertRaises(TypeError, ILILInt64Tag, '1')
        self.assertRaises(TypeError, ILILInt64Tag, 1.0)

    def test_value(self):
        t = ILILInt64Tag()

        t.value = 0
        self.assertEqual(0, t.value)

        t.value = 2**64 - 1
        self.assertEqual(2**64 - 1, t.value)

        for v in ['', '1', b'123', 1.0]:
            with self.assertRaises(TypeError):
                t.value = v
        for v in [-1, 2**64]:
            with self.assertRaises(ValueError):
                t.value = v

    def test_value_size(self):

        for v in [0, 0xFF, 0xFFFF, 0xFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF,
                  0xFFFFFFFFFF, 0xFFFFFFFFFFFF,
                  0xFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF]:
            t = ILILInt64Tag(v)
            self.assertEqual(pyilint.ilint_size(t.value), t.value_size())

    def test_deserialize_value_implicit(self):

        for v in [0, 0xFF, 0xFFFF, 0xFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF,
                  0xFFFFFFFFFF, 0xFFFFFFFFFFFF,
                  0xFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF]:
            t = ILILInt64Tag()
            val = bytearray()
            size = pyilint.ilint_encode(v, val)
            reader = io.BytesIO(val)
            t.deserialize_value(None, size, reader)
            self.assertEqual(size, reader.tell())
            self.assertEqual(v, t.value)

        t = ILILInt64Tag()
        reader = io.BytesIO(bytes.fromhex('FFFFFFFFFFFFFFFFFF'))
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 9, reader)
        reader.seek(0)
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 0, reader)
        reader.seek(0)
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 10, reader)
        reader.seek(0)
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 8, reader)

    def test_deserialize_value_explicit(self):

        for v in [0, 0xFF, 0xFFFF, 0xFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF,
                  0xFFFFFFFFFF, 0xFFFFFFFFFFFF,
                  0xFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF]:
            t = ILILInt64Tag(id=1234)
            val = bytearray()
            size = pyilint.ilint_encode(v, val)
            reader = io.BytesIO(val)
            t.deserialize_value(None, size, reader)
            self.assertEqual(size, reader.tell())
            self.assertEqual(v, t.value)

        t = ILILInt64Tag(id=1234)
        reader = io.BytesIO(bytes.fromhex('FFFFFFFFFFFFFFFFFF00'))
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 9, reader)
        reader.seek(0)
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 0, reader)
        reader.seek(0)
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 10, reader)
        reader.seek(0)
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 8, reader)

    def test_serialize_value(self):

        for v in [0, 0xFF, 0xFFFF, 0xFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF,
                  0xFFFFFFFFFF, 0xFFFFFFFFFFFF,
                  0xFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF]:
            t = ILILInt64Tag(v)

            val = bytearray()
            size = pyilint.ilint_encode(v, val)

            writer = io.BytesIO()
            t.serialize_value(writer)
            self.assertEqual(size, writer.tell())
            writer.seek(0)
            self.assertEqual(val, writer.read())


class TestILBinary32_64Tag(unittest.TestCase):

    def constructor_core(self, tag_class, id: int, size: int):
        t = tag_class()
        self.assertEqual(id, t.id)
        self.assertEqual(0.0, t.value)
        self.assertEqual(size, t.value_size())

        t = tag_class(1.0)
        self.assertEqual(id, t.id)
        self.assertEqual(1.0, t.value)
        self.assertEqual(size, t.value_size())

        t = tag_class(1.0, 1234)
        self.assertEqual(1234, t.id)
        self.assertEqual(1.0, t.value)
        self.assertEqual(size, t.value_size())

    def test_constructor(self):
        self.constructor_core(ILBinary32Tag, ILTAG_BINARY32_ID, 4)
        self.constructor_core(ILBinary64Tag, ILTAG_BINARY64_ID, 8)


class TestILBinary128Tag(unittest.TestCase):

    def test_constructor(self):
        t = ILBinary128Tag()
        self.assertEqual(ILTAG_BINARY128_ID, t.id)
        self.assertEqual(b'\x00' * 16, t.value)
        self.assertEqual(16, t.value_size())

        t = ILBinary128Tag(None)
        self.assertEqual(ILTAG_BINARY128_ID, t.id)
        self.assertEqual(b'\x00' * 16, t.value)
        self.assertEqual(16, t.value_size())

        t = ILBinary128Tag(b'\x01' * 16)
        self.assertEqual(ILTAG_BINARY128_ID, t.id)
        self.assertEqual(b'\x01' * 16, t.value)
        self.assertEqual(16, t.value_size())

        t = ILBinary128Tag(b'\x01' * 16, 1234)
        self.assertEqual(1234, t.id)
        self.assertEqual(b'\x01' * 16, t.value)
        self.assertEqual(16, t.value_size())

    def test_value(self):
        t = ILBinary128Tag()

        v = b'\x12' * 16
        t.value = v
        self.assertEqual(v, t.value)

        v = b'\x12' * 16
        t.value = bytearray(v)
        self.assertEqual(v, t.value)

        t.value = None
        self.assertEqual(b'\x00' * 16, t.value)

        for v in [1, 1.0, '1', b'\x00' * 15, b'\x00' * 17]:
            with self.assertRaises(TypeError):
                t.value = v

    def test_deserialize_value(self):
        t = ILBinary128Tag()
        exp = b'\x12' * 16
        reader = io.BytesIO(exp + exp)
        t.deserialize_value(None, 16, reader)
        self.assertEqual(exp, t.value)
        self.assertRaises(EOFError, t.deserialize_value, None, 15, reader)
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 17, reader)

    def test_serialize_value(self):
        exp = b'\x12' * 16
        t = ILBinary128Tag(exp)
        writer = io.BytesIO()
        t.serialize_value(writer)
        self.assertEqual(16, writer.tell())
        writer.seek(0)
        self.assertEqual(exp, writer.read())


class TestILByteArrayTag(unittest.TestCase):

    def test_constructor(self):
        t = ILByteArrayTag()
        self.assertEqual(ILTAG_BYTE_ARRAY_ID, t.id)
        self.assertEqual(None, t.value)

        paylod = b'1234'
        t = ILByteArrayTag(paylod)
        self.assertEqual(ILTAG_BYTE_ARRAY_ID, t.id)
        self.assertEqual(paylod, t.value)

        t = ILByteArrayTag(paylod, 1234)
        self.assertEqual(1234, t.id)
        self.assertEqual(paylod, t.value)


class TestILStringTag(unittest.TestCase):

    def test_constructor(self):
        t = ILStringTag()
        self.assertEqual(ILTAG_STRING_ID, t.id)
        self.assertEqual('', t.value)
        self.assertEqual(b'', t.utf8)

        t = ILStringTag('abc')
        self.assertEqual(ILTAG_STRING_ID, t.id)
        self.assertEqual('abc', t.value)
        self.assertEqual(b'abc', t.utf8)

        t = ILStringTag('abc', 1234)
        self.assertEqual(1234, t.id)
        self.assertEqual('abc', t.value)
        self.assertEqual(b'abc', t.utf8)

    def test_value(self):
        t = ILStringTag()

        sample = 'Blade Runner - O Caçador de Andróides'
        sample_utf8 = codecs.encode(sample, 'utf-8')
        t.value = sample
        self.assertEqual(sample, t.value)
        self.assertEqual(sample_utf8, t.utf8)

        t.value = None
        self.assertEqual('', t.value)
        self.assertEqual(b'', t.utf8)

        for v in [1, 1.0, [], b'123']:
            with self.assertRaises(TypeError):
                t.value = v

    def test_utf8(self):
        t = ILStringTag()

        sample = 'Blade Runner - O Caçador de Andróides'
        sample_utf8 = codecs.encode(sample, 'utf-8')
        t.utf8 = sample_utf8
        self.assertEqual(sample, t.value)
        self.assertEqual(sample_utf8, t.utf8)

        t.utf8 = None
        self.assertEqual('', t.value)
        self.assertEqual(b'', t.utf8)

        with self.assertRaises(ValueError):
            t.utf8 = b'\xF0\x90\x8D'
        self.assertEqual('', t.value)
        self.assertEqual(b'', t.utf8)

        for v in [1, 1.0, []]:
            with self.assertRaises(TypeError):
                t.utf8 = v

    def test_value_size(self):
        t = ILStringTag()

        self.assertEqual(0, t.value_size())

        sample = 'Blade Runner - O Caçador de Andróides'
        sample_utf8 = codecs.encode(sample, 'utf-8')
        t.value = sample
        self.assertEqual(len(sample_utf8), t.value_size())

    def test_deserialize_value(self):
        t = ILStringTag()

        sample = 'Blade Runner - O Caçador de Andróides'
        sample_utf8 = codecs.encode(sample, 'utf-8')

        reader = io.BytesIO(sample_utf8)
        t.deserialize_value(None, len(sample_utf8), reader)
        self.assertEqual(len(sample_utf8), reader.tell())
        self.assertEqual(sample, t.value)
        self.assertEqual(sample_utf8, t.utf8)

        reader = io.BytesIO(sample_utf8)
        t.deserialize_value(None, len(sample_utf8), reader)
        self.assertEqual(len(sample_utf8), reader.tell())
        self.assertEqual(sample, t.value)
        self.assertEqual(sample_utf8, t.utf8)

        reader = io.BytesIO()
        t.deserialize_value(None, 0, reader)
        self.assertEqual(0, reader.tell())
        self.assertEqual('', t.value)
        self.assertEqual(b'', t.utf8)

        self.assertRaises(ILTagCorruptedError, t.deserialize_value,
                          None, 3, io.BytesIO(b'\xF0\x90\x8D'))

    def test_serialize_value(self):
        t = ILStringTag()

        writer = io.BytesIO()
        t.serialize_value(writer)
        self.assertEqual(0, writer.tell())

        sample = 'Blade Runner - O Caçador de Andróides'
        sample_utf8 = codecs.encode(sample, 'utf-8')

        t.value = sample
        writer = io.BytesIO()
        t.serialize_value(writer)
        self.assertEqual(len(sample_utf8), writer.tell())
        writer.seek(0)
        self.assertEqual(sample_utf8, writer.read())

    def test_to_utf8(self):
        for s in STRING_SAMPLES:
            utf8 = ILStringTag.to_utf8(s)
            exp = codecs.encode(s, 'utf-8')
            self.assertEqual(exp, utf8)

    def test_from_utf8(self):
        for s in STRING_SAMPLES:
            self.assertEqual(s, ILStringTag.from_utf8(
                codecs.encode(s, 'utf-8')))
            self.assertEqual(s, ILStringTag.from_utf8(
                ILStringTag.to_utf8(s)))

    def test_size_in_utf8(self):
        for s in STRING_SAMPLES:
            exp = codecs.encode(s, 'utf-8')
            self.assertEqual(len(exp), ILStringTag.size_in_utf8(s))

    def test_compute_string_tag_size(self):
        for s in STRING_SAMPLES:
            t = ILStringTag(s)
            self.assertEqual(
                t.tag_size(), ILStringTag.compute_string_tag_size(s))

        for s in STRING_SAMPLES:
            t = ILStringTag(s, 0xFFFFFFFF)
            self.assertEqual(
                t.tag_size(), ILStringTag.compute_string_tag_size(s, 0xFFFFFFFF))

    def test_serialize_tag_from_components(self):

        for s in STRING_SAMPLES:
            t = ILStringTag(s)
            exp = io.BytesIO()
            t.serialize(exp)
            writer = io.BytesIO()
            size = ILStringTag.serialize_tag_from_components(s, writer)
            self.assertEqual(size, writer.tell())
            self.assertEqual(exp.tell(), writer.tell())
            exp.seek(0)
            writer.seek(0)
            self.assertEqual(exp.read(), writer.read())

        alt_id = 0xFFFFFFFF
        for s in STRING_SAMPLES:
            t = ILStringTag(s, alt_id)
            exp = io.BytesIO()
            t.serialize(exp)
            writer = io.BytesIO()
            size = ILStringTag.serialize_tag_from_components(s, writer, alt_id)
            self.assertEqual(size, writer.tell())
            self.assertEqual(exp.tell(), writer.tell())
            exp.seek(0)
            writer.seek(0)
            self.assertEqual(exp.read(), writer.read())

    def test_is_standard_string(self):
        self.assertTrue(ILStringTag.is_standard_string(ILStringTag()))

        self.assertFalse(ILStringTag.is_standard_string(
            ILStringTag(id=123123)))
        self.assertFalse(ILStringTag.is_standard_string(
            ILRawTag(ILTAG_STRING_ID)))


class TestILBigIntegerTag(unittest.TestCase):

    def test_constructor(self):
        t = ILBigIntegerTag()
        self.assertEqual(ILTAG_BINT_ID, t.id)
        self.assertEqual(b'\x00', t.value)

        t = ILBigIntegerTag(b'12345')
        self.assertEqual(ILTAG_BINT_ID, t.id)
        self.assertEqual(b'12345', t.value)

        t = ILBigIntegerTag(b'12345', 123)
        self.assertEqual(123, t.id)
        self.assertEqual(b'12345', t.value)

    def test_default(self):
        t = ILBigIntegerTag()
        self.assertEqual(b'\x00', t.default_value)

    def test_assert_value_valid(self):
        t = ILBigIntegerTag()
        t.assert_value_valid(b'\x00')
        self.assertRaises(ValueError, t.assert_value_valid, b'')


class TestILBigDecimalTag(unittest.TestCase):

    def test_constructor(self):
        t = ILBigDecimalTag()
        self.assertEqual(ILTAG_BDEC_ID, t.id)
        self.assertEqual(b'\0', t.value)
        self.assertEqual(0, t.scale)

        t = ILBigDecimalTag(b'1234')
        self.assertEqual(ILTAG_BDEC_ID, t.id)
        self.assertEqual(b'1234', t.value)
        self.assertEqual(0, t.scale)

        t = ILBigDecimalTag(b'1234', -10)
        self.assertEqual(ILTAG_BDEC_ID, t.id)
        self.assertEqual(b'1234', t.value)
        self.assertEqual(-10, t.scale)

        t = ILBigDecimalTag(b'1234', -10, 123456)
        self.assertEqual(123456, t.id)
        self.assertEqual(b'1234', t.value)
        self.assertEqual(-10, t.scale)

    def test_scale(self):
        t = ILBigDecimalTag()

        t.scale = -(2**31)
        self.assertEqual(-(2**31), t.scale)
        t.scale = 2**31 - 1
        self.assertEqual(2**31 - 1, t.scale)

        t.scale = 1
        for v in [1.0, [], '123']:
            with self.assertRaises(TypeError):
                t.scale = v
            self.assertEqual(1, t.scale)

        for v in [-(2**31 + 1), 2**31]:
            with self.assertRaises(ValueError):
                t.scale = v
            self.assertEqual(1, t.scale)

    def test_value_size(self):
        t = ILBigDecimalTag()
        self.assertEqual(4 + 1, t.value_size())

        t = ILBigDecimalTag(b'123456')
        self.assertEqual(4 + 6, t.value_size())

    def test_deserialize_value(self):
        t = ILBigDecimalTag()

        reader = io.BytesIO()
        write_int(-123, 4, True, reader)
        reader.write(b'123456789')
        tag_size = reader.tell()

        reader.seek(0)
        t.deserialize_value(None, tag_size, reader)
        self.assertEqual(-123, t.scale)
        self.assertEqual(b'123456789', t.value)

        reader.seek(0)
        t.deserialize_value(None, 5, reader)
        self.assertEqual(-123, t.scale)
        self.assertEqual(b'1', t.value)

        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, 4, reader)
        self.assertRaises(EOFError,
                          t.deserialize_value, None, tag_size+1, reader)

    def test_serialize_value(self):

        scale = -123
        value = b'123456789'

        exp = io.BytesIO()
        write_int(scale, 4, True, exp)
        exp.write(value)
        tag_size = exp.tell()

        t = ILBigDecimalTag(value, scale)
        writer = io.BytesIO()
        t.serialize_value(writer)
        self.assertEqual(exp.tell(), writer.tell())
        exp.seek(0)
        writer.seek(0)
        self.assertEqual(exp.read(), writer.read())


class TestILIntArrayTag(unittest.TestCase):

    def test_constructor(self):
        t = ILIntArrayTag()
        self.assertEqual(ILTAG_ILINT64_ARRAY_ID, t.id)
        self.assertEqual(0, len(t))

        t = ILIntArrayTag([1, 2, 3])
        self.assertEqual(ILTAG_ILINT64_ARRAY_ID, t.id)
        self.assertEqual(3, len(t))
        self.assertEqual(1, t[0])
        self.assertEqual(2, t[1])
        self.assertEqual(3, t[2])

        t = ILIntArrayTag(None, 1234)
        self.assertEqual(1234, t.id)
        self.assertEqual(0, len(t))

        t = ILIntArrayTag([1, 2, 3], 123)
        self.assertEqual(123, t.id)
        self.assertEqual(3, len(t))
        self.assertEqual(1, t[0])
        self.assertEqual(2, t[1])
        self.assertEqual(3, t[2])

    def test_assert_value_type(self):
        t = ILIntArrayTag()

        t.assert_value_type(0)
        t.assert_value_type(2**64 - 1)
        self.assertRaises(ValueError, t.assert_value_type, -1)
        self.assertRaises(ValueError, t.assert_value_type, 2**64)
        self.assertRaises(TypeError, t.assert_value_type, '')
        self.assertRaises(TypeError, t.assert_value_type, 1.0)

    def test_value_size(self):
        t = ILIntArrayTag()
        self.assertEqual(1, t.value_size())
        for count in range(256):
            t.append(random.randrange(0, 2**64))
            exp = pyilint.ilint_size(len(t))
            for v in t:
                exp += pyilint.ilint_size(v)
            self.assertEqual(exp, t.value_size())

    def test_deserialize_value(self):
        values = []
        for _ in range(0, 256, 8):
            values.append(random.randrange(0, 2**64))
            reader = io.BytesIO()
            pyilint.ilint_encode_to_stream(len(values), reader)
            for v in values:
                pyilint.ilint_encode_to_stream(v, reader)
            tag_size = reader.tell()
            reader.seek(0)
            t = ILIntArrayTag()
            t.deserialize_value(None, tag_size, reader)
            self.assertEqual(tag_size, reader.tell())
            self.assertEqual(len(values), len(t))
            for i in range(len(t)):
                self.assertEqual(values[i], t[i])

    def test_serialize_value(self):
        values = []
        for _ in range(0, 256, 8):
            values.append(random.randrange(0, 2**64))
            reader = io.BytesIO()
            pyilint.ilint_encode_to_stream(len(values), reader)
            for v in values:
                pyilint.ilint_encode_to_stream(v, reader)

            t = ILIntArrayTag()
            for v in values:
                t.append(v)
            writer = io.BytesIO()
            t.serialize_value(writer)
            self.assertEqual(reader.tell(), writer.tell())
            reader.seek(0)
            writer.seek(0)
            self.assertEqual(reader.read(), writer.read())


class ILTagComparatorMixin:
    def assertILTagEqual(self, a: ILTag, b: ILTag):
        self.assertEqual(a.id, b.id)
        # It is the most inefficient way possible but works
        aw = io.BytesIO()
        bw = io.BytesIO()
        a.serialize_value(aw)
        b.serialize_value(bw)
        aw.seek(0)
        bw.seek(0)
        self.assertEqual(aw.read(), bw.read())


class TestILTagArrayTag(unittest.TestCase, ILTagComparatorMixin):

    def test_constructor(self):
        t = ILTagArrayTag()
        self.assertEqual(ILTAG_ILTAG_ARRAY_ID, t.id)
        self.assertEqual(0, len(t))

        t = ILTagArrayTag(BASIC_TAG_SAMPLES)
        self.assertEqual(ILTAG_ILTAG_ARRAY_ID, t.id)
        self.assertEqual(len(BASIC_TAG_SAMPLES), len(t))
        for i in range(len(BASIC_TAG_SAMPLES)):
            self.assertILTagEqual(BASIC_TAG_SAMPLES[i], t[i])

        t = ILTagArrayTag(BASIC_TAG_SAMPLES, 1234)
        self.assertEqual(1234, t.id)
        self.assertEqual(len(BASIC_TAG_SAMPLES), len(t))
        for i in range(len(BASIC_TAG_SAMPLES)):
            self.assertILTagEqual(BASIC_TAG_SAMPLES[i], t[i])

    def test_assert_value_type(self):
        t = ILTagArrayTag()
        for tag in BASIC_TAG_SAMPLES:
            t.assert_value_type(tag)
        self.assertRaises(TypeError, t.assert_value_type, None)
        self.assertRaises(TypeError, t.assert_value_type, 'a')
        self.assertRaises(TypeError, t.assert_value_type, 1)
        self.assertRaises(TypeError, t.assert_value_type, 1.0)
        self.assertRaises(TypeError, t.assert_value_type, [])

    def test_value_size(self):

        t = ILTagArrayTag()
        tags = []
        for tag in BASIC_TAG_SAMPLES:
            tags.append(tag)
            t.append(tag)
            value_size = pyilint.ilint_size(len(tags))
            for v in tags:
                value_size += v.tag_size()
            self.assertEqual(value_size, t.value_size())

    def test_deserialize_value(self):

        tags = []
        t = ILTagArrayTag()
        for tag in BASIC_TAG_SAMPLES:
            tags.append(tag)
            reader = io.BytesIO()
            pyilint.ilint_encode_to_stream(len(tags), reader)
            for v in tags:
                v.serialize(reader)
            value_size = reader.tell()
            reader.seek(0)
            t.deserialize_value(ILStandardTagFactory(), value_size, reader)
            self.assertEqual(value_size, reader.tell())
            for i in range(len(tags)):
                self.assertILTagEqual(tags[i], t[i])

            reader.seek(0)
            self.assertRaises(ILTagCorruptedError, t.deserialize_value,
                              ILStandardTagFactory(), value_size - 1, reader)
            reader.seek(0)
            reader.write(b'\xFF')
            reader.seek(0)
            self.assertRaises(ILTagCorruptedError, t.deserialize_value,
                              ILStandardTagFactory(), value_size, reader)

    def test_serialize_value(self):

        tags = []
        for tag in BASIC_TAG_SAMPLES:
            t = ILTagArrayTag()
            tags.append(tag)
            exp = io.BytesIO()
            pyilint.ilint_encode_to_stream(len(tags), exp)
            for v in tags:
                v.serialize(exp)
                t.append(v)

            writer = io.BytesIO()
            t.serialize_value(writer)
            self.assertEqual(exp.tell(), writer.tell())
            exp.seek(0)
            writer.seek(0)
            self.assertEqual(exp.read(), writer.read())


class TestILTagSequenceTag(unittest.TestCase, ILTagComparatorMixin):
    def test_constructor(self):
        t = ILTagSequenceTag()
        self.assertEqual(ILTAG_ILTAG_SEQ_ID, t.id)
        self.assertEqual(0, len(t))

        t = ILTagSequenceTag(BASIC_TAG_SAMPLES)
        self.assertEqual(ILTAG_ILTAG_SEQ_ID, t.id)
        self.assertEqual(len(BASIC_TAG_SAMPLES), len(t))
        for i in range(len(BASIC_TAG_SAMPLES)):
            self.assertILTagEqual(BASIC_TAG_SAMPLES[i], t[i])

        t = ILTagSequenceTag(BASIC_TAG_SAMPLES, 1234)
        self.assertEqual(1234, t.id)
        self.assertEqual(len(BASIC_TAG_SAMPLES), len(t))
        for i in range(len(BASIC_TAG_SAMPLES)):
            self.assertILTagEqual(BASIC_TAG_SAMPLES[i], t[i])

    def test_assert_value_type(self):
        t = ILTagSequenceTag()
        for tag in BASIC_TAG_SAMPLES:
            t.assert_value_type(tag)
        self.assertRaises(TypeError, t.assert_value_type, None)
        self.assertRaises(TypeError, t.assert_value_type, 'a')
        self.assertRaises(TypeError, t.assert_value_type, 1)
        self.assertRaises(TypeError, t.assert_value_type, 1.0)
        self.assertRaises(TypeError, t.assert_value_type, [])

    def test_value_size(self):

        t = ILTagSequenceTag()
        tags = []
        for tag in BASIC_TAG_SAMPLES:
            tags.append(tag)
            t.append(tag)
            value_size = 0
            for v in tags:
                value_size += v.tag_size()
            self.assertEqual(value_size, t.value_size())

    def test_deserialize_value(self):

        tags = []
        t = ILTagSequenceTag(BASIC_TAG_SAMPLES)
        reader = io.BytesIO()
        t.deserialize_value(ILStandardTagFactory(), 0, reader)

        for tag in BASIC_TAG_SAMPLES:
            tags.append(tag)
            reader = io.BytesIO()
            for v in tags:
                v.serialize(reader)
            value_size = reader.tell()
            reader.seek(0)
            t.deserialize_value(ILStandardTagFactory(), value_size, reader)
            self.assertEqual(value_size, reader.tell())
            for i in range(len(tags)):
                self.assertILTagEqual(tags[i], t[i])

            reader.seek(0)
            if value_size > 1:
                self.assertRaises(ILTagCorruptedError, t.deserialize_value,
                                  ILStandardTagFactory(), value_size - 1, reader)
            reader.seek(0, SEEK_END)
            reader.write(b'\xFF')
            reader.seek(0)
            self.assertRaises(ILTagCorruptedError, t.deserialize_value,
                              ILStandardTagFactory(), value_size + 1, reader)

    def test_serialize_value(self):

        tags = []
        for tag in BASIC_TAG_SAMPLES:
            t = ILTagSequenceTag()
            tags.append(tag)
            exp = io.BytesIO()
            for v in tags:
                v.serialize(exp)
                t.append(v)

            writer = io.BytesIO()
            t.serialize_value(writer)
            self.assertEqual(exp.tell(), writer.tell())
            exp.seek(0)
            writer.seek(0)
            self.assertEqual(exp.read(), writer.read())


class TestILRangeTag(unittest.TestCase):

    def test_constructor(self):
        t = ILRangeTag()
        self.assertEqual(ILTAG_RANGE_ID, t.id)
        self.assertEqual(0, t.first)
        self.assertEqual(0, t.count)

        t = ILRangeTag(1, 2)
        self.assertEqual(ILTAG_RANGE_ID, t.id)
        self.assertEqual(1, t.first)
        self.assertEqual(2, t.count)

        t = ILRangeTag(1, 2, 123)
        self.assertEqual(123, t.id)
        self.assertEqual(1, t.first)
        self.assertEqual(2, t.count)

    def test_first(self):
        t = ILRangeTag()
        t.first = 0
        t.first = (2**64) - 1
        with self.assertRaises(ValueError):
            t.first = -1
        with self.assertRaises(ValueError):
            t.first = 2**64

    def test_count(self):
        t = ILRangeTag()
        t.count = 0
        t.count = (2**16) - 1
        with self.assertRaises(ValueError):
            t.count = -1
        with self.assertRaises(ValueError):
            t.count = 2**16

    def test_value_size(self):

        for start in SAMPLE_ILINT_VALUES:
            t = ILRangeTag(start, 123)
            exp = pyilint.ilint_size(start) + 2
            self.assertEqual(exp, t.value_size())

    def test_deserialize_value(self):

        for first in SAMPLE_ILINT_VALUES:
            count = random.randrange(0, 2**16)
            reader = io.BytesIO()
            pyilint.ilint_encode_to_stream(first, reader)
            write_int(count, 2, False, reader)
            value_size = reader.tell()

            t = ILRangeTag()
            reader.seek(0)
            t.deserialize_value(None, value_size, reader)
            self.assertEqual(first, t.first)
            self.assertEqual(count, t.count)
            self.assertEqual(value_size, reader.tell())

        sample = b'\xFF' * 9 + b'12'
        reader = io.BytesIO(sample)
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, len(sample), reader)

        sample = b'\xFF' * 4
        reader = io.BytesIO(sample)
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, len(sample), reader)

        sample = b'\x001'
        reader = io.BytesIO(sample)
        self.assertRaises(ILTagCorruptedError,
                          t.deserialize_value, None, len(sample), reader)

        sample = b'\xf8\x001'
        reader = io.BytesIO(sample)
        self.assertRaises(EOFError,
                          t.deserialize_value, None, len(sample), reader)

    def test_serialize_value(self):

        for first in SAMPLE_ILINT_VALUES:
            count = random.randrange(0, 2**16)
            exp = io.BytesIO()
            pyilint.ilint_encode_to_stream(first, exp)
            write_int(count, 2, False, exp)

            t = ILRangeTag(first, count)
            writer = io.BytesIO()
            t.serialize_value(writer)
            self.assertEqual(exp.tell(), writer.tell())
            self.assertEqual(exp.read(), writer.read())


class TestILVersionTag(unittest.TestCase):
    def test_constructor(self):
        t = ILVersionTag()
        self.assertEqual(16, t.value_size())
        self.assertEqual(ILTAG_VERSION_ID, t.id)
        self.assertEqual(0, t.major)
        self.assertEqual(0, t.minor)
        self.assertEqual(0, t.revision)
        self.assertEqual(0, t.build)

        t = ILVersionTag(1, 2, 3, 4)
        self.assertEqual(16, t.value_size())
        self.assertEqual(ILTAG_VERSION_ID, t.id)
        self.assertEqual(1, t.major)
        self.assertEqual(2, t.minor)
        self.assertEqual(3, t.revision)
        self.assertEqual(4, t.build)

        t = ILVersionTag(1, 2, 3, 4, 13123)
        self.assertEqual(16, t.value_size())
        self.assertEqual(13123, t.id)
        self.assertEqual(1, t.major)
        self.assertEqual(2, t.minor)
        self.assertEqual(3, t.revision)
        self.assertEqual(4, t.build)

    def test_major(self):
        t = ILVersionTag()
        t.major = -(2**31)
        t.major = (2**31) - 1
        with self.assertRaises(ValueError):
            t.major = -(2**31 + 1)
        with self.assertRaises(ValueError):
            t.major = 2**31

    def test_minor(self):
        t = ILVersionTag()
        t.minor = -(2**31)
        t.minor = (2**31) - 1
        with self.assertRaises(ValueError):
            t.minor = -(2**31 + 1)
        with self.assertRaises(ValueError):
            t.minor = 2**31

    def test_revision(self):
        t = ILVersionTag()
        t.revision = -(2**31)
        t.revision = (2**31) - 1
        with self.assertRaises(ValueError):
            t.revision = -(2**31 + 1)
        with self.assertRaises(ValueError):
            t.revision = 2**31

    def test_build(self):
        t = ILVersionTag()
        t.build = -(2**31)
        t.build = (2**31) - 1
        with self.assertRaises(ValueError):
            t.build = -(2**31 + 1)
        with self.assertRaises(ValueError):
            t.build = 2**31

    def test_deserialize_value(self):

        for sample in [[1, 2, 3, 4], [-1, -2, -3, -4]]:
            reader = io.BytesIO()
            for v in sample:
                write_int(v, 4, True, reader)
            reader.seek(0)
            t = ILVersionTag()
            t.deserialize_value(None, 16, reader)
            self.assertEqual(sample[0], t.major)
            self.assertEqual(sample[1], t.minor)
            self.assertEqual(sample[2], t.revision)
            self.assertEqual(sample[3], t.build)
            reader.seek(0)
            self.assertRaises(ILTagCorruptedError,
                              t.deserialize_value, None, 15, reader)
            reader.seek(1)
            self.assertRaises(EOFError,
                              t.deserialize_value, None, 16, reader)

    def test_serialize_value(self):

        for sample in [[1, 2, 3, 4], [-1, -2, -3, -4]]:
            exp = io.BytesIO()
            for v in sample:
                write_int(v, 4, True, exp)
            t = ILVersionTag(sample[0], sample[1], sample[2], sample[3])
            writer = io.BytesIO()
            t.serialize_value(writer)
            self.assertEqual(exp.tell(), writer.tell())
            exp.seek(0)
            writer.seek(0)
            self.assertEqual(exp.read(), writer.read())


class TestILOIDTag(unittest.TestCase):
    def test_constructor(self):
        t = ILOIDTag()
        self.assertEqual(ILTAG_OID_ID, t.id)
        self.assertEqual(0, len(t))

        t = ILOIDTag([1, 2, 3])
        self.assertEqual(ILTAG_OID_ID, t.id)
        self.assertEqual(3, len(t))
        self.assertEqual(1, t[0])
        self.assertEqual(2, t[1])
        self.assertEqual(3, t[2])


class TestILDictionaryTag(unittest.TestCase, ILTagComparatorMixin):

    def test_constructor(self):
        t = ILDictionaryTag()
        self.assertEqual(ILTAG_DICT_ID, t.id)
        self.assertEqual(0, len(t))

        t = ILDictionaryTag(1234)
        self.assertEqual(1234, t.id)
        self.assertEqual(0, len(t))

    def test_assert_value_type(self):
        t = ILDictionaryTag()
        t.assert_value_type(ILNullTag())
        t.assert_value_type(ILRawTag(123))
        for k in [1, 1.0, [], '1']:
            self.assertRaises(TypeError, t.assert_value_type, k)

    def test_assert_key_type(self):
        t = ILDictionaryTag()
        t.assert_key_type('')
        t.assert_key_type('123')
        for k in [1, 1.0, []]:
            self.assertRaises(TypeError, t.assert_key_type, k)

    def test_value_size(self):
        t = ILDictionaryTag()

        entries = []
        for e in SAMPLE_DICT:
            entries.append(e)
            t[e[0]] = e[1]
            value_size = pyilint.ilint_size(len(entries))
            for e in entries:
                value_size += ILStringTag.compute_string_tag_size(
                    e[0]) + e[1].tag_size()
            self.assertEqual(value_size, t.value_size())

    def test_deserialize_value(self):

        entries = []
        for e in SAMPLE_DICT:
            entries.append(e)
            reader = io.BytesIO()
            pyilint.ilint_encode_to_stream(len(entries), reader)
            for k in entries:
                ILStringTag.serialize_tag_from_components(k[0], reader)
                k[1].serialize(reader)
            value_size = reader.tell()
            reader.seek(0)
            t = ILDictionaryTag()
            t.deserialize_value(ILStandardTagFactory(), value_size, reader)
            self.assertEqual(value_size, reader.tell())
            for k in entries:
                self.assertILTagEqual(t[k[0]], k[1])

            reader.seek(1)
            self.assertRaises(ILTagCorruptedError, t.deserialize_value,
                              ILStandardTagFactory(), value_size, reader)
            reader.seek(0)
            self.assertRaises(ILTagCorruptedError, t.deserialize_value,
                              ILStandardTagFactory(), value_size - 1,
                              LimitedReaderWrapper(reader, value_size - 1))

        reader = io.BytesIO()
        pyilint.ilint_encode_to_stream(1, reader)
        ILNullTag().serialize(reader)
        ILStringTag().serialize(reader)
        value_size = reader.tell()
        reader.seek(0)
        t = ILDictionaryTag()
        self.assertRaises(ILTagCorruptedError, t.deserialize_value,
                          ILStandardTagFactory(), value_size, reader)

    def test_serialize_value(self):

        entries = []
        for e in SAMPLE_DICT:
            entries.append(e)
            exp = io.BytesIO()
            pyilint.ilint_encode_to_stream(len(entries), exp)
            t = ILDictionaryTag()
            for k in entries:
                ILStringTag.serialize_tag_from_components(k[0], exp)
                k[1].serialize(exp)
                t[k[0]] = k[1]
            writer = io.BytesIO()
            t.serialize_value(writer)
            self.assertEqual(exp.tell(), writer.tell())
            exp.seek(0)
            writer.seek(0)
            self.assertEqual(exp.read(), writer.read())


class TestILStringDictionaryTag(unittest.TestCase):

    def test_constructor(self):
        t = ILStringDictionaryTag()
        self.assertEqual(ILTAG_STRDICT_ID, t.id)
        self.assertEqual(0, len(t))

        t = ILStringDictionaryTag(1234)
        self.assertEqual(1234, t.id)
        self.assertEqual(0, len(t))

    def test_assert_value_type(self):
        t = ILStringDictionaryTag()
        t.assert_value_type('')
        t.assert_value_type('123')
        for k in [1, 1.0, []]:
            self.assertRaises(TypeError, t.assert_value_type, k)

    def test_assert_key_type(self):
        t = ILStringDictionaryTag()
        t.assert_key_type('')
        t.assert_key_type('123')
        for k in [1, 1.0, []]:
            self.assertRaises(TypeError, t.assert_key_type, k)

    def test_value_size(self):
        t = ILStringDictionaryTag()

        entries = []
        for k in STRING_KEY_SAMPLES:
            entries.append(k)
            t[k] = k + '-val'
            value_size = pyilint.ilint_size(len(entries))
            for e in entries:
                value_size += ILStringTag.compute_string_tag_size(
                    e) + ILStringTag.compute_string_tag_size(e + '-val')
            self.assertEqual(value_size, t.value_size())

    def test_deserialize_value(self):

        entries = []
        for k in STRING_KEY_SAMPLES:
            entries.append(k)
            reader = io.BytesIO()
            pyilint.ilint_encode_to_stream(len(entries), reader)
            for e in entries:
                v = e + '-val'
                ILStringTag.serialize_tag_from_components(e, reader)
                ILStringTag.serialize_tag_from_components(v, reader)
            value_size = reader.tell()
            reader.seek(0)
            t = ILStringDictionaryTag()
            t.deserialize_value(ILStandardTagFactory(), value_size, reader)
            self.assertEqual(value_size, reader.tell())
            for e in entries:
                v = e + '-val'
                self.assertEqual(v, t[e])

            reader.seek(1)
            self.assertRaises(ILTagCorruptedError, t.deserialize_value,
                              ILStandardTagFactory(), value_size, reader)
            reader.seek(0)
            self.assertRaises(ILTagCorruptedError, t.deserialize_value,
                              ILStandardTagFactory(), value_size - 1,
                              LimitedReaderWrapper(reader, value_size - 1))

        reader = io.BytesIO()
        pyilint.ilint_encode_to_stream(1, reader)
        ILNullTag().serialize(reader)
        ILStringTag().serialize(reader)
        value_size = reader.tell()
        reader.seek(0)
        t = ILStringDictionaryTag()
        self.assertRaises(ILTagCorruptedError, t.deserialize_value,
                          ILStandardTagFactory(), value_size, reader)

        reader = io.BytesIO()
        pyilint.ilint_encode_to_stream(1, reader)
        ILStringTag('123').serialize(reader)
        ILNullTag().serialize(reader)
        value_size = reader.tell()
        reader.seek(0)
        t = ILStringDictionaryTag()
        self.assertRaises(ILTagCorruptedError, t.deserialize_value,
                          ILStandardTagFactory(), value_size, reader)

    def test_serialize_value(self):

        entries = []
        for k in STRING_KEY_SAMPLES:
            entries.append(k)
            exp = io.BytesIO()
            pyilint.ilint_encode_to_stream(len(entries), exp)
            t = ILStringDictionaryTag()
            for k in entries:
                v = k + '-val'
                t[k] = v
                ILStringTag.serialize_tag_from_components(k, exp)
                ILStringTag.serialize_tag_from_components(v, exp)

            writer = io.BytesIO()
            t.serialize_value(writer)
            self.assertEqual(exp.tell(), writer.tell())
            exp.seek(0)
            writer.seek(0)
            self.assertEqual(exp.read(), writer.read())


class TestILStandardTagFactory(unittest.TestCase, ILTagComparatorMixin):

    def test_implicit_sizes(self):
        self.assertEqual(
            0, ILStandardTagFactory.ILTAG_IMPLICIT_SIZES[ILTAG_NULL_ID])
        self.assertEqual(
            1, ILStandardTagFactory.ILTAG_IMPLICIT_SIZES[ILTAG_BOOL_ID])
        self.assertEqual(
            1, ILStandardTagFactory.ILTAG_IMPLICIT_SIZES[ILTAG_INT8_ID])
        self.assertEqual(
            1, ILStandardTagFactory.ILTAG_IMPLICIT_SIZES[ILTAG_UINT8_ID])
        self.assertEqual(
            2, ILStandardTagFactory.ILTAG_IMPLICIT_SIZES[ILTAG_INT16_ID])
        self.assertEqual(
            2, ILStandardTagFactory.ILTAG_IMPLICIT_SIZES[ILTAG_UINT16_ID])
        self.assertEqual(
            4, ILStandardTagFactory.ILTAG_IMPLICIT_SIZES[ILTAG_INT32_ID])
        self.assertEqual(
            4, ILStandardTagFactory.ILTAG_IMPLICIT_SIZES[ILTAG_UINT32_ID])
        self.assertEqual(
            8, ILStandardTagFactory.ILTAG_IMPLICIT_SIZES[ILTAG_INT64_ID])
        self.assertEqual(
            8, ILStandardTagFactory.ILTAG_IMPLICIT_SIZES[ILTAG_UINT64_ID])
        self.assertEqual(
            9, ILStandardTagFactory.ILTAG_IMPLICIT_SIZES[ILTAG_ILINT64_ID])
        self.assertEqual(
            4, ILStandardTagFactory.ILTAG_IMPLICIT_SIZES[ILTAG_BINARY32_ID])
        self.assertEqual(
            8, ILStandardTagFactory.ILTAG_IMPLICIT_SIZES[ILTAG_BINARY64_ID])
        self.assertEqual(
            16, ILStandardTagFactory.ILTAG_IMPLICIT_SIZES[ILTAG_BINARY128_ID])
        self.assertEqual(
            -1, ILStandardTagFactory.ILTAG_IMPLICIT_SIZES[14])
        self.assertEqual(
            -1, ILStandardTagFactory.ILTAG_IMPLICIT_SIZES[15])

    def test_create(self):
        f = ILStandardTagFactory()
        self.assertIsInstance(f.create(ILTAG_NULL_ID), ILNullTag)
        self.assertIsInstance(f.create(ILTAG_BOOL_ID), ILBoolTag)
        self.assertIsInstance(f.create(ILTAG_INT8_ID), ILInt8Tag)
        self.assertIsInstance(f.create(ILTAG_UINT8_ID), ILUInt8Tag)
        self.assertIsInstance(f.create(ILTAG_INT16_ID), ILInt16Tag)
        self.assertIsInstance(f.create(ILTAG_UINT16_ID), ILUInt16Tag)
        self.assertIsInstance(f.create(ILTAG_INT32_ID), ILInt32Tag)
        self.assertIsInstance(f.create(ILTAG_UINT32_ID), ILUInt32Tag)
        self.assertIsInstance(f.create(ILTAG_INT64_ID), ILInt64Tag)
        self.assertIsInstance(f.create(ILTAG_UINT64_ID), ILUInt64Tag)
        self.assertIsInstance(f.create(ILTAG_ILINT64_ID), ILILInt64Tag)
        self.assertIsInstance(f.create(ILTAG_BINARY32_ID), ILBinary32Tag)
        self.assertIsInstance(f.create(ILTAG_BINARY64_ID), ILBinary64Tag)
        self.assertIsInstance(f.create(ILTAG_BINARY128_ID), ILBinary128Tag)
        self.assertIsNone(f.create(14))
        self.assertIsNone(f.create(15))
        self.assertIsInstance(f.create(ILTAG_BYTE_ARRAY_ID), ILByteArrayTag)
        self.assertIsInstance(f.create(ILTAG_STRING_ID), ILStringTag)
        self.assertIsInstance(f.create(ILTAG_BINT_ID), ILBigIntegerTag)
        self.assertIsInstance(f.create(ILTAG_BDEC_ID), ILBigDecimalTag)
        self.assertIsInstance(f.create(ILTAG_ILINT64_ARRAY_ID), ILIntArrayTag)
        self.assertIsInstance(f.create(ILTAG_ILTAG_ARRAY_ID), ILTagArrayTag)
        self.assertIsInstance(f.create(ILTAG_ILTAG_SEQ_ID), ILTagSequenceTag)
        self.assertIsInstance(f.create(ILTAG_RANGE_ID), ILRangeTag)
        self.assertIsInstance(f.create(ILTAG_VERSION_ID), ILVersionTag)
        self.assertIsInstance(f.create(ILTAG_OID_ID), ILOIDTag)
        self.assertIsNone(f.create(26))
        self.assertIsNone(f.create(27))
        self.assertIsNone(f.create(28))
        self.assertIsNone(f.create(29))
        self.assertIsInstance(f.create(ILTAG_DICT_ID), ILDictionaryTag)
        self.assertIsInstance(f.create(ILTAG_STRDICT_ID),
                              ILStringDictionaryTag)
        self.assertIsNone(f.create(32))

    def test_deserialize(self):
        f = ILStandardTagFactory()
        for tag in BASIC_TAG_SAMPLES:
            reader = io.BytesIO()
            tag.serialize(reader)
            reader.seek(0)
            t = f.deserialize(reader)
            self.assertILTagEqual(tag, t)

    def test_deserialize(self):
        f = ILStandardTagFactory()
        for tag in BASIC_TAG_SAMPLES + [generate_random_tag()] * 10:
            reader = io.BytesIO()
            tag.serialize(reader)
            reader.seek(0)
            t = f.deserialize(reader)
            self.assertILTagEqual(tag, t)

        reader = io.BytesIO(b'\x0E12312312312')
        self.assertRaises(ILTagUnknownError, f.deserialize, reader)
        reader = io.BytesIO(b'\x0F12312312312')
        self.assertRaises(ILTagUnknownError, f.deserialize, reader)

    def test_deserialize_strict(self):
        f = ILStandardTagFactory(True)
        for tag in BASIC_TAG_SAMPLES:
            reader = io.BytesIO()
            tag.serialize(reader)
            reader.seek(0)
            t = f.deserialize(reader)
            self.assertILTagEqual(tag, t)

        reader = io.BytesIO(b'\x0E12312312312')
        self.assertRaises(ILTagUnknownError, f.deserialize, reader)
        reader = io.BytesIO(b'\x0F12312312312')
        self.assertRaises(ILTagUnknownError, f.deserialize, reader)

        reader = io.BytesIO()
        tag = generate_random_tag(33)
        tag.serialize(reader)
        reader.seek(0)
        self.assertRaises(ILTagUnknownError, f.deserialize, reader)

    def test_register_custom(self):
        class Tag1234(ILRawTag):
            def __init__(self, value: bytes = None) -> None:
                super().__init__(1234, value)

        f = ILStandardTagFactory()

        f.register_custom(1234, Tag1234)
        self.assertIsInstance(f.create(1234), Tag1234)

        f.register_custom(12345, lambda: ILInt16Tag(id=12345))
        t = f.create(12345)
        self.assertEqual(12345, t.id)
        self.assertIsInstance(t, ILInt16Tag)

        for id in range(16):
            self.assertRaises(ValueError, f.register_custom,
                              id, lambda: ILInt16Tag(id))

        self.assertRaises(TypeError, f.register_custom,
                          1235, Tag1234)

        self.assertRaises(TypeError, f.register_custom,
                          1235, lambda x: ILInt16Tag(id=1235))

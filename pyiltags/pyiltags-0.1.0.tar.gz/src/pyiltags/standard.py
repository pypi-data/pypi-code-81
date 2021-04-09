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
import pyilint
from typing import Callable, List
from .base import *

# Standard tag IDs
ILTAG_NULL_ID = 0
ILTAG_BOOL_ID = 1
ILTAG_INT8_ID = 2
ILTAG_UINT8_ID = 3
ILTAG_INT16_ID = 4
ILTAG_UINT16_ID = 5
ILTAG_INT32_ID = 6
ILTAG_UINT32_ID = 7
ILTAG_INT64_ID = 8
ILTAG_UINT64_ID = 9
ILTAG_ILINT64_ID = 10
ILTAG_BINARY32_ID = 11
ILTAG_BINARY64_ID = 12
ILTAG_BINARY128_ID = 13
ILTAG_BYTE_ARRAY_ID = 16
ILTAG_STRING_ID = 17
ILTAG_BINT_ID = 18
ILTAG_BDEC_ID = 19
ILTAG_ILINT64_ARRAY_ID = 20
ILTAG_ILTAG_ARRAY_ID = 21
ILTAG_ILTAG_SEQ_ID = 22
ILTAG_RANGE_ID = 23
ILTAG_VERSION_ID = 24
ILTAG_OID_ID = 25
ILTAG_DICT_ID = 30
ILTAG_STRDICT_ID = 31


class ILNullTag(ILFixedSizeTag):
    """
    This class implements the standard tag ILTAG_NULL.
    """

    def __init__(self, id: int = ILTAG_NULL_ID) -> None:
        super().__init__(id, 0, True)

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        if tag_size != 0:
            raise ILTagCorruptedError('Corrupted null tag.')

    def serialize_value(self, writer: io.IOBase) -> None:
        pass


class ILBoolTag(ILFixedSizeTag):
    """
    This class implements the standard tag ILTAG_BOOL.
    """

    def __init__(self, value: bool = False, id: int = ILTAG_BOOL_ID) -> None:
        super().__init__(id, 1, True)
        self.value = value

    @property
    def value(self) -> bool:
        return self._value

    @value.setter
    def value(self, value: any) -> bool:
        """
        Sets the value of this tag. The final value will assume the result
        of `bool(value)`.
        """
        self._value = bool(value)

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        if tag_size < 1:
            raise EOFError('Unable to read the value of the tag.')
        if tag_size > 1:
            raise ILTagCorruptedError('Invalid boolean tag size.')
        v = read_bytes(1, reader)
        if v[0] == 0:
            self.value = False
        elif v[0] == 1:
            self.value = True
        else:
            raise ILTagCorruptedError('Invalid boolean value.')

    def serialize_value(self, writer: io.IOBase) -> None:
        if self.value:
            writer.write(b'\x01')
        else:
            writer.write(b'\x00')


class ILInt8Tag(ILBaseIntTag):
    """
    This class implements the tag ILTAG_INT8_ID.
    """

    def __init__(self, value: int = 0, id: int = ILTAG_INT8_ID) -> None:
        super().__init__(id, 1, True, value, True)


class ILUInt8Tag(ILBaseIntTag):
    """
    This class implements the tag ILTAG_UINT8_ID.
    """

    def __init__(self, value: int = 0, id: int = ILTAG_UINT8_ID) -> None:
        super().__init__(id, 1, False, value, True)


class ILInt16Tag(ILBaseIntTag):
    """
    This class implements the tag ILTAG_INT16_ID.
    """

    def __init__(self, value: int = 0, id: int = ILTAG_INT16_ID) -> None:
        super().__init__(id, 2, True, value, True)


class ILUInt16Tag(ILBaseIntTag):
    """
    This class implements the tag ILTAG_UINT16_ID.
    """

    def __init__(self, value: int = 0, id: int = ILTAG_UINT16_ID) -> None:
        super().__init__(id, 2, False, value, True)


class ILInt32Tag(ILBaseIntTag):
    """
    This class implements the tag ILTAG_INT32_ID.
    """

    def __init__(self, value: int = 0, id: int = ILTAG_INT32_ID) -> None:
        super().__init__(id, 4, True, value, True)


class ILUInt32Tag(ILBaseIntTag):
    """
    This class implements the tag ILTAG_UINT32_ID.
    """

    def __init__(self, value: int = 0, id: int = ILTAG_UINT32_ID) -> None:
        super().__init__(id, 4, False, value, True)


class ILInt64Tag(ILBaseIntTag):
    """
    This class implements the tag ILTAG_INT64_ID.
    """

    def __init__(self, value: int = 0, id: int = ILTAG_INT64_ID) -> None:
        super().__init__(id, 8, True, value, True)


class ILUInt64Tag(ILBaseIntTag):
    """
    This class implements the tag ILTAG_INT64_ID.
    """

    def __init__(self, value: int = 0, id: int = ILTAG_UINT64_ID) -> None:
        super().__init__(id, 8, False, value, True)


class ILILInt64Tag(ILTag):
    """
    This class implements the tag ILTAG_ILINT64_ID.
    """

    def __init__(self, value: int = 0, id: int = ILTAG_ILINT64_ID) -> None:
        super().__init__(id, True)
        self.value = value

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int):
        if not isinstance(value, int):
            raise TypeError('The value must be an integer.')
        assert_int_bounds(value, 8, False)
        self._value = value

    def value_size(self) -> int:
        return pyilint.ilint_size(self.value)

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        """
        This method behaves a little different if the tag is implicit or explicit. In the implicit
        case, the tag_size cannot be discovered without looking into the value itself. Thus, it is
        necessary to set tag_size to any value from 1 to 9. The actual tag_size will be discovered during the
        deserialization. If the tag is explicit, the tag_size must match the actual ILInt size, otherwise the
        deserialization will fail.
        """
        if tag_size < 1 or tag_size > 9:
            raise ILTagCorruptedError('Corrupted ILInt value.')
        try:
            if self.implicit:
                self.__deserialize_value_implicit(
                    tag_factory, tag_size, reader)
            else:
                self.__deserialize_value_explicit(
                    tag_factory, tag_size, reader)
        except ValueError:
            raise ILTagCorruptedError('Invalid ILInt value.')

    def __deserialize_value_implicit(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        header = read_bytes(1, reader)[0]
        size = pyilint.ilint_size_from_header(header)
        if size == 1:
            val = header
        else:
            if size > tag_size:
                raise ValueError()
            val, size = pyilint.ilint_decode_multibyte_core(
                header, size, read_bytes(size - 1, reader))
        self.value = val

    def __deserialize_value_explicit(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        value, size = pyilint.ilint_decode(read_bytes(tag_size, reader))
        if size != tag_size:
            raise ILTagCorruptedError('Invalid ILInt value.')
        self._value = value

    def serialize_value(self, writer: io.IOBase) -> None:
        pyilint.ilint_encode_to_stream(self.value, writer)


class ILBinary32Tag(ILBaseFloatTag):
    """
    This class implements the tag ILTAG_BINARY32_ID.
    """

    def __init__(self, value: float = 0.0, id: int = ILTAG_BINARY32_ID) -> None:
        super().__init__(id, 4, value, True)


class ILBinary64Tag(ILBaseFloatTag):
    """
    This class implements the tag ILTAG_BINARY64_ID.
    """

    def __init__(self, value: float = 0.0, id: int = ILTAG_BINARY64_ID) -> None:
        super().__init__(id, 8, value, True)


class ILBinary128Tag(ILFixedSizeTag):
    """
    This class implements the tag ILTAG_BINARY128_ID. Since Python does not support
    the IEEE 754 standard's binary128, it will be represented by its raw bytes.
    """

    ZERO = b'\x00' * 16

    def __init__(self, value: bytes = None, id: int = ILTAG_BINARY128_ID) -> None:
        super().__init__(id, 16, True)
        self.value = value

    @property
    def value(self) -> bytes:
        return self._value

    @value.setter
    def value(self, value: bytes):
        if value is None:
            self._value = ILBinary128Tag.ZERO
        else:
            if isinstance(value, bytearray):
                v = bytes(value)
            elif isinstance(value, bytes):
                v = value
            else:
                raise TypeError(
                    'The value must be an instance of bytes with 16 positions.')
            if len(v) != 16:
                raise TypeError(
                    'The value must be an instance of bytes with 16 positions.')
            self._value = v

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        if tag_size < 16:
            raise EOFError('Unable to read the value of the tag.')
        if tag_size > 16:
            raise ILTagCorruptedError(
                'Tag too long. Expecting 16 bytes but got {tag_size}.')
        self.value = read_bytes(16, reader)

    def serialize_value(self, writer: io.IOBase) -> None:
        writer.write(self.value)


class ILByteArrayTag(ILRawTag):
    """
    This class implements the tag ILTAG_BYTE_ARRAY_ID.
    """

    def __init__(self, value: bytes = None, id: int = ILTAG_BYTE_ARRAY_ID) -> None:
        super().__init__(id, value)


class ILStringTag(ILTag):
    """
    This class implements the tag ILTAG_STRING_ID. It also include a few helper functions 
    to better manupulate UTF-8 bytes directly.
    """

    def __init__(self, value: str = None, id: int = ILTAG_STRING_ID) -> None:
        """
        Creates a new instance of this class.

        Parameters:
        - `value`: The value of the tag. Must be a string or None. None is equivalent to '';
        - `id`: The id if necessary.
        """
        super().__init__(id)
        self.value = value

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        if value is None or value == '':
            self._value = ''
            self._utf8 = b''
        elif isinstance(value, str):
            self._value = value
            self._utf8 = ILStringTag.to_utf8(value)
        else:
            raise TypeError('The value must be a str.')

    def value_size(self) -> int:
        return len(self.utf8)

    @property
    def utf8(self) -> bytes:
        return self._utf8

    @utf8.setter
    def utf8(self, utf8: bytes):
        if utf8 is None or utf8 == b'':
            self._value = ''
            self._utf8 = b''
        elif isinstance(utf8, bytes):
            self._value = ILStringTag.from_utf8(utf8)
            if isinstance(utf8, bytearray):
                self._utf8 = bytes(utf8)
            else:
                self._utf8 = utf8
        else:
            raise TypeError(
                'The value must be an instance of bytes or bytearray.')

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        if tag_size == 0:
            self.utf8 = None
        else:
            try:
                self.utf8 = read_bytes(tag_size, reader)
            except ValueError:
                raise ILTagCorruptedError('Corrupted utf-8 string.')

    def serialize_value(self, writer: io.IOBase) -> None:
        if self.utf8 is not None:
            writer.write(self.utf8)

    @staticmethod
    def to_utf8(s: str) -> bytes:
        """
        Converts a string into its UTF-8 bytes.
        """
        return s.encode('utf-8')

    @staticmethod
    def from_utf8(utf8: bytes) -> str:
        """
        Converts UTF-8 bytes into a string. It may raise a `ValueError`
        if `utf8` is not a valid UTF-8 string.
        """
        return str(utf8, 'utf-8')

    @staticmethod
    def size_in_utf8(s: str) -> int:
        """
        Computes of the string encoded in UTF-8.
        """
        return len(s.encode('utf-8'))

    @staticmethod
    def compute_string_tag_size(value: str, id: id = ILTAG_STRING_ID) -> int:
        """
        Computes the size of a ILStringTag like tag based on its value.
        """
        return ILTag.compute_tag_size(id, ILStringTag.size_in_utf8(value))

    @staticmethod
    def serialize_tag_from_components(value: str, writer: io.IOBase,
                                      id: id = ILTAG_STRING_ID) -> int:
        """
        Serializes `ILStringTag` like tag without the need to create a new
        instance of ILStringTag. This method was devised as a way to avoid
        unnecessary allocation of `ILStringTags` whenever possible.

        Parameters:
        - `str`: The string to be serialized.
        - `writer`: The writer that will receive the tag.
        - `id`: Alternative tag id if it is not ILTAG_STRING_ID;
        """
        if isinstance(value, str):
            bin_value = ILStringTag.to_utf8(value)
        else:
            bin_value = value
        size = pyilint.ilint_encode_to_stream(id, writer)
        size += pyilint.ilint_encode_to_stream(len(bin_value), writer)
        writer.write(bin_value)
        return size + len(bin_value)

    @staticmethod
    def is_standard_string(tag: ILTag) -> bool:
        """
        Verifies if the given tag is a string.
        """
        return tag.id == ILTAG_STRING_ID and isinstance(tag, ILStringTag)


class ILBigIntegerTag(ILRawTag):
    """
    This class implements the tag ILTAG_BINT_ID.
    """
    DEFAULT_VALUE = b'\x00'

    def __init__(self, value: bytes = None, id: int = ILTAG_BINT_ID) -> None:
        super().__init__(id, value)

    def assert_value_valid(self, value: bytes):
        if len(value) == 0:
            raise ValueError('The value must have at least 1 byte.')


class ILBigDecimalTag(ILBigIntegerTag):
    """
    This class implements the tag ILTAG_BDEC_ID.
    """

    def __init__(self, value: bytes = None, scale: int = 0, id: int = ILTAG_BDEC_ID) -> None:
        super().__init__(value, id)
        self.scale = scale

    @property
    def scale(self) -> int:
        return self._scale

    @scale.setter
    def scale(self, scale: int):
        if not isinstance(scale, int):
            raise TypeError('The scale must be a valid integer.')
        assert_int_bounds(scale, 4, True)
        self._scale = scale

    def value_size(self) -> int:
        return 4 + len(self.value)

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        if tag_size < 5:
            raise ILTagCorruptedError('Corrupted tag value.')
        self.scale = read_int(4, True, reader)
        self.value = read_bytes(tag_size - 4, reader)

    def serialize_value(self, writer: io.IOBase) -> None:
        write_int(self.scale, 4, True, writer)
        writer.write(self.value)


class ILIntArrayTag(ILTag, RestrictListMixin[int]):
    """
    This class implements the tag ILTAG_ILINT64_ARRAY_ID.
    """

    def __init__(self, values: List[int] = None, id: int = ILTAG_ILINT64_ARRAY_ID) -> None:
        super().__init__(id)
        RestrictListMixin.__init__(self)
        if values:
            for v in values:
                self.append(v)

    def assert_value_type(self, value: T):
        if isinstance(value, int):
            assert_int_bounds(value, 8, False)
        else:
            raise TypeError('Only unsigned 64-bit integers are allowed.')

    def value_size(self) -> int:
        size = pyilint.ilint_size(len(self))
        for v in self:
            size += pyilint.ilint_size(v)
        return size

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        if tag_size < 1:
            raise ILTagCorruptedError('Corrupted tag.')
        self.clear()
        count, _ = pyilint.ilint_decode_from_stream(reader)
        for i in range(count):
            v, _ = pyilint.ilint_decode_from_stream(reader)
            self.append(v)

    def serialize_value(self, writer: io.IOBase) -> None:
        pyilint.ilint_encode_to_stream(len(self), writer)
        for v in self:
            pyilint.ilint_encode_to_stream(v, writer)


class ILTagArrayTag(ILTag, RestrictListMixin[ILTag]):
    """
    This class implements the tag ILTAG_ILTAG_ARRAY_ID.
    """

    def __init__(self, values: List[ILTag] = None, id: int = ILTAG_ILTAG_ARRAY_ID) -> None:
        super().__init__(id)
        RestrictListMixin.__init__(self)
        if values:
            for v in values:
                self.append(v)

    def assert_value_type(self, value: T):
        if not isinstance(value, ILTag):
            raise TypeError('Only ILTags are allowed.')

    def value_size(self) -> int:
        size = pyilint.ilint_size(len(self))
        for t in self:
            size += t.tag_size()
        return size

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        if tag_size < 1:
            raise ILTagCorruptedError('Corrupted tag.')
        reader = LimitedReaderWrapper(reader, tag_size)
        self.clear()
        try:
            count, _ = pyilint.ilint_decode_from_stream(reader)
        except ValueError:
            raise ILTagCorruptedError('Corrupted tag.')
        for i in range(count):
            t = tag_factory.deserialize(reader)
            self.append(t)

    def serialize_value(self, writer: io.IOBase) -> None:
        pyilint.ilint_encode_to_stream(len(self), writer)
        for t in self:
            t.serialize(writer)


class ILTagSequenceTag(ILTag, RestrictListMixin[ILTag]):
    """
    This class implements the tag ILTAG_ILTAG_SEQ_ID.
    """

    def __init__(self, values: List[ILTag] = None, id: int = ILTAG_ILTAG_SEQ_ID) -> None:
        super().__init__(id)
        RestrictListMixin.__init__(self)
        if values:
            for v in values:
                self.append(v)

    def assert_value_type(self, value: T):
        if not isinstance(value, ILTag):
            raise TypeError('Only ILTags are allowed.')

    def value_size(self) -> int:
        size = 0
        for t in self:
            size += t.tag_size()
        return size

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        reader = LimitedReaderWrapper(reader, tag_size)
        self.clear()
        while reader.remaining:
            t = tag_factory.deserialize(reader)
            self.append(t)

    def serialize_value(self, writer: io.IOBase) -> None:
        for t in self:
            t.serialize(writer)


class ILRangeTag(ILTag):
    """
    This class implements the tag ILTAG_RANGE_ID.
    """

    def __init__(self, first: int = 0, count: int = 0, id: int = ILTAG_RANGE_ID) -> None:
        super().__init__(id)
        self.first = first
        self.count = count

    @property
    def first(self) -> int:
        return self._first

    @first.setter
    def first(self, value: int):
        if not isinstance(value, int):
            raise TypeError('first must be an integer.')
        assert_int_bounds(value, 8, False)
        self._first = value

    @property
    def count(self) -> int:
        return self._count

    @count.setter
    def count(self, value: int):
        if not isinstance(value, int):
            raise TypeError('count must be an integer.')
        assert_int_bounds(value, 2, False)
        self._count = value

    def value_size(self) -> int:
        return pyilint.ilint_size(self.first) + 2

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        if tag_size < 3:
            raise ILTagCorruptedError('Corrupted range.')
        try:
            first, _ = pyilint.ilint_decode_from_stream(reader)
            count = read_int(2, False, reader)
            self.first = first
            self.count = count
        except ValueError:
            raise ILTagCorruptedError('Corrupted range.')

    def serialize_value(self, writer: io.IOBase) -> None:
        pyilint.ilint_encode_to_stream(self.first, writer)
        write_int(self.count, 2, False, writer)


class ILVersionTag(ILFixedSizeTag):
    """
    This class implements the tag ILTAG_VERSION_ID.
    """

    def __init__(self, major: int = 0, minor: int = 0, revision: int = 0, build: int = 0, id: int = ILTAG_VERSION_ID) -> None:
        super().__init__(id, 16)
        self._values = [0, 0, 0, 0]
        self.major = major
        self.minor = minor
        self.revision = revision
        self.build = build

    def _set_field_core(self, value: int, index: int):
        if not isinstance(value, int):
            raise TypeError('first must be an integer.')
        assert_int_bounds(value, 4, True)
        self._values[index] = value

    @property
    def major(self) -> int:
        return self._values[0]

    @major.setter
    def major(self, value: int):
        self._set_field_core(value, 0)

    @property
    def minor(self) -> int:
        return self._values[1]

    @minor.setter
    def minor(self, value: int):
        self._set_field_core(value, 1)

    @property
    def revision(self) -> int:
        return self._values[2]

    @revision.setter
    def revision(self, value: int):
        self._set_field_core(value, 2)

    @property
    def build(self) -> int:
        return self._values[3]

    @build.setter
    def build(self, value: int):
        self._set_field_core(value, 3)

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        if tag_size != 16:
            raise ILTagCorruptedError('Corrupted range.')
        for i in range(4):
            self._values[i] = read_int(4, True, reader)

    def serialize_value(self, writer: io.IOBase) -> None:
        for i in range(4):
            write_int(self._values[i], 4, True, writer)


class ILOIDTag(ILIntArrayTag):
    """
    This class implements the tag ILTAG_OID_ID.
    """

    def __init__(self, values: List[int] = None) -> None:
        super().__init__(values, ILTAG_OID_ID)


class ILDictionaryTag(ILTag, RestrictDictMixin[str, ILTag]):
    """
    This class implements the tag ILTAG_DICT_ID. Instances of this 
    class implements a dictionary interface that accepts strings as
    keys and ILTags as values. It also preserves the order of insertion.
    """

    def __init__(self, id: int = ILTAG_DICT_ID) -> None:
        super().__init__(id)
        RestrictDictMixin.__init__(self)

    def assert_value_type(self, value: T):
        if not isinstance(value, ILTag):
            raise TypeError('The value must an ILTag.')

    def assert_key_type(self, key: T):
        if not isinstance(key, str):
            raise TypeError('The key must be a string.')

    def value_size(self) -> int:
        size = pyilint.ilint_size(len(self))
        for key in self:
            size += (ILStringTag.compute_string_tag_size(
                key) + self[key].tag_size())
        return size

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        if tag_size < 1:
            raise ILTagCorruptedError('Corrupted tag.')
        count, _ = pyilint.ilint_decode_from_stream(reader)
        self.clear()
        for i in range(count):
            key = tag_factory.deserialize(reader)
            if not ILStringTag.is_standard_string(key):
                raise ILTagCorruptedError(
                    'Corrupted tag. One of the keys is not a string.')
            value = tag_factory.deserialize(reader)
            self[key.value] = value

    def serialize_value(self, writer: io.IOBase) -> None:
        pyilint.ilint_encode_to_stream(len(self), writer)
        for key in self:
            ILStringTag.serialize_tag_from_components(key, writer)
            self[key].serialize(writer)


class ILStringDictionaryTag(ILTag, RestrictDictMixin[str, str]):
    """
    This class implements the tag ILTAG_STRDICT_ID. Instances of this 
    class implements a dictionary interface that accepts strings as
    keys and ILTags as values. It also preserves the order of insertion.
    """

    def __init__(self, id: int = ILTAG_STRDICT_ID) -> None:
        super().__init__(id)
        RestrictDictMixin.__init__(self)

    def assert_value_type(self, value: T):
        if not isinstance(value, str):
            raise TypeError('The value must be a string.')

    def assert_key_type(self, key: T):
        if not isinstance(key, str):
            raise TypeError('The key must be a string.')

    def value_size(self) -> int:
        size = pyilint.ilint_size(len(self))
        for key in self:
            size += (ILStringTag.compute_string_tag_size(key) +
                     ILStringTag.compute_string_tag_size(self[key]))
        return size

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        if tag_size < 1:
            raise ILTagCorruptedError('Corrupted tag.')
        count, _ = pyilint.ilint_decode_from_stream(reader)
        self.clear()
        for i in range(count):
            key = tag_factory.deserialize(reader)
            if not ILStringTag.is_standard_string(key):
                raise ILTagCorruptedError(
                    'Corrupted tag. One of the keys is not a string.')
            value = tag_factory.deserialize(reader)
            if not ILStringTag.is_standard_string(value):
                raise ILTagCorruptedError(
                    'Corrupted tag. One of the keys is not a string.')
            self[key.value] = value.value

    def serialize_value(self, writer: io.IOBase) -> None:
        pyilint.ilint_encode_to_stream(len(self), writer)
        for key in self:
            ILStringTag.serialize_tag_from_components(key, writer)
            ILStringTag.serialize_tag_from_components(self[key], writer)


class ILStandardTagFactory(ILTagFactory):
    ILTAG_IMPLICIT_SIZES = [
        0,  # TAG_NULL
        1,  # TAG_BOOL
        1,  # TAG_INT8
        1,  # TAG_UINT8
        2,  # TAG_INT16
        2,  # TAG_UINT16
        4,  # TAG_INT32
        4,  # TAG_UINT32
        8,  # TAG_INT64
        8,  # TAG_UINT64
        9,  # TAG_ILINT64 (maximum size possible).
        4,  # TAG_BINARY32
        8,  # TAG_BINARY64
        16,  # TAG_BINARY128
        -1,  # Reserved
        -1  # Reserved
    ]

    _CLASS_MAP = {
        ILTAG_NULL_ID: ILNullTag,
        ILTAG_BOOL_ID: ILBoolTag,
        ILTAG_INT8_ID: ILInt8Tag,
        ILTAG_UINT8_ID: ILUInt8Tag,
        ILTAG_INT16_ID: ILInt16Tag,
        ILTAG_UINT16_ID: ILUInt16Tag,
        ILTAG_INT32_ID: ILInt32Tag,
        ILTAG_UINT32_ID: ILUInt32Tag,
        ILTAG_INT64_ID: ILInt64Tag,
        ILTAG_UINT64_ID: ILUInt64Tag,
        ILTAG_ILINT64_ID: ILILInt64Tag,
        ILTAG_BINARY32_ID: ILBinary32Tag,
        ILTAG_BINARY64_ID: ILBinary64Tag,
        ILTAG_BINARY128_ID: ILBinary128Tag,
        ILTAG_BYTE_ARRAY_ID: ILByteArrayTag,
        ILTAG_STRING_ID: ILStringTag,
        ILTAG_BINT_ID: ILBigIntegerTag,
        ILTAG_BDEC_ID: ILBigDecimalTag,
        ILTAG_ILINT64_ARRAY_ID: ILIntArrayTag,
        ILTAG_ILTAG_ARRAY_ID: ILTagArrayTag,
        ILTAG_ILTAG_SEQ_ID: ILTagSequenceTag,
        ILTAG_RANGE_ID: ILRangeTag,
        ILTAG_VERSION_ID: ILVersionTag,
        ILTAG_OID_ID: ILOIDTag,
        ILTAG_DICT_ID: ILDictionaryTag,
        ILTAG_STRDICT_ID: ILStringDictionaryTag
    }

    def __init__(self, strict: bool = False) -> None:
        super().__init__(strict)
        self._class_map = ILStandardTagFactory._CLASS_MAP.copy()

    def create(self, id: int) -> 'ILTag':
        if id in self._class_map:
            return self._class_map[id]()
        else:
            return None

    def deserialize(self, reader: io.IOBase) -> 'ILTag':
        tag_offset = reader.tell()
        try:
            tag_id, _ = pyilint.ilint_decode_from_stream(reader)
            tag = self.create(tag_id)
            if tag is None:
                if self.strict or iltags_is_implicit(tag_id):
                    raise ILTagUnknownError(
                        f'Unknown tag with id {id} at {tag_offset}.')
                else:
                    tag = ILRawTag(tag_id)

            if iltags_is_implicit(tag_id):
                tag_size = ILStandardTagFactory.ILTAG_IMPLICIT_SIZES[tag_id]
            else:
                tag_size, _ = pyilint.ilint_decode_from_stream(reader)

            if tag_id == ILTAG_ILINT64_ID:
                tag.deserialize_value(self, tag_size, reader)
            else:
                value_reader = io.BytesIO(read_bytes(tag_size, reader))
                tag.deserialize_value(self, tag_size, value_reader)
                left_behind = tag_size - value_reader.tell()
                if left_behind != 0:
                    raise ILTagCorruptedError(
                        f'The tag at {tag_offset} with id {tag_id} and size {tag_size} could not be deserialized by the class {tag.__class__}. {left_behind} bytes were not used.')
            return tag
        except (ValueError, EOFError):
            raise ILTagCorruptedError(
                f'Corrupted tag at {tag_offset}.')

    def register_custom(self, id: int, tag_type):
        """
        Register a custom class to parse a given tag id. This method is not thread safe.

        Parameters:
        - `id`: The tag id. It cannot be an id for an implicit tag;
        - `tag_type`: A function or a class with no parameters that is used to create an empty instance of the tag.
        """
        if iltags_is_implicit(id):
            raise ValueError(
                'It is not possible to register a custom implicit tag.')
        else:
            try:
                t = tag_type()
            except TypeError:
                raise TypeError(
                    'The function or constructor must work without any parameters.')
            if isinstance(t, ILTag):
                if t.id != id:
                    raise TypeError(
                        'The function or constructor must return an instance of ILTag.')
                self._class_map[id] = tag_type
            else:
                raise TypeError(
                    'The function or constructor must return an instance of ILTag.')

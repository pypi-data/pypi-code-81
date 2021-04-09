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
from typing import ForwardRef
import sys
import io
import pyilint
from .io import *
from .util import *


class ILTagError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ILTagStateError(ILTagError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ILTagCorruptedError(ILTagError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ILTagUnknownError(ILTagError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def iltags_assert_valid_id(id: int) -> None:
    """
    Asserts that the id is a valid ILTag id. Raises
    `ValueError` if the id is invalid.
    """
    assert_int_bounds(id, 8, False)


def iltags_is_implicit(id: int) -> bool:
    """
    Verifies if the given tag id represents an implicity tag.

    Parameters:
    - `id`: The tag id to be tested.
    """
    iltags_assert_valid_id(id)
    return id < 16


def iltags_is_standard(id: int) -> bool:
    """
    Verifies if the given tag id represents a standard tag.

    Parameters:
    - `id`: The tag id to be tested.
    """
    iltags_assert_valid_id(id)
    return id < 32


class ILTagFactory:
    """
    This abstract class implements a factory of tags. It is used to serialize classes.

    Instances of `ILTagFactory` are expected to be reused by one or multiple threads
    at once.
    """

    def __init__(self, strict: bool = False) -> None:
        """
        Creates a new instance of this class.
        """
        self.strict = strict

    def create(self, id: int) -> 'ILTag':
        """
        Creates the appropriate instance of the tags. Returns None if the class
        is unknown. This method is thread safe.

        This method must be overriden by subclasses.
        """
        raise NotImplementedError('Subclasses must override this method.')

    def deserialize(self, reader: io.IOBase) -> 'ILTag':
        """
        Deserializes a tag from the reader. This method is thread safe.

        This method must be overriden by subclasses.
        """
        raise NotImplementedError('Subclasses must override this method.')


class ILTag:
    def __init__(self, id: int, allow_implicit=False) -> None:
        """
        Creates a new instance of this class.

        Parameters:
        - `id`: The tag id;
        - `allow_implicit`: If True, allows the id to refer to an implicit tag.
        """
        iltags_assert_valid_id(id)
        self._id = id
        if not allow_implicit and self.implicit:
            raise ValueError('Implicit tag is not allowed.')

    @property
    def id(self) -> int:
        """
        Returns the id of the tag.
        """
        return self._id

    @property
    def implicit(self) -> bool:
        """
        Returns True if this tag is implicit.
        """
        return iltags_is_implicit(self.id)

    @property
    def standard(self) -> bool:
        """
        Returns True if this tag is one of the standard tags.
        """
        return iltags_is_standard(self.id)

    def value_size(self) -> int:
        """
        Returns the size of the payload in bytes. It must be overridden by subclasses.
        """
        raise NotImplementedError('Subclasses must override this method.')

    def tag_size(self) -> int:
        """
        Returns the size of the tag in bytes.
        """
        return ILTag.compute_tag_size(self.id, self.value_size())

    @staticmethod
    def compute_tag_size(id: int, value_size: int) -> int:
        """
        Computes the tag size based on the id and the value size.

        Parameters:
        - `id`: The tag id;
        - `value_size`: The value size;
        """
        size = pyilint.ilint_size(id) + value_size
        if not iltags_is_implicit(id):
            size += pyilint.ilint_size(value_size)
        return size

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        """
        Deserializes the value of this class.

        Parameters:
        - `tag_factory`: The current tag factory;
        - `tag_size`: The size of the payload;
        - `reader`: The reader;
        """
        raise NotImplementedError('Subclasses must override this method.')

    def serialize_value(self, writer: io.IOBase) -> None:
        """
        Serializes the value of this tag. It must be overridden by subclasses.

        Parameters:
        - `writer`: The writer;
        """
        raise NotImplementedError('Subclasses must override this method.')

    def serialize(self, writer: io.IOBase) -> None:
        """
        Serializes this tag.

        Parameters:
        - `writer`: The writer;
        """
        pyilint.ilint_encode_to_stream(self.id, writer)
        if not self.implicit:
            pyilint.ilint_encode_to_stream(self.value_size(), writer)
        self.serialize_value(writer)


class ILRawTag(ILTag):
    """
    This class implements a raw `ILTag`. It can be used as an opaque
    implementation for any explicit tag.
    """
    DEFAULT_VALUE = None

    def __init__(self, id: int, value: bytes = None) -> None:
        """
        Creates a new instance of this tag.

        Parameters:
        - `id`: The tag id. It must be an explicit tag ID;
        - `value`: The value of the tag as bytes. None is equivalent to `self.default_value`.
        """
        super().__init__(id, False)
        self.value = value

    @property
    def default_value(self) -> bytes:
        """
        Returns the default value to be used when setting `value` to None.

        To change the behavior of this property, set the class attribute `DEFAULT_VALUE` to
        the specified value. It must be an instance of bytes.
        """
        return self.__class__.DEFAULT_VALUE

    def assert_value_valid(self, value: bytes):
        """
        This method is called before setting the value. It must raise ValueError if the
        value is not acceptable somehow. This method does nothing by default and may
        be overriden to ensure a distinct behavior. 
        """
        pass

    @property
    def value(self) -> bytes:
        return self._value

    @value.setter
    def value(self, value: bytes):
        if value is None:
            self._value = self.default_value
        else:
            if isinstance(value, bytearray):
                v = bytes(value)
            elif isinstance(value, bytes):
                v = value
            else:
                raise TypeError('The payload must bytes or bytearray.')
            self.assert_value_valid(v)
            self._value = v

    def value_size(self) -> int:
        if self.value is not None:
            return len(self.value)
        else:
            return 0

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        self.value = read_bytes(tag_size, reader)

    def serialize_value(self, writer: io.IOBase) -> None:
        if self.value is not None:
            writer.write(self.value)


class ILFixedSizeTag(ILTag):
    """
    This is is a special subclass of **ILTag** that helps the implementation
    of tags with fixed size payloads.
    """

    def __init__(self, id: int, value_size: int, allow_implicit=False) -> None:
        """
        Creates a new instance of this class.

        Parameters:
        - `id`: The tag id;
        - `value_size`: The size of the value in bytes. It cannot exceed
          2**64 - 1;
        """
        super().__init__(id, allow_implicit)
        assert_int_bounds(value_size, 8, False)
        self._value_size = value_size

    def value_size(self) -> int:
        return self._value_size


class ILBaseIntTag(ILFixedSizeTag):
    """
    This is the base class for all big integer tags.
    """

    def __init__(self, id: int, value_size: int, signed: bool, value=0, allow_implicit=False) -> None:
        """
        Creates new instance of this class.

        Parameters:
        - `id`: The tag id;
        - `value_size`: The size of the value in bytes. It can be 1, 2, 4 or 8;
        - `signed`: Flag that indicates if the integer is signed or not;
        - `value`: The actual integer value. Its boundaries are checked based on the
          specified sizes;
        """
        super().__init__(id, value_size, allow_implicit)
        if value_size not in [1, 2, 4, 8]:
            raise ValueError('value_size must be 1, 2, 4 or 8.')
        self.signed = signed
        #assert_int_bounds(value, value_size, signed)
        #self._value = value
        self.value = value

    @property
    def value(self) -> int:
        """
        Returns the integer value.
        """
        return self._value

    @value.setter
    def value(self, value: int):
        """
        Sets the integer value. It may raise a `ValueError` if the
        value is outside of the range of the integer defined in the constructor.
        """
        if not isinstance(value, int):
            raise TypeError('value must be a int.')
        assert_int_bounds(value, self.value_size(), self.signed)
        self._value = value

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        if self.value_size() > tag_size:
            raise EOFError(
                f'At least {self.tag_size()} are required to deserialize this tag.')
        self.value = read_int(self.value_size(), self.signed, reader)

    def serialize_value(self, writer: io.IOBase) -> None:
        write_int(self.value, self.value_size(), self.signed, writer)


class ILBaseFloatTag(ILFixedSizeTag):
    """
    This class implements the base class for floating point tags with 32 and 64 bits.
    """

    def __init__(self, id: int, value_size: int, value: float = 0.0, allow_implicit=False) -> None:
        """
        Creates new instance of this class.

        Parameters:
        - `id`: The tag id;
        - `value_size`: The size of the value in bytes. It can be 4 or 8;
        - `value`: The actual float value;
        """
        super().__init__(id, value_size, allow_implicit)
        if value_size not in [4, 8]:
            raise ValueError('value_size must be 4 or 8.')
        self.value = value

    @property
    def value(self) -> float:
        """
        Returns the value of the tag.
        """
        return self._value

    @value.setter
    def value(self, value: float) -> None:
        """
        Sets the value of the tag.
        """
        if isinstance(value, int):
            value = float(value)
        elif not isinstance(value, float):
            raise TypeError('value must be a float or an integer.')
        self._value = value

    def deserialize_value(self, tag_factory: ILTagFactory, tag_size: int, reader: io.IOBase) -> None:
        if self.value_size() > tag_size:
            raise EOFError(
                f'At least {self.tag_size()} are required to deserialize this tag.')
        if self.value_size() == 4:
            self.value = read_binary32(reader)
        else:
            self.value = read_binary64(reader)

    def serialize_value(self, writer: io.IOBase) -> None:
        if self.value_size() == 4:
            write_binary32(self.value, writer)
        else:
            write_binary64(self.value, writer)

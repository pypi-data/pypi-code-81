# -*- coding: utf-8 -*-
"""
============================
Binary manipulation classes
============================

Provides classes that assist in managing, comparing, transforming and working
with binary data in general.

-----------------
Provided Classes
-----------------

Bit
===
The Bit is the smallest representation of binary data and represents True or
False. This class provides methods to perform binary comparisons and
conversions between different types that can be used to represent a single
binary value.

Bits
====
A Byte is the representation of 8 Bits. The Byte class provides methods to
compare a single binary Byte to other data types. The Class also provides
binary math functions and allows getting and setting the state of individual
Bits.

Bytes
=====
The Bytes class allows an arbitrary amount of binary data to be represented.
The Bytes class provides access to each byte using the Byte class, which
further allows all the methods to be used on the binary data provided by the
Byte and Bit classes. Bytes can be compared and converted between several
different data types.

"""

class Bit:
    """
    ====
    Bit
    ====

    A single binary bit representation of True or False

    A Bit object can be compared and converted to int, str, bool and other Bit
    objects. The Bit class is backed by a single bool variable. This backing
    bool object is converted as necessary to provide conversions and
    comparisons with other data types. Keep this in mind as converting an
    object to Bit and then attempting to convert back to the original object
    may not yield the exact same value.

    In the case of comparisons, the object being compared is cast as a Bit
    object, and the two Bit objects are then compared with each other and the
    result of the comparison is returned.

    ----------------
    Type Conversion
    ----------------
    The objects that can be converted to and from a Bit include *bool*, *int*,
    *str* and other *Bit* objects.

    Convert *bool* to *Bit*:
    .. code-block:: python

       />/>/> a_bit = Bit(True)
       />/>/> a_bit
       Bit(1)
       />/>/>

    Convert *Bit* to *bool*:
    .. code-block:: python

       />/>/> a_bool = bool(Bit(True))
       />/>/> a_bool
       True
       />/>/> type(a_bool)
       <class 'bool'>
       />/>/>

    Convert *int* to *Bit*:
    .. code-block:: python

       />/>/> unset_bit = Bit(0)
       />/>/> unset_bit
       Bit(0)
       />/>/> set_bit = Bit(1)
       />/>/> set_bit
       Bit(1)
       />/>/>

    Convert *Bit* to *int*:
    .. code-block:: python

       />/>/> my_int = int(Bit(1))
       />/>/> my_int
       1
       />/>/> type(my_int)
       <class 'int'>
       />/>/>

    .. note:: The only values allowed for *int* are **0** and **1**

    Convert *str* to *Bit*:
    .. code-block:: python

       />/>/> unset_bit = Bit("0")
       />/>/> unset_bit
       Bit(0)
       />/>/> set_bit = Bit("1")
       />/>/> set_bit
       Bit(1)
       />/>/>

    Convert *Bit* to *str*:
    .. code-block: python

       />/>/> my_str = str(Bit(False))
       />/>/> my_str
       '0'
       />/>/> type(my_str)
       <class 'str'>
       />/>/>

    .. note:: The only *str* characters allowed are a single **0** or **1**


    ------------
    Comparisons
    ------------
    A Bit object can be compared to any object which can be cast to a Bit

    .. code-block: python

       />/>/> 0 == Bit(False) == Bit("0") == Bit(0) == False
       True
       />/>/>

    .. note:: Comparing an object with a value that cannot be cast to Bit will
              return a ValueError.

    -----------------
    Rich Comparisons
    -----------------
    Bit objects also support "rich comparisons". For example:

    .. code-block: python

       />/>/> Bit(False) < 1
       True
       />/>/> Bit(True) <= 1
       True
       />/>/> Bit(False) <= "1"
       True
       />/>/> Bit(False) != True
       True
       />/>/> Bit(True) >= False
       False
       />/>/>


    --------
    Methods
    --------
    The action method `toggle` is provided for convenience.

    .. code-block: python

       />/>/> Bit(False).toggle()
       Bit(1)
       />/>/> Bit(True).toggle() == False
       True
       />/>/> int(Bit(False).toggle())
       1
       />/>/>

    The `set` and `unset` methods are also provided to explicitely set the
    value of Bit.

    .. code-block: python

       />/>/> a_bit = Bit(0)
       />/>/> a_bit
       Bit(0)
       />/>/> a_bit.set()
       />/>/> a_bit
       Bit(1)
       />/>/> a_bit.unset()
       />/>/> a_bit
       Bit(0)
       />/>/>


    -----------
    Properties
    -----------
    The `lie` property returns the opposite value of Bit as a *bool*. Unlike
    the `toggle` method, `lie` does not change the value of the Bit.

    .. code-block: python

       />/>/> Bit(1).lie
       False
       />/>/>

    """


    def __init__(self, var):
        """
        var: Any supported type
        Supported types: (bool, int, str, Bit)
                         bool: True or False
                         int: 0 = False, 1 = True
                         str: "0" = False, "1" = True
                         Bit: Bit = Bit
        """
        if not isinstance(var, (bool, int, str, Bit)):
            raise TypeError("Bit must be one of type (int, bool, str)")
        if isinstance(var, (int, Bit)):
            if var < 0 or var > 1:
                raise ValueError("Bit must be 0 or 1")
            self.__bit = bool(var)
        elif isinstance(var, str):
            if var == "0" or var == "1":
                self.__bit = bool(int(var))
            else:
                raise ValueError('Bit must be "0" or "1"')
        elif isinstance(var, bool):
            self.__bit = var

    def __str__(self):
        """Return '0' or '1'"""
        return str(int(self.__bit))

    def __int__(self):
        """Return 0 or 1"""
        return int(self.__bit)

    def __bool__(self):
        """Returns True or False"""
        return self.__bit

    def __repr__(self):
        return f'{self.__class__.__name__}({int(self.__bit)})'

    def __eq__(self, compare):
        """compare (self) to any supported object"""
        return bool(self) == bool(Bit(compare))

    def __ne__(self, compare):
        return bool(self) != bool(Bit(compare))

    def __lt__(self, compare):
        return bool(self) < bool(Bit(compare))

    def __le__(self, compare):
        return bool(self) <= bool(Bit(compare))

    def __gt__(self, compare):
        return bool(self) > bool(Bit(compare))

    def __ge__(self, compare):
        return bool(self) >= bool(Bit(compare))

    def __get__(self, instance, owner):
        return self.__bit

    def __hash__(self):
        """Not very useful, but provided nonetheless"""
        return hash(self.__bit)

    def toggle(self):
        """Change the state of (self) to Not (self)"""
        self.__bit = not self.__bit

    def set(self):
        """Set Bit to True"""
        self.__bit = True

    def unset(self):
        """Set Bit to False"""
        self.__bit = False

    @property
    def lie(self):
        """Return the opposite of bit, without changing the state of (self)"""
        return not self.__bit


class Bits:
    """
    =====
    Bits
    =====

    A single byte of data with helper methods and properties.

    A Bits object provides many helpful methods for working with a byte of
    information. The backing object is a single int, from which all operations
    and conversions are performed. A Bits object can be converted and compared
    to *bytes*, *int*, *str*, *list(of Bit)*, *bool* and other *Bits* objects.
    The custom object *Bytes* can also be cast to a Bits object, as long as the
    *Bytes* object has an *int* value >= **0** and <= **255**.

    When comparing or operating on *Bits* objects with objects of a different
    type, the *operand* object will first be cast to a Bits object. In this
    way, any object which can be used to create a *Bits* object can also be
    used to perform operations with *Bits*.

    ----------------
    Type Conversion
    ----------------
    The objects that can be converted to and from *Bits* include *bytes*,
    *int*, *str*, *list*, *bool* and other *Bits* objects. When using a list,
    the length of the list must be 8 or less, each list item must be castable
    to *int*, and each item will be evaluated as either *True* or *False*.

    Convert *bool* to *Bits*:
    .. code-block: python

       />/>/> my_bits = Bits(True)
       />/>/> my_bits
       Bits(1)
       />/>/>

    Convert *bytes* to *Bits*:
    .. code-block: python

       />/>/> my_bits = Bits(b'\\xab')
       />/>/> my_bits
       Bits(171)
       />/>/> my_bits = Bits(bytes([210]))
       />/>/> my_bits
       Bits(210)
       />/>/>

    Convert *int* to *Bits*:
    .. code-block: python

       />/>/> my_bits = Bits(234)
       />/>/> my_bits
       Bits(234)
       />/>/>

    Convert *str* to *Bits*:
    .. code-block: python

       />/>/> my_bits = Bits("01010101")
       />/>/> my_bits
       Bits(85)
       />/>/> my_bits = Bits("11")
       />/>/> my_bits
       Bits(3)
       />/>/>

    Convert *list* to *Bits*:
    .. code-block: python

       />/>/> my_bits = Bits(["0", "1", "0", "1", "0", "1", "0", "1"])
       />/>/> my_bits
       Bits(85)
       />/>/> my_bits = Bits([0, 1, 0, 1, 0, 1, 0, 1])
       />/>/> my_bits
       Bits(85)
       />/>/> my_bits = Bits([False, True, False, True, False, True])
       />/>/> my_bits
       Bits(21)
       />/>/> my_bits = Bits([True, True])
       />/>/> my_bits
       Bits(3)
       />/>/> my_bits = Bits([0, "1", False, True, "0", Bit(1), Bit(0), 127])
       />/>/> my_bits
       Bits(85)

    .. note:: Each item in a list will be evaluated to either True or False.


    -------------
    Type Casting
    -------------
    Bits objects support casting to multiple different types.
    .. code-block: python

       />/>/> my_bits = Bits(16)
       />/>/> str(my_bits)
       '00010000'
       />/>/> int(my_bits)
       16
       />/>/> bin(my_bits)
       '0b10000'
       />/>/> bool(my_bits)
       True
       />/>/> list(my_bits)
       [Bit(0), Bit(0), Bit(0), Bit(1), Bit(0), Bit(0), Bit(0), Bit(0)]
       />/>/> bytes(my_bits)
       b'\x10'
       />/>/> bytearray([my_bits])
       bytearray(b'\x10')
       />/>/>


    -------------
    Subscripting
    -------------
    Subscripting can be used to query or modify each Bit.
    .. code-block: python

       />/>/> my_bits = Bits('01101110')
       />/>/> my_bits[3]
       Bit(0)
       />/>/> my_bits[3] = True
       />/>/> my_bits[3]
       Bit(1)
       />/>/> str(my_bits)
       '01111110')
       />/>/> list(my_bits)
       [Bit(0), Bit(1), Bit(1), Bit(1), Bit(1), Bit(1), Bit(1), Bit(0)]
       />/>/>


    ------------
    Comparisons
    ------------
    Bits objects can be compared to any object which can be cast to a Bits
    object. This goes both ways.
    .. code-block: python

       />/>/> my_bits = Bits('01101110')
       />/>/> my_bits
       Bits(110)
       />/>/> 110 == my_bits
       True
       />/>/> 111 == my_bits
       False
       />/>/> 111 > my_bits
       True
       />/>/> my_bits > 112
       False
       />/>/> b'n' == my_bits
       True
       />/>/> my_bits >= b'#'
       True
       />/>/> my_bits >= '10000000'
       False
       />/>/> '10000000' >= my_bits
       True
       />/>/>


    --------------------
    Bit-Masks and Flags
    --------------------
    Bits objects support bitmask and flag operations.
    .. code-block: python

       />/>/> my_bits = Bits('01101110')
       />/>/> my_bits
       Bits(110)
       />/>/> 110 in my_bits
       True
       />/>/> Bits('00000010') in my_bits
       True
       />/>/> pow_2 = [0, 1, 2, 4, 8, 16, 32, 64, 128]
       />/>/> for p2 in pow_2:
       ...   print(str(Bits(p2)))
       ...
       00000000
       00000001
       00000010
       00000100
       00001000
       00010000
       00100000
       01000000
       10000000
       />/>/> for p2 in pow_2:
       ...   print(str(p2) + ' in Bits(110): ' + p2 in my_bits)
       ...
       0 in Bits(110): True
       1 in Bits(110): False
       2 in Bits(110): True
       4 in Bits(110): True
       8 in Bits(110): True
       16 in Bits(110): False
       32 in Bits(110): True
       64 in Bits(110): True
       128 in Bits(110): False
       />/>/> str(Bits(14))
       '00001110'
       />/>/> 14 in my_bits
       True
       />/>/> (0 + 2 + 4 + 8) in my_bits
       True
       />/>/>


    -------------------
    Bitwise operations
    -------------------
    Binary bitwise operations are supported.
    .. code-block: python

       />/>/> my_bits = Bits('01101110')
       />/>/> my_bits
       Bits(110)
       />/>/> str(my_bits & '0011')
       '00000010'
       />/>/> str(my_bits >> 3)
       '00001101'
       />/>/> str(my_bits << 1)
       '11011100'
       />/>/> str(my_bits|'10111110')
       '11111110'
       />/>/> str(my_bits^'10101010')
       '11000100'
       />/>/> str(~my_bits)
       '10010001'
       />/>/>

    """

    def __init__(self, var=0, msb_last=False):
        """
        var: any supported variant type that can be interpreted as Bits object
        msb_last: True to swap bit order for indexing and slicing. Equivalent
                  to Bits(Bits(var).stib)
        """
        self.__value = 0
        self.__r_to_l = bool(msb_last)
        self.__setvalue(var)

    def __bytes__(self):
        """
        Get copy(self) as binary object
        """
        return bytes([self.__value])

    def __bool__(self):
        """
        False if self = Bit(0), otherwise True if self > 0
        Use indexing to get value of specific bit, e.g. self[1] will return
        Bit(1) if self = "01000000" (left to right)
        Use self.stib[1] to get bit 6 in Bit("00000010")
        """
        return bool(int(self))

    def __int__(self):
        """
        Get integer value of self
        """
        return self.__value

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__value!r})'

    def __str__(self):
        """
        Get binary string representation of self
        """
        return self.bin()

    def __ord__(self):
        return int(self)

    def __index__(self):
        return int(self)

    def __len__(self):
        return 8

    def __eq__(self, compare):
        return int(self) == int(Bits(compare))

    def __ne__(self, compare):
        return int(self) != int(Bits(compare))

    def __lt__(self, compare):
        return int(self) < int(Bits(compare))

    def __le__(self, compare):
        return int(self) <= int(Bits(compare))

    def __gt__(self, compare):
        return int(self) > int(Bits(compare))

    def __ge__(self, compare):
        return int(self) >= int(Bits(compare))

    def __getitem__(self, index):
        """
        Get Bit at index from self
        """
        return self.list()[index]

    def __setitem__(self, index, value):
        """
        Change value of self by setting or resetting a single Bit
        index: The bit to change
        value: True or False to set or reset target bit
        Index should be an int from 0 to 7
        Value is any supported Bit-class compatible object
        """
        # we'll take the easy way for now
        l = self.list()
        # str->int->bool->int : accept bool, str, int, return either "0" or "1"
        l[index] = Bit(value)
        self.__setvalue(l)

    def __get__(self, instance, owner):
        return self.bin()

    def __add__(self, other):
        return Bits(int(self) + int(Bits(other)))

    def __sub__(self, other):
        return Bits(int(self) - int(Bits(other)))

    def __mul__(self, other):
        return Bits(int(self) * int(Bits(other)))

    def __matmul__(self, other):
        return NotImplemented

    def __truediv__(self, other):
        return NotImplemented

    def __floordiv__(self, other):
        return Bits(int(self) // int(Bits(other)))

    def __mod__(self, other):
        return Bits(int(self) % int(Bits(other)))

    def __divmod__(self, other):
        return (self // Bits(other), self % Bits(other))

    def __pow__(self, other, mod=None):
        ret = Bits(0)
        if mod is None:
            ret = Bits(int(self) ** int(Bits(other)))
        else:
            ret = Bits(int(self) ** int(Bits(other)) % int(Bits(mod)))
        return ret

    def __lshift__(self, other):
        return Bits(int(self) << int(Bits(other)))

    def __rshift__(self, other):
        return Bits(int(self) >> int(Bits(other)))

    def __and__(self, other):
        return Bits(int(self) & int(Bits(other)))

    def __xor__(self, other):
        return Bits(int(self) ^ int(Bits(other)))

    def __or__(self, other):
        return Bits(int(self) | int(Bits(other)))

    def __invert__(self):
        # There's probably a better way to do this...
        inv = str(self).replace('0', 'x').replace('1', '0').replace('x', '1')
        return Bits(inv)

    def __neg__(self):
        return ~ self

    def __radd__(self, other):
        return Bits(other) + self

    def __rsub__(self, other):
        return Bits(other) - self

    def __rmul__(self, other):
        return Bits(other) * self

    def __rmatmul__(self, other):
        return NotImplemented

    def __rtruediv__(self, other):
        return NotImplemented

    def __rfloordiv__(self, other):
        return Bits(other) // self

    def __rmod__(self, other):
        return Bits(other) % self

    def __rdivmod__(self, other):
        return (Bits(other) // self, Bits(other) % self)

    def __rpow__(self, other, mod=None):
        ret = Bits(0)
        if mod is None:
            ret = Bits(other) ** self
        else:
            ret = Bits(other) ** self % Bits(mod)
        return ret

    def __rlshift__(self, other):
        return Bits(other) << self

    def __rrshift__(self, other):
        return Bits(other) >> self

    def __rand__(self, other):
        return Bits(other) & self

    def __rxor__(self, other):
        return Bits(other) ^ self

    def __ror__(self, other):
        return Bits(other) | self

    def __iadd__(self, other):
        self = self + Bits(other)
        return self

    def __isub__(self, other):
        self = self - Bits(other)
        return self

    def __imul__(self, other):
        self = self * Bits(other)
        return self

    def __imatmul__(self, other):
        return NotImplemented

    def __itruediv__(self, other):
        return NotImplemented

    def __ifloordiv__(self, other):
        self = self // Bits(other)
        return self

    def __imod__(self, other):
        self = self % Bits(other)
        return self

    def __ipow__(self, other):
        self = self ** Bits(other)
        return self

    def __ilshift__(self, other):
        self = self << Bits(other)
        return self

    def __irshift__(self, other):
        self = self >> Bits(other)
        return self

    def __iand__(self, other):
        self = self & Bits(other)
        return self

    def __ixor__(self, other):
        self = self ^ Bits(other)
        return self

    def __ior__(self, other):
        """
        inverse or
        """
        self = self | Bits(other)
        return self

    def __contains__(self, item):
        """
        Return True if binary item is in self
        item: The bits to test
        Examples:
          self = "00110011"
          "1" in self -> True
          1 in self -> True
          "11" in self -> True (equiv to 3 in self, "00000011" in self)
          "00010000" in self -> True (equiv to 16 in self)
          "00100001" in self -> True (equiv to 33 in self, (32 + 1) in self)
        In other words, returns True if bit is set
        """
        val = Bits(item) & self
        return val == Bits(item)

    def __setvalue(self, var):
        """
        Internal function to process supported variants (object types) and
        set the value of self to int(var)
        """
        self.__value = 0
        if isinstance(var, (int, bool, Bits, Bytes, Bit)):
            var_i = int(var)
            if var_i < 0 or var_i > 255:
                raise ValueError("Integer must be between 0 and 255")
            self.__value = var_i
        elif isinstance(var, bytes):
            if len(var) == 1:
                self.__setvalue(ord(var))
            elif len(var) > 1:
                raise ValueError("bytes must be single byte with integer"
                                 " value between 0 and 255")
        elif isinstance(var, (list, str)) and (len(var) <=8):
            # handles: "01010101"
            #          ["0", "1", "0", "1", "0", "1", "0", "1"]
            #          [0, 1, 0, 1, 0, 1, 0, 1]
            #          [False, True, False, True, False, True, False, True]
            #          Other objects with len 1<>8 that are subscriptable
            #            and each subscript item can be cast to int
            for bit in range(0, len(var)):
                self.__value += (int(bool(int(var[bit]))) *
                                 (2 ** (len(var) - 1 - bit)))
        else:
            raise TypeError("Expected compatible object")

    def bin(self, pad=True, reverse=False):
        """
        Return binary string representation of self
        pad: True to include leading zeros, False to strip leading zeroes
        reverse: True to return binary string representation of self as stiB.
        """
        if self.__value == 0:
            if pad:
                return "0" * 8
            else:
                return "0"

        from math import ceil
        bitcount = self.__value.bit_length()
        ret = ""
        if pad and ((bitcount % 8) > 0):
            ret = "0" * (8 - (bitcount % 8))
        ret += bin(self.__value)[2:]
        if reverse:
            ret = ret[::-1]
        return ret

    @property
    def chr(self):
        """
        Return ascii character of int(self)
        """
        return chr(self.__value)

    @property
    def int(self):
        """
        Return int(self)
        """
        return int(self)

    @int.setter
    def int(self, value):
        """
        Set value of self
        value: int(0 - 255)
        """
        self.__setvalue(value)

    @property
    def byte(self):
        """
        Return b'(self)'
        """
        return bytes(self)

    def reverse(self):
        """
        Set Bits(self) to stiB(self)
        """
        self.__setvalue(self.bin()[::-1])

    @property
    def msb(self):
        """
        Return most significant bit
        """
        return self.bin()[0]

    @property
    def lsb(self):
        """
        Get least significant bit
        """
        return self.bin()[7]

    @property
    def nibble(self):
        """
        list(bit[0:4], bit[4:8])
        """
        return [self.bin()[:4], self.bin()[4:]]

    @property
    def rtl(self):
        """
        True if stib, otherwise bits
        """
        return self.__r_to_l

    @property
    def Bit(self):
        """
        Returns list(of Bit, self)
        """
        return list(self)

    @rtl.setter
    def rtl(self, msb_last):
        """
        bits|stib
        01100011 becomes 11000110
        """
        self.__r_to_l = bool(msb_last)

    def list(self, pad=True, reverse=False):
        """
        Return self as list(of Bit)
        """
        ret = []
        bits = self.bin(pad=pad, reverse=reverse)
        for b in bits:
            ret.append(Bit(b))
        return ret

    def hex(self):
        """
        Return the hex-string representation of self
        """
        return bytes(self).hex()


class Bytes:
    """
    A colletion of Bits with convenient properties for working with binary data
    """

    import sys

    def __init__(self, var=None, byteorder="big"):
        """
        var: a supported variant (object)
        byteorder: notimplemented, mostly ignored
        """
        self.__raw = bytearray(b'')
        self.__small = False
        self.__iter = None
        self.__list_len = None
        if byteorder.lower() in ["small", "little"]:
            self.__small = True
        if var is not None:
            self.__raw = self.__to_bytearray(var)

    def __bytes__(self):
        """
        Value of self in binary
        """
        return bytes(self.__raw)

    def __int__(self):
        """
        Self, but as an intfant
        """
        return self.int()

    def __repr__(self):
        """
        Represent self
        """
        ret = f'{self.__class__.__module__}.{self.__class__.__name__}'
        ret += f'({bytes(self)})'
        return ret

    def __index__(self):
        """
        Return int representation of self
        """
        return self.int()

    def __getitem__(self, index):
        """
        Get single byte from self as Bits object
        """
        if not isinstance(index, int):
            raise TypeError
        return Bits(self.__raw[index])

    def __setitem__(self, index, value):
        """
        Change value of byte in self
        """
        if not isinstance(index, int):
            raise TypeError
        self.__raw[index] = int(value)

    def __delitem__(self, index):
        """
        Delete (remove) byte from self
        """
        del self.__raw[index]

    def __test_key(self, key):
        if not isinstance(key, int):
            raise TypeError
        if key >= len(self.__raw):
            raise IndexError
        return True

    def __eq__(self, compare):
        """
        int(self) == int(compare)
        """
        return int(self) == int(compare)

    def __ne__(self, compare):
        """
        int(self) != int(compare)
        """
        return int(self) != int(compare)

    def __lt__(self, compare):
        """
        int(self) < int(compare)
        """
        return int(self) < int(compare)

    def __le__(self, compare):
        """
        int(self) <= int(compare)
        """
        return int(self) <= int(compare)

    def __gt__(self, compare):
        """
        int(self) > int(compare)
        """
        return int(self) > int(compare)

    def __ge__(self, compare):
        """
        int(self) >= int(compare)
        """
        return int(self) >= int(compare)

    def __hash__(self):
        """
        NotImplemented
        """
        return None

    def __bool__(self):
        """
        Return bool(int(self))
        """
        return bool(int(self))

    def __len__(self):
        """
        Return count of bytes in self
        """
        return len(self.__raw)

    def __get__(self, instance, owner=None):
        """
        get(self)
        """
        return self.__raw

    def __str__(self):
        """
        Return binary string of self
        """
        return self.bin()

    def __to_bytearray(self, var):
        """
        Internal function to cast compatible objects to bytearray.
        var: Any of (bytearray|int|bytes|str|Bytes|
                     list(of (bool|int|Bit|Bits|Bytes|bytes)))
        returns: Binary representation of var as <bytearray>
        """
        retvalue = bytearray(b'')
        byteorder="little" if self.__small else "big"
        if isinstance(var, int):
            retvalue = bytearray(self.from_int(var, byteorder))
        elif isinstance(var, bytes):
            retvalue = bytearray(var)
        elif isinstance(var, str):
            import re
            if not re.match('[01]*$', var):
                raise TypeError("Bytes(str): str must contain only binary "
                                "characters [0,1]")
            if len(var) % 8 > 0:
                var = ("0" * (8 - (len(var) % 8))) + var
            bitelist = []
            for i in range(0, len(var), 8):
                bitelist.append(Bits(var[i:i+8]))
            retvalue = bytearray(bitelist)
        elif isinstance(var, bytearray):
            retvalue = var
        elif isinstance(var, Bytes):
            retvalue = bytearray(bytes(var))
        elif isinstance(var, list):
            # test first item in list to see if it is Bit
            if len(var) > 0 and isinstance(var[0], (bool, Bit)):
                bitstring = ""
                for bit in var:
                    bitstring = bitstring + str(Bit(bit))
                retvalue += bytearray(bytes(Bytes(bitstring)))
            else:
                for item in var:
                    if isinstance(item, (int, Bits, Bytes)):
                        retvalue += bytearray(self.from_int(int(item),
                                                            byteorder))
                    elif isinstance(item, bytes):
                        retvalue += bytearray(item)
        return retvalue

    def int(self, _bytes=None, byteorder="big", signed=False):
        if _bytes is None:
            _bytes = bytes(self)
        return int.from_bytes(bytes=_bytes, byteorder=byteorder,
                              signed=signed)

    def bin(self, i=None, pad=True):
        if i is None:
            i = self.int()
        bitcount = i.bit_length()
        ret = ""
        if pad and ((bitcount % 8) > 0):
            ret = "0" * (8 - (bitcount % 8))
        chop = 2
        if i < 0:
            # account for the sign character
            chop += 1
        return ret + bin(i)[chop:]

    def hex(self, sep=None, bytes_per_sep=1):
        """
        Return the hex-string representation of self
        """
        hexvalue = bytes(self).hex()
        if sep is None or bytes_per_sep is None or bytes_per_sep == 0:
            return hexvalue
        else:
            if bytes_per_sep > 1:
                hexvalue = hexvalue[::-1] # reverse the hex string
                sep = sep[::-1]
            i = 0
            retvalue = ""
            while i < len(hexvalue):
                if i > 0:
                    retvalue = retvalue + sep
                retvalue = retvalue + hexvalue[i:(abs(bytes_per_sep * 2) + i)]
                i += abs(bytes_per_sep * 2)
            if bytes_per_sep > 1:
                retvalue = retvalue[::-1]
            return retvalue

    @property
    def bytes(self):
        return bytes(self)

    @property
    def bits(self):
        """
        List of Bit
        """
        bitlist = []
        for bite in list(self):
            bitlist += list(bite)
        return bitlist

    @property
    def stib(self):
        """
        Tsil of Bit
        """
        return self.bits[::-1]

    @property
    def bytearray(self):
        """
        Copy of self as bytearray
        """
        return bytearray(bytes(self))

    def from_int(self, i, byteorder="big"):
            signed = False
            # only work with objects that can cast to int
            i = int(i)
            if i < 0:
                signed = True
            length = int((len(self.bin(i=i, pad=True)) / 8))
            return i.to_bytes(length=length,
                              byteorder=byteorder,
                              signed=signed)


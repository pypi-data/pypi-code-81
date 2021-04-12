"""
encode byte type

Author: Anton Feldmann <anton.feldmann@gmail.com>
"""

# for floating point numbers
import struct

# because numpy byte date is special
import numpy as np


class Bytes(bytes):
    """ extends the byte datatype """
    @staticmethod
    def b2s(byt: bytes) -> str:
        """
            convert bytes to string

        Arguments:
            byt(byte): data of byte type

        Returns:
            (str): encoded byte in string

        Examples:
        ..  example_code::
            >>> from apu.encoding.bytes import Bytes

            >>> Bytes.b2s("test".encode())
            test
        """
        if isinstance(byt, bytes):
            return byt.decode()

        return str(byt)

    @staticmethod
    def f2b(fnumber: float) -> bytes:
        """
            convert a floating point number to byte

        Arguments:
            fnumber(float): float number

        Returns:
            (bytes): float as byte

        Examples:
        ..  example_code::
            >>> from apu.encoding.bytes import Bytes

            >>> Bytes.f2b(3.1)
            b'ffF@'
        """
        if not isinstance(fnumber, float):
            return fnumber
        return struct.pack('f', fnumber)

    @staticmethod
    def b2f(bnumber: bytes) -> float:
        """
            convert a byte string to a floating point number

        Arguments:
            bnumber(bytes): float in byte representation

        Returns:
            (float): float number

        Examples:
        ..  example_code::
            >>> from apu.encoding.bytes import Bytes

            >>> Bytes.b2f(b'ffF@')
            3.0999999046325684
        """
        if not isinstance(bnumber, bytes):
            return bnumber

        [number] = struct.unpack('f', bnumber)
        return number


class NumpyBytes(Bytes):
    """
    convert a numpy object to bytes and back
    """
    @staticmethod
    def array2byte(matrix: np.ndarray) -> bytes:
        """encode the matrix data to bytes

        Arguments:
            matrix(numpy.ndarray): numpy array

        Returns:
            (bytes): matrix as bytes

        Raises:
            TypeError: the matrix is not a numpy array type

        Examples:
        ..  example_code::
            >>> import numpy as np
            >>> from apu.encoding.bytes import NumpyBytes

            >>> array = np.zeros(1)
            >>> NumpyBytes.array2byte(array)
            <memory at 0x7f202e34fc80>
        """
        if not isinstance(matrix, np.ndarray):
            raise TypeError("argument not numpy array type")
        return matrix.data if matrix.flags['C_CONTIGUOUS'] else matrix.tobytes(
        )

    @staticmethod
    def number2bytes(num) -> bytes:
        """ convert a pure numpy number object to bytes

        Arguments:
            num(numpy.number, numpy.bool_): numpy number object

        Returns:
            (bytes): number in byte representation

        Raises:
            TypeError: the number is not a numpy number type

        Examples:
        ..  example_code::
            >>> import numpy as np
            >>> from apu.encoding.bytes import NumpyBytes

            >>> num = np.float32(1)
            >>> NumpyBytes.number2bytes(num)
            <memory at 0x7fcae8055ec0>
        """
        if not isinstance(num, (np.bool_, np.number)):
            raise TypeError("argument not numpy number type")
        return num.data

    @staticmethod
    def encode(npobj, chain=None):
        """numpy object encoder

        Arguments:
            npobj: numpy object
            chain: chain function activation

        Returns:
            (dict): object description with byte data

        Examples:
        ..  example_code::
            >>> import numpy as np
            >>> from apu.encoding.bytes import NumpyBytes

            >>> array = np.zeros(1)
            >>> NumpyBytes.encode(array)
            {b'nd': True, b'type': '<f8', b'kind': b'',
            b'shape': (1,), b'data': <memory at 0x7fcae79b87a0>}
        """
        coded = None
        if isinstance(npobj, np.ndarray):
            if npobj.dtype.kind == 'V':
                kind = b'V'
                descr = npobj.dtype.descr
            else:
                kind = b''
                descr = npobj.dtype.str
            coded = {
                b'nd': True,
                b'type': descr,
                b'kind': kind,
                b'shape': npobj.shape,
                b'data': NumpyBytes.array2byte(npobj)
            }

        elif isinstance(npobj, (np.bool_, np.number)):
            coded = {
                b'nd': False,
                b'type': npobj.dtype.str,
                b'data': NumpyBytes.number2bytes(npobj)
            }

        elif isinstance(npobj, complex):
            coded = {b'complex': True, b'data': npobj.__repr__()}
        else:
            coded = npobj if chain is None else chain(npobj)

        return coded

    @staticmethod
    def decode(npobj, chain=None):
        """numpy object decoder

        Arguments:
            npobj: numpy object as dict of bytes
            chain: chain function activation

        Returns:
            numpy object: object description with byte data

        Examples:
        ..  example_code::
            >>> import numpy as np
            >>> from apu.encoding.bytes import NumpyBytes

            >>> NumpyBytes.decode(
                {b'nd': True, b'type': '<f8', b'kind': b'',
                b'shape': (1,), b'data': <memory at 0x7fcae79b87a0>})
            array([0.])

        """
        decoded = None

        try:
            if b'nd' in npobj:
                if npobj[b'nd'] is True:
                    if b'kind' in npobj and npobj[b'kind'] == b'V':
                        descr = [tuple(NumpyBytes.b2s(t) \
                            if isinstance(t, bytes) else t for t in d) \
                            for d in npobj[b'type']]
                    else:
                        descr = npobj[b'type']
                    decoded = np.frombuffer(
                        npobj[b'data'],
                        dtype=NumpyBytes._unpack_dtype(descr)).reshape(
                            npobj[b'shape'])
                else:
                    descr = npobj[b'type']
                    decoded = np.frombuffer(
                        npobj[b'data'],
                        dtype=NumpyBytes._unpack_dtype(descr))[0]
            elif b'complex' in npobj:
                decoded = complex(NumpyBytes.b2s(npobj[b'data']))
            else:
                decoded = npobj if chain is None else chain(npobj)
        except KeyError:
            decoded = npobj if chain is None else chain(npobj)

        return decoded

    @staticmethod
    def _unpack_dtype(dtype):
        """ datatype unpacking for numby object decoder

        Arguments:
            dtype(bytes): datatype byte type

        Returns:
            (numpy.dtype): numpy datatype
        """
        if isinstance(dtype, (list, tuple)):
            # Unpack structured dtypes of the form: (name, type, *shape)
            dtype = [(subdtype[0], NumpyBytes._unpack_dtype(subdtype[1])) +
                     tuple(subdtype[2:]) for subdtype in dtype]
        return np.dtype(dtype)

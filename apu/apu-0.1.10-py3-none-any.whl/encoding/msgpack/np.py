""" massage paacker is a project to build fast, optimized binary code
    i want to use this for numpy as an json alternative
"""
#https://github.com/lebedov/msgpack-numpy


from functools import partial
import msgpack
from msgpack import (Packer as _Packer,
                    Unpacker as _Unpacker,
                    unpack as _unpack,
                    unpackb as _unpackb)

from apu.encoding.bytes import NumpyBytes

# pylint: disable=R0913,C0301

#check for msgpack version. I do not support msg pack < 1.0.0
if msgpack.version < (1, 0, 0):
    print(f"do not support msgpack version {msgpack.version}")
    # but i will make dummy classes
    class Packer(_Packer):
        """ dummy packer class"""

    class Unpacker(_Unpacker):
        """ dummy unpacker class"""
else:
    class Packer(_Packer):
        """ Build binary string """
        def __init__(self,
                     default=None,
                     use_single_float=False,
                     autoreset=True,
                     use_bin_type=True,
                     strict_types=False,
                     datetime=False,
                     unicode_errors=None):
            default = partial(NumpyBytes.encode, chain=default)
            super().__init__(default=default,
                             use_single_float=use_single_float,
                             autoreset=autoreset,
                             use_bin_type=use_bin_type,
                             strict_types=strict_types,
                             datetime=datetime,
                             unicode_errors=unicode_errors)

    class Unpacker(_Unpacker):
        """ unflold binary string """
        def __init__(self,
                     file_like=None,
                     read_size=0,
                     use_list=True,
                     raw=False,
                     timestamp=0,
                     strict_map_key=True,
                     object_hook=None,
                     object_pairs_hook=None,
                     list_hook=None,
                     unicode_errors=None,
                     max_buffer_size=100 * 1024 * 1024,
                     ext_hook=msgpack.ExtType,
                     max_str_len=-1,
                     max_bin_len=-1,
                     max_array_len=-1,
                     max_map_len=-1,
                     max_ext_len=-1):
            object_hook = partial(NumpyBytes.decode, chain=object_hook)
            super().__init__(file_like=file_like,
                             read_size=read_size,
                             use_list=use_list,
                             raw=raw,
                             timestamp=timestamp,
                             strict_map_key=strict_map_key,
                             object_hook=object_hook,
                             object_pairs_hook=object_pairs_hook,
                             list_hook=list_hook,
                             unicode_errors=unicode_errors,
                             max_buffer_size=max_buffer_size,
                             ext_hook=ext_hook,
                             max_str_len=max_str_len,
                             max_bin_len=max_bin_len,
                             max_array_len=max_array_len,
                             max_map_len=max_map_len,
                             max_ext_len=max_ext_len)


def pack(obj, stream, **kwargs):
    """
    Pack an object and write it to a stream.
    """
    packer = Packer(**kwargs)
    stream.write(packer.pack(obj))


def packb(obj, **kwargs):
    """
    Pack an object and return the packed bytes.
    """
    return Packer(**kwargs).pack(obj)


def unpack(stream, **kwargs):
    """
    Unpack a packed object from a stream.
    """
    object_hook = kwargs.get('object_hook')
    kwargs['object_hook'] = partial(NumpyBytes.decode, chain=object_hook)
    return _unpack(stream, **kwargs)


def unpackb(packed, **kwargs):
    """
    Unpack a packed object.
    """
    object_hook = kwargs.get('object_hook')
    kwargs['object_hook'] = partial(NumpyBytes.decode, chain=object_hook)
    return _unpackb(packed, **kwargs)


load = unpack
loads = unpackb
dump = pack
dumps = packb


def patch():
    """
    Monkey patch msgpack module to enable support for serializing numpy types.
    """

    setattr(msgpack, 'Packer', Packer)
    setattr(msgpack, 'Unpacker', Unpacker)
    setattr(msgpack, 'load', unpack)
    setattr(msgpack, 'loads', unpackb)
    setattr(msgpack, 'dump', pack)
    setattr(msgpack, 'dumps', packb)
    setattr(msgpack, 'pack', pack)
    setattr(msgpack, 'packb', packb)
    setattr(msgpack, 'unpack', unpack)
    setattr(msgpack, 'unpackb', unpackb)


class NumpyMSG:
    """ numpy class to handle

    Examples:
    ..  example_code::
        >>> from apu.encoding.msgpack.np import NumpyMSG
        >>> import numpy as np
        >>> arr = x = np.random.rand(5)
        array([0.24012777, 0.20899095, 0.88586647, 0.75854848, 0.22062769])
        >>> np_message = NumpyMSG.start()
        >>> msg = np_message.encode(x)
        b'\x85\xc4\x02nd\xc3\xc4\x04type\xa3<f8\xc4\x04kind\xc4\x00\xc4\x05shape
        \x91\x05\xc4\x04data\xc4(\xb0\x13\xe0\xb6\x81\xbc\xce?\xd8\t\x9a/7\xc0\xca?\xca\x19)
        \xa4\x04Y\xec?*\x14\x83v\x07F\xe8?\xd8\xf6P=\x87=\xcc?'
        >>> msg = np_message.decode(msg)
        [0.24012777 0.20899095 0.88586647 0.75854848 0.22062769]

    """
    def __init__(self):
        patch()

    @staticmethod
    def start():
        """ start the massage system"""
        return NumpyMSG()

    @staticmethod
    def encode(msg):
        """ encode the message giben the numpy byte encoder """
        return msgpack.packb(msg, default=NumpyBytes.encode)

    @staticmethod
    def decode(coded_msg, use_list=True, max_bin_len=-1):
        """ decode the massage utilizing the NumpyBytes decoder """
        return msgpack.unpackb(coded_msg,
                               use_list=use_list,
                               max_bin_len=max_bin_len,
                               object_hook=NumpyBytes.decode)

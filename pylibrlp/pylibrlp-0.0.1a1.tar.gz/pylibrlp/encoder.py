# standard imports
import sys
import logging
import ctypes
import enum

# local imports
from . import (
    LIBRLP_RLP_MAX_LIST_DEPTH,
    librlp,
        )

logg = logging.getLogger().getChild(__name__)


class RLPState(enum.IntEnum):
    RLP_DECODE=0,
    RLP_ENCODE=1,
    RLP_LIST_ASCEND=2,
    RLP_LIST_DESCEND=3,
    RLP_STRING=4,
    RLP_END=5,


class RLPEncoder:

    __nullptr = ctypes.POINTER(ctypes.c_void_p)()

    def __init__(self, buffer_size):

        class RLPEncoderBackend(ctypes.Structure):

            _fields_ = [
                    ('buf', ctypes.POINTER(ctypes.c_char * buffer_size)),
                    ('alloc', ctypes.c_char),
                    ('depth', ctypes.c_int),
                    ('size', ctypes.c_int),
                    ('state', ctypes.c_int),
                    ('list_ptr', ctypes.POINTER(ctypes.POINTER(ctypes.c_char)) * LIBRLP_RLP_MAX_LIST_DEPTH),
                    ('ptr', ctypes.POINTER(ctypes.c_char)),
                    ]
    
        self.buffer_size = buffer_size
        self.backend = RLPEncoderBackend()
        self.encoder = ctypes.pointer(self.backend)

        # decoder specific
        self.zl = ctypes.pointer(ctypes.c_int())
        self.buf = None


    def __del__(self):
        logg.debug('free')
        librlp.rlp_free(self.encoder)


    def encode_item(self, v):
        if isinstance(v, list):
            librlp.rlp_descend(self.encoder)
            for e in v:
                self.encode_item(e)
            librlp.rlp_ascend(self.encoder)

        else:
            b = (ctypes.c_char * len(v))(*v)
            librlp.rlp_add(self.encoder, len(v), b)

        return self.backend.size


    def encode(self, v):
        librlp.rlp_init(self.encoder, self.buffer_size, self.__nullptr)
        r = self.encode_item(v)

        return bytes(self.backend.buf.contents[:r])


    def decode_item(self, frame, stack):
        logg.debug('frame {} stack {} depth {}'.format(frame, stack, self.backend.depth))
        r = librlp.rlp_next(self.encoder, self.zl, ctypes.pointer(self.buf))

        if self.backend.state == RLPState.RLP_LIST_DESCEND:
            stack.append(frame)
            frame = []

        elif self.backend.state == RLPState.RLP_LIST_ASCEND:
            raise ValueError()
            frame.append(stack.append(frame))

        elif self.backend.state == RLPState.RLP_STRING:
            l = int(self.zl.contents.value)
            b = self.buf.contents[:l]
            logg.debug('v {}'.format(b))
            frame.append(b)

        elif self.backend.state == RLPState.RLP_END:
            stack = None

        else:
            raise AttributeError('unexpected state {}'.format(self.backend.state))
      
        return (frame, stack)

    def decode(self, v, size_hint=None):
        if size_hint == None:
            size_hint = sys.getsizeof(v)

        in_buffer = ctypes.c_char * len(v)
        in_buffer_p = in_buffer.from_buffer(bytearray(v))
        librlp.rlp_init(self.encoder, len(v), in_buffer_p)

        self.zl = ctypes.pointer(ctypes.c_int())
        self.buf = ctypes.pointer((ctypes.c_char * size_hint)())

        frame = []
        stack = []
        while stack != None:
            (frame, stack) = self.decode_item(frame, stack)
            l = self.backend.depth

        return frame[0]

# standard imports
import sys
import re
import os
import ctypes
import ctypes.util


LIBRLP_RLP_MAX_LIST_DEPTH = 1024


__path_librlp = ctypes.util.find_library('rlp')


if __path_librlp == None:
    v = sys.version_info
    re_so = r'^rlp.cpython-' + str(v[0]) + str(v[1]) + '.*\.so$'
    script_dir = os.path.dirname(__file__)
    root_dir = os.path.join(script_dir, '..')
    for f in os.listdir(root_dir):
        if re.match(re_so, f):
            __path_librlp = os.path.join(root_dir, f)
            break

if __path_librlp == None:
    raise ImportError('missing librlp shared library')

librlp = ctypes.CDLL(__path_librlp)

from .encoder import RLPEncoder

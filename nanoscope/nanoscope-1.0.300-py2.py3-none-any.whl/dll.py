# -*- coding: utf-8 -*-
"""
Common tools for the dll.

"""

import ctypes
import numpy as np
import os
import platform
from ctypes import c_char
from numpy.ctypeslib import ndpointer as ndp

_MAX_STRING_SIZE = 100
_np_int32 = ndp(np.int32, flags="C_CONTIGUOUS")
_np_float = ndp(np.float, flags="C_CONTIGUOUS")
_np_double = ndp(np.double, flags="C_CONTIGUOUS")
_string_buffer = c_char * _MAX_STRING_SIZE


def get_version_info():
    info = _string_buffer()
    _get("VersionInfo", info)
    return info.value.decode("latin-1")


def _load():
    """Load the dll.

    Raise a WindowsError if it fails.
    """
    cwd = os.getcwd()
    dir_ = os.path.dirname(os.path.realpath(__file__))
    arch = platform.architecture()[0]  # 32/64bit
    if arch not in ("32bit", "64bit"):
        raise WindowsError("Could not recognize platform.")
    os.chdir(os.path.join(dir_, "Lib", arch))
    if os.environ['PATH'].find(os.getcwd()) < 0:
        os.environ['PATH'] += r"" + os.pathsep + os.getcwd() + "\\"
    try:
        datasource_dll = ctypes.cdll.LoadLibrary("DataSourceDLL")
    except WindowsError:
        raise WindowsError("DLL load failed, "
                           "please check the installation.")
    finally:
        os.chdir(cwd)
    return datasource_dll


def _open(filename):
    if _current_filename:
        _close()
    success = _dll.DataSourceDllOpen(filename.encode("utf-8"))
    if success != 1:
        raise IOError("Could not open {}".format(filename))


def _close():
    global _current_filename
    _dll.DataSourceDllClose()
    _current_filename = None


def _get(arg_name, *args, **kwargs):
    """Execute the get function linked to the arg_name.

    That function must be part of the dll.
    """
    func = getattr(_dll, "DataSourceDllGet" + arg_name)
    if "argtypes" in kwargs.keys():
        func.argtypes = kwargs["argtypes"]
        del kwargs["argtypes"]
    val = func(*args, **kwargs)
    if not (val and val > 0):
            raise RuntimeError("DLL call resulted in an error.")


_dll = _load()
_current_filename = None

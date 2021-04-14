"""Implementation of the platform-dependent part of this module for Darwin."""

# Based on the work of Michael Lynn
# https://github.com/pudquick/pypmset/blob/master/pypmset.py

import atexit
from contextlib import contextmanager
from ctypes import POINTER, byref, c_int, c_uint32, c_void_p, cdll
from typing import Dict

from CoreFoundation import (  # type: ignore
    CFDictionaryGetValue,
    CFRelease,
    CFStringCreateWithCString,
    kCFStringEncodingASCII,
)
from objc import objc_object, pyobjc_id  # type: ignore

__all__ = ("_enter", "_exit", "_verify")


# Load the IOKit library
libIOKit = cdll.LoadLibrary("/System/Library/Frameworks/IOKit.framework/IOKit")

# Define argument types for the IOKit functions we are going to use
libIOKit.IOPMAssertionCreateWithName.argtypes = [
    c_void_p,
    c_uint32,
    c_void_p,
    POINTER(c_uint32),
]
libIOKit.IOPMCopyAssertionsStatus.argtypes = [c_void_p]
libIOKit.IOPMAssertionRelease.argtypes = [c_uint32]


def CFSTR(py_string: bytes):
    """Converts a Python byte string into an Objective C string, using ASCII
    encoding.
    """
    return CFStringCreateWithCString(None, py_string, kCFStringEncodingASCII)


def raw_ptr_from_string(pyobjc_string):
    return pyobjc_id(pyobjc_string.nsstring())


def IOPMAssertionCreateWithName(type: bytes, level: int, name: bytes) -> c_uint32:
    assertion_id = c_uint32(0)
    p_assertion_type = raw_ptr_from_string(CFSTR(type))
    p_assertion_name = raw_ptr_from_string(CFSTR(name))
    error_code = libIOKit.IOPMAssertionCreateWithName(
        p_assertion_type, level, p_assertion_name, byref(assertion_id)
    )
    if error_code != 0:
        raise RuntimeError("Failed to create power management assertion")
    return assertion_id


def IOPMAssertionRelease(assertion_id: c_uint32) -> None:
    error_code = libIOKit.IOPMAssertionRelease(assertion_id)
    if error_code != 0:
        raise RuntimeError("Failed to release power management assertion")


def get_assertion_type(display: bool) -> bytes:
    """Returns the macOS power management assertion type suitable for the given
    configuration.

    Parameters:
        display: whether to keep the display on

    Returns:
        the macOS power management assertion type as a Python byte string
    """
    if display:
        return b"NoDisplaySleepAssertion"
    else:
        return b"NoIdleSleepAssertion"


kIOPMAssertionLevelOn = 255
current_assertion_id = c_uint32(0)


def _enter(*, display: bool, reason: str) -> None:
    global current_assertion_id
    assertion_type = get_assertion_type(display)
    if current_assertion_id.value == 0:
        current_assertion_id = IOPMAssertionCreateWithName(
            assertion_type,
            kIOPMAssertionLevelOn,
            reason.encode("ascii", errors="replace"),
        )


def _exit() -> None:
    global current_assertion_id
    IOPMAssertionRelease(current_assertion_id)
    current_assertion_id.value = 0


def _verify() -> bool:
    from subprocess import check_output

    output = check_output(["pmset", "-g", "assertions"])
    lines = output.strip().split(b"\n")
    return any(
        b'SleepAssertion named: "Python adrenaline module"' in line for line in lines
    )

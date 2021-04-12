# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the names of the possible C and C++
compiler toolchains.
"""


def get_clang_toolchain_name():
    """Gives the name of the Clang compiler toolchain."""
    return "clang"


def get_gcc_toolchain_name():
    """Gives the name of the GCC compiler toolchain."""
    return "gcc"


def get_msvc_toolchain_name():
    """Gives the name of the MSVC compiler toolchain."""
    return "msvc"


def get_compiler_toolchain_names():
    """Gives the names of the possible compiler toolchains."""
    return [
        get_clang_toolchain_name(),
        get_gcc_toolchain_name(),
        get_msvc_toolchain_name()
    ]

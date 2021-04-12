# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains various constants related to the
platform.
"""


def get_darwin_system_name():
    """
    Gives the system name of a platform that runs on Darwin.
    """
    return "Darwin".lower()


def get_linux_system_name():
    """
    Gives the system name of a platform that runs on Linux.
    """
    return "Linux".lower()


def get_windows_system_name():
    """
    Gives the system name of a platform that runs on Windows.
    """
    return "Windows".lower()

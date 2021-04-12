# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""This support module contains the possible build variant."""


def get_debug_variant_name():
    """Gives the name of the debug build variant."""
    return "Debug"


def get_release_with_debuginfo_variant_name():
    """
    Gives the name of the release build variant with debug
    information.
    """
    return "RelWithDebInfo"


def get_release_variant_name():
    """Gives the name of the release build variant."""
    return "Release"


def get_minimum_size_release_variant_name():
    """
    Gives the name of the minimum size release build variant.
    """
    return "MinSizeRel"


def get_build_variant_names():
    """Gives the names of the possible build variants."""
    return [
        get_debug_variant_name(),
        get_release_with_debuginfo_variant_name(),
        get_release_variant_name(),
        get_minimum_size_release_variant_name()
    ]

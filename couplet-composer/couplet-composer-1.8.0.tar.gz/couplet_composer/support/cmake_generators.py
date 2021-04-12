# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the names of the possible CMake
generators for the project this script acts on.
"""


def get_ninja_cmake_generator_name():
    """
    Gives the name of the CMake generator that creates build
    scripts for Ninja.
    """
    return "Ninja"


def get_make_cmake_generator_name():
    """
    Gives the name of the CMake generator that creates build
    scripts for Make.
    """
    return "Unix Makefiles"


def get_visual_studio_16_cmake_generator_name():
    """
    Gives the name of the CMake generator that creates build
    scripts for Visual Studio 16.
    """
    return "Visual Studio 16 2019"


def get_cmake_generator_names():
    """Gives the names of the possible CMake generators."""
    return [
        get_ninja_cmake_generator_name(),
        get_make_cmake_generator_name(),
        get_visual_studio_16_cmake_generator_name()
    ]

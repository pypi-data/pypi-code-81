# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""
This support module contains type DependencyInstallInfo for
passing the data required to install a dependency.
"""

from collections import namedtuple


# The type 'DependencyInstallInfo' represents the data to install a
# tool.
#
# toolchain -- The toolchain object of the run.
#
# cmake_generator -- The name of the generator that CMake should
# use as the build system for which the build scripts are
# generated.
#
# build_root -- The path to the root directory that is used for
# all created files and directories.
#
# dependencies_root -- The root directory of the dependencies for
# the current build target.
#
# version -- The full version number of the dependency.
#
# target -- The target system of the build represented by a
# Target.
#
# host_system -- The system this script is run on.
#
# build_variant -- The build variant used to build the project.
#
# github_user_agent -- The user agent used when accessing the
# GitHub API.
#
# github_api_token -- The GitHub API token that is used to access
# the API.
#
# opengl_version -- The version of OpenGL that is used.
DependencyInstallInfo = namedtuple("DependencyInstallInfo", [
    "toolchain",
    "cmake_generator",
    "build_root",
    "dependencies_root",
    "version",
    "target",
    "host_system",
    "build_variant",
    "github_user_agent",
    "github_api_token",
    "opengl_version",
])

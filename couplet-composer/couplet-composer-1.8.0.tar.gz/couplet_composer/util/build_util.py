# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains helpers for making build calls for
the dependencies.
"""

import glob
import logging
import os

from ..support.cmake_generators import \
    get_ninja_cmake_generator_name, get_visual_studio_16_cmake_generator_name

from ..support.platform_names import get_windows_system_name

from . import shell


def build_with_cmake(
    toolchain,
    cmake_generator,
    source_directory,
    temporary_root,
    dependencies_root,
    target,
    host_system,
    build_variant,
    cmake_options=None,
    do_install=True,
    msbuild_target=None,
    dry_run=None,
    print_debug=None
):
    """
    Calls CMake and invokes the build script produced by CMake.

    toolchain -- The toolchain object of the run.

    cmake_generator -- The name of the generator that CMake
    should use as the build system for which the build scripts
    are generated.

    source_directory -- The path to the root directory of the
    project to be built with CMake.

    temporary_root -- The path to the root directory that is used
    for temporary files.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.

    build_variant -- The build variant used to build the project.

    cmake_options -- Additional options passed to CMake.

    do_install -- Whether or not the install command should be
    called after building the project.

    msbuild_target -- Optional name for the Visual Studio
    solution or project that is used to build the project.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    cmake_call = [
        toolchain.cmake,
        source_directory,
        "-DCMAKE_BUILD_TYPE={}".format(build_variant),
        "-DCMAKE_INSTALL_PREFIX={}".format(dependencies_root)
    ]

    if host_system != get_windows_system_name():
        cmake_call.extend(["-DCMAKE_C_COMPILER={}".format(
            toolchain.compiler["cc"]
            if isinstance(toolchain.compiler, dict) else toolchain.compiler
        )])
        cmake_call.extend(["-DCMAKE_CXX_COMPILER={}".format(
            toolchain.compiler["cxx"]
            if isinstance(toolchain.compiler, dict) else toolchain.compiler
        )])

    if cmake_generator == get_ninja_cmake_generator_name():
        cmake_call.extend([
            "-DCMAKE_MAKE_PROGRAM={}".format(toolchain.build_system)
        ])

    cmake_call.extend(["-G", cmake_generator])

    if cmake_options:
        if isinstance(cmake_options, dict):
            for k, v in cmake_options.items():
                if isinstance(v, bool):
                    cmake_call.extend(
                        ["-D{}={}".format(k, ("ON" if v else "OFF"))]
                    )
                else:
                    cmake_call.extend(["-D{}={}".format(k, v)])
        else:
            cmake_call += cmake_options

    if host_system != get_windows_system_name():
        if isinstance(toolchain.compiler, dict):
            cmake_env = {
                "CC": toolchain.compiler["cc"],
                "CXX": toolchain.compiler["cxx"]
            }
        else:
            cmake_env = {"CC": toolchain.compiler, "CXX": toolchain.compiler}
    else:
        cmake_env = None

    build_directory = os.path.join(temporary_root, "build")

    shell.makedirs(build_directory, dry_run=dry_run, echo=print_debug)

    with shell.pushd(build_directory, dry_run=dry_run, echo=print_debug):
        shell.call(
            cmake_call,
            env=cmake_env,
            dry_run=dry_run,
            echo=print_debug
        )
        # Have different call for Visual Studio as MSBuild is
        # used.
        if cmake_generator == get_visual_studio_16_cmake_generator_name():
            logging.debug(
                "The build directory contains the following files and "
                "directories:\n%s",
                "\n".join([f for f in os.listdir(build_directory)])
            )
            build_call = [toolchain.build_system]
            if msbuild_target:
                build_call.extend(["{}".format(msbuild_target)])
            build_call.extend(
                ["/property:Configuration={}".format(build_variant)]
            )
            shell.call(build_call, dry_run=dry_run, echo=print_debug)
            logging.debug(
                "The build library files are:\n%s",
                "\n".join(
                    glob.glob(os.path.join(build_directory, "**", "*.lib"))
                )
            )
        else:
            shell.call(
                [toolchain.build_system],
                dry_run=dry_run,
                echo=print_debug
            )
            if do_install:
                shell.call(
                    [toolchain.build_system, "install"],
                    dry_run=dry_run,
                    echo=print_debug
                )

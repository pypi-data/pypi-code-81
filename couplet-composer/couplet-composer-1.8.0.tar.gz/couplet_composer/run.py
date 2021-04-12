# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the functions that perform common
actions for the current run of the script.
"""

import logging
import sys
import time

from .support.cmake_generators import \
    get_ninja_cmake_generator_name, get_make_cmake_generator_name, \
    get_visual_studio_16_cmake_generator_name

from .support.compiler_toolchains import \
    get_clang_toolchain_name, get_gcc_toolchain_name, get_msvc_toolchain_name

from .support.environment import \
    get_build_root, get_composing_directory, get_dependencies_directory, \
    get_dependency_version_data_file, get_destination_directory, \
    get_tools_directory

from .support.mode_names import get_configuring_mode_name

from .support.tool_data import \
    create_clang_apply_replacements_tool_data, create_clang_tidy_tool_data, \
    create_clang_tool_data, create_cmake_tool_data, create_doxygen_tool_data, \
    create_gcc_tool_data, create_git_tool_data, create_make_tool_data, \
    create_msbuild_tool_data, create_msvc_tool_data, create_ninja_tool_data, \
    create_xvfb_tool_data

from .util.target import parse_target_from_argument_string

from .util import shell


def clean(arguments, source_root):
    """
    Cleans the directories and files before building when clean
    build is invoked.

    arguments -- The namespace containing the parsed command line
    arguments of the script.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    # Two spaces are required at the end of the first line as the
    # counter uses backspace characters.
    sys.stdout.write("\033[31mStarting a clean build in  \033[0m")
    for i in reversed(range(0, 4)):
        sys.stdout.write("\033[31m\b{!s}\033[0m".format(i))
        sys.stdout.flush()
        time.sleep(1)
    print("\033[31m\b\b\b\bnow.\033[0m")

    build_target = parse_target_from_argument_string(arguments.host_target)
    build_root = get_build_root(
        source_root=source_root,
        in_tree_build=arguments.in_tree_build
    )
    composing_root = get_composing_directory(
        build_root=build_root,
        target=build_target,
        cmake_generator=arguments.cmake_generator,
        build_variant=arguments.build_variant
    )
    destination_root = get_destination_directory(
        build_root=build_root,
        target=build_target,
        cmake_generator=arguments.cmake_generator,
        build_variant=arguments.build_variant,
        version=arguments.anthem_version
    )
    tools_root = get_tools_directory(
        build_root=build_root,
        target=build_target
    )
    dependencies_root = get_dependencies_directory(
        build_root=build_root,
        target=build_target,
        build_variant=arguments.build_variant
    )
    version_data_file = get_dependency_version_data_file(
            build_root=build_root,
            target=build_target,
            build_variant=arguments.build_variant
        )

    if arguments.composer_mode == get_configuring_mode_name():
        shell.rmtree(
            tools_root,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )
        shell.rmtree(
            dependencies_root,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )
        shell.rm(
            version_data_file,
            dry_run=arguments.dry_run,
            echo=arguments.print_debug
        )
    shell.rmtree(
        composing_root,
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )
    shell.rmtree(
        destination_root,
        dry_run=arguments.dry_run,
        echo=arguments.print_debug
    )


def construct_tool_data(arguments, host_system):
    """
    Constructs a dictionary containing the required ToolData
    objects for the toolchain for the current host system.

    arguments -- The namespace containing the parsed command line
    arguments of the script.

    host_system -- The system this script is run on.
    """
    def _create_compiler_data(arguments):
        """
        Returns the tool data or tool data pair representing the
        compiler for the script.

        arguments -- The namespace containing the parsed command
        line arguments of the script.
        """
        def _should_use_separate_compilers(arguments):
            """
            Returns whether or not the script should use separate
            C and C++ compilers in the current configuration.

            arguments -- The namespace containing the parsed
            command line arguments of the script.
            """
            if arguments.host_compiler:
                logging.debug(
                    "Going to use single compiler tool as only one is given "
                    "in command line options"
                )
                return False
            elif arguments.compiler_toolchain == get_msvc_toolchain_name():
                logging.debug(
                    "Going to use single compiler tool as the selected "
                    "compiler is MSVC"
                )
                return False
            logging.debug("Going to use separate C and C++ compilers")
            return True

        if _should_use_separate_compilers(arguments=arguments):
            if arguments.host_cc and arguments.host_cxx:
                if "clang" in arguments.host_cc:
                    return create_clang_tool_data(
                        cc_path=arguments.host_cc,
                        cxx_path=arguments.host_cxx
                    )
                elif "gcc" in arguments.host_cc:
                    return create_gcc_tool_data(
                        cc_path=arguments.host_cc,
                        cxx_path=arguments.host_cxx
                    )
                else:
                    return None
            else:
                if arguments.compiler_toolchain == get_clang_toolchain_name():
                    return create_clang_tool_data(
                        version=arguments.compiler_version
                    )
                elif arguments.compiler_toolchain == get_gcc_toolchain_name():
                    return create_gcc_tool_data(
                        version=arguments.compiler_version
                    )
                else:
                    return None
        else:
            if arguments.host_compiler:
                if "msvc" in arguments.host_compiler.lower() \
                        or "cl.exe" in arguments.host_compiler.lower():
                    return create_msvc_tool_data(
                        tool_path=arguments.host_compiler
                    )
            else:
                if arguments.compiler_toolchain == get_msvc_toolchain_name():
                    return create_msvc_tool_data()
                else:
                    return None

    def _create_build_system_data(arguments):
        """
        Returns the tool data representing the build system for
        the script.

        arguments -- The namespace containing the parsed command
        line arguments of the script.
        """
        generator = arguments.cmake_generator
        if generator == get_ninja_cmake_generator_name():
            return create_ninja_tool_data()
        elif generator == get_make_cmake_generator_name():
            return create_make_tool_data()
        elif generator == get_visual_studio_16_cmake_generator_name():
            if arguments.host_msbuild:
                return create_msbuild_tool_data(
                    tool_path=arguments.host_msbuild
                )
            else:
                return create_msbuild_tool_data()

    return {
        "compiler": _create_compiler_data(arguments=arguments),
        "cmake": create_cmake_tool_data(),
        "build_system": _create_build_system_data(arguments=arguments),
        "scm": create_git_tool_data(),
        "make": create_make_tool_data(),
        "doxygen": create_doxygen_tool_data(),
        "linter": create_clang_tidy_tool_data(
            linter_required=arguments.lint,
            tool_path=arguments.clang_tidy_binary
        ),
        "linter_replacements": create_clang_apply_replacements_tool_data(
            linter_required=arguments.lint,
            tool_path=arguments.clang_apply_replacements_binary
        ),
        "xvfb": create_xvfb_tool_data()
    }

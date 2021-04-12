# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the functions for running the
different modes of the script.
"""

from __future__ import print_function

import logging
import os
import sys

from .github.access import get_api_access_values

from .support.environment import \
    get_build_root, get_composing_directory, \
    get_dependency_version_data_file, get_destination_directory, \
    get_project_root, get_tools_directory

from .support.file_paths import \
    get_preset_file_path, get_project_dependencies_file_path

from .support.project_names import get_ode_repository_name, get_project_name

from .util.target import current_platform, parse_target_from_argument_string

from .util import shell

from .composing_mode import \
    compose_project, create_artefacts, create_composing_root, \
    create_destination_root, install_documentation, install_running_copies

from .configuring_mode import create_dependencies_root, create_tools_root

from .dependency_set import construct_dependencies_data, install_dependencies

from .preset_mode import \
    compose_preset_call, print_script_invocation, show_presets

from .toolchain import create_toolchain

from . import run


def run_in_preset_mode(arguments, source_root):
    """
    Runs the script in the preset mode. This function isn't pure
    as the functions called by it may modify the file system and
    run other scripts.

    arguments -- The namespace containing the parsed command line
    arguments of the script.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    logging.debug("Running %s in preset mode", get_project_name())

    if arguments.in_tree_build:
        preset_file_names = [os.path.join(source_root, get_preset_file_path())]
    else:
        preset_file_names = [os.path.join(
            source_root,
            get_ode_repository_name(),
            get_preset_file_path()
        )]

    logging.debug("The preset files are %s", ", ".join(preset_file_names))

    if arguments.show_presets:
        return show_presets(file_names=preset_file_names)

    if not arguments.preset:
        logging.critical("Missing the '--preset' option")

    build_call = compose_preset_call(
        arguments=arguments,
        file_names=preset_file_names
    )

    print_script_invocation(
        build_call=build_call,
        preset_name=arguments.preset,
        executable=sys.executable
    )

    if arguments.expand_script_invocation:
        logging.debug("The build script invocation is printed")
        return 0

    shell.caffeinate(build_call, dry_run=False, echo=True)

    return 0


def run_in_configuring_mode(arguments, source_root):
    """
    Runs the script in configuration mode and sets up the
    development and build environment. This function isn't pure
    as the functions called by it may modify the file system and
    run other scripts.

    arguments -- The namespace containing the parsed command line
    arguments of the script.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    if arguments.clean:
        run.clean(arguments=arguments, source_root=source_root)

    build_target = parse_target_from_argument_string(arguments.host_target)

    # Check the directories.
    tools_root = create_tools_root(
        source_root=source_root,
        in_tree_build=arguments.in_tree_build,
        target=build_target
    )
    build_root = get_build_root(
        source_root=source_root,
        in_tree_build=arguments.in_tree_build
    )

    logging.debug("Creating the toolchain for the run")

    github_user_agent, github_api_token = get_api_access_values(
        source_root=source_root,
        value_file=arguments.github_auth_file,
        user_agent=arguments.github_user_agent,
        api_token=arguments.github_api_token
    )

    toolchain = create_toolchain(
        tools_data=run.construct_tool_data(
            arguments=arguments,
            host_system=current_platform()
        ),
        cmake_generator=arguments.cmake_generator,
        target=build_target,
        host_system=current_platform(),
        github_user_agent=github_user_agent,
        github_api_token=github_api_token,
        tools_root=tools_root,
        build_root=build_root,
        read_only=False,
        dry_run=arguments.dry_run,
        print_debug=arguments.print_debug
    )

    logging.debug("The created toolchain is %s", toolchain)

    logging.debug("Starting to install the dependencies of the project")

    dependencies_root = create_dependencies_root(
        source_root=source_root,
        in_tree_build=arguments.in_tree_build,
        target=build_target,
        build_variant=arguments.build_variant
    )

    install_dependencies(
        dependencies_data=construct_dependencies_data(
            data_file=os.path.join(
                get_project_root(
                    source_root=source_root,
                    in_tree_build=arguments.in_tree_build
                ),
                get_project_dependencies_file_path(source_root)
            )
        ),
        toolchain=toolchain,
        cmake_generator=arguments.cmake_generator,
        target=build_target,
        host_system=current_platform(),
        build_variant=arguments.build_variant,
        github_user_agent=github_user_agent,
        github_api_token=github_api_token,
        opengl_version=arguments.opengl_version,
        dependencies_root=dependencies_root,
        build_root=build_root,
        version_data_file=get_dependency_version_data_file(
            build_root=build_root,
            target=build_target,
            build_variant=arguments.build_variant
        ),
        build_test=arguments.build_test,
        build_benchmark=arguments.build_benchmark,
        dry_run=arguments.dry_run,
        print_debug=arguments.print_debug
    )

    return 0


def run_in_composing_mode(arguments, source_root):
    """
    Runs the script in build mode. This function isn't pure as
    the functions called by it may modify the file system and run
    other scripts.

    arguments -- The namespace containing the parsed command line
    arguments of the script.

    source_root -- Path to the directory that is the root of the
    script run.
    """
    if arguments.clean:
        run.clean(arguments=arguments, source_root=source_root)

    build_target = parse_target_from_argument_string(arguments.host_target)

    # Check the directories.
    tools_root = get_tools_directory(
        build_root=get_build_root(
            source_root=source_root,
            in_tree_build=arguments.in_tree_build
        ),
        target=build_target
    )
    build_root = get_build_root(
        source_root=source_root,
        in_tree_build=arguments.in_tree_build
    )

    logging.debug("Creating the toolchain for the run")

    github_user_agent, github_api_token = get_api_access_values(
        source_root=source_root,
        value_file=arguments.github_auth_file,
        user_agent=arguments.github_user_agent,
        api_token=arguments.github_api_token
    )

    toolchain = create_toolchain(
        tools_data=run.construct_tool_data(
            arguments=arguments,
            host_system=current_platform()
        ),
        cmake_generator=arguments.cmake_generator,
        target=build_target,
        host_system=current_platform(),
        github_user_agent=github_user_agent,
        github_api_token=github_api_token,
        tools_root=tools_root,
        build_root=build_root,
        read_only=True,
        dry_run=arguments.dry_run,
        print_debug=arguments.print_debug
    )

    logging.debug("The created toolchain is %s", toolchain)

    compose_project(
        source_root=source_root,
        toolchain=toolchain,
        arguments=arguments,
        host_system=current_platform(),
        project_root=get_project_root(
            source_root=source_root,
            in_tree_build=arguments.in_tree_build
        ),
        build_root=build_root,
        composing_root=create_composing_root(
            source_root=source_root,
            in_tree_build=arguments.in_tree_build,
            target=build_target,
            cmake_generator=arguments.cmake_generator,
            build_variant=arguments.build_variant
        ),
        destination_root=create_destination_root(
            source_root=source_root,
            in_tree_build=arguments.in_tree_build,
            target=build_target,
            cmake_generator=arguments.cmake_generator,
            build_variant=arguments.build_variant,
            version=arguments.anthem_version
        ),
        dependencies_root=create_dependencies_root(
            source_root=source_root,
            in_tree_build=arguments.in_tree_build,
            target=build_target,
            build_variant=arguments.build_variant
        )
    )

    if arguments.skip_build:
        return 0

    install_running_copies(
        arguments=arguments,
        build_root=build_root,
        destination_root=get_destination_directory(
            build_root=build_root,
            target=build_target,
            cmake_generator=arguments.cmake_generator,
            build_variant=arguments.build_variant,
            version=arguments.anthem_version
        )
    )

    if arguments.build_docs and toolchain.doxygen and not arguments.skip_build:
        install_documentation(
            arguments=arguments,
            build_root=build_root,
            composing_root=get_composing_directory(
                build_root=build_root,
                target=build_target,
                cmake_generator=arguments.cmake_generator,
                build_variant=arguments.build_variant
            )
        )

    create_artefacts(
        arguments=arguments,
        host_system=current_platform(),
        build_root=build_root
    )

    return 0

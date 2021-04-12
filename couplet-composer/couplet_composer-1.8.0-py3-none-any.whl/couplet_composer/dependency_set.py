# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the functions for resolving and
building the dependencies required to by the project that this
script acts on.
"""

import json
import logging

from .support.dependency_data import create_dependency_data

from .support.dependency_install_information import DependencyInstallInfo

from .support.file_paths import \
    get_product_file_path, get_project_values_file_path


def construct_dependencies_data(data_file):
    """
    Constructs a list of objects of type 'DependencyData'
    representing the dependecies of the project this script acts
    on. This function isn't pure as it gets data from a JSON file
    in project this script acts on and from various dependency
    modules.

    data_file -- The file in the project this script acts on that
    contains the data about the required versions of the
    dependencies.
    """
    json_data = None
    with open(data_file) as f:
        json_data = json.load(f)
    dependency_data = json_data \
        if get_project_values_file_path() not in data_file \
            and get_product_file_path() not in data_file \
        else json_data["dependencies"]
    return [create_dependency_data(
        module_name=key,
        data_node=node
        ) for key, node in dependency_data.items()]


def _resolve_dependencies_to_install(
    dependencies_data,
    target,
    host_system,
    dependencies_root,
    build_test,
    build_benchmark,
    version_data
):
    """
    Checks whether or not the dependencies required by the
    project are installed and returns two lists: the first one
    contains the dependencies not requiring installation and the
    second ones requiring.

    dependencies_data -- List of objects of type DependencyData
    that contain the functions for checking and building the
    dependencies.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    build_test -- Whether or not the tests should be built.

    build_benchmark -- Whether or not the benchmarks should be
    built.

    version_data -- The dictionary read from the JSON file containing the
    versions of the currently installed dependencies.
    """
    accumulated_not_to_install = [
        data for data in dependencies_data
        if data.should_install is None or not data.should_install(
            build_test=build_test,
            build_benchmark=build_benchmark,
            dependencies_root=dependencies_root,
            version=data.get_required_version(
                target=target,
                host_system=host_system
            ),
            target=target,
            host_system=host_system,
            installed_version=version_data[data.get_key()]
            if version_data and data.get_key() in version_data else None
        )
    ]
    accumulated_to_install = [
        data for data in dependencies_data
        if data.should_install is not None and data.should_install(
            build_test=build_test,
            build_benchmark=build_benchmark,
            dependencies_root=dependencies_root,
            version=data.get_required_version(
                target=target,
                host_system=host_system
            ),
            target=target,
            host_system=host_system,
            installed_version=version_data[data.get_key()]
            if version_data and data.get_key() in version_data else None
        )
    ]
    return accumulated_not_to_install, accumulated_to_install


def install_dependencies(
    dependencies_data,
    toolchain,
    cmake_generator,
    target,
    host_system,
    build_variant,
    github_user_agent,
    github_api_token,
    opengl_version,
    dependencies_root,
    build_root,
    version_data_file,
    build_test,
    build_benchmark,
    dry_run,
    print_debug
):
    """
    Installs the dependencies of the project.

    dependencies_data -- List of objects of type DependencyData
    that contain the functions for checking and building the
    dependencies.

    toolchain -- The toolchain object of the run.

    cmake_generator -- The name of the generator that CMake
    should use as the build system for which the build scripts
    are generated.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.

    build_variant -- The build variant used to build the project.

    github_user_agent -- The user agent used when accessing the
    GitHub API.

    github_api_token -- The GitHub API token that is used to
    access the API.

    opengl_version -- The version of OpenGL that is used.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    build_root -- The path to the root directory that is used for
    all created files and directories.

    version_data_file -- Path to the JSON file that contains the
    currently installed versions of the dependencies.

    build_test -- Whether or not the tests should be built.

    build_benchmark -- Whether or not the benchmarks should be
    built.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    version_data = {}

    try:
        with open(version_data_file) as json_file:
            version_data = json.load(json_file)
    except Exception:
        logging.debug(
            "The version data file for dependencies wasn't found from path %s",
            version_data_file
        )

    not_to_install, to_install = _resolve_dependencies_to_install(
        dependencies_data=dependencies_data,
        target=target,
        host_system=host_system,
        dependencies_root=dependencies_root,
        build_test=build_test,
        build_benchmark=build_benchmark,
        version_data=version_data
    )

    logging.debug(
        "The dependencies that aren't being installed are: %s",
        ", ".join([data.get_name() for data in not_to_install])
    )

    for dependency in to_install:
        dependency.install_dependency(
            install_info=DependencyInstallInfo(
                toolchain=toolchain,
                cmake_generator=cmake_generator,
                build_root=build_root,
                dependencies_root=dependencies_root,
                version=dependency.get_required_version(
                    target=target,
                    host_system=host_system
                ),
                target=target,
                host_system=host_system,
                build_variant=build_variant,
                github_user_agent=github_user_agent,
                github_api_token=github_api_token,
                opengl_version=opengl_version
            ),
            dry_run=dry_run,
            print_debug=print_debug
        )
        version_data.update({
            dependency.get_key(): dependency.get_required_version(
                target=target,
                host_system=host_system
            )
        })

    with open(version_data_file, "w") as json_file:
        json.dump(version_data, json_file)

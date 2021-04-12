# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the functions related to the
building and finding Google Test.
"""

import logging
import os

from ..github import release

from ..support.cmake_generators import \
    get_visual_studio_16_cmake_generator_name

from ..support.environment import get_temporary_directory

from ..support.github_data import GitHubData

from ..support.platform_names import get_windows_system_name

from ..util.build_util import build_with_cmake

from ..util.cache import cached

from ..util import shell


@cached
def should_add_sources_to_project(host_system):
    """
    Tells whether or not the Google Test sources should be
    included in the build of project. If not, Google Test is
    built as a separate library and linked with the project.

    host_system -- The system this script is run on.
    """
    return host_system == get_windows_system_name()


@cached
def get_dependency_source_directory(dependencies_root):
    """
    Gives the path to the directory where the sources of Google
    Test are located in the dependencies directory.

    dependencies_root -- The root directory of the dependencies
    for the current build target.
    """
    return os.path.join(dependencies_root, "src", "googletest")


def _copy_sources_to_dependencies(
    dependencies_root,
    asset_directory,
    dry_run=None,
    print_debug=None
):
    """
    Copies the Google Test sources to the dependency directory so
    they can be used in the build of the project.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    asset_directory -- The temporary directory where the Google
    Test files are located.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    google_test_dependency_source_dir = get_dependency_source_directory(
        dependencies_root=dependencies_root
    )

    if os.path.isdir(google_test_dependency_source_dir):
        shell.rmtree(
            google_test_dependency_source_dir,
            dry_run=dry_run,
            echo=print_debug
        )

    dependency_source_dir = os.path.dirname(google_test_dependency_source_dir)

    shell.makedirs(dependency_source_dir, dry_run=dry_run, echo=print_debug)
    shell.copytree(
        os.path.join(asset_directory, "googletest"),
        google_test_dependency_source_dir,
        dry_run=dry_run,
        echo=print_debug
    )

    google_test_dependency_include_dir = os.path.join(
        dependencies_root,
        "include",
        "gtest"
    )

    # The headers of Google Test are copied to the same directory
    # where the other dependency header are for clarity.
    if os.path.isdir(google_test_dependency_include_dir):
        shell.rmtree(
            google_test_dependency_include_dir,
            dry_run=dry_run,
            echo=print_debug
        )

    shell.makedirs(
        os.path.join(dependencies_root, "include"),
        dry_run=dry_run,
        echo=print_debug
    )

    shell.copytree(
        os.path.join(asset_directory, "googletest", "include", "gtest"),
        google_test_dependency_include_dir,
        dry_run=dry_run,
        echo=print_debug
    )


def _build(
    toolchain,
    cmake_generator,
    dependencies_root,
    temporary_directory,
    asset_directory,
    target,
    host_system,
    build_variant,
    dry_run=None,
    print_debug=None
):
    """
    Builds and installs the Google Test libraries.

    toolchain -- The toolchain object of the run.

    cmake_generator -- The name of the generator that CMake
    should use as the build system for which the build scripts
    are generated.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    temporary_directory -- The temporary directory used for
    downloading and building Google Test.

    asset_directory -- The temporary directory where the Google
    Test files are located.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.

    build_variant -- The build variant used to build the project.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    build_with_cmake(
        toolchain=toolchain,
        cmake_generator=cmake_generator,
        source_directory=asset_directory,
        temporary_root=temporary_directory,
        dependencies_root=dependencies_root,
        target=target,
        host_system=host_system,
        build_variant=build_variant,
        cmake_options={"BUILD_GMOCK": False},
        msbuild_target="ALL_BUILD.vcxproj",
        dry_run=dry_run,
        print_debug=print_debug
    )

    if cmake_generator == get_visual_studio_16_cmake_generator_name():
        if not os.path.isdir(os.path.join(dependencies_root, "lib")):
            shell.makedirs(
                os.path.join(dependencies_root, "lib"),
                dry_run=dry_run,
                echo=print_debug
            )
        lib_file = os.path.join(dependencies_root, "lib", "gtestd.lib")
        if os.path.exists(lib_file):
            shell.rm(lib_file, dry_run=dry_run, echo=print_debug)
        shell.copy(
            os.path.join(
                temporary_directory,
                "build",
                "lib",
                build_variant,
                "gtestd.lib"
            ),
            lib_file,
            dry_run=dry_run,
            echo=print_debug
        )
        if not os.path.isdir(
            os.path.join(dependencies_root, "include", "gtest")
        ):
            shell.makedirs(
                os.path.join(dependencies_root, "include", "gtest"),
                dry_run=dry_run,
                echo=print_debug
            )
        shell.copytree(
            os.path.join(
                temporary_directory,
                "googletest",
                "googletest",
                "include",
                "gtest"
            ),
            os.path.join(dependencies_root, "include", "gtest"),
            dry_run=dry_run,
            echo=print_debug
        )


################################################################
# DEPENDENCY DATA FUNCTIONS
################################################################


@cached
def should_install(
    dependencies_root,
    version,
    target,
    host_system,
    installed_version
):
    """
    Tells whether the build of the dependency should be skipped.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    version -- The full version number of the dependency.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.

    installed_version -- The version of the dependecy that is
    written to the JSON file containing the currently installed
    versions of the dependencies.
    """
    if not installed_version or version != installed_version:
        return True

    if should_add_sources_to_project(host_system=host_system):
        logging.debug("Checking if the Google Test sources exist")
        return not os.path.isdir(get_dependency_source_directory(
            dependencies_root=dependencies_root
        )) or not os.path.exists(os.path.join(
            get_dependency_source_directory(
                dependencies_root=dependencies_root
            ),
            "CMakeLists.txt"
        ))

    if host_system == get_windows_system_name():
        return not os.path.exists(os.path.join(
            dependencies_root,
            "lib",
            "gtest.lib"
        )) and not os.path.exists(os.path.join(
            dependencies_root,
            "lib",
            "gtestd.lib"
        ))
    else:
        return not os.path.exists(os.path.join(
            dependencies_root,
            "lib",
            "libgtest.a"
        )) and not os.path.exists(os.path.join(
            dependencies_root,
            "lib",
            "libgtestd.a"
        ))


def install_dependency(install_info, dry_run=None, print_debug=None):
    """
    Installs the dependency by downloading and possibly building
    it. Returns the path to the built dependency.

    install_info -- The object containing the install information
    for this tool.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    temp_dir = get_temporary_directory(build_root=install_info.build_root)

    shell.makedirs(temp_dir, dry_run=dry_run, echo=print_debug)

    asset_path = release.download_tag(
        path=temp_dir,
        git=install_info.toolchain.scm,
        github_data=GitHubData(
            owner="google",
            name="googletest",
            tag_name="release-{}".format(install_info.version),
            asset_name=None
        ),
        user_agent=install_info.github_user_agent,
        api_token=install_info.github_api_token,
        host_system=install_info.host_system,
        dry_run=dry_run,
        print_debug=print_debug
    )

    if should_add_sources_to_project(host_system=install_info.host_system):
        _copy_sources_to_dependencies(
            dependencies_root=install_info.dependencies_root,
            asset_directory=asset_path,
            dry_run=dry_run,
            print_debug=print_debug
        )
    else:
        _build(
            toolchain=install_info.toolchain,
            cmake_generator=install_info.cmake_generator,
            dependencies_root=install_info.dependencies_root,
            temporary_directory=temp_dir,
            asset_directory=asset_path,
            target=install_info.target,
            host_system=install_info.host_system,
            build_variant=install_info.build_variant,
            dry_run=dry_run,
            print_debug=print_debug
        )

    shell.rmtree(temp_dir, dry_run=dry_run, echo=print_debug)

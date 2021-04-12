# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the functions related to the
building and finding Google Benchmark.
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
    # if host_system == get_windows_system_name():
    #     return False

    if not installed_version or version != installed_version:
        return True

    if host_system == get_windows_system_name():
        lib_file = os.path.join(dependencies_root, "lib", "benchmark.lib")
        if not os.path.exists(lib_file):
            lib_file = os.path.join(dependencies_root, "lib", "benchmarkd.lib")
            return not os.path.exists(lib_file)
        else:
            return False
    else:
        lib_file = os.path.join(dependencies_root, "lib", "libbenchmark.a")
        if not os.path.exists(lib_file):
            lib_file = os.path.join(
                dependencies_root,
                "lib",
                "libbenchmarkd.a"
            )
            return not os.path.exists(lib_file)
        else:
            return False


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
            name="benchmark",
            tag_name="v{}".format(install_info.version),
            asset_name=None
        ),
        user_agent=install_info.github_user_agent,
        api_token=install_info.github_api_token,
        host_system=install_info.host_system,
        dry_run=dry_run,
        print_debug=print_debug
    )

    build_with_cmake(
        toolchain=install_info.toolchain,
        cmake_generator=install_info.cmake_generator,
        source_directory=asset_path,
        temporary_root=temp_dir,
        dependencies_root=install_info.dependencies_root,
        target=install_info.target,
        host_system=install_info.host_system,
        build_variant=install_info.build_variant,
        cmake_options={"BENCHMARK_ENABLE_GTEST_TESTS": False},
        msbuild_target="ALL_BUILD.vcxproj",
        dry_run=dry_run,
        print_debug=print_debug
    )

    if install_info.cmake_generator == \
            get_visual_studio_16_cmake_generator_name():
        logging.debug("Google Benchmark files will be copied manually")
        build_dir = os.path.join(temp_dir, "build")
        if not os.path.isdir(
            os.path.join(install_info.dependencies_root, "lib")
        ):
            shell.makedirs(
                os.path.join(install_info.dependencies_root, "lib"),
                dry_run=dry_run,
                echo=print_debug
            )
        lib_file = os.path.join(
            install_info.dependencies_root,
            "lib",
            "benchmark.lib"
        )
        lib_file_d = os.path.join(
            install_info.dependencies_root,
            "lib",
            "benchmarkd.lib"
        )
        if os.path.exists(lib_file):
            shell.rm(lib_file, dry_run=dry_run, echo=print_debug)
        if os.path.exists(lib_file_d):
            shell.rm(lib_file_d, dry_run=dry_run, echo=print_debug)
        temp_lib_file = os.path.join(
            build_dir,
            "src",
            install_info.build_variant,
            "benchmark.lib"
        )
        temp_lib_file_d = os.path.join(
            build_dir,
            "src",
            install_info.build_variant,
            "benchmarkd.lib"
        )
        if os.path.exists(temp_lib_file):
            shell.copy(
                temp_lib_file,
                lib_file,
                dry_run=dry_run,
                echo=print_debug
            )
        elif os.path.exists(temp_lib_file_d):
            shell.copy(
                temp_lib_file_d,
                lib_file_d,
                dry_run=dry_run,
                echo=print_debug
            )
        else:
            logging.debug("No built Google Benchmark library was found")

        if not os.path.isdir(
            os.path.join(
                install_info.dependencies_root,
                "include",
                "benchmark"
            )
        ):
            shell.makedirs(
                os.path.join(
                    install_info.dependencies_root,
                    "include",
                    "benchmark"
                ),
                dry_run=dry_run,
                echo=print_debug
            )
        shell.copytree(
            os.path.join(asset_path, "include", "benchmark"),
            os.path.join(
                install_info.dependencies_root,
                "include",
                "benchmark"
            ),
            dry_run=dry_run,
            echo=print_debug
        )

    shell.rmtree(temp_dir, dry_run=dry_run, echo=print_debug)

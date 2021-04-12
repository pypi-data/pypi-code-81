# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the functions related to the
building and finding Ninja.
"""

import os
import stat

from ..github import release

from ..support.environment import get_temporary_directory

from ..support.github_data import GitHubData

from ..support.platform_names import \
    get_darwin_system_name, get_linux_system_name, get_windows_system_name

from ..util.cache import cached

from ..util import shell


def _get_ninja_version_info():
    """
    Gives a tuple containing the version information of Ninja,
    i.e. (major, minor, patch).
    """
    return 1, 10, 0


@cached
def get_required_ninja_version():
    """
    Gives the version of Ninja that is downloaded when the tool
    isn't found.
    """
    return ".".join([str(n) for n in _get_ninja_version_info()])


@cached
def get_local_ninja_executable(tools_root, version, system):
    """
    Gives the path to the local Ninja executable.

    tools_root -- The root directory of the tools for the current
    build target.

    version -- The full Ninja version number.

    system -- The system for which the wanted Ninja build is for.
    """
    def _resolve_executable():
        return os.path.join("bin", "ninja.exe") \
            if system == get_windows_system_name() \
            else os.path.join("bin", "ninja")

    return os.path.join(
        tools_root,
        "ninja",
        version,
        system,
        _resolve_executable()
    )


################################################################
# TOOLDATA FUNCTIONS
################################################################

@cached
def get_tool_type():
    """Returns the type of the tool for the toolchain."""
    return "build_system"


@cached
def get_version(target, host_system):
    """
    Returns a string that represents the version of the tool that
    is downloaded when it isn't found.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.
    """
    return get_required_ninja_version()


@cached
def get_local_executable(tools_root, version, target, host_system):
    """
    Returns path to the local executable of the tool.

    tools_root -- The root directory of the tools for the current
    build target.

    version -- The full version number of the tool.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.
    """
    return get_local_ninja_executable(
        tools_root=tools_root,
        version=version,
        system=host_system
    )


def install_tool(install_info, dry_run=None, print_debug=None):
    """
    Installs the tool by downloading and possibly building it.
    Returns the path to the built tool executable.

    install_info -- The object containing the install information
    for this tool.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    temp_dir = get_temporary_directory(build_root=install_info.build_root)
    tool_temp_dir = os.path.join(temp_dir, "ninja")

    shell.makedirs(temp_dir, dry_run=dry_run, echo=print_debug)
    shell.makedirs(tool_temp_dir, dry_run=dry_run, echo=print_debug)

    def _asset_name(host_system):
        if host_system == get_darwin_system_name():
            return "ninja-mac.zip"
        elif host_system == get_linux_system_name():
            return "ninja-linux.zip"
        elif host_system == get_windows_system_name():
            return "ninja-windows.zip"

    asset_path = release.download_asset(
        path=temp_dir,
        github_data=GitHubData(
            owner="ninja-build",
            name="ninja",
            tag_name="v{}".format(install_info.version),
            asset_name=_asset_name(install_info.host_system)
        ),
        user_agent=install_info.github_user_agent,
        api_token=install_info.github_api_token,
        host_system=install_info.host_system,
        dry_run=dry_run,
        print_debug=print_debug
    )

    shell.tar(asset_path, tool_temp_dir, dry_run=dry_run, echo=print_debug)

    dest_dir = os.path.dirname(get_local_ninja_executable(
        tools_root=install_info.tools_root,
        version=install_info.version,
        system=install_info.host_system
    ))

    if os.path.isdir(dest_dir):
        shell.rmtree(dest_dir, dry_run=dry_run, echo=print_debug)

    shell.makedirs(dest_dir, dry_run=dry_run, echo=print_debug)

    shell.copy(
        os.path.join(
            tool_temp_dir,
            "ninja.exe"
            if install_info.host_system == get_windows_system_name()
            else "ninja"
        ),
        dest_dir,
        dry_run=dry_run,
        echo=print_debug
    )

    shell.rmtree(temp_dir, dry_run=dry_run, echo=print_debug)

    if install_info.host_system == get_darwin_system_name() \
            or install_info.host_system == get_linux_system_name():
        dest_file = get_local_ninja_executable(
            tools_root=install_info.tools_root,
            version=install_info.version,
            system=install_info.host_system
        )
        mode = os.stat(dest_file).st_mode
        os.chmod(dest_file, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    return get_local_ninja_executable(
        tools_root=install_info.tools_root,
        version=install_info.version,
        system=install_info.host_system
    )

# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the functions related to the
building and finding CMake.
"""

import logging
import os

from ..support.environment import get_temporary_directory

from ..support.platform_names import \
    get_darwin_system_name, get_linux_system_name, get_windows_system_name

from ..util.cache import cached

from ..util import http, shell


def _get_cmake_version_info():
    """
    Gives a tuple containing the version information of CMake,
    i.e. (major, minor, patch).
    """
    return 3, 15, 6


@cached
def get_required_cmake_version():
    """
    Gives the version of CMake that is downloaded when the tool
    isn't found.
    """
    return ".".join([str(n) for n in _get_cmake_version_info()])


@cached
def _get_local_cmake_directory(tools_root, version, system):
    """
    Gives the path of the directory containing the local CMake
    files.

    tools_root -- The root directory of the tools for the current
    build target.

    version -- The full CMake version number.

    system -- The system for which the wanted CMake build is for.
    """
    return os.path.join(tools_root, "cmake", version, system)


@cached
def get_local_cmake_executable(tools_root, version, system):
    """
    Gives the path to the local CMake executable.

    tools_root -- The root directory of the tools for the current
    build target.

    version -- The full CMake version number.

    system -- The system for which the wanted CMake build is for.
    """
    def _darwin_app_name(path):
        if not os.path.isdir(path):
            return "CMake.app"
        # This is a workaround to check if there's actually files
        # in the CMake tool directory
        if [f for f in os.listdir(path) if not f.startswith(".")] == []:
            return "CMake.app"
        return [f for f in os.listdir(path) if f.endswith(".app")][0]

    def _resolve_executable(path):
        if system == get_darwin_system_name():
            app_name = _darwin_app_name(path)
            return None if not app_name else os.path.join(
                _darwin_app_name(path),
                "Contents",
                "bin",
                "cmake"
            )
        elif system == get_linux_system_name():
            return os.path.join("bin", "cmake")
        elif system == get_windows_system_name():
            return os.path.join("bin", "cmake.exe")
        raise NotImplementedError

    path = _get_local_cmake_directory(
        tools_root=tools_root,
        version=version,
        system=system
    )

    logging.debug("Looking for the CMake executable from %s", path)

    exec_path = _resolve_executable(path)

    return None if not exec_path else os.path.join(path, exec_path)


@cached
def _resolve_cmake_download_target(version, system):
    """
    Gives the target used in the name of the CMake archive
    downloaded for installation.

    version -- The full version number of CMake.

    system -- The system for which the wanted CMake build is for.
    """
    major_version, minor_version, patch_version = tuple(map(
        int,
        version.split(".")
    ))

    if system == get_darwin_system_name():
        # Starting at CMake 3.1.1 'Darwin-x86_64' variant is
        # available, before that the only option is
        # 'Darwin-universal'.
        if major_version < 3:
            return "Darwin-universal"
        if minor_version <= 1:
            if patch_version < 1:
                return "Darwin-universal"
            return "Darwin-x86_64"
        return "Darwin-x86_64"
    elif system == get_linux_system_name():
        def _resolve_linux():
            # Starting at CMake 3.1.0 'Linux-x86_64' variant is
            # available, before that the only option is
            # 'Linux-i386'.
            if major_version < 3:
                return "Linux-i386"
            if minor_version < 1:
                return "Linux-i386"
            return "Linux-x86_64"
        return _resolve_linux()
    elif system == get_windows_system_name():
        return "win32-x86"


################################################################
# TOOLDATA FUNCTIONS
################################################################

@cached
def get_tool_type():
    """Returns the type of the tool for the toolchain."""
    return "cmake"


@cached
def get_version(target, host_system):
    """
    Returns a string that represents the version of the tool that
    is downloaded when it isn't found.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.
    """
    return get_required_cmake_version()


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
    return get_local_cmake_executable(
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
    tool_temp_dir = os.path.join(temp_dir, "cmake")

    shell.makedirs(temp_dir, dry_run=dry_run, echo=print_debug)
    shell.makedirs(tool_temp_dir, dry_run=dry_run, echo=print_debug)

    major_version, minor_version, patch_version = tuple(map(
        int,
        install_info.version.split(".")
    ))

    url = "https://cmake.org/files/v{major}.{minor}/cmake-" \
        "{major}.{minor}.{patch}-{target}.{archive}".format(
            major=major_version,
            minor=minor_version,
            patch=patch_version,
            target=_resolve_cmake_download_target(
                version=install_info.version,
                system=install_info.host_system
            ),
            archive="zip"
            if install_info.host_system == "Windows"
            else "tar.gz"
        )
    dest = os.path.join(
        tool_temp_dir,
        "cmake.{}".format(
            "zip" if install_info.host_system == "Windows" else "tar.gz"
        )
    )

    http.stream(
        url=url,
        destination=dest,
        host_system=install_info.host_system,
        dry_run=dry_run,
        print_debug=print_debug
    )
    shell.tar(dest, tool_temp_dir, dry_run=dry_run, echo=print_debug)

    subdir = "cmake-{version}-{target}".format(
        version=install_info.version,
        target=_resolve_cmake_download_target(
            version=install_info.version,
            system=install_info.host_system
        )
    )

    local_dir = _get_local_cmake_directory(
        tools_root=install_info.tools_root,
        version=install_info.version,
        system=install_info.host_system
    )

    if os.path.isdir(local_dir):
        shell.rmtree(local_dir, dry_run=dry_run, echo=print_debug)

    shell.copytree(
        os.path.join(tool_temp_dir, subdir),
        local_dir,
        dry_run=dry_run,
        echo=print_debug
    )
    shell.rmtree(temp_dir, dry_run=dry_run, echo=print_debug)

    return get_local_executable(
        tools_root=install_info.tools_root,
        version=install_info.version,
        target=install_info.target,
        host_system=install_info.host_system
    )

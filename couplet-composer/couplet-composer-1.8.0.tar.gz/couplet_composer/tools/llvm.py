# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the functions related to the
building and finding LLVM.
"""

import os

import distro

from ..github import release

from ..support.environment import get_temporary_directory

from ..support.github_data import GitHubData

from ..support.platform_names import \
    get_darwin_system_name, get_linux_system_name, get_windows_system_name

from ..util.cache import cached

from ..util import shell


def _get_llvm_version_info():
    """
    Gives a tuple containing the version information of LLVM,
    i.e. (major, minor, patch).
    """
    return 10, 0, 0


@cached
def get_required_version():
    """
    Gives the version of LLVM that is downloaded when it isn't
    found.
    """
    return ".".join([str(n) for n in _get_llvm_version_info()])


@cached
def get_local_path(tools_root, version, system):
    """
    Gives the path to the local LLVM tool executables.

    tools_root -- The root directory of the tools for the current
    build target.

    version -- The full LLVM version number.

    system -- The system for which the wanted clang build is for.
    """
    return os.path.join(tools_root, "llvm", version, system)


@cached
def get_local_executable(tools_root, version, system, tool_name):
    """
    Gives the path to one of the local LLVM tool executables.

    tools_root -- The root directory of the tools for the current
    build target.

    version -- The full LLVM version number.

    system -- The system for which the wanted clang build is for.

    tool_name -- The name of the LLVM tool.
    """
    return os.path.join(
        get_local_path(tools_root=tools_root, version=version, system=system),
        "bin",
        tool_name
    )


def install_tool(install_info, tool_name, dry_run=None, print_debug=None):
    """
    Installs the LLVM tool by downloading and possibly building
    them. Returns the path to the built tool executable of the
    tool where the installation was made.

    This function does also check whether the LLVM tools are
    already built locally.

    Currently the only supported platforms for which LLVM can be
    installed are macOS and Ubuntu.

    install_info -- The object containing the install information
    for this tool.

    tool_name -- The name of the LLVM tool.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    # Don't build the tools if they're already installed.
    local_exe = get_local_executable(
        tools_root=install_info.tools_root,
        version=install_info.version,
        system=install_info.host_system,
        tool_name=tool_name
    )

    if os.path.exists(local_exe):
        return local_exe

    # Make sure that the current platform is supported.
    if install_info.host_system == get_windows_system_name():
        return None
    elif install_info.host_system == get_linux_system_name():
        if "ubuntu" != distro.id():
            return None

    temp_dir = get_temporary_directory(build_root=install_info.build_root)
    tool_temp_dir = os.path.join(temp_dir, "llvm")

    shell.makedirs(temp_dir, dry_run=dry_run, echo=print_debug)
    shell.makedirs(tool_temp_dir, dry_run=dry_run, echo=print_debug)

    def _asset_name(host_system, version, target):
        if host_system == get_darwin_system_name():
            return "clang+llvm-{version}-{arch}-darwin-apple".format(
                version=version,
                arch=target.machine
            )
        elif host_system == get_linux_system_name():
            return ("clang+llvm-{version}-{arch}-linux-gnu-{id}-"
                    "{sysver}".format(
                        version=version,
                        arch=target.machine,
                        id=distro.id(),
                        sysver=distro.version()
                    ))

    asset_name = _asset_name(
        host_system=install_info.host_system,
        version=install_info.version,
        target=install_info.target
    )

    asset_path = release.download_asset(
        path=temp_dir,
        github_data=GitHubData(
            owner="llvm",
            name="llvm-project",
            tag_name="llvmorg-{}".format(install_info.version),
            asset_name="{}.tar.xz".format(asset_name)
        ),
        user_agent=install_info.github_user_agent,
        api_token=install_info.github_api_token,
        host_system=install_info.host_system,
        dry_run=dry_run,
        print_debug=print_debug
    )

    shell.tar(asset_path, tool_temp_dir, dry_run=dry_run, echo=print_debug)

    local_dir = get_local_path(
        tools_root=install_info.tools_root,
        version=install_info.version,
        system=install_info.host_system
    )

    if os.path.isdir(local_dir):
        shell.rmtree(local_dir, dry_run=dry_run, echo=print_debug)

    shell.copytree(
        os.path.join(tool_temp_dir, asset_name),
        local_dir,
        dry_run=dry_run,
        echo=print_debug
    )
    shell.rmtree(temp_dir, dry_run=dry_run, echo=print_debug)

    return local_exe

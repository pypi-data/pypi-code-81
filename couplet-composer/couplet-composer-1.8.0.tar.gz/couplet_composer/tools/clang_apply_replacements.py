# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the functions related to the
building and finding clang-apply-replacements.
"""

from ..util.cache import cached

from . import llvm


################################################################
# TOOLDATA FUNCTIONS
################################################################

@cached
def get_version(target, host_system):
    """
    Returns a string that represents the version of the tool that
    is downloaded when it isn't found.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.
    """
    return llvm.get_required_version()


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
    return llvm.get_local_executable(
        tools_root=tools_root,
        version=version,
        system=host_system,
        tool_name="clang-apply-replacements"
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
    return llvm.install_tool(
        install_info=install_info,
        tool_name="clang-apply-replacements",
        dry_run=dry_run,
        print_debug=print_debug
    )

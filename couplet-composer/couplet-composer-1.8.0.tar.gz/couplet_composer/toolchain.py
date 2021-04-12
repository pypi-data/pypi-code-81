# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the functions for resolving and
building the toolchain required to build the project that this
script acts on.
"""

from collections import namedtuple

import logging
import os

from .support.platform_names import \
    get_darwin_system_name, get_linux_system_name, get_windows_system_name

from .support.tool_data import CompilerToolPair, list_tool_types

from .support.tool_install_information import ToolInstallInfo

from .util.where import where

from .util.which import which

from .util import xcrun


# The type 'Toolchain' represents the toolchain for the script.
# The tools in the toolchain are following: TODO
Toolchain = namedtuple("Toolchain", list_tool_types())


def _find_tool(tool, host_system):
    """
    Looks for a tool on the system and returns the path to the
    tool if it was found.

    tool -- The tool to look for.

    host_system -- The name of the system this script is run on.
    """
    if host_system == get_darwin_system_name():
        return xcrun.find(tool)
    elif host_system == get_linux_system_name():
        return which(tool)
    elif host_system == get_windows_system_name():
        return where(tool)
    else:
        return None


def _resolve_tools_on_system(tools_data, host_system):
    """
    Checks whether or not the tools required by this run of the
    script exist on the host system and returns two dictionaries:
    the first one contains the found tools and the second one the
    missing tools.

    tools_data -- List of objects of type ToolData that contain
    the functions for checking and building the tools.

    host_system -- The system this script is run on.
    """
    found = {}
    missing = {}

    for key, tool_data in tools_data.items():
        if isinstance(tool_data, CompilerToolPair):
            logging.debug(
                "Looking for %s toolchain on the system",
                tool_data.get_tool_name()
            )

            found_tool = {}

            logging.debug(
                "Looking for %s on the system",
                tool_data.cc.get_tool_name()
            )

            found_cc = None

            if tool_data.cc.use_predefined_path() and \
                    os.path.exists(tool_data.cc.get_searched_tool()):
                found_cc = tool_data.cc.get_searched_tool()
            else:
                found_cc = _find_tool(
                    tool=tool_data.cc.get_searched_tool(),
                    host_system=host_system
                )

            found_cxx = None

            if tool_data.cxx.use_predefined_path() and \
                    os.path.exists(tool_data.cxx.get_searched_tool()):
                found_cxx = tool_data.cxx.get_searched_tool()
            else:
                found_cxx = _find_tool(
                    tool=tool_data.cxx.get_searched_tool(),
                    host_system=host_system
                )

            if found_cc and found_cxx:
                logging.debug("Found %s and %s", found_cc, found_cxx)
                found_tool.update({"cc": found_cc, "cxx": found_cxx})
                found.update({key: found_tool})
            else:
                logging.debug(
                    "%s toolchain wasn't found",
                    tool_data.get_tool_name()
                )
                missing.update({key: tool_data})

        else:
            logging.debug(
                "Looking for %s on the system",
                tool_data.get_tool_name()
            )

            found_tool = None

            if tool_data.use_predefined_path() and \
                    os.path.exists(tool_data.get_searched_tool()):
                found_tool = tool_data.get_searched_tool()
            else:
                found_tool = _find_tool(
                    tool=tool_data.get_searched_tool(),
                    host_system=host_system
                )

            if found_tool:
                logging.debug("Found %s", found_tool)
                found.update({key: found_tool})
            else:
                logging.debug("%s wasn't found", tool_data.get_searched_tool())
                missing.update({key: tool_data})

    return found, missing


def _resolve_local_tools(
    missing_tools_data,
    cmake_generator,
    target,
    host_system,
    tools_root
):
    """
    Checks whether or not the tools required by this run of the
    script exist locally and returns two dictionaries: the first
    one contains the found tools and the second one the missing
    tools.

    missing_tools_data -- List of objects of type ToolData that
    contain the functions for checking and building the tools
    that aren't found yet.

    cmake_generator -- The name of the generator that CMake
    should use as the build system for which the build scripts
    are generated. It's used to determine which build system is
    checked for and built if necessary.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.

    tools_root -- The root directory of the tools for the current
    build target.
    """
    found = {}
    missing = {}

    for key, tool_data in missing_tools_data.items():
        if isinstance(tool_data, CompilerToolPair):
            logging.debug(
                "Looking for %s toolchain from the local tools",
                tool_data.get_tool_name()
            )

            found_tool = {}

            logging.debug(
                "Looking for %s from the local tools",
                tool_data.cc.get_tool_name()
            )

            found_cc = None

            local_cc_exe = tool_data.cc.get_local_executable(
                tools_root=tools_root,
                version=tool_data.cc.get_required_local_version(
                    target=target,
                    host_system=host_system
                ),
                target=target,
                host_system=host_system
            )

            if local_cc_exe and os.path.exists(local_cc_exe):
                found_cc = local_cc_exe

            found_cxx = None

            local_cxx_exe = tool_data.cxx.get_local_executable(
                tools_root=tools_root,
                version=tool_data.cxx.get_required_local_version(
                    target=target,
                    host_system=host_system
                ),
                target=target,
                host_system=host_system
            )

            if local_cxx_exe and os.path.exists(local_cxx_exe):
                found_cxx = local_cxx_exe

            if found_cc and found_cxx:
                logging.debug("Found %s and %s", found_cc, found_cxx)
                found_tool.update({"cc": found_cc, "cxx": found_cxx})
                found.update({key: found_tool})
            else:
                logging.debug(
                    "%s toolchain wasn't found",
                    tool_data.get_tool_name()
                )
                missing.update({key: tool_data})

        else:
            logging.debug(
                "Looking for %s from the local tools",
                tool_data.get_tool_name()
            )

            found_tool = None

            local_exe = tool_data.get_local_executable(
                tools_root=tools_root,
                version=tool_data.get_required_local_version(
                    target=target,
                    host_system=host_system
                ),
                target=target,
                host_system=host_system
            )

            if local_exe and os.path.exists(local_exe):
                found_tool = local_exe

            if found_tool:
                logging.debug("Found %s", found_tool)
                found.update({key: found_tool})
            else:
                logging.debug("%s wasn't found", tool_data.get_searched_tool())
                missing.update({key: tool_data})

    return found, missing


def _install_missing_tools(
    missing_tools_data,
    build_root,
    tools_root,
    target,
    host_system,
    github_user_agent,
    github_api_token,
    dry_run,
    print_debug
):
    """
    Installs the missing tools and returns two dictionaries: the
    first one contains the successfully installed tools and the
    second one the missing tools.

    missing_tools_data -- List of objects of type ToolData that
    contain the functions for checking and building the tools
    that aren't found yet.
    build_root -- The path to the root directory that is used for
    all created files and directories.

    tools_root -- The root directory of the tools for the current
    build target.

    target -- The target system of the build represented by a
    Target.

    host_system -- The name of the system this script is run on.

    github_user_agent -- The user agent used when accessing the
    GitHub API.

    github_api_token -- The GitHub API token that is used to
    access the API.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    def _install_tool(
        tool_data,
        build_root,
        tools_root,
        target,
        host_system,
        github_user_agent,
        github_api_token,
        dry_run,
        print_debug
    ):
        """
        Installs the given missing tool.

        tool_data -- The tool to install.

        build_root -- The path to the root directory that is used for
        all created files and directories.

        tools_root -- The root directory of the tools for the current
        build target.

        target -- The target system of the build represented by a
        Target.

        host_system -- The name of the system this script is run on.

        github_user_agent -- The user agent used when accessing the
        GitHub API.

        github_api_token -- The GitHub API token that is used to
        access the API.

        dry_run -- Whether the commands are only printed instead of
        running them.

        print_debug -- Whether debug output should be printed.
        """
        version = tool_data.get_required_local_version(
            target=target,
            host_system=host_system
        )
        if tool_data.install_tool is not None:
            tool_path = tool_data.install_tool(
                install_info=ToolInstallInfo(
                    build_root=build_root,
                    tools_root=tools_root,
                    version=version,
                    target=target,
                    host_system=host_system,
                    github_user_agent=github_user_agent,
                    github_api_token=github_api_token
                ),
                dry_run=dry_run,
                print_debug=print_debug
            )
            return tool_path
        else:
            return None

    installed = {}
    missing = {}

    for key, tool_data in missing_tools_data.items():
        if isinstance(tool_data, CompilerToolPair):
            logging.debug("Installing %s toolchain", tool_data.get_tool_name())

            installed_tool = {}

            logging.debug("Installing %s", tool_data.cc.get_tool_name())

            installed_cc = _install_tool(
                tool_data=tool_data.cc,
                build_root=build_root,
                tools_root=tools_root,
                target=target,
                host_system=host_system,
                github_user_agent=github_user_agent,
                github_api_token=github_api_token,
                dry_run=dry_run,
                print_debug=print_debug
            )

            installed_cxx = _install_tool(
                tool_data=tool_data.cxx,
                build_root=build_root,
                tools_root=tools_root,
                target=target,
                host_system=host_system,
                github_user_agent=github_user_agent,
                github_api_token=github_api_token,
                dry_run=dry_run,
                print_debug=print_debug
            )

            if installed_cc and installed_cxx:
                logging.debug(
                    "Installed %s and %s",
                    installed_cc,
                    installed_cxx
                )
                installed_tool.update({
                    "cc": installed_cc,
                    "cxx": installed_cxx
                })
                installed.update({key: installed_tool})
            else:
                logging.debug(
                    "%s toolchain wasn't installed",
                    tool_data.get_tool_name()
                )
                missing.update({key: tool_data})

        else:
            logging.debug("Installing %s", tool_data.get_tool_name())

            installed_tool = _install_tool(
                tool_data=tool_data,
                build_root=build_root,
                tools_root=tools_root,
                target=target,
                host_system=host_system,
                github_user_agent=github_user_agent,
                github_api_token=github_api_token,
                dry_run=dry_run,
                print_debug=print_debug
            )

            if installed_tool:
                logging.debug("Installed %s", installed_tool)
                installed.update({key: installed_tool})
            else:
                logging.debug("%s wasn't installed", tool_data.get_tool_name())
                missing.update({key: tool_data})

    return installed, missing


def _construct_toolchain(found_tools):
    """
    Creates a toolchain object from the found tools for the run.

    found_tools -- A dictionary containing the found tools. The
    key is the type of the tool that matches the type in the
    toolchain and the value is the path to the executable of the
    tool.
    """
    tool_dictionary = {}

    for key in list_tool_types():
        tool_dictionary[key] = None if key not in found_tools \
            else found_tools[key]

    return Toolchain(**tool_dictionary)


def create_toolchain(
    tools_data,
    cmake_generator,
    target,
    host_system,
    github_user_agent,
    github_api_token,
    tools_root,
    build_root,
    read_only,
    dry_run,
    print_debug
):
    """
    Creates the toolchain for this run. This function isn't pure
    as it reads files, calls shell commands, and downloads and
    builds the required tools if they're missing.

    This currently supports only downloading and building CMake
    and Ninja if they're missing from the system. Ninja isn't
    even required for the builds. Other tools, like compilers,
    must be presents.

    Returns a named tuple of type 'Toolchain' that contains the
    tool executables that are used.

    tools_data -- List of objects of type ToolData that contain
    the functions for checking and building the tools.

    cmake_generator -- The name of the generator that CMake
    should use as the build system for which the build scripts
    are generated. It's used to determine which build system is
    checked for and built if necessary.

    target -- The target system of the build represented by a
    Target.

    host_system -- The system this script is run on.

    github_user_agent -- The user agent used when accessing the
    GitHub API.

    github_api_token -- The GitHub API token that is used to
    access the API.

    tools_root -- The root directory of the tools for the current
    build target.

    build_root -- The path to the root directory that is used for
    all created files and directories.

    read_only -- Whether the creation of the toolchain is read
    only. It's read only when the script is run in composing mode
    instead of configuring mode.

    dry_run -- Whether the commands are only printed instead of
    running them.

    print_debug -- Whether debug output should be printed.
    """
    # The function contains internal non-pure element as this
    # dictionary is modified when new tools are resolved. It's
    # done this way for simplicity.
    found_tools, missing_tools = _resolve_tools_on_system(
        tools_data=tools_data,
        host_system=host_system
    )

    # Check if a correct local copy of the tool exists.
    found_local_tools, missing_local_tools = _resolve_local_tools(
        missing_tools_data=missing_tools,
        cmake_generator=cmake_generator,
        target=target,
        host_system=host_system,
        tools_root=tools_root
    )

    if found_local_tools:
        logging.debug(
            "The tools found locally are:\n%s",
            "\n".join([tool for tool in found_local_tools.values()])
        )
    else:
        logging.debug("No tools were found locally")

    # Add the found local tools to the dictionary.
    found_tools.update(found_local_tools)

    # Install the missing tools.
    if not read_only:
        installed_tools, missing_after_installation = _install_missing_tools(
            missing_tools_data=missing_local_tools,
            build_root=build_root,
            tools_root=tools_root,
            target=target,
            host_system=host_system,
            github_user_agent=github_user_agent,
            github_api_token=github_api_token,
            dry_run=dry_run,
            print_debug=print_debug
        )

        # Add the installed tools to the dictionary.
        found_tools.update(installed_tools)

        logging.debug(
            "The tools that are still missing after installing the missing "
            "tools are %s",
            ", ".join(missing_after_installation.keys())
        )

    return _construct_toolchain(found_tools=found_tools)

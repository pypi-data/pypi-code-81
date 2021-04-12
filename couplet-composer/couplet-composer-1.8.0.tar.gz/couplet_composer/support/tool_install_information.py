# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""
This support module contains type ToolInstallInfo for passing the
data required to install a tool.
"""

from collections import namedtuple


# The type 'ToolInstallInfo' represents the data to install a
# tool.
#
# build_root -- The path to the root directory that is used for
# all created files and directories.
#
# tools_root -- The root directory of the tools for the current
# build target.
#
# version -- The full version number of the tool.
#
# target -- The target system of the build represented by a
# Target.
#
# host_system -- The system this script is run on.
#
# github_user_agent -- The user agent used when accessing the
# GitHub API.
#
# github_api_token -- The GitHub API token that is used to access
# the API.
ToolInstallInfo = namedtuple("ToolInstallInfo", [
    "build_root",
    "tools_root",
    "version",
    "target",
    "host_system",
    "github_user_agent",
    "github_api_token"
])

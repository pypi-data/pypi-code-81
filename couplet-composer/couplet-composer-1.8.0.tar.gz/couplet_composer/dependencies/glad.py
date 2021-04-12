# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the functions related to the
building and finding Glad.
"""

import os
import sys

from ..github import tag

from ..support.environment import get_temporary_directory

from ..support.github_data import GitHubData

from ..util.cache import cached

from ..util import shell

from . import _common


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
    return _common.should_install(
        path=os.path.join("src", "glad.c"),
        dependencies_root=dependencies_root,
        version=version,
        installed_version=installed_version
    )


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

    asset_path = tag.download_tag(
        path=temp_dir,
        git=install_info.toolchain.scm,
        github_data=GitHubData(
            owner="Dav1dde",
            name="glad",
            tag_name="v{}".format(install_info.version),
            asset_name=None
        ),
        user_agent=install_info.github_user_agent,
        api_token=install_info.github_api_token,
        host_system=install_info.host_system,
        dry_run=dry_run,
        print_debug=print_debug
    )

    with shell.pushd(asset_path, dry_run=dry_run, echo=print_debug):
        shell.call(
            [
                sys.executable,
                "-m",
                "glad",
                "--profile=core",
                "--api=gl={}".format(install_info.opengl_version),
                "--generator=c-debug",
                "--spec=gl",
                "--out-path={}".format(install_info.dependencies_root)
            ],
            dry_run=dry_run,
            echo=print_debug
        )

    shell.rmtree(temp_dir, dry_run=dry_run, echo=print_debug)

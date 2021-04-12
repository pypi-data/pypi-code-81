# Copyright (c) 2020 Antti Kivi
# Licensed under the MIT License

"""
This support module contains the common functions related to the
building and finding dependencies.
"""

import os

from ..util.cache import cached


@cached
def should_install(path, dependencies_root, version, installed_version):
    """
    Tells whether the build of the dependency should be skipped.

    path -- The relative path from the dependency root to the
    file to check.

    dependencies_root -- The root directory of the dependencies
    for the current build target.

    version -- The full version number of the dependency.

    installed_version -- The version of the dependecy that is
    written to the JSON file containing the currently installed
    versions of the dependencies.
    """
    if not installed_version or version != installed_version:
        return True

    return not os.path.exists(os.path.join(dependencies_root, path))

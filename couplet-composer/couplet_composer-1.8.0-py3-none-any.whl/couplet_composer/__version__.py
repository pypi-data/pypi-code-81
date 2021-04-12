# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
The version data of Couplet Composer. The version number is given
according to Semantic Versioning.
"""

import os


def get_release_version():
    """
    Gives the current release version data of Couplet Composer
    and, thus, returns three values: the major version number,
    the minor version number, and the patch version number.
    """
    return 1, 8, 0


_VERSION_SUFFIX = ""


__version__ = "{}{}".format(
    ".".join([str(n) for n in get_release_version()]),
    _VERSION_SUFFIX
)


if __name__ == "__main__":
    print(__version__)

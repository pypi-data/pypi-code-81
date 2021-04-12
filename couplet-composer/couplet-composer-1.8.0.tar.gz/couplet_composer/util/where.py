# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""
This module contains helper for finding executables on Windows.
"""

import sys

from .cache import cached

from . import shell


@cached
def where(command):
    """
    Returns path to an executable which would be run if the given
    command was called. If no command would be called, returns
    None.

    Python 3.3+ provides this behaviour via the shutil.which()
    function; see:
    https://docs.python.org/3.3/library/shutil.html#shutil.which

    We provide our own implementation because shutil.which() has
    not been backported to Python 2.7, which we support.
    """
    if sys.version_info[0] >= 3:
        import shutil
        return shutil.which(command)
    out = shell.capture(
        ["where.exe", command],
        dry_run=False,
        echo=False,
        optional=True
    )
    return out.rstrip() if out is not None else None

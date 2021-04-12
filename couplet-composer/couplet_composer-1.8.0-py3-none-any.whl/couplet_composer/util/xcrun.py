# Copyright (c) 2019 Antti Kivi
# Licensed under the MIT License

"""This utility module has the xcrun helpers."""

from .cache import cached

from . import shell


@cached
def find(command):
    """
    Returns the path for the given tool according to
    'xcrun --find'. If 'xcrun --find' cannot find the tool,
    return None. This function isn't pure.

    command -- The tool to be searched for.
    """
    command_to_run = ["xcrun", "--find", command]
    # "xcrun --find" prints to stderr when it fails to find the
    # given tool. TODO We swallow that output with a pipe.
    out = shell.capture(
        command_to_run,
        stderr=shell.get_dev_null(),
        dry_run=False,
        echo=False,
        optional=True
    )
    if out is None:
        return None
    return out.rstrip()

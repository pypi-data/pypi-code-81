"""CLI utilities for the VSCode wrapper and utility tool."""

# Standard library:
from os.path import isfile

# 3rd party:
import click

# local:
from jarpyvscode.log import logger


def check_if_file_exists(
    ctx: click.Context,  # noqa: U100, needed when passed as callback to @click.argument
    passed_file_path: str,
):
    """Implement callback for the CLI sub command 'launch'.

    This callback checks, if the string ``passed_arg`` passed to
    ``vscode.py`` launch points to an existing file.

    Returns
    -------
    bool
        True, if *passed_file_path* points to an existing file.
        False, otherwise.

    """
    if passed_file_path is None:
        return passed_file_path
    if not isfile(passed_file_path):
        logger.warning(f"Cannot find a file '{passed_file_path}'!")
        return None
    return passed_file_path

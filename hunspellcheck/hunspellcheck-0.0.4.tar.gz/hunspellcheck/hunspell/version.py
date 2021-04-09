"""Utilities related with Hunspell versions."""

import os
import re
import subprocess


def get_hunspell_version(hunspell=True, ispell=True):
    """Returns the number of version of Hunspell and the version of Ispell
    that the installed Hunspell program is using.

    Args:
        hunspell (bool): Include the version of Hunspell in the response.
        ispell (bool): Include the version of Ispell in the response.

    Returns:
        dict: Their fields would be `hunspell` and `ispell`, if both included
            using the kwargs of this function.
    """
    if not hunspell and not ispell:
        raise ValueError(
            "At least one of optional arguments 'hunspell' or 'ispell' must be true."
        )

    previous_env_lang = os.environ.get("LANG", None)
    os.environ["LANG"] = "C"

    output = subprocess.run(
        ["hunspell", "--version"],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )

    if previous_env_lang is None:
        del os.environ["LANG"]
    else:
        os.environ["LANG"] = previous_env_lang

    version_line = output.stdout.splitlines()[0]

    response = {}

    if hunspell:
        response["hunspell"] = re.search(
            r"Hunspell\s([^\n\s)]+)",
            version_line,
        ).group(1)

    if ispell:
        response["ispell"] = re.search(
            r"Ispell\s(Version)?\s([^\n\s]+)", version_line
        ).group(2)
    return response

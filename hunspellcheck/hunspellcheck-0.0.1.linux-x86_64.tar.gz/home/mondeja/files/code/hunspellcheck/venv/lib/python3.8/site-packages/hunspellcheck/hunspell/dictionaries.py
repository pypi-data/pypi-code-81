"""Utilities about Hunspell dictionaries."""

import os
import subprocess
import sys


def gen_available_dictionaries(full_paths=False):
    """Generates the available dictionaries contained inside the search paths
    configured by hunspell.

    These dictionaries can be used without specify the full path to their
    location in the system calling hunspell, only their name is needed.

    Args:
        full_paths (bool): Yield complete paths to dictionaries (``True``) or
            their names only (``False``).
    """
    previous_env_lang = os.environ.get("LANG", "")
    os.environ["LANG"] = "C"

    output = subprocess.run(
        ["hunspell", "-D"],
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    os.environ["LANG"] = previous_env_lang

    _inside_available_dictionaries = False
    for line in output.stderr.splitlines():
        if _inside_available_dictionaries:
            yield line if full_paths else os.path.basename(line)
        elif line.startswith("AVAILABLE DICTIONARIES"):
            _inside_available_dictionaries = True


def list_available_dictionaries(**kwargs):
    """Convenient wrapper around the generator
    :py:func:`hunspellcheck.hunspell.dictionaries.gen_available_dictionaries`
    which returns the dictionary names in a list."""
    return list(gen_available_dictionaries(**kwargs))


def print_available_dictionaries(sort=True, stream=sys.stdout, **kwargs):
    """Prints into an stream the available hunspell dictionaries.

    By default are printed to the standard output of the system (STDOUT).

    Args:
        sort (bool): Indicates if the dictionaries will be printed in
            alphabetical order.
        stream (object): Stream to which the dictionaries will be printed.
            Must be any object that accepts a `write` method.
    """
    if sort:
        dictionaries_iter = sorted(list_available_dictionaries(**kwargs))
    else:
        dictionaries_iter = gen_available_dictionaries(**kwargs)

    for dictname in dictionaries_iter:
        stream.write(f"{dictname}\n")


def gen_available_dictionaries_with_langcodes(sort=True, **kwargs):
    dictionaries_iter = gen_available_dictionaries(**kwargs)
    if sort:
        dictionaries_iter = sorted(dictionaries_iter)
    unique_locales = []
    for dictname in dictionaries_iter:
        if "_" in dictname:
            locale = dictname.split("_")[0]
            if locale not in unique_locales:
                unique_locales.append(locale)
                yield locale
        yield dictname

"""Utilities about Hunspell dictionaries."""

import os
import subprocess
import sys

from babel import Locale

from hunspellcheck.exceptions import InvalidLanguageDictionaryError


def gen_available_dictionaries(full_paths=False):
    """Generates the available dictionaries contained inside the search paths
    configured by hunspell.

    These dictionaries can be used without specify the full path to their
    location in the system calling hunspell, only their name is needed.

    Args:
        full_paths (bool): Yield complete paths to dictionaries (``True``) or
            their names only (``False``).

    Yields:
        str: Dictionary names (locale with territory).
    """
    previous_env_lang = os.environ.get("LANG", None)
    os.environ["LANG"] = "C"

    output = subprocess.run(
        ["hunspell", "-D"],
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    if previous_env_lang is None:
        del os.environ["LANG"]
    else:
        os.environ["LANG"] = previous_env_lang

    _inside_available_dictionaries = False
    for line in output.stderr.splitlines():
        if _inside_available_dictionaries:
            yield line if full_paths else os.path.basename(line)
        elif line.startswith("AVAILABLE DICTIONARIES"):
            _inside_available_dictionaries = True


def list_available_dictionaries(full_paths=False):
    """Convenient wrapper around the generator
    :py:func:`hunspellcheck.gen_available_dictionaries`
    which returns the dictionary names in a list.

    Args:
        full_paths (bool): Print complete paths to dictionaries (``True``) or
            their names only (``False``).

    Returns:
        list: Available installed dictionaries.
    """
    return list(gen_available_dictionaries(full_paths=full_paths))


def print_available_dictionaries(sort=True, stream=sys.stdout, full_paths=False):
    """Prints into an stream the available hunspell dictionaries.

    By default are printed to the standard output of the system (STDOUT).

    Args:
        sort (bool): Indicates if the dictionaries will be printed in
            alphabetical order.
        stream (object): Stream to which the dictionaries will be printed.
            Must be any object that accepts a `write` method.
        full_paths (bool): Print complete paths to dictionaries (``True``) or
            their names only (``False``).
    """
    if sort:
        dictionaries_iter = sorted(list_available_dictionaries(full_paths=full_paths))
    else:
        dictionaries_iter = gen_available_dictionaries(full_paths=full_paths)

    for dictname in dictionaries_iter:
        stream.write(f"{dictname}\n")


def gen_available_dictionaries_with_langcodes(sort=True, full_paths=False):
    """Generates all available dictionaries installed along with their
    locale names (without territories).

    For example, if `es_ES` is installed, `es` also will be included
    in the response.

    Args:
        sort (bool): Sort languages alfabetically.

    Yields:
        str: Locale or dictionary names (locale with territory).
    """
    dictionaries_iter = gen_available_dictionaries(full_paths=full_paths)
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


def is_valid_dictionary_language(dictionary_name, negotiate_languages=False):
    """Check if a dictionary name is a valid dictionary installed
    for your Hunspell version.

    Args:
        dictionary_name (str): Dictionary language.
        negotiate_languages (bool): Enable language negotiation from locale
            name to territory.

    Returns:
        tuple: Has 3 values:

        - The first value is a boolean and indicates if the language is valid.
        - The second value is the dictionary language name, which could be
          changed from the input is language negotation is enabled.
        - The third value is a list with all available dictionaries.
    """
    available_dictionaries = list_available_dictionaries()
    if dictionary_name not in available_dictionaries:
        if negotiate_languages:
            dictionary_name = str(
                Locale.negotiate([dictionary_name], available_dictionaries)
            )
        else:
            return (False, None, available_dictionaries)
    return (True, dictionary_name, available_dictionaries)


def is_valid_dictionary_language_or_filename(value, negotiate_languages=False):
    """Returns if a value is a valid dictionary language name or an existent
    file defined by their path.

    Args:
        value (str): Dictionary language or filepath.
        negotiate_languages (bool): Enable language negotiation from locale
            name to territory.

    Returns:
        bool: Indicates if is a valid dictionary supported by Hunspell.
    """
    if os.path.isfile(value):
        return True
    is_valid, *_ = is_valid_dictionary_language(
        value,
        negotiate_languages=negotiate_languages,
    )
    return is_valid


def assert_is_valid_dictionary_language_or_filename(
    value,
    negotiate_languages=False,
):
    """Asserts if a value is a valid dictionary language name or an existent
    file defined by their path. If is not, raises an
    :py:class:`hunspellcheck.InvalidLanguageDictionaryError`.

    Args:
        value (str, list): Dictionary language/s or filepath/s.
        negotiate_languages (bool): Enable language negotiation from locale
            name to territory.
    """
    if isinstance(value, str):
        if not is_valid_dictionary_language_or_filename(
            value,
            negotiate_languages=negotiate_languages,
        ):
            raise InvalidLanguageDictionaryError(value)
    else:
        for language in value:
            if not is_valid_dictionary_language_or_filename(
                language,
                negotiate_languages=negotiate_languages,
            ):
                raise InvalidLanguageDictionaryError(value)

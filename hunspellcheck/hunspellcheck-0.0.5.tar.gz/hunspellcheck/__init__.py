"""Hunspellcheck package."""

from hunspellcheck.cli import hunspellchecker_argument_parser
from hunspellcheck.exceptions import InvalidLanguageDictionaryError
from hunspellcheck.hunspell.dictionaries import (
    assert_is_valid_dictionary_language_or_filename,
    gen_available_dictionaries,
    gen_available_dictionaries_with_langcodes,
    is_valid_dictionary_language,
    is_valid_dictionary_language_or_filename,
    list_available_dictionaries,
    print_available_dictionaries,
)
from hunspellcheck.hunspell.version import get_hunspell_version
from hunspellcheck.spellchecker import (
    HunspellChecker,
    looks_like_a_word,
    render_hunspell_word_error,
)


__version__ = "0.0.5"
__title__ = "hunspellcheck"
__all__ = (
    "HunspellChecker",
    "InvalidLanguageDictionaryError",
    "hunspellchecker_argument_parser",
    "gen_available_dictionaries",
    "gen_available_dictionaries_with_langcodes",
    "get_hunspell_version",
    "is_valid_dictionary_language",
    "is_valid_dictionary_language_or_filename",
    "assert_is_valid_dictionary_language_or_filename",
    "list_available_dictionaries",
    "looks_like_a_word",
    "print_available_dictionaries",
    "render_hunspell_word_error",
)

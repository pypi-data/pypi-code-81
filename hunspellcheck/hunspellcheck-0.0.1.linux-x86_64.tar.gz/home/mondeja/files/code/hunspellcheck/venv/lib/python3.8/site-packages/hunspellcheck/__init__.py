"""Hunspellcheck package."""

from hunspellcheck.cli import extend_argument_parser
from hunspellcheck.hunspell.dictionaries import (
    gen_available_dictionaries,
    list_available_dictionaries,
    print_available_dictionaries,
)
from hunspellcheck.hunspell.version import get_hunspell_version
from hunspellcheck.spellchecker import SpellChecker, render_error


__version__ = "0.0.1"
__title__ = "hunspellcheck"
__all__ = (
    "extend_argument_parser",
    "gen_available_dictionaries",
    "get_hunspell_version",
    "list_available_dictionaries",
    "print_available_dictionaries",
    "render_error",
    "SpellChecker",
)

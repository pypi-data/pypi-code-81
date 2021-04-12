"""Exceptons module of hunspellcheck."""


class HunspellCheckError(Exception):
    """All exceptions from this module inherit from this one."""


class Unreachable(HunspellCheckError):
    """The code encontered a state that should be unreachable."""


class InvalidLanguageDictionaryError(HunspellCheckError, ValueError):
    """Invalid language dictionary name."""

"""Spellchecker of hunspellcheck.

This module contains all the spellchecking logic.
"""

import string

from hunspellcheck.hunspell.spellcheck import hunspell_spellcheck


ERROR_FIELDS = [
    "filename",
    "line_number",
    "word",
    "word_line_index",
    "line",
    "text",
    "error_number",
    "near_misses",
]


class HunspellCheckException(Exception):
    """All exceptions from this module inherit from this one."""


class Unreachable(HunspellCheckException):
    """The code encontered a state that should be unreachable."""


def looks_like_a_word(word):
    """Return True if the given str looks like a word.

    Used to filter out non-words like `---` or `-0700` so they don't
    get reported. They typically are not errors.
    """
    if not word:
        return False
    if any(digit in word for digit in string.digits):
        return False
    return True


class SpellChecker:
    """Main spellchecking interface of hunspellcheck.

    Args:
        filenames_contents (dict): Dictionary mapping filenames to content of
            those files.
        languages ()
    """

    def __init__(
        self,
        filenames_contents,
        languages,
        personal_dict=None,
        looks_like_a_word=looks_like_a_word,
    ):
        self.filenames_contents = filenames_contents
        self.languages = languages
        self.personal_dict = personal_dict
        self.looks_like_a_word = looks_like_a_word
        self.errors = None

    def check(
        self,
        include_filename=True,
        include_line_number=True,
        include_word=True,
        include_word_line_index=True,
        include_line=False,
        include_text=False,
        include_error_number=False,
        include_near_misses=False,
    ):
        self.errors = yield from parse_hunspell_output(
            self.filenames_contents,
            hunspell_spellcheck(
                quote_for_hunspell("\n".join(self.filenames_contents.values())),
                self.languages,
                personal_dict=self.personal_dict,
            ),
            looks_like_a_word=self.looks_like_a_word,
            include_filename=include_filename,
            include_line_number=include_line_number,
            include_word=include_word,
            include_word_line_index=include_word_line_index,
            include_line=include_line,
            include_text=include_text,
            include_error_number=include_error_number,
            include_near_misses=include_near_misses,
        )


def quote_for_hunspell(text):
    """Quote a paragraph so hunspell don't misinterpret it.

    Quoting Hunspell's manpage: "It is recommended that programmatic interfaces
    prefix every data line with an uparrow to protect themselves against future
    changes in hunspell.
    """
    response = []
    for line in text.splitlines():
        response.append(f"^{line}" if line else "")
    return "\n".join(response)


def parse_hunspell_output(
    filenames_contents,
    hunspell_output,
    looks_like_a_word=looks_like_a_word,
    include_filename=True,
    include_line_number=True,
    include_word=True,
    include_word_line_index=True,
    include_line=False,
    include_text=False,
    include_error_number=False,
    include_near_misses=False,
):
    """Parse `hunspell -a` output."""
    locals_yielder = []

    _locals = locals()
    for possible_inclusion in ERROR_FIELDS:
        if _locals.get(f"include_{possible_inclusion}"):
            locals_yielder.append(possible_inclusion)

    error_number = 0
    checked_files = iter(filenames_contents.items())
    filename, text = next(checked_files)
    checked_lines = iter(text.split("\n"))
    line = next(checked_lines)
    line_number = 1

    for hunspell_line in hunspell_output.stdout.split("\n")[1:]:
        if not hunspell_line:
            try:
                line = next(checked_lines)
                line_number += 1
            except StopIteration:
                # next file
                try:
                    filename, text = next(checked_files)
                    checked_lines = iter(text.split("\n"))
                    line = next(checked_lines)
                    line_number = 1
                except StopIteration:
                    return error_number
            continue

        if hunspell_line[0] == "&":
            _, word, *mispell_data = hunspell_line.split()
            if include_word_line_index:
                word_line_index = int(mispell_data[1].rstrip(":")) - 1
            if include_near_misses:
                near_misses = [miss.rstrip(",") for miss in mispell_data[2:]]
            if looks_like_a_word(word):
                error_number += 1
                _locals = locals()
                yield ({field: _locals.get(field) for field in locals_yielder})

    raise Unreachable("Got this one? I'm sorry, read XKCD 2200, then open an issue.")


def render_error(
    data,
    fields=["filename", "word", "line_number", "word_line_index"],
    sep=":",
):
    values = []
    for field in fields:
        value = data.get(field)
        if value is not None:
            values.append(str(value))
    return (sep).join(values)

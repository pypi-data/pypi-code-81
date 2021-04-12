"""Spellchecker of hunspellcheck.

This module contains all the spellchecking logic.
"""

import string

from hunspellcheck.exceptions import Unreachable
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


def looks_like_a_word(text):
    """Return True if the given str looks like a word.

    Used to filter out non-words like `---` or `-0700` so they don't
    get reported. They typically are not errors.

    Args:
        word (str): Text to check if is a word.

    Returns:
        bool: ``True`` if the input looks like a word, ``False`` instead.
    """
    if not text:
        return False
    if any(digit in text for digit in string.digits):
        return False
    if text.startswith("-") or text.endswith("-"):
        return False
    return True


class HunspellChecker:
    """Main spellchecking interface of hunspellcheck.

    Args:
        filenames_contents (dict): Dictionary mapping filenames to content of
            those files.
        languages (list, str): Languages against will be checked the contents.
        personal_dicts (str, list): Globs of files which would be dictionaries
            with custom words to ignore from being triggered as positives. Can
            be globs or files, as string or list of strings.
        looks_like_a_word (types.FunctionType): Function to filter the positive
            words from being considered positives. By default, the function
            :py:func:`hunspellcheck.looks_like_a_word` will be used,
            which will do a basic check.
        encoding (str): Input encoding. If not defined, it will be autodetected
            by hunspell.
    """

    def __init__(
        self,
        filenames_contents,
        languages,
        personal_dicts=None,
        looks_like_a_word=looks_like_a_word,
        encoding=None,
    ):
        self.filenames_contents = filenames_contents
        self.languages = languages
        self.personal_dicts = personal_dicts
        self.looks_like_a_word = looks_like_a_word
        self.errors = None
        self.encoding = encoding

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
        """Spellchecking function.

        Yields each mispelled word data found in contents from a generator. The
        data generated for each word depends on the optional arguments
        ``include_<field>`` passed to this function, being ``field`` the name
        of the field inside the yielded dictionary.

        Args:
            include_filename (bool): Includes filename where the mispelled word
                has been found in yielded error data.
            include_line_number (bool): Includes the line number where the
                mispelled word has been found in the content for the yielded
                error data.
            include_word (bool): Includes the mispelled word found in the
                yielded error data.
            include_word_line_index (bool): Includes the index of the caracter
                in which the mispelled word starts in their line (starting at
                index 0).
            include_line (bool): Includes the entire line where the mispelled
                word resides inside the content.
            include_text (bool): Includes the full text of the content in where
                the mispelled word resides.
            include_error_number (bool): Include the number of the error in
                yielded data. This could be useful to avoid the need of define
                a counter.
            include_near_misses (bool): Includes a list with the near misses
                for the mispelled word.

        Yields:
            dict: Dictionary with all the included data for each mispelled word.
        """
        self.errors = yield from parse_hunspell_output(
            self.filenames_contents,
            hunspell_spellcheck(
                quote_for_hunspell("\n".join(self.filenames_contents.values())),
                self.languages,
                personal_dicts=self.personal_dicts,
                encoding=self.encoding,
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
    changes in hunspell."

    Args:
        text (str): Text to be quoted.

    Returns:
        str: Text quoted as Hunspell recommends.
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
                yielded_content = {}
                for field in locals_yielder:
                    value = _locals.get(field)
                    if value:
                        yielded_content[field] = value
                    elif not isinstance(value, (str, list)):
                        yielded_content[field] = value
                yield yielded_content

    raise Unreachable(
        "This line shouldn't be reachable. Please, open an issue at"
        " https://github.com/mondeja/hunspellcheck"
    )  # pragma: no cover


def render_hunspell_word_error(
    data,
    fields=["filename", "word", "line_number", "word_line_index"],
    sep=":",
):
    """Renders a mispelled word data dictionary.

    This function allows a convenient way to render each mispelled word data
    dictionary as a string, that could be useful to print in the context of
    spell checkers command line interfaces.

    Args:
        data (dict): Mispelled word data, as it is yielded by the method
            :py:meth:`hunspellcheck.HunspellChecker.check`.
        fields (list): List of fields to include in the response.
        sep (str): Separator string between each field value.

    Returns:
        str: Mispelled word data as a string.
    """
    values = []
    for field in fields:
        value = data.get(field)
        if value is not None:
            values.append(str(value))
    return (sep).join(values)

"""Text utils."""
import re
from typing import Union


def strip_ansi_escape(data: Union[str, bytes]) -> str:
    """Remove all ANSI escapes from string or bytes.

    If bytes is passed instead of string, it will be converted to string
    using UTF-8.
    """
    if isinstance(data, bytes):
        data = data.decode("utf-8")

    return re.sub(r"\x1b[^m]*m", "", data)


def toidentifier(text: str) -> str:
    """Convert unsafe chars to ones allowed in variables."""
    result = re.sub(r"[\s-]+", '_', text)
    if not result.isidentifier:
        raise RuntimeError(
            "Unable to convert role name '%s' to valid variable name." % text
        )
    return result

"""
This module contains various utilities.
"""

import typing


def extract_summary_from_string(target: str) -> str:
    """
    Extract the summary (first line) of a docstring.
    """
    try:
        doc = [x.strip() for x in (target or '').split('\n') if x.strip()]
        result = doc[0:1][0] or None
        return result
    except (AttributeError, IndexError):
        return None

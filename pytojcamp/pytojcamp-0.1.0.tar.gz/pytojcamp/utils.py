# -*- coding: utf-8 -*-
"""Helper functions"""
from typing import Union

from .constants import ADDITIONAL_META


class InvalidNtupleError(ValueError):
    pass


def _format_additional_header(meta: Union[dict, None]) -> str:
    """Create a multiline string for all the metadata

    Args:
        meta (Dict): Dictionary with metadata

    Raises:
        ValueError: If meta is not a dictionary

    Returns:
        str: multiline string for the JCAMP string
    """
    additional_header = ""
    if meta is not None:
        try:
            for key, value in meta.items():
                additional_header += ADDITIONAL_META.format(key=key, value=value)
        except AttributeError:
            raise ValueError(
                "If you provide metadata, you need to provide it as dictionary"
            )

    return additional_header

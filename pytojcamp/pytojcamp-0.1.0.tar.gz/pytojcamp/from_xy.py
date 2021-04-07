# -*- coding: utf-8 -*-
"""Convert simple x/y data to jcamp"""
from typing import Iterable, Tuple, Union

import numpy as np

from .constants import HEADER
from .utils import _format_additional_header


def from_xy(  # pylint:disable=too-many-arguments, too-many-locals
    data: Tuple[Iterable[Union[float, int]], Iterable[Union[float, int]]],
    title: str = "",
    owner: str = "",
    origin: str = "",
    data_type: str = "",
    x_units: str = "",
    y_units: str = "",
    meta: dict = None,
) -> str:
    """Convert a tuple of x/y data to a JCAMP string

    Args:
        data (Tuple[Iterable[Union[float, int]],
            Iterable[Union[float, int]]]): Tuple of data
        title (str, optional): Defaults to "".
        owner (str, optional): Defaults to "".
        origin (str, optional): Defaults to "".
        data_type (str, optional): Defaults to "".
        x_units (str, optional):  Defaults to "".
        y_units (str, optional):  Defaults to "".
        meta (dict, optional): Additional metadata for the header. Defaults to None.

    Raises:
        ValueError: [description]

    Returns:
        str: [description]
    """
    try:
        x_data, y_data = data
        first_x = np.min(x_data)
        first_y = np.min(y_data)
        last_x = np.max(x_data)
        last_y = np.max(y_data)
    except ValueError:
        raise ValueError(
            "You need to provide a tuple of iterables of floats or integers"
        )

    points = [f"{x_point}  {y_point}" for x_point, y_point in zip(x_data, y_data)]

    header_dict = {
        "dataType": data_type,
        "origin": origin,
        "owner": owner,
        "title": title,
        "xUnits": x_units,
        "yUnits": y_units,
        "firstX": first_x,
        "firstY": first_y,
        "lastX": last_x,
        "lastY": last_y,
        "points": len(points),
    }

    header = HEADER.format(**header_dict)
    additional_header = _format_additional_header(meta)
    point_list = "\n".join(points)

    full_jcamp = (
        header + additional_header + "##PEAK TABLE=(XY..XY)\n" + point_list + "\n##END"
    )

    return full_jcamp

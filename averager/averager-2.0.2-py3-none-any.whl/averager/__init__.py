"""Simple utilities for calculating averages"""

from __future__ import division

__version__ = "2.0.2"


def _optional_int(value):
    """Converts a ``float`` to an ``int`` if they're the same value

    Args:
        value (float)

    Returns:
        Either the original input or the input as an ``int``

    Example:
        >>> _optional_int(3.0)
        3

        >>> _optional_int(1.2)
        1.2
    """

    if value == int(value):
        return int(value)

    return value


def average(values):
    """Calculates an unweighted average

    Args:
        values (Iterable): The values to find the average of

    Returns:
        The average of the inputs

    Example:
        >>> average([1, 2, 3])
        2
    """

    res = sum(values) / len(values)

    return _optional_int(res)


def weighted_average(values):
    """Calculates an weighted average

    Args:
        values (Iterable): The values to find the average as an iterable of
            ``(value, weight)`` pairs

    Returns:
        The weighted average of the inputs

    Example:
        >>> weighted_average([(1, 2), (2, 3)])
        1.6
    """

    dividend, divisor = 0, 0

    for value, weight in values:
        if weight < 0:
            raise ValueError("Weights cannot be less than zero")

        dividend += value * weight
        divisor += weight

    res = dividend / divisor

    return _optional_int(res)

from typing import Callable


def safe_split(source: str, delimiter=',', converter: Callable = lambda x: x):
    """
    Splits a string via the delimiter, throws out any empties and strips the whitespace from each item
    :param source: str
    :param delimiter: str
    :param converter: Callable
    :return: list
    """
    if not source:
        return []
    return list(filter(None, [converter(item.strip()) for item in source.split(delimiter)]))

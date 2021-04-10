from typing import Any, Dict

from deepmerge import always_merger


def merge_dicts(*args: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Successively merge any number of dictionaries.

    >>> merge_dicts({'a': 1}, {'b': 2})
    {'a': 1, 'b': 2}

    >>> merge_dicts({'a': 1}, {'a': 2}, {'a': 3})
    {'a': 3}

    Returns:
        Dict: Dictionary of merged inputs.
    """
    out = {}  # type: Dict[Any, Any]
    for dct in args:
        out = {**out, **dct}
    return out


def deep_merge_dicts(*args: Dict[Any, Any]) -> Dict[Any, Any]:
    out = {}  # type: Dict[Any, Any]
    for dct in args:
        out = always_merger.merge(out, dct)
    return out


def collapse_dict(dct: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    >>> collapse_dict({'a': {'x': 1}, 'b': {'y': 2}})
    {'x': 1, 'y': 2}

    >>> collapse_dict({'a': {'x': 1}, 'b': 2})
    {'a': {'x': 1}, 'b': 2}
    """
    return (
        merge_dicts(*dct.values())
        if all(map(lambda x: isinstance(x, dict), dct.values()))
        else dct
    )


def key_is_true(dct: Dict[str, Any], key: str) -> bool:
    """
    >>> key_is_true({'a': True}, 'a')
    True

    >>> key_is_true({'a': False}, 'a')
    False

    >>> key_is_true({'a': True}, 'b')
    False
    """
    return key in dct and dct[key]

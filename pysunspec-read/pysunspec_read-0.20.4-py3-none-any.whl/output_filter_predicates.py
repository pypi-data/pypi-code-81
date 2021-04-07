from numbers import Number
from typing import Any


def apply(predicates, key, value):
    result = any(p for p in predicates if p(key, value))
    return result


def is_none(key: str, value: Any) -> bool:
    return value is None


def is_zero(key: str, value: Any) -> bool:
    return isinstance(value, Number) and value == 0


def is_scale_factor(key: str, value: Any) -> bool:
    return isinstance(key, str) and str(key).casefold().endswith("_sf")

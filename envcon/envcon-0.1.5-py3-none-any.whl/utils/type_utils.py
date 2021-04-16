import json
from typing import Final, Union, get_args, get_origin, List, Any

from .supported_types import SupportedTypes
from .functional import first

try:
    # list[T], dict[T,U] etc'
    from types import GenericAlias as _GenericAlias
except ImportError:

    class _GenericAlias:
        pass


def cast(value: str, to: type) -> SupportedTypes:
    if is_optional(to):
        return cast(value, get_first_optional_subtypes(to))
    elif to in [str, int, float]:
        return to(value)
    elif to is bool:
        return to_bool(value)
    elif is_list(to):
        return to_list(value, to)
    elif is_dict(to):
        return json.loads(value)

    return str(value)


def get_first_optional_subtypes(type_: type) -> type:
    if not is_optional(type_):
        raise ValueError(f"type {type_} is not an optional (Optional[T] or Union[T, U, ..., None]")
    return first(lambda t: not is_none_type(t), get_args(type_))


def is_optional(type_: type) -> bool:
    return get_origin(type_) == Union and any(is_none_type(t) for t in get_args(type_))


def is_none_type(val: Any) -> bool:
    return isinstance(val, type) and not isinstance(val, _GenericAlias) and isinstance(None, val)


def is_list(type_: type) -> bool:
    return type_ is list or get_origin(type_) is list


def is_dict(type_: type) -> bool:
    return type_ is dict or get_origin(type_) is dict


def to_list(value: str, value_type: type) -> List[Union[str, bool, int, float]]:
    type_args: Final[tuple] = get_args(value_type)
    generic_type: Final[type] = type_args[0] if type_args else str
    return value.split(",") if generic_type is str else [generic_type(element) for element in value.split(",")]


def to_bool(value: str) -> bool:
    return value and value.lower() not in ["", "0", "n", "no", "ney", "nan", "null", "not", "false", "off", "~"]

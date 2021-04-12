#
# Copyright (c) 2021 Carsten Igel.
#
# This file is part of nt2dc
# (see https://github.com/carstencodes/nt2dc).
#
# License: 3-clause BSD, see https://opensource.org/licenses/BSD-3-Clause
#
"""
    Provides methods for the conversion of dataclasses to untyped named tuples
"""

from dataclasses import is_dataclass, fields, asdict, Field
from collections import namedtuple as real_namedtuple
from typing import Any, NamedTuple, Tuple, Type, Optional, List, Dict


def namedtuple(clz: Type) -> Type[NamedTuple]:
    """Creates a named tuple equivalent to the dataclass specified
       by the given type.

    Args:
        clz (Type): The type of the dataclass to convert

    Raises:
        TypeError: If clz is not a dataclass type.

    Returns:
        Type[NamedTuple]: The named tuple class equivalent to clz.
    """
    if not is_dataclass(clz):
        raise TypeError("{} is not a dataclass.".format(clz.__name__))

    flds: Tuple[Field] = fields(clz)
    flds_by_name: Dict[str, Field] = {f.name: f for f in flds}
    nt_name: str = clz.__name__ + "NamedTuple"

    defaults: Optional[List[Any]] = None
    field_names: List[str] = [
        f.name
        for f in flds
        if f.default is not None or f.default_factory is not None
    ]
    for fld in field_names:
        if defaults is None:
            defaults = []
        field: Field = flds_by_name[fld]
        default_value: Optional[Any] = field.default
        if default_value is None:
            default_value = field.default_factory()

        defaults.append(default_value)

    field_names.extend(
        [
            f.name
            for f in flds
            if f.default is None and f.default_factory is None
        ]
    )

    return real_namedtuple(nt_name, field_names, defaults=defaults)


def get_named_tuple_object(instance: Any) -> Tuple[object, Type[object]]:
    """Creates a named tuple from the specified data class instance and
       returns the new instance and the type as a tuple.

    Args:
        instance (Any): The instance to convert.

    Returns:
        Tuple[object, Type[object]]: The converted instance and its type.
    """
    clz: Type = namedtuple(instance.__class__)
    instance_data = asdict(instance)
    for key, value in instance_data.items():
        if is_dataclass(value):
            obj, _ = get_named_tuple_object(value)
            instance_data[key] = obj

        # generics currently unsupported, maybe in later versions

    new_instance: clz = clz(**instance_data)
    return (new_instance, clz)

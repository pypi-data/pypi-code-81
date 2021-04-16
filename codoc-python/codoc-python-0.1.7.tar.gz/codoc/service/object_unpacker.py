#!/usr/bin/env python3
import inspect
from typing import Set, Tuple
from pkgutil import iter_modules
import importlib.util

from codoc.domain.model import Node

from .parsing.types import ObjectType
from .parsing.utils import is_not_an_instance

NodeTuple = Tuple[ObjectType, Node]


def recursively_get_all_subobjects_in_object(obj: ObjectType) -> Set[ObjectType]:
    sub_objects = get_relevant_objects_in_object(obj)
    return {obj} | get_all_objects_in_sub_objects(obj, sub_objects) | sub_objects


def get_all_objects_in_sub_objects(
    obj: ObjectType, sub_objects: Set[ObjectType]
) -> Set[ObjectType]:
    return set(
        sub_sub_obj
        for sub_obj in sub_objects
        if is_obj_part_of_module(sub_obj, obj)
        for sub_sub_obj in recursively_get_all_subobjects_in_object(sub_obj)
    )


def get_relevant_objects_in_object(obj: ObjectType) -> Set[ObjectType]:
    sub_objects = set(
        with_parentclass_attribute(sub_obj, obj)
        for name, sub_obj in _get_subobjects(obj)
        if is_obj_valid_for_return(name, sub_obj, obj)
    )
    return sub_objects


def _get_subobjects(obj: ObjectType) -> Set[ObjectType]:
    for member in inspect.getmembers(obj):
        yield member

    if inspect.ismodule(obj) and hasattr(obj, "__path__"):
        for sub_module in [
            _load_module(mod)
            for mod in iter_modules(obj.__path__, prefix=f"{obj.__name__}.")
        ]:
            yield sub_module


def _load_module(mod) -> ObjectType:
    name = mod.name
    spec = mod.module_finder.find_spec(name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return name, module


def with_parentclass_attribute(obj: ObjectType, parent: ObjectType) -> ObjectType:
    if inspect.isclass(parent):
        obj.__parentclass__ = parent
    return obj


def is_obj_valid_for_return(name: str, obj: ObjectType, parent: ObjectType) -> bool:
    return (
        not name.startswith("__")
        and is_not_an_instance(obj)
        and is_obj_part_of_module(obj, parent)
    )


# test functions individually
def is_obj_part_of_module(obj: ObjectType, parent: ObjectType) -> bool:
    module_name = get_name_of_module(obj)
    parent_name = get_name_of_module(parent)
    return module_name is not None and module_name.startswith(parent_name)


def get_name_of_module(obj: object) -> str:
    return obj.__name__ if inspect.ismodule(obj) else getattr(obj, "__module__", None)

#!/usr/bin/env python3
import importlib
import zlib
import os
import inspect
import logging
from typing import Optional, Tuple

from codoc.domain.model import Node, NodeType
from codoc.service.parsing.utils import is_an_instance
from codoc.service.parsing.types import ObjectType

logger = logging.getLogger(__name__)

DEBUG_MODE = True


def create_node_from_object(obj: ObjectType, external: bool = True) -> Node:
    if obj is None:
        raise ValueError()
    if is_an_instance(obj):
        raise ValueError()
    return Node(
        identifier=get_identifier_of_object(obj),
        name=get_name(obj),
        description=get_description(obj),
        of_type=get_type(obj),
        parent_identifier=get_parent_identifier(obj),
        path=get_path(obj),
        args=get_args(obj),
        lines=get_lines(obj),
        external=external,
    )


def get_identifier_of_object(obj: ObjectType) -> str:
    """
    Returns the unique identifier of this object
    """
    try:
        hash_id = hex(zlib.adler32(inspect.getsource(obj)))[2:]
    except (TypeError, OSError):
        # This is a suitable backup.
        # If we cannot find the source, it's probably
        # because the element is a builtin,
        # and the parent is then a fine hash.
        parent = get_parent_of_object(obj)
        if parent:
            hash_id = get_name(parent)
        else:
            hash_id = ""
    return f"{get_name(obj)}/{get_type(obj)}/{hash_id}"


def get_description(obj: ObjectType) -> str:
    return inspect.getdoc(obj) or ""


def get_args(obj: ObjectType) -> Optional[Tuple[str, ...]]:
    try:
        return tuple(inspect.getfullargspec(obj).args)
    except TypeError:
        return None


def get_path(obj: ObjectType) -> Optional[str]:
    try:
        abs_path = inspect.getfile(obj)

        cwd = os.getcwd()
        relative_path = os.path.relpath(abs_path, cwd)
        return relative_path
    except TypeError:
        return None


def get_lines(obj: ObjectType) -> Optional[Tuple[int, int]]:
    return None
    # TODO reenable when we get a relative path, not including home etc.
    # TODO or simply use another node_creator when running tests
    try:
        file_name = inspect.getfile(obj)
    except TypeError:
        return None
    try:
        with open(file_name) as f:
            content = f.read()
            try:
                source = inspect.getsource(obj)
            except OSError:
                return None
            start = len(content.split(source)[0].split("\n"))
            end = start + len(source.split("\n")) - 1
            return (start, end)
    except (FileNotFoundError, UnicodeDecodeError):
        return None


def get_name(obj: ObjectType) -> str:
    """
    Returns the human readable name of the object.

    This is often just the name of the object, i.e in this
    method it would be `get_name`.
    However on typing etc, they don't have a name in the
    same way, so there it will be a bit more tailored.
    """
    name = (
        getattr(obj, "__name__", None)
        or getattr(obj, "_name", None)
        or getattr(obj, "name", None)
    )

    if name is None:
        return str(obj)
        # raise NameNotFound(obj)

    return name


def get_type(obj: ObjectType) -> NodeType:

    # Some of the elements in `typing` are actually a str
    # so we have to check for this first
    # however some of the elements in `types` are also classes
    # so we need to check for types first
    if obj is str:
        return NodeType.CLASS

    if inspect.isclass(obj):
        if issubclass(obj, BaseException):
            return NodeType.EXCEPTION
        return NodeType.CLASS
    if getattr(obj, "__module__", "").startswith("typing"):
        return NodeType.CLASS
    if callable(obj):
        return NodeType.FUNCTION
    if inspect.ismodule(obj):
        return NodeType.MODULE

    # TODO find out if we can make this assumption
    return NodeType.CLASS


def get_parent_identifier(obj: ObjectType) -> Optional[str]:
    parent = get_parent_of_object(obj)

    if parent is None:
        return None

    return get_identifier_of_object(parent)


def get_parent_of_object(obj: ObjectType) -> Optional[ObjectType]:
    if inspect.ismodule(obj):
        return _get_outer_module(obj)
    try:
        return obj.__parentclass__
    except AttributeError:
        pass

    try:
        module = inspect.getmodule(obj)
        if module is not None:
            return module
    except AttributeError:
        pass
    try:
        return importlib.import_module(obj.__module__)
    except AttributeError:
        pass

    return None


def _get_outer_module(obj: ObjectType) -> Optional[object]:
    """
    If the current item is a module, then it tries to get the outer module
    """
    outer_module_name = ".".join(get_name(obj).split(".")[:-1])
    if outer_module_name == "":
        return None
    outer_module = importlib.import_module(outer_module_name)

    return outer_module


class UnrecognizedTypeError(Exception):
    def __init__(self, obj: object):
        super().__init__(f"cannot deduce type of `{obj}`")


class NameNotFound(Exception):
    def __init__(self, obj: object):
        super().__init__(f"cannot find the name of `{obj}` ({type(obj)})")

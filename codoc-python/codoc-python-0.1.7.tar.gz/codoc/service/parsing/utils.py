#!/usr/bin/env python3
import builtins
import inspect
import io
import types
import typing


def is_not_an_instance(value: object) -> bool:
    return not is_an_instance(value)


def is_an_instance(value: object) -> bool:
    is_class = inspect.isclass(value)
    is_function = isinstance(value, types.FunctionType)
    is_module = inspect.ismodule(value)
    is_type = inspect.getmodule(value) in {typing, types, builtins, io}

    return not (is_class or is_function or is_module or is_type)


def is_builtin(elm: typing.Any) -> bool:
    return getattr(elm, "__name__", "") in dir(builtins) or elm is builtins


def is_not_class(elm: object) -> bool:
    return not isinstance(elm, type)


def remove_indents_from_source(source: str) -> str:
    lines = source.split("\n")
    indents = _get_indents(lines[0])
    return "\n".join(line[indents:] for line in lines)


def _get_indents(line: str) -> int:
    return _get_indents(line[1:]) + 1 if line.startswith(" ") else 0

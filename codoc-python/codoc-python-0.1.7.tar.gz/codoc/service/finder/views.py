#!/usr/bin/env python3
from typing import Callable, List
import importlib.util
import inspect
from pathlib import Path
from codoc.domain.model import Graph
from codoc.service.finder.files import (
    get_all_python_files,
)

CodocView = Callable[[Graph], Graph]


def get_views_in_file(py_file: Path) -> List[CodocView]:
    file_name = py_file.name[:-3]
    # TODO create a helper for importing shit
    spec = importlib.util.spec_from_file_location(file_name, py_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    views = [
        value
        for key, value in inspect.getmembers(module)
        if getattr(value, "__is_codoc_view", False)
    ]

    return views


def get_views_in_folder(folder: Path) -> List[CodocView]:
    files = get_all_python_files(folder)
    return [view for f in files for view in get_views_in_file(f)]

#!/usr/bin/env python3
import importlib
import importlib.util
from pathlib import Path
from codoc.service.finder.files import (
    get_all_python_files,
)


def get_config(folder: Path) -> object:
    conf_file = get_config_file(folder)
    spec = importlib.util.spec_from_file_location(conf_file.name, conf_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def get_config_file(folder: Path) -> Path:
    try:
        return next(
            f
            for f in get_all_python_files(folder)
            if f.name in ["codoconf.py", "conf.py", "config.py"]
        )
    except StopIteration:
        raise NoConfigFileInFolder


class NoConfigFileInFolder(Exception):
    ...

    def __init__(self):
        super().__init__("No config.py file in view folder")

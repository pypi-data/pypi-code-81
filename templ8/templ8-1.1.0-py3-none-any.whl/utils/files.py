import json
from typing import Any, Dict

from yaml import Loader, load

from templ8.exceptions import UnrecognizedFormat

from .paths import path_ext


def parse_file(path: str) -> Dict[str, Any]:
    with open(path, "r") as stream:
        if path_ext(path) == ".json":
            return json.load(stream)

        if path_ext(path) in [".yml", ".yaml"]:
            return load(stream, Loader=Loader)

        raise UnrecognizedFormat(path_ext(path))

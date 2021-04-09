from typing import List
from pathlib import Path
from importlib import import_module

from dotcoin.core.abstract import Source

SOURCE_PATH = Path(__path__[0])


def find_source(name: str) -> Source.__class__:
    module = import_module(f"{__name__}.{name}.source")
    for key in dir(module):
        if key.lower() == f"{name}source":
            return getattr(module, key)


def all_sources() -> List[Source.__class__]:
    source_list = []
    for item in SOURCE_PATH.glob("*/"):
        if not item.name.startswith("_"):
            source = find_source(item.name)
            if issubclass(source, Source):
                source_list.append(source)
    return source_list

from pathlib import Path

from .utils.singleton import Singleton
from .utils.yaml import CommentedMap

DEFAULTS = [
    ("device", str, "cpu"),
    ("output_dir", Path, "output"),
    ("experiment_name", str, None),
    ("log_dir", Path, "log"),
]


class Env(dict, metaclass=Singleton):
    def __init__(self):
        ...

    @staticmethod
    def from_config(cls, config: CommentedMap):
        assert isinstance(config, CommentedMap), type(config)
        items = []
        for key, tp, default in DEFAULTS:
            if key not in config:
                value = default
            else:
                value = tp(config.pop(key))
            items.append((key, value))
        items += list(config.items())

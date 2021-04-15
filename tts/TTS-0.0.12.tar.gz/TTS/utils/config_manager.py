import json
import os

import yaml

from .generic_utils import find_module


def load_config(config_path: str) -> None:
    config_dict = {}
    ext = os.path.splitext(config_path)[1]
    if ext in (".yml", ".yaml"):
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    elif ext == ".json":
        with open(config_path, "r", encoding="utf-8") as f:
            input_str = f.read()
        data = json.loads(input_str)
    else:
        raise TypeError(f" [!] Unknown config file type {ext}")
    config_dict.update(data)
    config_class = find_module("TTS.tts.configs", config_dict["model"].lower() + "_config")
    config = config_class()
    config.from_dict(config_dict)
    return config

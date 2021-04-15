"""Configuration for hdev commands."""
import functools
import os
from collections.abc import Mapping

import toml

DEFAULT_CONFIG_FILENAME = "pyproject.toml"


class Configuration(Mapping):
    """Configuration for hdev file.

    Loaded from a toml file into a dict
    """

    def __init__(self, config: dict):
        self._config = config

    def __getitem__(self, key):
        return self._config[key]

    def __len__(self):
        return len(self._config)

    def __iter__(self):
        return iter(self._config)

    def get(self, key, default=None):
        """Get nested keys using "key" with dot as separator.

           config.get("key", {}).get("nested")

        becomes:

            config.get("key.nested")
        """
        if not "." in key:
            return super().get(key, default)

        get = lambda _default, d, key: dict.get(d, key, _default)

        parts = key.split(".")
        value = functools.reduce(functools.partial(get, {}), parts, self._config)
        return value if value not in [None, {}] else default


def load_configuration(config_path=None):
    """Load hdev configuration based on `config_path`."""
    if not config_path:
        config_path = os.path.join(os.getcwd(), DEFAULT_CONFIG_FILENAME)

    try:
        toml_config = toml.load(config_path)
    except FileNotFoundError:
        # No project file, use defaults
        toml_config = {}
    except ValueError:
        print(f"Invalid syntax on toml file '{config_path}'")
        return None

    return Configuration(toml_config)

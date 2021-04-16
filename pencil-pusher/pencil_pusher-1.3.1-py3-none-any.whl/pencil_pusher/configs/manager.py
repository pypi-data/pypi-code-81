import json
from typing import Any, Dict, List, Tuple
from sd_utils.plugins.plugin_manager import PluginManager


class ConfigManager(PluginManager):
    """
    Manager for all config variables. Provides interface
    for loading, validating and getting configs from a
    file.
    """

    VALIDATE = "validate"
    """
    constant for validate action
    """

    GET = "get"
    """
    constant for get action.
    """

    PROCESS_LANG_FILE = "process_lang_file"
    """
    constant for process lang file action
    """

    def __init__(self):
        self._config_file_contents = None
        self._languages = {}
        super().__init__()

    def validate(self):
        """
        Validates all the configs in the loaded config file

        Raises:
            ValueError: if the config file is not loaded
        """
        if self._config_file_contents is None:
            raise ValueError("Config file was not loaded")

        self.iterate_all(
            {
                "type": ConfigManager.VALIDATE,
                "contents": self._config_file_contents,
            },
        )

    def get(self, name: str) -> Any:
        """
        Gets a config defined by `name`

        Raises:
            ValueError: if the config file is not loaded

        Args:
            name (str): the name of the config being retrieved

        Returns:
            Any: the value of the config
        """
        if self._config_file_contents is None:
            raise ValueError("Config file was not loaded")

        return self.run(
            name,
            on_find_params={
                "type": ConfigManager.GET,
                "contents": self._config_file_contents,
            },
        )

    def has(self, name: str) -> bool:
        """
        Returns true if a given config is defined (false otherwise)

        Args:
            name (str): the name of the config being searched for

        Returns:
            bool: True if the config exists, false otherwise
        """

    def process_lang_file(self, file_path: str) -> Tuple[bool, str]:
        """
        processes a language file based on defined configurations

        Args:
            file_path (str): the path of the config file to load.
                (must be a local location)

        Returns:
            Tuple[bool, str]: the first value is if the file should be included,
                the second value is the new name of the file if it should be
                included.
        """
        ext = file_path[file_path.index(".") + 1 :]
        lang_name = ""
        for lang, exts in self._languages.items():
            for dext in exts:
                if ext == dext:
                    lang_name = lang
                    break
        return self.run(
            lang_name,
            on_find_params={
                "type": ConfigManager.PROCESS_LANG_FILE,
                "contents": self._config_file_contents,
                "file_path": file_path,
            },
        )

    def load_config_file(self, file_path: str):
        """
        Loads a given config file (must be a local
        file location)

        Args:
            file_path (str): path of the config file
                (must be a local location)
        """
        with open(file_path, "r") as fp:
            self._config_file_contents = json.load(fp)

    def get_on_search_params(self, name: str, **kwargs) -> Any:
        return {"name": name, **kwargs}

    def get_on_find_params(self, name: str, **kwargs) -> Any:
        return {"name": name, **kwargs}

    def get_on_register_params(self, name: str, **kwargs) -> Any:
        return {"manager": self}

    def add_lang(self, lang_name: str, extensions: List[str]):
        """
        Adds a language and its relevant file extensions to
        this config manager.
        """
        self._languages[lang_name] = extensions

    def get_langs(self) -> Dict[str, List[str]]:
        """
        Returns a dictionary which maps each language to
        its extensions

        Returns:
            Dict[str, List[str]]: a dict of languages and their
                file extensions
        """
        return self._languages

from pencil_pusher.configs.manager import ConfigManager
from typing import Any
from sd_utils.plugins.plugin_base import PluginBase


class ConfigParamBase(PluginBase):
    """
    Base class for config parameters. All config parameters should
    extend this base class.
    """

    def __init__(self):
        self._is_defined = False

    def on_find(self, data: Any) -> Any:
        """
        Returns the value of this config

        Args:
            data (Any): A `dict` which contains the following values
                "type": a constant on what action is running
                "contents": the full config file as a dictionary
                "name": the name of the action being run

        Returns:
            Any: the value of this config
        """
        if not self._is_defined:
            return None
        return data["contents"][data["name"]]

    def on_iterate(self, data: Any):
        """
        This is the validate function

        Raises:
            ValueError: if the config is invalid. invalidity is
                determined by each config

        Args:
            data (Any): a `dict` with the following values
                "type": a constant on what action is being run (always VALIDATE)
                "contents": the full config file as a dictionary
        """
        if data["type"] == ConfigManager.VALIDATE:
            self._validate(data["contents"])
            self.set_defined()

    def _validate(self, contents: dict) -> bool:
        """
        method for validating this specific config given
        the entire config file as a dict

        Args:
            contents (dict): the full config file to validate
        """
        raise NotImplementedError

    def set_defined(self):
        """
        Sets this config parameter to having
        been defined.

        It is assumed that a config errors and
        is marked not valid if it is required
        but not defined
        """
        self._is_defined = True

"""
File for processing and validating inputs
"""
from pencil_pusher.github_api import GithubAPI
from os import environ
from typing import Any, Dict, Tuple
import yaml
import time


class InputDefinition:
    def __init__(self, name: str, description: str, required: bool = False):
        """"""
        self._name = name
        self._description = description
        self._required = required

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def required(self) -> bool:
        return self._required


class InputManager:
    def __init__(self):
        """
        Manager class for input provided in the action file
        """
        self._input_definition: Dict[str, InputDefinition] = {}
        self._provided_inputs = {
            "GITHUB_OWNER_NAME": "",
            "GITHUB_REPOSITORY_NAME": "",
        }

    def define(self, personal_access_token: str = ""):
        """
        Defines the expected inputs from the action file
        located in the pencil-pusher repo

        Args:
            personal_access_token (str): the github token
                to use for authentication or to increase
                the rate limit
        """
        InputManager._sync_action_file(personal_access_token)
        # user defined inputs
        with open("./action.yml", "r") as fp:
            definition = yaml.safe_load(fp)
            for input_name, input_definition in definition["inputs"].items():
                self._input_definition[input_name] = InputDefinition(
                    input_name,
                    input_definition["description"],
                    input_definition["required"],
                )

        # provided inputs
        repo_slug = environ["GITHUB_REPOSITORY"]
        self._provided_inputs["GITHUB_OWNER_NAME"] = repo_slug.split("/")[0]
        self._provided_inputs["GITHUB_REPOSITORY_NAME"] = repo_slug.split("/")[
            1
        ]

    def validate(self) -> Tuple[bool, str]:
        """
        Validates that all inputs in the given action
        file match those of the defined action file

        Returns:
            Tuple[bool, str]: a flag if validation succeeded
                and a message why it either succeeded or failed
        """
        for key, value in self._input_definition.items():
            environ_key: str = InputManager._environ_key(key)
            if environ_key not in environ:
                return False, f"Undefined input [{key}] provided"
            if value.required and (
                environ[environ_key] is None or environ[environ_key] == ""
            ):
                return (
                    False,
                    f"Required Input [{key}] has illegal value [{environ[environ_key]}]",
                )

        return True, "Successfully validated all inputs"

    def get(self, name: str) -> Any:
        """
        Gets an input by name

        Args:
            name (str): the name of the input variable
        """
        environ_input_key: str = InputManager._environ_key(name)
        environ_provided_key: str = InputManager._environ_provided_key(name)
        if (
            environ_input_key not in environ
            and environ_provided_key not in self._provided_inputs
        ):
            raise ValueError(f"Input [{name}] does not exist")

        return (
            environ[environ_input_key]
            if environ_input_key in environ
            else self._provided_inputs[environ_provided_key]
        )

    @staticmethod
    def _environ_key(name: str) -> str:
        return f"INPUT_{name.upper()}"

    @staticmethod
    def _environ_provided_key(name: str) -> str:
        return f"GITHUB_{name.upper()}"

    @staticmethod
    def _sync_action_file(personal_access_token: str = ""):
        """
        internal method for syncing the action file
        """
        content = GithubAPI.get_public_file(
            "stephend017", "ghapd", "action.yml", personal_access_token
        )
        with open("./action.yml", "w") as fp:
            fp.write(content)
        time.sleep(1)

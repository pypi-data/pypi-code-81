# This file is part of Flatplan.
#
# Flatplan is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Flatplan is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Flatplan.  If not, see <https://www.gnu.org/licenses/>.

from abc import ABC, abstractmethod
from distutils.util import strtobool
from logging import Logger
from typing import Dict, Optional
from .logging import setup_logger


class HookContext:
    """
    A class that can be used as a context for the hook to provide information necessary during the hook run.

    ...

    Methods
    -------
    None.
    """

    debug: bool
    output: str
    path: str
    flat: Dict
    remove: str
    state: bool

    def __init__(
        self,
        flat: Dict,
        debug: Optional[bool] = False,
        output: Optional[str] = "",
        path: Optional[str] = "",
        remove: Optional[str] = "",
        state: Optional[bool] = False,
    ) -> None:
        """
        Constructs all the necessary attributes for the HookContext object.

        Parameters
        ----------
        flat : Dict
            the terraform plan or state after being processed by Flattener class

        debug : bool, optional
            whether we show debug log messages or not, default: false

        output : str, optional
            a file path where we will save the flattened plan or state file in JSON format, default is empty

        path : str, optional
            a path pointing to the location of the terraform plan or state in JSON format, default is empty

        remove : str, optional
            a string containing the name of the tag and the its value separated by an equal sign that will be used to
            remove resources from the final result, example "remove=true", default is empty

        state : bool, optional
            whether the file passed in the path option is a state file instead of a plan file, default: false
        """
        self.debug = debug
        self.output = output
        self.path = path
        self.flat = flat
        self.remove = remove
        self.state = state

    @property
    def debug(self) -> bool:
        return self.__debug

    @debug.setter
    def debug(self, value: bool) -> None:
        self.__debug = value

    @property
    def output(self) -> str:
        return self.__output

    @output.setter
    def output(self, value: str) -> None:
        self.__output = value

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, value: str) -> None:
        self.__path = value

    @property
    def flat(self) -> Dict:
        return self.__flat

    @flat.setter
    def flat(self, value: Dict) -> None:
        self.__flat = value

    @property
    def remove(self) -> str:
        return self.__remove

    @remove.setter
    def remove(self, value: str) -> None:
        self.__remove = value

    @property
    def state(self) -> bool:
        return self.__state

    @state.setter
    def state(self, value: bool) -> None:
        self.__state = value


class Hook(ABC):
    """
    An abstract class that can be used as a hook (interface) for the Flattener class to provide additional features.

    ...

    Methods
    -------
    run() -> Dict :
        runs the hook
    """

    _context: HookContext
    _logger: Logger

    def __init__(self, context: HookContext, logger: Optional[Logger] = None) -> None:
        """
        Constructs all the necessary attributes for the Hook object.

        Parameters
        ----------
        context : HookContext
            the context in which the hook is inserted

        logger : logging.Logger, optional
            the logger object to be used

        Returns
        -------
        None.
        """
        self._context = context
        self._logger = (
            logger if logger is not None else setup_logger("hook", debug=True)
        )

    @abstractmethod
    def run(self) -> Dict:
        """
        Runs the hook.

        Parameters
        ----------
        None.

        Returns
        -------
        plan : Dict
        """
        pass


class RemoveResourceByTagHook(Hook):
    """
    A class that can be used as a hook to Flatplan in order to remove resources from
    the flattened plan by their tags.

    ...

    Methods
    -------
    run() -> Dict :
        runs the hook
    """

    def is_tag_present(self, tags: Dict, tag: str, value: str) -> bool:
        if tag not in tags:
            return False

        try:
            if isinstance(tags[tag], bool):
                return tags[tag] == bool(strtobool(value))

            if isinstance(tags[tag], str):
                return tags[tag] == value

            if isinstance(tags[tag], int):
                return tags[tag] == int(value)

            if isinstance(tags[tag], float):
                return tags[tag] == float(value)
        except ValueError:
            return False

        return False

    def run(self) -> Dict:
        """
        Traverses the plan and removes the resources that contain a certain tag.

        Parameters
        ----------
        None.

        Returns
        -------
        plan : Dict
        """
        flat = self._context.flat

        if "resources" not in flat:
            self._logger.debug("Could not find resources section")
            return flat

        try:
            tag, value = self._context.remove.split("=")
        except ValueError:
            if self._context.remove != "":
                tag = self._context.remove
                value = ""
            else:
                self._logger.debug("Remove tag is empty")
                return flat

        resources = []

        for resource in flat["resources"]:
            resource_addr = resource["address"]

            self._logger.debug(f"Checking resource '{resource_addr}'")

            try:
                tags = resource["values"]["tags"]

                if tags is not None:
                    if not self.is_tag_present(tags, tag, value):
                        self._logger.debug(
                            f"Resource '{resource_addr}' does not meet criteria to be removed"
                        )
                        resources.append(resource)
                    else:
                        self._logger.debug(
                            f"Resource '{resource_addr}' will be removed"
                        )
                else:
                    self._logger.debug(
                        f"Resource '{resource_addr}' does not meet criteria to be removed"
                    )
                    resources.append(resource)
            except KeyError:
                self._logger.debug(
                    f"Resource '{resource_addr}' does not meet criteria to be removed"
                )
                resources.append(resource)

        flat["resources"] = resources

        return flat

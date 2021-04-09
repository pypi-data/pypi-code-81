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
from copy import deepcopy
from json import loads
from logging import Logger
from typing import Any, Dict, List, Optional
from .logging import setup_logger


class Flattener(ABC):
    """
    An abstract class that can be used to build specific resources flatteners for Terraform.

    ...

    Methods
    -------
    flatten() -> Dict :
    """

    _logger: Logger

    def __init__(self, logger: Optional[Logger] = None) -> None:
        """
        Constructs all the necessary attributes for the Flattener object.

        Parameters
        ----------
        logger : logging.Logger, optional
            the logger object to be used
        """
        self._logger = (
            logger if logger is not None else setup_logger("flatplan", debug=True)
        )

    def _flatten_child_modules(self, modules: List) -> List:
        """
        Recursively traverses the child modules and creates a list with all resources found.

        Parameters
        ----------
        modules : List
            List of modules from JSON file

        Returns
        -------
        resources : List
        """
        resources = []

        for module in modules:
            module_address = (
                module["address"] if "address" in module.keys() else "unknown"
            )

            if "resources" in module.keys():
                for resource in module["resources"]:
                    resource_address = (
                        resource["address"]
                        if "address" in resource.keys()
                        else "unknown"
                    )
                    self._logger.debug(f"Adding resource: {resource_address}")
                    resources.append(deepcopy(resource))
            else:
                self._logger.debug(f"No resources found in module: {module_address}")

            if "child_modules" in module.keys():
                resources.extend(self._flatten_child_modules(module["child_modules"]))
            else:
                self._logger.debug(
                    f"No child modules found in module: {module_address}"
                )

        return resources

    def _flatten_resources(self, root_module: Any) -> List:
        """
        Traverses the root module and creates a list with all resources found.

        Parameters
        ----------
        None.

        Returns
        -------
        resources : List
        """
        resources = []

        if "resources" in root_module.keys():
            for resource in root_module["resources"]:
                resource_address = (
                    resource["address"] if "address" in resource.keys() else "unknown"
                )
                self._logger.debug(f"Adding resource: {resource_address}")
                resources.append(deepcopy(resource))
        else:
            self._logger.warning("Could not find 'resources' section under root module")

        if "child_modules" in root_module.keys():
            child_modules_resources = self._flatten_child_modules(
                root_module["child_modules"]
            )
            resources.extend(child_modules_resources)
        else:
            self._logger.debug(
                "Could not find 'child_modules' section under root module"
            )

        return resources

    @abstractmethod
    def flatten(self) -> Dict:
        """
        Traverses the file and returns all resources found.

        Parameters
        ----------
        None.

        Returns
        -------
        plan : Dict
        """
        pass


class PlanFlattener(Flattener):
    """
    A class that can be used to flatten Terraform plans in JSON format.

    ...

    Methods
    -------
    flatten() -> Dict :
        flattens the plan and returns the processed result
    """

    _plan: Any

    def __init__(self, plan: str, logger: Optional[Logger] = None) -> None:
        """
        Constructs all the necessary attributes for the PlanFlattener object.

        Parameters
        ----------
        plan : str
            the terraform plan in JSON format

        logger : logging.Logger, optional
            the logger object to be used
        """
        super().__init__(logger=logger)
        self._plan = loads(plan)

    def _flatten_providers(self) -> List:
        """
        Traverses the plan and creates a list with all providers found.

        Parameters
        ----------
        None.

        Returns
        -------
        providers : List
        """
        providers = []

        if "configuration" in self._plan.keys():
            configuration = self._plan["configuration"]

            if "provider_config" in configuration.keys():
                provider_config = configuration["provider_config"]

                for provider in provider_config.values():
                    provider_name = (
                        provider["name"] if "name" in provider.keys() else "unknown"
                    )
                    self._logger.debug(f"Adding provider: {provider_name}")
                    providers.append(deepcopy(provider))
            else:
                self._logger.warning(
                    "Plan does not have 'provider_config' section under 'configuration'"
                )
        else:
            self._logger.warning("Plan does not have 'configuration' section")

        return providers

    def flatten(self) -> Dict:
        """
        Traverses the plan and creates a new flattened plan with all resources and providers found.

        Parameters
        ----------
        None.

        Returns
        -------
        plan : Dict
        """
        self._logger.debug("Flattening providers")
        providers = self._flatten_providers()

        self._logger.debug("Flattening resources")
        resources = []

        if "planned_values" in self._plan.keys():
            planned_values = self._plan["planned_values"]

            if "root_module" in planned_values.keys():
                root_module = planned_values["root_module"]

                resources.extend(self._flatten_resources(root_module))
            else:
                self._logger.warning(
                    "Plan does not have 'root_module' section under 'planned_values'"
                )
        else:
            self._logger.warning("Plan does not have 'planned_values' section")

        return {"providers": providers, "resources": resources}


class StateFlattener(Flattener):
    """
    A class that can be used to flatten Terraform states in JSON format.

    ...

    Methods
    -------
    flatten() -> Dict :
        flattens the plan and returns the processed result
    """

    _state: Any

    def __init__(self, state: str, logger: Optional[Logger] = None) -> None:
        """
        Constructs all the necessary attributes for the StateFlattener object.

        Parameters
        ----------
        state : str
            the terraform plan in JSON format

        logger : logging.Logger, optional
            the logger object to be used
        """
        super().__init__(logger=logger)
        self._state = loads(state)

    def flatten(self) -> Dict:
        """
        Traverses the state and creates a new flattened state with all resources found.

        Parameters
        ----------
        None.

        Returns
        -------
        state : Dict
        """
        self._logger.debug("Flattening resources")
        resources = []

        if "values" in self._state.keys():
            values = self._state["values"]

            if "root_module" in values.keys():
                root_module = values["root_module"]

                resources.extend(self._flatten_resources(root_module))
            else:
                self._logger.warning("State does not have 'root_module' section")
        else:
            self._logger.warning("State does not have 'values' section")

        return {"resources": resources}

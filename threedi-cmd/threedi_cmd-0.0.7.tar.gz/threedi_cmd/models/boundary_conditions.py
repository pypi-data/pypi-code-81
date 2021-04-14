from typing import Dict
from pathlib import Path

from openapi_client import SimulationsApi, Upload
from openapi_client.models import FileBoundaryCondition

from .base import EventWrapper
from .waitfor import WaitForEventValidation


class WaitForFileBoundaryConditionsWrapper(WaitForEventValidation):
    api_class = SimulationsApi
    model = FileBoundaryCondition
    scenario_name = "waitforfileboundaryconditions"


class FileBoundaryConditionsWrapper(EventWrapper):
    api_class = SimulationsApi
    model = Upload
    api_path: str = "boundaryconditions_file"
    scenario_name = "fileboundaryconditions"
    filepath: Path = None

    def initialize_instance(self, data: Dict):
        self.filepath = Path(data.pop("filepath"))
        super().initialize_instance(data)

    @property
    def extra_steps(self):
        file_boundary_conditions = (
            self.api.simulations_events_boundaryconditions_file_list(
                simulation_pk=self.simulation.id
            )
        )
        for file_boundaryconditions in file_boundary_conditions.results:
            if file_boundaryconditions.file:
                file_boundaryconditions.file.filename == self.instance.filename
                bulk_event_instance = file_boundaryconditions
                break
        assert bulk_event_instance is not None

        wait_for_validation = WaitForFileBoundaryConditionsWrapper(
            data=bulk_event_instance.to_dict(),
            api_client=self._api_client,
            simulation=self.simulation,
        )
        return [wait_for_validation]


WRAPPERS = [
    WaitForFileBoundaryConditionsWrapper,
    FileBoundaryConditionsWrapper,
]

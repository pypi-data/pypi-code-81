from typing import Dict
from pathlib import Path

from openapi_client import SimulationsApi, UploadEventFile
from openapi_client.models import (
    ConstantLateral,
    TimeseriesLateral,
    FileLateral,
)
from .base import EventWrapper
from .waitfor import WaitForEventValidation


class WaitForConstantLateralWrapper(WaitForEventValidation):
    api_class = SimulationsApi
    model = ConstantLateral
    scenario_name = "waitforconstantlateral"


class WaitForTimeseriesLateralWrapper(WaitForEventValidation):
    api_class = SimulationsApi
    model = TimeseriesLateral
    scenario_name = "waitfortimeserieslateral"


class WaitForFileLateralWrapper(WaitForEventValidation):
    api_class = SimulationsApi
    model = FileLateral
    scenario_name = "waitforfilelateral"


class ConstantLateralWrapper(EventWrapper):
    api_class = SimulationsApi
    model = ConstantLateral
    api_path: str = "lateral_constant"
    scenario_name = "constantlateral"

    @property
    def extra_steps(self):
        wait_for_validation = WaitForConstantLateralWrapper(
            data=self.instance.to_dict(),
            api_client=self._api_client,
            simulation=self.simulation,
        )
        return [wait_for_validation]


class TimeseriesLateralWrapper(EventWrapper):
    api_class = SimulationsApi
    model = TimeseriesLateral
    api_path: str = "lateral_timeseries"
    scenario_name = "timeserieslateral"

    @property
    def extra_steps(self):
        wait_for_validation = WaitForTimeseriesLateralWrapper(
            data=self.instance.to_dict(),
            api_client=self._api_client,
            simulation=self.simulation,
        )
        return [wait_for_validation]


class FileLateralWrapper(EventWrapper):
    api_class = SimulationsApi
    model = UploadEventFile
    api_path: str = "lateral_file"
    scenario_name = "filelateral"
    filepath: Path = None

    def initialize_instance(self, data: Dict):
        self.filepath = Path(data.pop("filepath"))
        super().initialize_instance(data)

    @property
    def extra_steps(self):
        file_laterals = self.api.simulations_events_lateral_file_list(
            simulation_pk=self.simulation.id
        )
        for file_lateral in file_laterals.results:
            if file_lateral.file:
                file_lateral.file.filename == self.instance.filename
                bulk_event_instance = file_lateral
                break
        assert bulk_event_instance is not None

        wait_for_validation = WaitForFileLateralWrapper(
            data=bulk_event_instance.to_dict(),
            api_client=self._api_client,
            simulation=self.simulation,
        )
        return [wait_for_validation]


WRAPPERS = [
    WaitForConstantLateralWrapper,
    WaitForTimeseriesLateralWrapper,
    WaitForFileLateralWrapper,
    ConstantLateralWrapper,
    TimeseriesLateralWrapper,
    FileLateralWrapper,
]

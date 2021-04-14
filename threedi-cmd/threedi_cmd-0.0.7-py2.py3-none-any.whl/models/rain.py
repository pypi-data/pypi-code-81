from pathlib import Path
from typing import Dict
from openapi_client import SimulationsApi
from openapi_client.models import (
    ConstantRain,
    TimeseriesRain,
    LizardRasterRain,
    LizardTimeseriesRain,
    Upload,
    FileTimeseriesRain,
    FileRasterRain,
    NetCDFRasterRain,
    NetCDFTimeseriesRain,
    LocalRain,
)

from threedi_cmd.models.base import EventWrapper
from threedi_cmd.models.waitfor import WaitForProcessedFileWrapper


class ConstantRainWrapper(EventWrapper):
    api_class = SimulationsApi
    model = ConstantRain
    api_path: str = "rain_constant"
    scenario_name = "constantrain"


class LocalConstantRainWrapper(EventWrapper):
    api_class = SimulationsApi
    model = LocalRain
    api_path: str = "rain_local_constant"
    scenario_name = "localrainconstant"


class RainTimeseriesWrapper(EventWrapper):
    api_class = SimulationsApi
    model = TimeseriesRain
    api_path: str = "rain_timeseries"
    scenario_name = "timeseriesrain"


class LocalRainTimeseriesWrapper(EventWrapper):
    api_class = SimulationsApi
    model = LocalRain
    api_path: str = "rain_local_timeseries"
    scenario_name = "localraintimeseries"


class RainRasterLizardWrapper(EventWrapper):
    api_class = SimulationsApi
    model = LizardRasterRain
    api_path: str = "rain_rasters_lizard"
    scenario_name = "rainrasterlizard"


class RainTimeseriesLizardWrapper(EventWrapper):
    api_class = SimulationsApi
    model = LizardTimeseriesRain
    api_path: str = "rain_timeseries_lizard"
    scenario_name = "raintimeserieslizard"


class WaitForProcessedTimeseriesFileWrapper(WaitForProcessedFileWrapper):
    api_class = SimulationsApi
    model = FileTimeseriesRain
    scenario_name = "waitforraintimeseriesfile"


class WaitForRainTimeseriesNetCDFWrapper(
    WaitForProcessedTimeseriesFileWrapper
):
    model = NetCDFTimeseriesRain
    websocket_model_name = "NetCDFTimeseriesRain"
    scenario_name = "waitforraintimeseriesnetcdf"


class RainTimeseriesNetCDFWrapper(EventWrapper):
    api_class = SimulationsApi
    model = Upload
    api_path: str = "rain_timeseries_netcdf"
    scenario_name = "raintimeseriesnetcdf"
    filepath: Path = None

    def initialize_instance(self, data: Dict):
        self.filepath = Path(data.pop("filepath"))
        super().initialize_instance(data)

    @property
    def extra_steps(self):
        data = {
            "file": {"state": "processed", "filename": self.instance.filename},
            "timeout": 10,
        }
        wait_for_validation = WaitForRainTimeseriesNetCDFWrapper(
            data=data, api_client=self._api_client, simulation=self.simulation
        )
        return [wait_for_validation]


class WaitForProcessedRasterFileWrapper(WaitForProcessedFileWrapper):
    api_class = SimulationsApi
    model = FileRasterRain
    scenario_name = "waitforrainrasterfile"


class WaitForRainRasterNetCDFWrapper(WaitForProcessedRasterFileWrapper):
    model = NetCDFRasterRain
    websocket_model_name = "NetCDFRasterRain"
    scenario_name = "waitforrainrasternetcdf"


class RainRasterNetCDFWrapper(EventWrapper):
    api_class = SimulationsApi
    model = Upload
    api_path: str = "rain_rasters_netcdf"
    scenario_name = "rainrasternetcdf"
    filepath = None

    def initialize_instance(self, data: Dict):
        self.filepath = Path(data.pop("filepath"))
        super().initialize_instance(data)

    @property
    def extra_steps(self):
        data = {
            "file": {"state": "processed", "filename": self.instance.filename},
            "timeout": 10,
        }
        wait_for_validation = WaitForRainRasterNetCDFWrapper(
            data=data, api_client=self._api_client, simulation=self.simulation
        )
        return [wait_for_validation]


WRAPPERS = [
    ConstantRainWrapper,
    RainTimeseriesWrapper,
    RainRasterLizardWrapper,
    RainTimeseriesLizardWrapper,
    RainTimeseriesNetCDFWrapper,
    WaitForRainTimeseriesNetCDFWrapper,
    RainRasterNetCDFWrapper,
    WaitForRainTimeseriesNetCDFWrapper,
    LocalConstantRainWrapper,
    LocalRainTimeseriesWrapper,
]

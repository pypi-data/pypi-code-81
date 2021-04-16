from abc import ABC, abstractmethod
from collections import defaultdict
from configparser import ConfigParser
import functools
from pathlib import Path
import logging
from typing import Dict, List, Optional
from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath

try:
    from openapi_client.models import GeneralSettings
    from openapi_client.models import TimeStepSettings
    from openapi_client.models import NumericalSettings
    from openapi_client.models import AggregationSettings
    from openapi_client import SimulationsApi
    from openapi_client import ApiException
    from threedi_api_client import ThreediApiClient
    from openapi_client.models import SimulationSettingsOverview
except ImportError:
    msg = "You need to install the extra 'api' (e.g. 'pip install threedi-settings[api]') to be able to use the threedi-settings http module"  # noqa
    raise ImportError(msg)

from threedi_settings.mappings import (
    general_settings_map,
    time_step_settings_map,
    numerical_settings_map,
    aggregation_settings_map,
)
from threedi_settings.threedimodel_config import ThreedimodelIni
from threedi_settings.http.api_clients import OpenAPISimulationSettings

logger = logging.getLogger(__name__)


class OpenAPISimulationSettingsWriter(OpenAPISimulationSettings):
    def __init__(
        self,
        simulation_id: int,
        ini_file_path: Path,
        aggregation_file_path: Path,
        legacy_ini_file_path: Optional[Path],
    ):
        super().__init__(simulation_id)
        self.aggr_config = ConfigParser()
        self.ini_output_file = ini_file_path
        self.aggregation_file_path = aggregation_file_path
        self.legacy_conf = None
        if legacy_ini_file_path:
            legacy_ini = ThreedimodelIni(legacy_ini_file_path)
            self.config = legacy_ini.config
        else:
            self.config = ConfigParser()

    @functools.cached_property
    def settings(self):
        resp = self.retrieve()
        if not resp:
            return
        return resp

    def to_ini(self):
        if not self.settings:
            logger.error(
                "Cannot create ini file, could not fetch data from API"
            )
            return
        self._add(general_settings_map, self.settings.general_settings)
        self._add(time_step_settings_map, self.settings.time_step_settings)
        self._add(numerical_settings_map, self.settings.numerical_settings)
        with self.ini_output_file.open("w") as configfile:
            self.config.write(configfile)
        if not self.settings.aggregation_settings:
            logger.debug(
                "No aggregation settings defined for simulation %s ",
                self.simulation_id,
            )
            return
        self._add_aggregations()
        with self.aggregation_file_path.open("w") as aggregation_file:
            self.aggr_config.write(aggregation_file)

    def _add(self, settings_map: Dict, sub_setting):
        for attr_name, mapping in settings_map.items():
            value = getattr(sub_setting, attr_name)
            legacy_field_info, _ = mapping
            if legacy_field_info.ini_section not in self.config:
                self.config[legacy_field_info.ini_section] = {}
            self.config[legacy_field_info.ini_section][
                legacy_field_info.name
            ] = f"{value}"

    def _add_aggregations(self):
        for i, entry in enumerate(self.settings.aggregation_settings, start=1):
            for attr_name, mapping in aggregation_settings_map.items():
                value = getattr(entry, attr_name)
                legacy_field_info, _ = mapping
                if str(i) not in self.aggr_config:
                    self.aggr_config[str(i)] = {}
                self.aggr_config[str(i)][legacy_field_info.name] = f"{value}"

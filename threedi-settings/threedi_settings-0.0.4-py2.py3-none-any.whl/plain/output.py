import logging
from typing import Optional, Dict
from configparser import ConfigParser
from pathlib import Path

from threedi_settings.mappings import (
    general_settings_map,
    time_step_settings_map,
    numerical_settings_map,
    aggregation_settings_map,
)
from threedi_settings.models import SimulationConfig
from threedi_settings.threedimodel_config import ThreedimodelIni

logger = logging.getLogger(__name__)


class SimulationConfigWriter:
    """
    Writes a 'legacy' ini from a `SimulationConfig` object.
    A `SimulationConfig` instance usually holds simulation settings
    data retrieved from the 3Di API V3.
    """

    def __init__(
        self,
        simulation_config: SimulationConfig,
        ini_file_path: Path,
        aggregation_file_path: Path,
        legacy_ini_file_path: Optional[Path] = None,
    ):
        self.simulation_config = simulation_config
        assert (self.simulation_config is not None,
                "simulation_config must not be 'None'")
        self.aggr_config = ConfigParser()
        self.ini_output_file = ini_file_path
        self.aggregation_file_path = aggregation_file_path
        self.legacy_conf = None
        if legacy_ini_file_path:
            legacy_ini = ThreedimodelIni(legacy_ini_file_path)
            self.config = legacy_ini.config
        else:
            self.config = ConfigParser()

    def to_ini(self):
        """
        produces a 'legacy style' ini file. Fields that exist in the
        legacy file but do not in the API, are populated with defaults defined
        in the mapping module.
        """
        if self.simulation_config.aggregation_config:
            self._add_aggregations()
            with self.aggregation_file_path.open("w") as aggregation_file:
                self.aggr_config.write(aggregation_file)
        else:
            logger.debug(
                "No aggregation settings defined for simulation %s ",
                self.simulation_config.sim_uid,
            )

        self._add(general_settings_map, self.simulation_config.general_config)
        self._add(
            time_step_settings_map, self.simulation_config.time_step_config
        )
        self._add(
            numerical_settings_map, self.simulation_config.numerical_config
        )
        self._update_aggregation_path()
        with self.ini_output_file.open("w") as configfile:
            self.config.write(configfile)

    def _add(self, settings_map: Dict, sub_setting):
        """
        converts settings values from API type to 'legacy' type and adds them
        to the config instance under their 'legacy' section.
        """
        for attr_name, mapping in settings_map.items():
            value = getattr(sub_setting, attr_name)
            legacy_field_info, api_field_info, _ = mapping
            if legacy_field_info.ini_section not in self.config:
                self.config[legacy_field_info.ini_section] = {}
            if legacy_field_info.type != api_field_info:
                value = legacy_field_info.type(value)
            self.config[legacy_field_info.ini_section][
                legacy_field_info.name
            ] = f"{value}"

    def _add_aggregations(self):
        """
        converts aggregation settings values from API type to 'legacy' type
        and adds them to the aggr_config instance
        """
        for i, entry in enumerate(
            self.simulation_config.aggregation_config, start=1
        ):
            for attr_name, mapping in aggregation_settings_map.items():
                value = getattr(entry, attr_name)
                legacy_field_info, _, _ = mapping
                if str(i) not in self.aggr_config:
                    self.aggr_config[str(i)] = {}
                self.aggr_config[str(i)][legacy_field_info.name] = f"{value}"

    def _update_aggregation_path(self):
        if (
            not self.aggregation_file_path.exists()
            or not self.aggregation_file_path.is_file()
        ):
            return
        self.config["output"][
            "aggregation_settings"
        ] = self.aggregation_file_path.resolve().as_posix()

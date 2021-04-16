# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from collections import defaultdict
import logging
from typing import Dict, List, Optional, Union
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
from threedi_settings.models import (
    NumericalConfig,
    TimeStepConfig,
    GeneralSimulationConfig,
    AggregationConfig,
    SimulationConfig,
    SourceTypes,
)
from . import api_config

logger = logging.getLogger(__name__)


OpenApiSettingsModel = Union[
    GeneralSettings,
    TimeStepSettings,
    NumericalSettings
]


class OpenApiSimulationClient:
    """
    Interface to the threedi-api-client.
    """
    def __init__(self, simulation_id: int):
        self.simulation_id = simulation_id
        _api_client = ThreediApiClient(config=api_config)
        self.api_client = SimulationsApi(_api_client)


class BaseOpenAPI(ABC, OpenApiSimulationClient):
    """Base class to interact with 3Di settings resources"""
    def __init__(
        self,
        simulation_id: int,
        config_dict: Dict,
        openapi_model: OpenApiSettingsModel,
        mapping: Dict,
        source_type: SourceTypes,
    ):
        super().__init__(simulation_id)
        self.config_dict = config_dict
        self.model = openapi_model
        self.mapping = mapping
        self._instance: OpenApiSettingsModel = None
        self.source_type = source_type

    @property
    def instance(self) -> OpenApiSettingsModel:
        """
        Converts the settings stored in `config_dict` conform the definitions
        in `mapping` and returns a populated `OpenApiSettingsModel` instance.
        """
        data = {}
        exclude = {
            "url",
            "id",
        }
        for name in self.model.openapi_types.keys():
            if name.lower() in exclude:
                continue
            if name == "simulation_id":
                data[name] = self.simulation_id
                continue
            ini_field_info, api_field_info, sqlite_field_info = self.mapping[name]
            if self.source_type == SourceTypes.ini_file:
                field_info = ini_field_info
            elif self.source_type == SourceTypes.sqlite_file:
                field_info = sqlite_field_info
            else:
                raise TypeError("input_type must be either ini or sqlite")
            value = self.config_dict[field_info.name]
            try:
                value = field_info.type(value)
                if api_field_info.type != field_info.type:
                    try:
                        value = api_field_info.type(value)
                    except Exception:
                        raise
            except (ValueError, TypeError) as err:
                logger.info(
                    "Using default value %s for %s",
                    api_field_info.default, name
                )
                value = api_field_info.default
            data[name] = value
        return self.model(**data)

    @property
    @abstractmethod
    def create_method_name(self) -> str:
        """name of the openapi client method to create a resource"""
        ...

    def _create_method(self):
        """
        :returns create method
        :raises AttributeError if the create_method_name is not known
        """
        try:
            return getattr(self.api_client, self.create_method_name)
        except AttributeError:
            raise AttributeError(
                f"Create method '{self.create_method_name}' unknown"
            )

    def create(self) -> Optional[OpenApiSettingsModel]:
        create = self._create_method()
        try:
            resp = create(self.simulation_id, self.instance)
        except ApiException as err:
            logger.error(
                "Could not create resource %s. Server response: %s",
                self.model.__name__,
                err,
            )
            return
        logger.info(
            "Successfully created resource %s. Server response: %s ",
            self.model.__name__,
            resp,
        )
        return resp


class OpenAPIGeneralSettings(BaseOpenAPI):
    def __init__(self, simulation_id: int, config: Dict, settings_source: SourceTypes):
        super().__init__(
            simulation_id, config, GeneralSettings, general_settings_map, settings_source
        )

    @property
    def create_method_name(self):
        return "simulations_settings_general_create"


class OpenAPITimeStepSettings(BaseOpenAPI):
    def __init__(self, simulation_id: int, config: Dict, settings_source: SourceTypes):
        super().__init__(
            simulation_id, config, TimeStepSettings, time_step_settings_map, settings_source
        )

    @property
    def create_method_name(self) -> str:
        return "simulations_settings_time_step_create"


class OpenAPINumericalSettings(BaseOpenAPI):
    def __init__(self, simulation_id: int, config: Dict, settings_source: SourceTypes):
        super().__init__(
            simulation_id, config, NumericalSettings, numerical_settings_map, settings_source
        )

    @property
    def create_method_name(self) -> str:
        return "simulations_settings_numerical_create"


class OpenAPIAggregationSettings(OpenApiSimulationClient):
    def __init__(self, simulation_id: int, config: Dict):
        super().__init__(simulation_id)
        self.config_dict = config
        self.model = AggregationSettings
        self.mapping = aggregation_settings_map
        self._instances = []

    @property
    def create_method_name(self) -> str:
        return "simulations_settings_aggregation_create"

    @property
    def instances(self) -> List[AggregationSettings]:
        if self._instances:
            return self._instances

        data = defaultdict(str)
        exclude = {
            "url",
            "name",
        }
        for k, d in self.config_dict.items():
            for name in self.model.openapi_types.keys():
                if name.lower() in exclude:
                    continue
                if name == "simulation_id":
                    data[name] = self.simulation_id
                    continue
                ini_field_info, api_field_info, sqlite_info = self.mapping[name]
                data[name] = d[ini_field_info.name]
            self._instances.append(self.model(**data))
        return self._instances

    def create(self) -> List[AggregationSettings]:
        try:
            create = getattr(self.api_client, self.create_method_name)
        except AttributeError:
            raise AttributeError(
                f"Create method '{self.create_method_name}' unknown"
            )
        responses = []
        for instance in self.instances:
            try:
                resp = create(self.simulation_id, instance)
            except ApiException as err:
                logger.error(
                    "Could not create resource %s. Server response: %s",
                    self.model.__name__,
                    err,
                )
                continue
            logger.info(
                "Successfully created resource %s. Server response: %s ",
                self.model.__name__,
                resp,
            )
            responses.append(resp)
        return responses


class OpenAPISimulationSettings(OpenApiSimulationClient):
    def __init__(self, simulation_id):
        super().__init__(simulation_id)
        self._simulation_config = None

    def retrieve(self) -> Optional[SimulationSettingsOverview]:
        """
        get the simulation settings from the 3Di API V3

        :returns `None` if any ApiException has been raised
        """
        try:
            return self.api_client.simulations_settings_overview(
                self.simulation_id
            )
        except ApiException as err:
            logger.error(
                "Could not retrieve settings information for simulation %s: "
                "Response: %s",
                self.simulation_id,
                err,
            )
            return

    @property
    def simulation_config(self) -> Optional[SimulationConfig]:
        if self._simulation_config:
            return self._simulation_config

        resp = self.retrieve()
        if not resp:
            return

        attr_names = [
            "general_settings",
            "time_step_settings",
            "numerical_settings",
        ]
        d = {}
        uid = ""
        sim_uid = ""
        for name in attr_names:
            try:
                tmp_d = getattr(resp, name).to_dict()
            except AttributeError:
                logger.debug("No %s api settings found", name)
                return
            uid = str(tmp_d.pop("id"))
            sim_uid = str(tmp_d.pop("simulation_id"))
            d[name] = tmp_d
        general_settings = GeneralSimulationConfig(
            uid=uid, sim_uid=sim_uid, **d["general_settings"]
        )
        time_step_settings = TimeStepConfig(
            uid=uid, sim_uid=sim_uid, **d["time_step_settings"]
        )
        numerical_settings = NumericalConfig(
            uid=uid, sim_uid=sim_uid, **d["numerical_settings"]
        )
        aggregation_settings = self._get_aggregations(resp, sim_uid)
        self._simulation_config = SimulationConfig(
            uid=uid,
            sim_uid=sim_uid,
            general_config=general_settings,
            time_step_config=time_step_settings,
            numerical_config=numerical_settings,
            aggregation_config=aggregation_settings,
        )
        return self._simulation_config

    def _get_aggregations(
        self,
        resp: SimulationSettingsOverview,
        sim_uid: str
    ) -> List:
        """
        extract the aggregation settings from the response data
        """
        aggregations = []
        for aggr_setting in resp.aggregation_settings:
            tmp_d = aggr_setting.to_dict()
            url_path = PurePosixPath(unquote(urlparse(tmp_d.pop("url")).path))
            ac = AggregationConfig(uid=url_path.name, sim_uid=sim_uid, **tmp_d)
            aggregations.append(ac)
        return aggregations

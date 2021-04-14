from .base import SettingsWrapper
from openapi_client import SimulationsApi
from openapi_client.models import (
    GeneralSettings,
    NumericalSettings,
    TimeStepSettings,
    AggregationSettings
)


class GeneralSettingsWrapper(SettingsWrapper):
    api_class = SimulationsApi
    model = GeneralSettings
    api_path: str = "general"
    scenario_name = "generalsettings"


class NumercialSettingsWrapper(SettingsWrapper):
    api_class = SimulationsApi
    model = NumericalSettings
    api_path: str = "numerical"
    scenario_name = "numericalsettings"


class TimeStepSettingsWrapper(SettingsWrapper):
    api_class = SimulationsApi
    model = TimeStepSettings
    api_path: str = "time_step"
    scenario_name = "timestepsettings"


class AggregationSettingsWrapper(SettingsWrapper):
    api_class = SimulationsApi
    model = AggregationSettings
    api_path: str = "aggregation"
    scenario_name = "aggregationsettings"


WRAPPERS = [
    GeneralSettingsWrapper,
    NumercialSettingsWrapper,
    TimeStepSettingsWrapper,
    AggregationSettingsWrapper
]

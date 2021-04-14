from openapi_client import SimulationsApi
from openapi_client.models import (
    ConstantWind,
    TimeseriesWind,
    WindDragCoefficient,
)
from .base import EventWrapper, InitialWrapper


class WindDragCoefficientWrapper(InitialWrapper):
    api_class = SimulationsApi
    model = WindDragCoefficient
    api_path = "wind_drag_coefficient"
    scenario_name = "winddragcoefficient"


class ConstantWindWrapper(EventWrapper):
    api_class = SimulationsApi
    model = ConstantWind
    api_path: str = "wind_constant"
    scenario_name = "constantwind"


class TimeseriesWindWrapper(EventWrapper):
    api_class = SimulationsApi
    model = TimeseriesWind
    api_path: str = "wind_timeseries"
    scenario_name = "timeserieswind"


WRAPPERS = [
    WindDragCoefficientWrapper,
    ConstantWindWrapper,
    TimeseriesWindWrapper,
]

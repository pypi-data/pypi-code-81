from openapi_client import SimulationsApi
from openapi_client.models import Breach
from .base import EventWrapper


class BreachWrapper(EventWrapper):
    api_class = SimulationsApi
    model = Breach
    api_path: str = "breaches"
    scenario_name = "breach"


WRAPPERS = [BreachWrapper]

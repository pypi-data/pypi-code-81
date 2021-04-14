from .base import ModelWrapper
from openapi_client.api import SimulationsApi
from openapi_client.models import Simulation


class SimulationWrapper(ModelWrapper):
    api_class = SimulationsApi
    model = Simulation
    api_path = "simulations"
    scenario_name = "simulation"

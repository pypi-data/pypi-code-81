from .base import SimulationChildWrapper
from openapi_client import SimulationsApi
from openapi_client.models import TimedSavedStateUpdate, InitialSavedState
from .base import InitialWrapper


class TimedSavedStateWrapper(SimulationChildWrapper):
    api_class = SimulationsApi
    model = TimedSavedStateUpdate
    api_path: str = "create_saved_states_timed"
    scenario_name = "timedsavedstate"


class InitialSavedStateWrapper(InitialWrapper):
    api_class = SimulationsApi
    model = InitialSavedState
    api_path: str = "saved_state"
    scenario_name = "initialsavedstate"


WRAPPERS = [TimedSavedStateWrapper, InitialSavedStateWrapper]

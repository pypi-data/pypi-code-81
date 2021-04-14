from .base import EventWrapper
from openapi_client import SimulationsApi
from openapi_client.models import TimedStructureControl

from threedi_cmd.models.waitfor import (
    WaitForEventValidation,
    match_validated_event,
)


class WaitForStructureControlWrapper(WaitForEventValidation):
    api_class = SimulationsApi
    model = TimedStructureControl
    scenario_name = "waitforstructurecontrol"

    def matches(self, websocket_instance):
        return match_validated_event(websocket_instance, self)


class StructureControlWrapper(EventWrapper):
    api_class = SimulationsApi
    model = TimedStructureControl
    api_path: str = "structure_control_timed"
    scenario_name = "structurecontroltimed"

    @property
    def extra_steps(self):
        wait_for_validation = WaitForStructureControlWrapper(
            data=self.instance.to_dict(),
            api_client=self._api_client,
            simulation=self.simulation,
        )
        return [wait_for_validation]


WRAPPERS = [StructureControlWrapper, WaitForStructureControlWrapper]

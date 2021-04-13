from palaestrai.core.protocol import MuscleUpdateResponse
from .brain import Brain


class DummyBrain(Brain):
    def __init__(
        self,
        muscle_connection,
        sensors,
        actuators,
        objective,
        seed: int,
        max_buffer=0,
    ):
        super().__init__(
            muscle_connection, sensors, actuators, objective, seed, max_buffer
        )

    def thinking(self, muscle_id, readings, actions, reward, done):
        response = MuscleUpdateResponse(False, None)
        return response

from __future__ import annotations
from typing import List, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from palaestrai.agent import SensorInformation, ActuatorInformation


@dataclass
class AgentUpdateRequest:
    """Provides fresh data from a :class:`SimulationController` to
    an :class:`Agent`.

    * Sender: :class:`SimulationController`
    * Receiver: :class:`Muscle`

    :param sender_simulation_controller: The sending
        :class:`SimulationController`
    :param receiver_agent_id: The receiving agent, e.g., a :class:`Muscle`
    :param experiment_run_id: ID of the experiment run this update is part of
    :param actuators: List of actuators available for the agent
    :param sensors: Sensor input data for the agent
    :param reward: Current reward from the environment
    :param is_terminal: Indicates whether this is the last update from the
        environment or not
    """

    sender_simulation_controller_id: str
    receiver_agent_id: str
    experiment_run_id: str
    actuators: List[ActuatorInformation]
    sensors: List[SensorInformation]
    reward: List[float]
    is_terminal: bool

    @property
    def sender(self):
        return self.sender_simulation_controller_id

    @property
    def receiver(self):
        return self.receiver_agent_id

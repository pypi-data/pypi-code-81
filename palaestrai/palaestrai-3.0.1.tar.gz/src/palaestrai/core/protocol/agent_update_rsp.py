from __future__ import annotations
from typing import List, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from palaestrai.agent import SensorInformation, ActuatorInformation


@dataclass
class AgentUpdateResponse:
    """Responds after an agent has acted via its :class:`Muscle`

    * Sender: :class:`Muscle`
    * Receiver: :class:`SimulationController`

    :param sender_agent_id: ID of the sending agent, e.g., a :class:`Muscle`
    :param receiver_simulation_controller_id: ID of the receiving
        :class:`SimulationController`
    :param experiment_run_id: ID of the experiment run we participate in
    :param sensor_information: list of sensor readings
        :class:`SensorInformation`
    :param actuator_information: list of actuator actions via
        :class:`ActuatorInformation`
    :param rewards: List of rewards
    """

    sender_agent_id: str
    receiver_simulation_controller_id: str
    experiment_run_id: str
    sensor_information: List[SensorInformation]
    actuator_information: List[ActuatorInformation]
    rewards: List[float]

    @property
    def sender(self):
        return self.sender_agent_id

    @property
    def receiver(self):
        return self.receiver

    @property
    def actuators(self):
        return self.actuator_information

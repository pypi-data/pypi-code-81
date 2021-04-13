from __future__ import annotations
from dataclasses import dataclass
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from palaestrai.agent import SensorInformation, ActuatorInformation


@dataclass
class AgentSetupRequest:
    """Initializes the setup of an :class:`Agent`.

    * Sender: :class:`SimulationController`
    * Receiver: :class:`AgentConductor`

    :param sender_simulation_controller: ID of the sending
        :class:`SimulationController`
    :param receiver_agent_conductor: ID of the receiving
        :class:`AgentConductor`
    :param experiment_run_id: ID of the experiment run the agent participates
        in
    :param agent_id: ID of the agent we're setting up (e.g., a :class:`Muscle`)
    :param sensors: List of :class:`SensorInformation` objects for the
        sensors available to the agent
    :param actuators: List of :class:`ActuatorInformation` objects for the
        actuators available to the agent
    :param agent_name: Name of the :class:`Agent`, if any
    """

    sender_simulation_controller: str
    receiver_agent_conductor: str
    experiment_run_id: str
    agent_id: str
    sensors: List[SensorInformation]
    actuators: List[ActuatorInformation]
    agent_name: str

    @property
    def sender(self):
        return self.sender_simulation_controller

    @property
    def receiver(self):
        return self.receiver_agent_conductor

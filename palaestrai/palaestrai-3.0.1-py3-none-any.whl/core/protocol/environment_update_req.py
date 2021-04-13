from __future__ import annotations
from dataclasses import dataclass
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from palaestrai.agent import ActuatorInformation


@dataclass
class EnvironmentUpdateRequest:
    """Updates an environment with new set points from actuators.

    * Sender: :class:`SimulationController`
    * Receiver: :class:`Environment`

    :param sender_simulation_controller: ID of the sending
        :class:`SimulationController`
    :param receiver_environment: ID of the receiving environment
    :param experiment_run_id: ID of the current experiment run this environment
        participates in
    :param environment_conductor_id: ID of the :class:`EnvironmentConductor`
        the environment belongs to
    :param actuators: list of :class:`ActuatorInformation` objects that convey
        new setpoints to the environment
    """

    sender_simulation_controller: str
    receiver_environment: str
    experiment_run_id: str
    environment_conductor_id: str
    actuators: List[ActuatorInformation]

    @property
    def sender(self):
        return self.sender_simulation_controller

    @property
    def receiver(self):
        return self.receiver_environment

    @property
    def environment_id(self):
        return self.receiver_environment

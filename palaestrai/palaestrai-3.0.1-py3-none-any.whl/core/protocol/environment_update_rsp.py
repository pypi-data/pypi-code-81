from __future__ import annotations
from dataclasses import dataclass
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from palaestrai.agent import SensorInformation


@dataclass
class EnvironmentUpdateResponse:
    """Reports the current state of the environment.

    * Sender: :class:`Environment`
    * Receiver: :class:`SimulationController

    :param sender_environment_id: ID of the sending :class:`Environment`
    :param receiver_simulation_controller_id: ID of the receiving
        :class:`SimulationController`
    :param experiment_run_id: ID of the current experiment run the environment
        participates in
    :param environment_conductor_id: ID of the :class:`EnvironmentConductor`
        the environment belongs to
    :param sensors: Current list of sensor data
    :param reard: Reward given by the environment
    :param is_terminal: Indicates whether the environment has reached
        a terminal state
    """

    sender_environment_id: str
    receiver_simulation_controller_id: str
    experiment_run_id: str
    environment_conductor_id: str
    sensors: List[SensorInformation]
    reward: float
    is_terminal: bool

    @property
    def sender(self):
        return self.sender_environment_id

    @property
    def receiver(self):
        return self.receiver_simulation_controller_id

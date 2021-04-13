from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from palaestrai.agent import SensorInformation


@dataclass
class MuscleUpdateRequest:
    """Notifies the :class:`Brain` that a :class:`Muscle` of an action.

    * Sender: A :class:`Muscle` after acting
    * Receiver: The :class:`Brain`

    :param sender_muscle_id: ID of the sending :class:`Muscle`
    :param receiver_brain_id: ID of the receiving :class:`Brain`
    :param experiment_run_id: ID of the experiment run this action happened in
    :param agent_id: ID of the :class:`Agent` muscle and brain belong to
    :param sensor_readings: A list of sensor readings on which the muscle
        acted
    :param last_actions: A list of actions the muscle proposed to do last
    :param reward: Reward received from the last action
    :param is_terminal: Indicates whether this was the last action as the
        environment (or agent) are done
    :param shutdown: Indiciates system shutdown
    """

    sender_muscle_id: str
    receiver_brain_id: Optional[str]
    experiment_run_id: str
    agent_id: str
    # sensor_readings: Optional[List[SensorInformation]]
    # last_actions: Optional[List]
    # reward: Optional[float]
    sensor_readings: List[SensorInformation]
    last_actions: List
    reward: List[float]
    is_terminal: bool
    shutdown: bool

    @property
    def sender(self):
        return self.sender_muscle_id

    @property
    def receiver(self):
        return self.receiver_brain_id

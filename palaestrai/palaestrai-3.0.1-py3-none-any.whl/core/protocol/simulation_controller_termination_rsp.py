import dataclasses
from typing import Union


@dataclasses.dataclass
class SimulationControllerTerminationResponse:
    """Acknowledges the termination of a :py:class:`SimulationController`.

    * Sender: :py:class:`RunGovernor`
    * Receiver: :py:class:`SimulationController`

    :param sender_run_governor_id: Opaque ID of the sending
        :py:class:`RunGovernor` instance
    :param receiver_simulation_controller_id: Opaque ID of the receiving
        :py:class:`SimulationController` instance
    :param complete_shutdown: If `True`, the message indicates that the
        :py:class:`RunGovernor` is now shutting down the whole run.
    """

    sender_run_governor_id: str
    receiver_simulation_controller_id: str
    experiment_run_id: Union[str, None]
    complete_shutdown: bool

    @property
    def sender(self):
        return self.sender_run_governor_id

    @property
    def receiver(self):
        return self.receiver_simulation_controller_id

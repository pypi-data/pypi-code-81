from dataclasses import dataclass


@dataclass
class EnvironmentSetupResponse:
    """Signals successful environment setup and delivers environment parameters

    * Sender: :class:`EnvironmentConductor´
    * Receiver: :class:`SimulationController`

    :param sender_environment_conductor: ID of the sending
        :class:`EnvironmentConductor`
    :param receiver_simulation_controller: ID of the receiving
        :class:`SimulationController`
    :param experiment_run_id: ID of the experiment run
    :param environment_id: ID of the newly setup environment
    :param environment_parameters: All parameters that describe the
        environment that has just been set up
    """

    environment_id: str
    experiment_run_id: str
    sender_environment_conductor: str
    receiver_simulation_controller: str
    environment_type: str
    environment_parameters: dict

    @property
    def sender(self):
        return self.sender_environment_conductor

    @property
    def receiver(self):
        return self.receiver_simulation_controller

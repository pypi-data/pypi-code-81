from dataclasses import dataclass


@dataclass
class EnvironmentSetupRequest:
    """Instructs an :class:`EnvironmentConductor` to initialize
    its :class:`Environment`

    * Sender: :class:`SimulationController`
    * Receiver: :class:`EnvironmentConductor`

    :param environment_id: ID of the :class:`Environment` to initialize
    :param experiment_run_id: ID of the experiment run for which the
        environment is set up
    :param sender_simulation_controller_id: The sending
        :class:`SimulationController`
    :param receiver_environment_conductor_id: Target
        :class:`EnvironmentConductor`
    """

    environment_id: str
    experiment_run_id: str
    sender_simulation_controller_id: str
    receiver_environment_conductor_id: str

    @property
    def environment_conductor_id(self):
        return self.receiver_envionrment_conductor_id

    @property
    def sender_id(self):
        return self.sender_simulation_controller_id

    @property
    def receiver(self):
        return self.receiver_envionrment_conductor_id

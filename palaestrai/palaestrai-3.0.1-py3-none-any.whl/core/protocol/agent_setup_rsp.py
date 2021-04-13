from dataclasses import dataclass


@dataclass
class AgentSetupResponse:
    """Response to a successful agent setup

    * Sender: :class:`AgentConductor`
    * Receiver: :class:`SimulationController`

    :param sender_agent_conductor: ID of the transmitting
        :class:`AgentConductor`
    :param receiver_simulation_controller: ID of the receiving
        :class:`SimulationController`
    :param experiment_run_id: ID of the experiment run this agent will
        participate in
    :param agent_id: ID of the respective :class:`Agent` we've just set up
    """

    sender_agent_conductor: str
    receiver_simulation_controller: str
    experiment_run_id: str
    agent_id: str

    @property
    def sender(self):
        return self.sender_agent_conductor

    @property
    def receiver(self):
        return self.receiver_simulation_controller

class SimulationStartRequest:
    """Requests a :class:`SimulationController` to start a simulation run.

    * Sender: :class:`RunGovernor`
    * Receiver: :class:`SimulationController`

    :param run_governor_id: ID of the :class:`RunGovernor` that requests the
        simulation start (i.e., parent of the :class:`SimulationController`)
    :param simulation_controller_id: Target :class:`SimulationController`
    :param experiment_run_id: ID of the experiment run being conducted
    """

    def __init__(
        self, run_governor_id, simulation_controller_id, experiment_run_id
    ):
        self.run_governor_id = run_governor_id
        self.experiment_run_id = experiment_run_id
        self.simulation_controller_id = simulation_controller_id

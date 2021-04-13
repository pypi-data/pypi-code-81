from typing import TYPE_CHECKING

from palaestrai.core.protocol import (
    ExperimentStartRequest,
    ExperimentStartResponse,
)

if TYPE_CHECKING:
    from palaestrai.experiment import RunGovernor

from palaestrai.util.exception import (
    ExperimentAlreadyRunningError,
    ExperimentSetupFailedError,
)

from . import LOG, RunGovernorState


class RGSStarting(RunGovernorState):
    """Represent the STARTING_EXPERIMENT state of the run governor.

    This state is entered if an ExperimentStartRequest was received in
    the TRANSCEIVING state. During this state, the
    ExperimentStartRequest is checked against a possibly already
    running experiment. If no experiment is running, the setup of the
    experiment is executed.

    In any case, an ExperimentStartResponse is prepared and stored as
    next_reply in the run governor.

    Possible next states are
    * :class:`.RGSStartinSimControllers in the normal case.
    * :class:`.RGSErrorHandlingStarting in the error case.

    Parameters
    ----------
    rgc: :class:`.RunGovernor`
        The run governor instance that provides the context for this
        state.

    """

    def __init__(self, rgc: "RunGovernor"):
        super().__init__(rgc, "STARTING_EXPERIMENT")

    async def run(self):
        request = self.rgc.last_request.pop()

        if self._is_experiment_running(request):
            return

        await self._experiment_start(request)

    def next_state(self):
        from . import RGSErrorHandlingStarting, RGSStartingSimControllers

        if len(self.rgc.errors) > 0:
            self.rgc.state = RGSErrorHandlingStarting(self.rgc)
        else:
            self.rgc.state = RGSStartingSimControllers(self.rgc)

    def _is_experiment_running(self, request: ExperimentStartRequest) -> bool:
        """Check if an experiment is already running.

        Adds an ExperimentAlreadyRunningError to the run governor error
        stack if an experiment is already running.

        Returns
        -------
        bool
            True, if an experiment is already running, False otherwise.

        """
        if self.rgc.experiment is not None:
            LOG.warning(
                "RunGovernor(id=0x%x, uid=%s) received request to start "
                "Experiment(id=%s), but this is recorded as already running.",
                id(self.rgc),
                self.rgc.uid,
                request.experiment_run_id,
            )
            self.rgc.next_reply.append(
                ExperimentStartResponse(
                    experiment_run_id=self.rgc.experiment_run_id,
                    successful=False,
                    error="Experiment is already active",
                )
            )
            self.add_error(ExperimentAlreadyRunningError())
            return True
        return False

    async def _experiment_start(self, request: ExperimentStartRequest):
        """Start an experiment.

        This function starts the experiment by receiving an
        ExperimentStartRequest. Adds an ExperimentSetupFailedError
        if an error occured during setup().

        Parameters
        ----------
        request: :class:`.ExperimentStartRequest`
            The instance of the start request with information about
            the experiment to start

        """
        successful = True
        msg = None

        # TODO: WTF copy
        self.rgc.experiment = request.experiment
        self.rgc.experiment_run_id = request.experiment_run_id
        try:
            self.rgc.experiment.setup(self.rgc.broker_uri)
        except Exception as e:
            self.add_error(ExperimentSetupFailedError())
            msg = e
            successful = False
        self.rgc.termination_condition = (
            self.rgc.experiment.run_governor_termination_condition
        )

        self.rgc.next_reply.append(
            ExperimentStartResponse(
                request.experiment_run_id, successful=successful, error=msg
            )
        )

import asyncio
from typing import TYPE_CHECKING

from palaestrai.core.protocol import (
    ExperimentShutdownResponse,
    SimulationStopRequest,
    SimulationStopResponse,
)

from . import LOG, RunGovernorState

if TYPE_CHECKING:
    from palaestrai.experiment import RunGovernor


class RGSStoppingSimulation(RunGovernorState):
    """Represents the STOPPING_SIMULATION state.

    This state is entered after the EXPERIMENT_RUNNING state if the run
    governor receives an experiment shutdown request. In this state, a
    reply is prepared and passed to the next state.

    Possible next states are
    * :class:`.RGSStoppingTransceiving in the normal case.
    (* ABORTING (error case), not handled yet)

    Parameters
    ----------
    ctx: :class:`.RunGovernor`
        The run governor instance that provides the context for this
        state.
    request: :class:`.ExperimentShutdownRequest`
        The experiment shutdown request that leads to this state.

    """

    def __init__(self, rgc: "RunGovernor"):
        super().__init__(rgc, "STOPPING_SIMULATION")

    async def run(self):
        if len(self.rgc.errors) > 0:
            timeout = 5
        else:
            timeout = None
        try:
            sc_terminated = await asyncio.wait_for(
                self._terminate_sim_controllers(), timeout
            )
            self._prepare_reply(sc_terminated)
        except asyncio.exceptions.TimeoutError:
            LOG.warning(
                "RunGovernor(id=0x%x, uid=%s) "
                "encountered a timeout while waiting for the "
                "remaining processes to shut down orderly; "
                "killing them now.",
                id(self.rgc),
                self.rgc.uid,
            )

    def next_state(self, *args, **kwargs):
        from . import RGSStoppingTransceiving

        self.rgc.state = RGSStoppingTransceiving(self.rgc)

    async def _terminate_sim_controllers(self):
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) shutting down "
            "Experiment(id=%s, experiment_run_id=%s)",
            id(self.rgc),
            self.rgc.uid,
            self.rgc.experiment.id,
            self.rgc.experiment_run_id,
        )

        sc_terminated = []
        for sc_uid in self.rgc.sim_controllers:
            response = await self.rgc.major_domo_client.send(
                sc_uid, SimulationStopRequest()
            )
            if response is None or not isinstance(
                response, SimulationStopResponse
            ):
                self.rgc.sim_controllers[sc_uid].terminate()
                sc_terminated += [sc_uid]
                continue
            LOG.debug(
                "RunGovernor(id=0x%x, uid=%s) received "
                "SimulationStopResponse(experiment_run_id=%s); "
                "list of running experiments contains: %s",
                id(self.rgc),
                self.rgc.uid,
                response.experiment_run_id,
                self.rgc.sim_controllers.keys(),
            )
        return sc_terminated

    def _prepare_reply(self, sc_terminated):
        self.rgc.next_reply.append(
            ExperimentShutdownResponse(
                len(sc_terminated) == 0,
                None
                if len(sc_terminated) == 0
                else "Had to terminate: %s" % sc_terminated,
            )
        )

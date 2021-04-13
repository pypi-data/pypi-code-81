import io
import signal
import traceback
from typing import TYPE_CHECKING

import aiomultiprocess
import setproctitle
from palaestrai.util.exception import AgentConductorFailedError

from . import LOG, RunGovernorState

if TYPE_CHECKING:
    from palaestrai.agent import AgentConductor
    from palaestrai.experiment import RunGovernor


class RGSStartingAgentConductors(RunGovernorState):
    """Represent the STARTING_AGENT_CONDUCTORS state of the run
    governor.

    This state is entered after STARTING_ENV_CONDUCTORS succeeds.
    During this state, processes for all required agent conductors are
    created (but not started).

    Possible next states are
    * :class:`.RGSStartingRun in the normal case
    * :class:`.RGSErrorHandlingStarting in the error case

    Parameters
    ----------
    rgc: :class:`.RunGovernor`
        The run governor instance that provides the context for this
        state.


    """

    def __init__(self, rgc: "RunGovernor"):
        super().__init__(rgc, "STARTING_AGENT_CONDUCTORS")

    async def run(self):
        self._init_agent_conductors()

    def next_state(self, *args, **kwargs):
        from . import RGSErrorHandlingStarting, RGSStartingRun

        if len(self.rgc.errors) > 0:
            self.rgc.state = RGSErrorHandlingStarting(self.rgc)
        else:
            self.rgc.state = RGSStartingRun(self.rgc)

    def _init_agent_conductors(self):
        """Initializes and starts given agent conductors as subprocesses.

        All objects of type :py:class:`AgentConductor` are treated as
        subprocesses. As long as they run on the same machine, they are
        initialized in this method.

        The processes are not started.

        :param agent_conductors: A list containing all agent
            conductor objects
        :return: A dictionary mapping UID -> process of all started
            agent conductors.
        :rtype: dict[str, aiomultiprocess.Process]
        """
        agent_conductors = self.rgc.experiment.agent_conductors.values()
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) initializing %d agent conductors",
            id(self.rgc),
            self.rgc.uid,
            len(agent_conductors),
        )
        self.rgc.agent_conductors = {
            ac.uid: aiomultiprocess.Process(
                name=f"AgentConductor-{ac.uid}",
                target=self._run_agent_conductor,
                args=(ac,),
            )
            for ac in agent_conductors
        }

    async def _run_agent_conductor(self, agent_conductor: "AgentConductor"):
        """Executes the :py:class:`AgentConductor` main loop

        This is a wrapper function around :py:func:`AgentConductor.run`.
        It takes care of clearing signal handlers, setting the proctitle,
        and generally catching errors in a meaningful in order to report it
        to the RunGovernor without simply dying.

        :param agent_conductor: An initialized agent conductor,
            ready to be run.

        :returns: Whatever the :py:func:`AgentConductor.run`
            method returns.
        """
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGABRT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        setproctitle.setproctitle(
            "palaestrAI[AgentConductor-%s]" % agent_conductor.uid[-6:]
        )
        try:
            rc = await agent_conductor.run()
            LOG.debug(
                "RunGovernor(id=0x%x, uid=%s) "
                "saw AgentConductor(id=0x%x, uid=%s) "
                "exit normally",
                id(self.rgc),
                self.rgc.uid,
                id(agent_conductor),
                agent_conductor.uid,
            )
            return rc
        except Exception as e:
            LOG.critical(
                "RunGovernor(id=0x%x, uid=%s) "
                "encountered a fatal error while executing "
                "AgentConductor(id=0x%x, uid=%s): %s",
                id(self.rgc),
                self.rgc.uid,
                id(agent_conductor),
                agent_conductor.uid,
                e,
            )
            tb = io.StringIO()
            traceback.print_exc(file=tb)
            LOG.debug(
                "RunGovernor(id=0x%x, uid=%s) "
                "encountered a fatal error while executing "
                "AgentConductor(id=0x%x, uid=%s): %s",
                id(self.rgc),
                self.rgc.uid,
                id(agent_conductor),
                agent_conductor.uid,
                tb.getvalue(),
            )
            self.add_error(AgentConductorFailedError())
            raise e

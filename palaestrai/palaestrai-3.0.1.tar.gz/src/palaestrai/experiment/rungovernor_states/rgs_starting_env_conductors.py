import io
import signal
import traceback
from typing import TYPE_CHECKING

import aiomultiprocess
import setproctitle

if TYPE_CHECKING:
    from palaestrai.environment import EnvironmentConductor
    from palaestrai.experiment import RunGovernor

from palaestrai.util.exception import EnvConductorFailedError

from . import LOG, RunGovernorState


class RGSStartingEnvConductors(RunGovernorState):
    """Represent the STARTING_ENV_CONDUCTORS state of the run
    governor.

    This state is entered after STARTING_SIM_CONTROLLERS succeeds.
    During this state, processes for all required environment
    conductors are created (but not started).

    Possible next states are
    * :class:`.RGSStartingAgentConductors in the normal case
    * :class:`.RGSErrorHandlingStarting in the error case

    Parameters
    ----------
    rgc: :class:`.RunGovernor`
        The run governor instance that provides the context for this
        state.

    """

    def __init__(self, rgc: "RunGovernor"):
        super().__init__(rgc, "STARTING_ENV_CONDUCTORS")

    async def run(self):

        self._init_environment_conductors()

    def next_state(self):
        from . import RGSErrorHandlingStarting, RGSStartingAgentConductors

        if len(self.rgc.errors) > 0:
            self.rgc.state = RGSErrorHandlingStarting(self.rgc)
        else:
            self.rgc.state = RGSStartingAgentConductors(self.rgc)

    def _init_environment_conductors(self):
        """Initializes and starts given environment conductors as subprocesses.

        All objects of type :py:class:`EnvironmentConductor` are treated as
        subprocesses. As long as they run on the same machine, they are
        initialized in this method.

        The processes are not started.

        :param environment_conductors: A list containing all environment
            conductor objects
        :return: A dictionary mapping UID -> process object.
        :rtype: Dict[str, aiomultiprocess.Process]
        """
        environment_conductors = (
            self.rgc.experiment.environment_conductors.values()
        )
        LOG.debug(
            "RunGovernor(id=0x%x, uid=%s) initializing "
            "%d environment conductors",
            id(self.rgc),
            self.rgc.uid,
            len(environment_conductors),
        )
        self.rgc.env_conductors = {
            ec.uid: aiomultiprocess.Process(
                name=f"EnvironmentConductor-{ec.uid}",
                target=self._run_environment_conductor,
                args=(ec,),
            )
            for ec in environment_conductors
        }

    async def _run_environment_conductor(
        self, environment_conductor: "EnvironmentConductor"
    ):
        """Executes the :py:class:`EnvironmentConductor` main loop

        This is a wrapper function around :py:func:`EnvironmentConductor.run`.
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
            "palaestrAI[EnvironmentConductor-%s]"
            % environment_conductor.uid[-6:]
        )
        try:
            rc = await environment_conductor.run()
            LOG.debug(
                "RunGovernor(id=0x%x, uid=%s) "
                "saw EnvironmentConductor(id=0x%x, uid=%s) "
                "exit normally",
                id(self.rgc),
                self.rgc.uid,
                id(environment_conductor),
                environment_conductor.uid,
            )
            return rc
        except Exception as e:
            LOG.critical(
                "RunGovernor(id=0x%x, uid=%s) "
                "encountered a fatal error while executing "
                "EnvironmentConductor(id=0x%x, uid=%s): %s",
                id(self.rgc),
                self.rgc.uid,
                id(environment_conductor),
                environment_conductor.uid,
                e,
            )
            tb = io.StringIO()
            traceback.print_exc(file=tb)
            LOG.debug(
                "RunGovernor(id=0x%x, uid=%s) "
                "encountered a fatal error while executing "
                "EnvironmentConductor(id=0x%x, uid=%s): %s",
                id(self.rgc),
                self.rgc.uid,
                id(environment_conductor),
                environment_conductor.uid,
                tb.getvalue(),
            )
            self.add_error(EnvConductorFailedError())

            raise e

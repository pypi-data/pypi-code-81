"""This module contains the class :class:`AgentConductor` that
stores all information the agents need about an actuator.

"""

import asyncio
import signal
import uuid
from uuid import uuid4

import aiomultiprocess
import setproctitle

from palaestrai.core import MajorDomoWorker
from palaestrai.core.protocol import (
    AgentSetupRequest,
    AgentSetupResponse,
    ShutdownRequest,
    ShutdownResponse,
)
from palaestrai.util.exception import (
    TasksNotFinishedError,
)
from palaestrai.util.dynaloader import load_with_params
from . import LOG
from .brain import Brain
from .muscle import Muscle


class AgentConductor:
    """This creates a new agent conductor (AC).

    The AC receives an agent config, which contains all information for
    the brain and the muscle. Additional information, like the current
    run ID, are part of the AgentSetupRequest.

    Parameters
    ----------
    broker_uri: str
        Connection information, should be in the format
        protocol://ip-address:port, e.g., "tcp://127.0.0.1:45310"
    agent_config: dict
        A *dict* containing information, how to instantiate brain and
        muscle.
    seed: int
        The random seed for this agent conductor.
    uid: str
        The uid for this agent conductor object.

    Attributes
    ----------
    agents: List[str]
        A list containing the uids of all the muscles.
    brain: :class:`.Brain`:
        A reference to the brain instance of this agent conductor.
    brain_process: :class:`aiomultiprocess.Process`
        A reference to the brain's process.
    objective: :class:`.Objective`
        A reference to the objective instance of this agent conductor.
    tasks: List[aiomultiprocess.Process]
        A list with references to the muscle's tasks.
    """

    def __init__(
        self, broker_uri: str, agent_config: dict, seed: int, uid=None
    ):
        self._worker = None
        self._broker_uri = broker_uri
        self._uid = str(uid) if uid else "AgentConductor-%s" % uuid4()

        self.tasks: list[aiomultiprocess.Process] = []
        self.seed = seed
        self.conf = agent_config
        self.brain = None
        self.objective = load_with_params(
            self.conf["objective"], self.conf["objective_params"]
        )
        self.agents: list[uuid.UUID] = []

        self.ac_socket = None
        self.brain_process = None

    def _handle_sigintterm(self, signum, frame):
        LOG.info(
            "AgentConductor(id=0x%x, uid=%s) "
            "interrpted by signal %s in frame %s",
            id(self),
            self.uid,
            signum,
            frame,
        )
        raise SystemExit()

    @property
    def uid(self):
        """Unique, opaque ID of the agent conductor object"""
        return self._uid

    @property
    def worker(self):
        """Getter for the :py:class:`MajorDomoWorker` object

        This method returns (possibly lazily creating) the current
        :py:class:`MajorDomoWorker` object. It creates this worker on demand.
        It is not safe to call this method between forks, as forks copy
        the context information for the worker which is process-depentent.

        :rtype: MajorDomoWorker
        """
        if self._worker is None:
            self._worker = MajorDomoWorker(self._broker_uri, self.uid)
        return self._worker

    async def _run_brain(self, brain: Brain):
        """Executes the Brain main loop, handling signals and errors

        This method wraps :py:func:`Brain.run`. It takes care of proper
        installment of signal handlers, setting of the proctitle, and most
        importantly, error handling. This method should be target of an
        :py:func:`aiomultiprocess.Process.run` call.
        """
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGABRT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        setproctitle.setproctitle("palaestrAI[Brain-%s]" % self.uid[-6:])
        try:
            return await brain.run()
        except Exception as e:
            LOG.critical(
                "AgentConductor(id=0x%x, uid=%s) "
                "encountered a fatal error while executing "
                "Brain(id=0x%x): %s",
                id(self),
                self.uid,
                id(brain),
                e,
            )
            raise e

    def _init_brain(self, sensors, actuators):
        """Initialize the brain process.

        Each agent, which is represented by an individual conductor,
        has one brain process. This function initializes the brain
        process.

        Parameters
        ----------
        sensors : list[sensor]
            List of available sensors.
        actuators : list[actuator]
            List of available actuators.
        """
        params = self.conf["brain_params"]
        params["sensors"] = sensors
        params["actuators"] = actuators
        params["objective"] = self.objective
        params["seed"] = self.seed
        self.brain: Brain = load_with_params(self.conf["brain"], params)
        self.brain_process = aiomultiprocess.Process(
            target=self._run_brain, args=(self.brain,)
        )
        self.brain_process.start()
        LOG.debug(
            "AgentConductor(id=0x%x, uid=%s) " "started Brain(id=0x%x)",
            id(self),
            self.uid,
            id(self.brain),
        )

    async def _run_muscle(self, muscle: Muscle):
        """Executes the Muscle main loop, handling signals and errors

        This method wraps :py:func:`Muscle.run`. It takes care of proper
        installment of signal handlers, setting of the proctitle, and most
        importantly, error handling. This method should be target of an
        :py:func:`aiomultiprocess.Process.run` call.
        """

        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGABRT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        setproctitle.setproctitle("palaestrAI[Muscle-%s]" % muscle.uid[-6:])
        try:
            return await muscle.run()
        except Exception as e:
            LOG.critical(
                "AgentConductor(id=0x%x, uid=%s) "
                "encountered a fatal error while executing "
                "Muscle(id=0x%x, uid=%s): %s",
                id(self),
                self.uid,
                id(muscle),
                muscle.uid,
                e,
            )
            raise e

    def _init_muscle(self, uid):
        """Function to initialize a new muscle

        Each agent consists of one brain and at least one muscle
        but is not limited to one muscle. There can be multiple
        muscles and muscles can be restarted.

        Parameters
        ----------
        uid : uuid4
            Unique identifier to identify the muscle
        """
        params = self.conf["muscle_params"]
        params["uid"] = uid
        muscle = load_with_params(self.conf["muscle"], params)
        muscle.setup()
        self.agents.append(uid)
        agent_process = aiomultiprocess.Process(
            name=uid, target=self._run_muscle, args=(muscle,)
        )
        agent_process.start()
        LOG.debug(
            "AgentConductor(id=0x%x, uid=%s) "
            "started Muscle(id=0x%x, uid=%s)",
            id(self),
            self.uid,
            id(muscle),
            muscle.uid,
        )
        self.tasks.append(agent_process)

    async def run(self):
        """Monitors agents and facilitates information interchange

        This method is the main loop for the :py:class:`AgentConductor`. It
        monitors the :py:class:`Brain` object and :py:class:`Muscle` instances
        of the agent (i.e., the processes) and transceives/routes messages.

        """
        signal.signal(signal.SIGINT, self._handle_sigintterm)
        signal.signal(signal.SIGTERM, self._handle_sigintterm)
        LOG.debug(
            "AgentConductor(id=0x%x, uid=%s) commencing run: "
            "Today's solutions to tomorrow's problems",
            id(self),
            self.uid,
        )
        proceed = True
        request = None
        reply = None
        while proceed:
            try:
                request = await self._housekeeping(reply)
            except TasksNotFinishedError:
                continue
            except SystemExit:
                break

            if isinstance(request, AgentSetupRequest):
                reply = self._handle_agent_setup(request)

            if isinstance(request, ShutdownRequest):
                await self._handle_shutdown(request)
                break

        LOG.debug(
            "AgentConductor(id=0x%x, uid=%s) shut down; sending "
            "ShutdownResponse(experiment_run_id=%s)",
            id(self),
            self.uid,
            request.run_id,
        )
        reply = ShutdownResponse(request.run_id)
        try:
            await self.worker.transceive(reply, skip_recv=True)
        except SystemExit:
            pass  # If they really want to, we can skip that, too.
        LOG.debug("ICH, AC, BIN NUN TOD, ADJÖ")

    async def _housekeeping(self, reply):
        """Keep the household clean and lively.

        In this method, replies are send and requests are received.
        Furthermore, the AC sees over his child tasks (muscles and
        brain).

        Parameters
        ----------
        reply:
            The next reply to send

        Returns
        -------
        request
            The request received during transceiving.

        """
        LOG.debug(
            "AgentConductor(id=0x%x, uid=%s) starts housekeeping. "
            "Everything needs to be in proper order.",
            id(self),
            self.uid,
        )
        try:
            transceive_task = asyncio.create_task(
                self.worker.transceive(reply)
            )
            muscle_tasks = [asyncio.create_task(p.join()) for p in self.tasks]
            brain_tasks = (
                [asyncio.create_task(self.brain_process.join())]
                if self.brain_process
                else []
            )
            tasks_done, tasks_pending = await asyncio.wait(
                [transceive_task] + muscle_tasks + brain_tasks,
                return_when=asyncio.FIRST_COMPLETED,
            )
            if not tasks_done:
                # This shouldn't happen, but you never know.
                raise TasksNotFinishedError()

            terminated_workers = [
                p
                for p in self.tasks + [self.brain_process]
                if p is not None and not p.is_alive() and p.exitcode != 0
            ]
            if terminated_workers:
                # I don't think the other tasks should end like this?
                LOG.critical(
                    "AgentConductor(id=0x%x, uid=%s) "
                    "has suffered from prematurely dead tasks: %s",
                    id(self),
                    self.uid,
                    [p.name for p in terminated_workers],
                )
                signal.signal(signal.SIGINT, signal.SIG_DFL)
                signal.signal(signal.SIGABRT, signal.SIG_DFL)
                signal.signal(signal.SIGTERM, signal.SIG_DFL)
                raise RuntimeError(
                    "AgentConductor(id=0x%x, uid=%s) "
                    "has dead tasks at hands: %s"
                    % (
                        id(self),
                        self.uid,
                        [p.name for p in terminated_workers],
                    )
                )
            if transceive_task not in tasks_done:
                await transceive_task
            request = transceive_task.result()
        except SystemExit as e:
            LOG.warning(
                "AgentConductor(id=0x%x, uid=%s) "
                "stopping due to SIGINT/SIGTERM",
                id(self),
                self.uid,
            )
            raise e

        LOG.debug(
            "AgentConductor(id=0x%x, uid=%s) got a %s. "
            "Let's see how we handle this one.",
            id(self),
            self.uid,
            request.__class__,
        )
        return request

    def _handle_agent_setup(self, request):
        """Handle the agent setup request.

        One setup request will result in one new muscle created.
        The brain will be created if necessary.

        Parameters
        ----------
        request: :class:`.AgentSetupRequest`
            The agent setup request with information for the muscle to
            be created.

        Returns
        -------
        :class:`.AgentSetupResponse`
            The response for the simulation controller.

        """

        if request.receiver_agent_conductor == self.uid:
            if self.brain is None:
                self._init_brain(request.sensors, request.actuators)
            self._init_muscle(request.agent_id)

            return AgentSetupResponse(
                sender_agent_conductor=self.uid,
                receiver_simulation_controller=request.sender,
                experiment_run_id=request.experiment_run_id,
                agent_id=request.agent_id,
            )

    async def _handle_shutdown(self, request):
        """Handle the shutdown request for this agent conductor.

        It is expected that all muscles and the brain of this
        agent conductor already received a shutdown request. Therefore,
        all this method does is to wait(join) for the processes.

        Parameters
        ----------
        request: :class:`.ShutdownRequest`

        """
        for task in self.tasks:
            await task.join()
        await self.brain_process.join()

"""This module contains the class :class:`EnvironmentConductor` that
controls the creation of new environments.

"""

import signal
import asyncio
import aiomultiprocess
from uuid import uuid4

from ..core import (
    BasicState,
    MajorDomoWorker,
)
from ..core.protocol import (
    EnvironmentSetupRequest,
    EnvironmentSetupResponse,
    ShutdownRequest,
    ShutdownResponse,
)

from ..util.dynaloader import load_with_params
from . import LOG
from .environment import Environment


class EnvironmentConductor:
    """The environment conductor creates new environment instances.

    There could be multiple simulation runs and each would need a
    separate environment. The environment conductor controls the
    creation of those new environment instances.

     Parameters
     ----------
     env_type : str
        Path to the used environment, it is specified in the
        experiment.yml
     env_params : dict
        Dictionary with parameters needed by the environment
     simulation_controller_connection : str
        URI used to connect to the simulation broker
     uid : uuid4
        Unique identifier

    """

    def __init__(self, env_type, env_params, broker_uri, seed: int, uid=None):
        self.seed = seed
        self._uid = str(uid) if uid else "EnvironmentConductor-%s" % uuid4()
        self.env_type = env_type
        self.env_params = env_params
        self._broker_uri = broker_uri
        self._state = BasicState.PRISTINE

        self._tasks: list[aiomultiprocess.Process] = []
        self._worker = None

        LOG.debug(
            "EnvironmentConductor(id=0x%x, uid=%s) created",
            id(self),
            self.uid,
        )

    @property
    def uid(self):
        return self._uid

    @property
    def worker(self):
        if not self._worker:
            self._worker = MajorDomoWorker(
                broker_uri=self._broker_uri,
                service=self.uid,
            )
        return self._worker

    def _handle_signal_interrupt(self, signum):
        """Handle interrupting signals by notifying of the state change."""
        LOG.info(
            "EnvironmentConductor(id=0x%x, uid=%s) " "interrpted by signal %s",
            id(self),
            self.uid,
            signum,
        )
        self._state = {
            signal.SIGINT.value: BasicState.SIGINT,
            signal.SIGABRT.value: BasicState.SIGABRT,
            signal.SIGTERM.value: BasicState.SIGTERM,
        }[signum]

    def _init_signal_handler(self):
        """Sets handlers for interrupting signals in the event loop."""
        signals = {signal.SIGINT, signal.SIGABRT, signal.SIGTERM}
        LOG.debug(
            "EnvironmentConductor(id=0x%x, uid=%s) "
            "registering signal handlers for signals %s",
            id(self),
            self.uid,
            signals,
        )
        loop = asyncio.get_running_loop()
        for signum in signals:
            loop.add_signal_handler(
                signum, self._handle_signal_interrupt, signum
            )

    async def _monitor_state(self):
        known_state = self._state
        while known_state.value == self._state.value:
            try:
                await asyncio.sleep(0.5)
            except asyncio.CancelledError:
                break
        LOG.debug(
            "EnvironmentConductor(id=0x%x, uid=%s) "
            "state changed from %s to %s",
            id(self),
            self.uid,
            known_state,
            self._state,
        )

    async def _run_environment(self, env: Environment):
        """Internal wrapper that awaits the environment run.

        The method wraps :py:func:`Environment.run`, watches exceptions,
        turns them into a log message, and also handles any other boilerplate
        stuff accordingly.
        """
        try:
            return await env.run()
        except Exception as e:
            LOG.critical(
                "EnvironmentConductor(id=0x%x, uid=%s) "
                "encountered a fatal error while executing "
                "Environment(id=0x%x, uid=%s): %s",
                id(self),
                self.uid,
                id(env),
                env.uid,
                e,
            )
            raise e

    def init_env(self, uid):
        """Initialize a new environment.

        Creates a new environment instance with its own UID.

        Parameters
        ----------
        uid : uuid4
            Unique identifier

        """
        env = load_with_params(
            self.env_type,
            {
                "connection": self.env_params["broker_connection"],
                "uid": uid,
                "seed": self.seed,
                "params": self.env_params.get("params", dict()),
            },
        )
        LOG.debug(
            "EnvironmentConductor(id=0x%x, uid=%s) "
            "loaded Environment %s(id=0x%x, uid=%s) - creating better worlds",
            id(self),
            self.uid,
            env.__class__,
            id(env),
            env.uid,
        )
        env_process = aiomultiprocess.Process(
            name="Environment-%s" % env.uid,
            target=self._run_environment,
            args=(env,),
        )
        env_process.start()
        self._tasks.append(env_process)

    async def run(self):
        self._init_signal_handler()
        self._state = BasicState.RUNNING
        request = None
        reply = None
        LOG.debug(
            "EnvironmentConductor(id=0x%x, uid=%s) comencing run",
            id(self),
            self.uid,
        )

        state_monitor_task = asyncio.create_task(self._monitor_state())
        while self._state == BasicState.RUNNING:
            transceive_task = asyncio.create_task(
                self.worker.transceive(reply)
            )
            tasks_done, tasks_pending = await asyncio.wait(
                {state_monitor_task, transceive_task},
                return_when=asyncio.FIRST_COMPLETED,
            )
            if transceive_task in tasks_pending:
                continue
            request = transceive_task.result()
            if not request:
                continue

            LOG.debug(
                "EnvironmentConductor(id=0x%x, uid=%s) "
                "received request: %s(%s)",
                id(self),
                self.uid,
                request.__class__,
                request.__dict__,
            )

            if isinstance(request, EnvironmentSetupRequest):
                LOG.debug(
                    "EnvironmentConductor(id=0x%x, uid=%s) "
                    "received EnvironmentSetupRequest(experiment_run_id=%s)",
                    id(self),
                    self.uid,
                    request.experiment_run_id,
                )
                self.init_env(request.environment_id)
                ssci = request.sender_simulation_controller_id
                reply = EnvironmentSetupResponse(
                    sender_environment_conductor=self.uid,
                    receiver_simulation_controller=ssci,
                    environment_id=request.environment_id,
                    experiment_run_id=request.experiment_run_id,
                    environment_type=self.env_type,
                    environment_parameters=self.env_params.get(
                        "params", dict()
                    ),
                )
            if isinstance(request, ShutdownRequest):
                self._state = BasicState.STOPPING
                for task in self._tasks:
                    await task.join()

        reply = ShutdownResponse(
            request.experiment_run_id if request else None
        )
        await self.worker.transceive(reply, skip_recv=True)
        self._state = BasicState.FINISHED

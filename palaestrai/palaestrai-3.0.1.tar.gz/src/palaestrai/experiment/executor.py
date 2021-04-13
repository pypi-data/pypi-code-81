import asyncio
import dataclasses
import enum
import io
import os
import signal
import traceback
import uuid
from collections import deque
from datetime import datetime
from typing import List, Union
from typing import Optional

import aiomultiprocess
import setproctitle
import zmq.error

from palaestrai.core import (
    RuntimeConfig,
    MajorDomoBroker,
    MajorDomoClient,
)
from palaestrai.core.protocol import (
    ExperimentShutdownRequest,
    ExperimentShutdownResponse,
    ExperimentStartRequest,
    ExperimentStartResponse,
)

from . import LOG
from .experiment import Experiment
from .run_governor import RunGovernor


class ExecutorState(enum.Enum):
    PRISTINE = 0
    INITIALIZED = 1
    RUNNING = 2
    SHUTDOWN = 3
    EXITED = 4
    SIGINT = 5
    SIGABRT = 6
    SIGTERM = 7


@dataclasses.dataclass
class _RunGovernorPCB:
    """Simple Process Control Block for RunGovernor control."""

    run_governor_id: str
    started_at: datetime
    run_governor_process: aiomultiprocess.Process
    experiment: Optional[Experiment] = None
    experiment_run_id: Optional[str] = None


@dataclasses.dataclass
class ExperimentRuntimeInformation:
    """Accumulated information about the one experiment run

    This structure contains information about one experiment run. It stores
    on which :py:class:`RunGovernor` it is executed, when it was started,
    which experiment is being run and what ID the experiment run has.
    """

    experiment: Experiment
    started_at: Union[datetime, None] = None
    run_governor_id: Union[str, None] = None
    experiment_run_id: Union[str, None] = None

    @property
    def is_running(self):
        return self.experiment_run_id is not None


class ExperimentStartError(RuntimeError):
    def __init__(self, experiment_run_id, run_governor_id, message):
        super().__init__(message)
        self.experipment_run_id = experiment_run_id
        self.run_governor_id = run_governor_id
        self.message = message


class InterruptSignal(RuntimeError):
    def __init__(self):
        super().__init__()


class Executor:
    """The executor is the entrypoint for every experiment execution.

    The role of the Executor is to receive new experiments and
    distribute them to existing :class:`RunGovernor` instances. If palaestrAI
    is used in local run mode, the Executor will initialize a
    :class:`RunGovernor`.

    Furthermore, the Executor can stop running experiments.
    """

    def __init__(self):
        # (At some point, when the core protocol has progressed far enough,
        # we will be able to run several experiments at once from an executor.
        # But, until we're sure we can, the public API accepts only one
        # experiment.)

        self._state = ExecutorState.PRISTINE
        self._broker: Union[None, MajorDomoBroker] = None
        self._client: Union[None, MajorDomoClient] = None
        self._broker_process: Union[None, aiomultiprocess.Process] = None
        self._broker_uri = "tcp://%s:%s" % (
            "*" if RuntimeConfig().public_bind else "127.0.0.1",
            RuntimeConfig().executor_bus_port,
        )
        self._run_governors = {}
        self._experiments_scheduled = deque()
        aiomultiprocess.set_start_method(None)  # Set best default for this OS.

    def _handle_signal_interrupt(self, signum):
        """Handle interrupting signals by notifying of the state change."""
        LOG.info("Executor has received signal %s, " "shutting down", signum)
        if signum not in {signal.SIGABRT, signal.SIGINT, signal.SIGTERM}:
            return
        self._state = {
            signal.SIGINT.value: ExecutorState.SIGINT,
            signal.SIGABRT.value: ExecutorState.SIGABRT,
            signal.SIGTERM.value: ExecutorState.SIGTERM,
        }[signum]

    def _init_signal_handler(self):
        """Sets handlers for interrupting signals in the event loop."""
        signals = {signal.SIGINT, signal.SIGABRT, signal.SIGTERM}
        LOG.debug(
            "Executor(id=0x%x) " "registering signal handlers for signals %s",
            id(self),
            signals,
        )
        loop = asyncio.get_running_loop()
        for signum in signals:
            loop.add_signal_handler(
                signum, self._handle_signal_interrupt, signum
            )

    def _init_communication(self):
        """Initialization of all core components"""
        self._broker = MajorDomoBroker(self._broker_uri)
        self._broker_process = aiomultiprocess.Process(
            daemon=True,
            target=self._broker.mediate,
            name="Executor-MajorDomoBroker",
        )
        self._broker_process.start()
        LOG.debug(
            "Executor(id=0x%x) started MajorDomoBroker(id=0x%x, uri=%s)",
            id(self),
            id(self._broker),
            self._broker_uri,
        )
        self._client = MajorDomoClient(
            "tcp://127.0.0.1:%s" % RuntimeConfig().executor_bus_port
        )
        LOG.debug(
            "Executor(id=0x%x) started MajorDomoClient(id=0x%x, uri=%s)",
            id(self),
            id(self._client),
            "tcp://127.0.0.1:%s" % RuntimeConfig().executor_bus_port,
        )

    def experiments(self) -> List[ExperimentRuntimeInformation]:
        return [
            ExperimentRuntimeInformation(experiment=e)
            for e in self._experiments_scheduled
        ] + [
            ExperimentRuntimeInformation(
                experiment=pcb.experiment,
                started_at=pcb.started_at,
                experiment_run_id=pcb.experiment_run_id,
            )
            for pcb in self._run_governors.values()
        ]

    async def _execute_run_governor(self, uid: str):
        """Executes the :py:class:`RunGovernor` main loop, catching errors

        This is a wrapper function around :py:func:`RunGovernor.run`. It takes
        care of clearing signal handlers, setting the proctitle, and generally
        catching errors in a meaningful in order to report it to the
        Executor without simply dying.
        """
        setproctitle.setproctitle("palaestrAI[RunGovernor-%s]" % uid[-6:])
        signal.signal(signal.SIGINT, signal.default_int_handler)
        signal.signal(signal.SIGABRT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        try:
            run_gov = RunGovernor(
                uid=uid,
                broker_uri=self._broker_uri,
            )
            await run_gov.run()
        except Exception as e:
            LOG.critical("Execution of RunGovernor failed: %s", e)
            tb = io.StringIO()
            traceback.print_exc(file=tb)
            LOG.debug(
                "Execution of RunGovernor() " "failed: %s; stack trace is: %s",
                e,
                tb.getvalue(),
            )
            raise e

    async def _launch_run_governor(self, experiment) -> _RunGovernorPCB:
        """Launches a new :py:class:`RunGovernor` process

        This method creates a new `aiomultiprocess.Process` and launches it,
        returning the appropriate PCB object.

        :rtype: _RunGovernorPCB
        """

        run_gov_uid = str(uuid.uuid4())

        run_gov_process = aiomultiprocess.Process(
            target=self._execute_run_governor,
            args=(run_gov_uid,),
            name="RunGovernor-%s" % run_gov_uid,
        )
        run_gov_process.start()

        return _RunGovernorPCB(
            experiment=experiment,
            started_at=datetime.now(),
            run_governor_id=run_gov_uid,
            run_governor_process=run_gov_process,
        )

    async def _deploy_experiment(self, experiment: Experiment):
        """Creates a :py:class:`RunGovernor` for a given experiment.

        This method creates a new :py:class:`RunGovernor` and deploys the
        provided :py:class:`Experiment` to it, pending start.

        The new :py:class:`RunGovernor` is started as a "python-parallel"
        process. All information about the running process is saved in the
        `self._run_governors` list, where we can also take care to stop all
        run governors should we need to.

        :param experiment: The experiment that should be executed.

        :return: An opaque :py:class:`RunGovernor` identification string.
        :rtype: str
        """

        pcb = await self._launch_run_governor(experiment)
        self._run_governors[pcb.run_governor_id] = pcb
        LOG.debug(
            "Executor(id=0x%x) started RunGovernor(uid=%s, broker_uri=%s)",
            id(self),
            pcb.run_governor_id,
            self._broker_uri,
        )
        return pcb.run_governor_id

    async def _start_experiment_run(self, run_governor_id):
        """Starts a previously deployed experiment.

        When the experiment is deployed via :py:meth:`_deploy_experiment`, the
        :py:class:`RunGovernor` is ready, but does not yet start it. This is
        done through this method, which sends the appropriate messages over
        the executor communications bus.

        :param run_governor_id: ID of the :class:`RunGovernor` that shall
            commence the experiment run.
        """
        experiment_run_id = str(uuid.uuid4())
        pcb = self._run_governors[run_governor_id]
        msg = ExperimentStartRequest(pcb.experiment, experiment_run_id)
        LOG.debug(
            "Executor(id=%s) starting experiment run: "
            "ExperimentStartRequest(experiment.id=%s, experiment_run_id=%s) "
            " - Our business is life itself",
            id(self),
            pcb.experiment.id,
            experiment_run_id,
        )
        response = await self._client.send(run_governor_id, msg)

        if isinstance(response, ExperimentStartResponse):
            if response.successful is True:
                self._run_governors[
                    run_governor_id
                ].experiment_run_id = experiment_run_id
            else:
                LOG.error("Could not start experiment run: %s", response.error)
                raise ExperimentStartError(
                    experiment_run_id=experiment_run_id,
                    run_governor_id=run_governor_id,
                    message=response.error,
                )
        else:
            LOG.error(
                "Executor expected ExperimentStartResponse, but got "
                "'%s' instead",
                response,
            )
            raise TypeError
        return experiment_run_id

    async def cancel(self, experiment_run_id):
        """Shuts an experiment down prematurely.

        This method sends a :py:class:`ExperimentShutdownRequest` to the
        :py:class:`RunGovernor` responsible for executing the associated
        experiment run. This allows for a graceful, yet premature shutdown
        of a running experiment. Normally, experiments terminate when their
        termination condition is met, so this method provides a way for an
        external user to interfere with a running experiment.

        :param experiment_run_id: UID of the experiment run to shut down.
        """
        run_governor_uid = next(
            filter(
                lambda i: i[1].experiment_run_id == experiment_run_id,
                self._run_governors.items(),
            ),
            None,
        )
        if run_governor_uid is None:
            LOG.error(
                "Cannot terminate ExperimentRun(id=%s): "
                "Cannot find RunGovernor",
                experiment_run_id,
            )
            return

        msg = ExperimentShutdownRequest(experiment_run_id)
        response = await self._client.send(run_governor_uid, msg)

        if not isinstance(response, ExperimentShutdownResponse):
            return
        if response.successful is True:
            self._run_governors.pop(run_governor_uid, None)
        else:
            raise RuntimeError(response.error)

    def schedule(self, experiment: Experiment):
        """Schedules an experiment to be run."""
        self._experiments_scheduled.append(experiment)

    async def _monitor_state(self):
        known_state = self._state
        while known_state.value == self._state.value:
            try:
                await asyncio.sleep(0.5)
            except asyncio.CancelledError:
                break
        LOG.debug(
            "Executor(id=0x%x) " "state changed from %s to %s",
            id(self),
            known_state,
            self._state,
        )

    async def execute(self):
        """Executes an experiment run.

        This method starts the whole experiment execution process. It
        initializes the :class:`RunGovernor` for the experiment run and
        sets up communication. This method returns only if:

        1. The experiment run has terminated successfully;
        2. an error has occurred, in which case an exception is raised;
        3. the user has terminated the process (e.g., by hitting ^C).

        :return: The state the executor is now in, either "SHUTDOWN" if
            everything exited normally, or one of the SIG* states if a
            signal was received.
        :rtype: ExecutorState
        """
        setproctitle.setproctitle("palaestrAI[Executor]")
        self._init_communication()
        self._init_signal_handler()
        n_broker_checks = 0
        self._state = ExecutorState.INITIALIZED

        LOG.debug("Executor(id=0x%x) starting main execution loop", id(self))
        self._state = ExecutorState.RUNNING
        while self._state == ExecutorState.RUNNING:
            if self._state and not self._broker_process.is_alive():
                if n_broker_checks == 3:
                    LOG.fatal(
                        "Executor(id=%s) lost the MajorDomoBroker, "
                        "committing seppuku",
                        id(self),
                    )
                    break
                else:
                    wait_time = 1 + n_broker_checks
                    LOG.debug(
                        "MajorDomoBroker is not yet online, waiting for"
                        "%s seconds",
                        wait_time,
                    )
                    n_broker_checks += 1
                    await asyncio.sleep(wait_time)
                    continue
            n_broker_checks = 0
            LOG.debug(
                "Executor(id=%s) " "checks whether to start new experiments",
                id(self),
            )
            while self._state and len(self._experiments_scheduled) > 0:
                experiment = self._experiments_scheduled.pop()
                try:
                    run_governor_id = await self._deploy_experiment(experiment)
                    state_change_monitor_task = asyncio.create_task(
                        self._monitor_state()
                    )
                    start_experiment_run_task = asyncio.create_task(
                        self._start_experiment_run(run_governor_id)
                    )
                    tasks_done, _ = await asyncio.wait(
                        {state_change_monitor_task, start_experiment_run_task},
                        return_when=asyncio.FIRST_COMPLETED,
                    )
                    if (
                        start_experiment_run_task in tasks_done
                        and start_experiment_run_task.exception()
                    ):
                        raise start_experiment_run_task.exception()
                    if state_change_monitor_task not in tasks_done:
                        state_change_monitor_task.cancel()
                except ExperimentStartError as e:
                    LOG.fatal(
                        "Executor(id=%s) "
                        "could not launch ExperimentRun(experiment_id=%s): "
                        "%s; killing associated RunGovernor(uid=%s).",
                        id(self),
                        experiment.id,
                        e,
                        e.run_governor_id,
                    )
                    pcb = self._run_governors[e.run_governor_id]
                    pcb.run_governor_process.terminate()
                    try:
                        await pcb.run_governor_process.join(3)
                    except asyncio.TimeoutError:
                        if pcb.run_governor_process.is_alive():
                            pcb.run_governor_process.kill()
                            await pcb.run_governor_process.join(3)
            LOG.debug(
                "Executor(id=0x%x) " "checks for finished RunGovernors",
                id(self),
            )
            self._run_governors = {
                uid: pcb
                for uid, pcb in self._run_governors.items()
                if pcb.run_governor_process.is_alive()
            }
            LOG.debug(
                "Executor(id=0x%x) "
                "has %d active run governors and %d experiments scheduled",
                id(self),
                len(self._run_governors),
                len(self._experiments_scheduled),
            )
            await asyncio.sleep(3)
            if (
                self._state == ExecutorState.RUNNING
                and len(self._run_governors) + len(self._experiments_scheduled)
                == 0
            ):
                self._state = ExecutorState.SHUTDOWN
        LOG.debug("Executor(id=0x%x) " "starting shut down", id(self))
        for run_gov_uid in self._run_governors:
            pcb = self._run_governors[run_gov_uid]
            if not pcb.run_governor_process.is_alive():
                continue
            LOG.debug(
                "Executor(id=%s) "
                "signalling RunGovernor(uid=%s, experiment_run_id=%s) "
                "to shut down",
                id(self),
                run_gov_uid,
                pcb.experiment_run_id,
            )
            if pcb.experiment_run_id:
                try:
                    LOG.debug(
                        "Executor(id=%s) "
                        "has encountered a "
                        "RunGovernor(uid=%s, experiment_run_id=%s) "
                        "that seems to be still active, trying to abort. "
                        "Did you hit ^C? Oh, you bad boy...",
                        id(self),
                        pcb.run_governor_id,
                        pcb.experiment_run_id,
                    )
                    await asyncio.wait_for(
                        self.cancel(pcb.experiment_run_id), timeout=15
                    )
                except asyncio.TimeoutError:
                    LOG.warn(
                        "Executor(id=%s) "
                        "could not shut down "
                        "RunGovernor(uid=%s, experiment_run_id=%s) "
                        "orderly",
                        id(self),
                        run_gov_uid,
                        pcb.experiment_run_id,
                    )
            run_governor_pgid = os.getpgid(pcb.run_governor_process.pid)
            pcb.run_governor_process.terminate()
            try:
                await pcb.run_governor_process.join(3)
            except asyncio.TimeoutError:
                pcb.run_governor_process.kill()
            try:
                # Zombies will be shot:
                os.killpg(run_governor_pgid, signal.SIGKILL)
            except ProcessLookupError:
                pass  # Just a shot in the dark.
        try:
            await self._client.destroy()
        except zmq.error.ZMQError:
            # This can happen on ^C. It's actually not that bad, so we just
            # do a debug log entry here.
            LOG.debug(
                "Executor(id=%s) "
                "could not send destroy message via MajorDomoClient to "
                "MajorDomoBroker(uri=%s); ignoring that anyways and dragging "
                "on",
                id(self),
                self._broker_uri,
            )
        self._broker_process.terminate()
        try:
            await self._broker_process.join(3)
        except asyncio.TimeoutError:
            self._broker_process.kill()
        if self._state == ExecutorState.SHUTDOWN:
            self._state = ExecutorState.EXITED
        return self._state

    def shutdown(self):
        """Stops all running processes."""
        LOG.info("Executor(id=%s) " "starting shutdown procedure", id(self))
        self._experiments_scheduled.clear()
        self._state = False

"""This module contains the :class:`.SimulationController`, which is
the abstract base class (ABC) for all specific simulation controllers.
"""
import asyncio
import uuid
from abc import ABC, abstractmethod
from importlib import import_module

from palaestrai.agent.agent import Agent
from palaestrai.core import MajorDomoClient, MajorDomoWorker
from palaestrai.core.protocol import (
    ShutdownRequest,
    AgentSetupRequest,
    AgentShutdownRequest,
    AgentShutdownResponse,
    EnvironmentSetupRequest,
    EnvironmentShutdownRequest,
    EnvironmentShutdownResponse,
    EnvironmentStartRequest,
    EnvironmentStartResponse,
    ShutdownRequest,
    SimulationStartRequest,
    SimulationStartResponse,
    SimulationStopRequest,
    SimulationStopResponse,
)

from . import LOG


class SimulationSetupError(RuntimeError):
    def __init__(self, experiment_run_id, message):
        super().__init__(message)
        self.message = message
        self.experiment_run_id = experiment_run_id

    def __str__(self):
        return "%s (in experiment run: %s)" % (
            self.message,
            self.experiment_run_id,
        )


class SimulationController(ABC):
    """The base class for simulation controllers.

    A :class:`.SimulationController` coordinates the core
    between agents and environment(s). Each simulation ontroller is
    responsible for one simulation run. The run_id identifies the
    simulation controller.

    Parameters
    ----------
    run_governor_uri : str
        A tcp string defining the location of the corresponding run
        governor. The string has the form:

            "tcp://127.0.0.1:5555"

    sim_connection : str
        A tcp string defining the location of this simulation
        controller.
    run_id : :class:`uuid.UUID`
        The unique identifier for this specific simulation run.
    agent_conductor_ids : list
        A list of :class:`uuid.UUID`s of the agent conductors of this
        run.
    environment_conductor_ids : list
        A list of :class:`uuid.UUID`s of the environment conductors of
        this run.
    termination_conditions : list
        A list of dicts containing import strings and params for
        termination conditions.
    verbose : bool
        This flag activates verbose logging if set to *True*.

    """

    def __init__(
        self,
        rungov_connection,
        sim_connection,
        agent_conductor_ids,
        environment_conductor_ids,
        agents,
        termination_conditions,
    ):
        self._uid = str(uuid.uuid4())
        self.experiment_run_id = None

        self._run_governor_uri = rungov_connection
        self.sim_connection = sim_connection
        self.agent_configs = agents
        self.ac_ids = agent_conductor_ids
        self.ec_ids = environment_conductor_ids
        LOG.debug(
            "SimulationController loading TerminationCondition objects %s",
            termination_conditions,
        )
        try:
            self.termination_conditions = [
                _load_with_params(cond["condition"], cond["params"])
                for cond in termination_conditions
            ]
        except Exception as e:
            LOG.fatal("Could not load termination condition: %s", e)
            raise e
        LOG.debug(
            "Create %s(%s) for experiment_run_id=%s "
            "with termination_condition=%s",
            self.__class__,
            self.uid,
            self.experiment_run_id,
            self.termination_conditions,
        )

        self._ctx = None
        self._task = None
        self._worker = None
        self._client = None
        self._rg_client = None
        self.ac_socket = None
        self.ec_socket = None
        self.rg_id = None
        self.experiment_id = None
        self.env_ids = {}

        self.all_sensors = []
        self.all_actuators = []
        self.agents = []
        self.ex_termination = False

    @property
    def uid(self):
        return self._uid

    @property
    def client(self):
        if self._client is None:
            self._client = MajorDomoClient(self.sim_connection)
        return self._client

    @property
    def worker(self):
        if self._worker is None:
            self._worker = MajorDomoWorker(
                broker_uri=self._run_governor_uri,
                service=self.experiment_run_id,
            )
        return self._worker

    @property
    def run_gov_client(self):
        if self._rg_client is None:
            self._rg_client = MajorDomoClient(self._run_governor_uri)
        return self._rg_client

    @abstractmethod
    async def simulation(self):
        pass

    async def conductor_shutdown(self):
        """Function to shutdown the conductors

        One part of the shutdown procedure is the conductor
        shutdown. This function shuts down all agent and
        environment conductors.

        """
        LOG.info("Stopping simulation: Sending shutdown request")
        msg = ShutdownRequest(self.experiment_run_id)
        for acuid in self.ac_ids:
            try:
                _ = await self.client.send(acuid, msg)
            except TypeError:
                LOG.info(
                    "SimulationController(id=0x%x, uid=%s): "
                    "AgentConductor shutdown done",
                    id(self),
                    self.uid,
                )
        for ecuid in self.ec_ids:
            try:
                _ = await self.client.send(ecuid, msg)
            except TypeError:
                LOG.info(
                    "SimulationController(id=0x%x, uid=%s): "
                    "EnvironmentConductor shutdown done",
                    id(self),
                    self.uid,
                )

    async def agent_shutdown(self, complete_shutdown):
        """Function to shutdown an agent

        This function is shutting down an agent. An agent is in this case
        a muscle. The parameter complete_shutdown indicates if the brain
        should also shut down. This is the case if the experiment has
        finished.

        Parameters
        ----------
        complete_shutdown : bool
            Indicates if the experiment has finished or if only the
            muscle has to shut down.
        """
        agents_to_remove = []
        while self.agents:
            LOG.debug(
                "SimulationController(id=0x%x, uid=%s) shutting down agents; "
                "%d to go",
                id(self),
                self.uid,
                len(self.agents),
            )
            for agent in self.agents:
                msg = AgentShutdownRequest(
                    self.experiment_run_id, str(agent.uid), complete_shutdown
                )
                LOG.debug(
                    "SimulationController(id=0x%x, uid=%s) sending "
                    "AgentShutdownRequest(agent.uid=%s)",
                    id(self),
                    self.uid,
                    agent.uid,
                )

                response = await self.client.send(agent.uid, msg)
                if isinstance(response, AgentShutdownResponse):
                    agents_to_remove.append(agent)
                elif response is None:
                    pass

            for agent in agents_to_remove:
                self.agents.remove(agent)
            agents_to_remove = None

    async def env_shutdown(self):
        """Function to shutdown the environment

        This functions shuts down an environment. Currently
        it shuts down all available environments. Partial
        shutdown is not possible.

        """
        envs_to_remove = []
        while self.env_ids:
            for env in self.env_ids:
                msg = EnvironmentShutdownRequest(
                    self.experiment_run_id, str(env)
                )
                response = await self.client.send(env, msg)
                if isinstance(response, EnvironmentShutdownResponse):
                    envs_to_remove.append(env)
                elif response is None:
                    pass

            LOG.debug(
                "SimulationController %s(id=0x%x, uid=%s) "
                "removing environments %s from the internal list: %s",
                self.__class__,
                id(self),
                self.uid,
                envs_to_remove,
                self.env_ids,
            )
            for env in envs_to_remove:
                _ = self.env_ids.pop(env, None)
            envs_to_remove = None

    async def stop_simulation(self, complete_shutdown):
        """Coordinating the shutdown

        This function coordinates the shutdown of the individual components.

        Parameters
        ----------
        complete_shutdown : bool
            Indicates if the experiment has finished or if only the
            muscle has to shut down.
        """
        LOG.debug(
            "SimulationController %s(id=0x%x, uid=%s) in stop_simulation, "
            "shutting down agents.",
            self.__class__,
            id(self),
            self.uid,
        )
        await self.agent_shutdown(complete_shutdown)
        LOG.debug(
            "SimulationController %s(id=0x%x, uid=%s) in stop_simulation, "
            "shutting down environment.",
            self.__class__,
            id(self),
            self.uid,
        )
        await self.env_shutdown()
        LOG.debug(
            "SimulationController %s(id=0x%x, uid=%s) in stop_simulation, "
            "shutting down conductors.",
            self.__class__,
            id(self),
            self.uid,
        )
        await self.conductor_shutdown()

    def _setup(self):
        LOG.debug(
            "%s(%s) creating new MajorDomoWorker for experiment_run_id=%s",
            self.__class__,
            self.uid,
            self.experiment_run_id,
        )
        self._worker = MajorDomoWorker(
            broker_uri=self._run_governor_uri, service=self.uid
        )

    def _generate_uid(self, gen_type):
        if gen_type == "agent":
            uid = self.experiment_run_id + "_A:" + str(uuid.uuid4())
        elif gen_type == "environment":
            uid = self.experiment_run_id + "_E:" + str(uuid.uuid4())
        else:
            uid = uuid.uuid4()
        return uid

    async def _init_simulation(self):
        LOG.debug(
            "SimulationController %s(id=0x%x, uid=%s) "
            "starting environment conducts",
            self.__class__,
            id(self),
            self.uid,
        )
        for ec in self.ec_ids:
            uid = self._generate_uid("environment")
            self.env_ids[uid] = ec
            LOG.debug(
                "SimulationController %s(id=0x%x, uid=%s) "
                "sending EnvironmentSetupRequest(experiment_run_id=%s, "
                "environment_id=%s, environment_conductor_id=%s)",
                self.__class__,
                id(self),
                self.uid,
                self.experiment_run_id,
                uid,
                ec,
            )
            request = EnvironmentSetupRequest(
                environment_id=uid,
                experiment_run_id=self.experiment_run_id,
                receiver_environment_conductor_id=ec,
                sender_simulation_controller_id=self.uid,
            )
            response = await self.client.send(ec, request)
            if not response:
                LOG.critical(
                    "SimulationController %s(id=0x%x, uid=%s) "
                    "received no EnvironmentSetupResponse after "
                    "sending EnvironmentSetupRequest(experiment_run_id=%s, "
                    "environment_id=%s, environment_conductor_id=%s)",
                    self.__class__,
                    id(self),
                    self.uid,
                    self.experiment_run_id,
                    uid,
                    ec,
                )
                raise SimulationSetupError(
                    experiment_run_id=self.experiment_run_id,
                    message="environment %s did not respond "
                    "to EnvironmentSetupRequest" % ec,
                )

            request = EnvironmentStartRequest(self.experiment_run_id, uid)
            response = await self.client.send(uid, request)

            if not response:
                LOG.critical(
                    "SimulationController %s(id=0x%x, uid=%s) "
                    "received no EnvironmentStartResponse after "
                    "sending EnvironmentStartRequest(experiment_run_id=%s, "
                    "environment_id=%s, environment_conductor_id=%s)",
                    self.__class__,
                    id(self),
                    self.uid,
                    self.experiment_run_id,
                    uid,
                    ec,
                )
                raise SimulationSetupError(
                    experiment_run_id=self.experiment_run_id,
                    message="environment %s did not respond "
                    "to EnvironmentStartRequest" % ec,
                )
            if isinstance(response, EnvironmentStartResponse):
                self.all_sensors = response.sensors
                self.all_actuators = response.actuators
        LOG.debug(
            "SimulationController %s(id=0x%x, uid=%s) "
            "starting agent conductors",
            self.__class__,
            id(self),
            self.uid,
        )
        for acuid in self.ac_ids:
            conf = self.agent_configs[acuid]
            # print("Sending AgentConductorSetup")
            # msg = AgentConductorSetupRequest(self.run_id, ac, conf)
            # response = await self.client.send(ac, msg)

            # print("Received AgentConductorSetup")
            # if not isinstance(response, AgentConductorSetupResponse):
            #     raise TypeError

            uid = self._generate_uid("agent")
            # self.agent_ids.append(uid)
            # uid = str(uuid.uuid4())
            sensors, actuators = self.access_list(
                conf["sensors"], conf["actuators"]
            )
            agent = Agent(
                uid,
                conf["brain"],
                conf["brain_params"],
                conf["muscle"],
                conf["muscle_params"],
                sensors,
                actuators,
            )
            self.agents.append(agent)
            LOG.debug(
                "SimulationController %s(id=0x%x, uid=%s) "
                "sending "
                "AgentSetupRequest(agent_conductor_id=%s, agent_id=%s)",
                self.__class__,
                id(self),
                self.uid,
                acuid,
                uid,
            )
            request = AgentSetupRequest(
                sender_simulation_controller=self.uid,
                receiver_agent_conductor=str(acuid),
                experiment_run_id=self.experiment_run_id,
                agent_id=uid,
                agent_name=conf["name"] if "name" in conf else None,
                sensors=sensors,
                actuators=actuators,
            )

            response = await self.client.send(acuid, request)
            if not response:
                LOG.critical(
                    "SimulationController %s(id=0x%x, uid=%s) "
                    "received no AgentSetupResponse after "
                    "sending AgentSetupRequest(receiver=%s, "
                    "experiment_run_id=%s, agent_id=%s, agent_name=%s)",
                    self.__class__,
                    id(self),
                    self.uid,
                    request.receiver_agent_conductor,
                    self.experiment_run_id,
                    uid,
                    conf["name"] if "name" in conf else None,
                )
                raise SimulationSetupError(
                    experiment_run_id=self.experiment_run_id,
                    message="AgentConductor %s did not respond "
                    "to AgentSetupRequest" % request.receiver,
                )

    async def run(self):
        """Main function, coordination of messages

        This function takes care of all the coordination. It performs the initial
        setup, it receives new messages and processes these messages.
        In addition, it also takes care of the shutdown.
        """
        LOG.info(
            "%s(%s) standing by for experiment_run_id=%s",
            self.__class__,
            self.uid,
            self.experiment_run_id,
        )
        self._setup()
        reply = None
        while not self._task or not self._task.done():
            LOG.debug(
                "%s(%s) waiting for next request", self.__class__, self.uid
            )

            transceive_task = asyncio.create_task(
                self.worker.transceive(reply)
            )
            tasks_done, _ = await asyncio.wait(
                {self._task, transceive_task}
                if self._task
                else {transceive_task},
                return_when=asyncio.FIRST_COMPLETED,
            )
            if transceive_task in tasks_done:
                request = transceive_task.result()
            if self._task in tasks_done:
                continue

            LOG.debug(
                "%s(%s) received request: %s",
                self.__class__,
                self.uid,
                request,
            )

            if isinstance(request, SimulationStartRequest):
                LOG.debug(
                    "SimulationController %s(id=0x%x, uid=%s) received "
                    "SimulationStartRequest from RunGovernor(%s) for "
                    "experiment_run_id=%s",
                    self.__class__,
                    id(self),
                    self.uid,
                    request.run_governor_id,
                    self.experiment_run_id,
                )
                self.rg_id = request.run_governor_id
                self.experiment_run_id = request.experiment_run_id

                reply = SimulationStartResponse()
                await self._init_simulation()
                self._task = asyncio.create_task(self.simulation())

                LOG.debug(
                    "SimulationController %s(id=0x%x, uid=%s) "
                    "initialized simulation",
                    self.__class__,
                    id(self),
                    self.uid,
                )
            elif isinstance(request, SimulationStopRequest):
                LOG.debug(
                    "SimulationController %s(id=0x%x, uid=%s) received "
                    "SimulationStopRequest(experiment_run_id=%s)",
                    self.__class__,
                    id(self),
                    self.uid,
                    self.experiment_run_id,
                )
                self.ex_termination = True

                reply = SimulationStopResponse(self.experiment_run_id)
                self._task.cancel()
                try:
                    await self._task
                except asyncio.CancelledError:
                    pass  # We actually expect this, more or less.

                LOG.debug(
                    "SimulationController %s(id=0x%x, uid=%s) finished "
                    "simulation of ExperimentRun(id=%s), sending "
                    "SimulationStopResponse(experiment_run_id=%s)",
                    self.__class__,
                    id(self),
                    self.uid,
                    self.experiment_run_id,
                    self.experiment_run_id,
                )
        LOG.debug(
            "SimulationController %s(id=0x%x, uid=%s) starting cleanup",
            self.__class__,
            id(self),
            self.uid,
        )
        await self.worker.transceive(reply, skip_recv=True)

    def get_sensor(self, uid):
        for sensor in self.all_sensors:
            if str(sensor.uid) == str(uid):
                return sensor

    def get_actuator(self, uid):
        for actuator in self.all_actuators:
            if str(actuator.uid) == str(uid):
                return uid

    @abstractmethod
    def access_list(self, sensor_list, actuator_list):
        pass


def _load_with_params(module_path, params):
    """Load a class from *module_path* and pass *params*."""
    module, clazz = module_path.split(":")
    module = import_module(module)
    return getattr(module, clazz)(**params)

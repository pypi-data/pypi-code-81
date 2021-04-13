import logging
from itertools import product

from palaestrai.core.protocol import (
    AgentUpdateRequest,
    AgentUpdateResponse,
    EnvironmentUpdateResponse,
    EnvironmentUpdateRequest,
    SimulationControllerTerminationRequest,
    SimulationControllerTerminationResponse,
)

from . import LOG
from .simulation_controller import SimulationController

# Very detailed debug logger
# Please do not remove until everything works
VDDLOG = logging.getLogger("palaestrai.verbose")


class VanillaSimController(SimulationController):
    """
    This is our vanilla controller. With this simulation,
    environment and agent(s) work alternately and not in
    parallel. It is not a continuous simulation.
    After each simulation step (independent if done
    by environment or agent) the Termination Condition
    is called.
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
        super().__init__(
            rungov_connection,
            sim_connection,
            agent_conductor_ids,
            environment_conductor_ids,
            agents,
            termination_conditions,
        )

    @staticmethod
    def env_update(responses: list):
        """
        This method will process a list of environment update responses
        and will combine the information to combined lists. Currently
        the termination variable is global because we assume, that
        the run terminates if at least one environment is env
        terminates.

        Parameters
        ----------
        responses = list of EnvironmentUpdateResponse

        Returns
        -------
        sensors = list of all sensor_information of all available environments
        rewards = list of all environment rewards
        termination = boolean which is true if one environment has terminated

        """
        sensors = []
        rewards = []
        termination = False
        for response in responses:
            sensors.extend(response.sensors)
            rewards.append(response.reward)
            if response.is_terminal:
                termination = True
        return sensors, rewards, termination

    @staticmethod
    def agent_update(responses: list) -> list:
        """

        This method combines all actuator_information of all Agents
        and creates on list.

        Parameters
        ----------
        responses = List of AgentUpdateResponses

        Returns
        -------
        actuators which is a list of actuator_information
        """
        actuators = []
        for response in responses:
            actuators.extend(response.actuators)
        return actuators

    async def simulation_shutdown(
        self, env_termination: bool, rewards: list, additional_results
    ):
        """
        This method will be called when the simulation has terminated
        it will send a SimControllerTerminationRequest to the runGov.
        The RunGov will respond and will tell if it will be a complete
        or partial shutdown.
        The complete shutdown includes the conductors while a partial
        shutdown is a reset which just deletes the muscle(s) and env(s)
        Parameters
        ----------
        env_termination : bool if the environment has terminated
        rewards : list of rewards to show the current performance
        additional_results : for any additional information

        Returns
        -------


        """

        msg = SimulationControllerTerminationRequest(
            sender_simulation_controller_id=self.uid,
            receiver_run_governor_id=self.rg_id,
            experiment_run_id=self.experiment_run_id,
            environment_terminated=env_termination,
            last_reward=rewards,
            additional_results=additional_results,
        )
        LOG.debug(
            "SimulationController %s(id=0x%x, uid=%s) "
            "sending "
            "SimulationControllerTerminationRequest(experiment_run_id=%s)",
            self.__class__,
            id(self),
            self.uid,
            self.experiment_run_id,
        )

        response = await self.run_gov_client.send(self.rg_id, msg)
        if not isinstance(response, SimulationControllerTerminationResponse):
            LOG.critical(
                "SimulationController %s(id=0x%x, uid=%s) "
                "waited for SimulationControllerTerminationResponse, but got "
                "%s instead. Dying without honor, trusting the RunGovernor "
                "to handle this disgrace",
                self.__class__,
                id(self),
                self.uid,
                response,
            )
            await self.stop_simulation(True)
        LOG.debug(
            "SimulationController %s(id=0x%x, uid=%s) " "received %s",
            self.__class__,
            id(self),
            self.uid,
            response,
        )
        if response.complete_shutdown:
            await self.stop_simulation(response.complete_shutdown)
        else:
            await self.agent_shutdown(response.complete_shutdown)
            await self.env_shutdown()

    async def get_env_update(self, env, actuators):
        """
        Sends an EnvironmentUpdateRequest to one env
        and collects the Response.
        The vanilla simController sends all actuators to all envs
        and the env has to select the own actuators. A access list
        could be needed if two envs of the same type are used.
        Parameters
        ----------
        env : id of the environment
        actuators : list of actuatorinformation

        Returns
        -------
        response : EnvironmentUpdateResponse
        """
        LOG.debug(
            "SimulationController %s(id=0x%x, uid=%s) "
            "starting EnvironmentUpdateRequest(experiment_run_id=%s, "
            "env=%s, actuators=%s)",
            self.__class__,
            id(self),
            self.uid,
            self.experiment_run_id,
            str(env),
            actuators,
        )
        msg = EnvironmentUpdateRequest(
            experiment_run_id=self.experiment_run_id,
            environment_conductor_id=str(self.env_ids[str(env)]),
            sender_simulation_controller=self.uid,
            receiver_environment=str(env),
            actuators=actuators,
        )
        response = await self.client.send(bytes(str(env), "ascii"), msg)
        LOG.debug(
            "SimulationController %s(id=0x%x, uid=%s) "
            "received EnvironmentUpdateResponse: %s",
            self.__class__,
            id(self),
            self.uid,
            response,
        )
        if isinstance(response, EnvironmentUpdateResponse):
            return response
        else:
            LOG.error(
                "SimulationController %s(id=0x%x, uid=%s) expected "
                "EnvironmentUpdateResponse, but got %s instead; ignoring",
                self.__class__,
                id(self),
                self.uid,
                response,
            )
            return None

    async def get_agent_update(
        self, agent_id, sensors, actuators, rewards, env_termination
    ):
        """
        This method sends an AgentUpdateRequest and collects
        the response which will be returned.

        Parameters
        ----------
        agent_id : id of the agent
        sensors : list of sensor information
        actuators : list of actuator information
        rewards : list of environment rewards
        env_termination : bool if env has terminated

        Returns
        -------
        AgentUpdateResponse
        """
        LOG.debug(
            "SimulationController %s(id=0x%x, uid=%s) "
            "requesting update from Agent(uid=%s)",
            self.__class__,
            id(self),
            self.uid,
            agent_id,
        )
        msg = AgentUpdateRequest(
            sender_simulation_controller_id=self.uid,
            receiver_agent_id=agent_id,
            experiment_run_id=self.experiment_run_id,
            sensors=sensors,
            actuators=actuators,
            reward=rewards,
            is_terminal=env_termination,
        )
        response = await self.client.send(agent_id, msg)

        if isinstance(response, AgentUpdateResponse):
            LOG.debug(
                "SimulationController %s(id=0x%x, uid=%s) "
                "received AgentUpdateResponse from Agent(uid=%s)",
                self.__class__,
                id(self),
                self.uid,
                agent_id,
            )
            return response
        else:
            LOG.error(
                "SimulationController %s(id=0x%x, uid=%s) expected "
                "AgentUpdateResponse, but got %s instead; ignoring",
                self.__class__,
                id(self),
                self.uid,
                response,
            )
            return None

    async def simulation(self):
        """
        This is the abstract method implementation of the
        simulation task. The vanilla sim controller simulation
        start by asking all environments for sensor information.
        These information will be send to the agent(s) which
        will respond which their actuator-setpoints.
        From there on it will be a ping pong between environment(s)
        and agent(s). All available information will be exchanged.
        Both, environment as well as agent information, can be
        used for the termination.
        Returns
        -------

        """
        termination = False
        actuators = self.all_actuators
        env_termination = False
        rewards = []
        LOG.debug(
            "SimulationController %s(id=0x%x, uid=%s) starting simulation",
            self.__class__,
            id(self),
            self.uid,
        )
        while not termination and not self.ex_termination:
            LOG.debug(
                "SimulationController %s(id=0x%x, uid=%s) "
                "running new iteration for experiment_run_id=%s; "
                "termination: %s",
                self.__class__,
                id(self),
                self.uid,
                self.experiment_run_id,
                self.ex_termination,
            )

            responses = [
                term
                for term in [
                    await self.get_env_update(eid, actuators)
                    for eid in self.env_ids
                ]
                if term
            ]
            termination = any(
                [
                    term[0].check_termination(term[1])
                    for term in product(self.termination_conditions, responses)
                ]
            )
            self.all_sensors, rewards, env_termination = self.env_update(
                responses
            )

            responses = [
                term
                for term in [
                    await self.get_agent_update(
                        str(agent.uid),
                        self.access_list(
                            [s.sensor_id for s in agent.sensors], []
                        )[
                            0
                        ],  # TODO: quite hacky
                        agent.actuators,
                        rewards,
                        env_termination,
                    )
                    for agent in self.agents
                ]
                if term
            ]
            termination = termination or any(
                [
                    term[0].check_termination(term[1])
                    for term in product(self.termination_conditions, responses)
                ]
            )
            actuators = self.collect_actuators(agent_responses=responses)
        if not self.ex_termination:
            LOG.debug(
                "SimulationController %s(id=0x%x, uid=%s) "
                "waiting for shutdown to complete",
                self.__class__,
                id(self),
                self.uid,
            )
            await self.simulation_shutdown(env_termination, rewards, None)
        else:
            LOG.debug(
                "SimulationController %s(id=0x%x, uid=%s) "
                "completing shutdown",
                self.__class__,
                id(self),
                self.uid,
            )
            await self.stop_simulation(True)
        LOG.debug(
            "SimulationController %s(id=0x%x, uid=%s) "
            "finished simulation()",
            self.__class__,
            id(self),
            self.uid,
        )

    def collect_actuators(self, agent_responses: list):
        """
        collect_actuators takes a list of agent_responses
        and combines all available actuators to one list.

        Parameters
        ----------
        agent_responses : list[agent_responses]

        Returns
        -------
        actuators : list[actuator]

        """
        actuators = []
        for response in agent_responses:
            # TODO: Workaround, works only for single env
            actuators.extend(response.actuators)
        return actuators

    def access_list(self, sensor_list, actuator_list):
        """
        access_list takes a list of sensors and actuators
        and checks if they are part of the available
        sensors/actuators. If that is the case they
        will be returned.

        Parameters
        ----------
        sensor_list : list
        actuator_list : list

        Returns
        -------
        sensor_list : list
        actuator_list : list

        """
        return (
            [s for s in self.all_sensors if s.sensor_id in sensor_list],
            [a for a in self.all_actuators if a.actuator_id in actuator_list],
        )

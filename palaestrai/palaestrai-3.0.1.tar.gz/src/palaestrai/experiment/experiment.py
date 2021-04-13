"""This module contains the class :class:`experiment` defines
an experiment and contains all the information needed to perform it.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List, Dict

from ..util import seeding

if TYPE_CHECKING:
    from palaestrai.experiment import (
        SimulationController,
        TerminationCondition,
    )

import uuid

import ruamel.yaml as yml
from ruamel.yaml.constructor import ConstructorError

from palaestrai.agent import AgentConductor
from palaestrai.environment import EnvironmentConductor
from palaestrai.util.dynaloader import load_with_params

from . import LOG


class ExperimentDefinitionError(RuntimeError):
    def __init__(self, experiment: Experiment, message):
        super().__init__(message)
        self.message = message
        self.experiment = experiment

    def __str__(self):
        return "%s (%s)" % (self.message, self.experiment)


class Experiment:
    """Defines an experiment and stores information.

    The experiment class defines an experiment in palaestrai.
    It contains all information needed to run the experiment.
    With the setup function the experiment can be built.

    Parameters
    ----------
    env_configs : list
        Contains all configuration information needed by the
        environment.
    agent_configs : list
        Contains all configuration information needed by the agent.
    experiment_config : dict
        Contains all information needed for the experiment run itself.
    seed: int
        Seed for recreation
    id : uuid4
        A unique identifier to identify the experiment.

    """

    def __init__(
        self,
        env_configs: list[dict],
        agent_configs: list[dict],
        experiment_config: dict,
        seed: int,
        id=None,
    ):
        if seed is None:
            self.seed: int = seeding.create_seed()
        else:
            self.seed = seed

        if id is None:
            self.id = "Experiment-%s" % uuid.uuid4()
            LOG.error(
                "Experiment has no id, please set one to identify it "
                "(assign the 'id' key). "
                "Generated: '%s', so that you can find it in the store.",
                self.id,
            )
        else:
            self.id = id
        self.env_configs = env_configs

        self.agent_config_list = agent_configs
        self.experiment_config: dict = experiment_config

        self._agent_conductors: dict[str, list[AgentConductor]] = {}
        self._environment_conductors: dict[
            str, list[EnvironmentConductor]
        ] = {}
        self._simulation_controllers: dict[
            str, list[SimulationController]
        ] = {}
        self._agent_configs: dict[str, dict] = {}

        rgtc = self.experiment_config["termination_conditions"]["run_governor"]
        LOG.debug(
            "Experiment loading RunGovernor TerminationCondition: %s" % rgtc
        )
        try:
            rgtc = load_with_params(rgtc["condition"], rgtc["params"])
        except Exception as e:
            LOG.critical(
                "Could not load termination condition for RunGovernor: "
                "%s, in load_with_params(%s, %s)"
                % (e, rgtc["condition"], rgtc["params"])
            )
            raise e
        self.run_governor_termination_condition: TerminationCondition = rgtc

    def setup(self, broker_uri):
        """Sets an experiment up: Creates & configures relevant actors."""
        LOG.debug("Experiment(id=0x%x, uid=%s) setup", id(self), self.id)
        for env_config in self.env_configs:
            ec = EnvironmentConductor(
                env_config["env_type"],
                {
                    "params": env_config["env_params"],
                    "broker_connection": broker_uri,
                },
                broker_uri,
                self.seed,
            )
            self._environment_conductors[ec.uid] = ec
        LOG.debug(
            "Experiment(id=0x%x, uid=%s) set up "
            "%d EnvironmentConductor object(s)",
            id(self),
            self.id,
            len(self._environment_conductors),
        )
        if len(self._environment_conductors) == 0:
            raise ExperimentDefinitionError(self, "No environment defined")

        for agent_config in self.agent_config_list:
            ac_conf = {key: value for key, value in agent_config.items()}
            ac = AgentConductor(broker_uri, ac_conf, self.seed)
            self._agent_conductors[ac.uid] = ac
            self._agent_configs[ac.uid] = ac_conf
        LOG.debug(
            "Experiment(id=0x%x, uid=%s) set up "
            "%d AgentConductor object(s)",
            id(self),
            self.id,
            len(self._agent_conductors),
        )
        if len(self._agent_conductors) == 0:
            raise ExperimentDefinitionError(self, "No agent defined")

        conditions = self.experiment_config["termination_conditions"][
            "simulation_controller"
        ]

        for _ in range(int(self.experiment_config["worker"])):
            sc: SimulationController = load_with_params(
                self.experiment_config["sim_type"],
                {
                    "sim_connection": broker_uri,
                    "rungov_connection": broker_uri,
                    "agent_conductor_ids": self._agent_conductors.keys(),
                    "environment_conductor_ids": self._environment_conductors.keys(),
                    "termination_conditions": conditions,
                    "agents": self._agent_configs,
                },
            )
            self._simulation_controllers[sc.uid] = sc
        LOG.debug(
            "Experiment(id=0x%x, uid=%s) set up "
            "%d SimulationController object(s)",
            id(self),
            self.id,
            len(self._simulation_controllers),
        )
        if len(self._simulation_controllers) == 0:
            raise ExperimentDefinitionError(
                self,
                "No simulation controllers defined: Either 'workers' is <1 "
                "or the 'sim_type' is not available",
            )
        LOG.debug(
            "Experiment(id=0x%x, uid=%s) setup complete", id(self), self.id
        )

    @property
    def environment_conductors(self) -> Dict[str, List[EnvironmentConductor]]:
        return self._environment_conductors

    @property
    def agent_conductors(self) -> Dict[str, List[AgentConductor]]:
        return self._agent_conductors

    @property
    def simulation_controllers(self) -> Dict[str, List[SimulationController]]:
        return self._simulation_controllers

    @classmethod
    def to_yaml(cls, representer: yml.YAML.representer, node):  # type: ignore
        return representer.represent_dict(  # type: ignore
            {
                "id": node.id,
                "seed": node.seed,
                "envs": node.env_configs,
                "agents": node.agent_config_list,
                "experiment": node.experiment_config,
            }
        )

    @staticmethod
    def load(stream):
        """Load an experiment from any readable file descriptor.

        Parameters
        ----------
        stream : Any text stream
            The text stream from which the experiment is loaded.

        Returns
        -------
        :class:`.Experiment`
            An initialized experiment object.

        """
        LOG.debug("Loading configuration from %s", stream)
        if isinstance(stream, str):
            try:
                stream = open(stream, "r")
            except OSError as e:
                LOG.error("Could not open experiment configuration: %s", e)
                raise e
        try:
            conf = yml.YAML(typ="safe", pure=True).load(stream)
            LOG.debug("Loaded configuration: %s", conf)
        except ConstructorError as e:
            LOG.error("Could not load experiment configuration: %s", e)
            raise e
        finally:
            stream.close()
        LOG.debug("Loaded configuration: %s", conf)

        return Experiment(
            id=conf["id"] if "id" in conf else None,
            seed=conf["seed"] if "seed" in conf else None,
            env_configs=conf["envs"],
            agent_configs=conf["agents"],
            experiment_config=conf["experiment"],
        )

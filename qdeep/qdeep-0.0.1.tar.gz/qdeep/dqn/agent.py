""" DQN agent implementation.

Heavily based on: https://github.com/deepmind/acme/blob/master/acme/agents/tf/dqn/agent.py
"""

import copy
from typing import Optional, List, Dict

import numpy as np
import reverb
import sonnet as snt
import tensorflow as tf
import trfl
from acme import datasets
from acme import specs
from acme.adders import reverb as adders
from acme.agents import agent
from acme.agents.tf import actors
from acme.tf import utils as tf2_utils
from acme.utils import loggers

from qdeep.dqn import learning


class DQNAgent(agent.Agent):
    """ DQN agent.

    This implements a single-process DQN agent. This is a simple Q-learning
    algorithm that inserts N-step transitions into a replay buffer, and
    periodically updates its policy by sampling these transitions using
    prioritization.

    Args:
        environment_spec: description of the actions, observations, etc.
        network: the online Q network (the one being optimized)
        batch_size: batch size for updates.
        prefetch_size: size to prefetch from replay.
        target_update_period: number of learner steps to perform before
            updating the target networks.
        samples_per_insert: number of samples to take from replay for every
            insert that is made.
        min_replay_size: minimum replay size before updating. This and all
            following arguments are related to dataset construction and will be
            ignored if a dataset argument is passed.
        max_replay_size: maximum replay size.
        importance_sampling_exponent: power to which importance weights are
            raised before normalizing.
        priority_exponent: exponent used in prioritized sampling.
        n_step: number of steps to squash into a single transition.
        epsilon: probability of taking a random action; ignored if a policy
            network is given.
        learning_rate: learning rate for the q-network update.
        discount: discount to use for TD updates.
        logger: logger object to be used by learner.
        max_gradient_norm: used for gradient clipping.
        expert_data: List of dictionaries containing the expert data to be added
            to the agent's replay memory. Each dictionary represents and episode
            and must have two keys: "first" and "mid". The "first" key's value
            must be a `TimeStep` object of the type `StepType.FIRST`. The "mid"
            key's value, on the other hand, must be a list containing tuples
            with, respectively, an action and a `TimeStep` object.
    """

    def __init__(
            self,
            environment_spec: specs.EnvironmentSpec,
            network: snt.Module,
            batch_size: int = 32,
            prefetch_size: int = 4,
            target_update_period: int = 100,
            samples_per_insert: float = 32.0,
            min_replay_size: int = 1000,
            max_replay_size: int = 100000,
            importance_sampling_exponent: float = 0.2,
            priority_exponent: float = 0.6,
            n_step: int = 5,
            epsilon: Optional[float] = 0.05,
            learning_rate: float = 1e-3,
            discount: float = 0.99,
            logger: loggers.Logger = None,
            max_gradient_norm: Optional[float] = None,
            expert_data: List[Dict] = None,
    ) -> None:
        """ Initialize the agent. """

        # Create a replay server to add data to. This uses no limiter behavior
        # in order to allow the Agent interface to handle it.
        replay_table = reverb.Table(
            name=adders.DEFAULT_PRIORITY_TABLE,
            sampler=reverb.selectors.Prioritized(priority_exponent),
            remover=reverb.selectors.Fifo(),
            max_size=max_replay_size,
            rate_limiter=reverb.rate_limiters.MinSize(1),
            signature=adders.NStepTransitionAdder.signature(environment_spec))
        self._server = reverb.Server([replay_table], port=None)

        # The adder is used to insert observations into replay.
        address = f'localhost:{self._server.port}'
        adder = adders.NStepTransitionAdder(
            client=reverb.Client(address),
            n_step=n_step,
            discount=discount)

        # Adding expert data to the replay memory:
        if expert_data is not None:
            for d in expert_data:
                adder.add_first(d["first"])
                for (action, next_ts) in d["mid"]:
                    adder.add(np.int32(action), next_ts)

        # The dataset provides an interface to sample from replay.
        replay_client = reverb.TFClient(address)
        dataset = datasets.make_reverb_dataset(
            server_address=address,
            batch_size=batch_size,
            prefetch_size=prefetch_size)

        # Creating the epsilon greedy policy network:
        epsilon = tf.Variable(epsilon)
        policy_network = snt.Sequential([
            network,
            lambda q: trfl.epsilon_greedy(q, epsilon=epsilon).sample(),
        ])

        # Create a target network.
        target_network = copy.deepcopy(network)

        # Ensure that we create the variables before proceeding (maybe not
        # needed).
        tf2_utils.create_variables(network, [environment_spec.observations])
        tf2_utils.create_variables(target_network,
                                   [environment_spec.observations])

        # Create the actor which defines how we take actions.
        actor = actors.FeedForwardActor(policy_network, adder)

        # The learner updates the parameters (and initializes them).
        learner = learning.DQNLearner(
            network=network,
            target_network=target_network,
            discount=discount,
            importance_sampling_exponent=importance_sampling_exponent,
            learning_rate=learning_rate,
            target_update_period=target_update_period,
            dataset=dataset,
            replay_client=replay_client,
            max_gradient_norm=max_gradient_norm,
            logger=logger,
        )

        super().__init__(
            actor=actor,
            learner=learner,
            min_observations=max(batch_size, min_replay_size),
            observations_per_step=float(batch_size) / samples_per_insert)

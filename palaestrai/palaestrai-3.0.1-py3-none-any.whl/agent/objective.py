"""This module contains the abstract baseclass :class:`.Objective`, 
from which all other objectives should be derived.

"""
from abc import ABC, abstractmethod


class Objective(ABC):
    """The base class for all objectives.

    An objective defines the goal of an agent and changing the
    objective can, e.g., transform an attacker agent to a defender
    agent.

    The objective can, e.g., a wrapper for the reward of the
    environment and, in the easiest case, the sign of the reward
    is flipped (or not) to define attacker or defender. However, the
    objective can as well use a complete different
    formula.

    """

    @abstractmethod
    def internal_reward(self, **kwargs):
        """Calculate the reward of this objective.

        This function takes a variable number of keywords (see the
        implementation of the concrete objective) and calculates an
        so-called internal reward.

        """
        raise NotImplementedError

from typing import List

from duckietown_challenges_runner.runner import dt_challenges_evaluator_
from .cli_common import ChallengeEnvironment

__all__ = ["dt_challenges_cli_evaluator"]


def dt_challenges_cli_evaluator(args: List[str], environment: ChallengeEnvironment):
    """ Runs an evaluator. """
    dt_challenges_evaluator_(args, token=environment.token)

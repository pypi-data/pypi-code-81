from typing import List

from duckietown_challenges_runner.runner_local import runner_local_main_
from .cli_common import ChallengeEnvironment

__all__ = ["dt_challenges_cli_evaluate"]


def dt_challenges_cli_evaluate(args: List[str], environment: ChallengeEnvironment):
    """ Evaluates a submission locally. """
    runner_local_main_(args, token=environment.token)

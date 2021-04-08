import argparse
from typing import List

from duckietown_challenges import follow_submission
from .cli_common import ChallengeEnvironment, wrap_server_operations

usage = """

To follow the fate of the submission, use:

    %(prog)s --submission ID


"""

__all__ = ["dt_challenges_cli_follow"]


def dt_challenges_cli_follow(args: List[str], environment: ChallengeEnvironment):
    """ Follows the fate of a submission. """
    prog = "dts challenges follow"

    parser = argparse.ArgumentParser(prog=prog, usage=usage)
    parser.add_argument("--submission", required=True, type=int)
    parsed = parser.parse_args(args)

    token = environment.token

    submission_id = parsed.submission

    with wrap_server_operations():
        follow_submission(token, submission_id)

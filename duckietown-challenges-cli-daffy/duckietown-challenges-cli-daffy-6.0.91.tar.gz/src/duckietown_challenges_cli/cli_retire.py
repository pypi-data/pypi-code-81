import argparse
from typing import List

from duckietown_challenges import dtserver_retire
from .cli_common import ChallengeEnvironment, sprint, wrap_server_operations

usage = """

To retire the submission ID, use:

    dts challenges retire --submission ID


"""

__all__ = ["dt_challenges_cli_retire"]


def dt_challenges_cli_retire(args: List[str], environment: ChallengeEnvironment):
    """ Retires a submission. """
    prog = "dts challenges retire"

    parser = argparse.ArgumentParser(prog=prog, usage=usage)
    parser.add_argument("--submission", required=True, type=int)
    parsed = parser.parse_args(args)

    token = environment.token

    submission_id = parsed.submission

    with wrap_server_operations():
        submission_id = dtserver_retire(token, submission_id)

    sprint("Successfully retired submission %s" % submission_id)

import argparse
from typing import List

from duckietown_challenges import dtserver_reset_job, dtserver_reset_submission
from duckietown_challenges_runner.exceptions import UserError
from .cli_common import ChallengeEnvironment, sprint, wrap_server_operations

__all__ = ["dt_challenges_cli_reset"]


def dt_challenges_cli_reset(args: List[str], environment: ChallengeEnvironment):
    """ Resets a submission (forces re-doing of jobs) """
    token = environment.token

    parser = argparse.ArgumentParser(prog="dts challenges reset")
    parser.add_argument("--job", default=None, help="Only reset this particular job", type=int)
    parser.add_argument(
        "--submission", default=None, type=int, help="Reset this particular submission",
    )
    parser.add_argument("--step", default=None, help="Only reset this particular step")
    parser.add_argument("--impersonate", default=None)
    parsed = parser.parse_args(args)

    if parsed.submission is None and parsed.job is None:
        msg = "You need to specify either --job or --submission."

        raise UserError(msg)

    with wrap_server_operations():
        if parsed.submission is not None:

            submission_id = dtserver_reset_submission(
                token, submission_id=parsed.submission, impersonate=parsed.impersonate, step_name=parsed.step,
            )
            sprint("Successfully reset %s" % submission_id)
        elif parsed.job is not None:

            job_id = dtserver_reset_job(token, job_id=parsed.job, impersonate=parsed.impersonate)
            sprint("Successfully reset %s" % job_id)
        else:
            assert False

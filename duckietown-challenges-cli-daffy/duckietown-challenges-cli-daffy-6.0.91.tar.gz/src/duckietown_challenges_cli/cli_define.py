import argparse
import os
from typing import List

import docker
from zuper_commons.types import ZValueError
from zuper_ipce import object_from_ipce

from duckietown_challenges import ChallengeDescription, read_yaml_file
from duckietown_challenges_runner.exceptions import UserError
from . import logger
from .cli_common import ChallengeEnvironment, wrap_server_operations
from .cmd_define import dts_define, Replication

__all__ = ["dt_challenges_cli_define"]


def dt_challenges_cli_define(args: List[str], environment: ChallengeEnvironment):
    """ [admin only] Defines a challenge. """
    parser = argparse.ArgumentParser(prog=environment.prog)
    parser.add_argument("--config", default="challenge.yaml", help="YAML configuration file")

    parser.add_argument("--no-cache", default=False, action="store_true")
    parser.add_argument("--steps", default=None, help="Which steps (comma separated)")
    parser.add_argument("--force-invalidate-subs", default=False, action="store_true")
    parser.add_argument("-C", dest="cwd", default=None, help="Base directory")
    parser.add_argument("--impersonate", type=str, default=None)
    parser.add_argument("--no-pull", default=False, action="store_true")
    parser.add_argument(
        "--replicate", default=[], action="append", help="replicate step --replicate STEP:1", required=False
    )

    parsed = parser.parse_args(args)
    impersonate = parsed.impersonate

    token = environment.token
    # username = environment.docker_credentials['docker.io']['username']
    client = docker.from_env()

    replication = []
    for x in parsed.replicate:
        a, _, n = x.partition(":")
        n = int(n)
        replication.append(Replication(a, n))
    if parsed.cwd is not None:
        logger.info(f"Changing to directory {parsed.cwd}")
        if not os.path.exists(parsed.cwd):
            msg = "Directory to change to does not exist."
            raise ZValueError(msg, cwd=parsed.cwd)
        os.chdir(parsed.cwd)

    no_cache = parsed.no_cache

    fn = os.path.join(parsed.config)
    if not os.path.exists(fn):
        msg = f"File {fn!r} does not exist."
        raise UserError(msg)

    data = read_yaml_file(fn)

    if "description" not in data or data["description"] is None:
        fnd = os.path.join(os.path.dirname(fn), "challenge.description.md")
        if os.path.exists(fnd):
            desc = open(fnd).read()
            data["description"] = desc
            msg = f"Read description from {fnd!r}"
            logger.info(msg)

    base = os.path.dirname(fn)
    logger.info(data=data)
    if "challenge" in data:
        challenge = ChallengeDescription.from_yaml(data)
    else:
        challenge = object_from_ipce(data, ChallengeDescription)

    assert challenge.date_close.tzinfo is not None, (
        challenge.date_close.tzinfo,
        challenge.date_open.tzinfo,
    )
    assert challenge.date_open.tzinfo is not None, (
        challenge.date_close.tzinfo,
        challenge.date_open.tzinfo,
    )

    for dep in challenge.dependencies:
        if challenge.name == dep:
            raise ZValueError(f"invalid recursive dependency {dep}")

    # logger.info("read challenge", challenge=challenge)
    with wrap_server_operations():
        dts_define(
            token=token,
            dopull=not parsed.no_pull,
            impersonate=impersonate,
            force_invalidate=parsed.force_invalidate_subs,
            steps=parsed.steps,
            challenge=challenge,
            base=base,
            client=client,
            no_cache=no_cache,
            credentials=environment.docker_credentials,
            replicate=replication,
        )

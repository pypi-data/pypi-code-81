import argparse
from typing import List

from docker import DockerClient

from duckietown_build_utils import (
    docker_pull_retry,
    DockerCompleteImageName,
)
from . import logger
from .cli_common import ChallengeEnvironment

__all__ = ["dt_pull"]


def dt_pull(args: List[str], environment: ChallengeEnvironment):
    """ Pull a container """
    parser = argparse.ArgumentParser(prog=environment.prog)

    parsed, rest = parser.parse_known_args(args)

    image = DockerCompleteImageName(rest[0])
    client = DockerClient.from_env()
    obtained = docker_pull_retry(
        client, image, ntimes=10, wait=10, quiet=False, credentials=environment.docker_credentials
    )
    logger.info(obtained=obtained)

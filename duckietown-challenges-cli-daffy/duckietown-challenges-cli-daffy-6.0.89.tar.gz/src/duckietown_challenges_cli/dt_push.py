import argparse
import sys
import traceback

from duckietown_build_utils import docker_push_optimized, DockerCompleteImageName, DockerCredentials
from . import logger

__all__ = ["dt_push_main"]


def dt_push_main(args=None, credentials: DockerCredentials = None):
    parser = argparse.ArgumentParser()
    # parser.add_argument("--image", required=True)
    parsed, rest = parser.parse_known_args(args=args)

    # noinspection PyBroadException
    try:
        if len(rest) != 1:
            raise Exception("need exactly one argument")

        image = DockerCompleteImageName(rest[0])
        logger.info(f"pushing image {image}")
        docker_push_optimized(image, credentials=credentials)
    except SystemExit:
        raise
    except BaseException:
        logger.error(traceback.format_exc())
        sys.exit(3)

import subprocess
from typing import Set, Tuple

from zuper_commons.types import ZException

from . import logger
from .buildresult import parse_complete_tag
from .credentials import DockerCredentials
from .types import DockerCompleteImageName, DockerRegistryName, DockerSecret, DockerUsername

__all__ = ["DockerLoginError", "docker_login", "do_login_for_registry"]


class DockerLoginError(ZException):
    pass


class LoggedInStorage:
    done: Set[Tuple[DockerRegistryName, DockerUsername]] = set()


def docker_login(
    registry: DockerRegistryName, docker_username: DockerUsername, docker_password: DockerSecret
):
    k = registry, docker_username
    if k in LoggedInStorage.done:
        logger.debug(f"Already logged as {docker_username!r} to {registry}")
        return
    LoggedInStorage.done.add(k)
    cmd = ["docker", "login", "-u", docker_username, "--password-stdin", registry]
    try:
        subprocess.check_output(cmd, input=docker_password.encode(), stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:

        is_timeout = "Client.Timeout" in e.stderr.decode()
        if is_timeout:
            msg = f"Docker timeout while logging in."
            raise DockerLoginError(msg, e=e.stderr.decode()) from None

        n = len(docker_password)

        password_masked = docker_password[0] + "*" * (n - 2) + docker_password[-1]
        msg = f'Failed to login with username "{docker_username}".'
        msg += f" password is {password_masked}"
        raise DockerLoginError(
            msg, cmd=e.cmd, returncode=e.returncode, output=e.output.decode(), stderr=e.stderr.decode()
        ) from e
    logger.debug(f"docker login to {registry} username {docker_username} OK")


def do_login_for_image(credentials: DockerCredentials, im: DockerCompleteImageName):
    if im is None:
        raise ValueError("im is None")
    try:
        br = parse_complete_tag(im)
        do_login_for_registry(credentials, br.registry)
    except Exception as e:
        msg = f"Could not log in for image {im!r}"
        raise Exception(msg) from e


def do_login_for_registry(credentials: DockerCredentials, registry: DockerRegistryName):
    if registry is None:
        raise ValueError("registry is None")
    if registry in credentials:
        docker_login(registry, credentials[registry]["username"], credentials[registry]["secret"])
    else:
        logger.warn(f"No credentials to login to registry {registry!r}", known=list(credentials))

# import getpass
# import grp
# import os
# import subprocess
#
# from zuper_commons.text import indent
# from zuper_commons.types import ZException
#
# from duckietown_docker_utils import ENV_REGISTRY
# from . import logger
# from .cli_common import ChallengeEnvironment
#
# __all__ = ["do_docker_login", "DockerLoginError"]
#
#
# class DockerLoginError(ZException):
#     pass
#
#
# def do_docker_login(ce: ChallengeEnvironment, force=False):
#     AIDO_REGISTRY = os.environ.get(ENV_REGISTRY, "docker.io")
#     if not force and ("duckietown.org" in AIDO_REGISTRY):
#         logger.info(f"No need to login for registry {AIDO_REGISTRY}")
#         return
#     cmd = ["docker", "login", "-u", ce.docker_username, "--password-stdin"]
#     try:
#         subprocess.check_output(cmd, input=ce.docker_password.encode(), stderr=subprocess.PIPE)
#     except subprocess.CalledProcessError as e:
#
#         is_timeout = "Client.Timeout" in e.stderr.decode()
#         if is_timeout:
#             msg = f"Docker timeout while logging in:\n{indent(e.stderr.decode(), '  ')}"
#             raise DockerLoginError(msg) from None
#
#         n = len(ce.docker_password)
#
#         password_masked = ce.docker_password[0] + "*" * (n - 2) + ce.docker_password[-1]
#         msg = f'Failed to login with username "{ce.docker_username}".'
#         msg += f" password is {password_masked}"
#         raise DockerLoginError(
#             msg,
#             cmd=e.cmd,
#             returncode=e.returncode,
#             output=e.output.decode(),
#             stderr=e.stderr.decode(),
#             uid=os.getuid(),
#             group_ids=[g.gr_gid for g in grp.getgrall() if getpass.getuser() in g.gr_mem],
#         ) from e
#     logger.info("docker login ok")

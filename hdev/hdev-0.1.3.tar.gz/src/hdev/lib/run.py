"""Functions to run processes in behalf of hdev users."""

import os
import subprocess


def list_tox_environments():
    """Return a list of available tox environments."""
    result = subprocess.run("tox -a", shell=True, check=True, stdout=subprocess.PIPE)
    return result.stdout.decode().strip().split("\n")


def run_tox(tox_env, cmd, check=True, extra_dependencies_path=None):
    """Run a `cmd` inside tox environment `env`.

    :param tox_env: which tox environment to run the command in
    :param cmd: command to run
    :param check: passed to subporcess.run, fail if the exit code is an error
    :param extra_dependencies_path: path to a requirements file to include as dependencies
    :return: Info of the subprocess. Same as subprocess.run
    :rtype: subprocess.CompletedProcess
    """
    env_vars = os.environ.copy()

    if extra_dependencies_path:
        env_vars["EXTRA_DEPS"] = f"-r {extra_dependencies_path}"

    return subprocess.run(
        f'tox -e {tox_env} --run-command "{cmd}"',
        shell=True,
        check=check,
        env=env_vars,
    )

"""Wrappers for access to tox functionality."""

import os
import subprocess


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

    command = f"tox -e {tox_env} --run-command '{cmd}'"
    return subprocess.run(command, shell=True, check=check, env=env_vars)

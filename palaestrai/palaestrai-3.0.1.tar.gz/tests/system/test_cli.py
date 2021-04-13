"""This module contains the debug script that can be used to start
the dummy experiment without the CLI.

"""
import os
from typing import AnyStr, Generic

from palaestrai.cli.manager import cli
from click.testing import CliRunner, Result

debug_script_path: str = os.path.abspath(
    f"{__file__}/../../fixtures/dummy_experiment.yml"
)

runtime_path: str = os.path.abspath(
    f"{__file__}/../../fixtures/arl-runtime-debug.conf.yaml"
)


def test_system_experiment_start() -> None:
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(
        cli, ["-c", runtime_path, "-vv", "experiment-start", debug_script_path]
    )
    assert result.exit_code == 0


if __name__ == "__main__":
    test_system_experiment_start()

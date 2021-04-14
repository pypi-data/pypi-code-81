from click.testing import CliRunner
from .__main__ import main

def test_start_project():
    runner = CliRunner()
    result = runner.invoke(main,["startproject"])
    assert result.exit_code == 0

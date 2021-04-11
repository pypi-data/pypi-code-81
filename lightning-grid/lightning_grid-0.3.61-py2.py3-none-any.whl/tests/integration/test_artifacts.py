from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

from click.testing import CliRunner

from grid import cli
from grid.cli.grid_artifacts import _download_artifacts
from grid.core import Artifact

RUNNER = CliRunner()


@patch("grid.cli.grid_artifacts.Experiment", autospec=True)
@patch("grid.cli.grid_artifacts.Run", autospec=True)
def test_artifacts_succeeds(experiment, run):
    """grid train without arguments fails"""
    experiment.artifacts = MagicMock()
    run.experiments = MagicMock()

    result = RUNNER.invoke(cli.artifacts, ["foo-bar", "foo-bar-exp0"])
    assert result.exit_code == 0
    assert not result.exception


def test_download_artifacts(tmpdir):
    artifact = Artifact(url="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                        path="test-path/",
                        filename="google.png")

    # path to download
    file_path = tmpdir / Path(artifact.path) / Path(artifact.filename)

    # download and verify
    _download_artifacts(artifacts=[artifact], download_dir=tmpdir)
    assert Path(file_path).exists()

from click.testing import CliRunner
from tests.mock_backend import resolvers
from tests.utilities import create_test_credentials
from tests.utilities import monkey_patch_client

from grid import cli
import grid.client as grid

RUNNER = CliRunner()


class TestCancel:
    @classmethod
    def setup_class(cls):
        grid.Grid._init_client = monkey_patch_client
        grid.gql = lambda x: x

        create_test_credentials()

    def test_cancel_without_arguments(self):
        """grid cancel without arguments fails"""
        result = RUNNER.invoke(cli.cancel, [])
        assert result.exit_code == 0
        result.stdout_bytes.decode('utf-8').startswith('Usage')

    def test_cancel_experiment(self):
        """grid cancel experiments with single and multi-input"""
        experiments = [f'test-experiment-exp{i}' for i in range(5)]

        result = RUNNER.invoke(cli.cancel, ["experiment", experiments[0]])
        assert result.exit_code == 0
        assert not result.exception
        assert 'cancelled successfully' in result.output

        result = RUNNER.invoke(cli.cancel, ["experiment", *experiments])
        assert result.exit_code == 0
        assert not result.exception
        assert 'cancelled successfully' in result.output

    def test_cancel_runs(self):
        """grid cancel Runs with single and multi-input"""
        runs = [f'test-run-{i}' for i in range(5)]
        result = RUNNER.invoke(cli.cancel, ["run", runs[0]])
        assert result.exit_code == 0
        assert not result.exception
        assert 'cancelled successfully' in result.output

        result = RUNNER.invoke(cli.cancel, ["run", *runs])
        assert result.exit_code == 0
        assert not result.exception
        assert 'cancelled successfully' in result.output

    def test_cancel_experiment_fails(self, monkeypatch):
        def mp_cancel_experiment(*args, **kwargs):
            return {'success': False}

        monkeypatch.setattr(resolvers, 'cancel_experiment', mp_cancel_experiment)
        result = RUNNER.invoke(cli.cancel, ["experiment", "some-experiment"])
        assert result.exit_code == 1
        assert result.exception
        assert 'Cancel failed' in result.output

    def test_cancel_run_fails(self, monkeypatch):
        def mp_cancel_run(*args, **kwargs):
            return {'success': False}

        monkeypatch.setattr(resolvers, 'cancel_run', mp_cancel_run)
        result = RUNNER.invoke(cli.cancel, ["run", "some-run"])
        assert result.exit_code == 1
        assert result.exception
        assert 'Cancel failed' in result.output

    def test_cancel_experiment_fails_when_experiment_not_found(self, monkeypatch):
        def mp_get_experiment_id(*args, **kwargs):
            return {"success": False}

        monkeypatch.setattr(resolvers, 'get_experiment_id', mp_get_experiment_id)
        result = RUNNER.invoke(cli.cancel, ["experiment", "some-experiment"])
        assert result.exit_code == 1
        assert result.exception
        assert 'Cancel failed' in result.output
        assert 'Could not find experiment' in result.output

    def test_cancel_experiment_fails_when_experiment_not_found_exception(self, monkeypatch):
        def mp_get_experiment_id(*args, **kwargs):
            raise Exception()

        monkeypatch.setattr(resolvers, 'get_experiment_id', mp_get_experiment_id)
        result = RUNNER.invoke(cli.cancel, ["experiment", "some-experiment"])
        assert result.exit_code == 1
        assert result.exception
        assert 'Cancel failed' in result.output
        assert 'Could not find experiment' in result.output

import click
from click.testing import CliRunner
from tests.utilities import create_test_credentials
from tests.utilities import monkey_patch_client

from grid import cli
from grid.client import Grid
import grid.client as grid
import grid.globals as env


class TestView:
    """Test case for the view command"""
    @classmethod
    def setup_class(cls):
        cls.runner = CliRunner()

        cls.credentials_path = 'tests/data/credentials.json'
        cls.test_run = 'manual-test-run'
        cls.test_exp = 'manual-test-run-exp0'

        # Setup the global DEBUG flag to True.
        env.DEBUG = True

        #  Monkey patches the GraphQL client to read from a local schema.
        grid.Grid._init_client = monkey_patch_client
        grid.gql = lambda x: x

        create_test_credentials()

    def monkey_patched_method(self, *args, **kwargs):
        return True

    def monkey_patch_grid_status(self, *args, **kwargs):
        result = {'getRuns': [{'name': self.test_run}]}
        return result

    def monkey_patch_grid_status_not_ready(self, *args, **kwargs):
        result = {'getRuns': [{'name': self.test_run}]}
        return result

    def monkey_patch_exception(self, *args, **kwargs):
        raise click.ClickException('test')

    def test_view_opens_browser(self, monkeypatch):
        """grid view RUN_ID opens browser."""
        monkeypatch.setattr(click, 'launch', self.monkey_patched_method)

        result = self.runner.invoke(cli.view, ["run", self.test_run])

        assert result.exit_code == 0
        assert 'http' in result.output
        assert 'run' in result.output
        assert self.test_run in result.output

        result = self.runner.invoke(cli.view, ["experiment", f'{self.test_run}-exp1'])
        assert result.exit_code == 0
        assert 'http' in result.output
        assert 'experiment' in result.output
        assert self.test_run in result.output

    def test_view_exception(self, monkeypatch):
        monkeypatch.setattr(click, 'launch', self.monkey_patched_method)

        old_status = Grid.status
        monkeypatch.setattr(Grid, 'status', self.monkey_patch_exception)

        # Set attribute again.
        monkeypatch.setattr(Grid, 'status', old_status)

from tests.utilities import monkey_patch_client

import grid.client as grid
from grid.core import Experiment
from grid.core import Run
from grid.core.task import Task


class TestRun:
    @classmethod
    def setup_class(cls):
        grid.Grid._init_client = monkey_patch_client
        grid.gql = lambda x: x

    def test_run_refresh(self):
        R = Run("test")
        R.refresh()

        assert R.name
        assert R.run_id

    def test_experiment_artifacts(self):
        R = Run("test")

        assert len(R.experiments) > 0
        for experiment in R.experiments:
            assert isinstance(experiment, Experiment)

    def test_tasks(self):
        R = Run("test")
        assert len(R.tasks) > 0
        assert all(isinstance(t, Task) for t in R.tasks)

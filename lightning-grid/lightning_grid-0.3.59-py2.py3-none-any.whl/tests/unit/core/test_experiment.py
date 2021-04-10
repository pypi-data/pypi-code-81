from tests.utilities import monkey_patch_client

import grid.client as grid
from grid.core import Artifact
from grid.core import Experiment


class TestExperiment:
    @classmethod
    def setup_class(cls):
        grid.Grid._init_client = monkey_patch_client
        grid.gql = lambda x: x

    def test_experiment_refresh(self):
        E = Experiment("test")
        E.refresh()

        assert E.name
        assert E.status

    def test_experiment_artifacts(self):
        E = Experiment("test")
        E.refresh()

        assert len(E.artifacts) > 0
        for artifact in E.artifacts:
            assert isinstance(artifact, Artifact)

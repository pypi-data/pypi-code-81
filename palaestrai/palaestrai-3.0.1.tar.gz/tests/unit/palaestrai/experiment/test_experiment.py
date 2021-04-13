import os.path
import unittest
import uuid
from unittest.mock import MagicMock, patch

import palaestrai.experiment.experiment
from tests import dummy_exp_path


class _UidentifiableMock(MagicMock):
    def __init__(self, id=None):
        super().__init__()
        self.uid = id if id else str(uuid.uuid4())


def load_with_params_side_effect(*args, **kwargs):
    return _UidentifiableMock()


@patch(
    "palaestrai.experiment.experiment.AgentConductor",
    MagicMock(side_effect=load_with_params_side_effect),
)
@patch(
    "palaestrai.experiment.experiment.load_with_params",
    MagicMock(side_effect=load_with_params_side_effect),
)
class ExperimentTest(unittest.TestCase):
    def setUp(self):
        dummy_exp_path = os.path.realpath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "../../../fixtures/dummy_experiment.yml",
            )
        )
        self.env_dic = [
            {
                "env_type": "",
                "env_params": {
                    "params": dict(),
                },
            }
        ]
        self.agent_dic = [
            {
                "name": "defender",
                "brain": "",
                "brain_params": dict(),
                "muscle": "",
                "muscle_params": dict(),
                "objective": "",
                "objective_params": dict(),
                "sensors": list(),
                "actuators": list(),
            },
            {
                "name": "attacker",
                "brain": "",
                "brain_params": dict(),
                "muscle": "",
                "muscle_params": dict(),
                "objective": "",
                "objective_params": dict(),
                "sensors": list(),
                "actuators": list(),
            },
        ]

        self.experiment_dic = {
            "sim_type": "",
            "sim_param": dict(),
            "sim_connection": "",
            "store_uri": "",
            "worker": 2,
            "termination_conditions": {
                "run_governor": {
                    "condition": (
                        "palaestrai.experiment.vanilla_rungovernor_termination"
                        "_condition:VanillaRunGovernorTerminationCondition"
                    ),
                    "params": dict(),
                },
                "simulation_controller": list(),
            },
            "is_local": True,
        }

    def test_properties(self):
        """Assert Not Empty list"""
        exp = palaestrai.experiment.experiment.Experiment(
            self.env_dic,
            self.agent_dic,
            self.experiment_dic,
            123,
            id="test_properties",
        )
        self.assertFalse(len(exp.environment_conductors))
        self.assertFalse(len(exp.agent_conductors))
        self.assertFalse(len(exp.simulation_controllers))

    def test_setup(self):
        """Assert setup"""
        exp = palaestrai.experiment.experiment.Experiment(
            self.env_dic,
            self.agent_dic,
            self.experiment_dic,
            123,
            id="test_setup",
        )
        exp.setup(broker_uri=None)
        self.assertEqual(
            len(exp.simulation_controllers), self.experiment_dic["worker"]
        )
        self.assertEqual(len(exp.agent_conductors), len(self.agent_dic))
        self.assertEqual(len(exp.environment_conductors), len(self.env_dic))

    def test_load_from_file(self):
        import palaestrai.experiment.experiment

        e = palaestrai.experiment.experiment.Experiment.load(dummy_exp_path)
        self.assertTrue(e.env_configs)
        self.assertTrue(e.agent_config_list)
        self.assertTrue(e.experiment_config)

    def test_load_from_stream(self):
        import palaestrai.experiment.experiment

        with open(dummy_exp_path, "r") as stream_:
            e = palaestrai.experiment.experiment.Experiment.load(stream_)
        self.assertTrue(e.env_configs)
        self.assertTrue(e.agent_config_list)
        self.assertTrue(e.experiment_config)

    def test_dump(self):
        import palaestrai.experiment.experiment
        from io import StringIO
        import ruamel.yaml as yml
        from palaestrai.experiment import Experiment

        sio = StringIO()
        yaml = yml.YAML(typ="safe")
        yaml.register_class(Experiment)
        e = palaestrai.experiment.experiment.Experiment.load(dummy_exp_path)
        yaml.dump(e, sio)
        with open(dummy_exp_path) as fp:
            y1 = yaml.load(fp)
        y2 = yaml.load(sio.getvalue())
        self.maxDiff = 4096
        self.assertEqual(y1, y2)


if __name__ == "__main__":
    unittest.main()

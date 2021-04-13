from unittest import TestCase

from palaestrai.experiment import VanillaSimControllerTerminationCondition
from palaestrai.core.protocol import EnvironmentUpdateResponse


class TestVanillaSimControllerTerminationCondition(TestCase):
    def test_check_termination_true(self):
        term_cond = VanillaSimControllerTerminationCondition()
        self.assertTrue(
            term_cond.check_termination(
                EnvironmentUpdateResponse(
                    sender_environment_id="0",
                    receiver_simulation_controller_id="0",
                    experiment_run_id="0",
                    environment_conductor_id="0",
                    sensors=["test"],
                    reward=0.0,
                    is_terminal=True,
                )
            )
        )

    def test_check_termination_False(self):
        term_cond = VanillaSimControllerTerminationCondition()
        self.assertFalse(
            term_cond.check_termination(
                EnvironmentUpdateResponse(
                    sender_environment_id="0",
                    receiver_simulation_controller_id="0",
                    experiment_run_id="0",
                    environment_conductor_id="0",
                    sensors=["test"],
                    reward=0.0,
                    is_terminal=False,
                )
            )
        )

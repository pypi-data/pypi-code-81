import unittest
from palaestrai.environment.random_environment import (
    ContinuousRandomEnvironment,
)


class ContinuousRandomEnvironmentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.env = ContinuousRandomEnvironment(
            None, 0, 123, {"num_sensors": 10, "max_value": 10, "max_iter": 10}
        )
        self.env.start_environment()

    def test_sensors_actuators(self):
        # the length of actuators should be the same as the specified
        # num_sensors (10)
        self.assertEqual(
            len(self.env.sensors),
            len(self.env.actuators),
            "Length of sensors and actuators did not match",
        )
        self.assertEqual(
            len(self.env.sensors), 10, "Unexpected length of sensors"
        )
        # no value in sensors or actuators should be greater than the
        # specified max_value (10)
        self.assertFalse(
            False in map(lambda x: 0 <= x() <= 10, self.env.sensors),
            "Value out of range for sensor",
        )
        self.assertFalse(
            False in map(lambda x: 0 <= x.setpoint <= 10, self.env.actuators),
            "Value out of range for actuator",
        )

    def test_reward(self):
        """Test the reward.

        The reward is defined as:
        max_value (10) - avg_discrepancy (0,1,2 respectively),
        so the resulting reward should be max_value, max_value-1,
        max_value-2, respectively.
        """
        actuators = self.env.actuators
        for i in range(len(self.env.sensors)):
            actuators[i].setpoint = round(self.env.sensors[i].sensor_value)
        self.assertEqual(
            10.0 - 0, self.env.update(actuators)[1], "unexpected reward"
        )

        for i in range(len(self.env.sensors)):
            actuators[i].setpoint = round(self.env.sensors[i].sensor_value) + 1
        self.assertEqual(
            10.0 - 1, self.env.update(actuators)[1], "unexpected reward"
        )

        for i in range(len(self.env.sensors)):
            actuators[i].setpoint = round(self.env.sensors[i].sensor_value) + 2
        self.assertEqual(
            10.0 - 2, self.env.update(actuators)[1], "unexpected reward"
        )

    def test_iteration(self):
        # The environment should terminate after the specified max_iter
        # (10) but not before
        for _ in range(10):
            self.assertNotEqual(
                (list(), 0, True),
                self.env.update(self.env.actuators),
                "Environment terminated unexpectedly",
            )
        self.assertEqual(
            (list(), 0, True),
            self.env.update(self.env.actuators),
            "Environment did not terminate on time",
        )


if __name__ == "__main__":
    unittest.main()

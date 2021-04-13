import unittest
from palaestrai.environment.random_environment import DiscreteRandomEnvironment


class DiscreteRandomEnvironmentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.env = DiscreteRandomEnvironment(
            None,
            0,
            0,
            {
                "num_sensors": 10,
                "max_value": 10,
                "max_iter": 10,
                "resolution": 100,
            },
        )
        self.env.start_environment()

    def test_sensors_actuators(self):
        # the length of actuators should be the same as the specified
        # resolution (10)
        self.assertEqual(len(self.env.actuators), 1, "expected one actuator")
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
            False in map(lambda x: 0 <= x.setpoint <= 100, self.env.actuators),
            "Value out of range for actuator",
        )

    def test_reward(self):
        """Test the reward

        The reward is defined as:

        resolution (100) - discrepancy (0,1,2 respectively)

        so the resulting reward should be resolution, resolution-1,
        resolution-2 respectively
        """
        actuator = self.env.actuators[0]
        mean_of_sensors = sum(map(lambda x: x(), self.env.sensors)) / len(
            self.env.sensors
        )
        perfect_actuator = round(
            mean_of_sensors / (self.env.max_value / self.env.resolution)
        )
        actuator.setpoint = perfect_actuator
        self.assertEqual(
            self.env.resolution,
            self.env.update([actuator])[1],
            "unexpected reward",
        )

        actuator = self.env.actuators[0]
        mean_of_sensors = sum(map(lambda x: x(), self.env.sensors)) / len(
            self.env.sensors
        )
        perfect_actuator = round(
            mean_of_sensors / (self.env.max_value / self.env.resolution)
        )
        actuator.setpoint = perfect_actuator + (
            1 if perfect_actuator < self.env.max_value - 1 else -1
        )
        self.assertEqual(
            self.env.resolution - 1,
            self.env.update([actuator])[1],
            "unexpected reward-1",
        )

        actuator = self.env.actuators[0]
        mean_of_sensors = sum(map(lambda x: x(), self.env.sensors)) / len(
            self.env.sensors
        )
        perfect_actuator = round(
            mean_of_sensors / (self.env.max_value / self.env.resolution)
        )
        actuator.setpoint = perfect_actuator + (
            2 if perfect_actuator < self.env.max_value - 2 else -2
        )
        self.assertEqual(
            self.env.resolution - 2,
            self.env.update([actuator])[1],
            "unexpected reward-2",
        )

    def test_iteration(self):
        # The environment should terminate after the specified
        # max_iter (10) but not before
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

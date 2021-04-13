import unittest
from palaestrai.environment.dummy_environment import DummyEnvironment


class DummyEnvironmentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.env = DummyEnvironment(None, 0, 123, {"test": 0})
        self.env.start_environment()

    def test_sensors_actuators(self):
        self.assertTrue(
            (len(self.env.actuators)) != 0,
            "expected at least one actuator",
        )

    def test_iteration(self):
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

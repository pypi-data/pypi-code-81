import unittest
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSErrorHandlingStarting,
    RGSStartingAgentConductors,
    RGSStartingEnvConductors,
)
from palaestrai.util.exception import EnvConductorFailedError


class TestStartingSimControllers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSStartingEnvConductors(self.rungov)
        self.rungov.state = self.rgs

    async def test_run(self):
        self.rgs._init_environment_conductors = MagicMock()

        await self.rgs.run()

        self.rgs._init_environment_conductors.assert_called_once()

    @patch(f"{RGSStartingEnvConductors.__module__}.aiomultiprocess.Process")
    def test_init_env_conductors(self, mock_amp):
        ec = MagicMock()
        type(ec).uid = PropertyMock(return_value="ec-1")

        self.rungov.experiment = MagicMock()
        self.rungov.experiment.environment_conductors = MagicMock()
        self.rungov.experiment.environment_conductors.values = MagicMock(
            return_value=[ec]
        )

        self.rgs._init_environment_conductors()

        self.assertEqual(len(self.rungov.env_conductors), 1)
        self.assertIn("ec-1", self.rungov.env_conductors)

    async def test_run_env_conductor(self):
        ec = AsyncMock()
        type(ec).uid = PropertyMock(return_value="ec-1")
        ec.run = AsyncMock()

        await self.rgs._run_environment_conductor(ec)

        # Just assert that no exception was raised.
        # There is nothing more to test here.

    async def test_run_env_conductor_with_error(self):
        ec = AsyncMock()
        type(ec).uid = PropertyMock(return_value="ec-1")
        ec.run = AsyncMock()
        ec.run.side_effect = ValueError()

        with self.assertRaises(ValueError):
            await self.rgs._run_environment_conductor(ec)

        self.assertEqual(len(self.rungov.errors), 1)
        self.assertIsInstance(
            self.rungov.errors[0][0], EnvConductorFailedError
        )

    def test_next_state(self):

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStartingAgentConductors)

    def test_next_state_with_errors(self):
        self.rgs.add_error(ValueError())

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSErrorHandlingStarting)


if __name__ == "__main__":
    unittest.main()

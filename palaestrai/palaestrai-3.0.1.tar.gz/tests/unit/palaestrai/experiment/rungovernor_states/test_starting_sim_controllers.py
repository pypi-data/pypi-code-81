import unittest
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSErrorHandlingStarting,
    RGSStartingEnvConductors,
    RGSStartingSimControllers,
)
from palaestrai.util.exception import SimControllerFailedError


class TestStartingSimControllers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSStartingSimControllers(self.rungov)
        self.rungov.state = self.rgs

    async def test_run(self):
        self.rgs._init_sim_controllers = MagicMock()

        await self.rgs.run()

        self.rgs._init_sim_controllers.assert_called_once()

    @patch(f"{RGSStartingSimControllers.__module__}.aiomultiprocess.Process")
    def test_init_sim_controllers(self, mock_amp):
        sc = MagicMock()
        type(sc).uid = PropertyMock(return_value="sim-1")

        self.rungov.experiment = MagicMock()
        self.rungov.experiment.simulation_controllers = MagicMock()
        self.rungov.experiment.simulation_controllers.values = MagicMock(
            return_value=[sc]
        )

        self.rgs._init_sim_controllers()

        self.assertEqual(len(self.rungov.sim_controllers), 1)
        self.assertIn("sim-1", self.rungov.sim_controllers)

    async def test_run_sim_controller(self):
        sc = AsyncMock()
        type(sc).uid = PropertyMock(return_value="sim-1")
        sc.run = AsyncMock()

        await self.rgs._run_simulation_controller(sc)

        # Just assert that no exception was raised.
        # There is nothing more to test here.

    async def test_run_sim_controller_with_error(self):
        sc = AsyncMock()
        type(sc).uid = PropertyMock(return_value="sim-1")
        sc.run = AsyncMock()
        sc.run.side_effect = ValueError()

        with self.assertRaises(ValueError):
            await self.rgs._run_simulation_controller(sc)

        self.assertEqual(len(self.rungov.errors), 1)
        self.assertIsInstance(
            self.rungov.errors[0][0], SimControllerFailedError
        )

    def test_next_state(self):

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStartingEnvConductors)

    def test_next_state_with_errors(self):
        self.rgs.add_error(ValueError())

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSErrorHandlingStarting)


if __name__ == "__main__":
    unittest.main()

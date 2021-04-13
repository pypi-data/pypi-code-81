import unittest
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSErrorHandlingStarting,
    RGSStartingAgentConductors,
    RGSStartingRun,
)
from palaestrai.util.exception import AgentConductorFailedError


class TestStartingSimControllers(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSStartingAgentConductors(self.rungov)
        self.rungov.state = self.rgs

    async def test_run(self):
        self.rgs._init_agent_conductors = MagicMock()

        await self.rgs.run()

        self.rgs._init_agent_conductors.assert_called_once()

    @patch(f"{RGSStartingAgentConductors.__module__}.aiomultiprocess.Process")
    def test_init_agent_conductors(self, mock_amp):
        ac = MagicMock()
        type(ac).uid = PropertyMock(return_value="ac-1")

        self.rungov.experiment = MagicMock()
        self.rungov.experiment.agent_conductors = MagicMock()
        self.rungov.experiment.agent_conductors.values = MagicMock(
            return_value=[ac]
        )

        self.rgs._init_agent_conductors()

        self.assertEqual(len(self.rungov.agent_conductors), 1)
        self.assertIn("ac-1", self.rungov.agent_conductors)

    async def test_run_agent_conductor(self):
        ac = AsyncMock()
        type(ac).uid = PropertyMock(return_value="ac-1")
        ac.run = AsyncMock()

        await self.rgs._run_agent_conductor(ac)

        # Just assert that no exception was raised.
        # There is nothing more to test here.

    async def test_run_agent_conductor_with_error(self):
        ac = AsyncMock()
        type(ac).uid = PropertyMock(return_value="ac-1")
        ac.run = AsyncMock()
        ac.run.side_effect = ValueError()

        with self.assertRaises(ValueError):
            await self.rgs._run_agent_conductor(ac)

        self.assertEqual(len(self.rungov.errors), 1)
        self.assertIsInstance(
            self.rungov.errors[0][0], AgentConductorFailedError
        )

    def test_next_state(self):

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStartingRun)

    def test_next_state_with_errors(self):
        self.rgs.add_error(ValueError())

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSErrorHandlingStarting)


if __name__ == "__main__":
    unittest.main()

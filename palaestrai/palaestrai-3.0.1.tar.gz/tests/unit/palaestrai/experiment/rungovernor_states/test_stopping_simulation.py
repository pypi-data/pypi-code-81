import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSStoppingTransceiving,
    RGSStoppingSimulation,
)
from palaestrai.core.protocol import (
    ExperimentShutdownResponse,
    SimulationStopResponse,
)


class TestStoppingSimulation(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSStoppingSimulation(self.rungov)
        self.rungov.state = self.rgs

    @patch(f"{RGSStoppingSimulation.__module__}.asyncio.wait_for")
    async def test_run(self, mock_wait):
        # self.rgs._is_experiment_running = MagicMock(return_value=False)
        # self.rgs._experiment_start = AsyncMock()
        # request = ExperimentStartRequest(None, None)
        self.rgs._prepare_reply = MagicMock()
        self.rgs._terminate_sim_controllers = MagicMock()

        # self.rungov.last_request.append(request)

        await self.rgs.run()

        self.rgs._prepare_reply.assert_called_once()
        self.rgs._terminate_sim_controllers.assert_called_once()

    def test_next_state(self):
        self.rgs.next_state()
        self.assertIsInstance(self.rungov.state, RGSStoppingTransceiving)

    async def test_terminate_sim_controllers(self):
        self.rungov.experiment = MagicMock()
        self.rungov.major_domo_client = MagicMock()
        self.rungov.major_domo_client.send = AsyncMock(
            return_value=SimulationStopResponse("run-1")
        )
        proc = MagicMock()
        proc.terminate = MagicMock()

        self.rungov.sim_controllers["sim-1"] = proc
        sc_terminated = await self.rgs._terminate_sim_controllers()

        proc.terminate.assert_not_called()
        self.assertEqual(0, len(sc_terminated))

    async def test_terminate_sim_controllers_no_response(self):
        self.rungov.experiment = MagicMock()
        self.rungov.major_domo_client = MagicMock()
        self.rungov.major_domo_client.send = AsyncMock(return_value=None)
        proc = MagicMock()
        proc.terminate = MagicMock()

        self.rungov.sim_controllers["sim-1"] = proc
        sc_terminated = await self.rgs._terminate_sim_controllers()

        proc.terminate.assert_called_once()
        self.assertEqual(1, len(sc_terminated))

    def test_prepare_reply(self):
        self.assertEqual(0, len(self.rungov.next_reply))

        self.rgs._prepare_reply(list())

        self.assertEqual(1, len(self.rungov.next_reply))
        self.assertIsInstance(
            self.rungov.next_reply[0], ExperimentShutdownResponse
        )


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import AsyncMock, MagicMock

from palaestrai.core.protocol import (
    SimulationStartRequest,
    SimulationStartResponse,
)
from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSErrorHandlingStarting,
    RGSStartingRun,
    RGSTransceiving,
)
from palaestrai.util.exception import InvalidResponseError


class TestStartingRun(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSStartingRun(self.rungov)
        self.rungov.state = self.rgs

    async def test_run(self):
        self.rgs._start_processes = MagicMock()
        self.rgs._send_start_request = AsyncMock()
        self.rgs._check_reply = MagicMock()

        await self.rgs.run()

        self.rgs._start_processes.assert_called_once()
        self.rgs._send_start_request.assert_called_once()
        self.rgs._check_reply.assert_called_once()

    def test_next_state(self):

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSTransceiving)

    def test_next_state_with_errors(self):
        self.rgs.add_error(ValueError())

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSErrorHandlingStarting)

    def test_start_processes(self):
        sim = MagicMock()
        sim.start = MagicMock()
        ac = MagicMock()
        ac.start = MagicMock()
        ec = MagicMock()
        ec.start = MagicMock()
        self.rungov.sim_controllers["sim-1"] = sim
        self.rungov.env_conductors["ec-1"] = ec
        self.rungov.agent_conductors["ac-1"] = ac

        self.rgs._start_processes()

        for proc in [sim, ec, ac]:
            proc.start.assert_called_once()

    async def test_send_start_request(self):
        sim = MagicMock()
        sim.start = MagicMock()
        self.rungov.sim_controllers["sim-1"] = sim
        rsp = SimulationStartResponse()
        self.rungov.major_domo_client = AsyncMock()
        self.rungov.major_domo_client.send = AsyncMock(return_value=rsp)
        logger = f"{RunGovernor.__module__}".rsplit(".", 1)[0]
        with self.assertLogs(logger, level="DEBUG") as cm:
            await self.rgs._send_start_request()

        self.assertIn("requesting", cm.output[0])
        self.assertIn("received", cm.output[1])

    async def test_send_start_request_with_error(self):
        sim = MagicMock()
        sim.start = MagicMock()
        self.rungov.sim_controllers["sim-1"] = sim
        rsp = SimulationStartRequest(None, None, None)
        self.rungov.major_domo_client = AsyncMock()
        self.rungov.major_domo_client.send = AsyncMock(return_value=rsp)
        logger = f"{RunGovernor.__module__}".rsplit(".", 1)[0]
        with self.assertLogs(logger, level="DEBUG") as cm:
            await self.rgs._send_start_request()

        self.assertIn("requesting", cm.output[0])
        self.assertEqual(len(cm.output), 1)
        self.assertEqual(len(self.rungov.errors), 1)
        self.assertIsInstance(self.rungov.errors[0][0], InvalidResponseError)


if __name__ == "__main__":
    unittest.main()

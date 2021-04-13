import unittest
from unittest.mock import MagicMock

from palaestrai.core.protocol import (
    SimulationControllerTerminationRequest,
    SimulationControllerTerminationResponse,
)
from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSHandlingSimControllerTermination,
    RGSStoppingSimulation,
    RGSTransceiving,
)


class TestHandlingSimControllerTermination(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSHandlingSimControllerTermination(self.rungov)
        self.rungov.state = self.rgs
        self.req = SimulationControllerTerminationRequest(
            None, None, None, None, None, None
        )

    async def test_run(self):
        self.rungov.last_request.append(self.req)
        self.rgs._handle_termination_request = MagicMock(return_value=False)
        self.rgs._prepare_reply = MagicMock()

        await self.rgs.run()

        self.rgs._handle_termination_request.assert_called_with(self.req)
        self.rgs._prepare_reply.assert_called_with(self.req, False)

    def test_next_state(self):
        self.rungov.next_reply.append(
            SimulationControllerTerminationResponse(
                sender_run_governor_id=None,
                receiver_simulation_controller_id=None,
                experiment_run_id=None,
                complete_shutdown=False,
            )
        )
        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSTransceiving)

    def test_next_state_complete_shutdown(self):
        self.rungov.next_reply.append(
            SimulationControllerTerminationResponse(
                sender_run_governor_id=None,
                receiver_simulation_controller_id=None,
                experiment_run_id=None,
                complete_shutdown=True,
            )
        )
        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStoppingSimulation)

    def test_handle_termination_request(self):
        self.rungov.sim_controllers["sim-1"] = MagicMock()
        self.req.sender_simulation_controller_id = "sim-1"
        self.rungov.termination_condition = MagicMock()
        self.rungov.termination_condition.check_termination = MagicMock(
            return_value=True
        )

        self.rgs._handle_termination_request(self.req)

        self.rungov.termination_condition.check_termination.assert_called_with(
            self.req, dict()
        )

    def test_prepare_reply(self):

        self.req.sender_simulation_controller_id = "sim-1"

        self.rgs._prepare_reply(self.req, False)

        self.assertIsInstance(
            self.rungov.next_reply[0], SimulationControllerTerminationResponse
        )

        self.assertEqual("sim-1", self.rungov.next_reply[0].receiver)


if __name__ == "__main__":
    unittest.main()

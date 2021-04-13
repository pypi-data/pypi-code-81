import unittest
from unittest.mock import AsyncMock, MagicMock

from palaestrai.core.protocol import (
    ExperimentStartRequest,
    ExperimentStartResponse,
)
from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSErrorHandlingStarting,
    RGSStarting,
    RGSStartingSimControllers,
)
from palaestrai.util.exception import ExperimentAlreadyRunningError


class TestStarting(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSStarting(self.rungov)
        self.rungov.state = self.rgs

    async def test_run(self):
        self.rgs._is_experiment_running = MagicMock(return_value=False)
        self.rgs._experiment_start = AsyncMock()
        request = ExperimentStartRequest(None, None)
        self.rungov.last_request.append(request)

        await self.rgs.run()

        self.rgs._is_experiment_running.assert_called_with(request)
        self.rgs._experiment_start.assert_called_with(request)

    async def test_run_experiment_already_running(self):
        self.rgs._is_experiment_running = MagicMock(return_value=True)
        self.rgs._experiment_start = AsyncMock()
        request = ExperimentStartRequest(None, None)
        self.rungov.last_request.append(request)

        await self.rgs.run()

        self.rgs._is_experiment_running.assert_called_with(request)
        self.rgs._experiment_start.assert_not_called()

    def test_next_state(self):

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStartingSimControllers)

    def test_next_state_with_errors(self):
        self.rgs.add_error(ValueError())

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSErrorHandlingStarting)

    def test_experiment_is_not_running(self):
        req = ExperimentStartRequest(None, "run-1")
        self.rungov.experiment = None

        res = self.rgs._is_experiment_running(req)

        self.assertFalse(res)
        self.assertEqual(0, len(self.rungov.errors))

    def test_experiment_is_running(self):
        req = ExperimentStartRequest(None, "run-1")
        self.rungov.experiment = 1

        res = self.rgs._is_experiment_running(req)

        self.assertTrue(res)
        self.assertEqual(1, len(self.rungov.errors))
        self.assertIsInstance(
            self.rungov.errors[0][0], ExperimentAlreadyRunningError
        )

    async def test_experiment_start(self):
        exp = MagicMock()
        req = ExperimentStartRequest(exp, "run-1")

        await self.rgs._experiment_start(req)

        self.assertEqual(1, len(self.rungov.next_reply))
        self.assertIsInstance(
            self.rungov.next_reply[0], ExperimentStartResponse
        )

    async def test_experiment_start_with_error(self):
        exp = MagicMock()
        exp.setup = MagicMock(side_effect=[])
        req = ExperimentStartRequest(exp, "run-1")

        await self.rgs._experiment_start(req)

        exp.setup.assert_called_once()
        self.assertEqual(1, len(self.rungov.errors))
        self.assertEqual(1, len(self.rungov.next_reply))
        self.assertIsInstance(
            self.rungov.next_reply[0], ExperimentStartResponse
        )
        self.assertFalse(self.rungov.next_reply[0].successful)


if __name__ == "__main__":
    unittest.main()

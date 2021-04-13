import unittest
from asyncio import Future
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch

from palaestrai.core.protocol import (
    ExperimentShutdownRequest,
    ExperimentStartRequest,
    SimulationControllerTerminationRequest,
)
from palaestrai.experiment import RunGovernor
from palaestrai.experiment.rungovernor_states import (
    RGSErrorHandlingTransceiving,
    RGSHandlingSimControllerTermination,
    RGSStarting,
    RGSStoppingSimulation,
    RGSTransceiving,
)
from palaestrai.util.exception import (
    DeadChildrenRisingAsZombiesError,
    InvalidRequestError,
    RequestIsNoneError,
    SignalInterruptError,
    TasksNotFinishedError,
)


class TestTransceiving(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.rungov = RunGovernor(None, None)
        self.rgs = RGSTransceiving(self.rungov)
        self.rungov.state = self.rgs

    async def test_run_success(self):
        self.rgs._create_transceive_task = MagicMock()
        self.rgs._wait_for_tasks = AsyncMock(return_value=(list(), list()))
        self.rgs._tasks_are_done = MagicMock(return_value=True)
        self.rgs._childrens_are_dead = MagicMock(return_value=False)
        self.rgs._get_request = AsyncMock()

        await self.rgs.run()

        self.rgs._create_transceive_task.assert_called_once()
        self.rgs._wait_for_tasks.assert_called_once()
        self.rgs._tasks_are_done.assert_called_once()
        self.rgs._childrens_are_dead.assert_called_once()
        self.rgs._get_request.assert_called_once()

    async def test_run_tasks_not_done(self):
        self.rgs._create_transceive_task = MagicMock()
        self.rgs._wait_for_tasks = AsyncMock(return_value=(list(), list()))
        self.rgs._tasks_are_done = MagicMock(return_value=False)
        self.rgs._childrens_are_dead = MagicMock(return_value=False)
        self.rgs._get_request = AsyncMock()

        await self.rgs.run()

        self.rgs._create_transceive_task.assert_called_once()
        self.rgs._wait_for_tasks.assert_called_once()
        self.rgs._tasks_are_done.assert_called_once()
        self.rgs._childrens_are_dead.assert_not_called()
        self.rgs._get_request.assert_not_called()

    async def test_run_childrens_dead(self):
        self.rgs._create_transceive_task = MagicMock()
        self.rgs._wait_for_tasks = AsyncMock(return_value=(list(), list()))
        self.rgs._tasks_are_done = MagicMock(return_value=True)
        self.rgs._childrens_are_dead = MagicMock(return_value=True)
        self.rgs._get_request = AsyncMock()

        await self.rgs.run()

        self.rgs._create_transceive_task.assert_called_once()
        self.rgs._wait_for_tasks.assert_called_once()
        self.rgs._tasks_are_done.assert_called_once()
        self.rgs._childrens_are_dead.assert_called_once()
        self.rgs._get_request.assert_not_called()

    def test_next_state_experiment_start(self):

        self.rungov.last_request.append(ExperimentStartRequest(None, None))

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStarting)

    def test_next_state_sim_controller_termination(self):

        self.rungov.last_request.append(
            SimulationControllerTerminationRequest(
                None, None, None, None, None, None
            )
        )

        self.rgs.next_state()

        self.assertIsInstance(
            self.rungov.state, RGSHandlingSimControllerTermination
        )

    def test_next_state_experiment_shutdown(self):

        self.rungov.last_request.append(ExperimentShutdownRequest(None))

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSStoppingSimulation)

    def test_next_state_invalid_request(self):

        self.rungov.last_request.append(0)

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSErrorHandlingTransceiving)
        self.assertEqual(len(self.rungov.errors), 1)
        self.assertIsInstance(self.rungov.errors[0][0], InvalidRequestError)

    def test_next_state_error_occured(self):
        self.rungov.last_request.append(ExperimentStartRequest(None, None))
        self.rgs.add_error(DeadChildrenRisingAsZombiesError())

        self.rgs.next_state()

        self.assertIsInstance(self.rungov.state, RGSErrorHandlingTransceiving)
        self.assertEqual(len(self.rungov.errors), 1)
        self.assertIsInstance(
            self.rungov.errors[0][0], DeadChildrenRisingAsZombiesError
        )

    @patch(f"{RGSTransceiving.__module__}.asyncio")
    def test_create_transceive_task(self, mock_asyncio):
        self.rungov.major_domo_worker = MagicMock()
        self.rungov.major_domo_worker.transceive = MagicMock()
        mock_asyncio.create_task = MagicMock()
        self.rungov.next_reply.append(None)
        self.rungov.transceive_task = None

        self.rgs._create_transceive_task()

        self.assertIsNotNone(self.rungov.transceive_task)
        self.rungov.major_domo_worker.transceive.assert_called_with(None)
        mock_asyncio.create_task.assert_called_once()

    @patch(f"{RGSTransceiving.__module__}.asyncio")
    async def test_wait_for_tasks(self, mock_asyncio):
        sim = MagicMock()
        type(sim).name = PropertyMock(return_value="sim-1")
        sim.is_alive = MagicMock(return_value=True)
        self.rungov.sim_controllers["sim-1"] = sim

        mock_asyncio.wait = AsyncMock(return_value=(list(), 0))
        self.rgs._join_process = MagicMock()

        await self.rgs._wait_for_tasks()

        sim.is_alive.assert_called_once()
        mock_asyncio.wait.assert_called_once()
        self.rgs._join_process.assert_called_once()

    def test_tasks_are_done(self):
        res = self.rgs._tasks_are_done(list("I am a task"))

        self.assertTrue(res)
        self.assertEqual(0, len(self.rungov.errors))

    def test_tasks_are_not_done(self):
        res = self.rgs._tasks_are_done(list())

        self.assertFalse(res)
        self.assertEqual(1, len(self.rungov.errors))
        self.assertIsInstance(self.rungov.errors[0][0], TasksNotFinishedError)

    def test_signal_task_is_done(self):
        self.rungov.signal_monitor_task = "signal"
        res = self.rgs._tasks_are_done(["signal"])

        self.assertFalse(res)
        self.assertEqual(1, len(self.rungov.errors))
        self.assertIsInstance(self.rungov.errors[0][0], SignalInterruptError)

    def test_childrens_are_not_dead(self):
        sim = MagicMock()
        sim.is_alive = MagicMock(return_value=True)

        res = self.rgs._childrens_are_dead([sim])

        self.assertFalse(res)
        self.assertEqual(0, len(self.rungov.errors))

    def test_childrens_are_dead(self):
        sim = MagicMock()
        sim.is_alive = MagicMock(return_value=False)

        res = self.rgs._childrens_are_dead([sim])

        self.assertTrue(res)
        self.assertEqual(1, len(self.rungov.errors))
        self.assertIsInstance(
            self.rungov.errors[0][0], DeadChildrenRisingAsZombiesError
        )

    async def test_get_request(self):

        self.rungov.transceive_task = MagicMock(return_value=Future())
        self.rungov.transceive_task.result = MagicMock()

        res = await self.rgs._get_request([self.rungov.transceive_task])

        self.assertTrue(res)

        self.assertEqual(0, len(self.rungov.errors))
        self.assertIsNone(self.rungov.transceive_task)
        self.assertEqual(1, len(self.rungov.last_request))

    async def test_get_request_is_none(self):

        self.rungov.transceive_task = MagicMock(return_value=Future())
        self.rungov.transceive_task.result = MagicMock(return_value=None)

        res = await self.rgs._get_request([self.rungov.transceive_task])

        self.assertFalse(res)

        self.assertEqual(1, len(self.rungov.errors))
        self.assertIsInstance(self.rungov.errors[0][0], RequestIsNoneError)
        self.assertIsNone(self.rungov.transceive_task)
        self.assertEqual(1, len(self.rungov.last_request))

    @patch(f"{RGSTransceiving.__module__}.asyncio")
    async def test_join_process(self, mock_asyncio):
        proc = MagicMock()
        proc.name.return_value = "proc-1"
        proc.is_alive = MagicMock(return_value=True)
        type(proc).exitcode = PropertyMock(side_effect=[None, 1, 1])
        mock_asyncio.sleep = AsyncMock()

        await self.rgs._join_process(proc)

        mock_asyncio.sleep.assert_called_once()
        self.assertEqual(2, proc.is_alive.call_count)


if __name__ == "__main__":
    unittest.main()

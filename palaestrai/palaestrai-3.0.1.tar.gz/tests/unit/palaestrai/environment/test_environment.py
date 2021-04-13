import unittest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from palaestrai.core.protocol import (
    EnvironmentShutdownRequest,
    EnvironmentShutdownResponse,
    EnvironmentStartRequest,
    EnvironmentStartResponse,
    EnvironmentUpdateRequest,
    EnvironmentUpdateResponse,
)
from palaestrai.environment.dummy_environment import DummyEnvironment


class TestEnvironment(unittest.IsolatedAsyncioTestCase):
    def setUp(self):

        self.env = DummyEnvironment("test_conn", uuid4(), dict())
        self.setup_req = EnvironmentStartRequest(
            environment_id="0",
            run_id="1",
        )
        self.update_req = EnvironmentUpdateRequest(
            sender_simulation_controller="2",
            receiver_environment="0",
            experiment_run_id="1",
            environment_conductor_id="3",
            actuators=list(),
        )
        self.shutdown_req = EnvironmentShutdownRequest(
            experiment_run_id="1", environment_id="0"
        )

    def test_handle_setup(self):
        self.env.start_environment = MagicMock(return_value=(list(), list()))
        rsp = self.env._handle_setup(self.setup_req)

        self.env.start_environment.assert_called_once()
        self.assertIsInstance(rsp, EnvironmentStartResponse)

    def test_handle_update(self):
        self.env.update = MagicMock(return_value=(list(), list(), False))
        rsp = self.env._handle_update(self.update_req)

        self.env.update.assert_called_once()
        self.assertIsInstance(rsp, EnvironmentUpdateResponse)

    def test_handle_shutdown(self):
        self.env.shutdown = MagicMock(return_value=True)
        rsp = self.env._handle_shutdown(self.shutdown_req)

        self.env.shutdown.assert_called_once()
        self.assertIsInstance(rsp, EnvironmentShutdownResponse)

    async def test_run(self):
        setup_msg = self.setup_req
        update_msg = self.update_req
        shutdown_msg = self.shutdown_req
        self.env.worker.transceive = AsyncMock()
        self.env.worker.transceive.side_effect = [
            setup_msg,
            update_msg,
            update_msg,
            update_msg,
            shutdown_msg,
            shutdown_msg,  # Final message, will not be handled
        ]
        self.env.start_environment = MagicMock(return_value=(list(), list()))
        self.env.update = MagicMock(return_value=(list(), list(), False))
        await self.env.run()

        self.assertEqual(self.env.worker.transceive.call_count, 6)
        self.env.start_environment.assert_called_once()
        self.assertEqual(self.env.update.call_count, 3)


if __name__ == "__main__":
    unittest.main()

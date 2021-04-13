import unittest
from unittest.mock import patch, AsyncMock, call
from uuid import uuid4

from palaestrai.environment.environment_conductor import EnvironmentConductor
from palaestrai.core.protocol import (
    EnvironmentSetupRequest,
    ShutdownRequest,
    EnvironmentSetupResponse,
    ShutdownResponse,
)
from palaestrai.environment.environment_conductor import EnvironmentConductor


class TestEnvironmentConductor(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.mockaio = patch(
            "palaestrai.environment.environment_conductor.aiomultiprocess."
            "Process",
            spec=True,
        ).start()

        self.addCleanup(patch.stopall)

        self.env_params = {"params": dict(), "broker_connection": "test_conn"}

        self.env_cond = EnvironmentConductor(
            "palaestrai.environment.dummy_environment:DummyEnvironment",
            self.env_params,
            "test_conn",
            123,
            uuid4(),
        )

    def test_one_process_per_environment(self):
        self.env_cond.init_env(uuid4())
        self.env_cond.init_env(uuid4())
        self.assertEqual(self.mockaio.call_count, 2)
        self.assertEqual(
            len(self.env_cond._tasks), 2, "not correctly executed"
        )

    async def test_run_shutdown(self):
        msg_shutdown = ShutdownRequest(42)
        self.env_cond.worker.transceive = AsyncMock(return_value=msg_shutdown)

        await self.env_cond.run()
        self.env_cond.worker.transceive.assert_awaited()

    async def test_setup_conductor(self):
        msg_setup = EnvironmentSetupRequest(
            environment_id="0815",
            experiment_run_id="run away",
            receiver_environment_conductor_id="the boss",
            sender_simulation_controller_id="the servant",
        )

        msg_setup_response = EnvironmentSetupResponse(
            sender_environment_conductor=self.env_cond.uid,
            receiver_simulation_controller="the servant",
            environment_id="0815",
            experiment_run_id="run away",
            environment_type=self.env_cond.env_type,
            environment_parameters=self.env_cond.env_params.get(
                "params", dict()
            ),
        )

        msg_shutdown = ShutdownRequest(42)
        msg_shutdown_response = ShutdownResponse(42)

        calls = (
            call(None),
            call(msg_setup_response),
            call(msg_setup_response),
            call(msg_shutdown_response, skip_recv=True),
        )

        self.env_cond.worker.transceive = AsyncMock(
            side_effect=[msg_setup, msg_setup, msg_shutdown, None]
        )

        await self.env_cond.run()
        self.assertEqual(len(self.env_cond._tasks), 2)
        self.env_cond._worker.transceive.assert_has_awaits(calls)


if __name__ == "__main__":
    unittest.main()

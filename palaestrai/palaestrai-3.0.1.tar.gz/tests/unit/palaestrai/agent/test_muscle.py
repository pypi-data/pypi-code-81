import unittest
from unittest.mock import MagicMock, PropertyMock, AsyncMock, patch
from uuid import uuid4

from palaestrai.agent.dummy_muscle import DummyMuscle
from palaestrai.core.serialisation import serialize
from palaestrai.agent import ActuatorInformation, SensorInformation
from palaestrai.types import Discrete
from palaestrai.core.protocol import (
    AgentUpdateRequest,
    AgentUpdateResponse,
    MuscleUpdateRequest,
    MuscleUpdateResponse,
    AgentShutdownRequest,
    AgentShutdownResponse,
)


class TestMuscle(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:

        self.uid = str(uuid4())
        agent_id = "agent"
        experiment_run_id = "exp_42"

        patch(
            "palaestrai.agent.dummy_muscle.Muscle.dealer_socket",
            new_callable=PropertyMock,
        ).start()
        patch("palaestrai.agent.dummy_muscle.DummyMuscle.update").start()
        patch(
            "palaestrai.agent.dummy_muscle.DummyMuscle.propose_actions",
            return_value=[ActuatorInformation(0.237, Discrete(1), 0)],
        ).start()
        patch("palaestrai.agent.muscle.signal", spec=True).start()
        self.addCleanup(patch.stopall)

        self.test_muscle = DummyMuscle(
            broker_connection="broker", brain_connection="brain", uid=self.uid
        )

        self.msg_agent_update_req = AgentUpdateRequest(
            sender_simulation_controller_id="0815",
            receiver_agent_id=agent_id,
            experiment_run_id=experiment_run_id,
            actuators=[ActuatorInformation(0, Discrete(1), 0)],
            sensors=[SensorInformation(1, Discrete(1), 0)],
            reward=[0.897],
            is_terminal=False,
        )

        self.msg_muscle_update_res = MuscleUpdateResponse(
            is_updated=True, updates=[0, 0, 0]
        )

        self.msg_agent_shutdown_req = AgentShutdownRequest(
            run_id=experiment_run_id,
            agent_id=agent_id,
            complete_shutdown=True,
        )

    def test_send_to_brain(self):
        muscle_update_req = MuscleUpdateRequest(
            sender_muscle_id=self.uid,
            receiver_brain_id=None,
            agent_id="agent-1",
            experiment_run_id="run-1",
            sensor_readings=[SensorInformation(1, Discrete(1), 0)],
            last_actions=None,
            reward=0.897,
            is_terminal=False,
            shutdown=False,
        )

        self.test_muscle.dealer_socket.recv_multipart = MagicMock(
            return_value=[serialize(self.msg_muscle_update_res)]
        )
        response = self.test_muscle.send_to_brain(muscle_update_req)
        self.test_muscle.dealer_socket.send.assert_called_with(
            serialize(muscle_update_req), flags=0
        )
        self.assertEqual(response.is_updated, True)

    async def test_run(self):

        self.test_muscle.worker.transceive = AsyncMock(
            side_effect=[
                self.msg_agent_update_req,
                self.msg_agent_shutdown_req,
                None,
            ]
        )
        self.test_muscle._handle_agent_update = MagicMock(return_value=None)
        self.test_muscle._handle_agent_shutdown = MagicMock(return_value=None)

        await self.test_muscle.run()

        self.assertEqual(3, self.test_muscle.worker.transceive.call_count)
        self.test_muscle._handle_agent_update.assert_called_once()
        self.test_muscle._handle_agent_shutdown.assert_called_once()
        self.test_muscle.worker.transceive.assert_awaited()

    async def test_handle_agent_update(self):
        self.test_muscle.send_to_brain = MagicMock(
            return_value=self.msg_muscle_update_res
        )
        response = self.test_muscle._handle_agent_update(
            self.msg_agent_update_req
        )

        self.assertEqual("exp_42", self.test_muscle.run_id)
        self.assertIsInstance(response, AgentUpdateResponse)

    async def test_handle_agent_shutdown(self):
        self.test_muscle.send_to_brain = MagicMock(return_value=None)
        response = self.test_muscle._handle_agent_shutdown(
            self.msg_agent_shutdown_req
        )
        self.assertIsInstance(response, AgentShutdownResponse)


if __name__ == "__main__":
    unittest.main()

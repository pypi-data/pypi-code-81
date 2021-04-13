import unittest
from unittest.mock import MagicMock, patch

from palaestrai.agent.dummy_brain import DummyBrain
from palaestrai.agent.dummy_objective import DummyObjective

from palaestrai.agent.state import State
from palaestrai.core.protocol import MuscleUpdateRequest, MuscleShutdownRequest
from palaestrai.core.serialisation import serialize


class TestBrain(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.brain_params = {}
        self.muscle_update_req = MuscleUpdateRequest(
            sender_muscle_id="0",
            receiver_brain_id="1",
            experiment_run_id="2",
            agent_id="3",
            sensor_readings=list(),
            last_actions=list(),
            reward=0,
            is_terminal=False,
            shutdown=False,
        )
        self.muscle_shutdown_req = MuscleShutdownRequest(
            sender_muscle_id="0",
            experiment_run_id="2",
            agent_id="3",
        )
        self.brain = DummyBrain(
            "test-con", list(), list(), DummyObjective(), 123
        )

    def test_process(self):
        self.brain._state = State.RUNNING
        self.brain._connect = MagicMock()
        self.brain._router_socket = MagicMock()
        self.brain._router_socket.recv_multipart = MagicMock()
        update_msg = serialize(self.muscle_update_req)
        shutdown_msg = serialize(self.muscle_shutdown_req)
        self.brain._router_socket.recv_multipart.side_effect = [
            ["0", update_msg],
            ["0", shutdown_msg],
        ]
        self.brain._receive_updates()

        self.assertEqual(self.brain._worker_updates.qsize(), 2)
        self.assertFalse(self.brain._receive_updates())
        msg = self.brain._worker_updates.get()
        self.assertIsInstance(msg[0], MuscleUpdateRequest)
        self.assertEqual(msg[1], "0")

        # TODO: Change to MuscleShutdownRequest as soon as it is merged
        msg = self.brain._worker_updates.get()
        self.assertIsInstance(msg[0], MuscleShutdownRequest)
        self.assertEqual(msg[1], "0")

    @patch("palaestrai.agent.brain.Thread")
    async def test_run(self, mockthread):
        self.brain._state = State.RUNNING
        self.brain._send = MagicMock()
        self.brain.thinking = MagicMock(return_value=0)
        self.brain._worker_updates.put([self.muscle_update_req, "0"])
        self.brain._worker_updates.put([self.muscle_shutdown_req, "0"])

        await self.brain.run()

        mockthread.assert_called_once()
        self.brain.thinking.assert_called_once()
        self.assertEqual(self.brain._send.call_count, 2)
        self.assertNotEqual(self.brain.state, State.RUNNING)


if __name__ == "__main__":
    unittest.main()

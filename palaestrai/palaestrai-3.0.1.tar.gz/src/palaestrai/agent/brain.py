"""This module contains the abstract class :class:`Brain` that is used
to implement the thinking part of agents.

"""
from __future__ import annotations
import asyncio
import pickle
import queue
import signal
import time
import zlib
from abc import ABC, abstractmethod
from threading import Thread
from typing import TYPE_CHECKING


import zmq

from palaestrai.core.protocol import (
    MuscleUpdateRequest,
    MuscleUpdateResponse,
    MuscleShutdownRequest,
    MuscleShutdownResponse,
)
from . import LOG
from .state import State

if TYPE_CHECKING:
    from . import SensorInformation, ActuatorInformation


class Brain(ABC):
    """Baseclass for all brain implementation

    The brain is the central learning instance. It coordinates all
    muscles (if multiple muscles are available). The brain does all
    (deep) learning tasks and delivers a model to the muscles.

    The brain has one abstract method :meth:`.thinking` that has to be
    implemented.

    Parameters
    ----------
    muscle_connection : str
        The IP and port on which the brain should bind, so that the
        muscles can connect to the brain, e.g: 'tcp://127.0.0.1:1234'.
    sensors : list[SensorInformation]
        A *list* of available sensors, can be used to define, e.g., the
        input space of a neural network.
    actuators : list[ActuatorInformation]
        A *list* of available actuators, can be used to define, e.g.,
        the output space of a neural network.
    max_buffer : int
        Size of the queue buffer.

    """

    def __init__(
        self,
        muscle_connection: str,
        sensors: list["SensorInformation"],
        actuators: list["ActuatorInformation"],
        objective: object,
        seed: int,
        max_buffer: int = 0,
    ):
        self._state = State.PRISTINE
        self.seed = seed
        self.muscle_connection = muscle_connection
        self._worker_updates: queue.Queue = queue.Queue(max_buffer)
        self.sensors = sensors
        self.actuators = actuators
        self.objective = objective
        self._ctx = None
        self._router_socket = None

    @property
    def state(self) -> State:
        return self._state

    @property
    def context(self):
        if self._ctx is None:
            self._ctx = zmq.Context()
        return self._ctx

    def _handle_sigintterm(self, signum, frame):
        self._state = State.CANCELLED
        LOG.warn(
            "Brain(id=0x%x) interrupted by signal %s in frame %s",
            id(self),
            signum,
            frame,
        )

    def _receive_updates(self):
        """Receives updates from workers and stores them in the queue."""
        self._connect()
        while self.state == State.RUNNING:
            try:
                z = self._router_socket.recv_multipart(flags=zmq.NOBLOCK)
            except zmq.ZMQError:
                time.sleep(0.05)
                continue
            p = zlib.decompress(z[1])
            msg = pickle.loads(p)
            if msg is not None:
                self._worker_updates.put([msg, z[0]])
            if isinstance(msg, MuscleShutdownRequest):
                self._state = State.STOPPING
        LOG.debug("Brain(id=0x%x) has shut down", id(self))

    def _connect(self):
        """connect the core channels to the specified uris"""
        self._router_socket = self.context.socket(zmq.ROUTER)
        self._router_socket.bind(self.muscle_connection)
        LOG.debug(
            "Brain(id=0x%x) bound to %s", id(self), self.muscle_connection
        )

    def _send(self, message, header, flags=0, protocol=-1):
        """Send a message to a muscle.

        Parameters
        ----------
        message : MuscleUpdateResponse
            The message that should be send as response.
        header : str or bytes
            The ID of the receiving muscle.
        flags : int, optional
            ZeroMQ-Flags which should be used when sending.
        protocol : int, optional
            Protocol used by pickle.dumps

        """
        p = pickle.dumps(message, protocol)
        z = zlib.compress(p)
        self._router_socket.send_multipart([bytes(header), z], flags=flags)

    async def run(self):
        """Start the brain main loop.

        This method starts the brain, it begins to listen for messages
        and as soon as messages are arriving, it processes those
        messages by calling the thinking methode. This will return a
        Muscleupdateresponse, which is sent back to the muscle.
        """
        self._state = State.RUNNING
        signal.signal(signal.SIGINT, self._handle_sigintterm)
        signal.signal(signal.SIGTERM, self._handle_sigintterm)
        receiver_thread = Thread(target=self._receive_updates)
        receiver_thread.start()

        while self.state == State.RUNNING or not self._worker_updates.empty():
            try:
                msg = self._worker_updates.get(timeout=1)
            except TimeoutError:
                continue
            except queue.Empty:
                await asyncio.sleep(0.05)
                continue
            msg, header = msg[0], msg[1]
            if isinstance(msg, MuscleUpdateRequest):
                self.objective.reward = msg.reward
                response = self.thinking(
                    header,
                    msg.sensor_readings,
                    msg.last_actions,
                    self.objective.internal_reward(),
                    msg.is_terminal,
                )
            elif isinstance(msg, MuscleShutdownRequest):
                response = MuscleShutdownResponse()
                self._state = State.STOPPING
            else:
                LOG.error(
                    "Brain(id=0x%x) "
                    "has received a message of type %s, but cannot handle it; "
                    "ignoring",
                    id(self),
                    type(msg),
                )
                continue

            self._send(response, header)

        LOG.debug(
            "Brain(id=0x%x) runner has ended, joining receiver thread",
            id(self),
        )
        receiver_thread.join()
        if self.state == State.STOPPING:
            self._state = State.FINISHED
        LOG.debug("Brain(id=0x%x) completed run, shut down", id(self))

    @abstractmethod
    def thinking(
        self, muscle_id, readings, actions, reward, done
    ) -> MuscleUpdateResponse:
        """Think about a response using the provided information.

        The :meth:`.thinking` method is the place for the
        implementation of the agent's/brain's logic. The brain can
        use the current sensor readings, review the actions of the
        previous thinking and consider the reward (provided by the
        objective).

        Usually, this is the place where machine learning happens,
        but other solutions are possible as well (like a set of rules
        or even random based results).

        Parameters
        -------
        muscle_id : UID
            This is the ID of the muscle which requested the update
        readings : list[sensor_information]
            A list containing the new sensor readings
        actions : list[actuator_information]
            A list containing the actions of the last iteration
        reward : list[floats] or list[int] or float
            A float of the environment reward, a list of floats if
            multiple environments are used in parallel
        done : bool
            A boolean which signals if the simulation run has
            terminated

        Returns
        -------
        MuscleUpdateResponse
        """
        pass

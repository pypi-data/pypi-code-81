"""This module contains the abstract class :class:`Muscle` that
is used to implement the acting part of an agent.

"""
import signal
import uuid
from abc import ABC, abstractmethod

import zmq
import zmq.asyncio

from palaestrai.core import MajorDomoWorker
from palaestrai.core.protocol import (
    AgentUpdateRequest,
    AgentUpdateResponse,
    MuscleUpdateRequest,
    MuscleShutdownRequest,
    AgentShutdownRequest,
    AgentShutdownResponse,
)
from palaestrai.core.serialisation import deserialize, serialize
from . import LOG


class Muscle(ABC):
    """
    Generates the actuator_information for each provided actuator while
    maintaining communication with the module `brain`.

    Parameters
    ----------
    broker_connection : str
        the URI which is used to connect to the simulation broker. It is
        used to communicate with the simulation controller.
    brain_connection : str
        a connection for communication with the brain.
    uid : uuid4
        a universal id, that is either provided or assigned here.

    """

    def __init__(self, broker_connection, brain_connection, uid):
        self.broker_connection = broker_connection
        self.brain_connection = brain_connection
        self._ctx = None
        self._sync_ctx = None
        self._dealer_socket = None
        self.uid = uid or uuid.uuid4()
        self._worker = None
        self.run_id = None
        self._last_actions = None

    @property
    def context(self):
        """Return the asynchronous zmq context.

        The context will be created if necessary.
        """
        if self._ctx is None:
            self._ctx = zmq.asyncio.Context()
        return self._ctx

    @property
    def sync_context(self):
        """Return the synchronous zmq context.

        The context will be created if necessary.
        """

        if self._sync_ctx is None:
            self._sync_ctx = zmq.Context()
        return self._sync_ctx

    @property
    def worker(self):
        """Return the major domo worker.

        The worker will be created if necessary.
        """

        if self._worker is None:
            self._worker = MajorDomoWorker(self.broker_connection, self.uid)
        return self._worker

    @property
    def dealer_socket(self):
        """Return the zmq dealer socket.

        The socket will be created if necessary.
        """

        if self._dealer_socket is None:
            self._dealer_socket = self.sync_context.socket(zmq.DEALER)
            self._dealer_socket.identity = str(self.uid).encode("ascii")
            self._dealer_socket.connect(self.brain_connection)
        return self._dealer_socket

    def _handle_sigintterm(self, signum, frame):
        LOG.info(
            "Muscle(id=0x%x, uid=%s) " "interrupted by signal %s in frame %s",
            id(self),
            self.uid,
            signum,
            frame,
        )
        raise SystemExit()

    def send_to_brain(self, message, flags=0):
        """
        This method is used for communication with the brain. It is
        needed to update the muscle.

        Parameters
        ----------
        message : MuscleUpdateRequest
            The message to be sent to the brain
        flags : int, optional
            Flags for the socket's send method.

        Returns
        -------
        MuscleUpdateResponse
            Response received from the brain.

        """
        z = serialize(message)
        self.dealer_socket.send(z, flags=flags)
        z = self.dealer_socket.recv_multipart(flags=flags)
        response = deserialize(z)
        return response

    async def run(self):
        """Start the main loop of the muscle.

        This method is handling incoming messages and calls the
        corresponding method.

        If an ´AgentUpdateRequest´ is received, it's processed to a
        ´MuscleUpdateRequest´, which triggers a reaction from the
        ´brain´ module (i.e. ´MuscleUpdateResponse´) and finally an
        ´AgentUpdateResponse´ with the action proposals is sent.

        If an ´AgentShutdownRequest´ is received it's processed to a
        ´MuscleUpdateRequest´ and an ´AgentShutdownResponse´ to initiate
        termination of the agent.

        """
        signal.signal(signal.SIGINT, self._handle_sigintterm)
        signal.signal(signal.SIGTERM, self._handle_sigintterm)

        terminal = False
        reply = None
        while not terminal:
            request = await self.worker.transceive(reply)

            if request is None:
                raise TypeError
            elif isinstance(request, AgentUpdateRequest):
                reply = self._handle_agent_update(request)
            elif isinstance(request, AgentShutdownRequest):
                reply = self._handle_agent_shutdown(request)
                terminal = True

        await self.worker.transceive(reply, skip_recv=True)

    def _handle_agent_update(
        self, request: AgentUpdateRequest
    ) -> AgentUpdateResponse:
        """Handle an agent update.

        Every update request to the muscle is forwarded to the brain.
        The brain answers with information that the muscle can use to
        update itself.

        Finally, an update response is prepared.

        Parameters
        ----------
        request : AgentUpdateRequest
            The update request from the simulation controller.
            Contains, among other information, the current sensor
            readings and the reward of the previous actions.

        Returns
        -------
        AgentUpdateResponse
            The update response with the agent's actions.

        """
        LOG.debug(
            "Muscle(id=0x%x, uid=%s) received %s",
            id(self),
            self.uid,
            request,
        )
        self.run_id = request.experiment_run_id
        msg = MuscleUpdateRequest(
            sender_muscle_id=self.uid,
            receiver_brain_id="",
            agent_id=request.receiver_agent_id,
            experiment_run_id=request.experiment_run_id,
            sensor_readings=request.sensors,
            last_actions=self._last_actions,
            reward=request.reward,
            is_terminal=request.is_terminal,
            shutdown=False,
        )
        LOG.info(
            "Muscle(id=0x%x, uid=%s) sending %s to brain.",
            id(self),
            self.uid,
            msg,
        )
        response = self.send_to_brain(msg)
        LOG.debug(
            "Muscle(id=0x%x, uid=%s) received %s from brain",
            id(self),
            self.uid,
            response,
        )
        if response.is_updated:
            self.update(response.updates)

        self._last_actions = self.propose_actions(
            request.sensors, request.actuators, False
        )
        return AgentUpdateResponse(
            sender_agent_id=self.uid,
            receiver_simulation_controller_id=request.sender,
            experiment_run_id=request.experiment_run_id,
            actuator_information=self._last_actions,
            sensor_information=request.sensors,
            rewards=request.reward,
        )

    def _handle_agent_shutdown(
        self, request: AgentShutdownRequest
    ) -> AgentShutdownResponse:
        """Handle agent shutdown.

        The muscle sends a final update request to the brain. The
        response from the brain is ignored.
        Finally, a shutdown response is preprared

        Parameters
        ----------
        request : AgentShutdownRequest
            The shutdown request from the simulation controller. This
            message has no further information that need to be
            processed.

        Returns
        -------
        AgentShutdownResponse
            The shutdown response that confirms the shutdown of the
            muscle.

        """
        LOG.debug(
            "Muscle %s(id=0x%x, uid=%s) received AgentShutdownRequest",
            self.__class__,
            id(self),
            self.uid,
        )
        msg = MuscleShutdownRequest(
            sender_muscle_id=self.uid,
            agent_id=request.agent_id,
            experiment_run_id=request.experiment_run_id,
        )
        _ = self.send_to_brain(msg)

        return AgentShutdownResponse(request.experiment_run_id, self.uid, True)

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def propose_actions(
        self, sensors, actuators_available, is_terminal=False
    ) -> list:
        """Process new sensor information and produce actuator
        setpoints.

        This is the abstract method which needs to be implemented.
        It works together with a brain and must be tuned to it
        accordingly.

        This method takes a list of :class:sensor_information and has
        to return a list of actuators (this information is given by the
        actuators_available parameter). How the actuator setpoints are
        produced and how the sensor information are processed is up to
        the developer.

        Mainly it is used for reinforcement learning agents. In this
        case, the muscle has a "finished" model and uses it to generate
        the actuator_information. All deep learning tasks are done by
        the brain. The muscle uses the model exclusively and does not
        make any changes itself.

        Parameters
        ----------
        sensors : list[SensorInformation]
            List of new SensorInformation for all available sensors
        actuators_available : list[ActuatorInformation]
            List of all actuators for which a new setpoint is required.
        is_terminal : bool
            Indicator if the simulation run has terminated

        """
        pass

    @abstractmethod
    def update(self, update):
        """Update the muscle.

        This method is called if the brain sends an update. What is to
        be updated is up to the specific implementation. However, this
        method should update all necessary components.

        """
        pass

    @abstractmethod
    def __repr__(self):
        pass

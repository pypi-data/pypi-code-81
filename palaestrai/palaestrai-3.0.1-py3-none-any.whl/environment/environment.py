"""This module contains the abstract class :class:`Environment` that
is used to implement a new environment.

"""
import signal
from abc import ABC, abstractmethod
from typing import Tuple, List

from palaestrai.core import MajorDomoWorker
from palaestrai.core.protocol import (
    EnvironmentShutdownRequest,
    EnvironmentShutdownResponse,
    EnvironmentStartRequest,
    EnvironmentStartResponse,
    EnvironmentUpdateRequest,
    EnvironmentUpdateResponse,
)

from . import LOG
from ..agent import SensorInformation, ActuatorInformation


class Environment(ABC):
    """Abstract class for environment implementation

    This abstract calls provides all necessary functions needed
    to implement a new environment. The developer only has to
    implement the functions start_environment and update.

    Parameters
    ----------
    connection : str
        URI used to connect to the simulation broker
    uid : uuid4
        Unique identifier to identify an environment
    seed : int
        Seed for recreation
    params : dict
        Dictionary of additional needed parameters
    """

    def __init__(self, connection, uid, seed: int, params=None):
        self._ctx = None
        self.broker_connection = connection
        self.uid = uid
        self.seed = seed
        self._worker = None

        self.params = params
        self.sensors: list[SensorInformation] = []
        self.actuators: list[ActuatorInformation] = []

        self.is_terminal = False
        LOG.debug(
            "Environment %s(id=0x%x, uid=%s) created",
            self.__class__,
            id(self),
            self.uid,
        )

    @property
    def worker(self):
        """Return the major domo worker.

        The worker will be created if necessary.
        """

        if self._worker is None:
            self._worker = MajorDomoWorker(
                self.broker_connection,
                self.uid,
            )
        return self._worker

    def _handle_sigintterm(self, signum, frame):
        LOG.info(
            "%s(id=0x%x, uid=%s) " "interrpted by signal %s in frame %s",
            self.__class__,
            id(self),
            self.uid,
            signum,
            frame,
        )
        raise SystemExit()

    async def run(self):
        """Main function for message handling

        This is the main function of the environment. It receives
        and processes incoming messages and calls the requested functions
        it also returns the responses.
        """
        reply = None
        LOG.debug(
            "Environment %s(id=0x%x, uid=%s) commencing run",
            self.__class__,
            id(self),
            self.uid,
        )
        signal.signal(signal.SIGINT, self._handle_sigintterm)
        signal.signal(signal.SIGTERM, self._handle_sigintterm)
        while not self.is_terminal:
            try:
                request = await self.worker.transceive(reply)
            except SystemExit:
                LOG.critical(
                    "%s(id=0x%x, uid=%s) "
                    "interrupted in transceive by SIGINT/SIGTERM, "
                    "existing run loop",
                    self.__class__,
                    id(self),
                    self.uid,
                )
                break

            LOG.debug(
                "Environment %s(id=0x%x, uid=%s) received message: %s",
                self.__class__,
                id(self),
                self.uid,
                request,
            )
            if request is None:
                break
            elif isinstance(request, EnvironmentStartRequest):
                reply = self._handle_setup(request)
            elif isinstance(request, EnvironmentUpdateRequest):
                reply = self._handle_update(request)
            elif isinstance(request, EnvironmentShutdownRequest):
                reply = self._handle_shutdown(request)

        await self.worker.transceive(reply, skip_recv=True)

    def _handle_setup(
        self, request: EnvironmentStartRequest
    ) -> EnvironmentStartResponse:
        """Handle an environment start request.

        The :meth:`start_environment` is called that can be used by
        environments for setup purposes and that should provide the
        available sensors and actuators.

        Finally, an start response is prepared.

        Parameters
        ----------
        request: EnvironmentStartRequest
            The start request from the simulation controller.

        Returns
        -------
        EnvironmentStartResponse
            The answer from the environment, contains the available
            sensors and actuators.

        """
        LOG.debug(
            "Environment %s(id=0x%x, uid=%s) received "
            "EnvironmentStartRequest("
            "experiment_run_id=%s, environment_id=%s)",
            self.__class__,
            id(self),
            self.uid,
            request.run_id,
            request.environment_id,
        )
        sensors, actuators = self.start_environment()
        msg = EnvironmentStartResponse(
            request.run_id, self.uid, sensors, actuators
        )
        LOG.debug(
            "Environment %s(id=0x%x, uid=%s) sending "
            "EnvironmentStartResponse(experiment_run_id=%s, "
            "environment_id=%s, sensors=%s, actuators=%s)",
            self.__class__,
            id(self),
            self.uid,
            msg.run_id,
            msg.environment_id,
            sensors,
            actuators,
        )
        return msg

    def _handle_update(
        self, request: EnvironmentUpdateRequest
    ) -> EnvironmentUpdateResponse:
        """Handle an environment update request.

        The request contains current actuator values and the
        environment receives the actuator values in the update method.
        The environment answers with updated sensor readings, an
        environment reward, and the is_terminal set, wether the
        environment has finished or not.

        Finally, an update response is prepared.

        Parameters
        ----------
        request: EnvironmentUpdateRequest
            The update request from the simulation controller, contains
            the current actuator values from one or more agent.

        Returns
        -------
        EnvironmentUpdateResponse
            The response for the simulation controller, containing the
            updated sensor values, a reward, and the is_terminal-flag.

        """

        sensor, reward, is_terminal = self.update(request.actuators)

        return EnvironmentUpdateResponse(
            sender_environment_id=self.uid,
            receiver_simulation_controller_id=request.sender,
            experiment_run_id=request.experiment_run_id,
            environment_conductor_id=request.environment_conductor_id,
            sensors=sensor,
            reward=reward,
            is_terminal=is_terminal,
        )

    def _handle_shutdown(
        self, request: EnvironmentShutdownRequest
    ) -> EnvironmentShutdownResponse:
        """Handle an environment shutdown request.

        The :meth:`shutdown` is called that handles the shutdown of the
        environment. Finally, a shutdown response is prepared.

        Parameters
        ----------
        request: EnvironmentShutdownRequest
            The shutdown request from the simulation controller.

        Returns
        -------
        EnvironmentShutdownResponse
            The shutdown response for the simulation controller.

        """
        _ = self.shutdown()
        return EnvironmentShutdownResponse(request.run_id, self.uid, True)

    @abstractmethod
    def start_environment(
        self,
    ) -> Tuple[List[SensorInformation], List[ActuatorInformation]]:
        """Function to start the environment

        If the environment uses a simulation tool, this function
        can be used to initiate the simulation tool. Otherwise this
        function is used to prepare the environment for the simulation.
        It must be able to provide initial sensor information.

        Returns
        -------
        tuple(List[SensorInformation], List[ActuatorInformation])
            A tuple containing a list of available sensors and a list
            of available actuators.

        """
        raise NotImplementedError

    @abstractmethod
    def update(
        self, actuators: List[ActuatorInformation]
    ) -> Tuple[List[SensorInformation], float, bool]:
        """Function to update the environment

        This function receives the agent's actions and has to respond
        with new sensor information. This function should create a
        new simulation step.

        Parameters
        ----------
        actuators : list[ActuatorInformation]
            List of actuators with setpoints

        Returns
        -------
        tuple[list[SensorInformation], list[float], bool]
            A tuple containing a list of SensorInformation, a list of
            environment rewards and a flag whether the environment has
            terminated.

        """
        raise NotImplementedError

    def shutdown(self) -> bool:
        """Initiate the environment shutdown.

        In this function the :attr:`.is_terminal` is set to True, which
        leads to a break of the main loop in the :meth:`.run` method.

        Returns
        -------
        bool
            *True* if the shutdown was successful, *False* otherwise.

        """
        self.is_terminal = True
        return self.is_terminal

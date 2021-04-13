class RequestIsNoneError(Exception):
    """Raised when a request is None."""


class ReplyIsNoneError(Exception):
    """Raised when a reply is None."""


class InvalidRequestError(Exception):
    """Raised when a wrong request was received."""

    def __init__(self, expected, got):
        super().__init__(f"Expected {expected}, got {got}.")


class InvalidResponseError(Exception):
    """Raised when a wrong response was received."""

    def __init__(self, expected, got):
        super().__init__(f"Expected {expected}, got {got}.")


class TasksNotFinishedError(Exception):
    """Raised when neither the signal_monitor_task nor the
    transceive_task returned.
    """


class SignalInterruptError(Exception):
    """Raised when a signal was received."""


class InitializationFailedError(Exception):
    """Raised when initialization of an experiment failed."""


class ExperimentSetupFailedError(Exception):
    """Raised when the experiment setup failed."""


class DeadChildrenRisingAsZombiesError(Exception):
    """Raised when childrens died and starting to become zombies."""


class PrematureTaskDeathError(Exception):
    """Raised when a tasks died for its time."""


class ExperimentAlreadyRunningError(Exception):
    """Raised during experiment start if experiment is already running."""


class SimControllerFailedError(Exception):
    """Raised when a simulation controller could not be started."""


class EnvConductorFailedError(Exception):
    """Raised when an error during the execution of an environment
    conductor occurs.
    """


class AgentConductorFailedError(Exception):
    """Raised when an error during the execution of an agent conductor
    occurs.
    """


class OutOfActionSpaceError(Exception):
    """This error is raised if an :class:`.ActuatorInformation`
    receives a setpoint that is not contained in the action space
    of that actuator.
    """


class OutOfObservationSpaceError(Exception):
    """This error is raised if a :class:`.SensorInformation` is
    created with a value that is not contained in the observation
    space of that sensor.
    """

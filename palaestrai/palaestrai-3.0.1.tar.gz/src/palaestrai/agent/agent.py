"""This module contains the class :class:`Agent` that
stores all information regarding a specific agent.

"""


class Agent:
    """Stores information about an agent.

    The agent class is used to store information about an
    agent. It is currently used by the simulation controller
    to have a internal representation of all agents.

    Parameters
    ----------
    uid : uuid4
        The uid is used to identify an agent
    brain: :class:`~.Brain`
        An instance of a palaestrai brain. It
        defines what type of AI is used
    brain_params: dict
        This dictionary contains all parameters needed
        by the brain.
    muscle: :class:`~.Muscle`
        An instance of a palaestrai muscle. It
        defines what type of AI is used and is linked
        to the type of brain
    muscle_params: dict
        This dictionary contains all parameters needed
        by the muscle.
    sensors: any
        The list of sensors the agent is allowed to
        access.
    actuators: any
        The list of actuators the agent is allowed to
        access.
    """

    def __init__(
        self,
        uid,
        brain,
        brain_params,
        muscle,
        muscle_params,
        sensors,
        actuators,
    ):
        self.uid = uid
        self.brain = brain
        self.brain_params = brain_params
        self.muscle = muscle
        self.muscle_params = muscle_params
        self.sensors = sensors
        self.actuators = actuators

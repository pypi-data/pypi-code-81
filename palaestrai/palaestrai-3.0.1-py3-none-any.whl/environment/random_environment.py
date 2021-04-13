"""This module contains a dummy environment that can be used for
reference purposes.
"""
import numpy as np

from palaestrai.agent.actuator_information import ActuatorInformation
from palaestrai.agent.sensor_information import SensorInformation
from palaestrai.environment.environment import Environment
from palaestrai.types import Box, Discrete


class ContinuousRandomEnvironment(Environment):
    """
    The continuous dummy environment.
    The goal is to set the actuators to the closest integer of the
    corresponding sensor values

    """

    def __init__(self, connection, uid, seed: int, params):
        super().__init__(connection, uid, seed, params)

        self.rng = np.random.RandomState(seed)
        self.iter = 0
        self.max_iter = params.get("max_iter", 1000)
        self.num_sensors = params.get("num_sensors", 10)
        self.max_value = params.get("max_value", 10)

    def start_environment(self):
        """Function to start the environment

        The function sets the random sensors and for each sensor one
        actuator.

        Returns
        -------
        tuple
            A *tuple* of two lists, one containing SensorInformation
            and the second containing ActuatorInformation.

        """
        self._set_random_sensors()
        for num in range(self.num_sensors):
            self.actuators.append(
                ActuatorInformation(
                    0, Box(0, self.max_value, (1,)), "Actuator-" + str(num)
                )
            )
        return self.sensors, self.actuators

    def update(self, actuators):
        """Creates new sensor information

        This method creates new sensor readings. The actuator setpoints
        are ignored because the values are random.

        Parameters
        ----------
        actuators : list[actuator]
            List of actuators, currently not used

        Returns
        -------
        sensors : list[SensorInformation]
            List of SensorInformation with new random values

        """
        self.iter += 1
        if self.iter <= self.max_iter:
            reward = (
                self.max_value
                - sum(
                    [
                        abs(round(sens()) - act.setpoint)
                        for sens, act in zip(self.sensors, actuators)
                    ]
                )
                / self.num_sensors
            )

            self._set_random_sensors()
            return self.sensors, reward, False
        else:
            return list(), 0, True

    def _set_random_sensors(self):
        """creates random value for a sensor

        This function creates a random value for each sensor.
        """
        self.sensors = [
            SensorInformation(
                self.rng.uniform() * self.max_value,
                [0, self.max_value],
                "Sensor-" + str(num),
            )
            for num in range(self.num_sensors)
        ]


class DiscreteRandomEnvironment(Environment):
    """
    The continuous dummy environment.
    The goal is to choose the actuator closest to the mean of the
    sensor values
    """

    def __init__(self, connection, uid, seed, params):
        super().__init__(connection, uid, seed, params)
        self.rng = np.random.RandomState(seed)
        self.iter = 0
        self.max_iter = params.get("max_iter", 1000)
        self.num_sensors = params.get("num_sensors", 10)
        self.max_value = params.get("max_value", 10)
        self.resolution = params.get("resolution", 100)

    def start_environment(self):
        """Function to start the environment

        The function sets the random sensors and for each sensor one
        actuator.
        """
        self._set_random_sensors()
        self.actuators = [
            ActuatorInformation(0, Discrete(self.resolution), "Actuator-0")
        ]
        return self.sensors, self.actuators

    def update(self, actuators):
        """Creates new sensor information

        This method creates new sensor readings. The actuator setpoint
        is ignored because the values are random. Only one actuator is
        allowed

        Parameters
        ----------
        actuators : list[ActuatorInformation]
            List of actuators, in this case only one actuator is
            allowed.

        Returns
        -------
        sensors : list[SensorInformation]
            List of SensorInformation with new random values

        """
        assert len(actuators) == 1, "Can only handle 1 actuator"
        actuator = actuators[0]
        self.iter += 1
        if self.iter <= self.max_iter:
            mean_of_sensors = sum(map(lambda x: x(), self.sensors)) / len(
                self.sensors
            )
            perfect_setpoint = round(
                mean_of_sensors / (self.max_value / self.resolution)
            )
            reward = self.resolution - abs(
                actuator.setpoint - perfect_setpoint
            )

            self._set_random_sensors()
            return self.sensors, reward, False
        else:
            return list(), 0, True

    def _set_random_sensors(self):
        """creates random value for a sensor

        This function creates a random value for each sensor.
        """
        self.sensors = [
            SensorInformation(
                self.rng.uniform() * self.max_value,
                [0, self.max_value],
                "Sensor-" + str(num),
            )
            for num in range(self.num_sensors)
        ]

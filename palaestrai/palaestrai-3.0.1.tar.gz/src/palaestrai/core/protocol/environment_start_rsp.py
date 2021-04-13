class EnvironmentStartResponse:
    def __init__(self, run_id, environment_id, sensors, actuators):
        self._run_id = run_id
        self._environment_id = environment_id
        self._sensors = sensors
        self._actuators = actuators

    @property
    def run_id(self):
        return self._run_id

    @run_id.setter
    def run_id(self, value):
        self._run_id = value

    @property
    def environment_id(self):
        return self._environment_id

    @environment_id.setter
    def environment_id(self, value):
        self._environment_id = value

    @property
    def actuators(self):
        return self._actuators

    @actuators.setter
    def actuators(self, value):
        self._actuators = value

    @property
    def sensors(self):
        return self._sensors

    @sensors.setter
    def sensors(self, value):
        self._sensors = value

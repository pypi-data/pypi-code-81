class ExperimentShutdownRequest:
    def __init__(self, experiment_id):
        self._experiment_id = experiment_id

    @property
    def experiment_id(self):
        return self._experiment_id

    @experiment_id.setter
    def experiment_id(self, value):
        self._experiment_id = value

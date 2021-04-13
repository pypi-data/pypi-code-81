class ExperimentShutdownResponse:
    def __init__(self, successful: bool, error):
        self._successful = successful
        self._error = error

    @property
    def successful(self):
        return self._successful

    @successful.setter
    def successful(self, value):
        self._successful = value

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = value

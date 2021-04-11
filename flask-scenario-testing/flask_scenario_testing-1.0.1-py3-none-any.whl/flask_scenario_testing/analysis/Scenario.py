class Scenario(object):

    def __init__(self, name, started_at, ended_at):
        self._name = name
        self._started_at = started_at
        self._ended_at = ended_at

    def name(self):
        return self._name

    def started_at(self):
        return self._started_at

    def ended_at(self):
        return self._ended_at

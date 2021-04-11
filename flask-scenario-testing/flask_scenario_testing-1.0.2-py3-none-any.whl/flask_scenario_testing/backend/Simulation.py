from datetime import datetime
from typing import Optional


class RunningScenario(object):

    def __init__(self, name: str, started_at: datetime, modifiers: dict):
        self._name = name
        self._started_at = started_at
        self._modifiers = modifiers
        self._stopped_at = None

    def name(self) -> str:
        return self._name

    def started_at(self) -> datetime:
        return self._started_at

    def has_modifiers(self):
        return bool(self._modifiers)

    def modifiers(self):
        return self._modifiers

    def end(self):
        self._stopped_at = datetime.utcnow()

    def is_running(self):
        return self._stopped_at is None

    def ended_at(self):
        return self._stopped_at


class Simulation:
    """
        Keeps track of running scenarios.
    """

    def __init__(self):
        self._scenarios = []
        self._started_at = None
        self._stopped_at = None

    def started_at(self):
        return self._started_at

    def stopped_at(self):
        return self._stopped_at

    def start(self):
        if self.is_running():
            raise Exception('Simulation is already running')

        self._started_at = datetime.utcnow()

    def start_scenario(self, name: str, modifiers: Optional[dict] = None):
        if not self.is_running():
            raise Exception('Can not start scenario when simulation is not running')

        if self.scenario_is_running():
            self.running_scenario().end()

        self._scenarios.append(RunningScenario(
            name=name,
            started_at=datetime.utcnow(),
            modifiers=modifiers or {}
        ))

    def current_modifiers(self):
        if not self.scenario_is_running():
            return {}

        return self.running_scenario().modifiers()

    def stop_running_scenario(self):
        assert self.scenario_is_running(), "No scenario is running"

        self.running_scenario().end()

    def stop(self):
        if not self.is_running():
            raise Exception('Simulation is not running')

        if self.scenario_is_running():
            self.running_scenario().end()

        self._stopped_at = datetime.utcnow()

    def _finalise_last_scenario(self):
        pass

    def scenario_is_running(self):
        return len(self.scenarios()) > 0 and self.scenarios()[-1].is_running()

    def is_running(self) -> bool:
        return self._started_at is not None

    def running_scenario(self) -> Optional[RunningScenario]:
        if not self.scenario_is_running():
            return None

        return self.scenarios()[-1]

    def scenarios(self):
        return self._scenarios


simulation: Simulation = Simulation()

from typing import Any

from moonspec import _MOONSPEC_RUNTIME_STATE
from moonspec.api.subject import Subject, SubjectExpectationException, ComparatorExpectations


class HistoricFact(Subject):
    """
    A subject used to hold value of a fact from previous runs
    """
    def __init__(self, key: str, value: Any) -> None:
        super().__init__(value, identity=key)
        self.key = key


class Fact(Subject):
    """
    A subject used to hold state indicator of a system - a fact
    """
    def __init__(self, key: str, value: Any) -> None:
        super().__init__(value, identity=key)
        self._previous: HistoricFact = HistoricFact(key, None)
        if _MOONSPEC_RUNTIME_STATE.has_historic_fact(key):
            self._previous = HistoricFact(key, _MOONSPEC_RUNTIME_STATE.get_historic_fact_value(key))

        self.key = key

    def should_not_have_changed(self, missing_ok: bool = True) -> None:
        """
        Verify if value of this fact has not changed over time
        :param missing_ok: True if absent historic values should be ignored, False otherwise. By default, True.
        :return: True if fact value has not changed when compared to current value (self vs historic)
        """
        if missing_ok and self._previous.value is None:
            return

        if self.value != self._previous.value:
            raise SubjectExpectationException(self._identity, self._previous.value,
                                              self.value, ComparatorExpectations.NOT_CHANGED)

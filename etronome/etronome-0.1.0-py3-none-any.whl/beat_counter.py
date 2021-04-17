import datetime

from .model import Model


class BeatCounter:
    TIMEOUT = 1.5

    def __init__(self, model: Model) -> None:
        self._model = model
        self._tap_times: list[datetime.datetime] = []

    def tap(self) -> None:
        tap_time = datetime.datetime.now()
        if len(self._tap_times) == 0:
            self._tap_times.append(tap_time)
            return

        time_since_last_tap = (tap_time - self._tap_times[-1]).total_seconds()
        if time_since_last_tap > BeatCounter.TIMEOUT:
            self._tap_times = [tap_time]
        else:
            self._tap_times.append(tap_time)
            self._model.bpm = self._bpm

    @property
    def _bpm(self) -> float:
        total_time = (self._tap_times[-1] - self._tap_times[0]).total_seconds()
        return 60 * (len(self._tap_times) - 1) / total_time

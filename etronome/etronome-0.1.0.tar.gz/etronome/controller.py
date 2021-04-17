from dataclasses import dataclass

from .beat_counter import BeatCounter
from .model import Model


@dataclass
class ControlsController:
    model: Model

    def up_action(self) -> None:
        self.model.bpm += 1

    def down_action(self) -> None:
        self.model.bpm -= 1


@dataclass
class PlayPauseController:
    model: Model

    def button_action(self) -> None:
        if self.model.is_playing:
            self.model.stop()
        else:
            self.model.start()


@dataclass
class TapperController:
    beat_counter: BeatCounter

    def button_action(self) -> None:
        self.beat_counter.tap()

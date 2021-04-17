import tkinter as tk

from ..controller import PlayPauseController
from ..model import Model


class PlayPause(tk.Frame):
    def __init__(
        self,
        master: tk.Frame,
        model: Model
    ) -> None:
        super().__init__(master=master)

        controller = PlayPauseController(model)

        self.button = tk.Button(master=self, text='play')
        self.button.bind(
            '<Button 1>',
            lambda event: controller.button_action()
        )
        self.button.pack()

        model.register_for_is_playing(self)
        self.update_(model.is_playing)

    def update_(self, value: bool) -> None:
        self.button['text'] = 'pause' if value else 'play'

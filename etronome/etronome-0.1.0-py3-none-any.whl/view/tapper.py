import tkinter as tk

from ..beat_counter import BeatCounter
from ..controller import TapperController
from ..model import Model


class Tapper(tk.Frame):
    def __init__(
        self,
        master: tk.Frame,
        model: Model
    ) -> None:
        super().__init__(master=master)

        beat_counter = BeatCounter(model)
        controller = TapperController(beat_counter)

        button = tk.Button(master=self, text='tap me', width=10)
        button.bind('<Button 1>', lambda event: controller.button_action())
        button.pack()

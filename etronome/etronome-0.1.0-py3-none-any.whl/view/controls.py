import tkinter as tk

from ..controller import ControlsController
from ..model import Model


class Controls(tk.Frame):
    def __init__(
        self,
        master: tk.Frame,
        model: Model,
    ) -> None:
        super().__init__(master=master)

        controller = ControlsController(model)

        up_button = tk.Button(master=self, text='+', width=2)
        up_button.bind('<Button 1>', lambda event: controller.up_action())
        up_button.pack()

        down_button = tk.Button(master=self, text='-', width=2)
        down_button.bind('<Button 1>', lambda event: controller.down_action())
        down_button.pack()

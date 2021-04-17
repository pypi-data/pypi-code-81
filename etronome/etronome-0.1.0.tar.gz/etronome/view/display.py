import tkinter as tk

from ..model import Model


class Display(tk.Frame):
    def __init__(self, master: tk.Frame, model: Model) -> None:
        super().__init__(master=master, height=2)

        self.bpm = tk.Label(master=self, text=str(model.bpm))
        self.bpm.pack(side=tk.LEFT)

        unit = tk.Label(master=self, text='bpm')
        unit.pack(side=tk.RIGHT)

        model.register_for_bpm(self)

    def update_(self, value: float) -> None:
        self.bpm['text'] = str(int(value))

import tkinter as tk

from .controls import Controls
from .display import Display
from .play_pause import PlayPause
from .tapper import Tapper
from ..model import Model


class TopView(tk.Frame):
    def __init__(self, master: tk.Tk, model: Model) -> None:
        super().__init__(master=master)

        top_frame = tk.Frame(master=self)
        left_frame = tk.Frame(master=top_frame)
        display = Display(master=left_frame, model=model)
        display.pack(side=tk.TOP)

        play_pause = PlayPause(master=left_frame, model=model)
        play_pause.pack(side=tk.BOTTOM)

        left_frame.pack(side=tk.LEFT)

        controls = Controls(master=top_frame, model=model)
        controls.pack(side=tk.RIGHT)
        top_frame.pack(side=tk.TOP)

        tapper = Tapper(master=self, model=model)
        tapper.pack(side=tk.BOTTOM)

        self.pack()

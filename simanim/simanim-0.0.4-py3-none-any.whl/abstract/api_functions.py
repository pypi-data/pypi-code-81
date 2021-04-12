from typing import Tuple, Callable
from contextlib import AbstractContextManager
import platform
from .core import anim_context_var, InputFloat, InputList, FinishAnimException, AnimVars

__all__ = ["InputFloat", "InputList", "PixelsPerUnit","ViewBox","FramesPerSecond","UpdatesPerFrame", "BackgroundColor", "Draw", "Rotate","Finish", "Run"]

def PixelsPerUnit(dpu:float):
    ctx = anim_context_var.get()
    ctx.settings.px_per_unit = dpu

def ViewBox(xy_min:Tuple[float,float], width:float, height:float):
    ctx = anim_context_var.get()
    ctx.settings.view_box = (xy_min, width, height)

def FramesPerSecond(fps:float):
    ctx = anim_context_var.get()
    ctx.settings.frames_per_second = fps

def UpdatesPerFrame(upf: int):
    ctx = anim_context_var.get()
    ctx.settings.updates_per_frame = upf

def BackgroundColor(color: str):
    ctx = anim_context_var.get()
    ctx.settings.background_color = color

def Finish():
    raise FinishAnimException()

def Draw(*primitives):
    ctx = anim_context_var.get()
    for p in primitives:
        ctx.dw_driver.draw(p)

def Rotate(point:Tuple[float,float], angle:float) -> AbstractContextManager:
    ctx = anim_context_var.get()
    return ctx.dw_driver.Rotate(point, angle)

def Run(setup_handler:Callable[[AnimVars], None], update_handler:Callable[[AnimVars], None], draw_handler:Callable[[AnimVars], None]):
    s = platform.system()
    if s == 'Emscripten':
        from ..pyodide.gui import Run as PyodideRun
        PyodideRun(setup_handler, update_handler, draw_handler)
    else:
        from ..qt.gui import Run as QtRun
        QtRun(setup_handler, update_handler, draw_handler)
    


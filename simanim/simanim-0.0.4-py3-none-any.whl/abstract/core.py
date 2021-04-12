from typing import Tuple, Callable, Dict, Any, Type, Optional, List
from contextvars import ContextVar
from abc import ABC, abstractmethod
from contextlib import AbstractContextManager

class DrawingPrimitive(ABC):
    def __init__(self):
        self.pen_color: str = self._default("pen_color")
        self.fill_color: str = self._default("fill_color")
        self.line_width: float = self._default("line_width")
        self.line_dashed: bool = self._default("line_dashed", False)
    
    def __setattr__(self, name, value):
        ctx = anim_context_var.get()
        super().__setattr__(name, value)
        ctx.primitives_defaults[(type(self), name)] = value
    
    def _default(self, name: str, value: Any = None):
        ctx = anim_context_var.get()
        key = (type(self), name)
        if key in ctx.primitives_defaults:
            return ctx.primitives_defaults[key]
        else:
            return value

class AnimSettings:
    def __init__(self):
        self.px_per_unit = 5.0
        self.view_box = ((0,0),160,90)
        self.frames_per_second = 30.0
        self.updates_per_frame = 1
        self.background_color = '#ffffff'

    def update_derived_attributes(self):
        _ , width, height = self.view_box
        self.updates_per_second = self.frames_per_second * self.updates_per_frame
        self.frame_period = 1 / self.frames_per_second
        self.update_period = 1 / self.updates_per_second
        self.window_with_px = int(width * self.px_per_unit)
        self.window_height_px = int(height * self.px_per_unit)

    def scalar_u_to_px(self, scalar_u:float):
        return scalar_u * self.px_per_unit

    def point_u_to_px(self, point_u: Tuple[float,float]):
        x_u, y_u = point_u
        (x_min, y_min), _, height = self.view_box
        x_px = self.scalar_u_to_px(x_u - x_min)
        y_px = self.scalar_u_to_px(y_min + height - y_u)
        return (x_px, y_px)

class DrawingDriver(ABC):

    def setup(self, anim_settings: AnimSettings):
        self.anim_settings = anim_settings

    @abstractmethod
    def Rotate(self, point:Tuple[float,float], angle:float) -> AbstractContextManager:
        pass

    @abstractmethod
    def draw(self, primitive: DrawingPrimitive):
        pass

class AnimVars:
    def __init__(self, input_var_getters: Optional[Dict[str, Callable[[], float]]] = None):
        self.t = 0
        self.dt = None
        self._input_vars = dict()
        self._input_var_getters = dict() if input_var_getters is None else input_var_getters

    def __setattr__(self, name, value):
        if isinstance(value, InputDeclaration):
            self._input_vars[name] = value
            if name in self._input_var_getters:
                input_value = self._input_var_getters[name]()
                super().__setattr__(name, input_value)
            else:
                super().__setattr__(name, value.default)
        else:
            super().__setattr__(name, value)


class InputDeclaration(ABC):
    pass
class InputFloat(InputDeclaration):
    def __init__(self,default:float, limits:Tuple[float,float]):
        self.default = default
        self.limit_from, self.limit_to = limits

class InputList(InputDeclaration):
    def __init__(self,default, lov:List):
        self.default = default
        self.lov = list(lov)

anim_context_var: ContextVar["AnimContext"] = ContextVar('anim_context_var')

class FinishAnimException(Exception):
    pass

class AnimContext:
    def __init__(self, setup_handler:Callable[[AnimVars], None], update_handler:Callable[[AnimVars], None], draw_handler:Callable[[AnimVars], None]):
        self.dw_driver = None
        self.setup_handler = setup_handler
        self.update_handler = update_handler
        self.draw_handler = draw_handler
        self.setting: AnimSettings = None
        self.vars: AnimVars = None
        self.primitives_defaults: Dict[Tuple[Type,str], Any] = None
        self.reset()

    def driver(self, dw_driver:DrawingDriver):
        self.dw_driver = dw_driver

    def reset(self, input_var_getters: Optional[Dict[str, Callable[[str], float]]] = None):
        self.vars = AnimVars(input_var_getters)
        self.settings = AnimSettings()
        try:
            ctx_token = anim_context_var.set(self)
            self.setup_handler(self.vars)
            self.settings.update_derived_attributes()
            self.vars.dt = self.settings.update_period
            self.vars.update_count = 0
        finally:
            anim_context_var.reset(ctx_token)

    def draw_frame(self):
        try:
            ctx_token = anim_context_var.set(self)
            self.primitives_defaults = dict()
            self.draw_handler(self.vars)
        finally:
            anim_context_var.reset(ctx_token)

    def updates_between_frames(self):
        try:
            ctx_token = anim_context_var.set(self)
            for _ in range(self.settings.updates_per_frame):
                self.vars.update_count += 1
                self.vars.t = self.vars.update_count * self.vars.dt
                self.update_handler(self.vars)
        except FinishAnimException:
            return False
        finally:
            anim_context_var.reset(ctx_token)
        return True

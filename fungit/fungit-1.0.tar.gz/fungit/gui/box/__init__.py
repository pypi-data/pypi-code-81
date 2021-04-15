from typing import Any

from fungit.shared import GitType
from ..style import Fx, Color, Cursor
from ..utils import create_profile
from ..renderer import Renderer


class Box:
    current: GitType
    name: str
    genre: int
    t_w: int
    t_h: int
    x: int
    y: int
    w: int
    h: int
    content: Any
    box: str

    @classmethod
    def create_profile(cls):
        # _line_color = BOX_SELECTED_COLOR if cls.genre & cls.current else ''
        _line_color = ""
        cls.box = create_profile(
            cls.x, cls.y, cls.w, cls.h, cls.name, line_color=_line_color
        )

    @classmethod
    def render(cls):
        Renderer.now(cls.box, cls.box_content)

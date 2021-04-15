from typing import List, Any

from fungit.shared import GitType
from ..renderer import Renderer
from ..style import Fx, Cursor
from ..theme import Theme
from ..utils import create_profile
from . import Box
from .content_box import ContentBox


class NavBox(Box):
    # only change in father class, sub class only read
    current: int = GitType.STATUS

    t_w: int
    t_h: int
    name: str
    genre: int
    x: int
    y: int
    w: int
    h: int
    raw: Any
    content: List
    selected: int
    box: str
    box_content: str

    @classmethod
    def set_current(cls, t: int):
        cls.current = t

    @classmethod
    def create_profile(cls):
        _line_color = Theme.BOX_SELECTED_COLOR if cls.genre & cls.current else ""
        _item_msg = (
            f"{cls.selected + 1} of {len(cls.content)}" if len(cls.content) > 1 else ""
        )
        cls.box = create_profile(
            cls.x, cls.y, cls.w, cls.h, cls.name, _item_msg, line_color=_line_color
        )

    @classmethod
    def fetch_data(cls):
        """Get raw data.

        Get the list of original data and cache it in `cls.raw`, each of which
        is an independent data object instance(Override by subclass).
        """
        pass

    @classmethod
    def generate(cls):
        """Content of production display.

        All the acquired data is produced as the class content that can be
        displayed, colored and cached in `cls.content`(Override by subclass).
        """
        pass

    @classmethod
    def update(cls):
        """Updatee display content.

        According to the currently selected item to update the displayed
        content block (current item BOLD), generate a content string, and
        assign it to `cla.box_content`.
        """
        start_x = cls.x + 1
        start_y = cls.y + 1
        line_w = cls.w - 2

        cls.box_content = ""
        for idx, line in enumerate(cls.content):
            if idx < cls.h - 2:
                _line = f"{Cursor.to(start_y, start_x)}{line if len(line) < line_w else line[:line_w]}"
                if cls.genre & cls.current:
                    _line = f"{Fx.b}{_line}{Fx.ub}"
                cls.box_content += _line
                start_y += 1

    @classmethod
    def render(cls):
        Renderer.now(cls.box, cls.box_content)

        if cls.current & cls.genre:
            ContentBox.notify(cls)

    @classmethod
    def notify(cls, update_data: bool = False, re_profile: bool = True):
        if update_data:
            cls.fetch_data()
            cls.generate()
        if re_profile:
            cls.create_profile()
        # every notify must update display string and render all.
        cls.update()
        cls.render()

    @classmethod
    def set_selected(cls, v):
        cls.selected = v
        cls.notify()

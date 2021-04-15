from typing import Tuple

from .style import Symbol, Fx, Color, Cursor


def create_profile(
    x: int = 0,
    y: int = 0,
    width: int = 0,
    height: int = 0,
    title: str = "",
    title2: str = "",
    line_color: Color = None,
    title_color: Color = None,
    fill: bool = True,
    box=None,
) -> str:
    """Create a box from a box object or by given arguments"""
    # out: str = f'{Term.fg}{Term.bg}'
    out: str = f""
    num: int = 0
    if not line_color:
        line_color = ""
    if not title_color:
        title_color = ""

    # * Get values from box class if given
    if box:
        x = box.x
        y = box.y
        width = box.width
        height = box.height
        title = box.name
        num = box.num
    hlines: Tuple[int, int] = (y, y + height - 1)

    out += f"{line_color}"

    # * Renderer all horizontal lines
    for hpos in hlines:
        out += f"{Cursor.to(hpos, x)}{Symbol.h_line * (width - 1)}"

    # * Renderer all vertical lines and fill if enabled
    for hpos in range(hlines[0] + 1, hlines[1]):
        out += f'{Cursor.to(hpos, x)}{Symbol.v_line}{" " * (width-2) if fill else Cursor.r(width-2)}{Symbol.v_line}'

    # * Renderer corners
    out += f"{Cursor.to(y, x)}{Symbol.left_up}{Cursor.to(y, x + width - 1)}{Symbol.right_up}{Cursor.to(y + height - 1, x)}{Symbol.left_down}{Cursor.to(y + height - 1, x + width - 1)}{Symbol.right_down}"

    # * Renderer titles if enabled
    if title:
        numbered: str = ""
        out += f"{Cursor.to(y, x + 2)}{Symbol.title_left}{Fx.b}{numbered}{title_color}{title}{Fx.ub}{line_color}{Symbol.title_right}"
    if title2:
        # out += f'{Cursor.to(hlines[1], width - 2 - len(title2))}{Symbol.title_left}{title_color}{Fx.b}{title2}{Fx.ub}{line_color}{Symbol.title_right}'
        out += f"{Cursor.to(hlines[1], width - 2 - len(title2))}{title_color}{Fx.b}{title2}{Fx.ub}{line_color}"

    # return f'{out}{Term.fg}{Cursor.to(y + 1, x + 1)}'
    return f"{out}{Fx.reset}"

import os
import sys
import termios
import threading
from typing import List, Tuple

from .gui.renderer import Renderer


class Term:
    """Terminal info and commands"""
    width: int = 0
    height: int = 0
    resized: bool = False
    _w: int = 0
    _h: int = 0
    fg: str = ""  # * Default foreground color
    bg: str = ""  # * Default background color
    hide_cursor = "\033[?25l"  # * Hide terminal cursor
    show_cursor = "\033[?25h"  # * Show terminal cursor
    alt_screen = "\033[?1049h"  # * Switch to alternate screen
    normal_screen = "\033[?1049l"  # * Switch to normal screen
    clear = "\033[2J\033[0;0f"  # * Clear screen and set cursor to position 0,0
    # * Enable reporting of mouse position on click and release
    mouse_on = "\033[?1002h\033[?1015h\033[?1006h"
    mouse_off = "\033[?1002l"  # * Disable mouse reporting
    # * Enable reporting of mouse position at any movement
    mouse_direct_on = "\033[?1003h"
    mouse_direct_off = "\033[?1003l"  # * Disable direct mouse reporting
    winch = threading.Event()
    old_boxes: List = []
    min_width: int = 0
    min_height: int = 0

    @classmethod
    def init(cls):
        Term.width = os.get_terminal_size().columns
        Term.height = os.get_terminal_size().lines

        Renderer.now(Term.alt_screen, Term.clear, Term.hide_cursor,
                     Term.mouse_on, Term.title("fungit"))
        cls.echo(False)

    @classmethod
    def clear(cls):
        Renderer.now(Term.clear, Term.normal_screen, Term.show_cursor,
                     Term.mouse_off, Term.mouse_direct_off, Term.title())
        cls.echo(True)

    @staticmethod
    def title(text: str = "") -> str:
        out: str = f'{os.environ.get("TERMINAL_TITLE", "")}'
        if out and text:
            out += " "
        if text:
            out += f'{text}'
        return f'\033]0;{out}\a'

    @staticmethod
    def echo(on: bool):
        """Toggle input echo"""
        (iflag, oflag, cflag, lflag, ispeed, ospeed,
            cc) = termios.tcgetattr(sys.stdin.fileno())
        if on:
            lflag |= termios.ECHO  # type: ignore
        else:
            lflag &= ~termios.ECHO  # type: ignore
        new_attr = [iflag, oflag, cflag, lflag, ispeed, ospeed, cc]
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSANOW, new_attr)

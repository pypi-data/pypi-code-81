import re
from typing import List, Dict, Tuple, Union, Iterable


class Cursor:
    """Class with collection of cursor movement functions: .t[o](line, column) | .r[ight](columns) | .l[eft](columns) | .u[p](lines) | .d[own](lines) | .save() | .restore()"""

    @staticmethod
    def to(line: int, col: int) -> str:
        # * Move cursor to line, column
        return "\033[{};{}f".format(line, col)

    @staticmethod
    def right(dx: int) -> str:
        return "\033[{}C".format(dx)

    @staticmethod
    def left(dx: int) -> str:
        return "\033[{}D".format(dx)

    @staticmethod
    def up(dy: int) -> str:
        return "\033[{}A".format(dy)

    @staticmethod
    def down(dy: int) -> str:
        return "\033[{}B".format(dy)

    save: str = "\033[s"  # * Save cursor position
    restore: str = "\033[u"  # * Restore saved cursor postion
    t = to
    r = right
    l = left
    u = up
    d = down


class Fx:
    """Text effects
    * trans(string: str): Replace whitespace with escape move right to not overwrite background behind whitespace.
    * uncolor(string: str) : Removes all 24-bit color and returns string .
    """

    start = "\033["  # * Escape sequence start
    sep = ";"  # * Escape sequence separator
    end = "m"  # * Escape sequence end
    # * Reset foreground/background color and text effects
    reset = rs = "\033[0m"
    bold = b = "\033[1m"  # * Bold on
    unbold = ub = "\033[22m"  # * Bold off
    dark = d = "\033[2m"  # * Dark on
    undark = ud = "\033[22m"  # * Dark off
    italic = i = "\033[3m"  # * Italic on
    unitalic = ui = "\033[23m"  # * Italic off
    underline = u = "\033[4m"  # * Underline on
    ununderline = uu = "\033[24m"  # * Underline off
    blink = bl = "\033[5m"  # * Blink on
    unblink = ubl = "\033[25m"  # * Blink off
    strike = s = "\033[9m"  # * Strike / crossed-out on
    unstrike = us = "\033[29m"  # * Strike / crossed-out off

    # * Precompiled regex for finding a 24-bit color escape sequence in a string
    color_re = re.compile(r"\033\[\d+;\d?;?\d*;?\d*;?\d*m")

    @staticmethod
    def trans(string: str):
        return string.replace(" ", "\033[1C")

    @classmethod
    def uncolor(cls, string: str) -> str:
        return f'{cls.color_re.sub("", string)}'


class Color:
    """Holds representations for a 24-bit color value
    __init__(color, depth="fg", default=False)
    -- color accepts 6 digit hexadecimal: string "#RRGGBB", 2 digit hexadecimal: string "#FF" or decimal RGB "255 255 255" as a string.
    -- depth accepts "fg" or "bg"
    __call__(*args) joins str arguments to a string and apply color
    __str__ returns escape sequence to set color
    __iter__ returns iteration over red, green and blue in integer values of 0-255.
    * Values:  .hexa: str  |  .dec: Tuple[int, int, int]  |  .red: int  |  .green: int  |  .blue: int  |  .depth: str  |  .escape: str
    """

    hexa: str
    dec: Tuple[int, int, int]
    red: int
    green: int
    blue: int
    depth: str
    escape: str
    default: bool

    TRUE_COLOR = False

    def __init__(self, color: str, depth: str = "fg", default: bool = False):
        self.depth = depth
        self.default = default
        try:
            if not color:
                self.dec = (-1, -1, -1)
                self.hexa = ""
                self.red = self.green = self.blue = -1
                self.escape = "\033[49m" if depth == "bg" and default else ""
                return

            elif color.startswith("#"):
                self.hexa = color
                if len(self.hexa) == 3:
                    self.hexa += self.hexa[1:3] + self.hexa[1:3]
                    c = int(self.hexa[1:3], base=16)
                    self.dec = (c, c, c)
                elif len(self.hexa) == 7:
                    self.dec = (
                        int(self.hexa[1:3], base=16),
                        int(self.hexa[3:5], base=16),
                        int(self.hexa[5:7], base=16),
                    )
                else:
                    raise ValueError(
                        f"Incorrectly formatted hexadecimal rgb string: {self.hexa}"
                    )

            else:
                c_t = tuple(map(int, color.split(" ")))
                if len(c_t) == 3:
                    self.dec = c_t  # type: ignore
                else:
                    raise ValueError(f'RGB dec should be "0-255 0-255 0-255"')

            ct = self.dec[0] + self.dec[1] + self.dec[2]
            if ct > 255 * 3 or ct < 0:
                raise ValueError(f"RGB values out of range: {color}")
        except Exception as e:
            # errlog.exception(str(e))
            self.escape = ""
            return

        if self.dec and not self.hexa:
            self.hexa = f'{hex(self.dec[0]).lstrip("0x").zfill(2)}{hex(self.dec[1]).lstrip("0x").zfill(2)}{hex(self.dec[2]).lstrip("0x").zfill(2)}'

        if self.dec and self.hexa:
            self.red, self.green, self.blue = self.dec
            self.escape = f'\033[{38 if self.depth == "fg" else 48};2;{";".join(str(c) for c in self.dec)}m'

        if Color.TRUE_COLOR:
            self.escape = f"{self.truecolor_to_256(rgb=self.dec, depth=self.depth)}"

    def __str__(self) -> str:
        return self.escape

    def __repr__(self) -> str:
        return repr(self.escape)

    def __iter__(self) -> Iterable:
        for c in self.dec:
            yield c

    # def __call__(self, *args: str) -> str:
    #     if len(args) < 1:
    #         return ""
    #     return f'{self.escape}{"".join(args)}{getattr(Term, self.depth)}'

    @staticmethod
    def truecolor_to_256(rgb: Tuple[int, int, int], depth: str = "fg") -> str:
        out: str = ""
        pre: str = f'\033[{"38" if depth == "fg" else "48"};5;'

        greyscale: Tuple[int, int, int] = (rgb[0] // 11, rgb[1] // 11, rgb[2] // 11)
        if greyscale[0] == greyscale[1] == greyscale[2]:
            out = f"{pre}{232 + greyscale[0]}m"
        else:
            out = f"{pre}{round(rgb[0] / 51) * 36 + round(rgb[1] / 51) * 6 + round(rgb[2] / 51) + 16}m"

        return out

    @staticmethod
    def escape_color(
        hexa: str = "", r: int = 0, g: int = 0, b: int = 0, depth: str = "fg"
    ) -> str:
        """Returns escape sequence to set color
        * accepts either 6 digit hexadecimal hexa="#RRGGBB", 2 digit hexadecimal: hexa="#FF"
        * or decimal RGB: r=0-255, g=0-255, b=0-255
        * depth="fg" or "bg"
        """
        dint: int = 38 if depth == "fg" else 48
        color: str = ""
        if hexa:
            try:
                if len(hexa) == 3:
                    c = int(hexa[1:], base=16)
                    if Color.TRUE_COLOR:
                        color = f"\033[{dint};2;{c};{c};{c}m"
                    else:
                        color = f"{Color.truecolor_to_256(rgb=(c, c, c), depth=depth)}"
                elif len(hexa) == 7:
                    if Color.TRUE_COLOR:
                        color = f"\033[{dint};2;{int(hexa[1:3], base=16)};{int(hexa[3:5], base=16)};{int(hexa[5:7], base=16)}m"
                    else:
                        color = f"{Color.truecolor_to_256(rgb=(int(hexa[1:3], base=16), int(hexa[3:5], base=16), int(hexa[5:7], base=16)), depth=depth)}"
            except ValueError as e:
                # errlog.exception(f'{e}')
                pass
        else:
            if Color.TRUE_COLOR:
                color = f"\033[{dint};2;{r};{g};{b}m"
            else:
                color = f"{Color.truecolor_to_256(rgb=(r, g, b), depth=depth)}"
        return color

    @classmethod
    def fg(cls, *args) -> str:
        if len(args) > 2:
            return cls.escape_color(r=args[0], g=args[1], b=args[2], depth="fg")
        else:
            return cls.escape_color(hexa=args[0], depth="fg")

    @classmethod
    def bg(cls, *args) -> str:
        if len(args) > 2:
            return cls.escape_color(r=args[0], g=args[1], b=args[2], depth="bg")
        else:
            return cls.escape_color(hexa=args[0], depth="bg")


class Symbol:
    h_line: str = "─"
    v_line: str = "│"
    left_up: str = "┌"
    right_up: str = "┐"
    left_down: str = "└"
    right_down: str = "┘"
    title_left: str = "┤"
    title_right: str = "├"
    div_up: str = "┬"
    div_down: str = "┴"
    graph_up: Dict[float, str] = {
        0.0: " ",
        0.1: "⢀",
        0.2: "⢠",
        0.3: "⢰",
        0.4: "⢸",
        1.0: "⡀",
        1.1: "⣀",
        1.2: "⣠",
        1.3: "⣰",
        1.4: "⣸",
        2.0: "⡄",
        2.1: "⣄",
        2.2: "⣤",
        2.3: "⣴",
        2.4: "⣼",
        3.0: "⡆",
        3.1: "⣆",
        3.2: "⣦",
        3.3: "⣶",
        3.4: "⣾",
        4.0: "⡇",
        4.1: "⣇",
        4.2: "⣧",
        4.3: "⣷",
        4.4: "⣿",
    }
    graph_up_small = graph_up.copy()
    graph_up_small[0.0] = "\033[1C"

    graph_down: Dict[float, str] = {
        0.0: " ",
        0.1: "⠈",
        0.2: "⠘",
        0.3: "⠸",
        0.4: "⢸",
        1.0: "⠁",
        1.1: "⠉",
        1.2: "⠙",
        1.3: "⠹",
        1.4: "⢹",
        2.0: "⠃",
        2.1: "⠋",
        2.2: "⠛",
        2.3: "⠻",
        2.4: "⢻",
        3.0: "⠇",
        3.1: "⠏",
        3.2: "⠟",
        3.3: "⠿",
        3.4: "⢿",
        4.0: "⡇",
        4.1: "⡏",
        4.2: "⡟",
        4.3: "⡿",
        4.4: "⣿",
    }
    graph_down_small = graph_down.copy()
    graph_down_small[0.0] = "\033[1C"
    meter: str = "■"
    up: str = "↑"
    down: str = "↓"
    left: str = "←"
    right: str = "→"
    enter: str = "↲"
    # ok: str = f'{Color.fg("#30ff50")}√{Color.fg("#cc")}'
    # fail: str = f'{Color.fg("#ff3050")}!{Color.fg("#cc")}'


if __name__ == "__main__":
    green = Color.fg("#00ff00")
    a = f"{green}abcde"
    print(len(a))

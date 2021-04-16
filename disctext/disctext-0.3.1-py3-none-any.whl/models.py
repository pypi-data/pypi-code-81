from __future__ import annotations

import os
import enum
import random

from typing import Union
from argparse import Namespace
from dataclasses import dataclass


class syntax(enum.Enum):
    null = ""
    ahk = "autohotkey"
    bash = "bash"
    c = "c"
    coffee = "coffee"
    cpp = "cpp"
    cs = "cs"
    css = "css"
    diff = "diff"
    fix = "fix"
    go = "go"
    glsl = "glsl"
    ini = "ini"
    json = "json"
    kotlin = "kotlin"
    less = "less"
    lua = "lua"
    make = "make"
    md = "md"
    ml = "ml"
    nginx = "nginx"
    php = "php"
    perl = "perl"
    prolog = "prolog"
    python = "python"
    py = "py"
    java = "java"
    js = "js"
    r = "r"
    repl = "python-repl"
    rust = "rust"
    ruby = "ruby"
    scss = "scss"
    sql = "sql"
    swift = "swift"
    tex = "tex"
    ts = "ts"
    vb = "v"
    xl = "xl"
    xml = "xml"
    yaml = "yaml"

    def __str__(self):
        return self.value

    def __repr__(self):
        return "<%s.\033[1m%s\033[0m>" % (
            self.__class__.__name__, self._name_)

    @classmethod
    def __contains__(cls, m):
        return m in [str(s) for s in cls.__members__.values()]

    @classmethod
    def view(cls):
        return "\n".join(sorted([repr(s) for s in set(cls.__members__.values())]))


@dataclass
class Bounded:
    min: Union[int, float]
    max: Union[int, float]

    def check(self) -> None:
        assert self.min <= self.max


@dataclass
class Area(Bounded):

    def __init__(self, min: int = 5, max: int = 1950):
        super().__init__(min, max)

    def check(self) -> None:
        super().check()
        assert self.max <= 1985


@dataclass
class Columns(Bounded):

    def __init__(self, min: int = 40, max: int = 100):
        super().__init__(min, max)


@dataclass
class Rate(Bounded):

    def __init__(self, min: float = 0.8, max: float = 1.0):
        super().__init__(min, max)

    def limit(self) -> float:
        return random.uniform(self.min, self.max)

    def check(self) -> None:
        super().check()
        assert self.min >= 0.8


class Settings(Namespace):
    def __init__(
            self,
            media: os.PathLike,
            token: str,
            channel: int,
            highlight: syntax = None,
            inverted: bool = False,
            min_cols: int = 40,
            max_cols: int = 100,
            min_area: int = 1,
            max_area: int = 1950,
            min_rate: float = 0.8,
            max_rate: float = 1.0) -> None:

        highlight = highlight or syntax.null
        cols = Columns(int(min_cols), int(max_cols))
        area = Area(int(min_area), int(max_area))
        rate = Rate(float(min_rate), float(max_rate))
        cols.check()
        area.check()
        rate.check()

        setattr(self, "media", str(media))
        setattr(self, "token", str(token))
        setattr(self, "channel", int(channel))
        setattr(self, "highlight", str(highlight))
        setattr(self, "inverted", bool(inverted))
        setattr(self, "cols", cols)
        setattr(self, "area", area)
        setattr(self, "rate", rate)

    def check(self):
        m = getattr(self, "media")
        s = getattr(self, "highlight")
        c = getattr(self, "cols")
        a = getattr(self, "area")
        r = getattr(self, "rate")

        assert os.path.exists(str(m))
        assert syntax.__contains__(str(s))
        c.check()
        a.check()
        r.check()

        return self

    def __eq__(self, other: Settings):
        return vars(self) == vars(other)

    def __contains__(self, key):
        return key in self.__dict__

#!/usr/bin/env python3
"""Command line tool that prevents the computer from sleeping while the
script is running.
"""

import platform
import sys
from argparse import ArgumentParser

from adrenaline import adrenaline


def decorate(text: str):
    # Linux and macOS terminals support emojis
    decoration = "\u2728" if platform.system() != "Windows" else ">"
    lines = text.strip().split("\n")
    for index, line in enumerate(lines):
        print(f"   {line}" if index else f"{decoration} {line}")


def main():
    parser = ArgumentParser(description=sys.modules[__name__].__doc__)

    parser.add_argument(
        "--display",
        action="store_true",
        default=False,
        help="forces the display to stay on as well",
    )

    options = parser.parse_args()

    decoration = ""
    indentation = ""

    with adrenaline(display=options.display):
        message = "Sleep mode inhibited."
        if options.display:
            message += " The display is also forced to stay on."

        decorate(f"{message}\nPress Enter to quit.")
        try:
            input()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()

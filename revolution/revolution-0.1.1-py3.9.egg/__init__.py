import argparse
import os
import platform

from .revolution import Revolution
from .visual_example import VisualExample
from .__version__ import (
    __title__, __version__, __author__, __author_email__,
    __description__, __url__, __license__, __copyright__,
)


def show_visual():
    ve = VisualExample()
    ve.start()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-e', '--example', help='displays an animation of all available spinners', action='store_true')
    args = parser.parse_args()

    if args.example:
        if platform.system() == 'Windows':
            os.system('color')
        show_visual()


if __name__ == '__main__':
    main()

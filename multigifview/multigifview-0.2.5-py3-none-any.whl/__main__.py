#!/usr/bin/env python3

import argparse

from Qt.QtWidgets import QApplication
import sys

from .core import MultiGifView


def show_gifs(*filenames, max_columns=2, titles=True):
    """Show gifs in a Qt window

    Any number of gifs can be opened. Each will be in a new column until there are
    max_columns columns. After that new rows will be created and filled until all the
    gifs are shown.

    Parameters
    ----------
    *args - list of str or pathlib.Path
        The .gif files to open
    max_columns : int, default 2
        Maximum number of columns to use
    """
    app = QApplication(sys.argv)
    window = MultiGifView(filenames, max_columns=max_columns, titles=titles)
    window.show()
    window.reset_minimum_size()

    return app.exec_()


def main():
    """Simple gif viewer.

    Commands:
    play - space;
    previous frame - p or left-arrow;
    next frame - n or right-arrow;
    beginning - b or up arrow;
    end - e or down arrow;
    quit - q, Ctrl-q, Ctrl-w or Ctrl-x.
    """
    # Make sure application exits on Ctrl-C
    import signal

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Use argparse to add help
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("file", nargs="+", help=".gif files to open")
    parser.add_argument(
        "-c",
        "--max-columns",
        help="maximum number of columns to use (default 2)",
        type=int,
        default=2,
    )
    parser.add_argument(
        "-n",
        "--no-titles",
        action="store_true",
        default=False,
        help="Disable titles above gifs",
    )
    from multigifview import __version__

    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s {}".format(__version__)
    )
    args = parser.parse_args()

    exit_code = show_gifs(
        *args.file, max_columns=args.max_columns, titles=not args.no_titles
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()

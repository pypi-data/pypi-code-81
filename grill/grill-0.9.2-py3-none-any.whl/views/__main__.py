"""Convenient way to load usdview without any stage. This might be removed if usdview supports it itself!"""
import sys
import signal
import tempfile
import pxr.Usdviewq as Usdviewq

from pxr import Usd
from pathlib import Path
from PySide2 import QtWebEngine

# Let Ctrl-C kill the app.
signal.signal(signal.SIGINT, signal.SIG_DFL)

# This must be called before launching an app!
QtWebEngine.QtWebEngine.initialize()


class Launcher(Usdviewq.Launcher):
    def RegisterPositionals(self, parser):
        """Bypass the original `usdFile` requirement as The Grill creates a new stage if none is provided"""

    def ParseOptions(self, parser):
        """we don't have a usdFile, which is later needed for window title."""
        result = parser.parse_args()
        result.usdFile = result.identifier
        return result

    def RegisterOptions(self, parser):
        """Register optional arguments on the ArgParser"""
        stage = Usd.Stage.CreateInMemory()
        root = stage.GetRootLayer()
        if not root.realPath:
            rootdir = tempfile.mkdtemp()
            default = str(Path(rootdir) / "test.usdc")
            root.Export(default)
        else:
            default = root.realPath
        parser.add_argument('--identifier', action='store',
                            type=str, dest='identifier',
                            help="Identifier of the USD layer to open a stage for.",
                            default=default)
        return super().RegisterOptions(parser)


def main():
    try:
        Launcher().Run()
    except Usdviewq.InvalidUsdviewOption as e:
        print("ERROR: " + e.message, file=sys.stderr)
        sys.exit(1)

main()

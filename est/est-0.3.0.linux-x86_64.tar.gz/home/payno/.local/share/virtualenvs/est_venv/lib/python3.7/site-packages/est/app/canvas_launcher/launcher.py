from silx.gui import qt
from Orange.canvas import __main__ as main

try:
    from orangecanvas import config
except ImportError:
    from Orange.canvas import config

    old_config = True
else:
    old_config = False
from .splash import splash_screen, getIcon
import os, sys
from Orange.misc import environ
import pkg_resources


def version():
    return pkg_resources.get_distribution("est").version


if old_config:

    class EstConfig(config.Config):
        ApplicationName = "est"
        ApplicationVersion = version()

        @staticmethod
        def splash_screen():
            return splash_screen()

        @staticmethod
        def core_packages():
            return super(EstConfig, EstConfig).core_packages() + ["est-add-on"]

        @staticmethod
        def application_icon(self):
            return getIcon()


else:

    class EstConfig(config.Config):
        ApplicationName = "est"
        ApplicationVersion = version()

        def splash_screen(self):
            return splash_screen()

        def core_packages(self):
            return super(EstConfig, EstConfig).core_packages() + ["est-add-on"]

        def application_icon(self):
            return getIcon()


class EstSplashScreen(qt.QSplashScreen):
    """SplashScreen to overwrite the one of Orange"""

    def __init__(
        self,
        parent=None,
        pixmap=None,
        textRect=None,
        textFormat=qt.Qt.PlainText,
        **kwargs
    ):
        qt.QSplashScreen.__init__(self, parent, pixmap=pixmap, **kwargs)

    def showMessage(self, message, alignment=qt.Qt.AlignLeft, color=qt.Qt.black):
        super().showMessage(
            version(), qt.Qt.AlignCenter | qt.Qt.AlignBottom, qt.QColor("#e68f17")
        )


class Launcher:
    """Proxy to orange-canvas"""

    def launch(self, argv):
        config.Config = EstConfig
        self.fix_application_dirs()
        self.replace_splash_screen()
        self.main(argv)

    def fix_application_dirs(self):
        def data_dir(versioned=True):
            """
            Return the platform dependent Orange data directory.

            This is ``data_dir_base()``/Orange/__VERSION__/ directory if versioned is
            `True` and ``data_dir_base()``/Orange/ otherwise.
            """
            base = environ.data_dir_base()
            if versioned:
                return os.path.join(base, "est", version())
            else:
                return os.path.join(base, "est")

        environ.data_dir = data_dir

        def cache_dir(*args):
            """
            Return the platform dependent Orange cache directory.
            """
            if sys.platform == "darwin":
                base = os.path.expanduser("~/Library/Caches")
            elif sys.platform == "win32":
                base = os.getenv("APPDATA", os.path.expanduser("~/AppData/Local"))
            elif os.name == "posix":
                base = os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
            else:
                base = os.path.expanduser("~/.cache")

            base = os.path.join(base, "est", version())
            if sys.platform == "win32":
                # On Windows cache and data dir are the same.
                # Microsoft suggest using a Cache subdirectory
                return os.path.join(base, "Cache")
            else:
                return base

        environ.cache_dir = cache_dir

    def replace_splash_screen(self):
        main.SplashScreen = EstSplashScreen

    def main(self, argv):
        from Orange.canvas.__main__ import main

        main(argv)

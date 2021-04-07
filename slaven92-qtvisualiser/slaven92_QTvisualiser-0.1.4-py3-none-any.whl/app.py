from PyQt5.QtWidgets import QApplication

from .controllers import MainController
from .views import mainWindow

class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.widget = mainWindow()
        self.widget.show()
        self.con = MainController(self.widget)
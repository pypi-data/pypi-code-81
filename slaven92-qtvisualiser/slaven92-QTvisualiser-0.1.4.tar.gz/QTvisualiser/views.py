import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from pyqtgraph.graphicsItems.PlotItem import PlotItem
from pyqtgraph.imageview import ImageView


class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.load_ui()
        self.mainWindow_setup()


    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        uic.loadUi(path, self)

    def mainWindow_setup(self):
         self.setWindowTitle("ploting the crosssections")


# same as ImageView but with coordinates
class myImageView(ImageView):
    def __init__(self, *args, **kwargs):
        super().__init__(view=PlotItem(), *args, **kwargs)
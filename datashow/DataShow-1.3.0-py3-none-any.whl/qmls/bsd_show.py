import os
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget
from PyQt5.QtQuickWidgets import QQuickWidget


class BsdWidget(QWidget):
    def __init__(self, paren=None):
        super(BsdWidget, self).__init__()

        self._addQML()

    def _addQML(self):
        self.qml_widget = QQuickWidget(self)
        self.qml_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)

        DIR_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        qml_path = os.path.join(DIR_PATH, "qmls", "bsd_show.qml")
        self.qml_widget.setSource(QUrl.fromLocalFile(qml_path))
        self.qml_widget.show()
        self.root_obj = self.qml_widget.rootObject()
   
# -*- coding: utf-8 -*-

"""
This widget will display the contents of Camera
"""

# @File  : cam_widget.py
# @Author: Andy.yang
# @Date  : 2021/02/22
# @Software: VS Code


from PyQt5.QtWidgets import QWidget
from ..ui.cam_ui import Ui_dlg_cam

class CamWidget(Ui_dlg_cam, QWidget):
    def __init__(self, parent=None):
        super(CamWidget, self).__init__(parent)
        self.setupUi(self)

        self.setAutoFillBackground(True)

    def showCam(pho)
    {
        
    }
# -*- coding:utf-8 -*-
"""
The entry of this software
"""

# @File  : DataReplay_gui.py
# @Author: Andy.yang
# @Date  : 2021/02/22
# @Software: VS Code

import sys
import ctypes

from PyQt5.QtWidgets import QApplication

from DataReplay.widgets.sim_widget import SimWidget

# The line below will show
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")


def main():
    app = QApplication(sys.argv)
    win = SimWidget()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
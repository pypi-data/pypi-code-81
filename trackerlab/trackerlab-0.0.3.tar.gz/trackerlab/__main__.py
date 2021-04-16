# -*- coding: utf-8 -*-

"""
Discription: TrackLab of the Molecular Nanophotonics.
Author(s): M. Fränzl, N. Söker
Data: 18/09/18
"""

import sys
from PyQt5.QtWidgets import QApplication

from trackerlab import app
    
if __name__ == '__main__':
    a = QApplication(sys.argv)
    window = app.MainWindow()
    window.show()
    sys.exit(a.exec_())
    
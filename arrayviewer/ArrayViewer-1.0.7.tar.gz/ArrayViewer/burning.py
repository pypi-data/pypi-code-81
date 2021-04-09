import sys
from PyQt4 import QtGui


class RangeSlider(QtGui.QHBoxLayout):
    def __init__(self, parent=None, minmax=[0, 1]):
        super(RangeSlider, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.items = []

        self.steps = 80
        self.offset = 21
        self.sca = 1.0 * (minmax[1] - minmax[0]) / self.steps
        self.minSlide = QtGui.QSlider()
        self.maxSlide = QtGui.QSlider(self.minSlide)
        self.minSlide.setRange(0, self.steps)
        self.maxSlide.setRange(0, self.steps)
        self.minSlide.setSliderPosition(0)
        self.maxSlide.setSliderPosition(self.steps)
        self.minSlide.setSingleStep(1)
        self.maxSlide.setSingleStep(1)
        self.minSlide.setTickInterval(self.steps / 10)
        self.maxSlide.setTickInterval(self.steps / 10)
        self.minSlide.valueChanged.connect(self.minRestict)
#        self.css = "QSlider {}"
#        self.minSlide.setStyleSheet(self.css)
#        self.maxSlide.setStyleSheet(self.css)
        self.rHeight = self.minSlide.geometry().height()

        self.lower = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
        self.lower.addWidget(self.minSlide)
        self.upper = QtGui.QBoxLayout(QtGui.QBoxLayout.TopToBottom)
        self.upper.addWidget(self.maxSlide)
        self.addLayout(self.lower)
        self.addLayout(self.upper)

    def minRestict(self, value):
        if value > self.maxSlide.value():
            self.minSlide.setSliderPosition(self.maxSlide.value())
            value = self.minSlide.value()

        fraction = 1.0 * (self.steps - value) / self.steps
        max_height = self.minSlide.geometry().height() - self.offset
        self.rHeight = max_height * fraction + self.offset - 15
        self.maxSlide.resize(18, self.rHeight)
        self.maxSlide.setRange(value, self.steps)

    def addLayout(self, layout):
        self.addChildLayout(layout)
        self.addItem(layout)
#        widget.setStyleSheet(self.css)

    def addItem(self, item):
        self.items.append(item)

    def setGeometry(self, rect):
        super(RangeSlider, self).setGeometry(rect)
        self.lower.setGeometry(rect)
        self.upper.setGeometry(rect)
        self.minRestict(self.minSlide.value())

    def itemAt(self, index):
        """Return the item at the given index."""
        if index >= 0 and index < len(self.items):
            return self.items[index]
        return None

    def count(self):
        return len(self.items)

    def value(self):
        return (self.minSlide.value() * self.sca,
                self.maxSlide.value() * self.sca)


class rangeSlider2(QtGui.QHBoxLayout):
    def __init__(self, parent=None, minmax=[0, 1]):
        super(rangeSlider2, self).__init__(parent)
        self.steps = 80
        self.items = []
        self.sca = 1.0 * (minmax[1] - minmax[0]) / self.steps
        self.setContentsMargins(0, 0, 0, 0)
        self.minSlide = QtGui.QSlider()
        self.maxSlide = QtGui.QSlider(self.minSlide)
        self.minSlide.setRange(0, self.steps)
        self.maxSlide.setRange(0, self.steps)
        self.minSlide.setTickPosition(self.minSlide.TicksLeft)
        self.minSlide.setSliderPosition(0)
        self.maxSlide.setSliderPosition(self.steps)
        self.minSlide.setSingleStep(1)
        self.maxSlide.setSingleStep(1)
        self.minSlide.setTickInterval(self.steps / 10)
        self.maxSlide.setTickInterval(self.steps / 10)
        self.minSlide.valueChanged.connect(self.minRestict)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.minSlide)
        self.addLayout(layout)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.maxSlide)
        self.addLayout(layout)

    def addItem(self, item):
        self.items.append(item)

    def itemAt(self, index):
        if index >= 0 and index < len(self.items):
            return self.items[index]
        return None

    def addLayout(self, layout):
        self.addChildLayout(layout)
        self.addItem(layout)

    def value(self):
        return (self.minSlide.value() * self.sca,
                self.maxSlide.value() * self.sca)

    def minRestict(self, value):
        if value > self.maxSlide.value():
            self.minSlide.setSliderPosition(self.maxSlide.value())
            value = self.minSlide.value()
        offset = 21
        fraction = 1.0 * (self.steps - value) / self.steps
        max_height = self.minSlide.geometry().height() - offset
        self.maxSlide.resize(18, max_height * fraction + offset)
        self.maxSlide.setRange(value, self.steps)

    def setGeometry(self, rect):
        super(rangeSlider2, self).setGeometry(rect)
        for item in self.items:
            item.setGeometry(rect)


class ViewerWindow(QtGui.QMainWindow):
    """ The main window of the array viewer """
    def __init__(self, parent=None):
        """ Initialize the window """
        super(self.__class__, self).__init__(parent)
        # General Options
        self.resize(50, 600)
        self.setWindowTitle("")

        CWgt = QtGui.QWidget(self)
        self.setCentralWidget(CWgt)
        QFra = QtGui.QVBoxLayout(CWgt)
        self.rangeSld = RangeSlider()
        QFra.addLayout(self.rangeSld)
        self.pushBtn = QtGui.QPushButton()
        self.pushBtn.released.connect(self.getVal)
        QFra.addWidget(self.pushBtn)

    def getVal(self):
        print(self.rangeSld.value())


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = ViewerWindow()
    window.show()
    app.exec_()

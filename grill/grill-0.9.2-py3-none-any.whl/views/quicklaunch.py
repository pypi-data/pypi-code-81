from PySide2.QtWidgets import QApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QUrl


if __name__ == "__main__":
    app = QApplication([])
    view = QQuickView()
    url = QUrl("quickview.qml")

    view.setSource(url)
    view.show()
    app.exec_()

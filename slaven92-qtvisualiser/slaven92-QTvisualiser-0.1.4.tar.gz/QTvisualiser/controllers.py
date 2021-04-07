from PyQt5.QtWidgets import QFileDialog, QLabel
import numpy as np
import os
from .models import ImgData


class MainController():
    def __init__(self, widget):
        self.widget = widget
        self._create_connections()
        self.data = ImgData()

    
    def _create_connections(self):
        #buttons
        self.widget.pushButton.clicked.connect(self.loadData)

        #connect slider in windows to update
        self.widget.graphicsView.timeLine.sigPositionChanged.connect(self.updateTextWithSliders)
        self.widget.graphicsView_2.timeLine.sigPositionChanged.connect(self.updateTextWithSliders)
        self.widget.graphicsView_3.timeLine.sigPositionChanged.connect(self.updateTextWithSliders)
        self.widget.actionLoad_Test_Data.triggered.connect(self.loadFakeData)


    #slots
    def loadData(self):
        filename = QFileDialog.getOpenFileName()
        self.data.loadData(filename)
        #rename the choose file dialog
        self.widget.lineEdit_4.setText(filename[0])
        self.plotData()

        #update what is slider value
        self.updateTextWithSliders()


    def loadFakeData(self):
        self.data.loadFakeData()
        self.plotData()
        self.updateTextWithSliders()


    def plotData(self):
        posSlice, scaleSlice, imgSlice = self.data.get_slice_parallel()
        self.widget.graphicsView.setImage(imgSlice, pos=posSlice, scale=scaleSlice)

        posPerp, scalePerp, imgPerp = self.data.get_slice_perp()
        self.widget.graphicsView_2.setImage(imgPerp, pos=posPerp, scale=scalePerp)

        posPerp2, scalePerp2, imgPerp2 = self.data.get_slice_perp2()
        self.widget.graphicsView_3.setImage(imgPerp2, pos=posPerp2, scale=scalePerp2)

    def updateTextWithSliders(self):
        z_ind = self.widget.graphicsView.currentIndex
        y_ind = self.widget.graphicsView_2.currentIndex
        x_ind = self.widget.graphicsView_3.currentIndex

        self.widget.lineEdit.setText(f"z={self.data.z[z_ind]}")
        self.widget.lineEdit_3.setText(f"y={self.data.y[y_ind]}")
        self.widget.lineEdit_2.setText(f"x={self.data.x[x_ind]}")
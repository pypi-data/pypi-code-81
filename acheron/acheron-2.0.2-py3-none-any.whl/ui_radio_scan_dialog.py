# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'radio_scan_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_RadioScanDialog(object):
    def setupUi(self, RadioScanDialog):
        if not RadioScanDialog.objectName():
            RadioScanDialog.setObjectName(u"RadioScanDialog")
        RadioScanDialog.resize(1000, 445)
        self.verticalLayout = QVBoxLayout(RadioScanDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableView = QTableView(RadioScanDialog)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableView.setSortingEnabled(True)
        self.tableView.setCornerButtonEnabled(False)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.verticalHeader().setVisible(False)

        self.verticalLayout.addWidget(self.tableView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.activeScan = QCheckBox(RadioScanDialog)
        self.activeScan.setObjectName(u"activeScan")

        self.horizontalLayout.addWidget(self.activeScan)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.filterLabel = QLabel(RadioScanDialog)
        self.filterLabel.setObjectName(u"filterLabel")

        self.horizontalLayout.addWidget(self.filterLabel)

        self.filterSlider = QSlider(RadioScanDialog)
        self.filterSlider.setObjectName(u"filterSlider")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filterSlider.sizePolicy().hasHeightForWidth())
        self.filterSlider.setSizePolicy(sizePolicy)
        self.filterSlider.setMinimumSize(QSize(200, 0))
        self.filterSlider.setMinimum(-100)
        self.filterSlider.setMaximum(0)
        self.filterSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.filterSlider)

        self.filterSpinBox = QSpinBox(RadioScanDialog)
        self.filterSpinBox.setObjectName(u"filterSpinBox")
        self.filterSpinBox.setMinimum(-100)
        self.filterSpinBox.setMaximum(0)

        self.horizontalLayout.addWidget(self.filterSpinBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(RadioScanDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.Reset)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(RadioScanDialog)
        self.buttonBox.accepted.connect(RadioScanDialog.accept)
        self.buttonBox.rejected.connect(RadioScanDialog.reject)
        self.filterSlider.valueChanged.connect(self.filterSpinBox.setValue)
        self.filterSpinBox.valueChanged.connect(self.filterSlider.setValue)

        QMetaObject.connectSlotsByName(RadioScanDialog)
    # setupUi

    def retranslateUi(self, RadioScanDialog):
        RadioScanDialog.setWindowTitle(QCoreApplication.translate("RadioScanDialog", u"Radio Scan", None))
        self.activeScan.setText(QCoreApplication.translate("RadioScanDialog", u"Active Scan", None))
        self.filterLabel.setText(QCoreApplication.translate("RadioScanDialog", u"Filter", None))
        self.filterSpinBox.setSuffix(QCoreApplication.translate("RadioScanDialog", u" dBm", None))
    # retranslateUi


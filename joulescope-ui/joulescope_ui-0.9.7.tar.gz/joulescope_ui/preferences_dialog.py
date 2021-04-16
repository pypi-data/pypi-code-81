# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preferences_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_PreferencesDialog(object):
    def setupUi(self, PreferencesDialog):
        if not PreferencesDialog.objectName():
            PreferencesDialog.setObjectName(u"PreferencesDialog")
        PreferencesDialog.resize(660, 388)
        PreferencesDialog.setModal(True)
        self.dialogLayout = QVBoxLayout(PreferencesDialog)
        self.dialogLayout.setObjectName(u"dialogLayout")
        self.profileWidget = QWidget(PreferencesDialog)
        self.profileWidget.setObjectName(u"profileWidget")
        self.profileLayout = QHBoxLayout(self.profileWidget)
        self.profileLayout.setObjectName(u"profileLayout")
        self.profileLabel = QLabel(self.profileWidget)
        self.profileLabel.setObjectName(u"profileLabel")

        self.profileLayout.addWidget(self.profileLabel)

        self.profileComboBox = QComboBox(self.profileWidget)
        self.profileComboBox.setObjectName(u"profileComboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.profileComboBox.sizePolicy().hasHeightForWidth())
        self.profileComboBox.setSizePolicy(sizePolicy)

        self.profileLayout.addWidget(self.profileComboBox)

        self.profileActivateButton = QPushButton(self.profileWidget)
        self.profileActivateButton.setObjectName(u"profileActivateButton")

        self.profileLayout.addWidget(self.profileActivateButton)

        self.profileResetButton = QPushButton(self.profileWidget)
        self.profileResetButton.setObjectName(u"profileResetButton")

        self.profileLayout.addWidget(self.profileResetButton)

        self.profileNewButton = QPushButton(self.profileWidget)
        self.profileNewButton.setObjectName(u"profileNewButton")

        self.profileLayout.addWidget(self.profileNewButton)

        self.profileSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.profileLayout.addItem(self.profileSpacer)

        self.helpButton = QPushButton(self.profileWidget)
        self.helpButton.setObjectName(u"helpButton")

        self.profileLayout.addWidget(self.helpButton)


        self.dialogLayout.addWidget(self.profileWidget)

        self.centerWidget = QWidget(PreferencesDialog)
        self.centerWidget.setObjectName(u"centerWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centerWidget.sizePolicy().hasHeightForWidth())
        self.centerWidget.setSizePolicy(sizePolicy1)
        self.centerLayout = QHBoxLayout(self.centerWidget)
        self.centerLayout.setObjectName(u"centerLayout")
        self.treeView = QTreeView(self.centerWidget)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setAnimated(True)
        self.treeView.header().setVisible(False)

        self.centerLayout.addWidget(self.treeView)

        self.scrollArea = QScrollArea(self.centerWidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.targetWidget = QWidget()
        self.targetWidget.setObjectName(u"targetWidget")
        self.targetWidget.setGeometry(QRect(0, 0, 307, 254))
        self.targetLayout = QVBoxLayout(self.targetWidget)
        self.targetLayout.setObjectName(u"targetLayout")
        self.scrollArea.setWidget(self.targetWidget)

        self.centerLayout.addWidget(self.scrollArea)


        self.dialogLayout.addWidget(self.centerWidget)

        self.buttonFrame = QFrame(PreferencesDialog)
        self.buttonFrame.setObjectName(u"buttonFrame")
        self.buttonFrame.setFrameShape(QFrame.StyledPanel)
        self.buttonFrame.setFrameShadow(QFrame.Raised)
        self.buttonLayout = QHBoxLayout(self.buttonFrame)
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.buttonSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.buttonLayout.addItem(self.buttonSpacer)

        self.resetButton = QPushButton(self.buttonFrame)
        self.resetButton.setObjectName(u"resetButton")

        self.buttonLayout.addWidget(self.resetButton)

        self.cancelButton = QPushButton(self.buttonFrame)
        self.cancelButton.setObjectName(u"cancelButton")

        self.buttonLayout.addWidget(self.cancelButton)

        self.okButton = QPushButton(self.buttonFrame)
        self.okButton.setObjectName(u"okButton")

        self.buttonLayout.addWidget(self.okButton)


        self.dialogLayout.addWidget(self.buttonFrame)


        self.retranslateUi(PreferencesDialog)

        QMetaObject.connectSlotsByName(PreferencesDialog)
    # setupUi

    def retranslateUi(self, PreferencesDialog):
        PreferencesDialog.setWindowTitle(QCoreApplication.translate("PreferencesDialog", u"Preferences", None))
        self.profileLabel.setText(QCoreApplication.translate("PreferencesDialog", u"Profile", None))
#if QT_CONFIG(tooltip)
        self.profileComboBox.setToolTip(QCoreApplication.translate("PreferencesDialog", u"Select the profile to view and edit.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.profileActivateButton.setToolTip(QCoreApplication.translate("PreferencesDialog", u"<html><head></head>\n"
"<body>\n"
"<p><b>Activate the selected profile.</b></p>\n"
"<p>This action updates Joulescope UI to use the preferences in the selected profile.</p>\n"
"</body>\n"
"</html>", None))
#endif // QT_CONFIG(tooltip)
        self.profileActivateButton.setText(QCoreApplication.translate("PreferencesDialog", u"Activate", None))
#if QT_CONFIG(tooltip)
        self.profileResetButton.setToolTip(QCoreApplication.translate("PreferencesDialog", u"<html><head/>\n"
"<body><p><b>Reset or erase the selected profile.</b></p>\n"
"<p>For the built-in profiles, <b>Reset</b> the profile to the factory defaults.  For custom profiles, <b>Erase</b> the profile so that it is no longer available.  You cannot erase the built-in profiles.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.profileResetButton.setText(QCoreApplication.translate("PreferencesDialog", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.profileNewButton.setToolTip(QCoreApplication.translate("PreferencesDialog", u"<html>\n"
"<head></head>\n"
"<body>\n"
"<p>Create a new custom profile.</p>\n"
"</body>\n"
"</html>", None))
#endif // QT_CONFIG(tooltip)
        self.profileNewButton.setText(QCoreApplication.translate("PreferencesDialog", u"New", None))
        self.helpButton.setText(QCoreApplication.translate("PreferencesDialog", u"Help", None))
#if QT_CONFIG(tooltip)
        self.treeView.setToolTip(QCoreApplication.translate("PreferencesDialog", u"Select the Preferences Group to display.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.scrollArea.setToolTip(QCoreApplication.translate("PreferencesDialog", u"View and edit the Preferences for the selected Profile and Preference Group.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.resetButton.setToolTip(QCoreApplication.translate("PreferencesDialog", u"<html><head/><body><p><span style=\" font-weight:600;\">Reset the Preferences for the selected Profile and Preferences Group.</span></p><p>This button only resets the Preferences that are currently shown in the right-hand side, and only for the selected Profile.  All other preference values are not changed.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.resetButton.setText(QCoreApplication.translate("PreferencesDialog", u"Reset to Defaults", None))
        self.cancelButton.setText(QCoreApplication.translate("PreferencesDialog", u"Cancel", None))
        self.okButton.setText(QCoreApplication.translate("PreferencesDialog", u"OK", None))
    # retranslateUi


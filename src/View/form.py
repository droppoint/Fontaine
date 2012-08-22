# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Python27\convert\form.ui'
#
# Created: Mon Aug 13 13:35:51 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(320, 270)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(320, 270))
        Form.setMaximumSize(QtCore.QSize(320, 270))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/fontaine/icons/fontaine_icon(32).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(120, 230, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(Form.close)
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(90, 10, 128, 128))
        self.label.setMaximumSize(QtCore.QSize(128, 128))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/fontaine/images/fontaine_icon(128).png"))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(80, 160, 139, 16))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(80, 178, 139, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(80, 196, 108, 16))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "О программе", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Fontaine v0.76", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Powered by PySide & Python", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Alexei Partilov @ 2012", None, QtGui.QApplication.UnicodeUTF8))

import res

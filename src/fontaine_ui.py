# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fontaine.ui'
#
# Created: Sun Apr  8 12:42:10 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(430, 240)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(310, 40, 100, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.setOpenFileName)
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 270, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setReadOnly(True)
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 180, 130, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 15, 180, 20))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 180, 20))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 105, 270, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setReadOnly(True)
        self.debug = QtGui.QCheckBox('Debug', self.centralwidget)
        self.debug.setGeometry(QtCore.QRect(20, 150, 100, 15))
        self.debug.setObjectName("debug")
        self.tracks = QtGui.QCheckBox('Side tracks', self.centralwidget)
        self.tracks.setGeometry(QtCore.QRect(120, 150, 100, 15))
        self.tracks.setObjectName("tracks")
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(310, 105, 100, 25))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.setFileName)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 428, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.native = QtGui.QCheckBox()
        self.native.setText("Use native file dialog.")
        self.native.setChecked(True)
        if sys.platform not in ("win32", "darwin"):
            self.native.hide()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QtGui.QApplication.translate("MainWindow", "Fontaine", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(
            QtGui.QApplication.translate("MainWindow", "Обзор", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.pushButton_3.setText(
            QtGui.QApplication.translate("MainWindow", "Обзор", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(
            QtGui.QApplication.translate("MainWindow", "Преобразовать", None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.label.setText(
            QtGui.QApplication.translate("MainWindow", "Выберите файл  *.rsm",
                                         None,
                                         QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(
            QtGui.QApplication.translate("MainWindow",
                                         "Выберите файл категории запасов",
                                         None,
                                         QtGui.QApplication.UnicodeUTF8))

    def setOpenFileName(self):
        options = QtGui.QFileDialog.Options()
        if not self.native.isChecked():
            options |= QtGui.QFileDialog.DontUseNativeDialog
        fileName, unused_filtr = QtGui.QFileDialog.getOpenFileName(
                    self.pushButton,
                    u"Открыть",
                    "",
                    "Eclipse RSM File (*.rsm);;All Files (*)",
                    "",
                    options)
        if fileName:
            self.lineEdit.setText(fileName)

    def setFileName(self):
        options = QtGui.QFileDialog.Options()
        if not self.native.isChecked():
            options |= QtGui.QFileDialog.DontUseNativeDialog
        fileName, unused_filtr = QtGui.QFileDialog.getOpenFileName(
                    self.pushButton,
                    u"Открыть",
                    "",
                    "All Files (*)",
                    "",
                    options)
        if fileName:
            self.lineEdit_2.setText(fileName)

    def setSaveFileName(self):
        options = QtGui.QFileDialog.Options()
        if not self.native.isChecked():
            options |= QtGui.QFileDialog.DontUseNativeDialog
        fileName, unused_ok = QtGui.QFileDialog.getSaveFileName(
                self.pushButton_2,
                u"Сохранить",
                "",
                "Excel File (*.xls);;All Files (*)", "", options)
        if fileName:
            return fileName

    def informationMessage(self, message, caption="Fontaine"):
        reply = QtGui.QMessageBox.information(self.pushButton_2,
                caption, message)

#        if reply == QtGui.QMessageBox.Ok:
#            self.informationLabel.setText("OK")
#        else:
#            self.informationLabel.setText("Escape")

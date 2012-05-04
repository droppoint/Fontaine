# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fontaine.ui'
#
# Created: Sun Apr  8 12:42:10 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys
#from First import parseData


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(430, 240)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(310, 80, 98, 27))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.setOpenFileName)
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 80, 271, 27))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setReadOnly(True)
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 140, 131, 27))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 35, 181, 17))
        self.label.setObjectName("label")
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
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Fontaine", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Обзор", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Преобразовать", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Выберите файл  *.rsm", None, QtGui.QApplication.UnicodeUTF8))
        
    def setOpenFileName(self):    
        options = QtGui.QFileDialog.Options()
        if not self.native.isChecked():
            options |= QtGui.QFileDialog.DontUseNativeDialog
        fileName, filtr = QtGui.QFileDialog.getOpenFileName(self.pushButton, 
                    u"Открыть",
                    "",
                    "Eclipse RSM File (*.rsm);;All Files (*)","",options)
        if fileName:
            self.lineEdit.setText(fileName)
            
    def setSaveFileName(self):    
        options = QtGui.QFileDialog.Options()
        if not self.native.isChecked():
            options |= QtGui.QFileDialog.DontUseNativeDialog
        fileName, ok = QtGui.QFileDialog.getSaveFileName(self.pushButton_2,
                u"Сохранить",
                "",
                "Excel File (*.xls);;All Files (*)", "", options)
        if fileName:
            return fileName
        
    
    def informationMessage(self, message):    
        reply = QtGui.QMessageBox.information(self.pushButton_2,
                u"QMessageBox.information()", message)

#        if reply == QtGui.QMessageBox.Ok:
#            self.informationLabel.setText("OK")
#        else:
#            self.informationLabel.setText("Escape")
            
        

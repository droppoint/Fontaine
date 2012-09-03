# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Python27\convert\mainwindow.ui'
#
# Created: Mon Aug 13 13:35:04 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys
import res
import dialog
import form


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(320, 175)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(320, 175))
        MainWindow.setMaximumSize(QtCore.QSize(320, 175))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/fontaine/icons/fontaine_icon(32).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.lineEdit = QtGui.QLineEdit(self.centralWidget)
        self.lineEdit.setGeometry(QtCore.QRect(14, 40, 261, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtGui.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(14, 20, 141, 16))
        self.label.setObjectName("label")
        self.pushButton_2 = QtGui.QPushButton(self.centralWidget)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 90, 121, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.toolButton = QtGui.QToolButton(self.centralWidget)
        self.toolButton.setGeometry(QtCore.QRect(284, 40, 21, 21))
        self.toolButton.setObjectName("toolButton")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 320, 20))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtGui.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtGui.QMenu(self.menuBar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.action = QtGui.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtGui.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_2.setEnabled(False)
        self.action_3 = QtGui.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_5 = QtGui.QAction(MainWindow)
        self.action_5.setObjectName("action_5")
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action_3)
        self.menu.addSeparator()
        self.menu.addAction(self.action_5)
        self.menu_2.addAction(self.action)
        self.menuBar.addAction(self.menu.menuAction())
        self.menuBar.addAction(self.menu_2.menuAction())
        self.action_3.triggered.connect(self.openPrefencesWindow)
        self.native = QtGui.QCheckBox()
        self.native.setText("Use native file dialog.")
        self.native.setChecked(True)
        if sys.platform not in ("win32", "darwin"):
            self.native.hide()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Fontaine", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Выберите файл *.rsm", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Преобразовать", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.setTitle(QtGui.QApplication.translate("MainWindow", "Файл", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_2.setTitle(QtGui.QApplication.translate("MainWindow", "Справка", None, QtGui.QApplication.UnicodeUTF8))
        self.action.setText(QtGui.QApplication.translate("MainWindow", "О программе", None, QtGui.QApplication.UnicodeUTF8))
        self.action_2.setText(QtGui.QApplication.translate("MainWindow", "Открыть файл ограничений", None, QtGui.QApplication.UnicodeUTF8))
        self.action_3.setText(QtGui.QApplication.translate("MainWindow", "Настройки", None, QtGui.QApplication.UnicodeUTF8))
        self.action_5.setText(QtGui.QApplication.translate("MainWindow", "Выход", None, QtGui.QApplication.UnicodeUTF8))

    def openPrefencesWindow(self):
        self.prefences.show()

    def acceptPrefences(self):
        self.prefences_values = self.prefences.get_prefences()
        self.debug = self.prefences.get_debug()
        self.lateral = self.prefences.get_lateral()

    def rejectPrefences(self):
        self.prefences.set_prefences(self.prefences_values)
        self.prefences.set_debug(self.debug)
        self.prefences.set_lateral(self.lateral)

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


class ProgressDialog(QtGui.QProgressDialog):
    def __init__(self, parent=None):
        super(ProgressDialog, self).__init__(parent)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/fontaine/icons/fontaine_icon(32).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui = QtGui.QProgressDialog(u"Подготовка отчета...",
                                    u"Отмена", 0, 100)
        self.ui.setWindowIcon(icon)
        self.ui.setWindowTitle(QtGui.QApplication.translate("Progress",
                        "Fontaine", None, QtGui.QApplication.UnicodeUTF8))
        self.ui.setWindowModality(QtCore.Qt.WindowModal)

    def setProgress(self, progress):
        self.ui.show()
        self.ui.setValue(progress)

    def close(self):
        self.ui.cancel()
        self.cancel()


class ConfigurationDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ConfigurationDialog, self).__init__(parent)
        self.ui = dialog.Ui_Dialog()
        self.ui.setupUi(self)

    def get_prefences(self):
        return {'oil_density': self.ui.doubleSpinBox.value(),
                'water_density': self.ui.doubleSpinBox_2.value()}

    def set_prefences(self, prefences):
        self.ui.doubleSpinBox.setProperty("value", prefences['oil_density'])
        self.ui.doubleSpinBox_2.setProperty("value", prefences['water_density'])

    def get_debug(self):
        return self.ui.checkBox.isChecked()

    def set_debug(self, state):
        self.ui.checkBox.setChecked(state)

    def get_lateral(self):
        return self.ui.checkBox_2.isChecked()

    def set_lateral(self, state):
        self.ui.checkBox_2.setChecked(state)

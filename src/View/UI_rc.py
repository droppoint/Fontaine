# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file
# 'C:\Python27\convert\mainwindow.ui'
#
# Created: Mon Aug 13 13:35:04 2012
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys
import res


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(320, 175)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                       QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
                    MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(320, 175))
        MainWindow.setMaximumSize(QtCore.QSize(320, 175))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/fontaine/icons/fontaine_icon(32).png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
#        self.action_2.setEnabled(False)
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
        self.native = QtGui.QCheckBox()
        self.native.setText("Use native file dialog.")
        self.native.setChecked(True)
        if sys.platform not in ("win32", "darwin"):
            self.native.hide()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow",
                "Fontaine", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow",
                "Выберите файл *.rsm", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow",
                "Преобразовать", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("MainWindow",
                "...", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.setTitle(QtGui.QApplication.translate("MainWindow",
                "Файл", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_2.setTitle(QtGui.QApplication.translate("MainWindow",
                "Справка", None, QtGui.QApplication.UnicodeUTF8))
        self.action.setText(QtGui.QApplication.translate("MainWindow",
                "О программе", None, QtGui.QApplication.UnicodeUTF8))
        self.action_2.setText(QtGui.QApplication.translate("MainWindow",
                "Открыть файл ограничений", None,
                QtGui.QApplication.UnicodeUTF8))
        self.action_3.setText(QtGui.QApplication.translate("MainWindow",
                "Настройки", None, QtGui.QApplication.UnicodeUTF8))
        self.action_5.setText(QtGui.QApplication.translate("MainWindow",
                "Выход", None, QtGui.QApplication.UnicodeUTF8))


class ProgressDialog(QtGui.QProgressDialog):
    def __init__(self, parent=None):
        super(ProgressDialog, self).__init__(parent)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/fontaine/icons/fontaine_icon(32).png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(220, 180)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                       QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(220, 180))
        Dialog.setMaximumSize(QtCore.QSize(220, 180))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/fontaine/icons/fontaine_icon(32).png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 145, 171, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel |
                                          QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 201, 81))
        self.groupBox.setObjectName("groupBox")
        self.widget = QtGui.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(13, 20, 181, 51))
        self.widget.setObjectName("widget")
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(30, 17, QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.widget)
        self.doubleSpinBox.setMaximumSize(QtCore.QSize(60, 20))
        self.doubleSpinBox.setDecimals(1)
        self.doubleSpinBox.setMaximum(10000.0)
        self.doubleSpinBox.setProperty("value", 800.0)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout.addWidget(self.doubleSpinBox, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(34, 17, QtGui.QSizePolicy.Expanding,
                                        QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)
        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(self.widget)
        self.doubleSpinBox_2.setMaximumSize(QtCore.QSize(60, 20))
        self.doubleSpinBox_2.setDecimals(1)
        self.doubleSpinBox_2.setMaximum(10000.0)
        self.doubleSpinBox_2.setProperty("value", 1000.0)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.gridLayout.addWidget(self.doubleSpinBox_2, 1, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 3, 1, 1)
        self.checkBox = QtGui.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(10, 100, 131, 17))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtGui.QCheckBox(Dialog)
        self.checkBox_2.setGeometry(QtCore.QRect(10, 125, 180, 17))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.setChecked(True)

        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog",
                            "Настройки", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog",
                            "Плотность", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog",
                            "Нефть", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog",
                            "кг/м3", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog",
                            "Вода", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog",
                            "кг/м3", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("Dialog",
                            "Включить отладку", None,
                            QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(QtGui.QApplication.translate("Dialog",
                            "Обнаружение боковых стволов", None,
                            QtGui.QApplication.UnicodeUTF8))


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(320, 270)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed,
                                       QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(320, 270))
        Form.setMaximumSize(QtCore.QSize(320, 270))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/fontaine/icons/fontaine_icon(32).png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(120, 230, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(Form.close)
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(90, 10, 128, 128))
        self.label.setMaximumSize(QtCore.QSize(128, 128))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(
                            ":/fontaine/images/fontaine_icon(128).png"))
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
        Form.setWindowTitle(QtGui.QApplication.translate("Form",
                            "О программе", None,
                            QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form",
                            "OK", None,
                            QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form",
                            "Fontaine v0.8", None,
                            QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form",
                            "Powered by PySide & Python", None,
                            QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form",
                            "Alexei Partilov @ 2012", None,
                            QtGui.QApplication.UnicodeUTF8))

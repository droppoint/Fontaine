#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative


def say_hello():
    print 'hello'


# Our main window
class MainWindow(QtDeclarative.QDeclarativeView):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Main Window")
        # Renders 'view.qml'
        self.setSource(QtCore.QUrl.fromLocalFile('playground.qml'))
        # QML resizes to main window
        self.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
        root = self.rootObject()
        button = root.findChild(QtCore.QObject, "mainWindowMouseArea")
#        button.clicked.connect()


if __name__ == '__main__':
    # Create the Qt Application
    app = QtGui.QApplication(sys.argv)
    # Create and show the main window
    window = MainWindow()
    window.show()

    # Run the main Qt loop
    sys.exit(app.exec_())

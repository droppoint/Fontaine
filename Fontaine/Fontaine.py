# -*- coding: UTF-8 -*-

'''
Created on 03.04.2012

@author: Alexei Partilov
'''

from __future__ import division
import sys
#import locale
from WellStorage import WellStorage
import Report
import Parser
from PySide import QtGui, QtCore
from fontaine_ui import Ui_MainWindow


class Singleton(type):
    '''
    Singleton class for creating 1 uniquie instance with
    1 input point
    '''
    def __init__(cls, name, bases, dictationary):
        super(Singleton, cls).__init__(name, bases, dictationary)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance

class _Constants:   # this class store initial data and constants

    class ConstError(TypeError):
        pass

    def __setitem__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError, "Can't rebind const(%s)" % name
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise self.ConstError, "Can't unbind const(%s)" % name
        raise NameError + name

    def reset(self):
        self.__dict__.clear()
#        self.logger.info('Constants cleared')


def timer(f):  # time benchmark
    from time import time

    def tmp(*args, **kwargs):
        t = time()
        res = f(*args, **kwargs)
        print "Время выполнения функции: %f" % (time() - t)
        return res
    return tmp

if __name__ == "__main__":
    const = _Constants()
    config = _Constants()
    storage = WellStorage()
    category = _Constants()
    app = QtGui.QApplication(sys.argv)
    mainwindow = QtGui.QMainWindow()
#    progress = QtGui.QProgressDialog(u"Подготовка отчета...",
#                                        u"Отмена", 0, 100)
#    progress.setWindowTitle(QtGui.QApplication.translate("Progress",
#                            "Fontaine", None, QtGui.QApplication.UnicodeUTF8))
#    progress.setWindowModality(QtCore.Qt.WindowModal)
    ui = Ui_MainWindow()
    ui.setupUi(mainwindow)

    def ignition():
        info_file = open("info.log", "w")
        sys.stdout = info_file
        error_file = open("error.log", "w")
        sys.stderr = error_file
        filename = ui.lineEdit.text()
        well_filename = ui.lineEdit_2.text()
        savefile = ui.setSaveFileName()
        const.reset()  # Блок try не помешал бы
        config.reset()
        config_init('config.ini')
        wells_init(well_filename)
        wells_input_override('input.ini')

        if filename and savefile:
            Parser.parseFile(filename, lateral=ui.tracks.isChecked())
            Report.render(savefile, debug=ui.debug.isChecked(),
                       lateral=ui.tracks.isChecked())
            storage.clear()
        elif not filename:
            ui.informationMessage(u"Выберите файл для обработки",
                                  caption=u"Ошибка запуска")
        else:
            ui.informationMessage(u"Выберите файл для сохранения",
                                  caption=u"Ошибка запуска")
        info_file.close()
        error_file.close()
    ui.pushButton_2.clicked.connect(ignition)

    mainwindow.show()
    sys.exit(app.exec_())

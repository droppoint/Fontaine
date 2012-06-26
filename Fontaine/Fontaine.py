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
import Initialization as Init
from PySide import QtGui, QtCore
from fontaine_ui import Ui_MainWindow


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
    storage = WellStorage()
    category = _Constants()
    app = QtGui.QApplication(sys.argv)
    mainwindow = QtGui.QMainWindow()
    p = Parser.Parser()
#    progress = QtGui.QProgressDialog(u"Подготовка отчета...",
#                                        u"Отмена", 0, 100)
#    progress.setWindowTitle(QtGui.QApplication.translate("Progress",
#                            "Fontaine", None, QtGui.QApplication.UnicodeUTF8))
#    progress.setWindowModality(QtCore.Qt.WindowModal)
    ui = Ui_MainWindow()
    ui.setupUi(mainwindow)

    def ignition():
        info_file = open("info.log", "w")
#        sys.stdout = info_file
        error_file = open("error.log", "w")
#        sys.stderr = error_file
        filename = ui.lineEdit.text()
        well_filename = ui.lineEdit_2.text()
        savefile = ui.setSaveFileName()
#        const.reset()  # Блок try не помешал бы
#        config.reset()
        const = Init.config_init('config.ini')
        storage.category = Init.wells_init(well_filename)
        storage.override = Init.wells_input_override('input.ini')

        if filename and savefile:
            p.initialization(filename)
            iterat = p.parse_file(filename, lateral=ui.tracks.isChecked())
            for rows in iterat:
                print iterat.next()
#            r = Report.Report()
#            r.compilation()
#            r.render()
#            Report.render(savefile, debug=ui.debug.isChecked(),
#                       lateral=ui.tracks.isChecked())
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

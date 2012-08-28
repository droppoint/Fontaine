# -*- coding: UTF-8 -*-
'''
Created on 27.08.2012

@author: APartilov
'''
from View.mainwindow import Ui_MainWindow
from PySide import QtGui


class UserInterface(QtGui.QMainWindow):
    '''
    classdocs
    '''

    def __init__(self, controller, model):
        '''
        Constructor
        '''
        super(UserInterface, self).__init__()
        self.controller = controller
        self.model = model
        '''
        UserInterface реализует паттерн "Наблюдатель"
        подписываясь на изменения в модели. View НЕ РАЗРЕШАЕТСЯ
        взаимодействовать с моделью напрямую, только через один
        контроллеров.
        '''
        self.model.add_observer(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.ui.pushButton_2.clicked.connect(self.ignition)

    def model_is_changed(self, signal):
        """
        Реакция на изменение модели
        Signal - кортеж который содержит в себе информацио о событии,
        например, ('complete',0) подразумевает что расчеты окончены
        без ошибок.
        """
        if signal == ('complete', 0):
            information_message("Завершено")
            self.ui.progress.close()
        elif signal[0] == 'progress':
            self.ui.progress.setProgress(signal[1])
        elif signal[0] == 'error':
            self.errorMessage("Ошибка")
            raise ValueError

    def ignition(self):
        savefile = self.ui.setSaveFileName()
        self.savefile = savefile     # костыль
        self.controller.transfer_consts(self.ui.prefences.get_prefences())
        openfile = self.ui.openfilename
        if savefile and openfile:
            self.controller.execute_converter(openfile, savefile)
        else:
            error_message('Файл для чтения не указан')


def information_message(message, caption="Fontaine"):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(unicode(message))
        msgBox.exec_()


def error_message(message, caption="Fontaine"):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(unicode(message))
        msgBox.exec_()

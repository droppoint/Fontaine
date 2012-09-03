# -*- coding: UTF-8 -*-
'''
Created on 27.08.2012

@author: APartilov
'''
from View.mainwindow import Ui_MainWindow, ProgressDialog
from View.mainwindow import Configuration
from View.form import Ui_Form
from PySide import QtGui, QtCore


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
        вносить изменения в модель напрямую, только через один
        из контроллеров. В то же время разрешается прямое чтение
        из модели
        '''
        self.model.add_observer(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Настройки
        self.settings = QtCore.QSettings()
        self.progress = ProgressDialog()
        self.prefences = ConfigurationDialog()
#        self.prefences_values = self.prefences.get_prefences()
#        self.prefences.set_debug(False)
#        self.prefences.set_lateral(True)
#        self.prefences.accepted.connect(self.acceptPrefences)
#        self.prefences.rejected.connect(self.rejectPrefences)
        # Диалоги и второстепенные окна

        # Инициализация логики
        self.__init_logic()

        self.show()

#        self.ui.pushButton_2.clicked.connect(self.ignition)

    def __init_logic(self):
        self.connect(self.ui.toolButton, QtCore.SIGNAL("clicked()"), self.setOpenFileName)
        self.connect(self.ui.action, QtCore.SIGNAL("triggered()"), self.openAboutWindow)

    def model_is_changed(self, signal):
        """
        Реакция на изменение модели
        Signal - кортеж который содержит в себе информацио о событии,
        например, ('complete',0) подразумевает что расчеты окончены
        без ошибок.
        """
        if signal == ('complete', 0):
            information_message("Завершено")
            self.progress.close()
        elif signal[0] == 'progress':
            self.progress.setProgress(signal[1])
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

    def open_about_window(self):
        about = QtGui.QDialog(self)
        ui = Ui_Form()
        ui.setupUi(about)
        about.show()

    def set_open_file_name(self):
        options = QtGui.QFileDialog.Options()
        if not self.ui.native.isChecked():
            options |= QtGui.QFileDialog.DontUseNativeDialog
        fileName, unused_filtr = QtGui.QFileDialog.getOpenFileName(
                    self.ui.toolButton,
                    u"Открыть",
                    "",
                    "Eclipse RSM File (*.rsm);;All Files (*)",
                    "",
                    options)
        if fileName:
            self.ui.lineEdit.setText(fileName)

def information_message(message, caption="Fontaine"):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(unicode(message))
        msgBox.exec_()


def error_message(message, caption="Fontaine"):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(unicode(message))
        msgBox.exec_()

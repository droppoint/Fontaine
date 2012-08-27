# -*- coding: UTF-8 -*-
'''
Created on 27.08.2012

@author: APartilov
'''
from View.mainwindow import Ui_MainWindow
from PySide import QtGui
from View import form


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

#                self.prefences = ConfigurationDialog()
#        self.prefences_values = self.prefences.get_prefences()
#        self.debug = False
#        self.lateral = True
#        self.prefences.accepted.connect(self.acceptPrefences)
#        self.prefences.rejected.connect(self.rejectPrefences)
#
#        self.progress = ProgressDialog()

    def modelIsChanged(self, signal):
        """
        Реакция на изменение модели
        """
        if signal == 'complete':
            self.information_message("Завершено")
        elif signal == 'progress':
            pass

    def setOpenFileName(self):
        options = QtGui.QFileDialog.Options()
        if not self.native.isChecked():
            options |= QtGui.QFileDialog.DontUseNativeDialog
        fileName, unused_filtr = QtGui.QFileDialog.getOpenFileName(
                    self.toolButton,
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

    def openAboutWindow(self):
        self.about = QtGui.QDialog()
        ui = form.Ui_Form()
        ui.setupUi(self.about)
        self.about.show()

    def informationMessage(self, message, caption="Fontaine"):
        _ = QtGui.QMessageBox.information(self.pushButton_2,
                caption, message)

    def errorMessage(self, message, caption="Fontaine"):
        _ = QtGui.QMessageBox.critical(self.pushButton_2,
                caption, message)
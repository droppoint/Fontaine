# -*- coding: UTF-8 -*-
'''
Created on 27.08.2012

@author: APartilov
'''
from View.UI_rc import Ui_MainWindow, Ui_Form
from View.UI_rc import Ui_Dialog, ProgressDialog
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
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        # Настройки
        self.settings = {}
        self.settings["oil_density"] = 800
        self.settings["water_density"] = 1000
        self.settings["debug"] = False
        self.settings["lateral"] = True

        # Диалоги и второстепенные окна
        self._progress = ProgressDialog()
        self._prefences = ConfigurationDialog(self.settings)

        # Инициализация логики
        self._init_logic()

        self.show()

    def _init_logic(self):
        self.connect(self._ui.toolButton, QtCore.SIGNAL("clicked()"), self._load_file)
        self.connect(self._ui.pushButton_2, QtCore.SIGNAL("clicked()"), self._ignition)
        self.connect(self._ui.action, QtCore.SIGNAL("triggered()"), self._show_about)
        self.connect(self._ui.action_3, QtCore.SIGNAL("triggered()"), self._prefences.show)
        self.connect(self._prefences, QtCore.SIGNAL("accepted()"), self._prefences.save_settings)
        self.connect(self._prefences, QtCore.SIGNAL("rejected()"), self._prefences.load_settings)

    def model_is_changed(self, signal):
        """
        Реакция на изменение модели
        Signal - кортеж который содержит в себе информацио о событии,
        например, ('complete',0) подразумевает что расчеты окончены
        без ошибок.
        """
        if signal == ('complete', 0):
            self._progress.close()
#            information_message("Завершено")
        elif signal[0] == 'progress':
            self._progress.setProgress(signal[1])
        elif signal[0] == 'error':
            self._progress.close()
            self.errorMessage("Ошибка")
            self.controller.emergency_shutdown("Ошибка при расчете модели")

    def _ignition(self):
        self.controller.transfer_consts(self.settings)
        if self._openfile:
            self.controller.execute_converter(self._openfile)
        else:
            error_message('Файл для чтения не указан')

    def _load_file(self):
        self._openfile = self.set_open_filename()
        self._ui.lineEdit.setText(self._openfile)

    def _show_about(self):
        about = QtGui.QDialog(self)
        ui = Ui_Form()
        ui.setupUi(about)
        about.show()

    def set_open_filename(self):
        options = QtGui.QFileDialog.Options()
        if not self._ui.native.isChecked():
            options |= QtGui.QFileDialog.DontUseNativeDialog
        filename, unused_filtr = QtGui.QFileDialog.getOpenFileName(
                    self._ui.toolButton,
                    u"Открыть",
                    "",
                    "Eclipse RSM File (*.rsm);;All Files (*)",
                    "",
                    options)
        if filename:
            return filename

    def set_save_filename(self):
        options = QtGui.QFileDialog.Options()
        if not self._ui.native.isChecked():
            options |= QtGui.QFileDialog.DontUseNativeDialog
        filename, unused_ok = QtGui.QFileDialog.getSaveFileName(
                self._ui.pushButton_2,
                u"Сохранить",
                "",
                "Excel File (*.xls);;All Files (*)", "", options)
        if filename:
            return filename

    def reset(self):
        self.progress.close()


class ConfigurationDialog(QtGui.QDialog):
    def __init__(self, settings, parent=None):
        super(ConfigurationDialog, self).__init__(parent)
        self._ui = Ui_Dialog()
        self._ui.setupUi(self)
        self.settings = settings
        self.load_settings()

    def save_settings(self):
        self.settings["oil_density"] = self._ui.doubleSpinBox.value()
        self.settings["water_density"] = self._ui.doubleSpinBox_2.value()
        self.settings["debug"] = self._ui.checkBox.isChecked()
        self.settings["lateral"] = self._ui.checkBox_2.isChecked()
        self.close()

    def load_settings(self):
        self._ui.doubleSpinBox.setValue(self.settings["oil_density"])
        self._ui.doubleSpinBox_2.setValue(self.settings["water_density"])
        self._ui.checkBox.setChecked(self.settings["debug"])
        self._ui.checkBox_2.setChecked(self.settings["lateral"])
        self.close()


def information_message(message, caption="Fontaine"):
        msgBox = QtGui.QMessageBox()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/fontaine/icons/fontaine_icon(32).png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msgBox.setWindowIcon(icon)
        msgBox.setWindowTitle(QtGui.QApplication.translate("Message",
                        "Fontaine", None, QtGui.QApplication.UnicodeUTF8))
        msgBox.setText(unicode(message))
        msgBox.exec_()


def error_message(message, caption="Fontaine"):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(unicode(message))
        msgBox.exec_()

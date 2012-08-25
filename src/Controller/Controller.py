'''
Created on 22.08.2012

@author: APartilov
'''
from View.Report import Report
from View.mainwindow import Ui_MainWindow
from PySide import QtGui


class Controller():
    '''
    classdocs
    '''

    def __init__(self, model):
        '''
        Constructor
        '''
        self.model = model
        self.view = Report(self, self.model)
        self.ui = mainwindow = QtGui.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(mainwindow)
#        ui.action_5.triggered.connect(app.quit)
        mainwindow.show()

#    def errorlog(func):
#
#        def error_msg(module, msg):
#            logger.exception('Fatal error in ' + module + '\n' + msg)
#            ui.errorMessage(u'Ошибка модуля ' + module + '\n' + msg,
#                            caption=u"Fontaine")
#
#        def decorator(*args, **kwargs):
#            try:
#                return func(*args, **kwargs)
#            except Parser.ParseError as e:
#                error_msg('Parser', str(e))
#            except Field.FieldError as e:
#                error_msg('Field', str(e))
#            except Report.ReportError as e:
#                error_msg('Report', e.msg)
##            except IOError:
##                error_msg('Initialization', "Ini-файл не найден или поврежден")
#            except Exception as inst:
#                logger.exception('Unknown error')
#                logger.exception(type(inst))
#                logger.exception(inst.args)
#                ui.errorMessage(u"Неизвестная ошибка. \n ",
#                                caption=u"Fontaine")
#                raise
#        return decorator
#
#    @errorlog
#    def ignition():
#        filename = ui.lineEdit.text()
#        savefile = ui.setSaveFileName()
#        const = ui.prefences_values
#        debug = ui.debug
#        lateral = ui.lateral
#        if filename and savefile:
#            ui.progress.reset()
#
#
#            storage.lateral_detect(lateral)
#
##            if Init.wells_init('c1.ini'):
##                storage.category = Init.wells_init('c1.ini')
##                tmp = [i for i in storage.wells]
##                for well in tmp:
##                    if not well in storage.category:
##                        del storage.wells[well]
#
#            storage.routine_operations()  # !!!!!!!
#            r.render(savefile)
#            storage.clear()
#            r.reset()
#            ui.progress.close()
#            ui.informationMessage(u"Завершено",
#                                  caption=u"Fontaine")
#        elif not filename:
#            ui.informationMessage(u"Выберите файл для обработки",
#                                  caption=u"Ошибка запуска")
#        else:
#            ui.informationMessage(u"Выберите файл для сохранения",
#                                  caption=u"Ошибка запуска")
#    ui.pushButton_2.clicked.connect(ignition)
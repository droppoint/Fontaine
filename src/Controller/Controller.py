# -*- coding: UTF-8 -*-
'''
Created on 22.08.2012

@author: APartilov
'''
from View.Report import Report
from View.UI import UserInterface


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
        self.ui = UserInterface(self, self.model)

    def set_file_name(self, filename):
        '''
        Initiating satellite scan
        '''
        self.model.add_file_for_parsing(filename)

    def execute_converter(self, openfile, savefile):
        '''
        Execute converting from RSM to xls
        '''
        self.set_file_name(openfile)
        self.view.savefile = savefile
        print openfile, savefile
        self.model.process_data()
        self.model.clear()

    def request_savefile(self):
        return self.ui.savefile

    def transfer_consts(self, consts):
        self.model.parameters.update(consts)
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
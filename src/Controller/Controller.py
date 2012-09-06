# -*- coding: UTF-8 -*-
'''
Created on 22.08.2012

@author: APartilov
'''
from View.Report import Report
from View.UI import UserInterface, information_message
from Utility.Utility import errorlog
import logging

logger = logging.getLogger('Fontaine.ErrorHandler')


class Controller():
    '''
    classdocs
    '''

    def __init__(self, model):
        '''
        Constructor
        '''
        self.model = model
        self.ui = UserInterface(self, self.model)
        self.view = Report(self, self.model)

    def set_file_name(self, filename):
        '''
        Initiating satellite scan
        '''
        self.model.add_file_for_parsing(filename)

    @errorlog
    def execute_converter(self, openfile):
        '''
        Execute converting from RSM to xls
        '''
        self.set_file_name(openfile)
        self.model.process_data()
        self.model.clear()

    def request_savefile(self):
        return self.ui.set_save_filename()

    def transfer_consts(self, consts):
        self.model.parameters.update(consts)

    def emergency_shutdown(self, message):
        logger.info("emergency shutdown initiated")
        self.view.reset()
        self.model.clear()
        information_message(message)

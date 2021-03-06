# -*- coding: UTF-8 -*-

'''
Created on 03.04.2012

@author: Alexei Partilov
'''

import sys
import logging.handlers
import Model.Field as Field
import Controller.Controller as Controller
from PySide.QtGui import QApplication

if __name__ == "__main__":
    # logger system initialization
    logger = logging.getLogger('Fontaine')
    logger.setLevel(logging.DEBUG)
    #basic config here
    fh = logging.handlers.RotatingFileHandler('debug.log',
                                      mode='w',
                                      maxBytes=524288,
                                      backupCount=1)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info('Fontaine start')

    app = QApplication(sys.argv)

    model = Field.Field()
    controller = Controller.Controller(model)

    sys.exit(app.exec_())
#    fh.close() нацепить на выход

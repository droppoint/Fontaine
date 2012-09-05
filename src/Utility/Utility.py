# -*- coding: UTF-8 -*-
'''
Created on 22.08.2012

@author: APartilov
'''
import logging
from View.Report import ReportError
from Controller.Controller import Controller

logger = logging.getLogger('Fontaine.ErrorHandler')


def errorlog(func):

    def error_msg(module, msg):
        logger.exception('Fatal error in ' + module + '\n' + msg)
#        ui.errorMessage(u'Ошибка модуля ' + module + '\n' + msg,
#                        caption=u"Fontaine")

    def decorator(*args, **kwargs):
        try:
            return func(*args, **kwargs)
#        except Parser.ParseError as e:
#            error_msg('Parser', str(e))
#        except Field.FieldError as e:
#            error_msg('Field', str(e))
        except ReportError as e:
            error_msg('Report', e.msg)
        except IOError as e:
            error_msg('Fatal', u"Ошибка чтения/записи")
#            except IOError:
#                error_msg('Initialization', "Ini-файл не найден или поврежден")
        except Exception as inst:
            Controller.emergency_shutdown("Неизвестная ошибка")
            logger.exception('Unknown error')
            logger.exception(type(inst))
            logger.exception(inst.args)
#            ui.errorMessage(u"Неизвестная ошибка. \n ",
#                            caption=u"Fontaine")
            raise
    return decorator


def timer(f):  # time benchmark
    from time import time

    def tmp(*args, **kwargs):
        t = time()
        res = f(*args, **kwargs)
        print "Время выполнения функции: %f" % (time() - t)
        return res
    return tmp


def wells_init(filename):
    import mmap
    import re

    result = {}
    try:
        f = open(filename, "r+")
    except IOError as unused_e:
        print "Category file not found, proceeding"
        return
    buf = mmap.mmap(f.fileno(), 0)  # add filename check
    filesize = buf.size()
    n = 0
    buf.seek(n)
    while True:
        print buf.tell()
        if buf.tell() == filesize:
            break
        data = buf.readline()
        raw = re.match(r"^((?:[0-9]+[A-Z]?(?:[-_]?\w*)?)|(?:[A-Z]{1,3}(?:[-_]\w*)?(?:[-_]\w*)?))\s+(0.\d+|1)", data)
        if raw:
            well = raw.groups()
            result.update(dict([well]))  # bad memory consumption
    return result


def wells_input_override(filename):
    import mmap
    import re
    result = {}
    try:
        f = open(filename, "r+")
    except IOError as unused_e:
        print "Wells input override file not found, proceeding"
        return
    buf = mmap.mmap(f.fileno(), 0)  # add filename check
    filesize = buf.size()
    n = 0
    buf.seek(n)
    while True:
        if buf.tell() == filesize:
            break
        data = buf.readline()
        while re.match(r"^\s*#", data):
            data = buf.readline()
        raw = re.match(r"^([0-9]+[A-Z]?(?:[-_]?\w*)?)\s+"
                             "((?:0[1-9]|[1-2][0-9]|3[0|1])/"
                             "(?:0[1-9]|1[0-2])/"
                             "(?:(?:19|20|21|22)\d{2}))", data)
        if raw:
            well = raw.groups()
            result.update(dict([well]))
    return result
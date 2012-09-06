# -*- coding: UTF-8 -*-
'''
Created on 22.08.2012

@author: APartilov
'''
import logging
from View.Report import ReportError
from Model.Field import FieldError
from Model.Parser import ParseError
from View.UI import information_message

logger = logging.getLogger('Fontaine.ErrorHandler')


def errorlog(func):

    def error_msg(module, msg):
        logger.exception('Fatal error in ' + module + '\n' + msg)
        information_message(u'Ошибка модуля ' + module + '\n' + msg,
                        caption=u"Fontaine")

    def decorator(*args, **kwargs):
        controller = args[0]
        try:
            return func(*args, **kwargs)
        except ParseError as e:
            error_msg('Parser', str(e))
            controller.emergency_shutdown("Ошибка при чтении RSM")
        except FieldError as e:
            error_msg('Field', str(e))
            controller.emergency_shutdown("Ошибка при расчете модели")
        except ReportError as e:
            error_msg('Report', e.msg)
        except IOError as e:
            error_msg('Fatal', u"Ошибка чтения/записи")
        except Exception as inst:
            controller.emergency_shutdown("Неизвестная ошибка")
            logger.exception('Unknown error')
            logger.exception(type(inst))
            logger.exception(inst.args)
            information_message(u"Неизвестная ошибка. \n ",
                            caption=u"Fontaine")
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


#Функция применения файла ограничений(имя файла)
def parse_cut_file(filename):
    try:
        f = open(filename, "r+")
    except IOError:
        print "Category file not found, returning None"
        return None
    result = {}
    for line in f:
        if not line:
            return None
        # Разделить строку по пробелу
        clear_line = line.split()
        # Если строка была пуста
        # пройти дальше
        if not clear_line:
            continue
        # Если строка начинается с "#"
        # Значить это комментарий и мы пропускаем строку
        if clear_line[0].startswith("#"):
            continue
        if len(clear_line) != 2:
            return None
        try:
            # Преобразовать второй элемент в число
            # так как второе число является
            # коэффициентом эксплуатации
            exp_factor = float(clear_line[1])
        except ValueError:
            return None
        # И если мы таки не напоролись ни на одно исключение
        result.update({clear_line[0]: exp_factor})
    return result

#def wells_init(filename):
#    import mmap
#    import re
#
#    result = {}
#    try:
#        f = open(filename, "r+")
#    except IOError as unused_e:
#        print "Category file not found, proceeding"
#        return
#    buf = mmap.mmap(f.fileno(), 0)  # add filename check
#    filesize = buf.size()
#    n = 0
#    buf.seek(n)
#    while True:
#        print buf.tell()
#        if buf.tell() == filesize:
#            break
#        data = buf.readline()
#        raw = re.match(r"^((?:[0-9]+[A-Z]?(?:[-_]?\w*)?)|(?:[A-Z]{1,3}(?:[-_]\w*)?(?:[-_]\w*)?))\s+(0.\d+|1)", data)
#        if raw:
#            well = raw.groups()
#            result.update(dict([well]))  # bad memory consumption
#    return result
#
#
#def wells_input_override(filename):
#    import mmap
#    import re
#    result = {}
#    try:
#        f = open(filename, "r+")
#    except IOError as unused_e:
#        print "Wells input override file not found, proceeding"
#        return
#    buf = mmap.mmap(f.fileno(), 0)  # add filename check
#    filesize = buf.size()
#    n = 0
#    buf.seek(n)
#    while True:
#        if buf.tell() == filesize:
#            break
#        data = buf.readline()
#        while re.match(r"^\s*#", data):
#            data = buf.readline()
#        raw = re.match(r"^([0-9]+[A-Z]?(?:[-_]?\w*)?)\s+"
#                             "((?:0[1-9]|[1-2][0-9]|3[0|1])/"
#                             "(?:0[1-9]|1[0-2])/"
#                             "(?:(?:19|20|21|22)\d{2}))", data)
#        if raw:
#            well = raw.groups()
#            result.update(dict([well]))
#    return result
# -*- coding: UTF-8 -*-

'''
Created on 18.06.2012

@author: APartilov
'''

#class MyClass(object):
#    '''
#    classdocs
#    '''
#
#
#    def __init__(selfparams):
#        '''
#        Constructor
#        '''


def initialization(filename):
    """Return primary parameters of RSM file,
    such as RSM filetype, height of data table,
    masks and other"""
    from datetime import datetime
    import re
    import mmap

    def fileTypeDetermination(buf):
        n = 0
        buf.seek(n)
        breaker = buf.readline()
        if breaker == "1\r\n":
            filetype = "tempest"
        elif breaker == "\r\n":
            filetype = "eclipse"
        else:
            raise IOError
        return filetype, breaker

    def dateFormatDetermination(dataline):
        date_pattern = ""  # date format check
        regex_pattern = ""
        if re.findall(r"\s((?:0[1-9]|[1-2][0-9]|3[0|1])/"
                             "(?:0[1-9]|1[0-2])/"
                             "(?:(?:19|20|21|22)\d{2}))\s", dataline):
            date_pattern = "%d/%m/%Y"
            regex_pattern = ("\s((?:0[1-9]|[1-2][0-9]|3[0|1])/"
                                 "(?:0[1-9]|1[0-2])/"
                                 "(?:(?:19|20|21|22)\d{2}))\s")
        elif re.findall(r"\s((?:0[1-9]|[1-2][0-9]|3[0|1])-"
                               "(?:[ADFJMNOS][A-Za-z]{2})-"
                               "(?:(?:19|20|21)\d{2}))\s", dataline):
            date_pattern = "%d-%b-%Y"
            regex_pattern = ("\s((?:0[1-9]|[1-2][0-9]|3[0|1])-"
                                  "(?:[ADFJMNOS][A-Za-z]{2})-"
                                  "(?:(?:19|20|21|22)\d{2}))\s")
        else:
            print "unknown date type"
            raise ValueError
        return date_pattern, regex_pattern

    dates = []
    mod_dates = {}
    f = open(filename, "r+")   # add filename check
    buf = mmap.mmap(f.fileno(), 0)
    filetype, breaker = fileTypeDetermination(buf)
    line = buf.readline()
    num = 0
    firstdataline = 0
    while not re.search(r"^%s$" % (breaker), line):
        num += 1
        if re.search(r"^\s*[-]*\r\n$", line):
            commentaryline = num
            firstdataline = buf.tell()
        elif re.findall(r"\s(DATE)", line):  # WHY???
#            header = num
            pass
        line = buf.readline()
    buf.seek(firstdataline)
    dataline = buf.readline()
    d_pattern, r_pattern = dateFormatDetermination(dataline)
    dataheight = num - commentaryline
    for unused_i in range(dataheight):  # получение массива дат
#        locale.setlocale(locale.LC_ALL, 'en_US.utf8')
        cur_date = datetime.strptime(re.findall(r_pattern, dataline)[0],
                                                            d_pattern)
        dataline = buf.readline()
        dates.append(cur_date)
    for date in dates:
        if date.month == 1:
            mod_dates[date.year] = dates.index(date)
    storage.dates = mod_dates
    config.filetype = filetype
    config.breaker = breaker
    config.r_pattern = r_pattern
    storage.minimal_year = min(storage.dates.keys())


def config_init(filename):
    import ConfigParser

    def parseConfigSection(section_name):
        if not section_name in config.sections():
            return
        for options in config.options(section_name):
            const[options] = config.get(section_name, options)
    try:
        config = ConfigParser.ConfigParser()
        config.read(filename)
        for sections in config.sections():
            parseConfigSection(sections)
    except:
        print "Configuration file not found"


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
        raw = re.match(r"^([0-9]+[A-Z]?(?:[-_]?\w*)?)\s+(0.\d+|1)", data)
        if raw:
            well = raw.groups()
            result.update(dict([well]))  # bad memory consumption
    storage.category = result


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
    date_pattern = "%d/%m/%Y"
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
    storage.override = result



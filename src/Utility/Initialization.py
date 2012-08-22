# -*- coding: UTF-8 -*-

'''
Created on 18.06.2012

@author: APartilov
'''


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

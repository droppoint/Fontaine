# -*- coding: UTF-8 -*-

'''
Created on 18.06.2012

@author: APartilov
'''
from WellStorage import WellStorage


import re

# Regular expressions used for parsing

regex_all_headers = re.compile(r"([A-Z0-9_]+)")
regex_necessary_headers = re.compile(
                r"\b(W[O|G|W|L][I|P][T|R|N]|WBPN|WBHP|FPRP?)\b")
regex_header = re.compile(r"^(W[O|G|W|L][I|P][T|R|N])|(WBPN|WBHP)$")
regex_well_properties = re.compile(r"^(W[O|G|W|L][I|P][T|R|N])|(WBPN|WBHP)$")
regex_field_properties = re.compile(r"^(FPRP?)$")
regex_numbers = re.compile(r"\s([0-9]+[A-Z]?(?:[-_]?\w*)?)\s")
regex_data_line = re.compile(r"\s((?:[-+]?[0-9]*\.[0-9]*E?-?[0-9]*)|0)\s")
regex_all_numbers = re.compile(r"^([\w-]+)\b")
regex_factor = re.compile(r"(?:\*10\*\*(\d))")


class ParseError(Exception):
    """Exception raised for all parse errors."""

    def __init__(self, msg, position=(None, None)):
        assert msg
        self.msg = msg
        self.lineno = position[0]
        self.offset = position[1]

    def __str__(self):
        result = self.msg
        if self.lineno is not None:
            result = result + ", at line %d" % self.lineno
        if self.offset is not None:
            result = result + ", column %d" % (self.offset + 1)
        return result


class Parser(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.reset()

    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
        self.data = {}

    def error(self, message):
        raise ParseError(message)

    def close(self):
        """Handle any buffered data."""
        self.goahead(1)

    def parse_file(self, filename, **kwargs):
        import mmap
        import math  # maybe in other place?
        lateral = kwargs.get('lateral')
        initialization(filename)
        storage = WellStorage()

        def parseBlock(pointer):
            result = {}
            #Reading header
            buf.seek(pointer)
            header_str = buf.readline()
            headers = re.findall(r"([A-Z0-9_]+)", header_str)
            result['headers'] = regex_necessary_headers.findall(header_str)

            #Comparision of the headers
            def indices(mylist, value):
                return [i for i, x in enumerate(mylist) if x == value]
            index = []
            temp = []
            for value in result['headers']:
                if not value in temp:
                    index += indices(headers, value)
                    temp.append(value)
            del(temp)
    #        quantity_str = buf.readline()
            line = buf.readline()
            factor = []
            while not re.search(r"\s([0-9]+[A-Z]?(?:[-_]?\w*)?)\s", line):  # ???
                if re.search(config.r_pattern, line):
                    break
                if regex_factor.search(line):
                    temp_num = line[14:]   # bad block of code
                    nn = 0
                    while nn + 13 < len(temp_num):
                        if factor.match(temp_num[nn:nn + 13]):
                            factor.append(regex_factor.findall(
                                            temp_num[nn:nn + 13])[0])
                        else:
                            factor.append(None)
                        nn += 13
                line = buf.readline()
            result['factor'] = list(factor)
            numbers_str = line
            numbers = regex_numbers.findall(numbers_str)

            if ((len(headers) - 1) > len(numbers)) and numbers != []:
                temp_num = numbers_str[14:]   # bad block of code
                numbers = []
                nn = 0
                while nn + 13 < len(temp_num):
                    if regex_all_numbers.match(temp_num[nn:nn + 13]):
                        numbers.append(regex_all_numbers.match(
                                        temp_num[nn:nn + 13]).group(0))
                    else:
                        numbers.append("N/A")
                    nn += 13
            if numbers == []:
                numbers = ["N/A" for unused_i in range(len(headers) - 1)]
            result['numbers'] = [numbers[i - 1] for i in index if numbers]
            #Reading data
            while not re.search(config.r_pattern, line):
                line = buf.readline()
            data = line
            result['data'] = []
            while not data == config.breaker:  # parsing the data
                dataline = regex_data_line.findall(data)
                result['data'].append([dataline[i - 1] for i in index])
                if buf.tell() == filesize:
                    break
                data = buf.readline()
            return result

        f = open(filename, "r+")
        buf = mmap.mmap(f.fileno(), 0)  # add filename check
        filesize = buf.size()
        n = 0
        buf.seek(n)
        while buf.find("SUMMARY", n) != -1:
    #        if progress.wasCanceled():
    #            f.close()
    #            break
    #        progress.setValue(int((n / filesize) * 100))
            n = buf.find("SUMMARY", n)
            m = buf.find("DATE", n)
            buf.seek(n)  # WHY???
            n += 1
            buf.seek(m)
            cur_str = buf.readline()
            if regex_necessary_headers.findall(cur_str):
                block = parseBlock(m)
                for key, well_num in enumerate(block['numbers']):
                    data = [i[key] for i in block['data']]
                    parameter = block['headers'][key]

                    if regex_well_properties.match(parameter):
                        if block['factor']:
                            factor = block['factor'][key]
                            if factor:
                                fl = float(factor)
                                fk = math.pow(10.0, fl)
                                data = [float(i) * fk for i in data]
                        storage.add_well(well_num, parameter,
                                            data, lateral=lateral)

                    if regex_field_properties.match(parameter):
                        welldata = []
                        for year in sorted(storage.dates.values()):
                            welldata.append(float(data[year]))
                        storage.add_parameter(parameter, welldata)

        f.close()

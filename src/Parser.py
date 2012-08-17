# -*- coding: UTF-8 -*-

'''
Created on 18.06.2012

@author: APartilov
'''


import re
import logging

# Regular expressions used for parsing

total_parameters = ['WOPT', 'WWPT', 'WGPT', 'WWIT', 'WOIT', 'WGIT', 'WLPT',
                    'WLPR', 'WOIN', 'WWIN', 'WGIN', 'WOIR', 'WWIR', 'WGIR', 
                    'WBP9', 'WBHP', 'FPRP', 'FPR']
regex_all_headers = re.compile(r"([A-Z0-9_]+)")
regex_necessary_headers = re.compile(
                r"\b(W[O|G|W|L][I|P][T|R|N]|WBP9|WBHP|FPRP?)\b")
regex_header = re.compile(r"^(W[O|G|W|L][I|P][T|R|N])|(WBP9|WBHP)$")
regex_properties = re.compile(
                r"^(W[O|G|W|L][I|P][T|R|N])|(WBP9|WBHP)|(FPRP?)$")
regex_numbers = re.compile(r"\s((?:[0-9]+[A-Z]?(?:[-_]?\w*)?)|(?:[A-Z]{1,3}(?:[-_]\w*)?(?:[-_]\w*)?))\s")
regex_data_line = re.compile(r"\s((?:[-+]?[0-9]*\.[0-9]*E?[+|-]?[0-9]*)|0)\s")
regex_all_numbers = re.compile(r"\b([\w-]+)\b")
regex_factor = re.compile(r"(?:\*10\*\*(\d))")
regex_date_numeric = re.compile(r"((?:0[1-9]|[1-2][0-9]|3[0|1])/"
                 "(?:0[1-9]|1[0-2])/"
                "(?:(?:19|20|21|22)\d{2}))")
regex_date_alphabetic = re.compile(r"((?:0[1-9]|[1-2][0-9]|3[0|1])-"
                                      "(?:[ADFJMNOS][A-Za-z]{2})-"
                                      "(?:(?:19|20|21|22)\d{2}))")


class ParserFileHandler(object):

    def __init__(self, filename):
        import mmap
        self.pointer = 0
        self.__file = open(filename, "r+")
        self.buf = mmap.mmap(self.__file.fileno(), 0)  # add filename check
        self.buf.seek(self.pointer)

    def readHeader(self):
        n = self.buf.find("DATE", self.pointer)
        self.buf.seek(n)
        tmp = self.buf.readline()
        self.buf.seek(self.pointer)
        return tmp

    def nextBlock(self):
        self.pointer += 1
        n = self.buf.find("SUMMARY", self.pointer)
        if n == -1:
            return False
        self.buf.seek(n)
        self.buf.readline()
        self.pointer = n
        return True

    def readBlock(self):
        self.buf.seek(self.pointer)
        start = self.buf.find("DATE", self.pointer)
        end = self.buf.find("SUMMARY", start)
        self.buf.seek(start)
        while not self.buf.tell() >= end:
            line = self.buf.readline()
            if not re.match(r'^\s*$|^&', line):
                yield line
        self.buf.seek(self.pointer)

    def close(self):
        self.buf.close()
        self.__file.close()

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
            result = result + " at line %d" % self.lineno
        if self.offset is not None:
            result = result + " column %d" % (self.offset + 1)
        return result


class Parser(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.logger = logging.getLogger('Fontaine.parser.Parser')
        self.logger.info('creating an instance of Parser')
        self.reset()
        self.__progress = 0.0

    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
        self.data = {}
        self.config = {}

    def close(self):
        """Handle any buffered data."""
        self.data.clear()
        self.config.clear()
        self.reset()
        self.__progress = 0.0

    def report_progress(self):
        return self.__progress

    def initialization(self, filename):
        """Return primary parameters of RSM file,
        such as RSM filetype, height of data table,
        masks and other"""
        from datetime import datetime
        import mmap

        def fileTypeDetermination():
            n = 0
            buf.seek(n)
            breaker = buf.readline()
            if breaker == "1\r\n":
                filetype = "tempest"
            elif breaker == "\r\n":
                filetype = "eclipse"
            else:
                raise ParseError('Unknown breaker ', position=(0, 0))
            return filetype, breaker

        def dateFormatDetermination(dataline):
            date_pattern = ""  # date format check
            regex_pattern = ""
            if regex_date_numeric.findall(dataline):
                date_pattern = "%d/%m/%Y"
                regex_pattern = regex_date_numeric
            elif regex_date_alphabetic.findall(dataline):
                date_pattern = "%d-%b-%Y"
                regex_pattern = regex_date_alphabetic
            else:
                raise ParseError('Unknown date type')
            return date_pattern, regex_pattern

        dates = []
        mod_dates = {}
        with open(filename, "r+") as f:
            f = open(filename, "r+")   # add filename check
            buf = mmap.mmap(f.fileno(), 0)
            filetype, breaker = fileTypeDetermination()
            line = buf.readline()
            num = 0
            firstdataline = 0
            while not re.search(r"^%s$" % (breaker), line):
                num += 1
                if re.search(r"^\s*[-]*\r\n$", line):
                    commentaryline = num
                    firstdataline = buf.tell()
                line = buf.readline()
            buf.seek(firstdataline)
            dataline = buf.readline()
            d_pattern, r_pattern = dateFormatDetermination(dataline)
            dataheight = num - commentaryline
            for line_number in range(dataheight):  # получение массива дат
        #        locale.setlocale(locale.LC_ALL, 'en_US.utf8')
                cur_date = r_pattern.search(dataline).group(0)
                cur_date = datetime.strptime(cur_date, d_pattern)
                dataline = buf.readline()
                dates.append(cur_date)
                if cur_date.month == 1:
                    mod_dates[cur_date.year] = line_number
            self.config['dates'] = mod_dates
            self.config['filetype'] = filetype
            self.config['breaker'] = breaker
            self.config['r_pattern'] = r_pattern
            buf.close()

    def get_dates_list(self):
        return self.config['dates']

    def parse_file(self, filename):
        import mmap
        import math  # maybe in other place?
        self.initialization(filename)

#        def parseBlock3(block):
#            pass
#        def parseBlock2(pointer):
#            result = {}
#            result['headers'] = []
#            result['numbers'] = []
#            result['factor'] = []
#            result['data'] = []
#            buf.seek(pointer)
#            header_str = buf.readline()
#            if not regex_necessary_headers.search(header_str):
#                return
#
#            def indices(mylist, value):
#                return [i for i, x in enumerate(mylist) if x == value]
#
#            result['headers'] = regex_all_headers.findall(header_str)
#            while not self.config['r_pattern'].search(line):
#                line = buf.readline()
#            while not line == self.config['breaker']:  # parsing the data
#                dataline = regex_data_line.findall(line)
#                result['data'].append(dataline)
#                if buf.tell() == filesize:
#                    break
#                line = buf.readline()
#            return result
#
#        def parseBlock(pointer):
#            result = {}
#            #Reading header
#            buf.seek(pointer)
#            header_str = buf.readline()
#            headers = regex_all_headers.findall(header_str)
#            result['headers'] = regex_necessary_headers.findall(header_str)
#            if not result['headers']:
#                return
#            #Comparsion of the headers
#
#            def indices(mylist, value):
#                return [i for i, x in enumerate(mylist) if x == value]
#
#            index = []
#            temp = []
#            for value in result['headers']:
#                if not value in temp:
#                    index += indices(headers, value)
#                    temp.append(value)
#            del(temp)
#            buf.readline()
#            line = buf.readline()  # to skip quantity
#            factor = []
#            while not regex_numbers.search(line):
#                if self.config['r_pattern'].search(line):
#                    break
#                if regex_factor.search(line):
#                    temp_num = line[14:]
#                    for word in split_by_n(temp_num, 13):
#                        if regex_factor.search(word):
#                            factor.append(regex_factor.findall(word)[0])
#                        else:
#                            factor.append(None)
#                line = buf.readline()
#            numbers_str = line
#            numbers = regex_numbers.findall(numbers_str)
#            if self.config['r_pattern'].search(line):
#                numbers = []
#            result['factor'] = [factor[i - 1] for i in index if factor]
#            if ((len(headers) - 1) > len(numbers)) and numbers != []:
#                temp_num = numbers_str[14:]   # bad block of code
#                numbers = []
#                for word in split_by_n(temp_num, 13):
#                    if regex_all_numbers.search(word):
#                        numbers.append(
#                            regex_all_numbers.search(word).group(0))
#                    else:
#                        numbers.append("N/A")
#            if numbers == []:
#                numbers = ["N/A" for unused_i in range(len(headers) - 1)]
#            result['numbers'] = [numbers[i - 1] for i in index if numbers]
#            #Reading data
#            while not re.search(self.config['r_pattern'], line):
#                line = buf.readline()
#            data = line
#            result['data'] = []
#            while not data == self.config['breaker']:  # parsing the data
#                dataline = regex_data_line.findall(data)
#                result['data'].append([dataline[i - 1] for i in index])
#                if buf.tell() == filesize:
#                    break
#                data = buf.readline()
#            return result

        stream = ParserFileHandler(filename)
        for line in stream.readBlock():
            print line
        while stream.nextBlock():
            stream.readHeader()
        stream.close()
#        f = open(filename, "r+")
#        buf = mmap.mmap(f.fileno(), 0)  # add filename check
#        filesize = buf.size()
#        n = 0
#        buf.seek(n)
#        while buf.find("SUMMARY", n) != -1:   # вложенность
#            n = buf.find("SUMMARY", n)
#            m = buf.find("DATE", n)
#            n += 1
#            buf.seek(m)
#            self.__progress = (m * 100)//filesize
#            cur_str = buf.readline()
#            if regex_necessary_headers.search(cur_str):
#                block = parseBlock(m)
##                print parseBlock2(m)
#                for key, well_num in enumerate(block['numbers']):
#                    data = [i[key] for i in block['data']]
#                    parameter = block['headers'][key]
#                    parsed_data = {}
#                    if regex_properties.match(parameter):
#                        if block['factor']:
#                            factor = block['factor'][key]
#                            if factor:
#                                fl = float(factor)
#                                fk = math.pow(10.0, fl)
#                                data = [float(i) * fk for i in data]
#                        parsed_data['number'] = well_num
#                        parsed_data['parameter_code'] = parameter
#                        parsed_data['welldata'] = data
#                        yield parsed_data

#        buf.close()
#        f.close()


def split_by_n(seq, n):
    """A generator to divide a sequence into chunks of n units."""
    while seq:
        yield seq[:n]
        seq = seq[n:]

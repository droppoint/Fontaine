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
regex_all_numbers = re.compile(r"\s([A-Za-z0-9][\w\-]*)\s")
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
        # Определение формата даты
        self.delimiter = self.read_delimiter_format()
        self.date_pattern, self.date_pattern_str = self.read_date_format()
        self.dates = self.read_dates()

    def report_progress(self):
        return self.pointer * 100 // self.buf.size()

    def read_delimiter_format(self):
        self.buf.seek(0)
        delimiter = self.buf.readline()
        if delimiter not in ("\r\n", '1\r\n'):
            raise ParseError('Unknown delimiter')
        self.buf.seek(self.pointer)
        return '\r\n' + delimiter

    def find_block_borders(self):
        start = self.buf.find("DATE", self.pointer)
        end = self.buf.find(self.delimiter, start)
        if end == -1:
            end = self.buf.size()
        return start, end

    def read_dates(self):
        from datetime import datetime
        self.buf.seek(self.pointer)
        start, end = self.find_block_borders()
        self.buf.seek(start)
        dates = {}
        n = 0
        while not self.buf.tell() >= end:
            line = self.buf.readline()
            if self.date_pattern.search(line):
                clear_line = self.date_pattern.search(line).group(0)
                date = datetime.strptime(clear_line, self.date_pattern_str)
                if date.month == 1:
                    dates[date.year] = n
                n += 1
        self.buf.seek(self.pointer)
        return dates

    def get_dates_list(self):
        return self.dates

    def read_date_format(self):
        start, end = self.find_block_borders()
        while True:
            line = self.buf.readline()
            if regex_date_numeric.search(line):
                return regex_date_numeric, "%d/%m/%Y"
            elif regex_date_alphabetic.search(line):
                return regex_date_alphabetic, "%d-%b-%Y"
            elif self.buf.tell() > end:
                raise ParseError('Unknown date type or file damaged')
        self.buf.seek(self.pointer)

    def read_header(self):
        n = self.buf.find("DATE", self.pointer)
        self.buf.seek(n)
        tmp = self.buf.readline()
        self.buf.seek(self.pointer)
        return tmp

    def next_block(self):
        self.pointer += 1
        n = self.buf.find("SUMMARY", self.pointer)
        if n == -1:
            return False
        self.buf.seek(n)
        self.pointer = n
        return True

    def read_block(self):
        start, end = self.find_block_borders()
        self.buf.seek(start)
        while not self.buf.tell() >= end:
            line = self.buf.readline()
            if not re.match(r'^\s*$|^&', line) and \
                self.date_pattern.search(line):
                yield line
        self.buf.seek(self.pointer)

    def read_context(self):
        self.buf.seek(self.pointer)
        start = self.buf.find("DATE", self.pointer)
        self.buf.seek(start)
        self.buf.readline()
        self.buf.readline() # skipping quantities
        numbers, factors = None, None
        while True:
            line = self.buf.readline()
            if self.date_pattern.search(line):
                break    # слабое место (нет ограничений)
            elif regex_all_numbers.search(line):
                numbers = line
            elif regex_factor.search(line):
                factors = line
        self.buf.seek(self.pointer)
        return numbers, factors

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

    def __init__(self, filename):
        '''
        Constructor
        '''
        self.logger = logging.getLogger('Fontaine.parser.Parser')
        self.logger.info('creating an instance of Parser')
        self.reset()
        self.stream = ParserFileHandler(filename)

    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
        pass

    def close(self):
        """Handle any buffered data."""
        self.reset()

    def report_progress(self):
        return self.stream.report_progress()

    def get_dates_list(self):  # Костыль
        return self.stream.get_dates_list()

    def parse_file(self):
        import math  # maybe in other place?

        while self.stream.next_block():
            '''
            Если в заголовке блока найден нужный заголовок/заголовки,
            то начинаем обработку блока. Если нет - то просто переходим
            к следующему. Проверяем через re.
            '''
            header = self.stream.read_header()
            if regex_necessary_headers.search(header):
                parsed_data = {}
                '''
                 Считываются номера скважин, степень(если есть) и сам блок данных
                 '''
                numbers, factors = self.stream.read_context()
                block = self.stream.read_block()
                # Здесь header становится массивом содержащим заголовки
                clear_headers = regex_necessary_headers.findall(header)
                header = header.split()

                tmp_header = []
                index = []      # костыль
                for i in clear_headers:
                    if i not in tmp_header:
                        index += indices(header, i)
                        tmp_header.append(i)

                clear_block = []
                for line in block:
#                    data = regex_data_line.findall(line)
                    data = line.split()
                    del data[0]  # удаляем дату из начала списка
                    clear_block.append([float(data[i]) for i in index])
                clear_block = zip_list(*clear_block)
                clear_block = [i for i in clear_block]
                if numbers:
                    clear_numbers = strip_line(regex_all_numbers, numbers)
                    clear_numbers = [clear_numbers[i] for i in index]
                if factors:
                    clear_factors = strip_line(regex_factor, factors)
                    clear_factors = [clear_factors[i] for i in index]
                    for num, factor in enumerate(clear_factors):   # костыль
                        if factor != 'N/A':
                            clear_block[num] = \
                             [math.pow(10, float(factor)) * i for i in clear_block[num]]
                for num, parameter in enumerate(clear_headers):
                    if numbers:
                        parsed_data['number'] = clear_numbers[num]
                    else:
                        parsed_data['number'] = 'N/A'
                    parsed_data['parameter_code'] = parameter
                    parsed_data['welldata'] = clear_block[num]
                    yield parsed_data
        self.stream.close()


def strip_line(regex, string):
    temp_num = string[13:]
    result = []
    for word in split_by_n(temp_num, 13):
        clear_str = regex.findall(word)
        if clear_str:
            result.append(clear_str[0])
        else:
            result.append('N/A')
    return result


def zip_list(*iterables):
    # izip('ABCD', 'xy') --> Ax By
    iterators = map(iter, iterables)
    while iterators:
        yield list(map(next, iterators))


def indices(mylist, value):
    return [i - 1 for i, x in enumerate(mylist) if x == value]


def split_by_n(seq, n):
    """A generator to divide a sequence into chunks of n units."""
    while seq and len(seq) >= n:
        yield seq[:n]
        seq = seq[n:]

# -*- coding: UTF-8 -*-
'''
Created on 04.07.2012

@author: APartilov
'''


total_parameters = ['WOPT', 'WWPT', 'WGPT', 'WWIT', 'WOIT', 'WGIT', 'WLPT']
total_prod_parameters = ['WOPT', 'WWPT', 'WGPT']
total_inj_parameters = ['WOIT', 'WWIT', 'WGIT']
total_dec_parameters = ['decWOPT', 'decWWPT', 'decWGPT',
                        'decWWIT', 'decWOIT', 'decWGIT']
rate_parameters = ['WLPR', 'WOIN', 'WWIN', 'WGIN']
rate_prod_parameters = ['WLPR']
rate_inj_parameters = ['WOIN', 'WWIN', 'WGIN', 'WOIR', 'WWIR', 'WGIR']

import numpy


class Borehole(object):
    '''
    classdocs
    '''

    def __init__(self, data=None):
        self.parameters = {}
        if data:
            self.add_parameter(data)

    def add_parameter(self, data):
        self.parameters.update(data)

    def compress_data(self, dates):  # уменьшить вложенность
        numpy.set_printoptions(precision=3)
        b = dates.values()
        for parameter in self.parameters:
            self.parameters[parameter] = \
                self.parameters[parameter].take(sorted(b))
            if parameter in total_parameters:
                a = self.parameters[parameter]
                a = numpy.roll(a, -1) - a
                self.parameters[parameter] = numpy.delete(a, -1)

    def recieve_parameter(self, code):
        return self.parameters.get(code)

    def recieve_parameters(self, *args):
        datalist = None
        for arg in args:
            datalist = self.recieve_parameter(arg)
            if datalist != None:
                yield datalist

    def clear(self):
        self.parameters.clear()


class Well(object):
    '''
    classdocs
    '''
    def __init__(self, data=None):  # number
        '''
        Constructor
        '''
        self.__boreholes = {}
        self.first_run = None
        self.abandonment = None
        self.work_time = None
        self.classification = None
        self.classification_by_rate = None
        if data:
            self.add_parameter(data)

    def add_parameter(self, number, data):
        if not number in self.__boreholes:
            self.__boreholes.update({number: Borehole()})
        self.__boreholes[number].add_parameter(data)

    def abandonment_year(self):
        for year, work_time in enumerate(reversed(self.work_time)):
            if work_time > 0:
                break
        if year == 0:
            self.abandonment = "working"
            return False
        self.abandonment = len(self.work_time) - 1 - year
        return len(self.work_time) - 1 - year

    def completion_year(self):
        for year, work_time in enumerate(self.work_time):
            if work_time > 0:
                break
        # add oil well type
        if year == len(self.work_time) + 1:
            self.first_run = "None"
            return False
        self.first_run = year
        return year

    def recieve_parameters(self, *args):
        for arg in args:
            datalist = None
            for borehole in self.__boreholes.values():
                if datalist == None:
                    exists = borehole.recieve_parameter(arg)
                    if exists != None:
                        datalist = exists
                    continue
                datalist = datalist + borehole.recieve_parameter(arg)
            if datalist == None:
                continue
            yield datalist

    def borehole_input(self, name):
        years = []
        for number in self.__boreholes:
            if number == name:
                continue
            production = self.__boreholes[number].recieve_parameters(
                                *total_prod_parameters)
            production = reduce(lambda x, y: x + y, production)
            injection = self.__boreholes[number].recieve_parameters(
                                *total_inj_parameters)
            injection = reduce(lambda x, y: x + y, injection)
            total = production + injection
            for year, total in enumerate(total):
                if total > 0:
                    years.append(year)
                    break
        return years

    def well_classification(self, mode='total'):
        if mode == 'total':
            production = self.recieve_parameters(*total_prod_parameters)
            injection = self.recieve_parameters(*total_inj_parameters)
        elif mode == 'rate':
            production = self.recieve_parameters(*rate_prod_parameters)
            injection = self.recieve_parameters(*rate_inj_parameters)
        else:
            raise ValueError
        production = reduce(lambda x, y: x + y, production)
        injection = reduce(lambda x, y: x + y, injection)
        rates = numpy.column_stack((production, injection))
        output = numpy.zeros_like(production, dtype="uint8")
        for year, rate in enumerate(rates):
            prod = rate[0]
            inj = rate[1]
            # inactiveness condition
            if inj + prod == 0 and  \
               year > self.first_run and year < self.abandonment:
                output[year] += 4
            elif inj + prod == 0 and \
                year > self.first_run and self.abandonment == "working":
                output[year] += 4
            elif inj > 0:
                    output[year] += 1
            elif prod > 0:
                    output[year] += 2
        if mode == 'total':
            self.classification = output
        elif mode == 'rate':
            self.classification_by_rate = output
        else:
            raise ValueError

    def inj_transfer_check(self):
        n = 0
        output = False
        a = numpy.roll(self.classification, -1)
        a = numpy.delete(a, -1)
        b = numpy.copy(self.classification)
        b = numpy.delete(b, -1)
        a = numpy.column_stack((a, b))
        for elem in a:
            nex = elem[0]
            cur = elem[1]
            n += 1
            if cur == 2 and nex == 1:
                output = n
                break
            if cur == 4 and nex == 1 and \
                (self.classification[self.first_run] == 2):
                output = n
                break
        return output

    def add_worktime(self, dates):
        # accepts numpy array as data
        def countMonth(self, data):
            m = 0
            k = 12 / len(data)
            for rate in data:
                if rate > 0:
                    m += 1 * k
            return m
        s_dates = sorted(dates.values())
        s_dates.pop(0)

        well_work_time = numpy.zeros(len(s_dates))
        parameters = self.recieve_parameters(*total_parameters)
        for data in parameters:

            a = data
            a = numpy.roll(a, -1) - a
            a = numpy.delete(a, -1)
            work_time = []
            for cur, nex in pairs(sorted(dates)):
                cur_line = dates[cur]
                next_line = dates[nex]
                sliced_data = a[cur_line:next_line]
                m = countMonth(cur, sliced_data)
                work_time.append(m)
            for i, val in enumerate(work_time):
                if val > well_work_time[i]:
                    well_work_time[i] = val
        self.work_time = well_work_time

    #  very very bad idea
    def compress_data(self, dates):
        for borehole in self.__boreholes.values():
            borehole.compress_data(dates)

    def clear(self):
        self.first_run = None
        self.abandonment = None
        self.work_time = None
        self.classification = None
        self.classification_by_rate = None
        for borehole in self.__boreholes.values():
            borehole.clear()


def pairs(lst):  # list generator
    i = iter(lst)
    prev = item = i.next()
    for item in i:
        yield prev, item
        prev = item

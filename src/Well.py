# -*- coding: UTF-8 -*-
'''
Created on 04.07.2012

@author: APartilov
'''


total_parameters = ['WOPT', 'WWPT', 'WGPT', 'WWIT', 'WOIT', 'WGIT']
total_prod_parameters = ['WOPT', 'WWPT', 'WGPT']
total_inj_parameters = ['WOIT', 'WWIT', 'WGIT']
total_dec_parameters = ['decWOPT', 'decWWPT', 'decWGPT',
                        'decWWIT', 'decWOIT', 'decWGIT']
rate_parameters = ['WLPR', 'WOIN', 'WWIN', 'WGIN']
rate_prod_parameters = ['WLPR']
rate_inj_parameters = ['WOIN', 'WWIN', 'WGIN']


class Well(object):
    '''
    classdocs
    '''
    dataline_length = 0
    mask = []

    def __init__(self, number, data={}):  # number
        '''
        Constructor
        '''
        self.name = number
        self.parameters = {}
        self.parameters.update(data)

        self.first_run = None
        self.abandonment = None
        self.work_time = None
        self.classification = None

#        for parameter in data:
#            if parameter in total_parameters:
#            self.add_worktime(parameter)

        '''
        Parameter length counter for class
        '''
        for datalist in data.values():
            if len(datalist) > self.__class__.dataline_length:
                self.__class__.dataline_length = len(datalist)
                self.__class__.mask = [0] * self.__class__.dataline_length

    def is_lateral(self):
        pass

    def compress_data(self):
        pass

    def add_parameter(self, parameter_code, data):
        self.parameters.update(data)

        for datalist in data.values():   # potentially to own def
            if len(datalist) > self.__class__.dataline_length:
                self.__class__.dataline_length = len(datalist)
                self.__class__.mask = [0] * self.__class__.dataline_length

    def recieve_parameters(self, *args):
        result = []  # и все-таки yield
        for arg in args:
            result.append(self.parameters.get(arg, self.__class__.mask))
        return result

    def abandonment_year(self):
#        for year in reversed(range(self.__class__.dataline_length)):
        #  Maybe this work
        for year, work_time in enumerate(reversed(self.work_time)):
            if work_time > 0:
                break
        if year == 0:
            self.abandonment = "working"
            return False
        self.last_call = len(work_time) - year
        return len(work_time) - year
        #  to last_call

    def completion_year(self):
        for year, work_time in enumerate(self.work_time):
            if work_time > 0:
                break
        # add oil well type
        if year == len(self.work_time) + 1:
            self.first_run = "None"
            return False
        self.first_run = year - 1
        return year - 1

    def well_classification(self):
        prod_parameters = self.recieve_parameters(*total_prod_parameters)
        production = list_sum(*prod_parameters)
        inj_parameters = self.recieve_parameters(*total_inj_parameters)
        injection = list_sum(*inj_parameters)
        output = self.__class__.mask
        for year, (prod, inj) in enumerate(zip(production, injection)):
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
        self.classification = output

    def inj_transfer_check(self):
        n = 0
        for cur, nex in pairs(self.classification):
            n += 1
            if cur == 2 and nex == 1:
                pass
            if cur == 4 and nex == 1 and self.type == "Production":
                pass
        return

    def add_worktime(self, data, wellcode):
        if wellcode in total_parameters:
            self.work_time = []
            for cur, nex in pairs(sorted(self.dates)):
                cur_line = self.dates[cur]
                next_line = self.dates[nex]
#                welldata.append(
#                    float(data[next_line]) - \
#                        float(data[cur_line]))
                m = self.countMonth(cur, data)
                self.work_time.append(m)

    def countMonth(self, pointer, data):
        m = 0
        start = self.dates[pointer]
        end = self.dates[pointer + 1]
        k = 12 / (end - start)
        for curr, nextt in pairs(range(end - start + 1)):
            if (float(data[nextt + start]) -
                    float(data[curr + start]) != 0):
                m += 1 * k
        return m

#        def cutter(self, number, start_p, end_p):  #  закомментировано до
#выяснения обстоятельств
#            if "Last_call" not in self.wells[number]:
#                return False
#            jan_mask = self.wells[number]["cls_mask_rate_jan"]
#            start_p = start_p - self.minimal_year
#            end_p = end_p - self.minimal_year
#            jan_mask = jan_mask[start_p:end_p]
#            return jan_mask


def pairs(lst):  # list generator
    i = iter(lst)
    prev = item = i.next()
    for item in i:
        yield prev, item
        prev = item


def list_sum(*args):  # сделать элегантнее
    length = len(args[0])
    for x in args:
        if len(x) != length:
            raise ValueError
    sum = []
    for x in range(length):
        s = 0
        for y in args:
            s += y[x]
        sum.append(s)
    return sum

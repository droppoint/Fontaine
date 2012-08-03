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
        for parameter in self.parameters:
            compress = list(self.parameters[parameter])
            self.parameters[parameter][:] = []
            if parameter in total_parameters:
                for cur_date, next_date in pairs(sorted(dates.values())):
                    value = float(compress[next_date]) - float(compress[cur_date])
                    self.parameters[parameter].append(value)
            else:
                s_dates = sorted(dates.values())
                s_dates.pop(0)
                self.__class__.short_mask = [0] * len(s_dates)
                for date in s_dates:
                    self.parameters[parameter].append(float(compress[date]))

    def recieve_parameter(self, code):
        return self.parameters.get(code)

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

#        for datalist in data.values():   # potentially to own def
#            len(datalist)
#            if len(datalist) > self.__class__.dataline_length:
#                self.__class__.dataline_length = len(datalist)
#                self.__class__.mask[:] = []
#                self.__class__.mask = [0] * self.__class__.dataline_length

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
            sum = None
            for borehole in self.__boreholes.values():
                if not sum:
                    exists = borehole.recieve_parameter(arg)
                    if exists:
                        sum = list(exists)  # слишком хитровыебано
                    continue
                sum = list_sum(sum, list(borehole.recieve_parameter(arg)))
            if sum == None:
                continue
#            yield (arg, sum)
            yield sum

    def well_classification(self, mode='total'):
        if mode == 'total':
            prod_parameters = self.recieve_parameters(*total_prod_parameters)
            inj_parameters = self.recieve_parameters(*total_inj_parameters)
        elif mode == 'rate':
            prod_parameters = self.recieve_parameters(*rate_prod_parameters)
            inj_parameters = self.recieve_parameters(*rate_inj_parameters)
        else:
            raise ValueError
        production = list_sum(*prod_parameters)
        injection = list_sum(*inj_parameters)
        output = list(self.__class__.short_mask)
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
        if mode == 'total':
            self.classification = output
        elif mode == 'rate':
            self.classification_by_rate = output
        else:
            raise ValueError

    def inj_transfer_check(self):
        n = 0
        output = False
        for cur, nex in pairs(self.classification):
            n += 1
            if cur == 2 and nex == 1:
                output = n
                break
            if cur == 4 and nex == 1 and self.classification[self.first_run] == 2:
                output = n
                break
        return output

    def add_worktime(self, dates):
        def countMonth(self, data):
            m = 0
            k = 12 / len(data)
            for rate in data:
                if float(rate) > 0:
                    m += 1 * k
            return m
        s_dates = sorted(dates.values())    # не элегантно
        s_dates.pop(0)
        self.__class__.short_mask = [0] * len(s_dates)
        well_work_time = list(self.__class__.short_mask)
        parameters = self.recieve_parameters(*total_parameters)
        for data in parameters:
            s_data = []
            for cur_total, next_total in pairs(data):  # не элегантно
                s_data.append(float(next_total) - float(cur_total))
            work_time = []
            for cur, nex in pairs(sorted(dates)):
                cur_line = dates[cur]
                next_line = dates[nex]
                sliced_data = s_data[cur_line:next_line:]
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
    list_sum = []
    for x in range(length):
        s = 0
        for y in args:
            s += float(y[x])
        list_sum.append(s)
    return list_sum

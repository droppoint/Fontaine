# -*- coding: UTF-8 -*-
'''
Created on 04.07.2012

@author: APartilov
'''

from Field import Field

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

    def add_parameter(self, data):
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



#        def cutter(self, number, start_p, end_p):  #  закомментировано до выяснения обстоятельств
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



    #  GARBAGE,  а выбросить жалко
#        if 'Lateral' in self.wells[number]:
#            for wells in self.wells[number]['Lateral']:
#                oil_prod2 = self.recieveLine(wells, 'WOPT')
#                water_prod2 = self.recieveLine(wells, 'WWPT')
#                gas_prod2 = self.recieveLine(wells, 'WGPT')
#                water_inj2 = self.recieveLine(wells, 'WWIT')
#                oil_inj2 = self.recieveLine(wells, 'WOIT')
#                gas_inj2 = self.recieveLine(wells, 'WGIT')
#                oil_prod = list(map(lambda x, y: x + y, oil_prod, oil_prod2))
#                water_prod = list(map(lambda x, y: x + y,
#                                      water_prod, water_prod2))
#                gas_prod = list(map(lambda x, y: x + y, gas_prod, gas_prod2))
#                oil_inj = list(map(lambda x, y: x + y, oil_inj, oil_inj2))
#                water_inj = list(map(lambda x, y: x + y,
#                                     water_inj, water_inj2))
#                gas_inj = list(map(lambda x, y: x + y, gas_inj, gas_inj2))

#        if ("L_Borholes" in self.parameters) and \
#            (number in self.parameters["L_Borholes"]):
#            return False
#        if not number in self.wells:
#            return False

#        def recieveLine(self, number, code):
#            if code in self.wells[number]:
#                return self.wells[number][code]
#            else:
#                mask = list(self.mask)
#                mask.remove(0)
#                return list(mask)

#    def add_worktime(self, number, data):   #   ????????
#        if not number in self.wells:
#            self.wells[number] = {}
#        if not 'In_work' in self.wells[number]:
#            self.wells[number]['In_work'] = data
#        else:
#            self.wells[number]['In_work'] = list(map(
#                                lambda x, y: x > y and x or y,
#                                self.wells[number]['In_work'],
#                                data))

#        '''
#        Recieving parameters and store it into parameters dict
#        '''
#        parameters = self.recieve_parameters(*total_parameters)
#        mask = list(self.mask)

##        over = kwargs.get('year')
##        if not number in self.wells:
##            self.wells[number] = {}
#
##        if not 'In_work' in self.parameters:
##            self.wells[number]['First_run'] = ('N/A', "Dummy", 0)
##            for wells in self.wells[number]["Lateral"]:   # new well check
##                if (self.wells[wells]['First_run'][0] < self.wells[number]['First_run']) and \
##                    self.wells[wells]['First_run'][0] > 0:
##                    self.wells[number]['First_run'] = (self.wells[wells]['First_run'][0],
##                                                       "Dummy",
##                                                       self.wells[wells]['First_run'][2])
##            return
#        for i, key in enumerate(self.parameters['In_work']):
##            if over:
##                i = over - self.minimal_year
##                key = self.wells[number]['In_work'][i]
#            if (oil_inj[i] + water_inj[i] + gas_inj[i]) > 0:
#                self.parameters['First_run'] = (i + self.minimal_year,
#                                                   "Injection",
#                                                   key)
#                mask[i] += 1
##                if ("L_Borholes" in self.parameters) and \
##                  (number in self.parameters["L_Borholes"]):
##                    self.add_parameter('NLB', mask)
##                else:
##                    self.add_parameter('NIW', mask)
#                return
#            elif (oil_prod[i] + water_prod[i] + gas_prod[i]) > 0:
#                self.first_run = (i + self.minimal_year,
#                                                   "Production",
#                                                   key)
#                mask[i] += 1
#
##                if ("L_Borholes" in self.parameters) and \
##                  (number in self.parameters["L_Borholes"]):  # bad spot
##                    self.add_parameter('NLB', mask)
##                else:
##                    self.add_parameter('NPW', mask)
##                    mask = list(self.mask)
##                    mask[i] += oil_prod[i]
##                    self.add_parameter("NOPT", mask)  # bad code
##
##                    mask = list(self.mask)
##                    mask[i] += water_prod[i]
##                    self.add_parameter("NWPT", mask)
#
#                return
#
#        self.first_run = ('N/A', "Exploratory", 0)

#        def well_classification2(self, number):  # FIXME: BAD MASK
#            if number in self.wells:
#                oil_inj = self.recieveLine(number, 'decWOIT')   # FIXME: To array
#                oil_prod = self.recieveLine(number, 'decWOPT')
#                gas_prod = self.recieveLine(number, 'decWGPT')
#                water_prod = self.recieveLine(number, 'decWWPT')
#                water_inj = self.recieveLine(number, 'decWWIT')
#                gas_inj = self.recieveLine(number, 'decWGIT')
#                output = [0 for unused_well in oil_prod]
#                for year, (oil_p, water_p, gas_p, water_i, oil_i, gas_i) in enumerate(
#                            zip(oil_prod, water_prod, gas_prod, oil_inj, water_inj, gas_inj)):
#                    if (water_i + oil_i + gas_i) > 0:
#                            output[year] += 1
#                    elif (oil_p + water_p + gas_p) > 0:
#                            output[year] += 2
#                self.wells[number]['cls_mask_dec'] = output
#            else:
#                return False
#
#        def well_classification3(self, number):  # BAD MASK
#            if number in self.wells:
#                liq_prod = self.recieveLine(number, 'WLPR')  # FIXME: To array
#                oil_inj = self.recieveLine(number, 'WOIN')
#                water_inj = self.recieveLine(number, 'WWIN')
#                gas_inj = self.recieveLine(number, 'WGIN')
#                output = [0 for unused_well in liq_prod]
#                for year, (liq_p, water_i, oil_i, gas_i) in enumerate(
#                            zip(liq_prod, water_inj, oil_inj, gas_inj)):
#                    if (water_i + oil_i + gas_i) > 0:
#                            output[year] += 1
#                    elif (liq_p) > 0:
#                            output[year] += 2
#                self.wells[number]['cls_mask_rate_jan'] = output
#            else:
#                return False
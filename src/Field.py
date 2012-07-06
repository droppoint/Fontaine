# -*- coding: UTF-8 -*-
'''
Created on 24.04.2012

@author: APartilov
'''
from Well import Well


# FIXME: expressions
class Singleton(type):
    '''
    Singleton class for creating 1 uniquie instance with
    1 input point
    '''
    def __init__(cls, name, bases, dictationary):
        super(Singleton, cls).__init__(name, bases, dictationary)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class Field(object):  # FIXME: More docstrings
    '''
    Storage for wellfield and wells data.
    Store data in dicts "wells" and "parameters"
    '''
    __metaclass__ = Singleton

    def __init__(self, name, dates_list):

        def set_dates_list(self, dates):
            self.dates = dates
            self.minimal_year = min(self.dates.keys())

        self.name = name
        self.wells = []
        self.parameters = {}
        self.mask = []  # может по датам?
        self.set_dates_list(dates_list)

    def add_well(self, number, parameter_code, data, **kwargs):
        if number in self.wells:  # ошибочка будет полюбому
            self.wells[number].add_parameter(parameter_code, data)
        else:
            self.wells.append(
                Well(number, parameter_code, data)  # может без parameter code?
                              )
#        shrt_num = re.findall(r"^([0-9A-Z]+)(?=BS|[_-])", number)
#        if shrt_num:
#            pass

    def add_parameter(self, parameter, data):
        if parameter == "FPR":
            parameter = "FPRP"
        if parameter == "FPRP":
            data.pop(0)
        if not parameter in self.parameters:
            self.parameters[parameter] = list(data)
        else:
            self.parameters[parameter] = list(map(lambda x, y: x + y,
                                     self.parameters[parameter], data))

    def production_rate(self, code):
        rate = []
        for wells in self.wells.values():  #  без values
            if code in wells:
                if not rate:
                    rate = list(wells[code])
                else:
                    rate = list(map(lambda x, y: x + y, wells[code], rate))
        return rate

    def well_fond(self, code):   # коды состояний 0.1.2.4
        wells_fond = list(self.mask)
        wells_fond.remove(0)
        for year, unused_item in enumerate(wells_fond):
            for well in self.wells:  # rework
                if ("L_Borholes" in self.parameters) and \
                  (well in self.parameters["L_Borholes"]):
                    continue
                if self.wells[well]['cls_mask_rate_jan'][year] == code:
                    wells_fond[year] += 1
                elif 'Lateral' in self.wells[well]:
                    for wells in self.wells[well]['Lateral']:
                        if self.wells[wells]['cls_mask_rate_jan'][year] == code:
                            wells_fond[year] += 1
                            break
        return wells_fond

    def avg_pressure(self, pres_type):
        mask = list(self.mask)
        mask.remove(0)
        avg_inj_pres = list(mask)  # проверить маску
        avg_prod_pres = list(mask)
        for num in range(len(mask)):
            pres_prod, pres_inj = 0, 0
            count_prod, count_inj = 0, 0
            for well in self.wells.values():
                if pres_type in well:
                    if well['cls_mask'][num] == 2:
                        pres_prod += well[pres_type][num]
                        count_prod += 1
                    elif well['cls_mask'][num] == 1:
                        pres_inj += well[pres_type][num]
                        count_inj += 1
            if count_prod != 0:
                avg_prod_pres[num] += pres_prod / count_prod
            if count_inj != 0:
                avg_inj_pres[num] += pres_inj / count_inj
        return avg_prod_pres, avg_inj_pres

    def dummyCheck(self):   # rework
        for well in self.wells:
            if not self.wells[well]['First_run'][1] == 'Dummy':
                continue
            if not "Lateral" in self.wells[well]:
                continue
            for lateral in self.wells[well]["Lateral"]:
                year = self.wells[lateral]['First_run'][0]
                index = int(year) - self.minimal_year
                worktime = self.wells[well]['First_run'][2]
#                if ((year <  self.wells[well]['First_run'][0])
#                        and self.wells[well]['First_run'][0] > 0) \
#                    or (self.wells[well]['First_run'][0] == "N/A"):
                self.parameters["NOPT"][index] += self.wells[lateral]['WOPT'][index]
                self.parameters["NWPT"][index] += self.wells[lateral]['WWPT'][index]
                self.parameters["NPW"][index] += 1

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

    def clear(self):
        self.wells.clear()
        self.parameters.clear()
        self.mask = []
        self.minimal_year = 0

def pairs(lst):  # list generator
    i = iter(lst)
    prev = item = i.next()
    for item in i:
        yield prev, item
        prev = item

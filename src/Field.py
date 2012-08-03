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


class FieldError(Exception):
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


class Field(object):  # FIXME: More docstrings
    '''
    Storage for wellfield and wells data.
    Store data in dicts "wells" and "parameters"
    '''
#    __metaclass__ = Singleton
#    __slots__ = {'name', 'wells', 'parameters', 'mask'
#                 'dates'}
    def __init__(self, name, dates_dict):

        def set_dates_list(self, dates):
            self.dates = dates
            self.mask = [0 for _ in self.dates]

        self.name = name
        self.wells = {}
        self.parameters = {}
        set_dates_list(self, dates_dict)

    def __call__(self):
        return self.name

    def add_well(self, number, data={}, **kwargs):
        import re
        print number
        shrt_num = re.search(r"^([0-9A-Z]+)(?=BS|[_-])", number)  # rework interfaces
        if shrt_num:
            parent_number = shrt_num.group()
            if not parent_number in self.wells:
                self.wells[parent_number] = Well()
            self.wells[parent_number].add_parameter(number, data)
            return

        if not number in self.wells:
            self.wells[number] = Well()
        self.wells[number].add_parameter(number, data)

    def add_parameter(self, parameter, data):
        if parameter == "FPR":
            parameter = "FPRP"
#        if parameter == "FPRP":
#            data.pop(0)
        if not parameter in self.parameters:
            tmp = []                                    # не совсем элегантно
            for year in sorted(self.dates.values()):
                tmp.append(data[year])
            self.parameters[parameter] = tmp
        else:
            raise FieldError("Repeated parameters")

    def routine_operations(self):
        map(lambda x: Well.add_worktime(x, dates=self.dates),
            self.wells.values())
        map(lambda x: Well.compress_data(x, dates=self.dates),
            self.wells.values())
        map(Well.abandonment_year, self.wells.values())
        map(Well.completion_year, self.wells.values())
        map(Well.well_classification, self.wells.values())
        map(lambda x: Well.well_classification(x, mode='rate'),
             self.wells.values())
        map(Well.inj_transfer_check, self.wells.values())

    def production_rate(self, code, density=1, degree=0):
        rate = []
        for well in self.wells.values():
            for data in well.recieve_parameters(code):
                if data:
                    if not rate:
                        rate = data
                    else:
                        tmp_rate = list(rate)
                        rate = []
                        for a, b in zip(tmp_rate, data):
                            rate.append(a + b)
        return [x * density * (10 ** degree) for x in rate]

    def new_well_rate(self, code, density=1, degree=0):
        rate = list(self.mask)
        for well in self.wells.values():  # без values
            for data in well.recieve_parameters(code):
                if data:
                    rate[well.first_run] += data[well.first_run]
        return [x * density * (10 ** degree) for x in rate]

    def new_well_work_time(self):
        work_time = list(self.mask)
        for well in self.wells.values():  # без values
            work_time[well.first_run] += well.work_time[well.first_run]
        return work_time

    def completed_wells(self, code='all'):
        output = list(self.mask)
        for well in self.wells.values():
            if code == 'all':
                output[well.first_run] += 1
            elif well.classification[well.first_run] == code:
                output[well.first_run] += 1
        return output

    def abandoned_wells(self, code='all'):
        output = list(self.mask)
        for well in self.wells.values():
            if well.abandonment == 'working':
                continue
            if code == 'all':
                output[well.abandonment] += 1
            elif well.classification[well.abandonment] == code:
                output[well.abandonment] += 1
        return output

    def transfered_wells(self):
        output = list(self.mask)
        for well in self.wells.values():
            n = well.inj_transfer_check()
            if n:
                output[n] += 1
        return output

    def inactive_transfer(self):
        in_prod, in_inje, out_prod, out_inje = \
        list(self.mask), list(self.mask), list(self.mask), list(self.mask)
        for well in self.wells.values():
            n = 0
            for cur_state, next_state in pairs(well.classification_by_rate):
                if cur_state == 1 and next_state == 4:
                    out_inje[n] += 1
                if cur_state == 4 and next_state == 1:
                    in_inje[n] += 1
                if cur_state == 2 and next_state == 4:
                    out_prod[n] += 1
                if cur_state == 4 and next_state == 2:
                    in_prod[n] += 1
                n += 1
        return in_prod, out_prod, in_inje, out_inje

    def work_time(self, code='all'):  # не элегантно
        output = list(self.mask)
        for well in self.wells.values():
            if code == 'new':
                output[well.first_run] += well.work_time[well.first_run]
            else:
                for year, worktime in enumerate(well.work_time):
                    if code == 'all':
                        output[year] += worktime
                    elif well.classification[year] == code:
                        output[year] += worktime
        return output

    def well_fond(self, code):   # коды состояний 0.1.2.4
        wells_fond = list(self.mask)
        wells_fond.pop(0)
        for well in self.wells.values():
            for year, _ in enumerate(wells_fond):
                if well.classification_by_rate[year] == code:
                    wells_fond[year] += 1
        return wells_fond

    def avg_pressure(self, pres_type):
        mask = list(self.mask)
        mask.pop(0)
        avg_inj_pres = list(mask)  # проверить маску
        avg_prod_pres = list(mask)
        for num in range(len(mask)):
            pres_prod, pres_inj = 0, 0
            count_prod, count_inj = 0, 0
            for well in self.wells.values():  # деление на well_fond
                for data in well.recieve_parameters(pres_type):
                    if data:
                        if well.classification_by_rate[num] == 2:
                            pres_prod += data[num]
                            count_prod += 1
                        elif well.classification_by_rate[num] == 1:
                            pres_inj += data[num]
                            count_inj += 1
            if count_prod != 0:
                avg_prod_pres[num] += pres_prod / count_prod
            if count_inj != 0:
                avg_inj_pres[num] += pres_inj / count_inj
        return avg_prod_pres, avg_inj_pres

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


def pairs(lst):  # list generator
    i = iter(lst)
    prev = item = i.next()
    for item in i:
        yield prev, item
        prev = item

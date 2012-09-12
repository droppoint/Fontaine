# -*- coding: UTF-8 -*-
'''
Created on 24.04.2012

@author: APartilov
'''
from Well import Well
import Parser
import numpy


class FieldError(Exception):
    """Exception raised for all parse errors."""

    def __init__(self, msg, well=None, parameter=None):
        assert msg
        self.msg = msg
        self.well = well
        self.parameter = parameter

    def __str__(self):
        result = self.msg
        if self.well is not None:
            result = result + " at well" + self.well
        if self.parameter is not None:
            result = result + " at parameter" + self.parameter
        return result


class Field(object):  # FIXME: More docstrings
    '''
    Storage for wellfield and wells data.
    Store data in dicts "wells" and "parameters"
    '''
#    __metaclass__ = Singleton
#    __slots__ = {'name', 'wells', 'parameters', 'mask'
#                 'dates'}
    def __init__(self):
#        self.name = name
        self.wells = {}
        self.parameters = {}
        self.lateral_detect(True)   # Костыль
        self.limit = {}
        self._mObservers = []

#    def __call__(self):
#        return self.name
    def set_dates_list(self, dates):
        self.dates = dates
        self.mask = [0 for _ in self.dates]
    '''
    add_observer, remove_observer и notify_observer -
    процедуры реализующие паттерн "Наблюдатель".
    '''
    def add_observer(self, inObserver):
        self._mObservers.append(inObserver)

    def remove_observer(self, inObserver):
        self._mObservers.remove(inObserver)

    def notify_observers(self, signal=None):
        for x in self._mObservers:
            x.model_is_changed(signal)

    def cut_off_wells(self):
        well_list = list(self.wells.keys())
        for well in well_list:
            if well not in self.limit:
                del self.wells[well]

    def process_data(self):
        '''
        Получение данных из источника и заполнение модели
        '''
        from time import time
        self.notify_observers(signal=('start', 0))
        t1 = time()
        parsed_data = self.parser.parse_file()
        for row in parsed_data:
            progress = self.parser.report_progress()
            self.notify_observers(signal=('progress', progress))
            if row['number'] == 'N/A':
                self.add_parameter(row['parameter_code'],
                                      row['welldata'])
            else:
                self.add_well(row['number'],
                    {row['parameter_code']: row['welldata']})
        print time() - t1
        if self.limit:
            self.cut_off_wells()
        self.routine_operations()
        print time() - t1
        self.notify_observers(signal=('complete', 0))

    def add_file_for_parsing(self, filename):
        self.parser = Parser.Parser(filename)
        self.set_dates_list(self.parser.get_dates_list())

    def lateral_detect(self, state):
        self.__lateral = state

    def add_well(self, number, data={}, **kwargs):
        import re
        if self.__lateral:
            shrt_num = re.search(r"^([0-9A-Z]+)(?=(?:BS|B)|(?:[-_]\d{1}))",
                                 number)
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
            raise FieldError("Repeated field parameters",
                             parameter=str(parameter))

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
        rate = None
        for well in self.wells.values():
            for data in well.recieve_parameters(code):
                if data != None:
                    if rate == None:
                        rate = data
                    else:
                        rate = rate + data
        return rate * density * 10 ** degree

    def new_well_rate(self, code, density=1, degree=0):
        rate = numpy.array(self.mask)
        for well in self.wells.values():  # без values
            for data in well.recieve_parameters(code):
                if data != None:
                    rate[well.first_run] += data[well.first_run]
        return rate * density * (10 ** degree)

    def new_well_work_time(self):
        work_time = numpy.array(self.mask)
        for well in self.wells.values():  # без values
            work_time[well.first_run] += well.work_time[well.first_run]
        return work_time

    def completed_wells(self, code='all'):
        output = numpy.array(self.mask, dtype="int16")
        for well in self.wells.values():
            if code == 'all':
                output[well.first_run] += 1
            elif well.classification[well.first_run] == code:
                output[well.first_run] += 1
        return output

    def abandoned_wells(self, code='all'):
        output = numpy.array(self.mask, dtype="int16")
        for well in self.wells.values():
            if well.abandonment == 'working':
                continue
            if code == 'all':
                output[well.abandonment] += 1
            elif well.classification[well.abandonment] == code:
                output[well.abandonment] += 1
        return output

    def transfered_wells(self):
        output = numpy.array(self.mask, dtype="int16")
        for well in self.wells.values():
            n = well.inj_transfer_check()
            if n:
                output[n] += 1
        return output

    def inactive_transfer(self):
        result = None
        for well in self.wells.values():
            if result == None:
                result = numpy.zeros_like(well.classification_by_rate, dtype="int32")
                result = numpy.vstack((result, result, result, result))
        a = numpy.roll(well.classification_by_rate, -1)
        a = numpy.delete(a, -1)
        b = numpy.copy(well.classification_by_rate)
        b = numpy.delete(b, -1)
        a = numpy.column_stack((a, b))
        n = 0
        for elem in a:
            cur = elem[0]
            nex = elem[1]
            if cur == 4 and nex == 2:
                result[0][n] += 1
            if cur == 2 and nex == 4:
                result[1][n] += 1
            if cur == 4 and nex == 1:
                result[2][n] += 1
            if cur == 1 and nex == 4:
                result[3][n] += 1
            n += 1
        return result

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
        wells_fond = None
        for well in self.wells.values():
            if wells_fond == None:
                wells_fond = numpy.zeros_like(well.classification_by_rate)
                wells_fond = numpy.delete(wells_fond, -1)
            for year, _ in enumerate(wells_fond):
                if well.classification_by_rate[year] == code:
                    wells_fond[year] += 1
        return wells_fond

    def borehole_fond(self):
        years = []
        for well in self.wells:
            years += self.wells[well].borehole_input(well)
        fond = list(self.mask)
        for year in years:
            fond[year] += 1
        return fond

    def avg_pressure(self, pres_type):
        mask = list(self.mask)  # плохо
        avg_inj_pres = numpy.array(mask, dtype="float32")
        avg_prod_pres = numpy.array(mask, dtype="float32")
        count_prod = numpy.array(mask, dtype="int16")
        count_inj = numpy.array(mask, dtype="int16")
        for well in self.wells.values():  # деление на well_fond
            pressure = well.recieve_parameters(pres_type)
            pressure = reduce(lambda x, y: x + y, pressure)
            for year, pres in enumerate(pressure):
                if well.classification_by_rate[year] == 2:
                    avg_prod_pres[year] += pres
                    count_prod[year] += 1
                elif well.classification_by_rate[year] == 1:
                    avg_inj_pres[year] += pres
                    count_inj[year] += 1
        numpy.seterr(divide="ignore")
        avg_prod_pres = avg_prod_pres / count_prod
        avg_prod_pres = numpy.nan_to_num(avg_prod_pres)
        avg_prod_pres = numpy.delete(avg_prod_pres, 0)
        avg_inj_pres = avg_inj_pres / count_inj
        avg_inj_pres = numpy.nan_to_num(avg_inj_pres)
        avg_inj_pres = numpy.delete(avg_inj_pres, 0)
        return avg_prod_pres, avg_inj_pres

    def clear(self):
        for well in self.wells.values():
            well.clear()
        self.parameters.clear()
        self.mask = []

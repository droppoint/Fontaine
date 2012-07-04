'''
Created on 24.04.2012

@author: APartilov
'''


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
    wells = {}
    parameters = {}
    mask = []
    minimal_year = 0

    def set_dates_list(self, dates):
        self.dates = dates
        self.minimal_year = min(self.dates.keys())

    def add_well(self, number, well_code, data, **kwargs):
        import re
        lateral = kwargs.get('lateral')

        def countMonth(pointer, data):
            m = 0
            start = self.dates[pointer]
            end = self.dates[pointer + 1]
            k = 12 / (end - start)
            for curr, nextt in pairs(range(end - start + 1)):
                if (float(data[nextt + start]) -
                        float(data[curr + start]) != 0):
                    m += 1 * k
            return m
        if not number in self.wells:
            self.wells[number] = {}
#            self.cls_logger.info(number)
#            self.cls_logger.info('pass')
        if lateral:
            shrt_num = re.findall(r"^([0-9A-Z]+)(?=BS|[_-])", number)
            if shrt_num:
                if not shrt_num[0] in self.wells:   # FIXME: conditions
                    self.wells[shrt_num[0]] = {}
                if not "Lateral" in self.wells[shrt_num[0]]:
                    self.wells[shrt_num[0]]["Lateral"] = []
                if not number in self.wells[shrt_num[0]]["Lateral"]:
                    self.wells[shrt_num[0]]["Lateral"].append(number)
                if not "L_Borholes" in self.parameters:
                    self.parameters["L_Borholes"] = []
                if not number in self.parameters["L_Borholes"]:
                    self.parameters["L_Borholes"].append(number)
        if not self.mask:
            self.mask = [0 for unused_item in self.dates]
        if re.match(r"^(W[O|G|W][I|P]T)$", well_code):
            welldata = []
            worktime = []
            welldata_dec = []
            for cur, nex in pairs(sorted(self.dates)):
                cur_line = self.dates[cur]
                next_line = self.dates[nex]
                welldata.append(
                    float(data[next_line]) - \
                        float(data[cur_line]))
                m = countMonth(cur, data)
                worktime.append(m)
            self.add_worktime(number, worktime)

            dec_dates = sorted(self.dates)
            dec_dates.pop(0)
            for cur in dec_dates:  # december pattern
                if self.dates[cur] == 0:
                    cur.next()
                cur_line = self.dates[cur] - 1
                next_line = self.dates[cur]
                welldata_dec.append(
                    float(data[next_line]) - \
                        float(data[cur_line]))

            if not well_code in self.wells[number]:
                self.wells[number][well_code] = welldata
                self.wells[number]["dec" + well_code] = welldata_dec
            else:  # bad code
                self.wells[number][well_code] = list(map(lambda x, y: x + y,
                                self.wells[number][well_code], welldata))
                self.wells[number]["dec" + well_code] = list(map(lambda x, y: x + y,
                                self.wells[number]["dec" + well_code], welldata_dec))
                print "lateral indeed", number, well_code
            if not "First_run" in self.wells[number]:
                self.wells[number]['First_run'] = ('N/A', "Exploratory", 0)

        if re.match(r"^(WBPN|WBHP|W[O|G|W|L][I|P][R|N])$", well_code):
            welldata = []
            for year in sorted(self.dates.values()):
                welldata.append(float(data[year]))
            welldata.pop(0)  # december pattern
            self.wells[number][well_code] = welldata

    def get_well(self, wellname):
        if wellname in self.wells:
            return self.wells[wellname]
        else:
            return False

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
        for wells in self.wells.values():
            if code in wells:
                if not rate:
                    rate = list(wells[code])
                else:
                    rate = list(map(lambda x, y: x + y, wells[code], rate))
        return rate

    def well_fond(self, code):
        wells_fond = list(self.mask)
        wells_fond.remove(0)
        for year, unused_item in enumerate(wells_fond):
            for well in self.wells:
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
        avg_inj_pres = list(mask)
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

    def dummyCheck(self):
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

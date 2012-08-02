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


class WellStorage(object):  # FIXME: More docstrings
    '''
    Storage for wellfield and wells data.
    Store data in dicts "wells" and "parameters"
    '''
    __metaclass__ = Singleton
    wells = {}
    parameters = {}
    mask = []
    minimal_year = 0

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

    def add_worktime(self, number, data):
        if not number in self.wells:
            self.wells[number] = {}
        if not 'In_work' in self.wells[number]:
            self.wells[number]['In_work'] = data
        else:
            self.wells[number]['In_work'] = list(map(
                                lambda x, y: x > y and x or y,
                                self.wells[number]['In_work'],
                                data))

    def well_classification(self, number):  # BAD MASK
        if number in self.wells:
            oil_inj = self.recieveLine(number, 'WOIT')  # FIXME: To array
            oil_prod = self.recieveLine(number, 'WOPT')
            gas_prod = self.recieveLine(number, 'WGPT')
            water_prod = self.recieveLine(number, 'WWPT')
            water_inj = self.recieveLine(number, 'WWIT')
            gas_inj = self.recieveLine(number, 'WGIT')
            output = [0 for unused_well in oil_prod]
            for year, (oil_p, water_p, gas_p, water_i, oil_i, gas_i) in enumerate(
                        zip(oil_prod, water_prod, gas_prod, oil_inj, water_inj, gas_inj)):
                if (water_i + oil_i + gas_i) > 0:
                        output[year] += 1
                elif (oil_p + water_p + gas_p) > 0:
                        output[year] += 2
            self.wells[number]['cls_mask'] = output
        else:
            return False

    def well_classification2(self, number):  # FIXME: BAD MASK
        if number in self.wells:
            oil_inj = self.recieveLine(number, 'decWOIT')   # FIXME: To array
            oil_prod = self.recieveLine(number, 'decWOPT')
            gas_prod = self.recieveLine(number, 'decWGPT')
            water_prod = self.recieveLine(number, 'decWWPT')
            water_inj = self.recieveLine(number, 'decWWIT')
            gas_inj = self.recieveLine(number, 'decWGIT')
            output = [0 for unused_well in oil_prod]
            for year, (oil_p, water_p, gas_p, water_i, oil_i, gas_i) in enumerate(
                        zip(oil_prod, water_prod, gas_prod, oil_inj, water_inj, gas_inj)):
                if (water_i + oil_i + gas_i) > 0:
                        output[year] += 1
                elif (oil_p + water_p + gas_p) > 0:
                        output[year] += 2
            self.wells[number]['cls_mask_dec'] = output
        else:
            return False

    def well_classification3(self, number):  # BAD MASK
        if number in self.wells:
            liq_prod = self.recieveLine(number, 'WLPR')  # FIXME: To array
            oil_inj = self.recieveLine(number, 'WOIN')
            water_inj = self.recieveLine(number, 'WWIN')
            gas_inj = self.recieveLine(number, 'WGIN')
            output = [0 for unused_well in liq_prod]
            for year, (liq_p, water_i, oil_i, gas_i) in enumerate(
                        zip(liq_prod, water_inj, oil_inj, gas_inj)):
                if (water_i + oil_i + gas_i) > 0:
                        output[year] += 1
                elif (liq_p) > 0:
                        output[year] += 2
            self.wells[number]['cls_mask_rate_jan'] = output
        else:
            return False

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

    def recieveLine(self, number, code):
        if code in self.wells[number]:
            return self.wells[number][code]
        else:
            mask = list(self.mask)
            mask.remove(0)
            return list(mask)

    def output_well(self, number):  # !!! Rework
        if ("L_Borholes" in self.parameters) and \
            (number in self.parameters["L_Borholes"]):
            return False
        if not number in self.wells:
            return False
        oil_prod = self.recieveLine(number, 'WOPT')  # FIXME: To array
        water_prod = self.recieveLine(number, 'WWPT')
        gas_prod = self.recieveLine(number, 'WGPT')
        water_inj = self.recieveLine(number, 'WWIT')
        oil_inj = self.recieveLine(number, 'WOIT')
        gas_inj = self.recieveLine(number, 'WGIT')
        if 'Lateral' in self.wells[number]:
            for wells in self.wells[number]['Lateral']:
                oil_prod2 = self.recieveLine(wells, 'WOPT')
                water_prod2 = self.recieveLine(wells, 'WWPT')
                gas_prod2 = self.recieveLine(wells, 'WGPT')
                water_inj2 = self.recieveLine(wells, 'WWIT')
                oil_inj2 = self.recieveLine(wells, 'WOIT')
                gas_inj2 = self.recieveLine(wells, 'WGIT')
                oil_prod = list(map(lambda x, y: x + y, oil_prod, oil_prod2))
                water_prod = list(map(lambda x, y: x + y,
                                      water_prod, water_prod2))
                gas_prod = list(map(lambda x, y: x + y, gas_prod, gas_prod2))
                oil_inj = list(map(lambda x, y: x + y, oil_inj, oil_inj2))
                water_inj = list(map(lambda x, y: x + y,
                                     water_inj, water_inj2))
                gas_inj = list(map(lambda x, y: x + y, gas_inj, gas_inj2))
        welltype = False  # false means production well
        for year in reversed(range(len(oil_prod))):  # change to mask
            if water_inj[year] + oil_inj[year] + gas_inj[year] > 0:
                welltype = True
                if "In_work" in self.wells[number]:
                    self.wells[number]["Last_call"] = [
                                            year + self.minimal_year,
                                            "Injection",
                                            self.wells[number]['In_work'][year]
                                            ]
                break
            elif oil_prod[year] + water_prod[year] + gas_prod[year] > 0:
                welltype = False
                if "In_work" in self.wells[number]:
                    self.wells[number]["Last_call"] = [
                                        year + self.minimal_year,
                                        "Production",
                                        self.wells[number]['In_work'][year]
                                        ]
                break
        if year == len(oil_prod) - 1:
            return False
        return year, welltype

    def inj_transfer_check(self, number):
        mask = list(self.mask)
        first_run = self.wells[number]['First_run']
        if number in self.wells:
            cls_mask = self.recieveLine(number, 'cls_mask')
            n = 0
            for cur, nex in pairs(cls_mask):
                n += 1
                if cur == 2 and nex == 1:
                    mask[n] += 1
                    self.wells[number]['First_run'] = (first_run[0],
                                     "Production_transfered", first_run[2])
                if cur == 0 and nex == 1 and first_run[1] == "Production":
                    mask[n] += 1
                    self.wells[number]['First_run'] = (first_run[0],
                                     "Production_transfered", first_run[2])
            return mask

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

    def add_First_Year(self, number, **kwargs):   # HARD REWORK
        mask = list(self.mask)
        over = kwargs.get('year')
        if not number in self.wells:
            self.wells[number] = {}
        self.wells[number]['First_run'] = ()
        oil_prod = self.recieveLine(number, 'WOPT')  # FIXME: To array
        water_prod = self.recieveLine(number, 'WWPT')
        gas_prod = self.recieveLine(number, 'WGPT')
        water_inj = self.recieveLine(number, 'WWIT')
        oil_inj = self.recieveLine(number, 'WOIT')
        gas_inj = self.recieveLine(number, 'WGIT')
        if not 'In_work' in self.wells[number]:
#            self.wells[number]['First_run'] = ('N/A', "Dummy", 0)
            for wells in self.wells[number]["Lateral"]:   # new well check
                if (self.wells[wells]['First_run'][0] < self.wells[number]['First_run']) and \
                    self.wells[wells]['First_run'][0] > 0:
                    self.wells[number]['First_run'] = (self.wells[wells]['First_run'][0],
                                                       "Dummy",
                                                       self.wells[wells]['First_run'][2])
            return
        for i, key in enumerate(self.wells[number]['In_work']):
#            if over:
#                i = over - self.minimal_year
#                key = self.wells[number]['In_work'][i]
            if (oil_inj[i] + water_inj[i] + gas_inj[i]) > 0:
                self.wells[number]['First_run'] = (i + self.minimal_year,
                                                   "Injection",
                                                   key)
                mask[i] += 1
                if ("L_Borholes" in self.parameters) and \
                  (number in self.parameters["L_Borholes"]):
                    self.add_parameter('NLB', mask)
                else:
                    self.add_parameter('NIW', mask)
                return
            elif (oil_prod[i] + water_prod[i] + gas_prod[i]) > 0:
                self.wells[number]['First_run'] = (i + self.minimal_year,
                                                   "Production",
                                                   key)
                mask[i] += 1

                if ("L_Borholes" in self.parameters) and \
                  (number in self.parameters["L_Borholes"]):  # bad spot
                    self.add_parameter('NLB', mask)
                else:
                    self.add_parameter('NPW', mask)
                    mask = list(self.mask)
                    mask[i] += oil_prod[i]
                    self.add_parameter("NOPT", mask)  # bad code

                    mask = list(self.mask)
                    mask[i] += water_prod[i]
                    self.add_parameter("NWPT", mask)

                return

        self.wells[number]['First_run'] = ('N/A', "Exploratory", 0)

    def dummyCheck(self):
        for well in self.wells:
            if not self.wells[well]['First_run'][1] == 'Dummy':
                continue
            if not "Lateral" in self.wells[well]:
                continue
            for lateral in self.wells[well]["Lateral"]:
                year = self.wells[lateral]['First_run'][0]
                if year == 'N/A':
                    continue
                index = int(year) - self.minimal_year
                worktime = self.wells[well]['First_run'][2]
#                if ((year <  self.wells[well]['First_run'][0])
#                        and self.wells[well]['First_run'][0] > 0) \
#                    or (self.wells[well]['First_run'][0] == "N/A"):
                self.parameters["NOPT"][index] += self.wells[lateral]['WOPT'][index]
                self.parameters["NWPT"][index] += self.wells[lateral]['WWPT'][index]
                self.parameters["NPW"][index] += 1

    def cutter(self, number, start_p, end_p):
        if "Last_call" not in self.wells[number]:
            return False
        jan_mask = self.wells[number]["cls_mask_rate_jan"]
        start_p = start_p - self.minimal_year
        end_p = end_p - self.minimal_year
        jan_mask = jan_mask[start_p:end_p]
        return jan_mask

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

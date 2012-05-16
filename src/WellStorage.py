'''
Created on 24.04.2012

@author: APartilov
'''

class Singleton(type):
    '''
    Singleton class for creating 1 uniquie instance with
    1 input point
    '''
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


class WellStorage(object):
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
        if lateral:
            shrt_num = re.findall(r"^([0-9A-Z]+)(?=BS|[_-])", number)
            if shrt_num:
                print "lateral", number, well_code, shrt_num[0]
#                number = shrt_num[0]
        if not number in self.wells:
            self.wells[number] = {}
        if not self.mask:
            self.mask = [0 for unused_item in self.dates]
        if re.match(r"^(W[O|G|W][I|P]T)$", well_code):
            firstYear = True
            welldata = []
            worktime = []
            welldata_dec = []
            for cur, next in pairs(sorted(self.dates)):
                cur_line = self.dates[cur]
                next_line = self.dates[next]
                welldata.append(
                    float(data[next_line]) - \
                        float(data[cur_line]))
                m = countMonth(cur, data)
                worktime.append(m)
            self.add_worktime(number, worktime)

            dec_dates = sorted(self.dates)  # baaaaaad
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

        if re.match(r"^(WBPN|WBHP)$", well_code):
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
            oil_inj = self.recieveLine(number, 'WOIT')
            oil_prod = self.recieveLine(number, 'WOPT')
            gas_prod = self.recieveLine(number, 'WGPT')
            water_prod = self.recieveLine(number, 'WWPT')
            water_inj = self.recieveLine(number, 'WWIT')
            gas_inj = self.recieveLine(number, 'WGIT')
            output = [0 for unused_well in oil_prod]
            for year, (oil_p, water_p, gas_p, water_i, oil_i, gas_i) in enumerate(
                        zip(oil_prod, water_prod, gas_prod, oil_inj, water_inj, gas_inj)):
#                if (oil_p + water_p + gas_p) < (water_i + oil_i + gas_i):
#                        output[year] += 1
#                elif (oil_p + water_p + gas_p) > (water_i + oil_i + gas_i):
#                        output[year] += 2
                if (water_i + oil_i + gas_i) > 0:
                        output[year] += 1
                elif (oil_p + water_p + gas_p) > 0:
                        output[year] += 2
            self.wells[number]['cls_mask'] = output
        else:
            return False

    def well_classification2(self, number):  # BAD MASK
        if number in self.wells:
            oil_inj = self.recieveLine(number, 'decWOIT')
            oil_prod = self.recieveLine(number, 'decWOPT')
            gas_prod = self.recieveLine(number, 'decWGPT')
            water_prod = self.recieveLine(number, 'decWWPT')
            water_inj = self.recieveLine(number, 'decWWIT')
            gas_inj = self.recieveLine(number, 'decWGIT')
            output = [0 for unused_well in oil_prod]
            for year, (oil_p, water_p, gas_p, water_i, oil_i, gas_i) in enumerate(
                        zip(oil_prod, water_prod, gas_prod, oil_inj, water_inj, gas_inj)):
#                if (oil_p + water_p + gas_p) < (water_i + oil_i + gas_i):
#                        output[year] += 1
#                elif (oil_p + water_p + gas_p) > (water_i + oil_i + gas_i):
#                        output[year] += 2
                if (water_i + oil_i + gas_i) > 0:
                        output[year] += 1
                elif (oil_p + water_p + gas_p) > 0:
                        output[year] += 2
            self.wells[number]['cls_mask_dec'] = output
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
            for well in self.wells.values():
                if well['cls_mask_dec'][year] == code:
                    wells_fond[year] += 1
        return wells_fond

    def recieveLine(self, number, code):
        if code in self.wells[number]:
            return self.wells[number][code]
        else:
            return list(self.mask)

    def output_well(self, number):  # !!! Rework
        if number in self.wells:
            oil_prod = self.recieveLine(number, 'WOPT')  # too many lines
            water_prod = self.recieveLine(number, 'WWPT')
            gas_prod = self.recieveLine(number, 'WGPT')
            water_inj = self.recieveLine(number, 'WWIT')
            oil_inj = self.recieveLine(number, 'WOIT')
            gas_inj = self.recieveLine(number, 'WGIT')
            welltype = False  # false means production well
            for year in reversed(range(len(oil_prod))):
                if oil_prod[year] > 0 or water_prod[year] > 0 or gas_prod[year] > 0:
                    break
                elif water_inj[year] > 0 or oil_inj[year] > 0 or gas_inj[year] > 0:
                    welltype = True
                    break
            if year == len(oil_prod) - 1:
                return False
            return year, welltype
        else:
            return False

    def inj_transfer_check(self, number):
        mask = list(self.mask)
        first_run = self.wells[number]['First_run']
        if number in self.wells:
            cls_mask = self.recieveLine(number, 'cls_mask')
            n = 0
            for cur, next in pairs(cls_mask):
                n += 1
                if cur == 2 and next == 1:
                    mask[n] += 1
                    self.wells[number]['First_run'] = (first_run[0],
                                     "Production_transfered", first_run[2])
                if cur == 0 and next == 1 and first_run[1] == "Production":
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

    def add_First_Year(self, number):   # HARD REWORK
        import re
        mask = list(self.mask)
        if not number in self.wells:
            self.wells[number] = {}
        self.wells[number]['First_run'] = ()
        oil_prod = self.recieveLine(number, 'WOPT')
        water_prod = self.recieveLine(number, 'WWPT')
        gas_prod = self.recieveLine(number, 'WGPT')
        water_inj = self.recieveLine(number, 'WWIT')
        oil_inj = self.recieveLine(number, 'WOIT')
        gas_inj = self.recieveLine(number, 'WGIT')
        for i, key in enumerate(self.wells[number]['In_work']):
#            if (oil_prod[i] + water_prod[i] + gas_prod[i] >
#                    oil_inj[i] + water_inj[i] + gas_inj[i]):
#                self.wells[number]['First_run'] = (i + self.minimal_year,
#                                                   "Production",
#                                                   key)
#                mask[i] += 1
#                self.add_parameter('NPW', mask)
#
#                mask = list(self.mask)
#                mask[i] += oil_prod[i]
#                self.add_parameter("NOPT", mask)  # bad code
#
#                mask = list(self.mask)
#                mask[i] += water_prod[i]
#                self.add_parameter("NWPT", mask)  # new wells
#
#                return

#            if (oil_prod[i] + water_prod[i] + gas_prod[i] <
#                    oil_inj[i] + water_inj[i] + gas_inj[i]):
            if (oil_inj[i] + water_inj[i] + gas_inj[i]) > 0:
                self.wells[number]['First_run'] = (i + self.minimal_year,
                                                   "Injection",
                                                   key)
                mask[i] += 1
                self.add_parameter('NIW', mask)
                return
            elif (oil_prod[i] + water_prod[i] + gas_prod[i]) > 0:
                self.wells[number]['First_run'] = (i + self.minimal_year,
                                                   "Production",
                                                   key)
                mask[i] += 1
                self.add_parameter('NPW', mask)

                mask = list(self.mask)
                mask[i] += oil_prod[i]
                self.add_parameter("NOPT", mask)  # bad code

                mask = list(self.mask)
                mask[i] += water_prod[i]
                self.add_parameter("NWPT", mask)  # new wells

                return

        self.wells[number]['First_run'] = ('N/A', "Exploratory", 0)

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

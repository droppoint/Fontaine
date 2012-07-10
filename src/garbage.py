# -*- coding: UTF-8 -*-
'''
Created on 06.07.2012

@author: APartilov
'''

#GARBAGE
#if ("L_Borholes" in self.parameters) and \
#                  (well in self.parameters["L_Borholes"]):
#                    continue
# lateral = kwargs.get('lateral')
#
#
#        if not number in self.wells:
#            self.wells[number] = {}
#        if lateral:
#            shrt_num = re.findall(r"^([0-9A-Z]+)(?=BS|[_-])", number)
#            if shrt_num:
#                if not shrt_num[0] in self.wells:   # FIXME: conditions
#                    self.wells[shrt_num[0]] = {}
#                if not "Lateral" in self.wells[shrt_num[0]]:
#                    self.wells[shrt_num[0]]["Lateral"] = []
#                if not number in self.wells[shrt_num[0]]["Lateral"]:
#                    self.wells[shrt_num[0]]["Lateral"].append(number)
#                if not "L_Borholes" in self.parameters:
#                    self.parameters["L_Borholes"] = []
#                if not number in self.parameters["L_Borholes"]:
#                    self.parameters["L_Borholes"].append(number)
#        if not self.mask:
#            self.mask = [0 for unused_item in self.dates]
#
#
#            dec_dates = sorted(self.dates)
#            dec_dates.pop(0)
#            for cur in dec_dates:  # december pattern
#                if self.dates[cur] == 0:
#                    cur.next()
#                cur_line = self.dates[cur] - 1
#                next_line = self.dates[cur]
#                welldata_dec.append(
#                    float(data[next_line]) - \
#                        float(data[cur_line]))
#
#            if not well_code in self.wells[number]:
#                self.wells[number][well_code] = welldata
#                self.wells[number]["dec" + well_code] = welldata_dec
#            else:  # bad code
#                self.wells[number][well_code] = list(map(lambda x, y: x + y,
#                                self.wells[number][well_code], welldata))
#                self.wells[number]["dec" + well_code] = list(map(lambda x, y: x + y,
#                                self.wells[number]["dec" + well_code], welldata_dec))
#                print "lateral indeed", number, well_code
#            if not "First_run" in self.wells[number]:
#                self.wells[number]['First_run'] = ('N/A', "Exploratory", 0)
#
#        if re.match(r"^(WBPN|WBHP|W[O|G|W|L][I|P][R|N])$", well_code):
#            welldata = []
#            for year in sorted(self.dates.values()):
#                welldata.append(float(data[year]))
#            welldata.pop(0)  # december pattern
#            self.wells[number][well_code] = welldata


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
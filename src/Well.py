'''
Created on 04.07.2012

@author: APartilov
'''


class Well(object):
    '''
    classdocs
    '''
    first_run = None
    last_call = None
    work_time = None
    classification = None

    def __init__(self, number, data=[]):
        '''
        Constructor
        '''
        self.name = number
        self.parameters = {}
        #  self.parameters[] add parameter

    def add_parameter(self, data):
        #  self.parameters[] add parameter
        pass

    def output_well(self):  # !!! Rework
#        if ("L_Borholes" in self.parameters) and \
#            (number in self.parameters["L_Borholes"]):
#            return False
#        if not number in self.wells:
#            return False
        oil_prod = self.parameters['WOPT']  # FIXME: To array
        water_prod = self.parameters['WWPT']
        gas_prod = self.parameters['WGPT']
        water_inj = self.parameters['WWIT']
        oil_inj = self.parameters['WOIT']
        gas_inj = self.parameters['WGIT']

        welltype = False  # false means production well
        for year in reversed(range(len(oil_prod))):  # change to mask
            if water_inj[year] + oil_inj[year] + gas_inj[year] > 0:
                welltype = True
                if "In_work" in self.parameters:
                    self.last_call = [
                                        year + self.minimal_year,
                                        "Injection",
                                        self.parameters['In_work'][year]
                                        ]
                break
            elif oil_prod[year] + water_prod[year] + gas_prod[year] > 0:
                welltype = False
                if "In_work" in self.parameters:
                    self.last_call = [
                                        year + self.minimal_year,
                                        "Production",
                                        self.parameters['In_work'][year]
                                        ]
                break
        if year == len(oil_prod) - 1:
            return False
        return year, welltype

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

    def add_First_Year(self, **kwargs):   # HARD REWORK
        mask = list(self.mask)
#        over = kwargs.get('year')
#        if not number in self.wells:
#            self.wells[number] = {}
        self.first_run = ()
        oil_prod = self.parameters['WOPT']  # FIXME: To array
        water_prod = self.parameters['WWPT']
        gas_prod = self.parameters['WGPT']
        water_inj = self.parameters['WWIT']
        oil_inj = self.parameters['WOIT']
        gas_inj = self.parameters['WGIT']
#        if not 'In_work' in self.parameters:
#            self.wells[number]['First_run'] = ('N/A', "Dummy", 0)
#            for wells in self.wells[number]["Lateral"]:   # new well check
#                if (self.wells[wells]['First_run'][0] < self.wells[number]['First_run']) and \
#                    self.wells[wells]['First_run'][0] > 0:
#                    self.wells[number]['First_run'] = (self.wells[wells]['First_run'][0],
#                                                       "Dummy",
#                                                       self.wells[wells]['First_run'][2])
#            return
        for i, key in enumerate(self.parameters['In_work']):
#            if over:
#                i = over - self.minimal_year
#                key = self.wells[number]['In_work'][i]
            if (oil_inj[i] + water_inj[i] + gas_inj[i]) > 0:
                self.parameters['First_run'] = (i + self.minimal_year,
                                                   "Injection",
                                                   key)
                mask[i] += 1
#                if ("L_Borholes" in self.parameters) and \
#                  (number in self.parameters["L_Borholes"]):
#                    self.add_parameter('NLB', mask)
#                else:
#                    self.add_parameter('NIW', mask)
                return
            elif (oil_prod[i] + water_prod[i] + gas_prod[i]) > 0:
                self.first_run = (i + self.minimal_year,
                                                   "Production",
                                                   key)
                mask[i] += 1

#                if ("L_Borholes" in self.parameters) and \
#                  (number in self.parameters["L_Borholes"]):  # bad spot
#                    self.add_parameter('NLB', mask)
#                else:
#                    self.add_parameter('NPW', mask)
#                    mask = list(self.mask)
#                    mask[i] += oil_prod[i]
#                    self.add_parameter("NOPT", mask)  # bad code
#
#                    mask = list(self.mask)
#                    mask[i] += water_prod[i]
#                    self.add_parameter("NWPT", mask)

                return

        self.first_run = ('N/A', "Exploratory", 0)

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

        def cutter(self, number, start_p, end_p):
            if "Last_call" not in self.wells[number]:
                return False
            jan_mask = self.wells[number]["cls_mask_rate_jan"]
            start_p = start_p - self.minimal_year
            end_p = end_p - self.minimal_year
            jan_mask = jan_mask[start_p:end_p]
            return jan_mask

#        def recieveLine(self, number, code):
#            if code in self.wells[number]:
#                return self.wells[number][code]
#            else:
#                mask = list(self.mask)
#                mask.remove(0)
#                return list(mask)

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
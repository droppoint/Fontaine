# -*- coding: UTF-8 -*-

'''
Created on 18.06.2012

@author: APartilov
'''
from datetime import datetime
from WellStorage import WellStorage


class Report(object):
    '''
    Report writing and render
    '''
    
    class ReportLine(object):
        '''
        Lines for report
        '''
        
        def __init__(self, number, caption = "", data = []):   
            '''
            Constructor with unnecessary arguments
            '''
            self.reset()
            self.number = number
            self.caption = caption
            self.data = data
            
        def reset(self):
            self.caption = ""
            self.number = 0
            self.data = []
            
        
    def __init__(self, input):
        '''
        Constructor
        '''
        self.reset()
        self.data = input

    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
        self.data = {}
        self.lines = {}

    def compilation(self, const, **kwargs):
        
        
        def SM_to_tons (density, data):
            return [x * oil_density / 1000000 for x in data]
        
    #    if progress.wasCanceled():   # Вернуть закрывашку
    #            return
        if hasattr(self.data, 'category'):  # cut if not in category
            pat = ['WOPT', 'WWPT', 'WGPT', 'WOIT', 'WWIT', 'WGIT']
            tmp = list(self.data.wells)
            for wells in tmp:
                if not wells in self.data.category:
                    del(self.data.wells[wells])
            for wells in self.data.wells:  # bad intendation
                k = float(self.data.category[wells])
                for p in pat:
                    if p in self.data.wells[wells]:
                        self.data.wells[wells][p] = list(
                            map(lambda x: x * k, self.data.wells[wells][p]))
                        
                        
        # annual production/injection
        oil_density = int(const['oil_density'])
        water_density = int(const['water_density'])
        oil_PR_tons = (oil_density, self.data.production_rate('WOPT'))
        water_PR_tons = (water_density, self.data.production_rate('WWPT'))
        gas_PR = self.data.production_rate('WGPT')
        gas_PR_mln = [x / 1000000 for x in gas_PR]
        liq_PR_tons = list(map(lambda x, y: x + y, oil_PR_tons, water_PR_tons))
        water_IR = self.data.production_rate('WWIT')
        water_IR_SM3 = [x / 1000 for x in water_IR]
        

        for well in self.data.wells:
            self.data.add_First_Year(well)
            if hasattr(self.data, 'override'):
                if well in self.data.override:
                    # TODO: logger override well
                    date = datetime.strptime(self.data.override[well], "%d/%m/%Y")
                    self.data.add_First_Year(well, year=date.year)
        index_output_well = list(self.data.output_well(well)
                             for well in self.data.wells
                             if self.data.output_well(well))

        all_output_well = list(mask)
        output_wells_prod = list(mask)
        output_wells_inj = list(mask)
        for year, welltype in index_output_well:
            all_output_well[year] += 1
            if welltype:
                output_wells_inj[year] += 1
            else:
                output_wells_prod[year] += 1

        for wellname in self.data.wells:  # initiating classification of wells
            self.data.well_classification(wellname)
            self.data.well_classification2(wellname)
            self.data.well_classification3(wellname)

        reservoir_pres = self.data.avg_pressure('WBPN')
        bottomhole_pres = self.data.avg_pressure('WBHP')
        prod_wells = self.data.well_fond(2)
        inj_wells = self.data.well_fond(1)
        inj_transfer = []
        for wellname in self.data.wells:
            if "First_run" in self.data.wells[wellname]:
                check = self.data.inj_transfer_check(wellname)
            else:
                check = list(mask)
            if not inj_transfer:
                inj_transfer = list(check)
            else:
                inj_transfer = list(map(lambda x, y: x + y, inj_transfer, check))
            if self.data.wells[wellname]['First_run'][1] == 'Production_transfered':
                output_wells_prod = list(map(lambda x, y: x + y, check,
                                              output_wells_prod))

        work_time = list(self.data.mask)  # bad
        for wells in self.data.wells.values():
            if not (wells['First_run'][1] == "Exploratory" or
                wells['First_run'][1] == "Dummy"):
                work_time[wells['First_run'][0] - self.data.minimal_year] += \
                         wells['First_run'][2]

        inactive_fond = list(self.data.mask)
        for well in self.data.wells:
            if "Last_call" in self.data.wells[well]:
                cut = self.data.cutter(well, self.data.wells[well]["First_run"][0],
                                     self.data.wells[well]["Last_call"][0])
                for index, status in enumerate(cut):
                    if status == 0:
                        year_index = int(self.data.wells[well]["First_run"][0]) \
                                           - int(self.data.minimal_year) + index
                        inactive_fond[year_index] += 1
#                        print str(int(self.data.wells[well]["First_run"][0]) +
#                                  index) + " WELL " + well + " inactive"

        self.data.mask.pop(0)
        inj = list(self.data.mask)
        prod = list(self.data.mask)
        for years, unused_val in enumerate(self.data.mask):
            for wells in self.data.wells:
                if self.data.wells[wells]['cls_mask'][years] == 2:
                    prod[years] += self.data.wells[wells]['In_work'][years]
                if self.data.wells[wells]['cls_mask'][years] == 1:
                    inj[years] += self.data.wells[wells]['In_work'][years]

        self.data.dummyCheck()
        new_wells_liq_tons = list(map(lambda x, y: (x * oil_density + y *
                                                    water_density) / 1000000,
                                 self.data.parameters.get('NOPT', mask),
                                 self.data.parameters.get('NWPT', mask)))
        new_wells_oil_tons = list(map(lambda x: x * oil_density / 1000000,
                                      self.data.parameters.get('NOPT', mask)))

    def render(self, filename, **kwargs):  # отдать объект для рендера
        import xlwt
        from xlwt.Utils import rowcol_to_cell
        
        if self.lines == {}:
            # Nothing to render
            return None
        
        lateral = kwargs.get('lateral')
        
        font0 = xlwt.Font()
        font0.name = 'Times New Roman'
        wb = xlwt.Workbook()
        ws = wb.add_sheet(u'gosplan_input')
        n = 0
        
        for line in lines:
            ws.write()
            #  line = {caption:---,number:---,data:[---]}
            pass
        
#        for unused_years in self.data.mask:
#            n += 1
#            ws.write(14, n, xlwt.Formula(   # Watercut
#                    "IF(%(liquid)s=0;0;(%(liquid)s-%(oil)s)/%(liquid)s*100)"
#                    % {"liquid": rowcol_to_cell(11, n),
#                       "oil":    rowcol_to_cell(10, n)}
#                     ))
#            ws.write(25, n, xlwt.Formula(   # New wells watercut
#                    "IF(%(liquid)s=0;0;(%(liquid)s-%(oil)s)/%(liquid)s*100)"
#                    % {"liquid": rowcol_to_cell(24, n),
#                       "oil":    rowcol_to_cell(23, n)}
#                    ))
#            ws.write(37, n, xlwt.Formula(   # Wells from drilling
#                    "(%s+%s)"
#                    % (rowcol_to_cell(38, n),   # Production wells
#                       rowcol_to_cell(39, n))   # Injection wells
#                    ))
#            ws.write(26, n, xlwt.Formula(   # oil rate of new wells
#                    "IF(%(worktime)s=0;0;(%(oil)s/%(worktime)s)/30.25*1000)"
#                    % {"worktime": rowcol_to_cell(28, n),
#                       "oil":   rowcol_to_cell(23, n)}
#                    ))
#            ws.write(27, n, xlwt.Formula(   # fluid rate of new wells
#                    "IF(%(worktime)s=0;0;(%(fluid)s/%(worktime)s)/30.25*1000)"
#                    % {"worktime": rowcol_to_cell(28, n),
#                       "fluid":   rowcol_to_cell(24, n)}
#                    ))

        def printRow(name, data, y):
            x = 0
            ws.write(y, x, name)
            x += 1
            for key in data:
                ws.write(y, x, key)
                x += 1

        if debug:
            debuglist = wb.add_sheet(u'debug')

            def printDebugRow(name, data, y):
                x = 0
                debuglist.write(y, x, name)
                x += 1
                for key in data:
                    debuglist.write(y, x, key)
                    x += 1
            n = 0
            for well in self.data.wells:
                printDebugRow(well, [], n)
                n += 1
                for parameter in self.data.wells[well]:
                    printDebugRow(parameter, self.data.wells[well][parameter], n)
                    n += 1

#        printRow(u'Годы', sorted(self.data.dates.iterkeys()), 0)
#
#        printRow(u'Годовые показатели', [], 9)
#        printRow(u'   Годовая добыча нефти, тыс.т', oil_PR_tons, 10)
#        printRow(u'   Годовая добыча жидкости, тыс.т', liq_PR_tons, 11)
#        printRow(u'   Годовая добыча газа, млн.м3', gas_PR_mln, 12)
#        printRow(u'   Годовая закачка воды, тыс.м3', water_IR_tons, 13)
#        printRow(u'   Обводненность,%', [], 14)
#
#        printRow(u'Показатели новых скважин', [], 22)
#        printRow(u'   Добыча нефти, тыс.т/год', new_wells_oil_tons, 23)
#        printRow(u'   Добыча жидкости, тыс.т/год', new_wells_liq_tons, 24)
#        printRow(u'   Обводненность,%', [], 25)
#        printRow(u'   Дебит нефти, т/сут', [], 26)
#        printRow(u'   Дебит жидкости, т/сут', [], 27)
#        printRow(u'   Время работы', work_time, 28)
#
#        printRow(u'Действ. фонд скважин', [], 33)
#        printRow(u'   добывающих', prod_wells, 34)
#        printRow(u'   нагнетательных', inj_wells, 35)
#
#        printRow(u'Ввод скважин из бурения', [], 37)
#        printRow(u'   добывающих', self.data.parameters.get('NPW', mask), 38)
#        printRow(u'   нагнетательных', self.data.parameters.get('NIW', mask), 39)
#        if lateral:
#            printRow(u'   боковые стволы', self.data.parameters.get('NLB', mask), 40)
#
#        printRow(u'Перевод из доб. в нагн.', inj_transfer, 41)
#
#        printRow(u'Выбытие скважин', all_output_well, 43)
#        printRow(u'   добывающих', output_wells_prod, 44)
#        printRow(u'      в т.ч. под закачку', inj_transfer, 45)
#        printRow(u'   нагнетательных', output_wells_inj, 46)
#
#        printRow(u'Ср. взв. пластовое давление, атм',
#                        self.data.parameters.get('FPRP', mask), 48)  # FPRP or FPR
#        printRow(u'   в зоне отбора, атм', reservoir_pres[0], 49)
#        printRow(u'   в зоне закачки, атм', reservoir_pres[1], 50)
#
#        printRow(u'Ср. забойное давление доб. скважин, атм',
#                                        bottomhole_pres[0], 52)
#        printRow(u'Ср. забойное давление нагн. скважин, атм',
#                                        bottomhole_pres[1], 53)
#
#        printRow(u'Время работы добывающих скважин',
#                                        prod, 54)
#        printRow(u'Время работы нагнетательных скважин',
#                                        inj, 55)
#
#        printRow(u'Бездействующий фонд', inactive_fond, 57)
#
#        printRow(u'   Перевод в б/д доб.', inactivity_trans_prod, 58)
#        printRow(u'   Перевод в б/д наг.', inactivity_trans_inj, 59)
#        printRow(u'   Вывод из бездействия доб.', active_trans_prod, 60)
#        printRow(u'   Вывод из бездействия наг.', active_trans_inj, 61)
#    #    progress.setValue(100)

        wb.save(filename)

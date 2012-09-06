# -*- coding: UTF-8 -*-

'''
Created on 18.06.2012

@author: APartilov
'''

import os


def get_formulas(template, args, number):
    import xlwt.ExcelFormula
    from xlwt.Utils import rowcol_to_cell
    formulas = []
    for n in range(number):
        formulas.append(xlwt.Formula(template %
                tuple(rowcol_to_cell(i, n + 1) for i in args)
                        ))
    return formulas


class ReportError(Exception):
    """Exception raised for all parse errors."""

    def __init__(self, msg, lineno=None):
        assert msg
        self.msg = msg
        self.lineno = lineno

    def __str__(self):
        result = self.msg
        if self.lineno is not None:
            result = result + " at line " % self.lineno
        return result


class ReportLine(object):
    '''
    Lines for report
    '''

    def __init__(self, number, caption="", data=[]):
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


class Report(object):
    '''
    Report writing and render
    '''

    def __init__(self, controller, model):
        '''
        Constructor
        '''
        self.reset()
        self.model = model
        self.model.add_observer(self)
        self.controller = controller
        self._savefile = None

    def model_is_changed(self, signal):
        """
        Реакция на изменение модели
        """
        # Если пришел сигнал об окончании расчета
        if signal == ('complete', 0):
            self._savefile = self.controller.request_savefile()
            self.report_formatting()
            self.render(self._savefile)
            self.reset()

    @property
    def savefile(self):
        return self._savefile

    @savefile.setter
    def savefile(self, value):
        self._savefile = value

    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
        if hasattr(self, 'lines'):
            for lines in self.lines:
                lines.reset()
        self.lines = []

    def add_line(self, number, caption="", data=[]):
        self.lines.append(ReportLine(number, caption, data))

    def render(self, filename):  # отдать объект для рендера
        import xlwt
#        from xlwt.Utils import rowcol_to_cell

        def printRow(name, data, y):
            x = 0
            ws.write(y, x, name)
            x += 1
            for key in data:
                ws.write(y, x, key)
                x += 1

        if self.lines == {}:
            raise ReportError('Nothing to render')
            return None

        font0 = xlwt.Font()
        font0.name = 'Times New Roman'
        wb = xlwt.Workbook()
        ws = wb.add_sheet(u'gosplan_input')

        for line in self.lines:
            printRow(line.caption, line.data, line.number)

        # костыль
        while True:
            if filename == None:
                print "Отменено"
                break
            try:
                wb.save(filename)
                print "Завершено"
                break
            except IOError:
                filename = self.controller.request_savefile()

    def report_formatting(self):
        ##############################
            # annual production/injection
            if (not 'oil_density' in self.model.parameters) or \
               (not 'water_density' in self.model.parameters):
                raise ReportError('Data shortage: consts')
                return
            oil_density = int(self.model.parameters['oil_density'])
            water_density = int(self.model.parameters['water_density'])
            oil_PR_tons = self.model.production_rate('WOPT',
                         density=oil_density, degree=-6)
            water_PR_tons = self.model.production_rate('WWPT',
                         density=water_density, degree=-6)
            gas_PR_mln = self.model.production_rate('WGPT', degree=-6)
            liq_PR_tons = list(map(lambda x, y: x + y,
                         oil_PR_tons, water_PR_tons))
            water_IR_SM3 = self.model.production_rate('WWIT', degree=-3)

            avg_res_pres_prod, avg_res_pres_inj = self.model.avg_pressure('WBP9')
            avg_btm_pres_prod, avg_btm_pres_inj = self.model.avg_pressure('WBHP')

            oil_nw_PR_tons = self.model.new_well_rate('WOPT',
                         density=oil_density, degree=-6)
            water_nw_PR_tons = self.model.new_well_rate('WWPT',
                         density=water_density, degree=-6)
            liq_nw_PR_tons = list(map(lambda x, y: x + y,
                         oil_nw_PR_tons, water_nw_PR_tons))

#            self.model.dummyCheck()
            # new_well_rate
            self.add_line(0, u'Годы', sorted(self.model.dates.keys()))

            self.add_line(9, u'Годовые показатели', [])
            self.add_line(10, u'    Годовая добыча нефти, тыс.т', oil_PR_tons)
            self.add_line(11, u'    Годовая добыча жидкости, тыс.т', liq_PR_tons)
            self.add_line(12, u'    Годовая добыча газа, млн.м3', gas_PR_mln)
            self.add_line(13, u'    Годовая закачка воды, тыс.м3', water_IR_SM3)
#            self.add_line(14, u'    Обводненность,%', [])

            self.add_line(22, u'Показатели новых скважин', [])
            self.add_line(23, u'    Добыча нефти, тыс.т/год', oil_nw_PR_tons)
            self.add_line(24, u'    Добыча жидкости, тыс.т/год', liq_nw_PR_tons)
            self.add_line(25, u'    Обводненность,%', [])
            self.add_line(26, u'    Дебит нефти, т/сут', [])
            self.add_line(27, u'    Дебит жидкости, т/сут', [])
            self.add_line(28, u'    Время работы', self.model.new_well_work_time())

            self.add_line(33, u'Действ. фонд скважин', [])
            self.add_line(34, u'    добывающих', self.model.well_fond(2))
            self.add_line(35, u'    нагнетательных', self.model.well_fond(1))

            self.add_line(37, u'Ввод скважин из бурения',
                       self.model.completed_wells())
            self.add_line(38, u'    добывающих',
                       self.model.completed_wells(code=2))
            self.add_line(39, u'    нагнетательных',
                       self.model.completed_wells(code=1))
            self.add_line(40, u'    боковые стволы', self.model.borehole_fond())

            self.add_line(41, u'Перевод из доб. в нагн.',
                       self.model.transfered_wells())

            self.add_line(43, u'Выбытие скважин', self.model.abandoned_wells())
            self.add_line(44, u'    добывающих', self.model.abandoned_wells(code=2))
            self.add_line(45, u'        в т.ч. под закачку', [])
            self.add_line(46, u'    нагнетательных',
                       self.model.abandoned_wells(code=1))

            self.add_line(48, u'Ср. взв. пластовое давление, атм',
                       self.model.parameters.get('FPRP', self.model.mask))
            self.add_line(49, u'    в зоне отбора, атм', avg_res_pres_prod)
            self.add_line(50, u'    в зоне закачки, атм', avg_res_pres_inj)

            self.add_line(52, u'Ср. забойное давление доб. скважин, атм',
                       avg_btm_pres_prod)
            self.add_line(53, u'Ср. забойное давление нагн. скважин, атм',
                       avg_btm_pres_inj)

            self.add_line(54, u'Время работы добывающих скважин',
                       self.model.work_time(code=2))
            self.add_line(55, u'Время работы нагнетательных скважин',
                       self.model.work_time(code=1))

            self.add_line(57, u'Бездействующий фонд', self.model.well_fond(4))
            inactive_fond = self.model.inactive_transfer()
            self.add_line(58, u'    Перевод в б/д доб.', inactive_fond[1])
            self.add_line(59, u'    Перевод в б/д наг.', inactive_fond[3])
            self.add_line(60, u'    Вывод из бездействия доб.', inactive_fond[0])
            self.add_line(61, u'    Вывод из бездействия наг.', inactive_fond[2])

            formulas = get_formulas("IF(%s=0;0;(%s-%s)/%s*100)",
                                (11, 11, 10, 11),
                                len(self.model.mask))
            self.add_line(14, u'    Обводненность, %', formulas)

#            if debug:
#                n = 62
#                for well in self.model.wells:
#                    self.add_line(n, well, [])
#                    n += 1
#                    self.add_line(n, 'class',
#                               self.model.wells[well].classification_by_rate)
#                    n += 1
######################################

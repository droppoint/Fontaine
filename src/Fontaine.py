# -*- coding: UTF-8 -*-

'''
Created on 03.04.2012

@author: Alexei Partilov
'''

from __future__ import division
import sys
import logging
import logging.handlers
import Field
import Report
import Parser
import Initialization as Init
from PySide import QtGui, QtCore
from fontaine_ui import Ui_MainWindow


class _Constants:   # this class store initial data and constants

    class ConstError(TypeError):
        pass

    def __setitem__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError, "Can't rebind const(%s)" % name
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise self.ConstError, "Can't unbind const(%s)" % name
        raise NameError + name

    def reset(self):
        self.__dict__.clear()
#        self.logger.info('Constants cleared')


def timer(f):  # time benchmark
    from time import time

    def tmp(*args, **kwargs):
        t = time()
        res = f(*args, **kwargs)
        print "Время выполнения функции: %f" % (time() - t)
        return res
    return tmp

if __name__ == "__main__":
    # logger system initialization
    logger = logging.getLogger('')
    logger.setLevel(logging.DEBUG)
    #basic config here
    fh = logging.handlers.RotatingFileHandler('debug.log',
                                      mode='w',
                                      maxBytes=524288,
                                      backupCount=1)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info('Fontaine start')

    const = _Constants()
    category = _Constants()
    app = QtGui.QApplication(sys.argv)
    mainwindow = QtGui.QMainWindow()
#    progress = QtGui.QProgressDialog(u"Подготовка отчета...",
#                                        u"Отмена", 0, 100)
#    progress.setWindowTitle(QtGui.QApplication.translate("Progress",
#                            "Fontaine", None, QtGui.QApplication.UnicodeUTF8))
#    progress.setWindowModality(QtCore.Qt.WindowModal)
    ui = Ui_MainWindow()
    ui.setupUi(mainwindow)

    def errorlog(func):

        def error_msg(module, msg):
            logger.exception('Fatal error in ' + module + '\n' + msg)
            ui.errorMessage(u'Ошибка модуля ' + module + '\n' + msg,
                            caption=u"Fontaine")

        def decorator(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Parser.ParseError as e:
                error_msg('Parser', str(e))
            except Field.FieldError as e:
                error_msg('Field', str(e))
            except Report.ReportError as e:
                error_msg('Report', e.msg)
            except Exception as inst:
                logger.exception('Unknown error')
                logger.exception(type(inst))
                logger.exception(inst.args)
                ui.errorMessage(u"Неизвестная ошибка. \n ",
                                caption=u"Fontaine")
                raise
        return decorator

    @errorlog
    def ignition():
        filename = ui.lineEdit.text()
        well_filename = ui.lineEdit_2.text()
        savefile = ui.setSaveFileName()
        const = Init.config_init('../config.ini')
        debug = ui.debug.isChecked()
        if well_filename:
#            storage.category = Init.wells_init(well_filename)
#        storage.override = Init.wells_input_override('input.ini')
            pass
        if filename and savefile:
            p = Parser.Parser()
            p.initialization(filename)   # FIX: remove initialization or rename
            storage = Field.Field('test field', p.get_dates_list())
            parsed_data = p.parse_file(filename)
            p.close()
            for row in parsed_data:
                if row['number'] == 'N/A':
                    storage.add_parameter(row['parameter_code'],
                                          row['welldata'])
                else:
                    storage.add_well(row['number'],
                        {row['parameter_code']: row['welldata']})
            r = Report.Report()
            storage.routine_operations()  # !!!!!!!
##############################
            # annual production/injection
            oil_density = int(const['oil_density'])
            water_density = int(const['water_density'])
            oil_PR_tons = storage.production_rate('WOPT',
                         density=oil_density, degree=-6)
            water_PR_tons = storage.production_rate('WWPT',
                         density=water_density, degree=-6)
            gas_PR_mln = storage.production_rate('WGPT', degree=-6)
            liq_PR_tons = list(map(lambda x, y: x + y,
                         oil_PR_tons, water_PR_tons))
            water_IR_SM3 = storage.production_rate('WWIT', degree=-3)

            avg_res_pres_prod, avg_res_pres_inj = storage.avg_pressure('WBP9')
            avg_btm_pres_prod, avg_btm_pres_inj = storage.avg_pressure('WBHP')

            oil_nw_PR_tons = storage.new_well_rate('WOPT',
                         density=oil_density, degree=-6)
            water_nw_PR_tons = storage.new_well_rate('WWPT',
                         density=water_density, degree=-6)
            liq_nw_PR_tons = list(map(lambda x, y: x + y,
                         oil_nw_PR_tons, water_nw_PR_tons))

#            storage.dummyCheck()
            # new_well_rate
            r.add_line(0, u'Годы', sorted(storage.dates.keys()))

            r.add_line(9, u'Годовые показатели', [])
            r.add_line(10, u'    Годовая добыча нефти, тыс.т', oil_PR_tons)
            r.add_line(11, u'    Годовая добыча жидкости, тыс.т', liq_PR_tons)
            r.add_line(12, u'    Годовая добыча газа, млн.м3', gas_PR_mln)
            r.add_line(13, u'    Годовая закачка воды, тыс.м3', water_IR_SM3)
#            r.add_line(14, u'    Обводненность,%', [])

            r.add_line(22, u'Показатели новых скважин', [])
            r.add_line(23, u'    Добыча нефти, тыс.т/год', oil_nw_PR_tons)
            r.add_line(24, u'    Добыча жидкости, тыс.т/год', liq_nw_PR_tons)
            r.add_line(25, u'    Обводненность,%', [])
            r.add_line(26, u'    Дебит нефти, т/сут', [])
            r.add_line(27, u'    Дебит жидкости, т/сут', [])
            r.add_line(28, u'    Время работы', storage.new_well_work_time())

            r.add_line(33, u'Действ. фонд скважин', [])
            r.add_line(34, u'    добывающих', storage.well_fond(2))
            r.add_line(35, u'    нагнетательных', storage.well_fond(1))

            r.add_line(37, u'Ввод скважин из бурения',
                       storage.completed_wells())
            r.add_line(38, u'    добывающих',
                       storage.completed_wells(code=2))
            r.add_line(39, u'    нагнетательных',
                       storage.completed_wells(code=1))
            r.add_line(40, u'    боковые стволы', storage.borehole_fond())

            r.add_line(41, u'Перевод из доб. в нагн.',
                       storage.transfered_wells())

            r.add_line(43, u'Выбытие скважин', storage.abandoned_wells())
            r.add_line(44, u'    добывающих', storage.abandoned_wells(code=2))
            r.add_line(45, u'        в т.ч. под закачку', [])
            r.add_line(46, u'    нагнетательных',
                       storage.abandoned_wells(code=1))

            r.add_line(48, u'Ср. взв. пластовое давление, атм',
                       storage.parameters.get('FPRP', storage.mask))
            r.add_line(49, u'    в зоне отбора, атм', avg_res_pres_prod)
            r.add_line(50, u'    в зоне закачки, атм', avg_res_pres_inj)

            r.add_line(52, u'Ср. забойное давление доб. скважин, атм',
                       avg_btm_pres_prod)
            r.add_line(53, u'Ср. забойное давление нагн. скважин, атм',
                       avg_btm_pres_inj)

            r.add_line(54, u'Время работы добывающих скважин',
                       storage.work_time(code=2))
            r.add_line(55, u'Время работы нагнетательных скважин',
                       storage.work_time(code=1))

            r.add_line(57, u'Бездействующий фонд', storage.well_fond(4))
            inactive_fond = storage.inactive_transfer()
            r.add_line(58, u'    Перевод в б/д доб.', inactive_fond[1])
            r.add_line(59, u'    Перевод в б/д наг.', inactive_fond[3])
            r.add_line(60, u'    Вывод из бездействия доб.', inactive_fond[0])
            r.add_line(61, u'    Вывод из бездействия наг.', inactive_fond[2])

            formulas = Report.get_formulas("IF(%s=0;0;(%s-%s)/%s*100)",
                                (11, 11, 10, 11),
                                len(storage.mask))
            r.add_line(14, u'    Обводненность, %', formulas)
            
            if debug:
                n = 62
                for well in storage.wells:
                    r.add_line(n, well, [])
                    n += 1
#                    r.add_line(n, 'WOPT',
#                               storage.wells[well].parameters['WOPT'])
#                    n += 1
#                    r.add_line(n, 'WWPT',
#                               storage.wells[well].parameters['WWPT'])
#                    n += 1
#                    r.add_line(n, 'WWIT',
#                               storage.wells[well].parameters['WWIT'])
#                    n += 1
#                    r.add_line(n, 'WLPR',
#                               storage.wells[well].parameters['WLPR'])
#                    n += 1
#                    r.add_line(n, 'WWIN',
#                               storage.wells[well].parameters['WWIN'])
#                    n += 1
                    r.add_line(n, 'class',
                               storage.wells[well].classification_by_rate)
                    n += 1
######################################
            r.render(savefile)
            storage.clear()
            r.reset()
            ui.informationMessage(u"Завершено",
                                  caption=u"Fontaine")
        elif not filename:
            ui.informationMessage(u"Выберите файл для обработки",
                                  caption=u"Ошибка запуска")
        else:
            ui.informationMessage(u"Выберите файл для сохранения",
                                  caption=u"Ошибка запуска")
    ui.pushButton_2.clicked.connect(ignition)

    mainwindow.show()
    sys.exit(app.exec_())
#    fh.close() нацепить на выход
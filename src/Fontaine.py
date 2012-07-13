# -*- coding: UTF-8 -*-

'''
Created on 03.04.2012

@author: Alexei Partilov
'''

from __future__ import division
import sys
from Field import Field
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

    def ignition():
        filename = ui.lineEdit.text()
        well_filename = ui.lineEdit_2.text()
        savefile = ui.setSaveFileName()
        const = Init.config_init('../config.ini')
        if well_filename:
#            storage.category = Init.wells_init(well_filename)
#        storage.override = Init.wells_input_override('input.ini')
            pass
        if filename and savefile:
            p = Parser.Parser()

            p.initialization(filename)   # FIX: remove initialization or rename
            storage = Field('test field', p.get_dates_list())
            parsed_data = p.parse_file(filename, lateral=ui.tracks.isChecked())
            p.close()
            for row in parsed_data:
                if row['number'] == 'N/A':
                    storage.add_parameter(row['parameter_code'],
                                          row['welldata'])
                else:
                    storage.add_well(row['number'],
                        {row['parameter_code']: row['welldata']})
            r = Report.Report()
            n = 0
##############################
            # annual production/injection
            oil_density = int(const['oil_density'])
            water_density = int(const['water_density'])
            oil_PR_tons = storage.production_rate('WOPT', density=oil_density, degree=-6)
            water_PR_tons = storage.production_rate('WWPT', density=water_density, degree=-6)
            gas_PR_mln = storage.production_rate('WGPT', degree=-6)
            liq_PR_tons = list(map(lambda x, y: x + y, oil_PR_tons, water_PR_tons))
            water_IR_SM3 = storage.production_rate('WWIT', degree=-3)

            storage.routine_operations()

            all_output_well = storage.abandoned_wells()   # abandon_wells
            output_wells_prod = storage.abandoned_wells(code=2)
            output_wells_inj = storage.abandoned_wells(code=1)

            reservoir_pres = storage.avg_pressure('WBPN')
            bottomhole_pres = storage.avg_pressure('WBHP')

            # можно и без переменных
            inactive_fond = storage.well_fond(4)
            prod_wells = storage.well_fond(2)
            inj_wells = storage.well_fond(1)

            inj_transfer = storage.transfered_wells()

            new_wells_work_time = list(storage.mask)

            inj = storage.work_time(code=1)
            prod = storage.work_time(code=2)

#            storage.dummyCheck()
            # new_well_rate

#            if debug:
#                debuglist = wb.add_sheet(u'debug')
            r.add_line(0, u'Годы', sorted(storage.dates.keys()))
#            for well in storage.wells:
#                r.add_line(n, well, [])
#                n += 1
#                r.add_line(n, 'WOPT', storage.wells[well].parameters['WOPT'])
#                n += 1
#######################################
            r.render(savefile, debug=ui.debug.isChecked(),
                       lateral=ui.tracks.isChecked())
            storage.clear()
            r.reset()
        elif not filename:
            ui.informationMessage(u"Выберите файл для обработки",
                                  caption=u"Ошибка запуска")
        else:
            ui.informationMessage(u"Выберите файл для сохранения",
                                  caption=u"Ошибка запуска")
    ui.pushButton_2.clicked.connect(ignition)

    mainwindow.show()
    sys.exit(app.exec_())

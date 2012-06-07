# -*- coding: UTF-8 -*-

'''
Created on 03.04.2012

@author: Alexei Partilov
'''

from __future__ import division
import sys
#import locale
from WellStorage import WellStorage
from PySide import QtGui, QtCore
from fontaine_ui import Ui_MainWindow


class _Constants:   # this class store initial data and constants

    class ConstError(TypeError):
        pass

    def __init__(self):
#        import logging
#        logging.basicConfig(level=logging.DEBUG,
#                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#                    datefmt='%m-%d %H:%M',
#                    filemode='w')
#        self.logger = logging.getLogger('Constants_class')
#        console = logging.StreamHandler()
#        console.setLevel(logging.INFO)
#        self.logger.info('Creating instance of constants class')
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


def config_init(filename):
    import ConfigParser

    def parseSection(section_name):
        if not section_name in config.sections():
            return
        for options in config.options(section_name):
            const[options] = config.get(section_name, options)
    try:
        config = ConfigParser.ConfigParser()
        config.read(filename)
        for sections in config.sections():
            parseSection(sections)
    except:
        print "Configuration file not found"


def wells_init(filename):
    import mmap
    import re

    result = {}
    try:
        f = open(filename, "r+")
    except IOError as unused_e:
        print "Category file not found, proceeding"
        return
    buf = mmap.mmap(f.fileno(), 0)  # add filename check
    filesize = buf.size()
    n = 0
    buf.seek(n)
    while True:
        print buf.tell()
        if buf.tell() == filesize:
            break
        data = buf.readline()
        raw = re.match(r"^([0-9]+[A-Z]?(?:[-_]?\w*)?)\s+(0.\d+|1)", data)
        if raw:
            well = raw.groups()
            result.update(dict([well]))  # bad memory consumption
    storage.category = result


def wells_input_override(filename):
    import mmap
    import re

    result = {}
    try:
        f = open(filename, "r+")
    except IOError as unused_e:
        print "Wells input override file not found, proceeding"
        return
    buf = mmap.mmap(f.fileno(), 0)  # add filename check
    filesize = buf.size()
    n = 0
    buf.seek(n)
    date_pattern = "%d/%m/%Y"
    while True:
        if buf.tell() == filesize:
            break
        data = buf.readline()
        while re.match(r"^\s*#", data):
            data = buf.readline()
        raw = re.match(r"^([0-9]+[A-Z]?(?:[-_]?\w*)?)\s+"
                             "((?:0[1-9]|[1-2][0-9]|3[0|1])/"
                             "(?:0[1-9]|1[0-2])/"
                             "(?:(?:19|20|21|22)\d{2}))", data)
        if raw:
            well = raw.groups()
            result.update(dict([well]))
    storage.override = result


@timer
def getline(filename, **kwargs):
    import re
    import mmap
    import math  # maybe in other place?
    lateral = kwargs.get('lateral')
    initialization(filename)

    def parseBlock(pointer):
        result = {}
        #Reading header
        buf.seek(pointer)
        header_str = buf.readline()
        headers = re.findall(r"([A-Z0-9_]+)", header_str)
        result['headers'] = re.findall(
                            r"\b(W[O|G|W|L][I|P][T|R]|WBPN|WBHP|FPRP?)\b",
                                                              header_str)

        #Comparision of the headers
        def indices(mylist, value):
            return [i for i, x in enumerate(mylist) if x == value]
        index = []
        temp = []
        for value in result['headers']:
            if not value in temp:
                index += indices(headers, value)
                temp.append(value)
        del(temp)
#        quantity_str = buf.readline()
        line = buf.readline()
        factor = []
        while not re.search(r"\s([0-9]+[A-Z]?(?:[-_]?\w*)?)\s", line):
            if re.search(config.r_pattern, line):
                break
            if re.search(r"(?:\*10\*\*(\d))", line):
                temp_num = line[14:]   # bad block of code
                nn = 0
                while nn + 13 < len(temp_num):
                    if re.match(r"(?:\*10\*\*(\d))", temp_num[nn:nn + 13]):
                        factor.append(re.findall(r"(?:\*10\*\*(\d))",
                                                temp_num[nn:nn + 13])[0])
                    else:
                        factor.append(None)
                    nn += 13
            line = buf.readline()
        result['factor'] = list(factor)
        numbers_str = line
        numbers = re.findall(r"\s([0-9]+[A-Z]?(?:[-_]?\w*)?)\s", numbers_str)

        if ((len(headers) - 1) > len(numbers)) and numbers != []:
            temp_num = numbers_str[14:]   # bad block of code
            numbers = []
            nn = 0
            while nn + 13 < len(temp_num):
                if re.match(r"^([\w-]+)\b", temp_num[nn:nn + 13]):
                    numbers.append(re.match(r"^([\w-]+)\b",
                                            temp_num[nn:nn + 13]).group(0))
                else:
                    numbers.append("N/A")
                nn += 13
        if numbers == []:
            numbers = ["N/A" for unused_i in range(len(headers) - 1)]
        result['numbers'] = [numbers[i - 1] for i in index if numbers]
        #Reading data
        while not re.search(config.r_pattern, line):
            line = buf.readline()
        data = line
        result['data'] = []
        while not data == config.breaker:  # parsing the data
            dataline = re.findall(r"\s((?:[-+]?[0-9]*\.[0-9]*E?-?[0-9]*)|0)\s",
                                   data)
            result['data'].append([dataline[i - 1] for i in index])
            if buf.tell() == filesize:
                break
            data = buf.readline()
        return result

    f = open(filename, "r+")
    buf = mmap.mmap(f.fileno(), 0)  # add filename check
    filesize = buf.size()
    n = 0
    buf.seek(n)
    while buf.find("SUMMARY", n) != -1:
        if progress.wasCanceled():
            f.close()
            break
        progress.setValue(int((n / filesize) * 100))
        n = buf.find("SUMMARY", n)
        m = buf.find("DATE", n)
        buf.seek(n)  # WHY???
        n += 1
        buf.seek(m)
        cur_str = buf.readline()
        if re.findall(r"\b(W[O|G|W|L][I|P][T|R]|WBPN|WBHP|FPRP?)\b", cur_str):
            block = parseBlock(m)
            for key, well_num in enumerate(block['numbers']):
                data = [i[key] for i in block['data']]
                parameter = block['headers'][key]

                if re.match(r"^(W[O|G|W|L][I|P][T|R])|(WBPN|WBHP)$",
                            parameter):
                    if block['factor']:
                        factor = block['factor'][key]
                        if factor:
                            fl = float(factor)
                            fk = math.pow(10.0, fl)
                            data = [float(i) * fk for i in data]
                    storage.add_well(well_num, parameter,
                                        data, lateral=lateral)

                if re.match(r"^(FPRP?)$", parameter):
                    welldata = []
                    for year in sorted(storage.dates.values()):
                        welldata.append(float(data[year]))
                    storage.add_parameter(parameter, welldata)

    f.close()


def initialization(filename):
    """Return primary parameters of RSM file,
    such as RSM filetype, height of data table,
    masks and other"""
    from datetime import datetime
    import re
    import mmap

    def filetypecheck(buf):
        n = 0
        buf.seek(n)
        breaker = buf.readline()
        if breaker == "1\r\n":
            filetype = "tempest"
        elif breaker == "\r\n":
            filetype = "eclipse"
        else:
            raise IOError
        return filetype, breaker

    def dateformatcheck(dataline):
        date_pattern = ""  # date format check
        regex_pattern = ""
        if re.findall(r"\s((?:0[1-9]|[1-2][0-9]|3[0|1])/"
                             "(?:0[1-9]|1[0-2])/"
                             "(?:(?:19|20|21|22)\d{2}))\s", dataline):
            date_pattern = "%d/%m/%Y"
            regex_pattern = ("\s((?:0[1-9]|[1-2][0-9]|3[0|1])/"
                                 "(?:0[1-9]|1[0-2])/"
                                 "(?:(?:19|20|21|22)\d{2}))\s")
        elif re.findall(r"\s((?:0[1-9]|[1-2][0-9]|3[0|1])-"
                               "(?:[ADFJMNOS][A-Za-z]{2})-"
                               "(?:(?:19|20|21)\d{2}))\s", dataline):
            date_pattern = "%d-%b-%Y"
            regex_pattern = ("\s((?:0[1-9]|[1-2][0-9]|3[0|1])-"
                                  "(?:[ADFJMNOS][A-Za-z]{2})-"
                                  "(?:(?:19|20|21|22)\d{2}))\s")
        else:
            print "unknown date type"
            raise ValueError
        return date_pattern, regex_pattern

    dates = []
    mod_dates = {}
    f = open(filename, "r+")   # add filename check
    buf = mmap.mmap(f.fileno(), 0)
    filetype, breaker = filetypecheck(buf)
    line = buf.readline()
    num = 0
    firstdataline = 0
    while not re.search(r"^%s$" % (breaker), line):
        num += 1
        if re.search(r"^\s*[-]*\r\n$", line):
            commentaryline = num
            firstdataline = buf.tell()
        elif re.findall(r"\s(DATE)", line):  # WHY???
#            header = num
            pass
        line = buf.readline()
    buf.seek(firstdataline)
    dataline = buf.readline()
    d_pattern, r_pattern = dateformatcheck(dataline)
    dataheight = num - commentaryline
    for unused_i in range(dataheight):  # получение массива дат
#        locale.setlocale(locale.LC_ALL, 'en_US.utf8')
        cur_date = datetime.strptime(re.findall(r_pattern, dataline)[0],
                                                            d_pattern)
        dataline = buf.readline()
        dates.append(cur_date)
    for date in dates:
        if date.month == 1:
            mod_dates[date.year] = dates.index(date)
    storage.dates = mod_dates
    config.filetype = filetype
    config.breaker = breaker
    config.r_pattern = r_pattern
    storage.minimal_year = min(storage.dates.keys())


#Excel write module
@timer
def renderData(filename, **kwargs):
    import xlwt
    from datetime import datetime

    from xlwt.Utils import rowcol_to_cell
    lateral = kwargs.get('lateral')
    debug = kwargs.get('debug')
    if progress.wasCanceled():
            return

    if hasattr(storage, 'category'):  # cut if not in category
        pat = ['WOPT', 'WWPT', 'WGPT', 'WOIT', 'WWIT', 'WGIT']
        tmp = list(storage.wells)
        for wells in tmp:
            if not wells in storage.category:
                del(storage.wells[wells])
        for wells in storage.wells:  # bad intendation
            k = float(storage.category[wells])
            for p in pat:
                if p in storage.wells[wells]:
                    storage.wells[wells][p] = list(
                        map(lambda x: x * k, storage.wells[wells][p]))

    mask = list(storage.mask)
    oil_density = int(const.oil_density)
    water_density = int(const.water_density)

    font0 = xlwt.Font()
    font0.name = 'Times New Roman'
    wb = xlwt.Workbook()
    ws = wb.add_sheet(u'gosplan_input')

    oil_PR = storage.production_rate('WOPT')  # TODO: save to list
    oil_PR_tons = [x * oil_density / 1000000 for x in oil_PR]
    water_PR = storage.production_rate('WWPT')
    water_PR_tons = [x * water_density / 1000000 for x in water_PR]
    gas_PR = storage.production_rate('WGPT')
    gas_PR_mln = [x / 1000000 for x in gas_PR]
    liq_PR_tons = list(map(lambda x, y: x + y, oil_PR_tons, water_PR_tons))
    water_IR = storage.production_rate('WWIT')
    water_IR_tons = [x / 1000 for x in water_IR]
#            datetime.strptime(storage.override[well], "%d/%m/%Y")
    for well in storage.wells:
        storage.add_First_Year(well)
        if hasattr(storage, 'override'):
            if well in storage.override:
                # logger override well
                date = datetime.strptime(storage.override[well], "%d/%m/%Y")
                storage.add_First_Year(well, year=date.year)

    new_wells_liq_tons = list(map(lambda x, y: (x * oil_density + y *
                                                water_density) / 1000000,
                             storage.parameters.get('NOPT', mask),
                             storage.parameters.get('NWPT', mask)))
    new_wells_oil_tons = list(map(lambda x: x * oil_density / 1000000,
                                  storage.parameters.get('NOPT', mask)))

    n = 0
    for unused_years in oil_PR:
        n += 1
        ws.write(14, n, xlwt.Formula(   # Watercut
                "IF(%(liquid)s=0;0;(%(liquid)s-%(oil)s)/%(liquid)s*100)"
                % {"liquid": rowcol_to_cell(11, n),
                   "oil":    rowcol_to_cell(10, n)}
                 ))
        ws.write(25, n, xlwt.Formula(   # New wells watercut
                "IF(%(liquid)s=0;0;(%(liquid)s-%(oil)s)/%(liquid)s*100)"
                % {"liquid": rowcol_to_cell(24, n),
                   "oil":    rowcol_to_cell(23, n)}
                ))
        ws.write(37, n, xlwt.Formula(   # Wells from drilling
                "(%s+%s)"
                % (rowcol_to_cell(38, n),   # Production wells
                   rowcol_to_cell(39, n))   # Injection wells
                ))
        ws.write(26, n, xlwt.Formula(   # oil rate of new wells
                "IF(%(worktime)s=0;0;(%(oil)s/%(worktime)s)/30.25*1000)"
                % {"worktime": rowcol_to_cell(28, n),
                   "oil":   rowcol_to_cell(23, n)}
                ))
        ws.write(27, n, xlwt.Formula(   # fluid rate of new wells
                "IF(%(worktime)s=0;0;(%(fluid)s/%(worktime)s)/30.25*1000)"
                % {"worktime": rowcol_to_cell(28, n),
                   "fluid":   rowcol_to_cell(24, n)}
                ))
    index_output_well = list(storage.output_well(well)
                             for well in storage.wells
                             if storage.output_well(well))
    print index_output_well
    all_output_well = list(mask)
    output_wells_prod = list(mask)
    output_wells_inj = list(mask)
    for year, welltype in index_output_well:
        all_output_well[year] += 1
        if welltype:
            output_wells_inj[year] += 1
        else:
            output_wells_prod[year] += 1

    for wellname in storage.wells:  # initiating classification of wells
        storage.well_classification(wellname)
        storage.well_classification2(wellname)
        storage.well_classification3(wellname)

    reservoir_pres = storage.avg_pressure('WBPN')
    bottomhole_pres = storage.avg_pressure('WBHP')
    prod_wells = storage.well_fond(2)
    inj_wells = storage.well_fond(1)
    inj_transfer = []
    for wellname in storage.wells:
        if "First_run" in storage.wells[wellname]:
            check = storage.inj_transfer_check(wellname)
        else:
            check = list(mask)
        if not inj_transfer:
            inj_transfer = list(check)
        else:
            inj_transfer = list(map(lambda x, y: x + y, inj_transfer, check))
        if storage.wells[wellname]['First_run'][1] == 'Production_transfered':
            output_wells_prod = list(map(lambda x, y: x + y, check,
                                          output_wells_prod))

    work_time = list(storage.mask)  # bad
    for wells in storage.wells.values():
        if not (wells['First_run'][1] == "Exploratory" or
            wells['First_run'][1] == "Dummy"):
            work_time[wells['First_run'][0] - storage.minimal_year] += \
                     wells['First_run'][2]

    storage.mask.pop(0)
    inj = list(storage.mask)
    prod = list(storage.mask)
    for years, unused_val in enumerate(storage.mask):
        for wells in storage.wells:
            if storage.wells[wells]['cls_mask'][years] == 2:
                prod[years] += storage.wells[wells]['In_work'][years]
            if storage.wells[wells]['cls_mask'][years] == 1:
                inj[years] += storage.wells[wells]['In_work'][years]

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
        for well in storage.wells:
            printDebugRow(well, [], n)
            n += 1
            for parameter in storage.wells[well]:
                printDebugRow(parameter, storage.wells[well][parameter], n)
                n += 1

    printRow(u'Годы', sorted(storage.dates.iterkeys()), 0)

    printRow(u'Годовые показатели', [], 9)
    printRow(u'   Годовая добыча нефти, тыс.т', oil_PR_tons, 10)
    printRow(u'   Годовая добыча жидкости, тыс.т', liq_PR_tons, 11)
    printRow(u'   Годовая добыча газа, млн.м3', gas_PR_mln, 12)
    printRow(u'   Годовая закачка воды, тыс.м3', water_IR_tons, 13)
    printRow(u'   Обводненность,%', [], 14)

    printRow(u'Показатели новых скважин', [], 22)
    printRow(u'   Добыча нефти, тыс.т/год', new_wells_oil_tons, 23)
    printRow(u'   Добыча жидкости, тыс.т/год', new_wells_liq_tons, 24)
    printRow(u'   Обводненность,%', [], 25)
    printRow(u'   Дебит нефти, т/сут', [], 26)
    printRow(u'   Дебит жидкости, т/сут', [], 27)
    printRow(u'   Время работы', work_time, 28)

    printRow(u'Действ. фонд скважин', [], 33)
    printRow(u'   добывающих', prod_wells, 34)
    printRow(u'   нагнетательных', inj_wells, 35)

    printRow(u'Ввод скважин из бурения', [], 37)
    printRow(u'   добывающих', storage.parameters.get('NPW', mask), 38)
    printRow(u'   нагнетательных', storage.parameters.get('NIW', mask), 39)
    if lateral:
        printRow(u'   боковые стволы', storage.parameters.get('NLB', mask), 40)

    printRow(u'Перевод из доб. в нагн.', inj_transfer, 41)

    printRow(u'Выбытие скважин', all_output_well, 43)
    printRow(u'   добывающих', output_wells_prod, 44)
    printRow(u'      в т.ч. под закачку', inj_transfer, 45)
    printRow(u'   нагнетательных', output_wells_inj, 46)

    printRow(u'Ср. взв. пластовое давление, атм',
                    storage.parameters.get('FPRP', mask), 48)  # FPRP or FPR
    printRow(u'   в зоне отбора, атм', reservoir_pres[0], 49)
    printRow(u'   в зоне закачки, атм', reservoir_pres[1], 50)

    printRow(u'Ср. забойное давление доб. скважин, атм',
                                    bottomhole_pres[0], 52)
    printRow(u'Ср. забойное давление нагн. скважин, атм',
                                    bottomhole_pres[1], 53)

    printRow(u'Время работы добывающих скважин',
                                    prod, 54)
    printRow(u'Время работы нагнетательных скважин',
                                    inj, 55)
    progress.setValue(100)
    print storage.wells.keys()
    try:
        wb.save(filename)
        ui.informationMessage(u"Завершено")
    except:
        ui.informationMessage(u"<p>Не удалось сохранить файл</p>",
                              caption=u"Ошибка сохранения")


if __name__ == "__main__":
    const = _Constants()
    config = _Constants()
    storage = WellStorage()
    category = _Constants()
    app = QtGui.QApplication(sys.argv)
    mainwindow = QtGui.QMainWindow()
    progress = QtGui.QProgressDialog(u"Подготовка отчета...",
                                        u"Отмена", 0, 100)
    progress.setWindowTitle(QtGui.QApplication.translate("Progress", "Fontaine", None, QtGui.QApplication.UnicodeUTF8))
    progress.setWindowModality(QtCore.Qt.WindowModal)
    ui = Ui_MainWindow()
    ui.setupUi(mainwindow)

    def ignition():
        info_file = open("info.log", "w")
        sys.stdout = info_file
        error_file = open("error.log", "w")
        sys.stderr = error_file
        filename = ui.lineEdit.text()
        well_filename = ui.lineEdit_2.text()
        savefile = ui.setSaveFileName()
        const.reset()  # Блок try не помешал бы
        config.reset()
        config_init('config.ini')
        wells_init(well_filename)
        wells_input_override('input.ini')

        if filename and savefile:
            getline(filename, lateral=ui.tracks.isChecked())
            renderData(savefile, debug=ui.debug.isChecked(),
                       lateral=ui.tracks.isChecked())
            storage.clear()
        elif not filename:
            ui.informationMessage(u"Выберите файл для обработки",
                                  caption=u"Ошибка запуска")
        else:
            ui.informationMessage(u"Выберите файл для сохранения",
                                  caption=u"Ошибка запуска")
        info_file.close()
        error_file.close()
    ui.pushButton_2.clicked.connect(ignition)

    mainwindow.show()
    sys.exit(app.exec_())


#Garbage

#ws.write(0, 0, 'Test', style0)
#ws.write(1, 0, datetime.now(), style1)
#ws.write(2, 2, xlwt.Formula("A3+B3"))

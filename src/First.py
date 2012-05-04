# -*- coding: UTF-8 -*-

'''
Created on 03.04.2012

@author: Alexei Partilov
'''

#TODO : december pattern for cls_mask

from __future__ import division
import xlwt
from xlwt.Utils import rowcol_to_cell
import sys
from datetime import datetime
from time import time
import re
import linechc
import mmap
import ConfigParser
#import locale
from WellStorage import *
from PySide import QtGui, QtCore
from fontaine_ui import Ui_MainWindow


class _Constants:   # this class store initial data and constants
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError, "Can't rebind const(%s)" % name
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise self.ConstError, "Can't unbind const(%s)" % name
        raise NameError + name


def timer(f):  # time benchmark
    def tmp(*args, **kwargs):
        t = time()
        res = f(*args, **kwargs)
        print "Время выполнения функции: %f" % (time() - t)
        return res
    return tmp


@timer
def bufcount(filename):
    f = open(filename)
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read  # loop optimization
    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)
    return lines


@timer
def mapcount(filename):  # file uploading into memory?
    f = open(filename, "r+")
    buf = mmap.mmap(f.fileno(), 0)
    lines = 0
    readline = buf.readline
    while readline():
        lines += 1
    return lines


def config_init(filename):
    try:
        config = ConfigParser.ConfigParser()
        config.read(filename)
        const.oil_density = config.get('Fluid Properties', 'OIL_DENSITY')
        const.water_density = config.get('Fluid Properties', 'WATER_DENSITY')
    except:
        pass


def initialization(filename):
    try:
        if not linechc.getline(filename, 1):  # checking file
            raise IOError
        breaker = linechc.getline(filename, 1)
        if breaker == "1\n":
            filetype = "tempest"
        elif breaker == "\n":
            filetype = "eclipse"
        else:
            raise IOError
        n = 2
        dates = []
        commentaryline = 0
        header = 0
        mod_dates = {}
        line = linechc.getline(filename, n)
        while not re.search(r"^%s$" % (breaker), line):
            n += 1
            line = linechc.getline(filename, n)
            if re.search(r"^\s+[-]*\n$", line):
                commentaryline = n
            elif re.findall(r"\s(DATE)", line):
                header = n
        line = linechc.getline(filename, 1 + commentaryline)
        date_pattern = ""  # date format check
        regex_pattern = ""
        if re.findall(r"\s((?:0[1-9]|[1-2][0-9]|3[0|1])/"
                             "(?:0[1-9]|1[0-2])/"
                             "(?:(?:19|20|21)\d{2}))\s", line):
            date_pattern = "%d/%m/%Y"
            regex_pattern = ("\s((?:0[1-9]|[1-2][0-9]|3[0|1])/"
                                 "(?:0[1-9]|1[0-2])/"
                                 "(?:(?:19|20|21)\d{2}))\s")
        elif re.findall(r"\s((?:0[1-9]|[1-2][0-9]|3[0|1])-"
                               "(?:[ADFJMNOS][A-Za-z]{2})-"
                               "(?:(?:19|20|21)\d{2}))\s", line):
            date_pattern = "%d-%b-%Y"
            regex_pattern = ("\s((?:0[1-9]|[1-2][0-9]|3[0|1])-"
                                  "(?:[ADFJMNOS][A-Za-z]{2})-"
                                  "(?:(?:19|20|21)\d{2}))\s")
        else:
            print "unknown date type"
            raise ValueError

        for i in range(n - 1 - commentaryline):  # получение массива дат
            line = linechc.getline(filename, i + 1 + commentaryline)
#            locale.setlocale(locale.LC_ALL, 'en_US.utf8')
            cur_date = datetime.strptime(re.findall(regex_pattern, line)[0],
                                                                date_pattern)
            dates.append(cur_date)  # TODO заменить на regex?
        for date in dates:
            if date.month == 1:
                mod_dates[date.year] = dates.index(date)
        config.dates = mod_dates

        mod_dates = {}
        for date in dates:
            if date.month == 12:
                mod_dates[date.year] = dates.index(date)
        if filetype == "eclipse":
            config.dates_dec = config.dates
        else:
            config.dates_dec = mod_dates
#        storage.mask = [0 for unused_item in config.dates]
        config.filetype = filetype
        config.lines = n - 1
        config.headerline = header
        config.header = commentaryline
        storage.minimal_year = min(config.dates.keys())
#        return data

    except IOError as(errno, strerror):
        print "Ошибка ввода/вывода({0}: {1})".format(errno, strerror)
        raise
    except:
        print "Где-то что-то пошло не так", sys.exc_info()[0]
        raise


# Open text file module
@timer
def parseData(filename):

    def countMonth(pointer, data):
        m = 0
        start = mod_dates[pointer]
        for curr, nextt in pairs(range(13)):
            if (float(data[nextt + start][key]) -
                    float(data[curr + start][key]) > 0):
                m += 1
        return m

    filelength = mapcount(filename)
    initialization(filename)
    lines = config.lines
    headerlines = config.header
    headerline = config.headerline
    mod_dates = config.dates
    mod_dates_dec = config.dates_dec
    if config.filetype == "tempest":
        skipper = 1
    elif config.filetype == "eclipse":
        skipper = 0

    n = 2
    while linechc.getline(filename, n):
        progress.setValue(int((n / filelength) * 100))
        if progress.wasCanceled():
            break
        header = linechc.getline(filename, n + headerline - 2)
        numbers = linechc.getline(filename, n + headerline + skipper)  # +1
        # searching right headers
        if re.findall(r"\b(W[O|G|W][I|P]T|WBPN|WBHP|FPRP)\b", header):
            necessary_headers = re.findall(
                                r"\b(W[O|G|W][I|P]T|WBPN|WBHP|FPRP)\b", header)
            all_headers = re.findall(r"([A-Z0-9]+)", header)
            all_numbers = re.findall(r"\b([\w-]+)\b", numbers)
            if ((len(all_headers) - 1) > len(all_numbers)) and numbers != "\n":
                temp_num = numbers[14:]
                all_numbers = []
                nn = 0
                while nn + 13 < len(temp_num):
                    if re.match(r"^([\w-]+)\b", temp_num[nn:nn + 13]):
                        all_numbers.append(re.match(r"^([\w-]+)\b",
                                                temp_num[nn:nn + 13]).group(0))
                    else:
                        all_numbers.append("N/A")
                    nn += 13
            index = []
            data = []

            #Comparision of the headers
#            def indices(mylist, value):
#                return [i for i, x in enumerate(mylist) if x == value]
#            for values in necessary_headers:
#                index.append(indices(all_headers, values))
            index = [all_headers.index(value) for value in necessary_headers]

            for i in range(lines - headerlines):  # parsing the data
                txtline = linechc.getline(filename, n + i - 1 + headerlines)
                dataline = re.findall(r"\s((?:[-+]?[0-9]*\.[0-9]*E?-?[0-9]*)|0)\s",
                                       txtline)
                comp_dataline = []  # necessary data in current line
                comp_dataline = [dataline[key - 1] for key in index]
                data.append(comp_dataline)  # list of necessary data

            for value in index:  # compression of the array
                key = index.index(value)
                welldata = []
                worktime = []
                if re.match(r"^(W[O|G|W][I|P]T)$", necessary_headers[key]):
                    firstYear = True
                    for cur, next in pairs(sorted(mod_dates)):
                        cur_line = mod_dates[cur]
                        next_line = mod_dates[next]
                        welldata.append(
                            float(data[next_line][key]) - \
                                float(data[cur_line][key]))
                        if mod_dates[next] - mod_dates[cur] < 10:
                            m = "N/A"
                        else:
                            m = countMonth(cur, data)
                        worktime.append(m)
                        if float(data[next_line][key]) - \
                        float(data[cur_line][key]) > 0 and firstYear:
                            storage.add_First_Year(cur, necessary_headers[key],
                                                all_numbers[value - 1], m)

                            mask = list(storage.mask)
                            mask[cur - min(config.dates.keys())] += \
                                float(data[next_line][key]) - \
                                 float(data[cur_line][key])  # bad line
                            storage.add_parameter("N" +
                                    necessary_headers[key][1:3] + "T", mask)
                            firstYear = False
                    storage.add_worktime(all_numbers[value - 1], worktime)
                    storage.add_well(all_numbers[value - 1],
                                  necessary_headers[key], welldata)
                    storage.add_well(all_numbers[value - 1],
                                  necessary_headers[key], welldata)
                    if 'First_run' in storage.wells[all_numbers[value - 1]]:
                        mask = list(storage.mask)

                if re.match(r"^(WBPN|WBHP)$", necessary_headers[key]):
                    for year in sorted(mod_dates_dec.values()):
                        welldata.append(float(data[year][key]))
                    storage.add_well(all_numbers[value - 1],
                                  necessary_headers[key], welldata)
                    storage.add_well(all_numbers[value - 1],
                                  necessary_headers[key], welldata)
                if re.match(r"^(FPRP)$", necessary_headers[key]):
                    for year in sorted(mod_dates_dec.values()):
                        welldata.append(float(data[year][key]))
                    storage.add_parameter(necessary_headers[key], welldata)
            n += lines      # jump to next block
        else:
            n += lines    # anyway


#Excel write module
@timer
def renderData(filename):
    if progress.wasCanceled():
            return
    mask = list(storage.mask)
    oil_density = int(const.oil_density)
    water_density = int(const.water_density)

    font0 = xlwt.Font()
    font0.name = 'Times New Roman'
    wb = xlwt.Workbook()
    ws = wb.add_sheet(u'gosplan_input')
    debuglist = wb.add_sheet(u'debug')

    oil_PR = storage.production_rate('WOPT')
    oil_PR_tons = [x * oil_density / 1000000 for x in oil_PR]
    water_PR = storage.production_rate('WWPT')
    water_PR_tons = [x * water_density / 1000000 for x in water_PR]
    gas_PR = storage.production_rate('WGPT')
    gas_PR_mln = [x / 1000000 for x in gas_PR]
    liq_PR_tons = list(map(lambda x, y: x + y, oil_PR_tons, water_PR_tons))
    water_IR = storage.production_rate('WWIT')
    water_IR_tons = [x / 1000 for x in water_IR]
    new_wells_liq_tons = list(map(lambda x, y: (x * oil_density + y *
                                                water_density) / 1000000,
                             storage.parameters.get('NOPT', mask),
                             storage.parameters.get('NWPT', mask)))
    new_wells_oil_tons = list(map(lambda x: x * oil_density / 1000000,
                                  storage.parameters.get('NOPT', mask)))

    n = 0
    for unused_years in oil_PR:
        n += 1
        cell1 = rowcol_to_cell(10, n)
        cell2 = rowcol_to_cell(11, n)
        ws.write(14, n, xlwt.Formula(
                "IF(%s=0;0;(%s-%s)/%s*100)" % (cell2, cell2, cell1, cell2))
                 )

        cell3 = rowcol_to_cell(23, n)
        cell4 = rowcol_to_cell(24, n)
        ws.write(25, n, xlwt.Formula(
                "IF(%s=0;0;(%s-%s)/%s*100)" % (cell4, cell4, cell3, cell4))
                 )

        cell5 = rowcol_to_cell(38, n)
        cell6 = rowcol_to_cell(39, n)
        ws.write(37, n, xlwt.Formula("(%s+%s)" % (cell5, cell6)))

        cell7 = rowcol_to_cell(23, n)
        cell8 = rowcol_to_cell(28, n)
        ws.write(26, n, xlwt.Formula(
                "IF(%s=0;0;(%s/%s)/30.25*1000)" % (cell8, cell7, cell8))
                 )

        cell9 = rowcol_to_cell(24, n)
        cell0 = rowcol_to_cell(28, n)
        ws.write(27, n, xlwt.Formula(
                "IF(%s=0;0;(%s/%s)/30.25*1000)" % (cell0, cell9, cell0))
                 )

    index_output_well = list(storage.output_well(well)
                             for well in storage.wells
                             if storage.output_well(well))
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

    reservoir_pres = storage.avg_pressure('WBPN')
    bottomhole_pres = storage.avg_pressure('WBHP')

    prod_wells = storage.well_fond(2)
    inj_wells = storage.well_fond(1)
    inj_transfer = []
    for wellname in storage.wells:
        check = storage.inj_transfer_check(wellname)
        if not inj_transfer:
            inj_transfer = list(check)
        else:
            inj_transfer = list(map(lambda x, y: x + y, inj_transfer, check))
        if storage.wells[wellname]['First_run'][1] == 'Production_transfered':
            output_wells_prod = list(map(lambda x, y: x + y, check,
                                          output_wells_prod))

    work_time = list(storage.mask)  # bad
    for wells in storage.wells.values():
        if not wells['First_run'][1] == "Exploratory":
            work_time[wells['First_run'][0] - storage.minimal_year] += \
                     wells['First_run'][2]

    def printRow(name, data, y):
        x = 0
        ws.write(y, x, name)
        x += 1
        for key in data:
            ws.write(y, x, key)
            x += 1

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

    printRow(u'Годы', sorted(config.dates_dec.iterkeys()), 0)

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

    printRow(u'Перевод из доб. в нагн.', inj_transfer, 41)

    printRow(u'Выбытие скважин', all_output_well, 43)
    printRow(u'   добывающих', output_wells_prod, 44)
    printRow(u'      в т.ч. под закачку', inj_transfer, 45)
    printRow(u'   нагнетательных', output_wells_inj, 46)

    printRow(u'Ср. взв. пластовое давление, атм', storage.parameters.get('FPRP',mask), 48)   
    printRow(u'   в зоне отбора, атм', reservoir_pres[0], 49)
    printRow(u'   в зоне закачки, атм', reservoir_pres[1], 50)
    
    printRow(u'Ср. забойное давление доб. скважин , атм', bottomhole_pres[0], 52)   
    printRow(u'Ср. забойное давление нагн. скважин , атм', bottomhole_pres[1], 53)
    printRow(u'Список скважин', storage.wells, 54)
    printRow(u'С боковым стволом', storage.lateral_borehole, 55)            
    
    progress.setValue(100)   
    try: 
        wb.save(filename)
        ui.informationMessage(u"Завершено")
    except: 
        ui.informationMessage(u"<p>Не удалось сохранить файл</p>")

if __name__ == "__main__":
    const = _Constants()
    config = _Constants()
    storage = WellStorage()
#    sys.stdout = open("info.log", "w")
#    sys.stderr = open("error.log", "w")
    config_init('config.ini')
    app = QtGui.QApplication(sys.argv)
    mainwindow = QtGui.QMainWindow()
    progress = QtGui.QProgressDialog(u"Подготовка отчета...", u"Отмена", 0, 100)
    progress.setWindowModality(QtCore.Qt.WindowModal)
    ui = Ui_MainWindow()
    ui.setupUi(mainwindow)
    
    def ignition ():
        filename = ui.lineEdit.text()
        savefile = ui.setSaveFileName()
        
        if filename and savefile: 
            parseData(filename)
            renderData(savefile)
        elif not filename:
            ui.informationMessage(u"Выберите файл для обработки")
        else:
            ui.informationMessage(u"Выберите файл для сохранения")
    ui.pushButton_2.clicked.connect(ignition)
    
    mainwindow.show()
    sys.exit(app.exec_())


#Garbage

#ws.write(0, 0, 'Test', style0)
#ws.write(1, 0, datetime.now(), style1)
#ws.write(2, 2, xlwt.Formula("A3+B3"))
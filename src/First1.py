# -*- coding: UTF-8 -*-

'''
Created on 03.04.2012

@author: Alexei Partilov
'''

#TODO : december pattern for cls_mask

from __future__ import division
import sys
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
    from time import time
    def tmp(*args, **kwargs):
        t = time()
        res = f(*args, **kwargs)
        print "Время выполнения функции: %f" % (time() - t)
        return res
    return tmp

@timer
def mapcount(filename):  # input file lines counter
    import mmap          # whole file in memory
    f = open(filename, "r+")
    buf = mmap.mmap(f.fileno(), 0)
    lines = 0
    readline = buf.readline
    while readline():
        lines += 1
    f.close()
    return lines


def config_init(filename):
    import ConfigParser
    try:
        config = ConfigParser.ConfigParser()
        config.read(filename)
        const.oil_density = config.get('Fluid Properties', 'OIL_DENSITY')
        const.water_density = config.get('Fluid Properties', 'WATER_DENSITY')
    except:
        pass


@timer
def getline(file):
    import re
    import mmap
    line = ''
    filelength = mapcount(file)
    initialization(file)

    def parseBlock(pointer):
        result = {}
        #Reading header
        buf.seek(pointer)
        header_str = buf.readline()
        headers = re.findall(r"([A-Z0-9]+)", header_str)
        result['headers'] = re.findall(r"\b(W[O|G|W][I|P]T|WBPN|WBHP|FPRP?)\b",
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
        buf.readline()
        numbers_str = buf.readline()
        numbers = re.findall(r"\b([E0-9.-]+)\b", numbers_str)
        if ((len(headers) - 1) > len(numbers)) and numbers != "\n":
            temp_num = numbers[14:]   # bad block of code
            numbers = []
            nn = 0
            while nn + 13 < len(temp_num):
                if re.match(r"^([\w-]+)\b", temp_num[nn:nn + 13]):
                    numbers.append(re.match(r"^([\w-]+)\b",
                                            temp_num[nn:nn + 13]).group(0))
                else:
                    numbers.append("N/A")
                nn += 13
        result['numbers'] = [numbers[i - 1] for i in index if numbers]
        #Reading data
        line = buf.readline()
        while not re.search(config.r_pattern, line):
            line = buf.readline()
        data = line
        result['data'] = []
        while not data == config.breaker:  # parsing the data
            dataline = re.findall(r"\s((?:[-+]?[0-9]*\.[0-9]*E?-?[0-9]*)|0)\s",
                                   data)
            result['data'].append([dataline[i - 1] for i in index])
            data = buf.readline()
        return result

    f = open(file, "r+")
    buf = mmap.mmap(f.fileno(), 0)  # add filename check
    n = 0
    buf.seek(n)
    while buf.find("SUMMARY", n) != -1:
        n = buf.find("SUMMARY", n)
        m = buf.find("DATE", n)
        buf.seek(n)
        n += 1
        buf.seek(m)
        str = buf.readline()
        if re.findall(r"\b(W[O|G|W][I|P]T|WBPN|WBHP|FPRP?)\b", str):
            block = parseBlock(m)
            for key, well_num in enumerate(block['numbers']):
                data = [i[key] for i in block['data']]
                parameter = block['headers'][key]

                if re.match(r"^(W[O|G|W][I|P]T)|(WBPN|WBHP)$", parameter):
                    storage.add_well(well_num, parameter, data)

                if re.match(r"^(FPRP?)$", parameter):
                    welldata = []
                    for year in sorted(storage.dates.values()):
                        welldata.append(float(data[year]))
                    storage.add_parameter(parameter, welldata)

    f.close()
    return line


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
                             "(?:(?:19|20|21)\d{2}))\s", dataline):
            date_pattern = "%d/%m/%Y"
            regex_pattern = ("\s((?:0[1-9]|[1-2][0-9]|3[0|1])/"
                                 "(?:0[1-9]|1[0-2])/"
                                 "(?:(?:19|20|21)\d{2}))\s")
        elif re.findall(r"\s((?:0[1-9]|[1-2][0-9]|3[0|1])-"
                               "(?:[ADFJMNOS][A-Za-z]{2})-"
                               "(?:(?:19|20|21)\d{2}))\s", dataline):
            date_pattern = "%d-%b-%Y"
            regex_pattern = ("\s((?:0[1-9]|[1-2][0-9]|3[0|1])-"
                                  "(?:[ADFJMNOS][A-Za-z]{2})-"
                                  "(?:(?:19|20|21)\d{2}))\s")
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
        elif re.findall(r"\s(DATE)", line):
            header = num
        line = buf.readline()
    buf.seek(firstdataline)
    dataline = buf.readline()
    d_pattern, r_pattern = dateformatcheck(dataline)
    dataheight = num - commentaryline
    for i in range(dataheight - 1):  # получение массива дат
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
#    config.dataheight = dataheight
    storage.minimal_year = min(storage.dates.keys())


#Excel write module
@timer
def renderData(filename):
    import xlwt
    from xlwt.Utils import rowcol_to_cell
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
    for well in storage.wells:
        print well
        storage.add_First_Year(well)
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
        print wells['First_run']
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

    printRow(u'Перевод из доб. в нагн.', inj_transfer, 41)

    printRow(u'Выбытие скважин', all_output_well, 43)
    printRow(u'   добывающих', output_wells_prod, 44)
    printRow(u'      в т.ч. под закачку', inj_transfer, 45)
    printRow(u'   нагнетательных', output_wells_inj, 46)

    printRow(u'Ср. взв. пластовое давление, атм', storage.parameters.get('FPR',mask), 48) # FPRP or FPR
    printRow(u'   в зоне отбора, атм', reservoir_pres[0], 49)
    printRow(u'   в зоне закачки, атм', reservoir_pres[1], 50)
    
    printRow(u'Ср. забойное давление доб. скважин , атм', bottomhole_pres[0], 53)   
    printRow(u'Ср. забойное давление нагн. скважин , атм', bottomhole_pres[1], 54)
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
            getline(filename)
            renderData(savefile)
            storage.clear()
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
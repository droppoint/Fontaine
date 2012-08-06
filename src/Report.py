# -*- coding: UTF-8 -*-

'''
Created on 18.06.2012

@author: APartilov
'''


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

    def __init__(self):
        '''
        Constructor
        '''
        self.reset()

    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
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

        wb.save(filename)

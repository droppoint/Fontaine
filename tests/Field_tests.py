'''
Created on 06.07.2012

@author: APartilov
'''
import unittest
from src.Field import Field

class Test(unittest.TestCase):

    def setUp(self):
        self.field = Field('Test Tield', [dates])
        self.field.add_well(number, parameter_code, data)
        self.field.add_parameter(parameter, data)
        self.field.add_well(number, parameter_code, data)
        self.field.add_parameter(parameter, data)

    def tearDown(self):
        pass

    def testName(self):
        self.field.production_rate(code)
        self.assertTrue(self.field.production_rate(code), [])

    def testName(self):
        self.field.well_fond(code)
        self.assertTrue(self.field.well_fond(code), [])

    def testName(self):
        self.field.avg_pressure(pres_type)
        self.assertTrue(self.field.avg_pressure(pres_type), [])

if __name__ == "__main__":
    unittest.main()

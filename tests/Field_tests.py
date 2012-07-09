'''
Created on 06.07.2012

@author: APartilov
'''
import unittest
from src.Field import Field
from src.Field import FieldError


class Test(unittest.TestCase):

    def setUp(self):
        self.field = Field('Test Tield', {'1990': 0, 1991: '1', 1992: '2'})
        self.field.add_well('402', {'WOPT': [1, 0, 2]})
        self.field.add_well('403', {'WOPT': [1, 0, 2]})
        self.field.wells['402'].dates = {'1990': 0, '1991': 2, '1992': 4}
        self.field.wells['403'].dates = {'1990': 0, '1991': 2, '1992': 4}

    def tearDown(self):
        self.field.clear()
        del(self.field)

    @unittest.skip("demonstrating skipping")
    def testProduction_rate(self):
        self.assertTrue(self.field.production_rate('WOPT'), [2, 0, 4])

    def testRoutine_operations(self):
        self.field.routine_operations()

    @unittest.skip("demonstrating skipping")
    def testWell_fond(self):
        self.assertTrue(self.field.well_fond('1'), [2, 0, 2])

    @unittest.skip("demonstrating skipping")
    def testPressure_type(self):
        self.field.avg_pressure('WBHP')
        self.assertTrue(self.field.avg_pressure('WBHP'), [])

    def testAdd_parameter(self):
        self.field.add_parameter('FPR', [1, 0, 2])
        with self.assertRaises(FieldError) as cm:
            self.field.add_parameter('FPRP', [2, 4, 0])
        the_exception = cm.exception
        self.assertEqual(the_exception.msg, "Repeated parameters")
if __name__ == "__main__":
    unittest.main()

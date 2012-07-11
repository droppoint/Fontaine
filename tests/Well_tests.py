# -*- coding: UTF-8 -*-
'''
Created on 18.05.2012

@author: APartilov
'''
import unittest
import os
import sys
sys.path.append(os.path.join(os.getcwd(), os.path.pardir))
from src.Well import Well


class Test(unittest.TestCase):

    def setUp(self):
        self.well = Well(data={'WOPT': [1, 1, 2, 4, 5]})
        self.well.add_parameter({'WWPT': [1, 1, 2, 4, 5]})
        self.well.add_parameter({'WLPR': [1, 1, 1, 2, 4]})

    def tearDown(self):
        del(self.well)

#    def test_add_well(self):
#        self.assertTrue(self.well)
#        self.assertEqual(self.well.classification, [2, 4, 2])

    def test_add_worktime(self):
        self.well.add_worktime()
        self.assertEqual(self.well.work_time, [12, 12])

    @unittest.skip("demonstrating skipping")
    def test_completion_year(self):
        self.well.add_worktime()
        self.well.completion_year()
        self.assertEqual(self.well.first_run, 0)

    @unittest.skip("demonstrating skipping")
    def test_abandonment_year(self):
        self.well.add_worktime()
        self.well.abandonment_year()
        self.assertEqual(self.well.abandonment, 'working')

    @unittest.skip("demonstrating skipping")
    def test_classification(self):
        self.well.add_worktime()
        self.well.completion_year()
        self.well.abandonment_year()
        self.well.well_classification()
        self.assertEqual(self.well.classification, [2, 4, 2, 2])

    @unittest.skip("demonstrating skipping")
    def test_classification_rate(self):
        self.well.add_worktime()
        self.well.completion_year()
        self.well.abandonment_year()
        self.well.well_classification(mode='rate')
        self.assertEqual(self.well.classification_by_rate, [2, 4, 2, 2])

    def test_compress_data(self):
        self.well.add_worktime({'1990': 0, '1991': 2, '1992': 4})
        self.well.compress_data({'1990': 0, '1991': 2, '1992': 4})
        self.assertEqual(self.well.parameters['WOPT'], [1, 3])
        self.assertEqual(self.well.parameters['WWPT'], [1, 3])
        self.assertEqual(self.well.parameters['WLPR'], [1, 4])

if __name__ == "__main__":
    sys.argv = ['', 'Test.testName']
    unittest.main()

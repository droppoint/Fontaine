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
        self.well = Well(data={'WOPT': [1, 0, 2, 4]})
        self.well.add_parameter({'WWPT': [1, 0, 2, 4]})
        self.well.add_parameter({'WLPR': [1, 0, 1, 2]})
        self.well.dates = {'1990': 0, '1991': 2, '1992': 4}

    def tearDown(self):
        del(self.well)

#    def test_add_well(self):
#        self.assertTrue(self.well)
#        self.assertEqual(self.well.classification, [2, 4, 2])

    def test_add_worktime(self):
        self.well.add_worktime()
        self.assertEqual(self.well.work_time, [6, 12])

    def test_completion_year(self):
        self.well.add_worktime()
        self.well.completion_year()
        self.assertEqual(self.well.first_run, 0)

    def test_abandonment_year(self):
        self.well.add_worktime()
        self.well.abandonment_year()
        self.assertEqual(self.well.abandonment, 'working')

    def test_classification(self):
        self.well.add_worktime()
        self.well.completion_year()
        self.well.abandonment_year()
        self.well.well_classification()
        self.assertEqual(self.well.classification, [2, 4, 2, 2])

    def test_classification_rate(self):
        self.well.add_worktime()
        self.well.completion_year()
        self.well.abandonment_year()
        self.well.well_classification(mode='rate')
        self.assertEqual(self.well.classification_by_rate, [2, 4, 2, 2])

if __name__ == "__main__":
    sys.argv = ['', 'Test.testName']
    unittest.main()

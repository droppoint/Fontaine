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
        self.well = Well('402', {'WOPT':[1, 0, 2]})
        self.well.add_parameter({'WWPT':[1, 0, 2]})
        self.well.dates = [0, 1, 2]
        self.well.add_worktime([1, 1, 2],'WOPT')
        self.well.completion_year()
        self.well.abandonment_year()
        self.well.well_classification()

    def tearDown(self):
        del(self.well)

    def test_add_well(self):
        self.assertTrue(self.well)
        self.assertEqual(self.well.classification, [2, 4, 2])

if __name__ == "__main__":
    sys.argv = ['', 'Test.testName']
    unittest.main()

# -*- coding: UTF-8 -*-
'''
Created on 18.05.2012

@author: APartilov
'''
import unittest
import os, sys
sys.path.append(os.path.join(os.getcwd(), os.path.pardir))
from Fontaine.WellStorage import WellStorage

class Test(unittest.TestCase):

    def setUp(self):
        self.storage = WellStorage()
        self.storage.dates = {0: 0, 1: 2}

    def tearDown(self):
        del(self.storage)

    def test_add_well(self):
        self.storage.add_well('402', 'WOPT', [1, 0, 2])
        self.assertTrue(self.storage.wells)
        self.assertTrue(self.storage.wells['402'])
        self.assertEqual(self.storage.wells['402']['WOPT'], [1])

if __name__ == "__main__":
    sys.argv = ['', 'Test.testName']
    unittest.main()

# -*- coding: UTF-8 -*-
'''
Created on 18.05.2012

@author: APartilov
'''
import unittest
import os, sys
sys.path.append(os.path.join(os.getcwd(), os.path.pardir))
from Fontaine import WellStorage

class Test(unittest.TestCase):

    def setUp(self):
        self.storage = WellStorage()

    def tearDown(self):
        del(self.storage)

    def test_add_well(self):
        self.storage.add_well('402', 'WOPT', [1, 0], lateral=True, adsfasd=False)
        self.assertTrue(self.storage.wells)
        self.assertTrue(self.storage.wells['402'])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

#import random
#import unittest
#class TestSequenceFunctions(unittest.TestCase):
#
#    def setUp(self):
#        self.seq = range(10)
#
#    def test_shuffle(self):
#        # проверяем, что в перемешанной последовательности
#        #не потерялись элементы
#        random.shuffle(self.seq)
#        self.seq.sort()
#        self.assertEqual(self.seq, range(10))
#
#    def test_choice(self):
#        element = random.choice(self.seq)
#        self.assertTrue(element in self.seq)
#
#    def test_sample(self):
#        self.assertRaises(ValueError, random.sample, self.seq, 20)
#        for element in random.sample(self.seq, 5):
#            self.assertTrue(element in self.seq)
#
#if __name__ == '__main__':
#    unittest.main(

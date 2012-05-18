# -*- coding: UTF-8 -*-
'''
Created on 18.05.2012

@author: APartilov
'''
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testName(self):
        pass


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

'''
Created on 22.06.2012

@author: APartilov
'''
import unittest
import src.Parser as par


class Test(unittest.TestCase):

    def setUp(self):
        self.p = par.Parser('Kosh_case2.rsm')

    def tearDown(self):
        pass

    def testTempestParseFile(self):
        for i in self.p.parse_file():
            pass

    def testEclipseParseFile(self):
        for i in self.p.parse_file():
            pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

'''
Created on 22.06.2012

@author: APartilov
'''
import unittest
import Fontaine.Parser as par


class Test(unittest.TestCase):

    def setUp(self):
        self.p = par.Parser()

    def tearDown(self):
        pass

    def testTempestParseFile(self):
        self.p.parse_file('test.rsm')

    def testEclipseParseFile(self):
        self.p.parse_file('testeclipse.rsm')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

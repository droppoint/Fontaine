'''
Created on 22.06.2012

@author: APartilov
'''
import unittest
import src.Parser as par


class Test(unittest.TestCase):

    def setUp(self):
        self.p = par.Parser()

    def tearDown(self):
        pass

    def testTempestParseFile(self):
        for i in self.p.parse_file('test.rsm'):
            print i

    def testEclipseParseFile(self):
        for i in self.p.parse_file('testeclipse.rsm'):
            print i

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

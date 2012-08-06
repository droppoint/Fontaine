# -*- coding: UTF-8 -*-

'''
Created on 06.08.2012

@author: APartilov
'''

import pstats
import sys

if __name__ == '__main__':
    sys.stdout = open('stats_report.report', 'w')
    p = pstats.Stats('fontaine.pyprof')
    p.sort_stats('calls')
    p.print_stats()
    p.sort_stats('time')
    p.print_stats()

    

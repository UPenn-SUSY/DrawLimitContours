#!/usr/bin/env python

import sys
import os.path
import optparse
import time
import math

# ------------------------------------------------------------------------------
def readFile(in_file_name):
    input = []
    f = file(in_file_name, 'r')
    for l in f.readlines():
        pieces = l.split()
        if len(pieces) == 0: continue
        if pieces[0] == '#': continue
        print l.split()

        dsid = pieces[0]
        mc1 = pieces[1]
        mn0 = pieces[2]
        zn_me = max(0.,float(pieces[3]))
        zn_mm = max(0.,float(pieces[4]))
        zn_combined = math.sqrt(zn_me*zn_me + zn_mm*zn_mm)

        input.append( { 'dsid':dsid
                      , 'mc1':mc1
                      , 'mn0':mn0
                      , 'zn_me':zn_me
                      , 'zn_mm':zn_mm
                      , 'zn_combined':zn_combined
                      }
                    )
    return input

# ------------------------------------------------------------------------------
def printToFile(info, out_file_name):
    out_file = file(out_file_name,'w')
    out_file.write('# DSID\tmc1\tmn0\tZn_me\tZn_mm\tZn_combined\n')
    for i in info:
        out_file.write('%(dsid)s\t%(mc1)s \t%(mn0)s \t%(zn_me)s   \t%(zn_mm)s   \t%(zn_combined)s\n' % i)

if __name__ == '__main__':
    input = readFile('channel_sensitivities.txt')
    print input
    printToFile(input, 'combined_sensitities.txt')

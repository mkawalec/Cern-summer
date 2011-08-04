#!/usr/bin/env python2.5
"""plotpulls.py

usage::
    plotpulls.py FILE1 [FILE2 ...]

"""

import sys
import os.path
import re

import ROOT
ROOT.gROOT.SetBatch(1)

from professor.tools.rootplot import plotRootHistogram

pathre = re.compile(r'/(?P<DIM>\d+)D/(?P<MC>\d+)MC_(?P<NR>\d+)\.dat')

def plotPullData(path):
    path = os.path.abspath(path)
    print path
    mdict = pathre.search(path).groupdict()
    f = open(path)
    h = ROOT.TH1F('h_pull', 'h_pull', 10, -10, 10)
    dim = int(mdict['DIM'])
    mc = int(mdict['MC'])
    nr = int(mdict['NR'])

    for line in f:
        if not line.startswith('#'):
            h.Fill(float(line.strip()))

    plotRootHistogram(h, xlabel='(interpolation-MC)/error',
                          title='pull %i D %i MC %i'%(dim, mc, nr),
                          dogaussfit=True)

if __name__ == '__main__':
    print __doc__
    for p in sys.argv[1:]:
        try:
            plotPullData(p)
        except Exception, e:
            print "Problem with '%s':"%(p)
            print e


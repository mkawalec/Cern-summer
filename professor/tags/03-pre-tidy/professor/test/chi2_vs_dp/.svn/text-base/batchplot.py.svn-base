#!/usr/bin/env python2.5
"""batchplot.py

Create chi^2 vs. dp plots for given data files.

usage::
    batchplot.py [OPTIONS] FILES

use --help for more information.
"""

import os.path
import pylab
from optparse import OptionParser
import matplotlib
from professor.test.chi2_vs_dp.displaydata import OneSet, createBigFigure


parser = OptionParser(usage="%prog [options] FILE1 [FILE2 ...]")
parser.add_option('--dpbins', action='store', type="int", help='# of dp bins')
parser.add_option('--chi2bins', action='store', type="int",
                  help='# of chi2 bins')
parser.add_option('--chi2cut', action='store', type="float",
                  help='upper chi2 cut', default=None)
parser.add_option('--logchi2', action='store_true', default=False,
                  help='flag indicating log scaled chi2 is wanted'
                       ' (default: %default)')
parser.add_option('--type', action='store',
                  help='the image type (default: %default)',
                  default='eps')
opts, args = parser.parse_args()


def handleFile(path):
    oset = OneSet(path)
    fig, fname = createBigFigure(oset, opts.dpbins, opts.chi2bins,
                                 opts.chi2cut, opts.logchi2)
    newname = os.path.join(os.path.split(path)[0], fname + '.' + opts.type)
    fig.savefig(newname)
    print "saved", newname

# matplotlib.rc('text', usetex=True)
matplotlib.rc('savefig', dpi=300)
# make the plot big
matplotlib.rc('figure', figsize=(18,17))
# don't require a xserver connection
matplotlib.rcParams['backend'] = 'Agg'
for p in args:
    handleFile(p)

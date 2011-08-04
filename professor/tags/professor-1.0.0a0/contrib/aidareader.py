#! /usr/bin/env python 

import os, sys, re
from professor import *
from optparse import OptionParser


## Parse command line options
parser = OptionParser()
#parser.add_option("-V", "--verbose", action="store_true", dest="VERBOSE",
#                  default=False, help="print status messages")
#parser.add_option("-D", "--debug", action="store_true", dest="DEBUG",
#                  default=False, help="print debug (very verbose) messages")
#parser.add_option("-Q", "--quiet", action="store_true", dest="QUIET",
#                  default=False, help="be very quiet (overrides verbose and debug)")
parser.add_option("--rundir", dest="OUT_DIR",
                  default="", help="directory containing run output files")
parser.add_option("--refdir", dest="REF_DIR",
                  default="", help="directory containing reference files")
(opts, args) = parser.parse_args()


## Normalize the paths
opts.OUT_DIR = os.path.abspath(opts.OUT_DIR)
opts.REF_DIR = os.path.abspath(opts.REF_DIR)
print "Reading MC output from " + opts.OUT_DIR
print "Reading reference data from " + opts.REF_DIR


## Data container
data = histo.TuningData()

## Get the reference histos first
try:
    refhistos = rivetreader.getRefHistos(opts.REF_DIR)
except OSError, ose:
    print "Trouble reading reference data from", refdir
    print "Exiting..."
    sys.exit(1)
else:
    for name, histo in refhistos.iteritems():
        data.setRefHisto(name, histo)

## Run over all the available tunings
try:
    mchistos, mcparams, titles = rivetreader.getMCHistosAndParams(opts.OUT_DIR)
except OSError, ose:
    print "Trouble reading MC data from", opts.OUT_DIR
    print "Exiting..."
    sys.exit(2)
else:
    for run, histos in mchistos.iteritems():
        for name, histo in histos.iteritems():
            data.setMCHisto(name, run, histo)
    for run, params in mcparams.iteritems():
        data.setParams(run, params)


## Print out the ref and MC histos
print data, titles

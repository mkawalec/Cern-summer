#! /usr/bin/env python

import os, sys, re
from professor import *

## TODO:
##  * Provide optparser interface (collision with paida?)


## Directories containing reference and MC histograms
OUT_DIR = "out"
REF_DIR = "../rivet/data"
## Normalize the paths
OUT_DIR = os.path.abspath(OUT_DIR)
REF_DIR = os.path.abspath(REF_DIR)
print "Reading MC output from " + OUT_DIR
print "Reading reference data from " + REF_DIR
print


## Data container
data = histo.TuningData()


## Get the reference histos first
try:
    refhistos = rivetreader.getRefHistos(REF_DIR)
except OSError, ose:
    print "Trouble reading reference data from", refdir
    print "Exiting..."
    sys.exit(1)
else:
    for name, histo in refhistos.iteritems():
        data.setRefHisto(name, histo)


## Run over all the available tunings
try:
    mchistos, mcparams = rivetreader.getMCHistosAndParams(OUT_DIR)
except OSError, ose:
    print "Trouble reading MC data from", OUT_DIR
    print "Exiting..."
    sys.exit(2)
else:
    for run, histos in mchistos.iteritems():
        for name, histo in histos.iteritems():
            data.setMCHisto(name, run, histo) 
    for run, params in mcparams.iteritems():
        data.setParams(run, params)


## Print out the ref and MC histos
print data

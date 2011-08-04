#!/usr/bin/env python

USAGE = \
"""Usage: %prog [options] [--datadir=]<datadir>

Calculate goodness of fit for a run (or set of runs).
Intended to be used with rivetrunner in "scan mode".
"""

import sys, os, numpy, re, traceback

# Professor imports and config
from professor.tools.config import Config
import professor.rivetreader

# from optparse import OptionParser, OptionGroup

conf = Config()
conf.setUsage(USAGE)
conf.initModule("data source",
        {"datadir" : (None, None, True,
                      "specify directory containing mc and ref directories")
        ,"mcdir" : (None, None, True,
                    "specify directory containing MC runs")
        ,"refdir" : (None, None, True,
                    "specify directory containing reference runs")
        ,"obsfile" : (None, None, True,
                    "specify file with observable names (and optional weights)")
        ,"outdir" : (None, None, True,
                    "specify directory in which to write out chi2 data files")
        })
conf.initModule("goodness of fit",
        {"use referror" : (False, conf.convBool, "use-referror",
                           "use the reference data error in computing the chi2")
        })
logger = conf.initModule("scanchi2",
        {"verbose" : (False, conf.convBool, True,
                      "print extra status messages")
        ,"debug" : (False, conf.convBool, True,
                    "print debugging messages")
        })

(opts, args) = conf.parseCommandline()

OUTDIR = conf.getOption('data source', 'outdir')
DATADIR = conf.getOption('data source', 'datadir')
REFDIR = conf.getOption('data source', 'refdir')
MCDIR = conf.getOption('data source', 'mcdir')

OBSFILE = conf.getOption('data source', 'obsfile')

USE_REFERROR = conf.getOption('goodness of fit', 'use referror')

VERBOSE = conf.getOption('scanchi2', 'verbose')
DEBUG = conf.getOption('scanchi2', 'debug')

## Check/make output directory
if not os.access(OUTDIR, os.R_OK):
    if VERBOSE:
        print "Making output directory:", OUTDIR
    os.makedirs(os.path.abspath(OUTDIR))
if not os.access(OUTDIR, os.W_OK):
    sys.stderr.write("Can't write to output directory \n" % OUTDIR)
    sys.stderr.write("Exiting...\n")
    sys.exit(1)


## Specify data directories and get data
try:
    if DATADIR is None and len(args) == 1:
        DATADIR = args[0]
    if REFDIR is None:
        REFDIR = os.path.join(DATADIR, "ref")
    if MCDIR is None:
        MCDIR = os.path.join(DATADIR, "mc")
    data = professor.rivetreader.getTuningData(REFDIR, MCDIR)
except Exception, e:
    sys.stderr.write("Problem reading files: did you specify the data directory?\n")
    sys.stderr.write("Exiting...\n")
    if DEBUG:
        traceback.print_exc()
    sys.exit(1)


## Check data
try:
    data.isValid()
except:
    sys.stderr.write("Invalid data... exiting\n")
    sys.exit(1)


## Select the observables we want to use, from file if possible
if OBSFILE is not None and not os.access(OBSFILE, os.R_OK):
    sys.stderr.write("Can't read observable file %s" % OBSFILE)
    OBSFILE = None

## Set observables and weights (from file if supplied)
weights = { }
if OBSFILE is not None:
    obsfile = open(OBSFILE, "r")
    for line in obsfile:
        line = re.sub(r' +', r' ', line) # collapse spaces
        line = re.sub(r'\n', r'', line) # remove newline
        if len(line) == 0 or line == " ":
            continue
        tokens = line.split(" ")
        if len(tokens) in (1,2):
            obsname = str(tokens[0])
            obsweight = 1.0
            ## If the config file specifies the weight, use it
            if len(tokens) == 2:
                obsweight = float(tokens[1])
            weights[obsname] = obsweight
        else:
            sys.stderr.write("Parameter def %s is invalid\n" % str(tokens))
    obsfile.close()
else:
    print "Using all observables in first MC run, with all weights == 1"
    for obs in data.getMCHistoNames():
        weights[obs] = 1.0

if VERBOSE:
    print "Observables and weights:"
    for o, w in weights.iteritems():
        print o, ":", w

## For each run, get chi2/Ndof and params.
def calcChi2PerDoF(data, weights):
    Nweightedbins = 0
    ## Calculate GoF numerators first
    sqdevs = dict([(run, 0) for run in data.getRunNums()])
    Nbins = dict([(run, 0) for run in data.getRunNums()])
    for name, weight in sorted(weights.iteritems()):
        ## TODO: normalize per-observable (i.e. ignore bin number)?
        refhisto = data.getRefHisto(name)
        for run in data.getRunNums():
            mchisto = data.getMCHisto(name, run)
            for b in range(mchisto.numBins()):
                refbin = refhisto.getBin(b)
                mcbin = mchisto.getBin(b)
                if mcbin.getYErr() != 0:
                    binDevSq = (mcbin.getYVal() - refbin.getYVal())**2
                    errorSq = mcbin.getYErr()**2
                    if USE_REFERROR:
                        errorSq += refbin.getYErr()**2
                    binDevOverErrSq = binDevSq / errorSq
                    sqdevs[run] += weight * binDevOverErrSq
                    Nbins[run] += weight
                elif VERBOSE:
                    print "Zero MC error on run %s, obs %s, bin %d" % (run, name, b)
    ## Work out the number of DoF for the denominator
    Nparams = data.numberOfParams()
    Ndofs, gofs = dict(), dict()
    for run in sorted(data.getRunNums()):
        Ndofs[run] = Nbins[run] - Nparams
        gofs[run] = sqdevs[run]/Ndofs[run]
    return Ndofs, gofs

## Calculate chi2
Ndofs, gofs = calcChi2PerDoF(data, weights)

## Write out data file of chi2 vs. scan number/param
datafile = open(os.path.join(OUTDIR, "scan-chi2.dat"), "w")
if VERBOSE:
    print "\nChi2 data on scan line"
for run, gof in sorted(gofs.iteritems()):
    if VERBOSE:
        print "Run %s: chi2/Ndof=%2.3f, Ndof=%2.1f" % (int(run), gof, Ndofs[run])
    datafile.write("%s %f\n" % (int(run), gof))
datafile.close()

def strToFilename(string):
    for char in ["(", ")"]:
        string = string.replace(char, "")
    return string

## For each param, get overall param range and plot chi2
for pname in data.paramsNames():
    datafilename = "scan-chi2-%s.dat" % strToFilename(pname)
    pdatafile = open(os.path.join(OUTDIR, datafilename), "w")
    if VERBOSE:
        print "\nChi2/Ndof data for param", pname
    for run, gof in sorted(gofs.iteritems()):
        pvalue = data.getParam(run, pname)
        if VERBOSE:
            print "Run %s: %s=%f, chi2/Ndof=%2.3f, Ndof=%2.1f" % (int(run), pname, pvalue, gof, Ndofs[run])
        pdatafile.write("%f %f\n" % (pvalue, gof))
    pdatafile.close()

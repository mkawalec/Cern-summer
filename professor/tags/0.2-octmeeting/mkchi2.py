#! /usr/bin/env python

from professor import *

## TODO:
##  * Provide optparser interface (collision with paida?)

## Directories containing reference and MC histograms
OUT_DIR = "../paramscan" #"../testdata/out"
REF_DIR = "../testref"

## Get the data
data = rivetreader.getTuningData(REF_DIR, OUT_DIR)

## Get all the chi2 values for every plot in every run
chi2s = {}
for hname in data.getMCHistoNames():
    ref = data.getRefHisto(hname)
    chi2s[hname] = {}
    safehname = hname.replace("/", "_")
    if safehname[0] == "_":
        safehname = safehname[1:]
    f = file(safehname+".dat", "w")
    for run, hist in data.getMCHistos(hname).iteritems():
        params = data.getParams(run)
        chi2s[hname][run] = 0
        bins = hist.getBins()
        for bin in range(len(bins)):
            if ref[bin].getYErr() != 0:
                binChi2 = (hist[bin].getYVal()-ref[bin].getYVal())**2/ref[bin].getYErr()
                chi2s[hname][run] += binChi2
        ## Build the output line
        line = str()
        for val in params.values():
            line += str(val) + " "
        line += str(chi2s[hname][run])
        print "%s: %s" % (hname, line)
        f.write(line + "\n")
    f.close()
    #break

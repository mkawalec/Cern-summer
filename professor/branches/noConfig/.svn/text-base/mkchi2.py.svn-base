#! /usr/bin/env python 

## TODO
## * Profile

from professor import *
import os.path, os, sys
import pylab as lab
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-V", "--verbose", action="store_true", dest="VERBOSE", 
                  default=False, help="print extra status messages")
(opts, args) = parser.parse_args()

## Directories containing reference and MC histograms
if len(args) == 0:
    print "You must supply the scan directory as a parameter"
    sys.exit(1)
DATA_DIR = os.path.abspath(args[0])
REF_DIR = os.path.join(DATA_DIR, "ref")
MC_DIR = os.path.join(DATA_DIR, "mc")
if not os.access(DATA_DIR, os.R_OK) or \
        not os.access(REF_DIR, os.R_OK) or \
        not os.access(MC_DIR, os.R_OK):
    print DATA_DIR, "is not a valid data directory"
    sys.exit(2)
OUT_DIR = os.path.join(DATA_DIR, "plotdata")
if not os.access(OUT_DIR, os.R_OK):
    os.mkdir(OUT_DIR)

## Get the data
data = rivetreader.getTuningData(REF_DIR, MC_DIR)

## Get all the chi2 values for every plot in every run
chi2s = {}
hnames = data.getMCHistoNames()
hnames.sort()
for hname in hnames:
    print hname
    #if hname.find("ds34") == -1: continue
    ref = data.getRefHisto(hname)
    chi2s[hname] = {}
    safehname = hname.replace("/", "_")
    if safehname[0] == "_":
        safehname = safehname[1:]
    f = file(os.path.join(OUT_DIR, safehname + ".dat"), "w")
    mchistos = data.getMCHistos(hname)
    runs = mchistos.keys()
    runs.sort()
    for run in runs:
        hist = mchistos[run]
        params = data.getParams(run)
        chi2s[hname][run] = 0
        lab.cla()
        bins = hist.getBins()
        histxs, histys, histxerrs, histyerrs = [], [], [], []
        refedges, refxs, refys, refyerrs = [0], [], [], []
        valid = False
        for bin in range(len(bins)):
            ## MC data
            histxrange = hist[bin].getXRange()
            histxval = (histxrange[1] + histxrange[0])/2.0
            histxerr = (histxrange[1] - histxrange[0])/2.0
            histxs.append(histxval)
            histxerrs.append(histxerr)
            histys.append(hist[bin].getYVal())
            histyerrs.append(hist[bin].getYErr())
            ## Ref data
            refxrange = ref[bin].getXRange()
            refxval = (refxrange[1] + refxrange[0])/2.0
            refxerr = (refxrange[1] - refxrange[0])/2.0
            refedges.append(refxrange[0])
            refedges.append(refxrange[1])
            refxs.append(refxval)
            refys.append(ref[bin].getYVal())
            refyerrs.append(ref[bin].getYErr())
            ## Calc chi2
            if ref[bin].getYErr() != 0:
                binChi2 = (hist[bin].getYVal()-ref[bin].getYVal())**2/ref[bin].getYErr()
                chi2s[hname][run] += binChi2

        ## Make plot
        lab.title(hist.title)
        ## Ref histo
        refedges.append(0)
        refedges[0] = refedges[1]
        refedges[-1] = refedges[-2]
        refdblys = [0]
        for y in refys:
            refdblys.append(y)
            refdblys.append(y)
        refdblys.append(0)
        lab.errorbar(refxs, refys, yerr=refyerrs, fmt=None, ecolor='red', capsize=1)
        lab.plot(refedges, refdblys, "r-")
        ## MC data points
        lab.errorbar(histxs, histys, xerr=histxerrs, fmt=None, ecolor='black', capsize=1)
        lab.errorbar(histxs, histys, yerr=histyerrs, fmt=None, ecolor='black', capsize=1)
        lab.plot(histxs, histys, "ko", ms=4)
        ## Write out
        figfile = os.path.join(OUT_DIR, safehname + "-" + str(run) + ".eps")
        print "Writing figure " + figfile
        lab.savefig(figfile)

        ## Build the output chi2 line
        line = " ".join(map(str, params.values()))
        line += " " + str(chi2s[hname][run])
        if opts.VERBOSE:
            print "%s: %s" % (hname, line)
        f.write(line + "\n")
        
    f.close()

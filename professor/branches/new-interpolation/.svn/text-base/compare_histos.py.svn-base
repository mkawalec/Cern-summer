#! /usr/bin/env python

import os, sys, re
from professor.rivetreader import *

## Parse command line options
from optparse import OptionParser
parser = OptionParser(usage="Usage: %prog [options] reffile mcfile1 [mcfile2 ...]")
#parser.add_option("-r", "--reffile", dest="REFFILE",
#                  default="data/ref/DELPHI_1996_S3430090.aida", help="reference AIDA data file")
#parser.add_option("-m", "--mcfile", dest="MCFILE",
#                  default="data/mc/000/out.aida", help="MC-simulated AIDA data file")
parser.add_option("-o", "--outdir", dest="OUTDIR",
                  default=".", help="write data files into this directory")
parser.add_option("-l", "--histogram-list", dest="HISTOGRAMLIST",
                  default=None, help="this file contains a list of histograms to plot")
(opts, args) = parser.parse_args()

def getHistos(aidafile):
    '''Get a dictionary of histograms indexed by name.'''

    ## Initialize the return values
    histos = {}
    titles = {}

    filename = os.path.split(aidafile)[1]
    refname = re.sub(r'(.*)\.aida$', r'\1', filename)
    if not re.match(r'.*\.aida$', aidafile):
        print 'Error: Input file is not an AIDA file'
        sys.exit(2)

    aidafilepath = os.path.abspath(aidafile)
    if not os.path.isfile(aidafilepath):
        print 'Error: Cannot use the file', aidafile
        sys.exit(2)

    tree = ET.parse(aidafilepath)
    for dps in tree.findall("dataPointSet"):
        ## Get the histogram's title
        title = dps.get("title")
        ## Get this histogram's path name, stripped of the "/HepData" prefix
        dpsname = os.path.join(dps.get("path"), dps.get("name"))
        if dpsname[:8] == "/HepData":
            dpsname = dpsname[8:]

        ## Make a histogram and add it to the return dictionary
        histos[dpsname] = mkHistoFromDPS(dps)
        titles[dpsname] = title

    ## Return collection of histos
    return histos, titles


STYLES=[('black', 'solid'),
        ('red',   'solid'),
        ('blue',  'solid'),
        ('green', 'solid'),
        ('red',   'dashed'),
        ('blue',  'dashed'),
        ('green', 'dashed'),
        ('red',   'dotted'),
        ('blue',  'dotted'),
        ('green', 'dotted'),
       ]

FILES = args
if (len(FILES) < 2):
    print parser.get_usage()
    sys.exit(2)

HISTOS = {}
TITLES = {}

for file in FILES:
    HISTOS[file], TITLES[file] = getHistos(file)

if opts.HISTOGRAMLIST is not None:
    NAMES = []
    try:
        f = open(opts.HISTOGRAMLIST, 'r')
    except:
        print 'Cannot open file %s' %(opts.HISTOGRAMLIST)
        sys.exit(2)
    for line in f:
        if line.startswith("#"): continue
        if HISTOS[FILES[0]].has_key(line.strip()):
            NAMES.append(line.strip())
    f.close()
else:
    NAMES = HISTOS[FILES[0]].keys()

def sanitiseString(s):
    return s.replace('_','\\_').replace('^','\\^{}').replace('$','\\$').replace('#','\\#').replace('%','\\%')

for name in sorted(NAMES):
    outfilename = '%s.dat' % (name.split('/')[-1])
    outfilepath = os.path.join(opts.OUTDIR, outfilename)
    if not os.access(opts.OUTDIR, os.R_OK):
        try:
            os.mkdir(opts.OUTDIR)
        except:
            sys.stderr.write("Can't make directory %s" % opts.OUTDIR) 
            sys.exit(2)
    if not os.access(opts.OUTDIR, os.W_OK):
        sys.stderr.write("Can't write to directory %s" % opts.OUTDIR)
        sys.exit(2)
    f = open(outfilepath, 'w')

    ## Write plot header
    f.write('# BEGIN PLOT\n')
    try:
        title = TITLES[FILES[1]][name]
    except:
        title = name
    else:
        f.write('Title=%s\n' % sanitiseString(title) )
    f.write('Legend=1\n')
    f.write('LogY=1\n')
    drawonly=''
    for i in FILES:
        drawonly += '%s ' % i
    f.write('DrawOnly=%s\n' % drawonly)
    f.write('RatioPlot=1\n')
    f.write('RatioPlotReference=%s\n' % FILES[0])
    f.write('RatioPlotYMin=0.5\n')
    f.write('RatioPlotYMax=1.5\n')
    f.write('RatioPlotYLabel=MC/data\n')
    f.write('# END PLOT\n\n')

    ## Write reference histo
    f.write('# BEGIN HISTOGRAM %s\n' % FILES[0])
    f.write('ErrorBars=1\n')
    f.write('PolyMarker=*\n')
    f.write('Title=Delphi\n')
    for bin in HISTOS[FILES[0]][name].getBins():
        xmin, xmax = bin.getXRange()
        f.write('%f\t%f\t%f\t%f\n' % (xmin, xmax, bin.getYVal(), bin.getYErr(),))
    f.write('# END HISTOGRAM\n\n')

    ## Write MC histos
    filecount=1
    for file in FILES[1:]:
        color, style = STYLES[filecount]
        if HISTOS[file].has_key(name):
            f.write('# BEGIN HISTOGRAM %s\n' % file)
            f.write('LineColor=%s\n' % color)
            f.write('LineStyle=%s\n' % style)
            f.write('Title=Pythia\n')
            for bin in HISTOS[file][name].getBins():
                xmin, xmax = bin.getXRange()
                f.write('%f\t%f\t%f\t%f\n' % (xmin, xmax, bin.getYVal(), bin.getYErr(),))
            f.write('# END HISTOGRAM\n\n')
        filecount += 1

    f.close()

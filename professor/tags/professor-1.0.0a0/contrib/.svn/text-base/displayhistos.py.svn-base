#!/usr/bin/env python2.5
"""displayhistos.py

Display interactively histograms.

usage::
    displayhistos.py --file OUT.aida
 or displayhistos.py --mcdir MCDIR  --refdir REFDIR

after that use the IPython shell:

>>> ls()
>>> plothisto('/Test/FOO')
"""

# import from possibly buggy to non-buggy

from professor.rivetreader import ET, mkHistoFromDPS, getTuningData
from professor.tools.config import Config

from IPython.Shell import IPShellEmbed
ipshell = IPShellEmbed([])

import numpy, pylab

import sys
from optparse import OptionParser

logger = Config().getLogger()

# helper functions
def _readaidafile(path):
    histos = {}
    tree = ET.parse(path)
    for dps in tree.findall("dataPointSet"):
        ## Get this histogram's path name, stripped of the "/HepData" prefix
        dpsname = dps.get("path") + "/" + dps.get("name")
        if dpsname[:8] == "/HepData":
            dpsname = dpsname[8:]

        ## Make a histogram and add it to the return dictionary
        histos[dpsname] = mkHistoFromDPS(dps)
    return histos

def _plothisto(histo, name='unkown', log=False,
        start=None, stop=None):
    """Takes a Histo instance and plots it."""
    bins = [b for b in histo[start:stop]]

    xlows = -1. * numpy.ones(len(bins))
    widths = 1. * xlows[:]
    yvals = 1.* xlows[:]
    yerrs = 1. * xlows[:]
    for i, bin in enumerate(bins):
        xl, xh = bin.getXRange()
        xlows[i] = xl
        widths[i] = xh - xl
        yvals[i] = bin.getYVal()
        yerrs[i] = bin.getYErr()
    pylab.figure()
    pylab.title('histogram %s'%(name))
    pylab.xlabel('a.u.')
    pylab.ylabel('#')
    pylab.bar(xlows, yvals, widths, yerr=yerrs,
            color='b', ecolor='r', log=log)
    # pylab.show()
    pylab.draw()

_plothisto.kwarg_doc = """Accepted kwargs (default values):
  log : True|False  flag indicating if y-axis is logarithmic.
        (False)
  start : Slice index of the first bin, that should be plotted.
          (None meaning no restriction)
  stop : Slice index of the last bin, that should be plotted.
         (None meaning no restriction)"""


# parse opts
parser = OptionParser()
parser.add_option('-f', '--file', action='store', help='path to the xml file')
parser.add_option('-m', '--mcdir', action='store')
parser.add_option('-r', '--refdir', action='store')
opts, args = parser.parse_args()

# build interactive environment
if opts.file is not None and opts.mcdir is None and opts.refdir is None:
    histos = _readaidafile(opts.file)

    def h():
        print 'available commands:'
        print 'h()   print this help'
        print 'ls()  list available histograms'
        print 'plothisto(NAME, [**kwargs])  plot histogram NAME in new window'
        for l in _plothisto.kwarg_doc.split('\n'):
            print ' '*4 + l
        print
        print 'exit() or Ctrl-D to exit.'

    def ls():
        print ('available histograms: ' +
                ' '.join(sorted(histos.keys())))

    def plothisto(name, **kwargs):
        print 'plotting histogram "%s"'%(name)
        return _plothisto(histos[name], name, **kwargs)

    # EIKE: this `pass' is here because my vim's code folding breaks here
    pass


elif opts.mcdir is not None and opts.refdir is not None:
    td = getTuningData(opts.refdir, opts.mcdir)
    def h():
        print 'available commands:'
        print 'h()  this help'
        print 'ls()  list available histograms and runs'
        print 'plothisto(NAME, RUN|"ref", [**kwargs])  plot histogram NAME'
        print '    of MC run RUN or reference histogram in new window'
        for l in _plothisto.kwarg_doc.split('\n'):
            print ' '*4 + l
        print
        print 'exit() or Ctrl-D to exit.'

    def ls():
        print ('available histograms: ' +
               ' '.join(sorted(td.getMCHistoNames())))
        print ('available MC runs: ' +
               ' '.join(sorted(td.getRunNums())))

    def plothisto(name, runnum, **kwargs):
        print 'plotting histogram "%s" from run "%s"'%(name, runnum)
        if runnum.lower() == 'ref':
            return _plothisto(td.getRefHisto(name), "%s reference run"%(name),
                    **kwargs)
        else:
            return _plothisto(td.getMCHistos(name)[runnum],
                    "%s MC run %s"%(name, runnum), **kwargs)

    # EIKE: this `pass' is here because my vim's code folding breaks here
    pass

else:
    logger.error("Bad combination of options: %s!"%(opts))
    logger.error(__doc__)
    sys.exit(1)

h()
pylab.ion()
ipshell()

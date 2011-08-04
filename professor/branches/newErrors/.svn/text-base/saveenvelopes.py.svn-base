#!/usr/bin/env python2.5
"""savenevelopes.py

Produce Envelope Plots

usage::
    saveenvelopes.py --mcdir MCDIR  --refdir REFDIR --outdir OUTDIR --observable OBSERVABLE
    or
    saveenvelopes.py --mcdir MCDIR  --refdir REFDIR --outdir OUTDIR --observable all
    or, if you are happy with the default settings
    saveenvelopes.py

"""

from professor.rivetreader import ET, mkHistoFromDPS, getTuningData
from professor.tools.config import Config
from professor.tools.progressbar import ForLoopProgressBar as flpb
from professor.controlplots import envelope as env
from professor.histo import Bin

import numpy, pylab
import sys, os
from optparse import OptionParser

from professor.tools import translate

params = {
        'axes.labelsize': 10,
        'axes.titlesize': 9,
        'text.fontsize': 8,
        'legend.fontsize': 7,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'text.usetex': True,
        'math.usetex': True,
        'text.latex.preamble' : ['\usepackage{amsmath}'],
        }
pylab.rcParams.update(params)

logger = Config().getLogger()

parser = OptionParser()
parser.add_option('-b', '--bruteforce', action='store',
        help="overwrite files", default='0')
parser.add_option('-f', '--filetype', action='store',
        help="filetype for output images", default='png')
parser.add_option('-g', '--gallery', action='store',
        help="whether or whether not create html-gallery", default='no')
parser.add_option('-m', '--mcdir', action='store', default='mc',
        help="specify the subdirectory, where the MC-Histos can be found")
parser.add_option('-o', '--outdir', action='store', default='envelopes',
        help="specify the subdirectory, where plots are to be saved")
parser.add_option('-O', '--observable', action='store',
        help="file with observables to plot, 'all' plots all observables", default='all')
parser.add_option('-r', '--refdir', action='store', default='ref',
        help="specify the subdirectory, where the REF-Histos can be found")
parser.add_option('-t', '--usetex', action='store', default='no',
        help="whether or whether not to use LATEX")
parser.add_option('-v', '--validate', action='store', default='no',
        help="validate TuningData object after its construction")
parser.add_option('-l', '--logy', action='store', default='no',
        help="produce semilogy plots")
opts, args = parser.parse_args()

if opts.usetex == 'yes':
    pylab.matplotlib.rc('text', usetex=True) # causes problems on some machines

logy = opts.logy

def getAvailableObservables(td):
    temp = td.getMCHistoNames()
    temp.sort()
    return temp

def plotTheseObservables(td):
    obslist = []
    if opts.observable == 'all':
        obslist = getAvailableObservables(td)
    else:
        f = open(opts.observable)
        for line in f:
            if (line.strip()).startswith('#'):
                continue
            if not line.strip() == "":
                obslist.append((line.split()[0]).strip())
        f.close()
    return obslist

def plotRefData(sp, envelope):
    """ this plots the reference data
    """
    temp = numpy.array([(bin.getXRange()[0] + .5*(
        bin.getXRange()[1] -bin.getXRange()[0]), bin.getYVal(), bin.getYErr())
        for bin in envelope._td.getRefHisto(envelope._obs).getBins()])
    if opts.usetex == 'yes':
        sp.errorbar(temp[:,0], temp[:,1], temp[:,2], ls=' ', fmt='kx', label='\\scriptsize Reference Data')
    else:
        sp.errorbar(temp[:,0], temp[:,1], temp[:,2], ls=' ', fmt='kx', label='Reference Data')

def plotEnvelope(sp, envelope):
    """ plot several patch objects """
    # the value enclosing patches
    vpatches    = [numpy.array(envelope.getPatch(i[0],i[1], logy=logy)[0])
            for i in envelope._allxranges
            if not envelope.getPatch(i[0],i[1])[0] is None]
    # the upper error enclosing patches                                                                                                        
    uvpepatches = [numpy.array(envelope.getPatch(i[0],i[1], logy=logy)[1])
            for i in envelope._allxranges
            if not envelope.getPatch(i[0],i[1])[1] is None]
    # the lower error enclosing patches                                                                                                        
    lvpepatches = [numpy.array(envelope.getPatch(i[0],i[1], logy=logy)[2])
            for i in envelope._allxranges
            if not envelope.getPatch(i[0],i[1])[2] is None]

    for patchtuple in vpatches[:-1]:
        myFill(sp, patchtuple,'b', alpha = .3)
    myFill(sp, vpatches[-1],'b', alpha = .3, label='Value Envelope')
    # the line above is a workaround to get only one entry in the legend

    for patchtuple in uvpepatches[:-1]:
        myFill(sp, patchtuple,'k', alpha = .1)
    myFill(sp, uvpepatches[-1],'k', alpha = .1, label='Error Envelope')
    # the line above is a workaround to get only one entry in the legend

    for patchtuple in lvpepatches:
        myFill(sp, patchtuple,'k', alpha = .1)

def plotBest(sp, td, obs):
    bestrun = getBest(td, obs)
    if not bestrun is None:
        bins = td.getMCHistos(obs)[bestrun].getBins()
        x = map(Bin.getBinCenter, bins)
        y = map(Bin.getYVal, bins)
        if not logy=='no':
            sp.semilogy(x,y, ls=':', label='Best Run: %s'%bestrun)
        else:
            sp.plot(x,y, ls=':', label='Best Run: %s'%bestrun)

def myFill(sp, ptuple , color='r', alpha = .3, label=None):
    """ nasty workaround """
    try:
        ptuple[:,0]
        sp.fill(ptuple[:,0], ptuple[:,1], color, alpha=alpha, label=label)
    except IndexError:
        pass

def getBest(td, obs):
    """ return the runkey of the run that is closest to the ref-data """
    mchistos = td.getMCHistos(obs)
    refbins = td.getRefHisto(obs).getBins()
    allchi2s = {}
    for runnr, mchisto in mchistos.iteritems():
        mcbins = mchisto.getBins()
        chi2 = sum([(mcbins[i].getYVal() - refbins[i].getYVal())**2 for i in xrange(len(mcbins))])
        allchi2s[runnr] = chi2
    for k,v in allchi2s.iteritems():
        if v == min(allchi2s.values()):
            return k

def doPlot(sp, envelope, plotwhat=(True, True, False)):
    """ this will draw everything """
    if plotwhat[0]:
        plotEnvelope(sp, envelope)
    if plotwhat[1]:
        plotRefData(sp, envelope)

def makeItFancy(envelope, obs):
    """ show everything that was plotted before, create title, labels and
        legends
    """
    a, b = envelope.getTotalXRange()[0][0], envelope.getTotalXRange()[1][1]
    pylab.xlim(a - .1*(b-a), b + .1*(b-a))
    if logy=='no':
        pylab.ylim(0)
    ## create title
    if opts.usetex == 'yes':
        title = '\\Large \\bf{%s}\\quad\\small{\\tt{(%s)}}'%(
                envelope._td.getTitle(obs).replace('_', '\\_').replace(
                    '^', '\\^'), obs.replace('_', '\\_') )
        #title = '%s'%(envelope._td.getTitle(obs).replace('_', '\\_').replace(
                    #'^', '\\^'))
    else:
        title = envelope._td.getTitle(obs)#.replace('^', '\\^')

    params = 'params varied:'
    for i in envelope._params:
        #if opts.usetex == 'yes':
            ##params += '\\quad \\Large{%s} \\normalsize{\\tt{(%s)}} '%(
                    ##translate.translate(i), i)
            #params += '\\small{%s} '%(i)
        #else:
        params += ' ' + i
    ## display title
    pylab.figtext(.5,.96, title,ha='center')
    pylab.figtext(.5,.92, params,ha='center')
    pylab.xlabel('Observable')
    pylab.figtext(.05,.5,'Entries', ha='center',va='center', rotation='vertical')
    pylab.legend(loc='upper left')
    pylab.grid(True)

# create TuningData-object
if opts.mcdir is not None and opts.refdir is not None:
    logger.info("building TuningData object...")
    td = getTuningData(opts.refdir, opts.mcdir)
    logger.info("...done!")
else:
    logger.error("no mcdir and/or refdir specified, aborting...")
    logger.error(__doc__)
    sys.exit(1)

# validate TuningData object
if opts.validate == 'yes':
    td.isValid()
else:
    logger.warning("skipping validation of TuningData object"
            " - use -v yes on the commandline to validate")

# selection of observables to plot
if opts.observable is not None and os.path.exists(opts.observable):
    logger.info("creating envelopes for observables found in %s"%opts.observable)
elif opts.observable is not None and opts.observable == 'all':
    logger.info("saving envelope-plots for all available observables")
else:
    logger.error("specified observable doesn't exist or none specified")
    print 'list of available observables:'
    for i in getAvailableObservables(td):
        print i
    logger.error(__doc__)
    sys.exit(1)


# check, if specified outdir exists and create it otherwise
if not os.path.exists(opts.outdir):
    os.system('mkdir -p %s'%opts.outdir)
elif os.path.exists(opts.outdir) and opts.bruteforce is '1':
    pass
else:
    logger.error("outdir already exists! Use '-b 1' to overwrite")
    sys.exit(1)


# save envelope-plots in the directory specified via --outdir
obslist = plotTheseObservables(td)
bar = flpb(0, len(obslist), 30, 'saving envelopes ')
for num, i in enumerate(obslist):
    bar.update(num)
    # create plot-window
    fig = pylab.figure(facecolor='w')
    sp = fig.add_subplot(1, 1, 1)
    envelope = env.Envelope(td, observable=i)
    doPlot(sp, envelope)
    plotBest(sp, td, i)
    makeItFancy(envelope, i)
    try:
        pylab.savefig(opts.outdir +'/'+ i.replace('/','_') + '.' + opts.filetype, format=opts.filetype)
    except ValueError:
        logger.error("\nCould not save envelope for %s.\r"%i)
logger.info("done!")
print "You may now want to create an html-gallery using 'makegallery.py' as such:\n"
print "         professor/tools/makegallery.py -s %s %s envelopes.html\n"%(opts.outdir, opts.filetype)

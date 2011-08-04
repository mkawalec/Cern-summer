#!/usr/bin/env python2.5
"""savenevelopes.py

Produce Sensitivity Plots as such:
          ___________________________________
         |                 |                 |
PARAM 1  |    colormap     |    2D-plot      |
         |___________________________________|
         |                 |                 |
PARAM 2  |    colormap     |    2D-plot      |
    .    |_________________|_________________|
    .     	  .		    .
    .     	  .		    .
    . 	          .		    .
    .             .                 .

usage::
    if you are happy with the default settings:
    saveenvelopes.py
    or, to specify an output directory:
    savesensitivities.py --outdir OUTDIR
    or, to specifiy the mc and ref directories:
    savesensitivities.py --mcdir MCDIR  --refdir REFDIR --outdir OUTDIR

"""
from professor.rivetreader import getConfiguredData, readObservableFile
from professor.tools.config import Config
from professor.controlplots import sensitivity as sens
from professor.tools.progressbar import ForLoopProgressBar as flpb

try:
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed([])
except:
    print "Ipython shell not available."

try:
    import psyco
    psyco.log()
    psyco.profile(0.2)
except:
    print "Psyco not available."


import numpy, pylab, matplotlib
import sys, os
from optparse import OptionParser

params = {
        'backend':'pdf',
        'axes.labelsize': 10,
        'text.fontsize': 10,
        'legend.fontsize': 10,
        'axes.titlesize': 10,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'text.usetex': True,
        'text.latex.preamble' :  ['\usepackage{amsmath}'],
        'figure.dpi': 300,
        'lines.markersize':7.5,
        'figure.subplot.left' : 0.07,
        'figure.subplot.right' : 0.98,
        'figure.subplot.bottom' : 0.07,
        'figure.subplot.top' : 0.95,
        'figure.subplot.wspace' : 0.4,
        'lines.markersize':5
        }

pylab.rcParams.update(params)

from professor.tools import translate, histotools as hito

conf = Config()

logger = conf.initModule("save sensitivities",
        {"bruteforce" : (False, conf.convBool, True,
                         "Overwrite files.")
        ,"center" : (.5, None, True,
                     "Set the interpolation center as float.")
        ,"mode" : ("ref", None, True,
                   "Calculate sensitivities w.r.t. mc or ref histos: ref|mc .")
        ,"errorlevel" : (30., None, True,
                         "Maximum error a bin may have to be recognized.")
        ,"filetype" : ("png", None, True,
                       "Filetype for output images, e.g. eps or png.")
        ,"method" : ("centered", None, True,
                     "Use centered or projected sensitivities:"
                     " centered|projected")
        ,"outdir" : ("sens", None, True,
                     "The subdirectory where the plots are saved.")
        ,"observables" : ("all", None, True,
                         "Select the observable to plot. Use 'all' to plot"
                         " all observables")
        ,"params" : ("all", None, True,
                         "Select the parameters to plot. Use 'all' to plot"
                         " all available params")
        })
conf.setUsage(__doc__)
conf.parseCommandline()

def getAvailableObservables(td):
    temp = td.getMCHistoNames()
    temp.sort()
    return temp

def plotTheseObservables(td):
    """ evaluate some input and find out whether to plot all or a certain
        observable(s)
    """
    observables = conf.getOption("save sensitivities", "observables")
    if observables == 'all':
        obslist = getAvailableObservables(td)
        logger.info("producing sensitivity-plots for all available observables")
    elif os.path.exists(observables):
        obslist = [obs for obs in readObservableFile(observables).keys(
            ) if obs in td.getMCHistoNames()]
        logger.info("producing plots for observables found in %s"%observables)
    else:
        logger.error("no observables specified")
        sys.exit(1)
    #else:
        #try:
            #int(observable)
        #except ValueError:
            #if observable in td.getMCHistoNames():
                #obslist.append(observable)
                #obsname=observable
        #if int(observable) <= len(getAvailableObservables(td)):
            #obslist.append(getAvailableObservables(td)[int(observable)])
            #obsname=getAvailableObservables(td)[int(observable)]
        #logger.info("only producing sensitivity-plot for observable %s"%obsname)
    return obslist


def createShortFilename(method, use_obs):
    fname = use_obs + '_' + method
    return fname.replace('/','_')

def createOverviewPlot(fig, Svity, use_obs, intcenter, method, errorlimit, mode,
        cmap=matplotlib.cm.RdBu, nrofparbins = 'same', cscale='single'):
    #TODO: docstring
    """ docstring
    """
    methods = {'centered':('interpolation center','dummy'), 'projected':(True, False)}

    x=hito.getPlotRange(td, use_obs, for_cmap=True)

    nrows = len(paramstoplot)
    ncols = len(methods[method])

    # handles arrangement of subplots
    allsens = []
    allbadbins = []

    for j, param in enumerate(paramstoplot):
        sens, badbins = Svity.getSens(Svity._runs, use_obs, param)
        allsens.append(sens)
        allbadbins.append(badbins)
    vmin_g, vmax_g = Svity.getGlobalVminVmax(allsens)

    for j, param in enumerate(sorted(paramstoplot)):
        y = Svity.getYBins(use_obs, nrofparbins=nrofparbins, unscaled=True, paramindex=j)
        X, Y = numpy.meshgrid(x, y)
        Z=numpy.array(allsens[j])
        Svity._badbins = allbadbins[j]
        ## Colormap, left hand plot
        sp_1 = fig.add_subplot(nrows, ncols, ncols*j + 1)
        coll = sp_1.pcolormesh(X, Y, Z.transpose(), cmap=cmap, vmin=vmin_g, vmax=vmax_g)
        pylab.xlim((x[0], x[-1]))
        cbar = fig.colorbar(coll)
        ## Averaged Sensitivitiy (1D), right hand plot
        sp_2 = fig.add_subplot(nrows, ncols, ncols*j + 2)
        pylab.axhline(y=0, color='k', ls='--' )
        A = Svity.getSensAvg_wrt_p(allsens[j])
        avg_x = hito.getPlotRange(td, use_obs, for_cmap=False)
        for i, V in enumerate(A):
            if i in badbins:
                pylab.errorbar(avg_x[i], V[0], V[1], fmt='rx')
            else:
                pylab.errorbar(avg_x[i], V[0], V[1], fmt='kx')
        pylab.xlim((x[0], x[-1]))

        ## subplot labels
        if j == nrows -1: # have xlabels only once in a column 
            name = Svity._td.getTitle(use_obs)
            if "$" in name:
                sp_1.set_xlabel("%s"%name)
                sp_2.set_xlabel("%s"%name)
            else:
                sp_1.set_xlabel("$\\mathrm{%s}$"%name.replace(" ","\\:"))
                sp_2.set_xlabel("$\\mathrm{%s}$"%name.replace(" ","\\:"))
        cbar.set_label('$\\Large \\mathrm{Sensitivity}$')
        sp_1.set_ylabel('$\\Large \\mathrm{%s}$'%param)
        sp_2.set_ylabel('$\\Large \\mathrm{avg.\\: Sensitivity}$')
        sp_2.set_ylim(-1.*vmax_g, vmax_g)

# check, if specified outdir exists and create it otherwise
outdir = conf.getOption("save sensitivities", "outdir")
if not os.path.exists(outdir):
    os.makedirs(outdir)
elif (os.path.exists(outdir)
        and conf.getOption("save sensitivities", "bruteforce")):
    pass
else:
    logger.error("outdir already exists! Use '--bruteforce 1' to overwrite.")
    sys.exit(1)

# check output filetype
if conf.getOption("save sensitivities", "filetype") == "png":
    extension = '.png'
elif conf.getOption("save sensitivities", "filetype") == "pdf":
    extension = '.pdf'
else:
    raise ValueError("Unsupported filetyp '%s'!"%(
        conf.getOption("save sensitivities", "filetype")))

## create TuningData-object and call TuningData.getTuneData for convenience
td = getConfiguredData()
#td.isValid()
#logger.info('TuningData is valid')

## confirm that selection of observables to plot is valid, i.e. exist in td
obs2plot = plotTheseObservables(td)

## create Sensitivity-object
S = sens.Sensitivity(td, use_obs=obs2plot)
logger.info('interpolations done')

if conf.getOption("save sensitivities", "params") == "all":
    paramstoplot = S._params
else:
    paramstoplot = (conf.getOption("save sensitivities", "params")).split(":")

#global vmax, vmax_g
#lim = conf.getOption("save sensitivities", "limit")
#if lim == 'max':
    #vmax = getMaxSensitivity(S, obs2plot, False)
#else:
    #vmax = float(lim)
#vmax_g = 1.2 * vmax

bar = flpb(0, len(obs2plot) - 1, 30, 'saving sensitivities ')
for num, i, in enumerate(obs2plot):
    bar.update(num)
    fig = pylab.figure(facecolor='w')
    fig.set_figwidth(8)
    fig.set_figheight(0.4*len(paramstoplot)*fig.get_figwidth())

    # define function call abbreviation (cgo = _c_onf._g_et_O_ption(...)
    cgo = lambda name: conf.getOption("save sensitivities", name)
    createOverviewPlot(fig, S, i, cgo("center"), cgo("method"),
                       cgo("errorlevel"), cgo("mode"))


    ## I think this is redundant
    #tit, par, leg =  createTitleAndLegend(S, i, cgo("method"), cgo("mode"),
                                          #cgo("errorlevel"), .5)
    #pylab.figtext(.5,.96, tit,ha='center')
    #pylab.figtext(.5,.92, par,ha='center')
    #pylab.figtext(.5,.01, leg,ha='center')

    pylab.savefig(os.path.join(outdir, createShortFilename(cgo("method"), i) + extension),
                  orientation='landscape')

logger.info("done!")
print "You may now want to create an html-gallery using 'makegallery.py' as such:\n"
print ("         trunk/professor/tools/makegallery.py -s %s %s"
       " sens.html\n")%(outdir, conf.getOption("save sensitivities", "filetype"))

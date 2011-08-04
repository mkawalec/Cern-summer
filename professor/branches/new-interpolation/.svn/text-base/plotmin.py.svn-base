#!/usr/bin/env python2.5
"""plotmin.py

creates eps plots in the current directory for minization results with chi^2
vs. parameter

usage:
    plotmin.py [--saveprefix PREFIX] [--logy] [--help] RESULT.XML [RESULT2.XML...]

    RESULT.XML xml file with the minimization results generated with genmin.py
    PREFIX     any string to be used as prefix a "_" is appended if it does
               exist
    use --help for more information
"""

import sys
import pylab
import numpy

from professor.tools.config import Config
from professor.minimize import ResultList

conf = Config()
conf.initModule('plotmin', {
    'saveprefix': ('', None, True,
                   "prefix for file names. Can contain"
                   " directories where the files are saved, a '_' is"
                   " appended if it does not exist. (E.g."
                   " 'plots/example_')"),
    'ndof' : (True, conf.convBool, True,
              "use chi^2/ndof axis instead of plain chi^2"),
    'method' : ('chi2vsparam', None, True,
                "select the plot method: chi2vsparam|paramvsobs")
    })
conf.setUsage("%prog [options] result.xml [result2.xml ...]")

opts, args = conf.parseCommandline()

if len(args) == 0:
    print conf.getHelp()
    print "Error: no result file given!"
    sys.exit(1)

results = ResultList()
for p in args:
    t = ResultList.fromXML(p)
    for r in t:
        results.append(r)
results.isValid()


class ResultPlotter(object):
    def __init__(self, results, fig):
        self.__results = results
        self.figure = fig

    def getParamNames(self):
        return self.__results.getParamNames()

    def chi2VsParam(self, param):
        # A: prepare the data for plotting
        # dict: keys = number of runs
        #       vals = (chi^2 (over ndof) list, param list)
        if type(param) != int:
            param = self.__results[0].getIndex(param)

        data = {}
        for r in self.__results:
            nor = len(r.runs)
            if not data.has_key(nor):
                data[nor] = ([], [])
            data[nor][0].append(r.chi2)
            data[nor][1].append(r.parunscaled[param])
        return data

    def chi2NdofVsParam(self, param):
        # A: prepare the data for plotting
        # dict: keys = number of runs
        #       vals = (chi^2 (over ndof) list, param list)
        if type(param) != int:
            param = self.__results[0].getIndex(param)

        data = {}
        for r in self.__results:
            nor = len(r.runs)
            if not data.has_key(nor):
                data[nor] = ([], [])
            data[nor][0].append(r.chi2/r.ndof)
            data[nor][1].append(r.parunscaled[param])
        return data

    def plotRunDataDict(self, d, runcolors=None):
        """plot chi^2 vs. param values with different colors for different
        numbers of runs"""
        if runcolors is None:
            runcolors = {}
        self.figure.clear()
        sub = self.figure.add_subplot(111)
        for runs, (chi2s, params) in d.iteritems():
            kwargs = {'marker':'o', 'linestyle':'',
                      'label':'#runs = %i'%(runs)}
            if runcolors.has_key(runs):
                kwargs['color'] = runcolors[runs]

            sub.plot(params, chi2s, **kwargs)
        return sub

    def obsSelVsParam(self, param):
        if type(param) != int:
            param = self.__results[0].getIndex(param)

        data = {}
        maxnoruns = max(self.__results.getRunCounts())
        for r in self.__results:
            if maxnoruns > len(r.runs):
                continue
            obs = ','.join(r.obs)
            if data.has_key(obs):
                raise ValueError("multiple occurances of observable selection:"
                                 " %s"%(obs))
            data[obs] = r.parunscaled[param]

        t = []
        for obs in sorted(data.iterkeys()):
            t.append((obs, data[obs]))
        return t

    def plotObsLists(self, data):
        self.figure.clear()
        sub = self.figure.add_subplot(111)
        for i, (obs, param) in enumerate(data):
            # sub.plot([i], [param], marker='o')
            sub.plot([param], [i], marker='o')
        sub.set_ylim(-.5, len(data) - .5)
        return sub


saveprefix = conf.getOption('plotmin', 'saveprefix')
if saveprefix and not saveprefix.endswith('_'):
    saveprefix += '_'
method = conf.getOption('plotmin', 'method').lower()
rp = ResultPlotter(results, pylab.figure())

if method == 'chi2vsparam':
    for pname in rp.getParamNames():
        if conf.getOption('plotmin', 'ndof'):
            fname = saveprefix + "chi2ndof_vs_" + pname + ".eps"
            d =  rp.chi2NdofVsParam(pname)
            ylabel = "chi^2/ndof"
        else:
            fname = saveprefix + "chi2_vs_" + pname + ".eps"
            d = rp.chi2VsParam(pname)
            ylabel = "chi^2"
        sub = rp.plotRunDataDict(d, runcolors={30:'r'})
        sub.set_xlabel("%s [phys. scale]"%(pname))
        sub.set_ylabel(ylabel)
        sub.legend(loc="best")
        rp.figure.savefig(fname)
        print "saved", fname
elif method == 'paramvsobs':
    old = None
    for pname in rp.getParamNames():
        fname = saveprefix + pname + "_vs_obssel.eps"
        d = rp.obsSelVsParam(pname)
        sub = rp.plotObsLists(d)
        sub.set_xlabel("%s [phys. scale]"%(pname))
        sub.set_ylabel("observable selection index")
        rp.figure.savefig(fname)
        print "saved", fname
        # code to test the integrity of the plots
        cur = [i[0] for i in d]
        if old is not None:
            if cur != old:
                print ("Warning: observable selections differ between"
                       " parameters!")
        old = cur
    for i, obssel in enumerate(old):
        print i, obssel
        print
else:
    print conf.getHelp()
    print "Error: bad plot method specified!"
    sys.exit(1)

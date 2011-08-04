# for epydoc
__docformat__ = "epytext"


import numpy

import professor.tools.parameter
from professor.tools.parameter import ParameterPoint, ppFromList, Scaler
from professor.interpolation import InterpolationSet, BinDistribution


class Histo:
    def __init__(self):
        self._bins = []
        self._issorted = False
        self._name = None
        self._title = None

    def __str__(self):
        out = "Histogram with %d bins:" % self.numBins()
        for b in self.getBins():
            out += "\n" + str(b)
        return out

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name
        return self
    name = property(getName, setName)

    def getTitle(self):
        return self._title

    def setTitle(self, title):
        self._title = title
        return self
    title = property(getTitle, setTitle)

    def numBins(self):
        return len(self._bins)

    def getBins(self):
        if not self._issorted:
            self._bins.sort()
            self._issorted = True
        return self._bins

    def setBins(self, bins):
        self._bins = bins
        self._issorted = False
        return self

    def addBin(self, bin):
        self._bins.append(bin)
        self._issorted = False
        return self

    def getBin(self, index):
        return self.getBins()[index]

    def __iter__(self):
        return iter(self.getBins())

    def __len__(self):
        return len(self._bins)

    def __getitem__(self, index):
        return self.getBin(index)


class Bin:
    """A simple container for a binned value with an error."""
    def __init__(self, xlow=None, xhigh=None, yval=0, yerr=0, focus=0):
        self._xlow = xlow
        self._xhigh= xhigh
        self._yval = yval
        self._yerr = yerr
        self._focus= focus

    def __str__(self):
        out = "%f to %f: %f +- %f" % (self._xlow, self._xhigh, self._yval, self._yerr)
        return out

    def __cmp__(self, other):
        """Sort by mean x value (yeah, I know...)"""
        return (self._xlow + self._xhigh) > (other._xlow + other._xhigh)

    def getXRange(self):
        return (self._xlow, self._xhigh)

    def setXRange(self, xlow, xhigh):
        self._xlow = xlow
        self._xhigh = xhigh
        return self

    def getBinCenter(self):
        """Geometric middle of the bin range."""
        return self._xlow + .5*(self._xhigh - self._xlow)

    def getFocus(self):
        """Mean x-value of the bin."""
        return self._focus

    def getYVal(self):
        return self._yval

    def setYVal(self, yval):
        self._yval = yval
        return self

    def getYErr(self):
        return self._yerr

    def setYErr(self, yerr):
        self._yerr = yerr
        return self


class TuningDataError(Exception):
    pass


## Data structure is map[hname] -> [runnum/"REF"] -> MiniHisto 
class TuningData(object):
    """A container for reference and MC histograms and MC
    parameters, all in one place.
    """
    def __init__(self):
        """Structure of stored data:
        * self._mchistos = {obs-name : { run-key : Histo instance, ...}, ...}
        * self._refhistos = {obs-name : Histo instance, ...}
        * self._params = {run-key : { paramname: paramvalue } ...}
        """
        self._mchistos = { }
        self._refhistos = { }
        self._params = { }
        self._titles = { }

        # map[runkey] -> [hname] -> interpolation
        self._ipols = {}

    def getMCHistoNames(self):
        return self._mchistos.keys()

    def getMCHistos(self, histname):
        if not self._mchistos.has_key(histname):
            return None
        return self._mchistos[histname]

    def getMCHisto(self, histname, runnum):
        try:
            return self._mchistos[histname][runnum]
        except:
            return None

    def setMCHisto(self, histname, runnum, hist):
        if not self._mchistos.has_key(histname):
            self._mchistos[histname] = { }
        self._mchistos[histname][runnum] = hist
        return self

    def getRunNums(self):
        return self._params.keys()

    def setTitles(self, titledict):
        """ @param titledict: a dictionary that has the RefHistoNames as keys
            and identifying strings as values. Might be useful for cryptic
            observable names.
        """
        self._titles = titledict

    def getTitle(self, observable):
        return self._titles[observable]

    def getRefHistoNames(self):
        return self._refhistos.keys()

    def getRefHisto(self, histname):
        if not self._refhistos.has_key(histname):
            return None
        return self._refhistos[histname]

    def setRefHisto(self, histname, hist):
        self._refhistos[histname] = hist
        return self

    def getParams(self, runnum):
        if not self._params.has_key(runnum):
            return None
        return self._params[runnum]

    def setParams(self, runnum, params):
        if not self._params.has_key(runnum):
            self._params[runnum] = { }
        self._params[runnum] = params

    def addParam(self, runnum, paramkey, paramvalue):
        if not self._params.has_key(runnum):
            self._params[runnum] = { }
        self._params[runnum][paramkey] = paramvalue

    def getParam(self, runnum, paramkey):
        runparams = self.getParams(runnum)
        if runparams is None or not runparams.has_key(paramkey):
            return None
        return runparams[paramkey]

    def numberOfParams(self):
        return len(self._params.values()[0])

    def paramNames(self):
        return sorted(self._params.values()[0].keys())

    def __str__(self):
        s = ""
        for hname, runs in self._mchistos.iteritems():
            s += "*** %s ***\n" % hname
            #s += "Runs: " + str(runs.keys()) + "\n"
            if self.getRefHisto(hname):
                s += "Reference histogram\n"
                s += str(self.getRefHisto(hname)) + "\n\n"
            for run, hist in runs.iteritems():
                s += "Run %s\n" % str(run)
                s += str(hist) + "\n\n"
        return s

    def isValid(self):
        """Check if this instance is consistent, otherwise an error is raised.

        The following is checked:
            - Are there the same run keys in the MC histo dict as in the MC
              param dict?
            - Are the same parameters used in the different runs?
            - Do MC histos exist for every observable in the reference dict?

        @raise TuningDataError: If one of the criteria is not met.
        """
        pruns = self._params.keys()
        pruns.sort()
        for name in self.getMCHistoNames():
            mcruns = self.getMCHistos(name).keys()
            mcruns.sort()
            if pruns != mcruns:
                # print pruns, '!=', mcruns
                raise TuningDataError("run-keys for parameters and" +
                        " MC histos (observable %s) differ!"%(name))

        pnames = self.getParams(self.getRunNums()[0]).keys()
        pnames.sort()
        for run in self.getRunNums()[1:]:
            t = self.getParams(run).keys()
            t.sort()
            if pnames != t:
                # print pnames, '!=', t
                raise TuningDataError("parameter names in run %s are"
                        " different from run %s!"%(run, self.getRunNums()[0]))

        mcnames = self.getMCHistoNames()
        mcnames.sort()
        refnames = self.getRefHistoNames()
        refnames.sort()
        #if mcnames != refnames:
        #    # print mcnames, '!=', refnames
        #    raise TuningDataError("reference histo names and MC histo names" +
        #            " differ!")

    def getScaler(self, use_runnums=None):
        # the parameter boundaries
        pbound = {}
        for name, value in self._params.values()[0].iteritems():
            pbound[name] = [value, value]

        for runnum, pdict in self._params.iteritems():
            if use_runnums is None or runnum in use_runnums:
                for name, value in pdict.iteritems():
                    pbound[name][0] = min(pbound[name][0], value)
                    pbound[name][1] = max(pbound[name][1], value)
        # print pbound
        return Scaler(pbound)

    @staticmethod
    def getBinID(histo, ibin):
        return "%s:%i"%(histo.name, ibin)
        # return "%s:%g:%g"%(histo.name, bin.getXRange()[0],
                           # bin.getXRange()[1])

    def getTuneData(self, use_runnums=None, use_obs=None):
        if use_runnums is None:
            use_runnums = self.getRunNums()
        if use_obs is None:
            use_obs = self.getMCHistoNames()

        refbins = {}
        for obs in use_obs:
            refhist = self.getRefHisto(obs)
            for ibin in xrange(refhist.numBins()):
                binid = self.getBinID(refhist, ibin)
                refbins[binid] = refhist.getBin(ibin)

        # binid -> run num -> histo
        mcbins = {}
        for obs in use_obs:
            dummyhisto = self.getMCHisto(obs, use_runnums[0])
            for ibin in xrange(dummyhisto.numBins()):
                binid = self.getBinID(dummyhisto, ibin)
                bindict = {}
                for runnum in use_runnums:
                    bindict[runnum] = self.getMCHisto(obs, runnum).getBin(ibin)
                mcbins[binid] = bindict
        ipolset = self.getInterpolationSet(use_runnums, use_obs)
        return SingleTuneData(refbins, mcbins, ipolset)

    def getInterpolationSet(self, use_runnums, use_obs=None):
        if use_obs is None:
            use_obs = self.getMCHistoNames()
        runskey = ':'.join(sorted(use_runnums))

        parnames = self.paramNames()

        # build a new interpolation list, if needed
        if not self._ipols.has_key(runskey):
            scaler = self.getScaler(use_runnums)
            # TODO: don't use hard coded center value
            center = ppFromList(.5 * numpy.ones(scaler.dim()),
                                scaler, scaled=True)
            self._ipols[runskey] = InterpolationSet(center, runskey)

        # The cached interpolations for this run selection.
        gipols = self._ipols[runskey]
        scaler = gipols.scaler
        center = gipols.center

        # the interpolation set we will return
        ripols = InterpolationSet(center, runskey)

        # runnum -> ParameterPoint
        ppcache = {}
        for runnum in use_runnums:
            ppcache[runnum] = ParameterPoint(self.getParams(runnum), scaler)

        for obs in use_obs:
            # how many bins do we have in this observable?
            dummyhisto = self.getMCHisto(obs, use_runnums[0])
            for ibin in xrange(dummyhisto.numBins()):
                binid = self.getBinID(dummyhisto, ibin)

                # add the interpolation to gipol if it's not there already
                if not gipols.has_key(binid):
                    bd = BinDistribution(parnames, binid)
                    for runnum in use_runnums:
                        bd.addRun(ppcache[runnum],
                                  self.getMCHisto(obs, runnum).getBin(ibin))
                    gipols.addBindistribution(bd)
                ripols[binid] = gipols[binid]
        return ripols


class BinProps(object):
    def __init__(self, refbin, mcdict, ipol):
        self.refbin = refbin
        self.mcdict = mcdict
        self.ipol = ipol

        self.veto = False
        self.__weight = 1.
        self.__sqrtweight = 1.

    def setWeight(self, w):
        self.__weight = w
        self.__sqrtweight = numpy.sqrt(w)

    def setSqrtWeight(self, sw):
        self.__weight = sw**2
        self.__sqrtweight = sw

    weight = property(lambda s: s.__weight, setWeight)
    sqrtweight = property(lambda s: s.__sqrtweight, setSqrtWeight)
    binid = property(lambda s: s.ipol.binid)


class SingleTuneData(dict):
    """Maps binid to a 4-tuple: ref Bin, mcrun->Bin dict, ipol, BinProps."""
    def __init__(self, refbins, mcbins, ipolset):
        """
        @param refbins: dict with binid -> Bin pairs
        @param mcbins: nested dict with binid -> runnum -> Bin items
        @param ipolset: InterpolationSet instance
                        (basicly a binid -> interpolation dict)
        """
        t = {}
        for binid in refbins.iterkeys():
            t[binid] = BinProps(refbins[binid], mcbins[binid], ipolset[binid])
            # (refbins[binid], mcbins[binid],
                        # ipolset[binid], BinProps())
        super(SingleTuneData, self).__init__(t)
        self.scaler = ipolset.scaler
        self.selfuncs = []

    def getInterpolationValues(self, pdict, scaled=False):
        r = {}
        scpar = ParameterPoint(pdict, self,
                               scaled=scaled).getScaled()
        for binid in self.iterkeys():
            r[binid] = self[binid].ipol.getValue(scpar)
        return r

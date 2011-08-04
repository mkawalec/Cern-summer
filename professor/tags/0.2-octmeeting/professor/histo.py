import os
from professor.interpolation.analytic_interpolation import BinDistribution

import warnings


class Histo:
    def __init__(self):
        self._bins = []

    def __str__(self):
        out = "Histogram with %d bins:" % len(self._bins)
        for b in self.getBins():
            out += "\n" + str(b)
        return out

    def getBins(self):
        self._bins.sort()
        return self._bins

    def setBins(self, bins):
        self._bins = bins
        return self

    def addBin(self, bin):
        self._bins.append(bin)
        return self

    def getBin(self, index):
        return self.getBins()[index]

    def __iter__(self):
        return self.getBins()

    def __len__(self):
        return len(self._bins)

    def __getitem__(self, index):
        return self.getBin(index)


class MCHisto(Histo):
    def __init__(self, parameters=None, run=None):
        Histo.__init__(self)
        self._parameters = parameters
        self._runnr = run
        warnings.warn(warnings.DeprecationWarning("We don't want to use MCHisto class anymore!"))

    def setParameters(self, pars):
        self._parameters = pars

    def getParameters(self):
        return self._parameters

    def getRunnr(self):
        return self._runnr

    def setRunnr(self, runnr):
        self._runnr = runnr

    def getObservable(self):
        return self._observable

    def setObservable(self, obs):
        self._observable = obs


class Bin:
    """A simple container for a binned value with an error."""
    def __init__(self, xlow, xhigh, yval=0, yerr=0, focus=0):
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

    # returns the bin-focus
    def getFocus(self):
        return self._focus


class HistoFromAscii(MCHisto):
    def __init__(self, filename, mc=True):
        MCHisto.__init__(self)
        self._filename = filename
        self._mc = mc
        #if mc == True:
        #    self._h = MCHisto()
        #else:
        #    self._h = Histo()
        self.parseFile()

    def parseFile(self):
        if not self._mc == True:
            for line in open(self._filename):
                self.readBinContent(line)
        else:
            for line in open(self._filename):
                if line.startswith('# Observable'):
                    self.readObservable(line)
                elif line.startswith('# Parameters'):
                    self.readParameters(line)
                elif line.startswith('# Run'):
                    self.readRun(line)
                else:
                    self.readBinContent(line)

    def readBinContent(self, line):
        temp = line.split()
        if len(temp)==3:
            bin = Bin( float(temp[0]), float(temp[1]), float(temp[2]),
                    0)
        elif len(temp)==4:
            bin = Bin( float(temp[0]), float(temp[1]), float(temp[2]),
                    float(temp[3]) )
        elif len(temp)==5:
            bin = Bin( float(temp[0]), float(temp[1]), float(temp[2]),
                    float(temp[3]), float(temp[4]) )
        try:
            self.addBin(bin)
            # self._h.addBin(bin)
        except UnboundLocalError, e:
            print line, temp
            raise e

    def readObservable(self, line):
        name = line.split()[-1]
        self.setObservable(name)
        # self._h.setObservable(name)

    def readParameters(self, line):
        d = {}
        trash, v = line.split(':')
        for i in xrange(0, len(v.split()), 2):
            d[ v.split()[i] ] = float(v.split()[i+1])
        self.setParameters(d)
        # self._h.setParameters(d)

    def readRun(self, line):
        run = line.split()[-1]
        self.setRunnr(run)
        # self._h.setRunnr(run)

    def getHisto(self):
        return self._h


class TuningDataError(StandardError):
    pass

## Data structure is map[hname] -> [runnum/"REF"] -> MiniHisto 
class TuningData:
    """A container for reference and MC histograms and MC
    parameters, all in one place.
    """
    def __init__(self):
        # Structure of stored data:
        # self._mchistos = {obs-name : { run-key : Histo instance, ...}, ...}
        # self._refhistos = {obs-name : Histo instance, ...}
        # self._params = {run-key : param dict, ...}

        self._mchistos = { }
        self._refhistos = { }
        self._params = { }


    def getMCHistoNames(self):
        return self._mchistos.keys()

    def getMCHistos(self, histname):
        if not self._mchistos.has_key(histname):
            return None
        return self._mchistos[histname]

    def setMCHisto(self, histname, runnum, hist):
        if not self._mchistos.has_key(histname):
            self._mchistos[histname] = { }
        self._mchistos[histname][runnum] = hist
        return self

    def getRunNums(self):
        return self._params.keys()


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

    def numberOfParams(self):
        return len(self._params.values()[0])

    def paramsNames(self):
        return dictToLists(self._params.values()[0])[1]

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
            * Are there the same run keys in the MC histo dict as in the MC
              param dict?
            * Are the same parameters used in the different runs?
            * Do MC histos exist for every observable in the reference dict?

        @raise: TuningDataError
        """
        pruns = self._params.keys()
        pruns.sort()
        for name in self.getMCHistoNames():
            mcruns = self.getMCHistos(name).keys()
            mcruns.sort()
            if pruns != mcruns:
                print pruns, '!=', mcruns
                raise TuningDataError("run-keys for parameters and" +
                        " MC histos (observable %s) differ!"%(name))

        pnames = self.getParams(self.getRunNums()[0]).keys()
        pnames.sort()
        for run in self.getRunNums()[1:]:
            t = self.getParams(run).keys()
            t.sort()
            if pnames != t:
                print pnames, '!=', t
                raise TuningDataError("parameter names in run %s are" +
                        " different from run %s!"%(run, self.getRunNums()[0]))

        mcnames = self.getMCHistoNames()
        mcnames.sort()
        refnames = self.getRefHistoNames()
        refnames.sort()
        if mcnames != refnames:
            print mcnames, '!=', refnames
            raise TuningDataError("reference histo names and MC histo names" +
                    " differ!")

    def getParameterBoundaries(self, use_runnums=None):
        """Returns the minimal and maximal parameter values.

        @param use_runnums: a list with the run numbers for which the
            BinDistributions are wanted. C{None} if all stored runs are
            used.
        @type use_runnums: C{list} of C{strings}
        @return: C{list} with the minimal values, C{list} with the maximal values.
        """
        pmin = dictToLists(self._params.values()[0])[0]
        pmax = dictToLists(self._params.values()[0])[0]
        # print pmin, pmax
        for runnum, pdict in self._params.iteritems():
            if use_runnums == None or runnum in use_runnums:
                pv = dictToLists(pdict)[0]
                # print runnum, pv
                for i, v in enumerate(pv):
                    pmin[i] = min(pmin[i], v)
                    pmax[i] = max(pmax[i], v)
                # print runnum, pv
        # print pmin, pmax
        return pmin, pmax

    def buildBinDistList(self, use_runnums=None, use_obs=None, center=.5):
        """Returns a list of (refbin, BinDistribution) pairs build from this
        TuningData object.

        The parameters for the BinDistributions are normalized!

        This code supposes that all runs use the same set of parameter names
        and all histogramms for one observable use the same binning.

        @param use_runnums: a list with the run numbers for which the
            BinDistributions are wanted. C{None} if all stored runs are
            used.
        @type use_runnums: C{list} of C{strings}
        @param use_obs: a list with the observables for which the
            BinDistributions are wanted. C{None} if all stored observables
            are used.
        @type use_obs: C{list} of C{strings}
        """
        # the list returned
        bds = []

        # the parameter names
        pnames = dictToLists(self._params.values()[0])[1]

        pmin, pmax = self.getParameterBoundaries(use_runnums)
        # print pmin, pmax

        # run through all observables
        for obs in self.getRefHistoNames():
            if use_obs == None or obs in use_obs:
                refhisto = self._refhistos[obs]

                # run through all bins of this observable
                for binnum, refbin in enumerate(refhisto.getBins()):
                    bd = BinDistribution(obs, refbin.getXRange(), pnames)
                    bd.setCenter(center)
                    for runnum, mchist in self._mchistos[obs].iteritems():
                        # take care of use_runnums
                        if use_runnums == None or runnum in use_runnums:
                            bd.addRun(mchist.getBin(binnum),
                                    normalizeParameterDict(
                                        self._params[runnum], pmin, pmax))
                                    # dictToLists(self._params[runnum])[0])
                    bd.calcInterpolationCoefficients()
                    bds.append((refhisto.getBin(binnum), bd))
        return bds


# little helper function
def dictToLists(pardict):
    """Converts a parameter dictionary to two lists.

    Values are sorted with the parameter names.
    @return: Two lists: I{parameter values, parameter names}
        sorted by the parameter names.
    """
    pv = []
    pnames = pardict.keys()
    pnames.sort()
    for i, k in enumerate(pnames):
        pv.append(pardict[k])
    return pv, pnames

def normalizeParameterDict(pdict, pmin, pmax):
    r = []
    for i, v in enumerate(dictToLists(pdict)[0]):
        r.append((v - pmin[i])/(pmax[i] - pmin[i]))
    return r

def unNormalizeParameterDict(pdict, pmin, pmax):
    r = []
    for i, v in enumerate(dictToLists(pdict)[0]):
        r.append(v*(pmax[i] - pmin[i]) + pmin[i])
    return r


def getHistolist(path, obs, ascii=True, filetype='txt', mc=True):
    """ create a list of Histo/MCHisto-class-objects of the same Observable.\n
        Returns tuple: (list, name of observable)
        Default is: ASCII-files of type *.txt
    """
    histolist = []
    if ascii:
        for asciifile in os.listdir(path):
            if asciifile.startswith(str(obs)) and asciifile.endswith(filetype):
                hfa = HistoFromAscii(path+'/'+asciifile)
                histolist.append(hfa)#.getHisto())
        return (histolist, obs) # return tuple: (histolist, obs) 
    else:
        print 'Feature not yet implemented'


def makePackage(histolist):
    """ prepare a dictionary of data out of several histogram-files
        so that calculation of sensitivity can be handled easily
    """
    container = {}
    histdata = {}
    keys = []
    for histo in histolist[0]: # histolist[0] contains the histograms
                               # histolist[1] is the observable's name
        dataset = {}
        dataset['Parameters'] = histo.getParameters()
        if len(keys) == 0:
            for par in histo.getParameters().iterkeys():
                keys.append(par)

        bins = {}
        for i in histo.getBins():
            bins[i.getXRange()]= ( i.getYVal(), i.getYErr())

        dataset['Bins'] = bins
        histdata[histo.getRunnr()] = dataset

    container[histolist[1]] = histdata
    container['Observable'] = histolist[1]
    container['Parametersused'] = keys

    return container

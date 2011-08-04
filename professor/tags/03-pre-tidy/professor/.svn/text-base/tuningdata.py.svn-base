"""tuningdata.py

"""

import logging
import itertools
import operator
import os.path
import numpy, re
import tempfile

from professor.tools.parameter import ParameterPoint, ppFromList, Scaler
from professor.tools.elementtree import ET
from professor.interpolation import InterpolationSet, BinDistribution
from professor import histo
from professor.minimize.result import MinimizationResult


class TuningDataError(Exception):
    pass


class GoFData(list):
    """Data container for chi^2/goodness of fit calculation.

    It's a list of 3-tuples: [(ref bin, sim bin, weight), ...]
    Where sim bin can be eather from MC data or from an
    Interpolation.getBin(param) call.
    """
    def __init__(self, nopar, referror=True, simerror=False):
        self.referror = referror
        self.simerror = simerror
        self.__nopar = nopar

    nopar = property(lambda s: s.__nopar)

    def calcNdof(self):
        # sumw = 0.0
        # for rb, sb, w in self:
            # sumw += w
        sumw = sum(map(operator.itemgetter(2), self))
        return sumw - self.nopar
    ndof = property(calcNdof)

    def calcChi2(self):
        """ converting to numpy.float types mandatory if
        simerrors are used # this is still buggy :(
        """
        re = self.referror
        se = self.simerror
        #logging.debug("Calculating chi^2 with re=%s se=%s"%(re, se))
        rchi2 = numpy.float(0.0)
        # try:
#<<<<<<< .mine
        #for refbin, simbin, weight in self:
#=======
        # for refbin, simbin, weight, sim_deriv in self:
            # qerr = numpy.float(0.0)
            # if re:
                # qerr += numpy.float(refbin.getYErr())**2
            # if se:
                # qerr += numpy.float(simbin.getYErr())**2

            # rchi2 += numpy.float(weight) * numpy.float(
                    # refbin.getYVal() - simbin.getYVal())**2 / qerr
        # except:
        for refbin, simbin, weight in self:
#>>>>>>> .r594
            qerr = numpy.float(0.0)
            if re:
                qerr += numpy.float(refbin.getYErr())**2
            if se:
                qerr += numpy.float(simbin.getYErr())**2

            rchi2 += numpy.float(weight) * numpy.float(
                    refbin.getYVal() - simbin.getYVal())**2 / qerr
        return rchi2
    chi2 = property(calcChi2)


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
        * self._scanparams = {run-key : paramvalue ...}
        """
        self._mchistos = { }
        self._refhistos = { }
        self._params = { }
        self._scanparams = { }
        self._titles = { }

    def getMCHistoNames(self):
        return self._mchistos.keys()

    def getMCHistos(self, histname):
        return self._mchistos[histname]

    def getMCHisto(self, histname, runnum):
        return self._mchistos[histname][runnum]

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
        """Return the stored title for the given observable.

        If no title is found, the observable is returned.
        """
        try:
            return self._titles[observable]
        except KeyError:
            return observable

    def getRefHistoNames(self):
        return self._refhistos.keys()

    def getRefHisto(self, histname):
        return self._refhistos[histname]

    def setRefHisto(self, histname, hist):
        self._refhistos[histname] = hist
        return self

    def getParams(self, runnum):
        return self._params[runnum]

    def setParams(self, runnum, params):
        if not self._params.has_key(runnum):
            self._params[runnum] = { }
        for k, v in params.iteritems():
            self.addParam(runnum, k, v)

    def setScanParam(self, runnum, param):
        self._scanparams[runnum] = param

    def getScanParam(self, runnum):
        return self._scanparams[runnum]

    def addParam(self, runnum, paramkey, paramvalue):
        if not self._params.has_key(runnum):
            self._params[runnum] = { }
        self._params[runnum][paramkey] = paramvalue

    def getParam(self, runnum, paramkey):
        return self.getParams(runnum)[paramkey]

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

    @staticmethod
    def getBinRanges(histo):
        """ return a 2xN numpy.array of the N bins in a histo the first column
            keeps the lower, the second column the upper bin edges
        """
        return numpy.array([bin.getXRange() for bin in histo])

    def isValid(self):
        """Check if this instance is consistent, otherwise an error is raised.

        The following is checked:
            - Are there the same run keys in the MC histo dict as in the MC
              param dict?
            - Are the same parameters used in the different runs?
            - Do MC histos exist for every observable in the reference dict?
            - Do reference and MC histos have the same bin ranges?

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
                raise TuningDataError("parameter names in run %s are"
                        " different from run %s!"%(run, self.getRunNums()[0]))

        # mcnames = self.getMCHistoNames()
        # mcnames.sort()
        # refnames = self.getRefHistoNames()
        # refnames.sort()
        # if mcnames != refnames:
        #     # print mcnames, '!=', refnames
        #     raise TuningDataError("reference histo names and MC histo names" +
        #             " differ!")
        for obs in self.getMCHistoNames():
            refrange = self.getBinRanges(self.getRefHisto(obs))
            for run in self.getRunNums():
                mcrange = self.getBinRanges(self.getMCHisto(obs, run))
                # ref and MC histo have different numbers of bins
                if refrange.shape != mcrange.shape:
                    raise TuningDataError("%s REF and MC run %s histos have"
                            " different numbers of bins (ref=%i mc=%i)" % (
                            obs, run, refrange.shape[0], mcrange.shape[0]))

                # Ref and MC histo bin ranges differ by more than AIDA 
                # standard numerical output precision, which is AFAIK 1.0e-12 .
                elif numpy.max(numpy.abs(refrange - mcrange)) > 1.0e-12:
                    logging.error("max(ref-MC bin range) = %e" % (
                        numpy.max(numpy.abs(refrange - mcrange))))
                    logging.error("refrange - mcrange = %s" %(refrange - mcrange))
                    raise TuningDataError("%s REF and MC run %s histos have"
                            " different bin ranges!" % (obs, run))

    def getNaNInfo(self):
        """Return a {obspath => {runnum => Bin}} nested dict bins that contain NaNs."""
        ret = {}
        for obs in self.getMCHistoNames():
            mchists = self.getMCHistos(obs)
            for runnum, histo in mchists.items():
                for bin in histo:
                    if (not numpy.isfinite(bin.getYVal()) or
                        not numpy.isfinite(bin.getYErr())):
                        if not ret.has_key(obs):
                            ret[obs] = {}
                        ret[obs][runnum] = bin
        return ret

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
        return Scaler(pbound)

    @staticmethod
    def getBinID(histo, ibin):
        return "%s:%i"%(histo.fullname, ibin)

    def getTuneData(self, ipolcls, use_runnums=None, use_obs=None):
        """
        Get tune data for the requested observables, including the MC data from
        the requested runs, and an optimised interpolation function based on
        those runs.

        @param use_runnums : list of run name strings
        @param use_obs : list of observable name strings
        @return A SingleTuneData object
        """
        if use_runnums is None:
            use_runnums = self.getRunNums()
        if use_obs is None:
            use_obs = self.getMCHistoNames()

        refbins = {}
        for obs in use_obs:
            try:
                refhist = self.getRefHisto(obs)
                for ibin in xrange(refhist.numBins()):
                    binid = self.getBinID(refhist, ibin)
                    refbins[binid] = refhist.getBin(ibin)
            except:
                print "could not get ref histo for %s"%obs

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
        ipolset = self.getInterpolationSet(ipolcls, use_runnums, use_obs)
        return SingleTuneData(refbins, ipolset, mcbins)

    def getGoFFromMC(self, run, weightdict, extraveto=None):
        gofdata = GoFData(self.numberOfParams())
        for obsname, weight in weightdict.iteritems():
            try:
                mchist = self.getMCHisto(obsname, run)
            except:
                logging.debug("Requested observable %s not in TuningData object!"%obsname)
                continue
            for ibin, refbin in enumerate(self.getRefHisto(obsname).getBins()):
                # only add bins, where the reference error is > 0.0
                if extraveto is None:
                    if refbin.getYErr() > 0.0:
                        gofdata.append((refbin, mchist.getBin(ibin), weight))
                else:
                    if refbin.getYErr() > 0.0 and self.getBinID(
                            mchist, ibin) not in extraveto:
                        gofdata.append((refbin, mchist.getBin(ibin), weight))
                    else:
                        logging.debug('vetoing binid: %s '%str(
                            self.getBinID(mchist, ibin)))

        return gofdata

    def getParameterRanges(self, runs=None):
        ranges = {}
        for name in self.paramNames():
            if runs is not None:
                temp = [self.getParams(run)[name] for run in runs]
            else:
                temp = [self.getParams(run)[name] for run in self.getRunNums()]
            ranges[name]=(min(temp), max(temp))
        return ranges

    def getInterpolationSet(self, ipolmethod, use_runnums, use_obs=None):
        if use_obs is None:
            use_obs = self.getMCHistoNames()
        runskey = ':'.join(sorted(use_runnums))

        scaler = self.getScaler(use_runnums)
        center = ppFromList(.5 * numpy.ones(scaler.dim()), scaler,
                scaled=True)

        pnames = self.paramNames()

        # the interpolation set we will return
        ipolset = InterpolationSet(center, runskey, ipolmethod)

        # runnum -> ParameterPoint
        ppcache = {}
        for runnum in use_runnums:
            ppcache[runnum] = ParameterPoint(self.getParams(runnum), scaler,
                    scaled=False)

        for obs in use_obs:
            dummyhisto = self.getMCHisto(obs, use_runnums[0])
            for ibin in xrange(dummyhisto.numBins()):
                binid = self.getBinID(dummyhisto, ibin)
                binrange = dummyhisto.getBin(ibin).getXRange()
                bd = BinDistribution(pnames, binid, binrange)
                for runnum in use_runnums:
                    bd.addRun(ppcache[runnum],
                            self.getMCHisto(obs, runnum).getBin(ibin))
                ipolset.addBindistribution(bd)
        return ipolset


class CachingTuningData(TuningData):
    """TuningData that caches the interpolations and optionally writes them to disk.
    """
    def __init__(self):
        super(CachingTuningData, self).__init__()

        # map ipolcls -> runkey -> interpolation set
        #                          (binid -> interpolation)
        self._ipols = {}

    def setInterpolationSet(self, ipolset):
        ipolmethod = ipolset.ipolmethod
        runskey = ipolset.runskey
        logging.debug("Caching interpolation set with method '%s' and runs"
                " '%s'" % (ipolmethod, runskey))
        if not self._ipols.has_key(ipolmethod):
            self._ipols[ipolmethod] = dict()

        if self._ipols[ipolmethod].has_key(runskey):
            logging.warn("Interpolations for runs %s with method %s already"
                    " set! Overwriting previous interpolations!" % (
                        runskey, ipolmethod))
        self._ipols[ipolmethod][runskey] = ipolset

    def getInterpolationSet(self, ipolmethod, use_runnums, use_obs=None):
        """Return an interpolation set for the given runs and observables.

        Interpolations are cached in TuningData and created on demand.
        """
        if use_obs is None:
            use_obs = self.getMCHistoNames()
        runskey = ':'.join(sorted(use_runnums))

        parnames = self.paramNames()

        if not self._ipols.has_key(ipolmethod):
            self._ipols[ipolmethod] = dict()

        # Build a new interpolation set, if needed.
        if not self._ipols[ipolmethod].has_key(runskey):
            logging.debug("Calculating %s interpolation for %s."%(ipolmethod, runskey))
            scaler = self.getScaler(use_runnums)
            # TODO: Don't use hard coded center value.
            center = ppFromList(.5 * numpy.ones(scaler.dim()),
                                scaler, scaled=True)
            self._ipols[ipolmethod][runskey] = InterpolationSet(center, runskey, ipolmethod)

        # The cached interpolations for this run selection.
        gipols = self._ipols[ipolmethod][runskey]
        scaler = gipols.scaler
        center = gipols.center

        # the interpolation set we will return
        ripols = InterpolationSet(center, runskey, ipolmethod)

        # runnum -> ParameterPoint
        ppcache = {}
        for runnum in use_runnums:
            ppcache[runnum] = ParameterPoint(self.getParams(runnum), scaler,
                    scaled=False)

        try:
            for obs in use_obs:
                # how many bins do we have in this observable?
                dummyhisto = self.getMCHisto(obs, use_runnums[0])
                for ibin in xrange(dummyhisto.numBins()):
                    binid = self.getBinID(dummyhisto, ibin)
                    binrange = dummyhisto.getBin(ibin).getXRange()

                    # add the interpolation to gipol if it's not there
                    # already
                    if not gipols.has_key(binid):
                        bd = BinDistribution(parnames, binid, binrange)
                        for runnum in use_runnums:
                            bd.addRun(ppcache[runnum],
                                      self.getMCHisto(obs, runnum).getBin(ibin))
                        gipols.addBindistribution(bd, ipolmethod)
                    ripols[binid] = gipols[binid]
            return ripols
        except ValueError, e:
            logging.error("Failed to build interpolations: %s"%(e))
            logging.error("Removing runskey '%s' from cache."%(runskey))
            del self._ipols[ipolcls][runskey]
            raise e

    def writeInterpolationSets(self, ipoldir):
        """
        Write all currently cached interpolation sets to files under ipoldir.
        """
        # this should be done during commandline argument parsing
        # ipoldir = os.path.abspath(ipoldir)
        # allruns = set(self.getRunNums())
        for methodvals in self._ipols.itervalues():
            for ipolset in methodvals.itervalues():
                if not ipolset.getWriteFlag():
                    fname = tempfile.mktemp(dir="", suffix=".pkl", prefix="ipolset")

                    logging.debug("Storing %s in '%s'"%(ipolset, fname))
                    ipolset.write(os.path.join(ipoldir, fname))
                else:
                    logging.debug("%s already exists on hardrive." % (ipolset))


class WriteBackTuningData(CachingTuningData):
    """This is a enhanced TuningData version which writes back all cached
    interpolations when it's destroyed.
    """
    def __init__(self, ipoldir):
        super(WriteBackTuningData, self).__init__()
        # test if we have write access to given ipoldir
        if not os.path.isdir(ipoldir):
            raise IOError("Given interpolation directory '%s' does not exist"
                          " or is not a directory!"%(ipoldir))
        if not os.access(ipoldir, os.W_OK|os.X_OK):
            raise IOError("Missing 'w' or 'x' permission for given"
                          " interpolation directory '%s'!"%(ipoldir))
        self.__ipoldir = ipoldir

    def __del__(self):
        logging.info("Writing all interpolation sets to directory"
                     " '%s'"%(self.__ipoldir))
        try:
            self.writeInterpolationSets(self.__ipoldir)
        except Exception, e:
            logging.error("Failed to write all interpolation sets: %s"%(e))


class SingleTuneData(dict):
    """
    Container for the data used for one tune, i.e. a specific choice of run
    numbers, observables and selection functions (= weights and vetos).
    """
    def __init__(self, refbins, ipolset, mcbins=None, extraveto=None):
        """
        @param refbins: dict with binid -> Bin pairs
        @param mcbins: nested dict with binid -> runnum -> Bin items
        @param ipolset: InterpolationSet instance
                        (basically a binid -> interpolation dict)
        @param extraveto: a list of binids to veto
        """
        t = {}
        if mcbins is None:
            for binid in refbins.iterkeys():
                t[binid] = BinProps(refbins[binid], None, ipolset[binid])
            self.__mcdata = False
            # Store the run numbers from ipolset because we don't have MC
            # data from where we take them otherwise.
            self.__runnums = ipolset.runskey.split(":")
        else:
            for binid in refbins.iterkeys():
                t[binid] = BinProps(refbins[binid], mcbins[binid],
                        ipolset[binid])
            self.__mcdata = True
        super(SingleTuneData, self).__init__(t)
        self._zerocoeffbinids = []
        self._extraveto = extraveto
        self.vetoEmptyErrors()
        self.vetoZeroCoeffs()
        self.vetoExtra()
        self.scaler = ipolset.scaler

    def vetoZeroCoeffs(self):
        for bp in self.itervalues():
            # if bp.refbin.getYErr() == 0 or bp.refbin.getYVal() == 0:
            if bp.ipol.coeffs.all() == numpy.zeros(len(bp.ipol.coeffs)).all():
                bp.veto = True
                if not bp.binid in self._zerocoeffbinids:
                    self._zerocoeffbinids.append(bp.binid)
                logging.debug('all ipol-coeffs == 0 for binid: %s'%str(bp.binid))
                continue

    def vetoExtra(self):
        if self._extraveto is not None:
            for bp in self.itervalues():
                if bp.binid in extraveto:
                    bp.veto = True

    def vetoEmptyErrors(self):
        for bp in self.itervalues():
            # if bp.refbin.getYErr() == 0 or bp.refbin.getYVal() == 0:
            if bp.refbin.getYErr() <= 0.0:
                bp.veto = True
                continue


    def numParams(self):
        return self.scaler.dim()

    def getBinProps(self, use_obs, apply_veto=False):
        """ return all binprops of a certain observable
            @param apply_veto: this is a switch that filters out those
            binprops whose .veto value is True
        """
        if apply_veto:
            return [binprop for binid, binprop in self.iteritems()
                    if binid.startswith(use_obs) and not binprop.veto]
        else:
            return [binprop for binid, binprop in self.iteritems()
                    if binid.startswith(use_obs)]

    def applyObservableWeightDict(self, weights):
        """
        Make sure the keys fit the observable names in the bin ID in this
        instance!
        """
        for binid, binprop in self.iteritems():
            obsname = binid.split(':')[0]
            w = weights[obsname]
            logging.debug("weighting bin %s with %g"%(binid, w))
            binprop.weight = w

    def getChi2Function(self):
        """
        Return a chi^2 function (interpolation vs. reference data) for
        minimization.

        The ndof can be accessed by the chi2func.ndof property or the getNdof
        method of the SingleTuneData instance.
        """
        def chi2func(p):
            return self.getGoFFromIpol(p, scaled=True).chi2

        chi2func.ndof = self.getNdof()

        return chi2func

    def filteredValues(self):
        """Return an iterator with the bin properties without vetoed or
        zero-weighted bins.
        """
        return itertools.ifilterfalse(lambda bp: bp.veto or bp.weight <= 0.0, self.itervalues())

    def getNdof(self):
        """Return the number of degrees of freedom.

        Ndof = sum_bin{weight_bin} - n_params
        """
        # calculate the sum of weights with python's builtin magic
        #TODO: take care of vetoes
        sumweights = sum(map(lambda binprop: binprop.weight,
                             self.filteredValues()))
        return sumweights - self.scaler.dim()

    def getGoFFromMC(self, run):
        """Return reference vs. MC compare data for given run."""
        if not self.__mcdata:
            raise ValueError("This SingleTuneData was created without MC data!")
        gofdata = GoFData(self.numParams())
        for binprop in self.filteredValues():
            gofdata.append((binprop.refbin, binprop.mcdict[run],
                             binprop.weight))
        return gofdata

    def getGoFFromIpol(self, params, scaled=False):
        """Return reference vs. interpolation compare data at the given
        parameter point.

        @param: Can be a list or a dict with the (un-)scaled values.
        """
        compdata = GoFData(self.numParams())
        if type(params) == dict:
            pp = ParameterPoint(params, self.scaler, scaled=scaled)
        else:
            pp = ppFromList(params, self.scaler, scaled=scaled)
        for binprop in self.filteredValues():
            refbin = binprop.refbin
            simbin = binprop.ipol.getBin(pp.getScaled())
            # try:
                # sim_deriv = binprop.ipol.getGradient(pp.getScaled())
            # except:
                # sim_deriv = None
            #logging.debug("refbin: %s \t simbin: %s"%(refbin, simbin))
#<<<<<<< .mine
            #compdata.append((refbin, simbin, binprop.weight))
#=======
            # compdata.append((refbin, simbin, binprop.weight, sim_deriv))
            compdata.append((refbin, simbin, binprop.weight))
#>>>>>>> .r594
        return compdata

    def getRunNums(self):
        """Return a list with the run numbers."""
        if self.__mcdata:
            return self.values()[0].mcdict.keys()
        else:
            return self.__runnums

    def getObservables(self):
        obs = map(lambda s: s.split(":")[0], self.keys())

        # make the list unique
        obs = set(obs)

        return list(obs)

    def getInterpolationHisto(self, observable, parampoint, title=None):
        """ return a Histo object of an observable derived
            from the interpolation at a certain parameter point
            @param parampoint: can be a dict or a ParameterPoint instance
            or even a MinimizationResult instance
        """
        if not observable in self.getObservables():
            raise ValueError("Observable %s not amongst these:"%observable)

        if isinstance(parampoint, MinimizationResult):
            pointasarray = parampoint.parscaled
        elif isinstance(parampoint, ParameterPoint):
            pointasarray = parampoint.getScaled()
        elif type(parampoint) == dict:
            pointasarray = ParameterPoint(parampoint, self.scaler).getScaled()
        else:
            raise TypeError("Argument parampoint must be of types"
                    " MinimizationResult, ParameterPoint, or dict!")

        h = histo.Histo()
        binprobs = self.getBinProps(observable)
        binprobs.sort()
        for i in binprobs:
            h.addBin(i.ipol.getBin(pointasarray))
        h.setName(observable)
        h.setTitle(title)
        return h


class BinProps(object):
    """
    Container for all data related to a bin needed to do a minimisation.

    A container for all the variants on a distribution bin: its weight, its
    reference value and errors, a collection of its simulated equivalents from a
    set of MC runs, and an interpolation function for that bin, based on
    optimising the fit to a sampling of MC points in the parameter space.

    At the moment the following is stored:
     - refbin: a Bin instance with the reference bin
     - mcdict: a run number -> MC Bin dictionary
     - ipol: a QuadraticBinInterpolation instance
     - veto: a flag for vetoing this bin in the GoF calculation
     - weight/sqrtweight: weights for the GoF calculation
    """
    def __init__(self, refbin, mcdict, ipol):
        self.refbin = refbin
        self.mcdict = mcdict
        self.ipol = ipol

        self.veto = False
        self.__weight = 1.0
        self.__sqrtweight = 1.0

    def __cmp__(self, other):
        """ This allows for sorting BinProps by binids """
        return cmp(int(self.binid.split(':')[-1]),
                int(other.binid.split(':')[-1]))

    def setWeight(self, w):
        self.__weight = w
        self.__sqrtweight = numpy.sqrt(w)

    def setSqrtWeight(self, sw):
        self.__weight = sw**2
        self.__sqrtweight = sw

    def getBinCenter(self):
        return self.refbin.getBinCenter()

    weight = property(lambda s: s.__weight, setWeight)
    sqrtweight = property(lambda s: s.__sqrtweight, setSqrtWeight)
    binid = property(lambda s: s.ipol.binid)



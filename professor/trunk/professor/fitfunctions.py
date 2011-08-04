"""GoF calculators

Interface for the generic Professor goodness of fit (GoF) calculator object, and
commonly-used derivations and concrete implementations of that interface for
various kinds of chi^2 and similar measures.

TODO: make interface sufficiently generic that it can do very specific things
like optimising the difference between sets of histograms (e.g. for observable
optimisation.)
"""

import numpy
from professor.tools import log
from professor.tools.decorators import virtualmethod
from professor.params import ParameterPoint

__all__ = ["SimpleIpolChi2", "SimpleMCChi2", "SingleSimpleIpolChi2", "SingleSimpleMCChi2"]


class BaseGoF(object):
    """Interface definition for all GoF calculators.
    """
    def __init__(self, tunedata):
        self.tunedata = tunedata

    @virtualmethod
    def calcGoF(self):
        pass



class BaseChi2(BaseGoF):
    """Interface definition for all chi^2-like GoF calculators.
    """
    def __init__(self, tunedata):
        BaseGoF.__init__(self, tunedata)

    def calcGoF(self):
        "For chi^2 GoFs, the GoF is the chi2/Ndf"
        return self.calcChi2()/self.calcNdof()

    @virtualmethod
    def calcChi2(self):
        pass

    @virtualmethod
    def calcNdof(self):
        pass



class SimpleIpolChi2(BaseChi2):
    """Calculating chi^2/Ndf from the interpolations.

    The parameter point needs to be set before the chi^2 calculation with
    setParams().

    The use_ref_error and use_mc_error properties determine how the error terms
    in the chi^2 are defined. The "epsilon" term is an extra fractional error to
    be used as a regulariser, i.e. a minimum possible systematic error beyond
    that seen from the reference or statistical plot errors.

    TODO: allow the epsilon factors to be set in a distribution-specific way
    like the observable weights (including by ranges, by specific bins, etc.)
    """

    def __init__(self, tunedata, epsilon=0.0, withcorrelation=False):
        BaseChi2.__init__(self, tunedata)
        self.params = None
        self.epsilon = epsilon # TODO: remove, in favour of the value on the BinProps
        self.use_ref_error = True
        self.use_mc_error = True
        self.withcorrelation = withcorrelation
        # TODO: Remove this in the future.
        ## For now disable use of median MC error for interpolations if a
        ## BinProps with an interpolation that lacks a medianmcerror is found.
        if len(filter(lambda bp: not hasattr(bp.ipol, "medianmcerr"),
                      self.tunedata.filteredValues())) > 0:
            log.warn("Some interpolations lack a 'medianmcerr'! Rebuild"
                         " your interpolations or deal with the consequences"
                         " (i.e. no MC error is included in GoF)")
            self.use_mc_error = False


    def setParams(self, params):
        """
        Set the parameter point. Argument type should either be a ParameterPoint or a dict.

        Returns self to allow chaining for convenience.
        """
        if type(params) is dict:
            params = ParameterPoint.mkFromDict(params)
        self.params = numpy.asarray(params)
        return self


    def calcChi2(self, params=None):
        """
        Calculate and return the chi^2 at the currently-set parameter point.

        When correlation consideration is disabled from command line,
        the old code is used where chi2 is calculated cumulatively.

        Otherwise, a dictionary for all observables considered in the tuning
        is built-up.

        From the bins in this dictionary a covariance matrix can be calculated
        (from a given correlation file), and later on the chi2 can be obtained
        from a matrix relation.

        TODO:
        =====
        * Test functionality of covariance matrix/correlations.
        * If it works, cache covariance matrix.
        """
        if not params:
            params = self.params
        else:
            params = numpy.asarray(params)

        def getExtraErr(bp):
            extraerr = bp.getProperty("extraerr")
            if not extraerr:
                return 0.0
            if type(extraerr) is str:
                #print bp.binid, extraerr
                # TODO: I've chosen to multiply the ref value, but could use the MC value... or both. Hmm!
                relval = bp.refbin.getVal()
                if extraerr.strip().endswith("x"):
                    num = float(extraerr.strip()[:-1])
                    extraerr = relval * num
                elif extraerr.strip().endswith("%"):
                    num = float(extraerr.strip()[:-1])
                    extraerr = relval * num / 100
                #print "->", bp.binid, extraerr
            return float(extraerr)

        if not self.withcorrelation:
            chi2 = 0.0
            for binprop in sorted(self.tunedata.filteredValues()):
                err2 = 0.0
                simbin = binprop.ipol.getBin(self.params)
                ## Reference error
                if self.use_ref_error:
                    err2 += binprop.refbin.getErr()**2
                ## Median MC error
                if self.use_mc_error:
                    err2 += binprop.ipol.medianmcerr**2
                ## The extra "epsilon" fudge factor error
                err2 += (self.epsilon * binprop.refbin.getVal())**2
                err2 += getExtraErr(binprop)**2
                #
                diff = binprop.refbin.getVal() - simbin.getVal()
                chi2 += binprop.weight * diff**2 / err2
            return chi2

        ## If using correlations:
        by_observables = {}
        for binprop in sorted(self.tunedata.filteredValues()):
            obs, bid = binprop.binid.split(":")
            if not obs in by_observables.keys():
                by_observables[obs] = {}
            if bid in by_observables[obs]:
                raise ValueError, "Already had this bin." # pretty strange error
            err2 = 0.0
            simbin = binprop.ipol.getBin(params)
            ## Reference error
            if self.use_ref_error:
                err2 += binprop.refbin.getErr()**2
            ## Median MC error
            if self.use_mc_error:
                err2 += binprop.ipol.medianmcerr**2
            ## The extra "epsilon" fudge factor error
            err2 += (self.epsilon * binprop.refbin.getVal())**2
            err2 += getExtraErr(binprop)**2
            #
            diff = binprop.refbin.getVal() - simbin.getVal()
            by_observables[obs][bid] = {
                "val": binprop.refbin.getVal(),
                "err2": err2,
                "referr2": binprop.refbin.getErr()**2,
                "diff": diff,
                "weight": binprop.weight}

        chi2 = 0.0
        correlations_used = False
        for obs in by_observables.keys():
            # get observable/bin data in numpy-friendly array
            a = sorted(tuple((int(bid),i['val'],i['diff'],i['err2'],i['referr2'],i['weight'])
                             for (bid, i) in by_observables[obs].iteritems()), key=lambda x: x[0])
            a = numpy.array(a)
            bid, val, diff, err2, referr2, weight = numpy.int_(a[...,0]),a[...,1],a[...,2],a[...,3],a[...,4],a[...,5]

            # get correlation matrix... e.g. from file
            if self.withcorrelation in ('minoverlap','minimumoverlap','minimum-overlap'):
                CovM = self.minimumOverlapCovariance(referr2, err2)
            else:
                CovM = self.findCovarianceMatrix(obs, val)

            # suitable correlation matrix
            if (not CovM is None) and CovM.shape[0] == CovM.shape[1] and CovM.shape[0] == len(bid):
                # chi2 = x^{T} * V^{-1} * x... additionally one x gets the weights in here.
                tempChi2 = numpy.dot(numpy.dot(diff,numpy.linalg.inv(CovM)),diff*weight)
                chi2 += tempChi2
                correlations_used = True

            # otherwise: use formula - avoid matrix inversion
            else:
                tempChi2 = numpy.dot(diff**2/err2,weight)
                chi2 += tempChi2

        # if we did not use correlations at all, we can disable them for the
        # following iterations to speedup things
        if not correlations_used:
          self.withcorrelation = False
        return chi2


    def findCovarianceMatrix(self, obsname, binval):
        """
        Reads covariance matrix from file.

        Every line corresponds to one bin in the reference data definition.
        Following form has to be followed:
        uncorr uncertainties --- corr uncertainties
        There can be multiple entries for uncertainties separated by whitespace.
        Remember to separate correlated from uncorrelated unc. by ---.

        The files should be created with prof-lsobs (for correct filename and path)
        and filled afterwards.
        """

        try:
            filename = self.withcorrelation+"/"+obsname[1:].split(":")[0].replace("/","--")
            f = open(filename)
        except:
            return None

        lines_old = 0
        lines = f.read().splitlines()


        if not len(binval) == len(lines):
            return None

        # make sure only single whitespaces within the lines
        while not lines_old == lines:
            lines_old = lines
            lines = map(lambda x: x.replace("  ", " "), lines)
        lines = map(lambda x: x.strip(), lines)

        # parse errors from file
        # numpy should throw a meaningful error whenever the file does
        # not provide same number of errors for every bin.
        all_errors = tuple(tuple(float(u) for u in us.strip().split(" ")) for line in lines for us in line.split("---"))
        uncorr = numpy.array(all_errors[::2])
        corr = numpy.array(all_errors[1::2])

        # ugly but helpful to prevent from singularities for empty bins
        binval[binval==0] = 1.e-10

        binvalues = numpy.outer(binval, binval)
        covM = numpy.zeros(binvalues.shape)

        for u in uncorr.T:
            covM += numpy.diag(u*u)

        for u in corr.T:
            covM += numpy.outer(u,u)

        covM *= binvalues
        return covM


    def minimumOverlapCovariance(self, referr2, err2):
        """
        This method is a first-guess-method if there's no exact information about correlations.
        We assume the covariance between bins i, j to be:

            cov_i,j = min(sigma_i, sigma_j)**2

        This gives a conservative guess of the correlations and uncertainties.

        The method was applied e.g. in CERN-PH-EP-2010-089 (OPAL), arXiv:1101.1470.
        """
        # cov matrix following upper definition
        # only take reference data error for this!
        covM = numpy.minimum(*numpy.meshgrid(referr2,referr2))

        # if  there's additional MC error (already incorporated in err2)
        # add it up
        if not numpy.all(numpy.diag(covM) == err2):
            covM = covM - numpy.diag(numpy.diag(covM)+err2)

        return covM


    def calcNdof(self):
        ## TODO: optimise by doing one loop and caching values?
        sumw = sum(bp.weight for bp in self.tunedata.filteredValues())
        return sumw - len(self.params)



class SingleSimpleIpolChi2(SimpleIpolChi2):
    """ Class for calculating GoF of a single observable.
        Obs is a string with the observable name.
    """

    def __init__(self, tunedata, obs):
        SimpleIpolChi2.__init__(self, tunedata)
        self._obs = obs
        # Lazy cache for the number of bins in `obs'.
        self._numbins = None

        # These are already set by the above call to SimpleIpolChi2.__init__
        # self.params = None
        # self.use_ref_error = True
        # self.use_mc_error = True


    def setObs(self, newobs):
        "Set the observable to calculate the GoF for."
        # Number of bins most likely changes, so we reset it here.
        self._numbins = None
        self._obs = newobs

    obs = property(lambda self: self._obs, setObs,
                   doc="observable path to calculate chi2 for.")


    def getNumBins(self):
        """The number of bins in self.obs."""
        if self._numbins is None:
            self._numbins = len(self.tunedata.getBinProps(self.obs))
        return self._numbins
    numbins = property(getNumBins, doc="Number of bins in observable self.obs")


    def calcChi2(self):
        chi2 = 0.0
        for binprop in self.tunedata.getBinProps(self.obs):
            err2 = 0.0
            simbin = binprop.ipol.getBin(self.params)
            if self.use_ref_error:
                err2 += binprop.refbin.getErr()**2
            if self.use_mc_error:
                err2 += binprop.ipol.medianmcerr**2
            if err2 <= 0.0:
                continue
            diff = binprop.refbin.getVal() - simbin.getVal()
            chi2 += diff**2 / err2
        return chi2


    def calcNdof(self):
        """ This returns the number of bins - number of parameters are
            unaccounted for, should be sensible in case of 1Bin observables.
        """
        return len(self.tunedata.getBinProps(self.obs))


    def calcChi2PerBin(self):
        """Return the chi2 per bin measure."""
        return self.calcChi2()/self.numbins



class SimpleMCChi2(SimpleIpolChi2):
    """Chi2 between MC data from `run' and ref data."""

    def __init__(self, tunedata, run):
        BaseChi2.__init__(self, tunedata)
        self.use_ref_error = True
        self.use_mc_error = False
        self.run = run


    def calcChi2(self):
        chi2 = 0.0
        for binprop in self.tunedata.filteredValues():
            err2 = 0.0
            mcbin = binprop.mcdict[self.run]
            if self.use_ref_error:
                err2 += binprop.refbin.getErr()**2
            if self.use_mc_error:
                err2 += binprop.ipol.medianmcerr**2
            diff = binprop.refbin.getVal() - mcbin.getVal()
            chi2 += binprop.weight * diff**2 / err2
        return chi2


    def setParams(self, *args, **kwargs):
        """Overwrite setParams method of SimpleIpolChi2.

        Overwrite setParams to make programming errors more obvious.
        """
        raise RuntimeError("Method SimpleMCChi2.setParams is a no-op and"
                           " should not be called!")


    def calcNdof(self):
        """Calculate the Ndof as sum of weights."""
        return sum(bp.weight for bp in self.tunedata.filteredValues())



class SingleSimpleMCChi2(SingleSimpleIpolChi2):
    def __init__(self, tunedata, obs, run):
        super(SingleSimpleIpolChi2, self).__init__(tunedata, obs)

        ## Do not use median MC error (interpolations are not necessarily available)
        self.use_mc_error = False

        self.run = run


    def setParams(self, *args, **kwargs):
        """Overwrite setParams method of SimpleIpolChi2.

        Overwrite setParams to make programming errors more obvious.
        """
        raise RuntimeError("Method SimpleMCChi2.setParams is a no-op and"
                " should not be called!")


    def calcChi2(self):
        chi2 = 0.0
        for binprop in self.tunedata.getBinProps(self.obs):
            err2 = 0.0
            mcbin = binprop.mcdict[self.run]
            if self.use_ref_error:
                err2 += binprop.refbin.getErr()**2
            if self.use_mc_error:
                err2 += binprop.ipol.medianmcerr**2
            if err2 <= 0.0:
                continue
            diff = binprop.refbin.getVal() - mcbin.getVal()
            chi2 += diff**2 / err2
        return chi2



## TO BE REWRITTEN

# class RelativeIpolChi2(SimpleIpolChi2):
#     def calcNdof(self):
#         return 1.0

#     def calcChi2(self):
#         relchi2 = 0.0
#         for ref, sim, w in self:
#             relchi2 += w * (ref.getVal() - sim.getVal())**2/ref.getVal()**2
#         return relchi2


# class RelativeMCChi2(RelativeIpolChi2):
#     def __init__(self, tunedata, run):
#         for bp in tunedata.filteredValues():
#             ref = bp.refbin
#             sim = bp.mcdict[run]
#             self.append((ref, sim, bp.weight))

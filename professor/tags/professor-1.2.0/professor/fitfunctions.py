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

__all__ = ["SimpleIpolChi2", "SimpleMCChi2", "SingleSimpleIpolChi2",
           "SingleSimpleMCChi2"]


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
    def __init__(self, tunedata, epsilon=0.0):
        BaseChi2.__init__(self, tunedata)
        self.params = None
        self.epsilon = epsilon
        self.use_ref_error = True
        self.use_mc_error = True
        ## TODO: Remove this in the future.
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
        Set the parameter point.

        Returns self to allow chaining for convenience.
        """
        if type(params) == dict:
            params = ParameterPoint.mkFromDict(params)
        # # elif type(params) == list:
            # # self.params = ParameterPoint(self.tunedata.paramranges.names, params)
        # else:
            # raise TypeError("Unsupported type for argument `params': '%s'!" % type(params))
        self.params = numpy.asarray(params)
        return self


    def calcChi2(self):
        """
        Calculate and return the chi^2 at the currently-set parameter point.

        TODO
        ====

        - Allow on the fly calculation of chi^2 with params given as an argument.
        """
        chi2 = 0.0
        for binprop in self.tunedata.filteredValues():
            err2 = 0.0
            simbin = binprop.ipol.getBin(self.params)
            ## Reference error
            if self.use_ref_error:
                err2 += binprop.refbin.getYErr()**2
            ## Median MC error
            if self.use_mc_error:
                err2 += binprop.ipol.medianmcerr**2
            ## The extra "epsilon" fudge factor error
            ## TODO: I've chosen to multiply the ref value, but could
            ## use the MC value... or both. Hmm!
            err2 += (self.epsilon * binprop.refbin.getYVal())**2
            diff = binprop.refbin.getYVal() - simbin.getYVal()
            chi2 += binprop.weight * diff**2 / err2
        return chi2


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
                err2 += binprop.refbin.getYErr()**2
            if self.use_mc_error:
                err2 += binprop.ipol.medianmcerr**2
            if err2 <= 0.0:
                continue
            diff = binprop.refbin.getYVal() - simbin.getYVal()
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
                err2 += binprop.refbin.getYErr()**2
            if self.use_mc_error:
                err2 += binprop.ipol.medianmcerr**2
            diff = binprop.refbin.getYVal() - mcbin.getYVal()
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

        # do not use mdeian mc error (interpolations are not necessarily
        # available)
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
                err2 += binprop.refbin.getYErr()**2
            if self.use_mc_error:
                err2 += binprop.ipol.medianmcerr**2
            if err2 <= 0.0:
                continue
            diff = binprop.refbin.getYVal() - mcbin.getYVal()
            chi2 += diff**2 / err2
        return chi2



## TO BE REWRITTEN

# class RelativeIpolChi2(SimpleIpolChi2):
#     def calcNdof(self):
#         return 1.0

#     def calcChi2(self):
#         relchi2 = 0.0
#         for ref, sim, w in self:
#             relchi2 += w * (ref.getYVal() - sim.getYVal())**2/ref.getYVal()**2
#         return relchi2


# class RelativeMCChi2(RelativeIpolChi2):
#     def __init__(self, tunedata, run):
#         for bp in tunedata.filteredValues():
#             ref = bp.refbin
#             sim = bp.mcdict[run]
#             self.append((ref, sim, bp.weight))

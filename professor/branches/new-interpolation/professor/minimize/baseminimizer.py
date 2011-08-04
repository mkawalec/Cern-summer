"""baseminimizer.py

"""

import numpy

from professor.tools.decorators import virtualmethod, deprecated

# import our central config/logging module
from professor.tools.config import Config as _conf
_logger = _conf().getLogger('minimize')

class StillGoodMessage(Exception):
    """Exception used during the initilization of the minimizers to
    indicate, that nothing has changed and we don't need to recreate chi^2
    functions and stuff.
    """
    pass


class ValidationFailed(Exception):
    pass


class BaseMinimizer(object):
    """Base class for minimizers defining the interface to use.

    Methods for external use
    ========================
        - __init__: create new minimizer based for given L{TuningData}
          object
        - L{guessMinimum}: takes method for start point selection, choice of
          runs, choice of observables, list of selection functions to apply
          and returns a L{MinimizationResult} instance.
        - L{validateResult}: validata a given result.
    """
    def __init__(self, tuningdata):
        self.__td = tuningdata

        # lists which describe what we want to use for the next minimization
        #
        self.__obs = []
        self.__runs = []

        # list of selection functions which must return True 
        #
        # selection functions must be declared like this:
        # def selection_example(refbin, interpolation):
        #       pass
        #
        self.__selfs = []

        # lists which describe what we used to build the interpolation in
        # __currentdata
        self.__currentobs = None
        self.__currentruns = None
        self.__currentselfs = None


        # the current list with (ref bin, interpolation, BinProps) triples
        self.__currentdata = None

        # a dict of param index (starting with 0) param value to handle
        # fixed parameters
        self.__fixedparams = {}

        # starting point used for minimizations: a plain numpy array
        # it can be configured how it is set
        self.__startpoint = None
        self.__startpointmethod = None

    def getTD(self):
        """Return the TuningData instance."""
        return self.__td

    def getData(self):
        """Return the current SingleTuneData."""
        return self.__currentdata

    def getScaler(self):
        """Return the scaler of the current minimization."""
        return self.__currentdata.scaler

    def setStartpoint(self, method):
        """Sets the starting point for the next minimization.

        uses the data in self.__currentdata for the 'minmc' method. So
        initMinimization must be called before this method is used. To make
        sure that

        @param method: the method how the starting point is found:
            C{center|random|minmc}
                - center: use the center of the scaled parameter space
                - random: use a random point
                - minmc: use the anchor point with the smallest chi^2 value
        @type method: C{string}
        """
        _logger.debug("setting starting point for next minimization:"
                       " '%s'"%(method))
        dim = self.getTD().numberOfParams()
        if method == "center":
            self.__startpoint = .5 * numpy.ones(dim)

        elif method == "random":
            self.__startpoint = numpy.random.rand(dim)

        # elif method == "minmc":
            # def chi2func(pp):
                # r = .0
                # for bin, interp in self.__currentdata:
                    # r += ((bin.getYVal() - interp.getValue(pp))**2
                           # /bin.getYErr()**2)
                # return r

            # minchi2 = 1.e18
            # # the first bin distribution
            # bd = self.__currentdata[0][1].getBD()

            # for apoint, bin_unused in bd:
                # chi2 = chi2func(apoint)
                # _logger.debug("chi^2 = %f for anchor point %s"%(chi2, apoint.getScaled()))

                # if chi2 < minchi2:
                    # minchi2 = chi2
                    # self.__startpoint = apoint.getScaled()
            # _logger.debug("minimal chi^2 = %f"%(minchi2))

        else:
            raise ValueError("Bad value for argument 'method': %s"%(method))
        self.__startpointmethod = method
        _logger.info("new starting point: %s (method: %s)"%(self.__startpoint,
                     self.__startpointmethod))

    def getStartpoint(self):
        return self.__startpoint

    def getStartpointMethod(self):
        return self.__startpointmethod

    def getFixedParameter(self, index):
        """Return scaled value if param #i is fixed, None otherwise."""
        return self.__fixedparams.get(index)


    # this function must/should be overwritten in subclasses but 
    # it must must/should be called via super(...) or similar at the
    # beginning of the suclass's method
    def initMinimization(self):
        """Inits the minimization stuff, if needed.

        Checks if differences exist between wanted and cached run numbers,
        observables and selection functions. If no differences exist a
        StillGoodMessage is raised to stop further initialization in
        subclass methods.

        Must be overwritten in subclasses to set up the concrete data
        structures needed for minimization!
        """
        # check if we need to build a new __currentdata
        stillgood = True

        # order of apperance: runs will most likely be changed
        if self.__currentruns != self.__runs:
            stillgood = False

        if stillgood and self.__currentobs != self.__obs:
            stillgood = False

        if stillgood and self.__currentselfs != self.__selfs:
            stillgood = False

        if self.__currentdata is None:
            stillgood = False

        if stillgood:
            raise StillGoodMessage()

        # build new __currentdata
        _logger.debug("building new __currentdata for minimization")
        _logger.debug("calling getTuneData with runs=%s, obs=%s"%(
                      self.__runs, self.__obs))
        self.__currentdata = self.getTD().getTuneData(self.__currentruns,
                                                      self.__currentobs)

        # apply selection functions
        for sf in self.__selfs:
            sf(self.__currentdata)

        # store copies of the used lists to check the next time, if we need
        # to rebuild __currentdata
        self.__currentselfs = self.__selfs[:]
        self.__currentobs = self.__obs[:]
        self.__currentruns = self.__runs[:]

    @virtualmethod
    def minimize(self):
        """Do the real minimization process. Implement this in subclasses!"""
        pass

    def guessMinimum(self, spmethod, runs=None, obs=None, selfuncs=None):
        """Minimize chi^2 and return a MinimizationResult instance.

        If one of the optional arguments is not None, the corresponding
        internal variable is set to the given value. For the first
        minimization all must not be None!

        runs and obs are passed to L{TuningData.buildBinDistList}
        @param spmethod: the method to set the starting point of the
            minimization. See L{setStartpoint}.
        """

        if runs is not None:
            self.__runs = runs
        if obs is not None:
            self.__obs = obs
        if selfuncs is not None:
            self.__selfs = selfuncs

        # rebuild self.__currentdata and set chi^2 stuff in subclasses,
        # if needed
        try:
            _logger.debug("Trying to rebuild __currentdata...")
            self.initMinimization()
        except StillGoodMessage:
            # nothing was/had to be changed
            # this is no problem
            _logger.debug("__currentdata has not been rebuilt we reuse the"
                " old data.")
            pass
        self.setStartpoint(spmethod)

        # free all parameters
        self.__fixedparams = {}

        _logger.debug("starting minimization...")
        mr = self.minimize()
        _logger.debug("minimization result: %s"%(mr))

        # save the used run numbers, observables and selection functions
        # used for this result
        mr.runs = sorted(self.__currentruns)
        mr.obs = sorted(self.__currentobs)
        mr.selfuncs = sorted(self.__currentselfs)
        mr.spmethod = self.getStartpointMethod()
        # calculate the ndof:
        # ndof = sum_bins( weight_bin ) - npars
        # sumweights = sum((i[2].weight for i in self.getData()))
        sumweights = 0.
        for bp in self.getData().itervalues():
            if not bp.veto:
                sumweights += bp.weight
        mr.ndof = sumweights - self.getScaler().dim()

        return mr

    def validateResult(self, res, paramstofix=None, relchi2acc=1.e-3, relparamacc=1.e-3):
        """Perform checks on given minimization result.

        This does not call initMinimization! Make sure you call it directly
        after guessMinimum.

        Checks performed:
            - fix single parameters and compare the result

        @param res: the MinimizationResult to validate.
        @param paramstofix: list with parameter indices to fix. The
            parameters are fixed one after another. If None all parameters
            are fixed.
        """
        if paramstofix is None:
            paramstofix = xrange(self.getScaler().dim())
        if type(paramstofix) != dict:
            t = {}
            for i in paramstofix:
                t[i] = res.parscaled[i]
            paramstofix = t

        for i, v in paramstofix.iteritems():
            # fix only the ith parameter
            self.__fixedparams = {i:v}
            # and fix only this one to the given value
            # self.__fixedparams[i] = res.parscaled[i]
            checkres = self.minimize()
            if abs(checkres.chi2 - res.chi2)/res.chi2 > relchi2acc:
                raise ValidationFailed("chi^2 differ:"
                        " (%g - %g)/%g > %g"%(checkres.chi2, res.chi2,
                                              res.chi2, relchi2acc))
            if (abs((res.parscaled - checkres.parscaled)/res.parscaled) > relparamacc).any():
                raise ValidationFailed("parameters differ!")
            _logger.debug("validated with fixed parameter #%i (%e)"%(i, v))

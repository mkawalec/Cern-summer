"""baseminimizer.py

"""

import numpy

from professor.tools.decorators import virtualmethod
from professor.tools.errors import ValidationFailed
from professor.tools import log as logging


class BaseMinimizer(object):
    """Base class for minimizers defining the interface to use.

    Methods for external use
    ========================
        - __init__: create new minimizer
        - L{guessMinimum}: Takes method for start point selection, choice of
          runs, choice of observables, list of selection functions to apply
          and returns a L{MinimizationResult} instance.
        - L{validateResult}: Validates a given result.
    """
    def __init__(self):
        self.gof = None

        # a dict of param index (starting with 0) param value to handle
        # fixed parameters
        self.__fixedparams = {}
        self.__limits = {}

        # starting point used for minimizations: a plain numpy array
        # it can be configured how it is chosen
        self.__startpoint = None
        self.__startpointmethod = None

    def setStartpoint(self, method="random", manual=None):
        """Sets the starting point for the next minimization.

        uses the data in self.__currentdata for the 'minmc' method. So
        initMinimization must be called before this method is used. To make
        sure that

        @param method: the method how the starting point is found:
            C{center|random|manual}
                - center: use the center of the scaled parameter space
                - random: use a random point
                - manual: use values given in argument manual. manual must
                          not be C{None}! See description of manual below.
        @type method: C{string}
        @param manual: Use the values in here for starting points. Ignored
            if method is not "manual". Can be either a list/numpy.array with
            scaled values or a dict with parameter name - *unscaled* value
            pairs. If it's a list/numpy.array it must have the correct
            dimension. If it's a dict parameters not set in it will be
            chosen randomly. Keys are parameter names, e.g. PARJ(41).
        """
        logging.debug("setting starting point for next minimization:"
                       " '%s'"%(method))
        dim = self.gof.tunedata.numParams()
        if method == "center":
            self.__startpoint = .5 * numpy.ones(dim)
        elif method == "random":
            self.__startpoint = numpy.random.rand(dim)
        elif method == "manual":
            if type(manual) == list:
                if len(manual) != dim:
                    ValueError("Given list of manual start point values has"
                            " wrong dimension: %s"%(manual))
                self.__startpoint = numpy.ndarray(manual)
            elif type(manual) == numpy.ndarray:
                if manual.shape != (dim,):
                    ValueError("Given ndarray of manual start point values has"
                            " wrong shape: %s"%(manual))
                self.__startpoint = manual.copy()
            elif type(manual) == dict:
                sca = self.gof.tunedata.scaler
                rand = numpy.random.rand(dim)
                unscaled = numpy.NaN * numpy.zeros(dim)
                for pname, pval in manual.iteritems():
                    i = sca.getIndex(pname)
                    unscaled[i] = pval
                scaled = sca.scale(unscaled)
                for i, pname in enumerate(sca.getKeys()):
                    if not manual.has_key(pname):
                        scaled[i] = rand[i]
                self.__startpoint = scaled
            else:
                TypeError("Given argument manual of wrong type: %s"%(manual))
        else:
            raise ValueError("Bad value for argument 'method': %s"%(method))

        self.__startpointmethod = method
        logging.info("new starting point: %s (method: %s)"%(self.__startpoint,
                     self.__startpointmethod))

    def getStartpoint(self):
        """Return the current start point as numpy array.

        Takes care that values for fixed parameters are set correctly in the
        returned start point.
        """
        sp = self.__startpoint.copy()
        for pname, val in self.__fixedparams.iteritems():
            i = self.gof.tunedata.scaler.getIndex(pname)
            sp[i] = val
        return sp

    def getStartpointMethod(self):
        return self.__startpointmethod

    def getFixedParameter(self, parname):
        """Return scaled value if param parname is fixed, None otherwise."""
        return self.__fixedparams.get(parname)

    def getAllFixedParameters(self):
        """Return a list of all fixed parameters."""
        return self.__fixedparams.keys()

    def getParameterLimits(self, parname):
        """Return scaled parameter limits if #i has limits, None otherwise."""
        return self.__limits.get(parname)

    def getLimitedParameters(self):
        """Return a list of all limited parameters."""
        return self.__limits.keys()


    # this function must/should be overwritten in subclasses but
    # it must must/should be called via super(...) or similar at the
    # beginning of the suclass's method
    #
    # In the subclasses this function builds the minimization data
    # structures, e.g. it builds the chi^2 function to use. This should take
    # care of fixed parameters!
    def initMinimization(self):
        """Empty function.
        Perhaps we can put some code in here in the future.
        """
        pass

    @virtualmethod
    def minimize(self):
        """Do the real minimization process. Implement this in subclasses!"""
        pass

    def goffunc(self, params):
        self.gof.setParams(params, scaled=True)
        return self.gof.calcGoF()


    def fixParams(self, fixed, free=True):
        """Fixes params and optionally removes old fixes.

        Should be used only internally. But it's made public for fine
        tuning. It depends on that the current SingleTuneData instance in
        self.tunedata is valid and used for the next minimizations!

        @param fixed: dictionary with parameter name - unscaled value pairs
        """
        if free:
            self.__fixedparams = {}
        sca = self.gof.tunedata.scaler

        # temporary storage for fixed parameters
        fixparunscaled = numpy.NaN * numpy.zeros(sca.dim())
        # logging.debug("fixparunscaled before filling: %s"%(fixparunscaled))

        for pname, unscaledval in fixed.iteritems():
            i = sca.getIndex(pname)
            fixparunscaled[i] = unscaledval
        logging.debug("fixparunscaled after filling for %s: %s"%(fixed,
            fixparunscaled))
        fixparscaled = sca.scale(fixparunscaled)
        logging.debug("using fixparscaled: %s"%(fixparscaled))
        for pname in fixed.iterkeys():
            i = sca.getIndex(pname)
            self.__fixedparams[pname] = fixparscaled[i]
        logging.debug("fixed parameters unscaled(%s) -> scaled(%s)"%(fixed, self.__fixedparams))
        logging.info("Fixed parameters %s"%(fixed))

    def setLimits(self, limits):
        """
        limits  -- {pname => (low, high)} dict with limits.
        """
        sca = self.gof.tunedata.scaler
        # temporary storage for parameters to set limits for
        limlow  = numpy.NaN * numpy.zeros(sca.dim())
        limhigh = numpy.NaN * numpy.zeros(sca.dim())
        for k, v in limits.iteritems():
            i = sca.getIndex(k)
            limlow[i]  = min(v)
            limhigh[i] = max(v)

        low_scaled  = sca.scale(limlow)
        high_scaled = sca.scale(limhigh)
        for pname in limits.iterkeys():
            i = sca.getIndex(pname)
            self.__limits[pname] = (low_scaled[i], high_scaled[i])
        logging.debug("Scaled parameter limits %s" % str(self.__limits))

    def guessMinimum(self, gof, spmethod="center", manualsp=None,
            fixedpars=None, limits=None):
        """Minimize chi^2 and return a MinimizationResult instance.

        The following work is done:
            1. Update self.gof.
            2. Set startpoint method and optionally manual values.
            3. Fix parameters (optionally).
            4. Set up minimizer via initMinimization.
            5. Minimize and store relevant information (e.g. used runs,
                observables) in the MinimizationResult.

        @param tunedata: the SingleTuneData instance used for tuning.
        @param spmethod: the method to set the starting point of the
            minimization. See L{setStartpoint}.
        @param manualsp: values for manually setting starting point. See
            L{setStartpoint}.
        @param fixedpars: dictionary with parameter name - unscaled value
            pairs used to fix parameters during minimization.
        @param returnSTD: if true, return value is a tuple
            (MinimizationResult, SingleTuneData)
        """
        self.gof = gof
        self.setStartpoint(spmethod, manual=manualsp)
        # fix parameters if wanted or free all fixed parameters
        if fixedpars is not None:
            self.fixParams(fixedpars, free=True)
        else:
            self.__fixedparams = {}

        if limits is not None:
            self.setLimits(limits)
        else:
            self.__limits = {}

        self.initMinimization()

        logging.debug("Starting minimisation...")
        mr = self.minimize()
        logging.debug("Finished minimisation.")

        # save the used run numbers, observables used for this result
        mr.runs = sorted(self.gof.tunedata.runnums)
        mr.obs = sorted(self.gof.tunedata.observables)
        mr.spmethod = self.getStartpointMethod()

        return mr


    def guessMinimumLegacy(self, gof, spmethod="center", returnSTD=False):
        """Minimize chi^2 and return a MinimizationResult instance.

        If one of the optional arguments is not None, the corresponding
        internal variable is set to the given value. For the first
        minimization all must not be None!

        @param spmethod: the method to set the starting point of the
            minimization. See L{setStartpoint}.
        @param returnSTD: if true, return value is a tuple
            (MinimizationResult, SingleTuneData)
        """
        self.gof.tunedata = gof
        self.setStartpoint(spmethod)

        # free all parameters
        self.__fixedparams = {}

        self.initMinimization()

        logging.debug("starting minimization...")
        mr = self.minimize()
        logging.debug("minimization result: %s" % mr)

        # save the used run numbers, observables used for this result
        mr.runs = sorted(self.gof.tunedata.getRunNums())
        mr.obs = sorted(self.gof.tunedata.getObservables())
        mr.spmethod = self.getStartpointMethod()

        if returnSTD:
            return mr, gof
        else:
            return mr

    def validateResult(self, minres, paramstofix=None, relgofacc=1e-3, relparamacc=1e-3):
        """Perform checks on given minimization result.

        This does not call initMinimization! Make sure you call it directly
        after guessMinimum.

        Checks performed:
            - fix each parameter and compare the result

        @param minres: the MinimizationResult to validate.
        @param paramstofix: list with parameter indices to fix or a dict
            mapping parameter index to parameter value. If it's a list the
            paramters are fixed to the values in minres. The parameters are
            fixed one after another. If None all parameters are fixed.
        """
        if paramstofix is None:
            paramstofix = xrange(self.gof.tunedata.scaler.dim())
        if type(paramstofix) != dict:
            t = {}
            for i in paramstofix:
                t[i] = minres.parscaled[i]
            paramstofix = t

        for i, v in paramstofix.iteritems():
            # fix only the ith parameter
            self.__fixedparams = {i:v}

            # update the underlying minimizers data structures and minimize
            self.initMinimization()
            checkres = self.minimize()

            if abs(checkres.gof - minres.gof)/minres.gof > relgofacc:
                raise ValidationFailed("chi^2 differ:"
                                       " (%g - %g)/%g > %g"%(checkres.gof, minres.gof, minres.gof, relgofacc))
            paramacc = abs( (minres.parscaled - checkres.parscaled)/minres.parscaled )
            if (paramacc > relparamacc).any():
                raise ValidationFailed("Parameters differ!")
            logging.debug("Validated with fixed parameter #%i (%e)" % (i, v))

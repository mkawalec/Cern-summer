"""
Defines base class for numerical minimisers used to optimise fits to ref data.
"""

import numpy

from professor.tools.decorators import virtualmethod
from professor.tools.errors import ValidationFailed
from professor.tools import log as logging
from professor.params import ParameterPoint


class BaseMinimizer(object):
    """Base class for minimizers defining the interface to use.

    Methods for external use:

    `__init__`
        create new minimizer

    `guessMinimum`
        Takes a GoF object and optimizes the GoF. A `MinimizationResult` is returned.

     `validateResult`
        Validate a given result.
    """

    def __init__(self):
        self.gof = None

        ## A dict of param index (starting with 0) param value to handle
        ## fixed parameters
        self.__fixedparams = {}
        self.__limits = {}

        ## Starting point used for minimizations (a ParameterPoint instance)
        ## it can be configured how it is chosen
        self.__startpoint = None
        self.__startpointmethod = None


    ## Start point code
    def setStartpoint(self, method="random", manualsp=None):
        """Sets the starting point for the next minimization.

        Parameters
        ----------
        method : ("center", "random", "manual")
            How to set the start point::
            "center"
                Use the center of the hyper cube spanned by the MC runs.
            "random"
                Use a random point from hyper cube spanned by the MC runs.
            "manual"
                Use values given in argument manual. manual must not be
                `None`! See description of manual below.
        manualsp : ParameterPoint, dict, array_like
            The start point for the "manual" method.
        """
        logging.debug("setting starting point for next minimization:"
                       " '%s'"%(method))
        # short cut
        ranges = self.gof.tunedata.paramranges

        if method == "center":
            self.__startpoint = ranges.center
        elif method == "random":
            self.__startpoint = ranges.getRelativePoint(numpy.random.rand(ranges.dim))
        elif method == "manual":
            if type(manualsp) == dict:
                manualsp = ParameterPoint.mkFromDict(manualsp)
            elif type(manualsp) == list or type(manualsp) == numpy.ndarray:
                manualsp = ParameterPoint(ranges.names, manualsp)
            elif type(manualsp) != ParameterPoint:
                TypeError("Given argument manualsp of wrong type: %s" % manualsp)

            # Fill missing parameter values with random values.
            if manualsp.dim < ranges.dim:
                t = ranges.getRelativePoint(numpy.random.rand(ranges.dim))
                for name in manualsp.names:
                    try:
                        t[name] = manualsp[name]
                    except ValueError:
                        raise ValueError("Manual start point contains bad parameter name '%s'!" % name)
                manualsp = t

            self.__startpoint = manualsp

        else:
            raise ValueError("Bad value for argument 'method': %s" % (method))

        self.__startpointmethod = method
        logging.info("New starting point (method=%s):\n%s" % (self.__startpointmethod, self.__startpoint))


    def getStartpoint(self):
        """Return the current start point.

        Takes care that values for fixed parameters are set correctly in the
        returned start point.

        Returns
        -------
        sp : ParameterPoint
        """
        sp = self.__startpoint.copy()
        for name, val in self.__fixedparams.iteritems():
            sp[name] = val
        return sp


    @property
    def startpointmethod(self):
        return self.__startpointmethod


    ## Parameter limiting
    def getParameterLimits(self, parname):
        """Return the limits for one parameter.

        Raises
        ------
        KeyError
            If no limits are set for `parname`.
        """
        return self.__limits[parname]


    @property
    def limitedparameters(self):
        """Return a list of all limited parameters."""
        return self.__limits.keys()


    def limitParams(self, limits, clear=True):
        """Set parameter limits.

        Parameters
        ----------
        limits : dict, ParameterPoint
            {pname => (low, high)} dict with limits.
        clear : bool, optional
            Clear all previously set limits (default).
        """
        if clear:
            self.__limits.clear()
        self.__limits.update(limits)
        logging.debug("Updated parameter limits: %s" % (self.__limits))


    ## Parameter fixing
    def getFixedParameter(self, parname):
        """Return a fixed parameter value.

        Raises
        ------
        KeyError
            If `parname` is not fixed.
        """
        return self.__fixedparams[parname]


    @property
    def fixedparameters(self):
        """Return the names of fixed parameters."""
        return self.__fixedparams.keys()


    def fixParams(self, fixed, free=True):
        """Fixes params and optionally removes old fixes.

        Should be used only internally. But it's made public for fine
        tuning. It depends on that the current SingleTuneData instance in
        self.tunedata is valid and used for the next minimizations!

        Parameters
        ----------
        fixed : dict, ParameterPoint
            The fixed parameter values.
        free : bool, optional
            Free all previously fixed parameters before fixing new parameters.
        """
        if free:
            self.__fixedparams.clear()
        self.__fixedparams.update(fixed)
        # logging.debug("Updated fixed parameters: %s" % (self.__fixedparams))
        logging.info("Fixed parameters: %s" % ", ".join("%s=%e" % (k,v) for k,v in self.__fixedparams.iteritems()))


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
    def _minimize(self):
        """Do the real minimization process. Implement this in subclasses!"""
        pass


    def goffunc(self, params):
        self.gof.setParams(params)
        return self.gof.calcGoF()


    def minimize(self, gof, spmethod="center", manualsp=None,
                 fixedpars=None, limits=None):
        """Minimize GoF and return a MinimizationResult instance.

        The following work is done:
            1. Update self.gof.
            2. Set startpoint method and optionally manual values.
            3. Fix parameters (optionally).
            4. Set up minimizer via initMinimization.
            5. Minimize and store relevant information (e.g. used runs,
                observables) in the MinimizationResult.

        Parameters
        ----------
        gof
            The goodness of fit data that is to be optimized.
        spmethod : str, optional
            The start point method. See: `setStartpoint`.
        manualsp : ParameterPoint, dict, array_like
            The start point for the "manual" method.
        fixedpars : dict, ParameterPoint
            Parameters to fix during minimization.
        limits : dict, ParameterPoint
            Parameter limits.
        """
        self.gof = gof
        self.setStartpoint(spmethod, manualsp=manualsp)
        ## Fix parameters if wanted or free all fixed parameters
        if fixedpars is not None:
            self.fixParams(fixedpars, free=True)
        else:
            self.__fixedparams.clear()

        if limits is not None:
            self.limitParams(limits, clear=True)
        else:
            self.__limits.clear()

        self.initMinimization()

        logging.debug("Starting minimisation...")
        mr = self._minimize()
        logging.debug("Finished minimisation.")

        for name in self.fixedparameters:
            mr.setFixed(name)
        for name in self.limitedparameters:
            mr.setLimits(name, self.getParameterLimits(name))
        mr.startpointmethod = self.startpointmethod
        mr.ipolmethod = self.gof.tunedata.ipolmethod

        return mr


    def validateResult(self, minres, paramstofix=None, relgofacc=1e-3, relparamacc=1e-3):
        """Perform checks on given minimization result.

        Checks performed:
            - fix each parameter and compare the result with `minres`

        Parameters
        ----------
        minres : MinimizationResult
            The result to validate.
        paramstofix : {list, dict}, optional
            List with parameter indices to fix or a dict
            mapping parameter index to parameter value. If it's a list the
            paramters are fixed to the values in minres. The parameters are
            fixed one after another. If None all parameters are fixed.
        """
        if paramstofix is None:
            paramstofix = xrange(self.gof.tunedata.scaler.dim())
        if type(paramstofix) != dict:
            t = {}
            for i in paramstofix:
                t[i] = minres.values[i]
            paramstofix = t

        for i, v in paramstofix.iteritems():
            # fix only the ith parameter
            self.fixParams({i : v})

            # update the underlying minimizers data structures and minimize
            self.initMinimization()
            checkres = self._minimize()

            if abs(checkres.gof - minres.gof)/minres.gof > relgofacc:
                raise ValidationFailed("chi^2 differ:"
                                       " (%g - %g)/%g > %g" % (checkres.gof, minres.gof, minres.gof, relgofacc))
            paramacc = abs( (minres.values - checkres.values)/minres.values )
            if (paramacc > relparamacc).any():
                raise ValidationFailed("Parameters differ!")
            logging.debug("Validated with fixed parameter #%i (%e)" % (i, v))

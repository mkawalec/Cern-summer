"""
Definition of data objects returned from a GoF minimization.

The MinimizationResult class is the type of object returned from the Minimizer
object, and the ResultList class is used to handle a collection of
MinimizationResults.
"""

import os
import numpy

from professor.tools.persistency import pickle
from professor.tools import sorting, stats, eigen
from professor.tools.errors import ResultError
from professor.tools.decorators import deprecated
import professor.tools.log as logging
from professor.params import ParameterPoint, ParameterErrors


class ParameterTune(ParameterPoint):
    """
    A slightly specialised parameter set container, with extra attributes for
    storing information relevant to a tune such as the MC runs included and the
    observables used.
    """

    # def __init__(self, paramnames, params, runs=None, obs=None):
        # super(ParameterTune, self).__init__(paramnames, params)
        # self._runs = runs
        # self._obs = obs

    def __new__(cls, names, values, runs=None, obs=None):
        new = ParameterPoint.__new__(cls, names, values)
        new = new.view(type=cls)
        new._runs = runs
        new._obs = obs
        return new


    @classmethod
    def mkFromDict(cls, d, runs=None, obs=None):
        # split (key, value) pairs in two lists
        names, values = zip(*d.items())
        return cls(names, values, runs, obs)


    def __array_finalize__(self, obj):
        super(ParameterPoint, self).__array_finalize__(obj)
        self._runs = getattr(obj, "_runs", None)
        self._obs = getattr(obj, "_obs", None)


    # Implement the pickle protocol
    def __reduce__(self):
        obj_state = list(super(ParameterTune, self).__reduce__())
        sub_state = (self._runs, self._obs)
        obj_state[2] = (obj_state[2], sub_state)
        return tuple(obj_state)


    def __setstate__(self, state):
        obj_state, sub_state = state
        super(ParameterTune, self).__setstate__(obj_state)

        runs, obs = sub_state
        self._runs = runs
        self._obs = obs


    # def __str__(self):
        # r = str()
        # # if self.runs:
        # #     r += "Made using runs: %s\n" % self.runs
        # # if self.obs:
        # #     r += "Made using observables: %s\n" % self.obs
        # r += super(ParameterTune, self).__str__()
        # return r.strip()


    def setRuns(self, runs):
        self._runs = sorted(runs)
    runs = property(lambda s: s._runs, setRuns)


    def setObs(self, obs):
        self._obs = sorted(obs)
    obs = property(lambda s: s._obs, setObs)


class MinimizationResult(object):
    """Container for minimization results.

    Attributes
    ----------
    names : tuple of str, inherited from ParameterPoint
        The parameter names.
    dim : int, inherited from ParameterPoint

    runs : list, inherited from ParameterTune, optional
    obs : list, inherited from ParameterTune, optional

    gof : float
        The GoF estimate.
    ndof : float
        The number of degrees of freedom.
    values : ParameterTune
        The tuned parameter values.
    errors : ParameterErrors, optional
        The estimated parameter uncertainties of the minimum.
    covariance : ParameterMatrix, optional
        The estimated parameter covariance matrix at the minimum.
        Note: fixed parameters are *not* included with dummy values.

    startpointmethod : str, optional
        The start point method used.
    ipolmethod : class, optional
        The interpolation method used.
    """
    def __init__(self, gof, ndof, values, errors=None, covariance=None):
        """
        Parameters
        ----------
        gof : float
            The GoF estimate.
        ndof : float
            The number of degrees of freedom.
        values : ParameterTune
            The tuned parameter values (together with the used runs and
            observables).
        errors : ParameterErrors, optional
            The estimated parameter uncertainties of the minimum.
        covariance : ParameterMatrix, optional
            The estimated parameter correlations at the minimum.
        """
        self._gof = gof
        self._ndof = ndof

        self.values = values
        if errors is not None:
            if not isinstance(errors, ParameterErrors):
                raise TypeError("Errors must be of type ParameterErrors!")
            elif errors.names != values.names:
                raise ValueError("Values and errors have different parameter names!")
        self.errors = errors
        self.covariance = covariance
        # set of ints that correspond to the parameter index
        self._fixed = set()
        # param name => (low, high)
        self._limited = dict()

        self.startpointmethod = None
        self.ipolmethod = None

        # Now stored in `values`
        # self._runs = runs
        # self._obs = obs
    gof = property(lambda s: s._gof)
    ndof = property(lambda s: s._ndof)

    ## Set up some pass-through functions/attributes.
    ## Note: We cannot set these conveniently in __init__ because this
    ## breaks pickling.
    def getIndex(self, name):
        return self.values.getIndex(name)

    @property
    def names(self):
        return self.values.names

    @property
    def dim(self):
        return self.values.dim

    def setRuns(self, runs):
        self.values.runs = runs
    runs = property(lambda s: s.values.runs, setRuns)

    def setObs(self, obs):
        self.values.obs = obs
    obs = property(lambda s: s.values.obs, setObs)

    def setFixed(self, idx):
        """
        Parameters
        ----------
        idx : str, int
            Parameter name or index
        """
        if type(idx) != int:
            idx = self.getIndex(idx)

        self._fixed.add(idx)
        # Update error for fixed parameters.
        self.errors[idx] = [0., 0.]


    @property
    def fixedparameters(self):
        """Get the names of fixed parameters."""
        return [self.names[i] for i in self._fixed]


    def setLimits(self, param, limits):
        if param not in self.names:
            raise ValueError("unknown parameter name '%s'" % param)
        self._limited[param] = limits


    def getLimits(self, param):
        return self._limited[param]

    @property
    def limitedparameters(self):
        return self._limited.keys()

    @property
    def freeparameters(self):
        freeparams = set(self.names)
        freeparams.difference_update(self.fixedparameters)
        return sorted(freeparams)

    def inBounds(self, bounds):
        """ Return true if MinResult is inside parameter bounds """
        for num, b in enumerate(bounds):
            if self.values[num] < min(b) or self.values[num] > max(b):
                return False
        return True



    def __str__(self):
        r = str()
        if self.ipolmethod:
            r += "Ipol method: %s\n" % self.ipolmethod.method
        if self.gof:
            r += "Goodness of fit: %s\n" % self.gof
        if self.ndof:
            r += "Ndf: %i\n" % self.ndof
        W = max(map(len, self.names))
        W = max(5, W)
        r += "Param".ljust(W) + "  Value\n"
        for n in self.names:
            r += n.ljust(W)
            r += "  %e" % (self.values[n])
            if n in self.fixedparameters:
                r += "  (fixed)"
            elif self.errors is not None:
                r += "  -%e  +%e" % (self.errors[n, "low"],
                                     self.errors[n, "high"])
            r += "\n"
        return r[:-1]



## Keep this for later reference:

# TODO: Remove
class MinimizationResultOLD(ParameterTune):
    """
    Minimization result container.

    Data stored (type)
    ==================
        - resulting GoF  (float)
        - resulting Ndof  (float)
        - parameter point (1D-numpy.array)

        - parameter errors* (2D-numpy.array)
          indices are:
            - 0: parameter index(=dimension),
            - 1: low/high error
          e.g. to get the lower unscaled error for param #2 you would use:

            >>> minresult.errunscaled[1,0]

          lower+upper errors are positive
        - covariance matrix* (dictionary)

        - used run numbers* (sorted list of strings)
        - used observables*  (sorted list of strings)
        - used start point method* (string)
        - used interpolation method* (string)

        - names of fixed parameters* (set of strings)
        - flag if any parameter was limited* (bool)
        - flag if result is in region of extrapolation* (bool)
        - flag if result is at edge of limit range* (bool)


        *: this data is optional (defaults to None)

    Array layout
    ============
    Parameters and errors are stored scaled and unscaled:
     - (par|err)scaled
     - (par|err)unscaled

    Instance creation
    =================
        - L{withScaler}: create an instance from scaled parameters and a
          L{Scaler} instance. This is used after a minimization is performed
          to turn the scaled parameters and errors to unscaled values. Used
          in L{BaseMinimizer.minimize}.
        - __init__ itself should not be needed.

    TODOs
    =====

     - Can we remove all reference to scalers, please? Maybe subclass to include
       scaled params if they are really, *really* wanted?

     - Inherit from ParameterPoint, once tidied.

     - Wherever scalers go to, they should use the inherited
       ParameterPoint._scaled property, rather than duplicating it with
       self.parscaled

    """

    @classmethod
    def mkInstanceWithScaler(cls, gof, ndof, scaler, parscaled, **kwargs):
        """
        Create a MinimizationResult from a L{Scaler} and an array of scaled
        parameters.
        """

        ## Unscale scaled params
        parunscaled = scaler.descale(parscaled)

        ## Debug print-out
        msg = "Creating MinimizationResult:\n"
        msg += "  scaler: %s\n" % scaler
        msg += "  scaled values: %s\n" % parscaled
        msg += "  unscaled values: %s\n" % parunscaled
        msg += "  kwargs: %s" % kwargs
        logging.debug(msg)

        errunscaled = None
        if kwargs.has_key("errscaled"):
            errscaled = kwargs["errscaled"]
            t = -1. * numpy.ones((scaler.dim(), 2))
            errunscaled = -1.0 * numpy.ones((scaler.dim(), 2))
            for i, errs in enumerate(errscaled):
                t[i] = numpy.array(errs)
            if (t < 0).any():
                raise ValueError("Negative errors make no sense!")
            tmin = scaler.getMinVals()
            tmax = scaler.getMaxVals()
            tdiff =  tmax - tmin
            errunscaled[:,0] = t[:,0] * tdiff
            errunscaled[:,1] = t[:,1] * tdiff
            errscaled = t
            del kwargs["errscaled"]

        new = cls(gof, ndof, scaler, parscaled, parunscaled)

        if errunscaled is not None:
            new.errunscaled = errunscaled
            new.errscaled = errscaled
        for k, val in kwargs.items():
            if hasattr(new, k):
                setattr(new, k, val)
            else:
                raise AttributeError("MinimizationResult has no attribute '%s'!" % k)
        return new


    def __init__(self, gof, ndof, scaler, parscaled, parunscaled, runs=None, obs=None):
        super(MinimizationResult, self).__init__(scaler.getKeys(), parunscaled, runs, obs)
        self.gof = gof
        self.ndof = ndof
        self.parscaled = numpy.array(parscaled)

        self.scaler = scaler

        ## A set with the names of fixed parameters
        self.fixedparams = set()

        ## Optional attributes
        self.errscaled = None
        self.errunscaled = None
        self.covariance = None

        self.spmethod = None
        self.ipolmethod = None

        ## Optional flags
        self.f_extrapolation = False
        self.f_limits = False
        self.f_hitlimit = False


    def setOutsideFlag(self):
        self.f_extrapolation = True


    def setLimitUsedFlag(self):
        self.f_limits = True


    def setHitLimitFlag(self):
        self.f_hitlimit = True


    def setFixedFlag(self, param):
        "Add param to the list of fixed parameters."
        if param not in self.getKeys():
            raise ValueError("Cannot mark unknown parameter '%s' as"
                             " fixed!" % (param))
        if type(self.fixedparams) == set:
            self.fixedparams.add(param)
        else:
            self.fixedparams[param] = True


    def getFixedParameters(self):
        if type(self.fixedparams) == set:
            return self.fixedparams
        else:
            return set(self.fixedparams.keys())


    def __str__(self):
        r = str()
        if self.ipolmethod:
            r += "Ipol method: %s\n" % type(self.ipolmethod).__name__
        if self.gof:
            r += "Goodness of fit: %s\n" % self.gof
        if self.ndof:
            r += "Ndf: %i\n" % self.ndof
        r += super(MinimizationResult, self).__str__()
        return r.strip()


    def asDict(self, scaled=True, include_errors=False):
        """
        Return minimization result as a simple dictionary.

        TODO: Remove or move scaled stuff away.
        """
        temp = dict.fromkeys(self._keys)
        for param in self._keys:
            if scaled:
                v = self.parscaled[self.getIndex(param)]
                if include_errors:
                    e_low = self.errscaled[self.getIndex(param)][0]
                    e_high= self.errscaled[self.getIndex(param)][1]
                    temp[param] = [v, e_low, e_high]
                else:
                    temp[param] = v
            else:
                v = self.parunscaled[self.getIndex(param)]
                if include_errors:
                    e_low = self.errunscaled[self.getIndex(param)][0]
                    e_high= self.errunscaled[self.getIndex(param)][1]
                    temp[param] = [v, e_low, e_high]
                else:
                    temp[param] = v
        return temp


    def asFlat(self, fname, scaled=False, include_errors=True):
        """
        Write minimization result to a flat file 'fname'.
        """
        f = open(fname, 'w')
        d = self.asDict(scaled=scaled, include_errors=include_errors)
        for k in self.getKeys():
            if include_errors:
                f.write("%s   %e   %e   %e\n" % (k, d[k][0], d[k][1], d[k][2]))
            else:
                f.write("%s   %e\n" % (k, d[k]))
        f.close()
        logging.debug("Written result to %s." % (fname))


    def isInRange(self, rangedict):
        """
        Determine whether minimization result is inside ranges specified via
        rangedict.
        """
        L_s = len(self.keys)
        L_r = len(rangedict.keys())
        if L_s == L_r:
            sharedkeys = [k for k in self.keys if rangedict.has_key(k)]
        elif L_s > L_r:
            sharedkeys = [k for k in rangedict.keys() if k in self.keys]
        else:
            raise ValueError("Given range contains more parameters than were"
                             " used for minimization.")

        MR_d = self.asDict(scaled=False)
        for k in sharedkeys:
            m = min(rangedict[k])
            M = max(rangedict[k])
            if MR_d[k] >= m  and MR_d[k] <= M:
                continue
            else:
                logging.debug("Result not appended due to %s=%.3f" % (k,MR_d[k])
                              + " being outside range (%.3f...%.3f)" % (m,M))
                return False
        return True


    def getFreeParameters(self):
        """
        Return names of all free parameters in a sorted list.
        """
        freeparams = set(self.getKeys())
        freeparams.difference_update(self.getFixedParameters())
        return sorted(freeparams)


    def getCovMatrix(self):
        """
        Return the covariance matrix as a numpy array.

        Use getFreeParameters() to get a list of the free parameters.

        Note
        ====

        Fixed parameters are discarded from the MINUIT output. Therefore the
        number of rows/columns of the covariance matrix differs from the
        number of parameters!

        TODO
        ====

        - Can we add the fixed parameters with trivial covariance, for param array consistency?
        """
        if self.covariance is None:
            raise ResultError("No covariance data stored!")

        freeparams = self.getFreeParameters()

        ## Initialize empty matrix (array) first
        V = numpy.zeros((len(freeparams), len(freeparams)))
        ## Fill yet empty covariance matrix
        for mpnames, v in self.covariance.iteritems():
            # We know MINUIT parameter names are MPxx
            # translate MINUIT parameter indices back to clear-text names
            p0 = self.getKeys()[int(mpnames[0][2:])]
            p1 = self.getKeys()[int(mpnames[1][2:])]
            if p0 in self.fixedparams:
                logging.info("Parameter '%s' was fixed during minimisation!" % p0)
                continue
            elif p1 in self.fixedparams:
                logging.info("Parameter '%s' was fixed during minimisation!" % p1)
                continue
            i0 = freeparams.index(p0)
            i1 = freeparams.index(p1)
            logging.debug("[%s -> %s -> %i], [%s -> %s -> %i] = %e" %
                          (mpnames[0], p0, i0, mpnames[1], p1, i1, v))
            V[i0,i1] = v
        return V


    def getCorrelMatrix(self):
        # code copied from numpy
        c = self.getCovMatrix()
        try:
            d = numpy.diag(c)
        except ValueError: # scalar covariance
            return 1
        return c/numpy.sqrt(numpy.multiply.outer(d,d))


    def setIpolMethod(self, method):
        self.ipolmethod = method


    def getIpolMethod(self):
        return self.ipolmethod


    def isInKsigmaEllipsisOfM0(self, m0, k=1):
        """
        Decide whether this minimization result is inside the k-sigma ellipsis of
        the MinimizationResult m0.

        TODO: Move to eigen, or similar: it's better as a non-member function, I
        think, and is crowding the MR interface.
        """
        c0 = m0.getCovMatrix()
        t_transp, s, t = eigen.eigenDecomposition(c0)
        p0 = list(eigen.transformParameter(m0.parunscaled, t_transp))
        p1 = list(eigen.transformParameter(self.parunscaled, t_transp))

        ellipsis = 0.0
        for n, sigq in enumerate(s):
            ellipsis += (p1[n] - p0[n])**2/(2*sigq)

        if ellipsis <= 0.5*k**2:
            return True
        else:
            return False


##################################


# TODO: clean the interface. Do we need all these methods?

class ResultList(list):
    """
    Container class for storing list of MinimizationResults.

    It is expected that all results were created with the same set of
    observables (and weighting).

    Usage examples::

    creating empty instance:

        >>> results = ResultList()

    adding a MinimizationResult:
        >>> results.append(minresult)

    writing filled list to xml file:
        >>> results.write("path/to/results.xml")

    creating instance from pickle file:
        >>> results = ResultList.mkFromPickle("path/to/results.pkl")

    TODOs
    -----
     - Superclass to handle general {ParameterSet}s.
    """


    @classmethod
    def mkFromPickle(cls, path):
        f=open(path)
        rlist = pickle.load(f)
        f.close()
        return rlist

    @classmethod
    @deprecated("ResultList.mkFromPickle")
    def fromPickle(cls, path):
        return cls.mkFromPickle(path)


    @classmethod
    def mkFromDirectory(cls, directory='.', identifier='results'):
        """ Create a ResultList instance from all identifier*.pkl files
            found in the directory specified via directory
            NOTE: you need to know what you are doing here, validation is
            switched of here!
        """
        ## Find all the suitable xml files in the directory first.
        resultfiles = [f for f in os.listdir(directory)
                       if f.endswith('.pkl') and f.startswith(identifier)]

        ## Iterate over all files and store each MinimizationResult in a list.
        results = []
        for f in resultfiles:
            for mr in cls.mkFromPickle(f):
                results.append(mr)
        return cls(results, validate=False)

    @classmethod
    @deprecated("ResultList.mkFromDirectory")
    def fromDirectory(cls, path):
        return cls.mkFromDirectory(path)


    def write(self, outfile):
        """
        Write MinimizationResults as pickle/cPickle object to outfile

        """
        f = open(outfile,"w")
        pickle.dump(self, f)
        f.close()


    def __init__(self, results=None, validate=True):
        if results is None:
            super(ResultList, self).__init__()
        else:
            super(ResultList, self).__init__(results)

        if validate:
            self.isValid()


    def __str__(self):
        if not len(self) == 0:
            r = "Summary of %i minimization results:\n" % len(self)
            for param in sorted(self.getParamNames(), cmp=sorting.cmpByInt):
                w_mean, w_err = self.mean(param)
                r += "%s %e +- %e (%.3f %%)\n" % \
                    (param.ljust(30), w_mean, w_err, 100 * float(w_err/w_mean))
            return r
        else:
            return "ResultList instance is empty!"


    @deprecated("Is this used/should this be kept?")
    def getMinimum(self):
        """Return result that yields the smallest GoF value """
        def gof(mr):
            return mr.gof
        return min(self, key=gof)


    @deprecated("Is this used/should this be kept?")
    def getUnique(self, goftol=1.e-10, paramtol=None):
        """Returns a ResultList instance with only one result per choice of
        runs.

        Fails if results for the same choice of runs differ.

        @param goftol: absolute tolerance for GoF values.
        @param paramtol: list/array with absolute parameter tolerance values.
            If C{None} 1e-10 for all parameters.
        @raises ValueError: if results for the same choice of runs differ.
        """
        # dictionary mapping run numbers to results
        uniq = {}
        if paramtol is None:
            paramtol = 1.e-10 * numpy.ones(self[0].dim())
        for res in self:
            key = ''.join(sorted(res.runs))
            if not uniq.has_key(key):
                uniq[key] = res
                continue
            cmpres = uniq[key]
            if abs(cmpres.gof - res.gof) >= goftol:
                msg = "GoF for runs '%s' differs too much: " % res.runs
                msg += "%r vs. %r" % (res.gof, cmpres.gof)
                raise ValueError(msg)
            for i, ptol  in enumerate(paramtol):
                if abs(cmpres.parunscaled[i] - res.parunscaled[i]) >= ptol:
                    msg = "Parameter #%i(%s) for runs '%s' differs too much: " \
                        % (i, res.names[i], res.runs)
                    msg += "%r vs. %r" % (res.parunscaled[i],
                                          cmpres.parunscaled[i])
                    raise ValueError(msg)
        return ResultList(uniq.values())


    def getRunCounts(self):
        """
        Return a list with the different numbers of runs used for the results.
        """
        ret = set()
        for r in self:
            ret.add(len(r.runs))
        return sorted(ret)


    def getIpolMethods(self):
        """
        Return a list of the IpolMethods used.
        """
        methods = []
        for mr in self:
            met = mr.getIpolMethod()
            if not met in methods:
                methods.append(met)
        return methods


    def isValid(self):
        """
        Perform some validity checks.

        - Checks if all stored results have the same parameters.
        - Checks if all stored results have the same set of observables.

        @raises FixedSortedKeysError: if results have different parameter names
                @see{FixedSortedKeys.goodPartner()}.
        @raises ValueError: if results have different sets of observables.
        """
        if len(self) > 0:
            first = self[0]
            # Validation functions. Used to filter `self` and check that the
            # returned list is empty.
            def diffparamnames(mr):
                return first.names != mr.names

            def diffobservables(mr):
                return first.obs != mr.obs

            t = filter(diffparamnames, self)
            if len(t):
                raise ResultError("Results with different parameter names"
                                  " found!")
            t = filter(diffobservables, self)
            if len(t):
                raise ResultError("Results with different observables found!")
        return True


    def getObservables(self):
        if len(self):
            return self[0].obs
        else:
            return []


    def getParamNames(self):
        return self[0].names
    names = property(getParamNames)


    @deprecated("Is this used/should this be kept?")
    def getKBest(self, K):
        """
        Return the K results that have the lowest GoF.
        @param K: an integer that specifies how many results you want.
        """
        best = sorted(self, key=lambda res: res.gof)[:K]
        return ResultList(best)


    @deprecated("Is this used/should this be kept?")
    def getResultsInsideRange(self, rangedict):
        """
        Return only those Minimization Results that are inside parameter ranges
        specified via rangedict.
        """
        clean = [i for i in self if i.isInRange(rangedict)]
        return ResultList(clean)


    @deprecated("Is this used/should this be kept?")
    def getResultsInsideKsigmaEllipsisOfM0(self, M0, k=1):
        inside =[mr for mr in self if mr.isInKsigmaEllipsisOfM0(M0, k=k)]
        return ResultList(inside)


    def filtered(self, ff):
        """Get filtered result list.

        The returned `ResultList` will contain only results for that the filter
        function `ff` returned `True`.
        """
        return ResultList(filter(ff, self), validate=False)


    def getMaxRunsResults(self):
        """
        Return sublist with all results using the maximal #(runs).

        This is a short-cut for:
            >>> maxnrruns = max(rl.getRunCounts())
            >>> new = rl.filtered(lambda mr: len(mr.runs) == maxnrruns)
        """
        maxnrruns = max(self.getRunCounts())
        return self.filtered(lambda mr: len(mr.runs) == maxnrruns)


    def getParamValues(self, param, K=0):
        """Return all parameter values of a certain parameter param from
        either all results in the resultlist or the K best (in terms of GoF)

        Parameters
        ----------
        param : str
            The parameter name.
        K: int|'all', optional
            Return only the parameter values of the `K` best results. If `K`
            is negative or zero all values are returned. The special value
            'all' is accepted, too.

        Returns
        -------
        values : numpy.ndarray
        """
        if K > 0:
            return self.getKBest(K).getParamValues(param)
        values = numpy.empty(len(self))
        idx = self[0].getIndex(param)
        for i, res in enumerate(self):
            values[i] = res.values[idx]
        return values


    @deprecated("Is this used/should this be kept?")
    def translateCovariance(self, covdict, translator):
        """
        Translate paramnames as given in the translator dict.

        TODO: the current translations will be removed from the professor
        library!
        """
        newdict = {}
        for k, v in covdict.iteritems():
            temp = [translator[name] for name in k]
            newdict[tuple(temp)] = v
        return newdict


    @deprecated("Is this used/should this be kept?")
    def getCovariances(self, retranslate=False):
        """
        Return a list of the covariance matrices as calculated by Minuit.
        """
        if not self[0].covariance is None:
            if retranslate:
                # create dictionary between minuit parnames and the real ones
                translator = {}
                keys = self[0].covariance.keys()
                minuitpars = []
                for k in keys:
                    for param in k:
                        if not param in minuitpars:
                            minuitpars.append(param)
                minuitpars.sort()
                for num, mpar in enumerate(minuitpars):
                    translator[mpar] = self.getParamNames()[num]

                return [self.translateCovariance(i.covariance, translator) for
                        i in self if not i.covariance is None]
            else:
                return [i.covariance for i in self if not i.covariance is None]
        else:
            return None


    @deprecated("Is this used/should this be kept?")
    def getCorrelationMatrix(self, covmat):
        """
        Return a matrix of parameter correlation coefficients calculated
        from a covariance matrix covmat.
        """
        corrmat = {}
        for i in covmat.keys():
            corrmat[i] = stats.getCorrelation(covmat, i[0], i[1])
        return corrmat


    @deprecated("Is this used/should this be kept?")
    def getCorrelations(self, retranslate=False, meansonly=False):
        """
        Return a list of matrices of correlation coefficients for all
        MinimizationResults in the ResultList.

        If retranslate is set to True, then the common parameter names are
        used, otherwise the minuit names will be used.

        If meansonly is set to yes, only the mean and the rms of the
        calculated correlation coefficients are returned for each pair
        of parameters. This method is probably to be disfavoured if
        the covariance matrices to not overlap.
        """
        if not self.getCovariances() is None:
            corrmats = map(self.getCorrelationMatrix, self.getCovariances(retranslate))
            if meansonly:
                statdict = {}
                for key in corrmats[0].keys():
                    temp = [d[key] for d in corrmats]
                    statdict[key] = (numpy.mean(temp), stats.rms(temp))
                return statdict
            else:
                return corrmats
        else:
            return None


    def mean(self, param):
        """
        Return weighted mean of param values and the mean of the largest and the
        smallest uncertainty as typical error.
        """
        temp = []
        idx = self[0].getIndex(param)
        for res in self:
            value = res.values[idx]
            maxerror = max(res.errors[idx])
            temp.append((value, maxerror))
        E = numpy.array(temp)[:,1]
        return stats.weightedMean(temp)[0], 0.5*(max(E)+min(E))


    @deprecated("Is this used/should this be kept?")
    def getSampleCovMat(self, as_array=False, correlations=False):
        """
        Return the covariance matrix from the complete ResultList. Instead of
        using the covariance matrices calculated by Minuit, use the definition
        of covariance of samples instead.
        """
        ## Some data preparation
        t = {}
        names = self.getParamNames()
        for n in names:
            t[n] = []
        for mr in self:
            for n in names:
                t[n].append(mr.parunscaled[mr.getIndex(n)])

        ## Covariance matrix as dictionary:
        covmat = stats.getCovMatFromSample(t)

        ## We have four output options:
        ##
        ## 1.) a dict-type covariance matrix
        if correlations is False and as_array is False:
            return covmat

        ## 2.) an array-type covariance matrix
        elif correlations is False and as_array is True:
            return stats.convertCovMatToArray(covmat,
                    names=self.getParamNames())

        ## 3.) a dict-type matrix of correlation coefficients
        elif correlations is True and as_array is False:
            return stats.convertCovMatToCorrMat(covmat)

        ## 4.) an array-type matrix of correlation coefficients
        elif correlations is True and as_array is True:
            return stats.convertCovMatToArray(
                    stats.convertCovMatToCorrMat(covmat),
                    names=self.getParamNames())


    def getSampleCorrelations(self, retcov=False):
        """
        Return the sample correlation (or covariance) matrix.

        This uses the numpy implementation of the covariance estimator.

        To create nice color plots from the output of this function you can
        do the following::

            >>> corrcoeffs = resultlist.getSampleCorrelations()
            >>> paramnames = resultlist.getParamNames()
            >>> X, Y = pyplot.meshgrid(arange(len(paramnames) + 1),
            ... arange(len(paramnames) + 1))
            >>> # the y-axis (= axis 0 in pcolor semantics) must be inverted
            ... # to get the usual matrix ordering
            ...
            >>> pyplot.pcolor(X, Y, corrcoeffs[::-1], vmin=-1.0, vmax=1.0)

        Parameters
        ----------
        retcov : bool, optional
            Return the covariance matrix instead if set to ``True``.
        """
        m = numpy.empty((len(self.names), len(self)))
        # fill the parameter sample vectors
        for i, paramname in enumerate(self.names):
            m[i] = self.getParamValues(paramname)
        if retcov:
            return numpy.cov(m)
        else:
            return numpy.corrcoef(m)

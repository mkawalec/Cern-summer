#!/usr/bin/env python
# vim:fileencoding=utf-8
"""analytic_interpolation.py

This module contains the L{BinDistribution} class. It interpolates the
distribution of the Monte Carlo answers for each bin of each observable.
"""

#for epydoc
__docformat__ = "epytext"

import numpy, numpy.dual
import types, warnings
#from professor.histo import Bin

class InterpolationError(StandardError):
    pass

class InterpolationWarning(Warning):
    pass


class BinDistribution:
    """This class takes a C{list} of (bin content, parameter) C{tuples} and
    tries to do an analytic interpolation up to 2nd order for the distribution
    of the given bin contents in the parameter space.

    Example usage:

        >>> bd = BinDistribution("dummy-obs", "dummy-bin", ["p1", "p2"])
        >>> # fill with data using AddRun(...)
        >>> bd.setCenter(.5)
        >>> bd.calcInterpolationCoefficients()
        >>> bd.calcValue([.4,.3])

    @ivar _center: The center (M{p_0}) for the interpolation.
    @ivar _bins: C{list} of (L{Bin}, parameters) pairs for the interpolation.
    @ivar _coeffs: The result of the interpolation, stored in a
        C{numpy.ndarray} object.
    @ivar _coeff_sig2: The quadratic standard deviation for the interpolation
        coefficients.
    @ivar _observable: An identifier for the observable, this bin belongs to.
    @ivar _binrange: An identifier for this bin.
    """
    def __init__(self, observable, binrange, parameter_names, bins = None):
        """Initialise internal variables.

        @param observable: string describing the the observable this bin
            distribution belings to,
        @param binrange: the x range of this bin, see L{Bin.getXRange()},
        @param parameter_names: list with the names of the used parameters, is
            used to caculate the number of interpolation coefficients,
        @param bins: list with (bin data, parameter values) tuples used
            for the interpolation,
        """
        self._observable = observable
        self._binrange = binrange

        #: List with the parameter names, used in L{numberOfCoefficients()}
        self._parameter_names = parameter_names

        #: The center (M{p_0}) for the interpolation
        self._center = None

        #: A list of (bin data, parameters) tuples for the bins with
        #: which we want to calculate our analytic interpolation.
        self._bins = []

        #: The coefficients for the analytic interpolation in a column vector
        #: array.
        self._coeffs = None
        self._coeff_sig2 = None

        # see "important warning" for list-type default arguments in
        # http://docs.python.org/tut/node6.html#SECTION006710000000000000000

        if bins != None:
            for bindata, parameter in bins:
                self.addRun(bindata, parameter)

    def _check_parameters(self, parameters, errormessage="Given parameters have wrong length!"):
        """Check length of given parameters against len(self._parameter_names).

        @raise InterpolationError:
        """
        if len(parameters) != len(self._parameter_names):
            raise InterpolationError(errormessage)

    def addRun(self, bin, parameters):
        """Adds a bin to the list of work bins.

        The bin's xrange should be the one given to the constructor.

        @param bin: The content and errors of the bin.
        @type  bin: L{Bin} instance.
        @param parameters: The location in parameter space.
        @type parameters: subscriptable object,
            see L{createLongParameterVector()}
        """
        self._check_parameters(parameters)
        if bin.getXRange() != self._binrange:
            w = InterpolationWarning("Adding run with different x range:"+
                    " bin %s\n    continuing..."%(bin))
            warnings.warn(w)

        # invalidate previous interpolation
        self._coeffs = None
        self._coeff_sig2 = None

        self._bins.append( (bin, parameters) )

    def getRuns(self):
        return self._bins

    addBin = addRun

    def setCenter(self, center):
        """Set the center (M{p_0}) for the interpolation.

        Clears previously calculated interpolation coefficients.

        @param center: The new center for the interpolation.
        @type  center: C{numpy.ndarray} or C{float}
        """
        if isinstance(center, numpy.ndarray):
            center = center
        elif type(center) == types.FloatType:
            center = center*numpy.ones(len(self._parameter_names))
        elif type(center) in (types.ListType, types.TupleType):
            center = numpy.array(center)
        else:
            raise TypeError("Argument center must be numpy.ndarray or float!")

        self._check_parameters(center)
        self._center = center

        self._coeffs = None
        self._coeff_sig2 = None

    def getCenter(self):
        """
        @rtype: C{numpy.ndarray}
        """
        return self._center

    def getObservable(self):
        return self._observable

    def getBinRange(self):
        return self._binrange

    def requiredRuns(self):
        """Return the minimal number of runs / bins required for SVD.

        This is one more than the number of interpolation coefficients so that
        the linear system of equations is over-determined.

        @rtype: C{int}
        """
        return 1 + self.numberOfCoefficients()

    @staticmethod
    def s_requiredRuns(n):
        return 2 + n + n*(n+1)/2

    def numberOfCoefficients(self):
        """Return the number of coefficients for the analytic fit.

        @rtype: C{int}
        """
        n = len(self._parameter_names)
        return 1 + n + n*(n+1)/2

    @staticmethod
    def s_numberOfCoefficients(n):
        return 1 + n + n*(n+1)/2

    def createLongParameterVector(self, parameters):
        """Return a row vector with combinations of the parameter values.

        The calculation does the following:
            1. Calculate M{dp}, the difference between parameters and
                the set center.
            2. Fill the row vector with the relevant combinations of M{dp}
                entries. See L{s_longParameterVector}.

        Used for computing both the interpolation coefficients and the
        results of the interpolation.

        @param parameters: The location in parameter space.
        @type  parameters: subscriptable object like C{numpy.ndarray}, C{list},
            or C{tuple}.

        @rtype: C{numpy.ndarray}
        """
        self._check_parameters(parameters)

        if self._center == None:
            raise InterpolationError("Center not set!")
        # stores the long row vector, entries are:
        # ( 1. , dp_1 , ... , dp_n , 
        #     dp_1*dp_1 , dp_1*dp_2 , ... , dp_1*dp_n ,
        #     dp_2*dp_2 , dp_2*dp_3 , ... , dp_2*dp_n ,
        #                      ...
        #                                   dp_n*dp_n )
        retvec = numpy.ones(self.numberOfCoefficients())
        nr_of_parameters = len(self._parameter_names)
        hor_index = 1
        dp = parameters - self._center

        for j in xrange(nr_of_parameters):
            retvec[hor_index] = dp[j]
            hor_index += 1

        for j in xrange(nr_of_parameters):
            for k in xrange(j, nr_of_parameters):
                retvec[hor_index] = dp[j]*dp[k]
                hor_index += 1

        return retvec

    @staticmethod
    def s_longParameterVector(p):
        """Return a row vector with combinations of the parameter values.

        The calculation does the following:
            1. Fill the row vector with the relevant combinations of M{p}
                entries.

        Used for computing both the interpolation coefficients and the
        results of the interpolation.

        @param p: The location in parameter space.
        @type  p: subscriptable object like C{numpy.ndarray}, C{list},
            or C{tuple}.

        @rtype: C{numpy.ndarray}
        """
        # stores the long row vector, entries are:
        # ( 1. , p_1 , ... , p_n , 
        #     p_1*p_1 , p_1*p_2 , ... , p_1*p_n ,
        #     p_2*p_2 , p_2*p_3 , ... , p_2*p_n ,
        #                      ...
        #                                   p_n*p_n )
        nr_of_parameters = len(p)
        retvec = numpy.ones(
                BinDistribution.s_numberOfCoefficients(nr_of_parameters))
        hor_index = 1

        for j in xrange(nr_of_parameters):
            retvec[hor_index] = p[j]
            hor_index += 1

        for j in xrange(nr_of_parameters):
            for k in xrange(j, nr_of_parameters):
                retvec[hor_index] = p[j]*p[k]
                hor_index += 1

        return retvec

    def calcInterpolationCoefficients(self):
        """Calculates the coefficients and errors for the analytic
        interpolation.

        This is done by solving

        M{ MC = P . a  <==> a = P^-1 . MC},

        where M{MC} is a column vector with the bin contents, M{P} is a matrix
        which rows are the relevant combinations of parameters, and a is the
        row vector with the coefficients for the interpolation.  For the
        solution the M{P} matrix is (pseudo-)inverted using the
        L{numpy.dual.pinv} function.

        For the error:

        M{ \sigma(a)^2 = (P^-1)^2 . \sigma(MC)^2 }

        where M{(P^-1)^2} is the elementwise squared of M{P^-1}.
        """
        if self.numberOfRuns() < self.requiredRuns():
            raise InterpolationError("Not enough work bins to perform SVD!")

        self._coeffs = None
        self._coeff_sigs = None

        P = numpy.ones( (len(self._bins), self.numberOfCoefficients()) )
        MC = numpy.zeros(len(self._bins))
        sig_MC = numpy.zeros(len(self._bins))

        # fill the P matrix and the MC vector
        for i, t in enumerate(self._bins):
            bin = t[0]
            parameters = t[1]

            MC[i] = bin.getYVal()
            sig_MC[i] = bin.getYErr()**2
            P[i] = self.createLongParameterVector(parameters)

        P_inv = numpy.dual.pinv(P)

        self._coeffs = numpy.dot(P_inv, MC)
        self._coeff_sig2 = numpy.dot(P_inv**2, sig_MC)

    #TODO: calculate the error/test the error
    def calcValue(self, parameters, error=False):
        """Return the value (and error) of the interpolation.

        @param parameters: The location in parameter space.
        @type  parameters: subscriptable object,
            see L{createLongParameterVector}.
        @param error: Flag, if C{True} a C{tuple} (value, error) is returned,
            otherwise only the value (default).
        @type  error: C{bool}
        @rtype: C{numpy.float64} or C{tuple} of C{numpy.float64}s
        """
        self._check_parameters(parameters)

        if self._coeffs == None:
            raise InterpolationError("Coefficients for interpolation not" +
                    " yet calculated!")

        P = self.createLongParameterVector(parameters)

        if error:
            return (numpy.dot(P, self._coeffs),
                    numpy.sqrt(numpy.dot(P**2, self._coeff_sig2)))
        else:
            return numpy.dot(P, self._coeffs)

    #TODO: verify the calculation
    def calcGradient(self, parameters):
        self._check_parameters(parameters)
        dp = parameters - self.getCenter()
        grad = numpy.zeros(len(self._parameter_names))
        for k in xrange(len(self._parameter_names)):
            g_k = self.getCoefficient(k) + self.getCoefficient(k,k) * dp[k]

            # make i <= k
            for i in xrange(k):
                g_k += self.getCoefficient(i, k) * dp[i]

            for i in xrange(k, len(self._parameter_names)):
                g_k += self.getCoefficient(k, i) * dp[i]

            grad[k] = g_k
        return grad

    #TODO: this is not a good method to test the "goodness of the fit"
    def simpleChi2(self):
        """Returns a simple chi2 value.

        M{ chi^2 = sum_i (x_i - MC(p_i))^2 / dx_i^2 }

        If there are bins with no associated error, a warning is raised and
        these bins are not used for calculation.

        @return: simple chi2 value
        @rtype: C{float}
        """
        chi2 = .0
        for bin, parameters in self._bins:

            if bin.getYErr() == None:
                w = InterpolationWarning("Encountered bin with no" +
                    " associated error:" +
                    " parameters: %s bin data: %s"%(parameters, bindata))
                warnings.warn(w)
                continue

            d = bin.getYVal() - self.calcValue(parameters)
            chi2 += (d / bin.getYErr())**2

        return chi2 # / (self.numberOfRuns() - self.numberOfCoefficients())

    def normChi2(self):
        return self.simpleChi2() / ( self.numberOfRuns()
                                     - self.numberOfCoefficients() )

    def getCoefficient(self, i1=None, i2=None):
        """Returns an interpolation coefficient.

        Return values are::
            a^0_0          if i1 == None
            a^1_i1         if i1 != None and i2 == None
            a^2_(i1,i2)    if i1 != None and i2 != None

        Indices run from 0 to n-1 , where n is the number of parameters!

        @raise InterpolationError: if C{i1 > i2}.
        """
        if self._coeffs == None:
            raise InterpolationError("Coefficients for interpolation not" +
                    " yet calculated!")

        if i1 == None:
            ind = 0
        elif i2 == None:
            # we want a linear coefficient
            ind = i1 + 1
        else:
            # now we want a quadratic coefficient
            ind = 1 + len(self._parameter_names)

            if i1 > i2:
                raise InterpolationError("Index i1 must not be greater" +
                        " than i2!")
                # make i1 <= i2
                #i1, i2 = i2, i1

            for n in xrange(i1):
                ind += len(self._parameter_names) - n

            ind += i2 - i1

        #print i1, i2, ind
        return self._coeffs[ind]

    def numberOfRuns(self):
        return len(self._bins)

    def __str__(self):
        return ('BinDistribution for observable "%s" bin "%s"' +
                ' with data from %i runs for parameters %s')%(
                        self._observable, self._binname, self.numberOfRuns(),
                        self._parameter_names)

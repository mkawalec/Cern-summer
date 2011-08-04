"""
Module defining interpolation mechanisms.
"""

import numpy
import numpy.dual

from professor.tools import log as logging
from professor.tools.decorators import virtualmethod
from professor.histo import Bin


class InterpolationError(Exception):
    """Base class for all errors during interpolation."""
    pass


class InterpolationFailedError(InterpolationError):
    """Raise this if an interpolation has invalid coefficients/coeff errors.

    The constructor takes error message and bin id as arguments.
    """
    def __init__(self, message, binid):
        super(InterpolationError, self).__init__(message)
        self.binid = binid


class BaseBinInterpolation(object):
    method = None

    def __init__(self, binid, binrange, coeffs, center, medianmcerr=None):
        self.binid = binid
        self.binrange = binrange

        if type(coeffs) != numpy.ndarray:
            coeffs = numpy.array(coeffs)
        if not numpy.isfinite(coeffs).any():
            raise InterpolationFailedError("Some coefficients are not finite"
                        " for bin %s!" % (binid), binid)
        self.coeffs = coeffs

        assert type(center) == numpy.ndarray
        if not numpy.isfinite(center).any():
            raise InterpolationError(
                    "Center contains non finite elements for bin" " %s!" %
                        (binid), binid)
        self.center = center

        self.npar = len(self.center)
        self.medianmcerr = medianmcerr

    @virtualmethod
    @classmethod
    def fromBindist(cls, center, bd):
        pass

    @virtualmethod
    @classmethod
    def getLongVector(cls, p):
        pass

    @virtualmethod
    @classmethod
    def numOfCoefficients(cls, dim):
        pass

    @virtualmethod
    @classmethod
    def minNumOfRuns(cls, dim):
        pass

    def getValue(self, p):
        """Returns the interpolation value for an already scaled parameter
        vector.

        @param p: the parameter vector from the normed hypercube.
        @type p: numpy.ndarray
        """
        DP = self.getLongVector(p - self.center)
        val = numpy.dot(DP, self.coeffs)
        return val

    def getBin(self, p, error=True):
        return Bin(xlow=self.binrange[0], xhigh=self.binrange[1],
                   yval=self.getValue(p), yerrplus=0.0, yerrminus=0.0)

    def getBinCenter(self):
        return self.binrange[0] + 0.5*(self.binrange[1] - self.binrange[0])


class QuadraticBinInterpolation(BaseBinInterpolation):
    method = "quadratic"
    @classmethod
    def fromBindist(cls, center, bd):
        dim = bd.dim()
        if bd.numberOfRuns() < cls.minNumOfRuns(dim):
            raise ValueError("Not enough runs for this interpolation!")

        DP = numpy.ones(( bd.numberOfRuns(),
                          cls.numOfCoefficients(dim) ))
        MC = numpy.zeros(bd.numberOfRuns())
        for i, (params, bin) in enumerate(bd):
            center.goodPartner(params)
            MC[i] = bin.getYVal()

            dp = params.getScaled() - center.getScaled()

            DP[i] = cls.getLongVector(dp)


        DP_inv = numpy.dual.pinv(DP)
        coeffs = numpy.dot(DP_inv, MC)

        binid = bd.binid
        binrange = bd.binrange
        return cls(binid, binrange, coeffs, center.getScaled(), bd.getMedianMCError())

    @classmethod
    def getLongVector(cls, p):
        """Return a row vector with relevant combinations of the parameter
        values.

        Used for computing both the interpolation coefficients and the
        results of the interpolation.

        @type  p: C{numpy.ndarray} instance.
        @rtype: C{numpy.ndarray}
        """
        # stores the long row vector, entries are:
        # ( 1. , p_1 , ... , p_n ,
        #     p_1*p_1 , p_1*p_2 , ... , p_1*p_n ,
        #     p_2*p_2 , p_2*p_3 , ... , p_2*p_n ,
        #                      ...
        #                                   p_n*p_n )
        nop = len(p)
        retvec = numpy.ones(cls.numOfCoefficients(nop))

        ind1 = 1
        ind2 = nop + 1

        for i in xrange(nop):
            retvec[ind1] = p[i]
            ind1 += 1
            for j in xrange(i, nop):
                retvec[ind2] = p[i]*p[j]
                ind2 += 1

        return retvec

    @classmethod
    def numOfCoefficients(cls, dim):
        return 1 + dim + dim*(dim+1)/2
    minNumOfRuns = numOfCoefficients

    def getCoefficient(self, i1=None, i2=None):
        """Returns an interpolation coefficient.

        Return values are::
            a^0_0          if i1 == None
            a^1_i1         if i1 != None and i2 == None
            a^2_(i1,i2)    if i1 != None and i2 != None

        Indices run from 0 to n-1 , where n is the number of parameters!

        @raise ValueError: if i1 > i2 or i1, i2 >= npar.
        """
        if i1 is None and i2 is None:
            ind = 0
        elif i1 is not None and i2 is None:
            # we want a linear coefficient
            if i1 >= self.npar:
                raise ValueError("Index i1 must be less than"
                                 " the number of parameters")
            ind = i1 + 1
        else:
            if i1 >= self.npar:
                raise ValueError("Index i1 must be less than"
                                 " the number of parameters")
            if i2 >= self.npar:
                raise ValueError("Index i2 must be less than"
                                 " the number of parameters")
            ind = 1 + self.npar

            if i1 > i2:
                raise ValueError("Index i1 must not be greater"
                                 " than i2!")

            for n in xrange(i1):
                ind += self.npar - n

            ind += i2 - i1

        return self.coeffs[ind]

    def getGradient(self, params):
        """
        See L{getGradient}.
        """
        dp = params - self.center
        grad = numpy.zeros(self.npar)
        for m in xrange(self.npar):
            g_m = self.getCoefficient(m) + 2.*self.getCoefficient(m,m) * dp[m]

            if m < self.npar - 1:
                for i in xrange(m+1, self.npar):
                    g_m += self.getCoefficient(m, i) * dp[i]

            for i in xrange(self.npar):
                if m > i:
                    g_m += self.getCoefficient(i, m) * dp[i]

            grad[m] = g_m
        return grad


class CubicBinInterpolation(BaseBinInterpolation):
    method = "cubic"
    @classmethod
    def numOfCoefficients(cls, dim):
        return 1 + dim + dim*(dim+1)/2 + dim*(dim+1)*(dim+2)/6
    minNumOfRuns = numOfCoefficients

    @classmethod
    def fromBindist(cls, center, bd):
        dim = bd.dim()
        if bd.numberOfRuns() < cls.minNumOfRuns(dim):
            raise ValueError("Not enough runs for this interpolation!")

        DP = numpy.ones(( bd.numberOfRuns(),
                          cls.numOfCoefficients(dim) ))
        MC = numpy.zeros(bd.numberOfRuns())
        for i, (params, bin) in enumerate(bd):
            center.goodPartner(params)
            MC[i] = bin.getYVal()

            dp = params.getScaled()- center.getScaled()
            DP[i] = cls.getLongVector(dp)

        DP_inv = numpy.dual.pinv(DP)
        coeffs = numpy.dot(DP_inv, MC)

        binid = bd.binid
        binrange = bd.binrange
        return cls(binid, binrange, coeffs, center.getScaled(), bd.getMedianMCError())

    @classmethod
    def getLongVector(cls, p):
        nop = len(p)
        # retvec = numpy.ones(CubicBinInterpolation.numOfCoefficients(nop))
        #
        # For testing fill the parameter with NaN's
        retvec = numpy.zeros(cls.numOfCoefficients(nop)) * numpy.NaN
        retvec[0] = 1.0

        ind1 = 1
        ind2 = 1 + nop # end of linear parameters
        ind3 = 1 + nop + nop*(nop+1)/2 # end of quadratic parameters
        for i in xrange(nop):
            # fill linear
            retvec[ind1] = p[i]
            ind1 += 1
            for j in xrange(i, nop):
                retvec[ind2] = p[i]*p[j]
                ind2 += 1
                for k in xrange(j, nop):
                    retvec[ind3] = p[i]*p[j]*p[k]
                    ind3 += 1
        return retvec


def getInterpolationClass(method, weave):
    """Return class implementing the desired method of interpolation.

    method can be 'quadratic' or 'cubic'.

    If parameter weave is 'True' the weave implementations are tried first
    and the pure-Python implementations are returned as fall backs.
    """
    if weave == True:
        try:
            import interpolationweave
        except ImportError, err:
            logging.error(("Failed to import interpolationweave: %s\n"
                    "Probably your SciPy installation is broken! Using "
                    " slower pure-Python version.") % (err))
            weave = False

    if method == "quadratic" and not weave:
        return QuadraticBinInterpolation
    elif method == "cubic" and not weave:
        return CubicBinInterpolation

    elif method == "quadratic" and weave:
        return interpolationweave.QuadraticBinInterpolationWeave
    elif method == "cubic" and weave:
        return interpolationweave.CubicBinInterpolationWeave

    raise ValueError("Unknown interpolation method '%s'!"%(method))

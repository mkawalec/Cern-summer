"""
Module defining interpolation mechanisms.
"""

import numpy
import numpy.dual

from professor.tools import log as logging
from professor.tools.decorators import virtualmethod
from professor.tools.errors import InterpolationError, InterpolationFailedError, ParameterError
from professor.histo import Bin


class BaseBinInterpolation(object):
    """Base class for the bin-wise interpolation of the MC response function.

    Tailored for polynomial interpolations. The matrix of interpolation
    coefficients is stored. And a method to compute the *extended* parameter
    vector is available.

    A new interpolation is created from a :class:`BinDistribution` instance
    with the :meth:`mkFromBinDist` method. This method must be overwritten by
    the sub-classes. This method calculates the matrix of coefficients.

    .. note::
        The constructor should not be called directly.

    See Also
    --------
    getInterpolationClass : Get a :class:`BaseBinInterpolation` sub-class.
    """
    method = None

    def __init__(self, binid, binrange, coeffs, center, medianmcerr=None):
        """ short doc string """
        self.binid = binid
        self.binrange = binrange

        if type(coeffs) != numpy.ndarray:
            coeffs = numpy.array(coeffs)
        if not numpy.isfinite(coeffs).any():
            raise InterpolationFailedError("Some coefficients are not finite"
                                           " for bin %s!" % (binid), binid)
        self.coeffs = coeffs

        assert isinstance(center, numpy.ndarray)
        if not numpy.isfinite(center).any():
            raise InterpolationError("Center contains non finite elements"
                                     "for bin %s!" % (binid), binid)
        self.center = center

        self.npar = len(self.center)
        self.medianmcerr = medianmcerr

    @classmethod
    @virtualmethod
    def mkFromBinDist(cls, bd, center=None):
        """Make an interpolation from a bin distribution.

        This calculates the interpolation coefficients.

        Parameters
        ----------
        bd : BinDistribution
            The distribution of the MC response function.
        center : ParameterPoint, optional
            The center of the interpolation. If `None` the center of the
            hyper cube spanned by the anchor points is used.
        """
        pass

    @classmethod
    @virtualmethod
    def getLongVector(cls, p):
        """Make an extended parameter vector.

        Parameters
        ----------
        p : numpy.ndarray
        """
        pass

    @classmethod
    @virtualmethod
    def numOfCoefficients(cls, dim):
        """The number of coefficients for a `dim` dimensional space.

        Parameters
        ----------
        dim : int
        """
        pass

    @classmethod
    @virtualmethod
    def minNumOfRuns(cls, dim):
        """Get the minimal number of runs necessary.

        Parameters
        ----------
        dim : int
        """
        pass

    def getValue(self, p):
        """Get the interpolation value.

        Parameters
        ----------
        p : array_like

        Returns
        -------
        val : float
        """
        DP = self.getLongVector(p - self.center)
        val = numpy.dot(DP, self.coeffs)
        return val

    def getBin(self, p, error=True):
        """Get the interpolated bin.

        Parameters
        ----------
        p : numpy.ndarray
            The parameter vector.

        Returns
        -------
        bin : Bin
        """
        return Bin(xlow=self.binrange[0], xhigh=self.binrange[1],
                   yval=self.getValue(p), yerrplus=0.0, yerrminus=0.0)

    def getBinCenter(self):
        return self.binrange[0] + 0.5*(self.binrange[1] - self.binrange[0])


class QuadraticBinInterpolation(BaseBinInterpolation):
    method = "quadratic"
    @classmethod
    def mkFromBinDist(cls, bd, center=None):
        if center is None:
            center = bd.getRanges().center
        # a simple short cut
        dim = bd.dim

        # check the arguments
        if bd.paramnames != center.names:
            raise ParameterError("Parameter names of bin distribution and"
                                 " interpolation center mismatch!")
        if bd.numberOfRuns() < cls.minNumOfRuns(dim):
            raise ValueError("Not enough runs for this interpolation!")

        # NOTE: The parameter names are not needed here. By converting all
        # parameter points to plain arrays, no copying of the parameter
        # names during vector operations takes place. This results in a
        # factor 3 speed-up during the construction of the interpolation
        # coefficients with prof-interpolate and a factor 6 during tuning.

        center = numpy.asarray(center)

        DP = numpy.ones(( bd.numberOfRuns(),
                          cls.numOfCoefficients(dim) ))
        MC = numpy.zeros(bd.numberOfRuns())
        for i, (params, bin) in enumerate(bd):
            MC[i] = bin.getYVal()

            dp = numpy.asarray(params) - center

            DP[i] = cls.getLongVector(dp)


        DP_inv = numpy.dual.pinv(DP)
        coeffs = numpy.dot(DP_inv, MC)

        binid = bd.binid
        binrange = bd.binrange
        return cls(binid, binrange, coeffs, center, bd.getMedianMCError())

    @classmethod
    def getLongVector(cls, p):
        """Return a row vector with relevant combinations of the parameter
        values.

        Used for computing both the interpolation coefficients and the
        results of the interpolation.

        Parameters
        ----------
        p : array_like
        """
        # stores the long row vector, entries are:
        # ( 1. , p_1 , ... , p_n ,
        #     p_1*p_1 , p_1*p_2 , ... , p_1*p_n ,
        #     p_2*p_2 , p_2*p_3 , ... , p_2*p_n ,
        #                      ...
        #                                   p_n*p_n )
        nop = len(p)
        retvec = numpy.empty(cls.numOfCoefficients(nop))
        retvec[0] = 1.0

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

        Indices run from 0 to npar-1 , where npar is the number of parameters!

        Raises
        ------
        ValueError
            If i1 > i2 or i1, i2 >= npar.
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
            if i1 > i2:
                raise ValueError("Index i1 must not be greater"
                                 " than i2!")

            ind = 1 + self.npar

            for n in xrange(i1):
                ind += self.npar - n

            ind += i2 - i1

        logging.debug("getCoefficient for dim(%i): i1(%s), i2(%s) =>"
                      " ind(%i)" % (self.npar, i1, i2, ind))

        return self.coeffs[ind]

    def getGradient(self, params, k=-1):
        """Calculate the gradient of the polynomial.

        Optionally the parameter `k` can be used to calculate only the k-th
        component of the gradient to safe some computing time.

        Written in terms of the stored polynomial coefficients,
        :math:`a_{ij}^{(2)}`, the k-th component of the gradient is:

        .. math::

            \frac{\partial f}{\partial p_k} =
                    a_k^{(1)}
                    + \sum_{i=0}^k a_{ik}^{(2)} p_i
                    + \sum_{j=k}^{n-1} a_{kj}^{(2)} p_j

        Note, that for the quadratic coefficients we always have
        :math:`i<=j`. The derivitave of the quadratic term in :math:`p_k` is
        taken into account by the overlap of the two sums.

        Parameters
        ----------
        params : array_like
            The point where the gradient is calculated.
        k : int, optional
            The component of the gradient that is calculated. `k` must be a
            valid array index, i.e. between 0 and npar-1.

        Returns
        -------
        grad : array, float
            The gradient as a vector. If the optional parameter `k` is
            non-negative only one component of the gradient is calculated
            and returned.
        """
        dp = numpy.asarray(params) - self.center
        if k >= self.npar:
            raise ValueError("Parameter k must be in range [0, npar-1]!")

        elif k >= 0:
            # linear part
            grad = self.getCoefficient(k)
            # quadratic part
            for i in xrange(0, k+1):
                grad += dp[i] * self.getCoefficient(i, k)
            for i in xrange(k, self.npar):
                grad += dp[i] * self.getCoefficient(k, i)
            return grad

        else:
            grad = numpy.empty(self.npar)
            for k in xrange(self.npar):
                # linear part
                grad_k = self.getCoefficient(k)
                # quadratic part
                for i in xrange(0, k+1):
                    grad_k += dp[i] * self.getCoefficient(i, k)
                for i in xrange(k, self.npar):
                    grad_k += dp[i] * self.getCoefficient(k, i)

                grad[k] = grad_k
            return grad


class CubicBinInterpolation(QuadraticBinInterpolation):
    method = "cubic"
    @classmethod
    def numOfCoefficients(cls, dim):
        return 1 + dim + dim*(dim+1)/2 + dim*(dim+1)*(dim+2)/6
    minNumOfRuns = numOfCoefficients

    @classmethod
    def getLongVector(cls, p):
        nop = len(p)
        # For testing fill the parameter with NaN's
        # retvec = numpy.zeros(cls.numOfCoefficients(nop)) * numpy.NaN
        retvec = numpy.empty(cls.numOfCoefficients(nop))
        retvec[0] = 1.0

        ind1 = 1
        ind2 = 1 + nop # end of linear parameters
        ind3 = 1 + nop + nop*(nop+1)/2 # end of quadratic parameters
        for i in xrange(nop):
            # fill linear
            retvec[ind1] = p[i]
            ind1 += 1
            for j in xrange(i, nop):
                # fill quadratic
                retvec[ind2] = p[i]*p[j]
                ind2 += 1
                for k in xrange(j, nop):
                    # fill cubic
                    retvec[ind3] = p[i]*p[j]*p[k]
                    ind3 += 1
        return retvec

    def getCoefficient(self, i1 = None, i2 = None, i3 = None):
        if i3 is None:
            return QuadraticBinInterpolation.getCoefficient(self, i1, i2)
        if not (i1 <= i2 <= i3):
            raise ValueError("Indices must fulfil i1 <= i2 <= i3!")

        # Jump to the beginning of the block with the cubic parameters.
        off = QuadraticBinInterpolation.numOfCoefficients(self.npar)
        # Skip the triangular blocks with first index less than i1.
        for x in xrange(i1):
            off += (self.npar - x) * (self.npar -  x + 1)/2

        # Skip the remaining rows with second index less than i2.
        for y in xrange(i1, i2):
            off += self.npar - y

        # Jump to the element in the final row.
        off += i3 - i2
        # print "N = %i : (%i, %i, %i) => %i" % (self.npar, i1, i2, i3, off)
        return self.coeffs[off]


    # TODO: make this functional
    def getGradient(self, params, k=-1):
        """Calculate the gradient of the polynomial.

        Optionally the parameter `k` can be used to calculate only the k-th
        component of the gradient to safe some computing time.

        Parameters
        ----------
        params : array_like
            The point where the gradient is calculated.
        k : int, optional
            The component of the gradient that is calculated. `k` must be a
            valid array index, i.e. between 0 and npar-1.

        Returns
        -------
        grad : array, float
            The gradient as a vector. If the optional parameter `k` is
            non-negative only one component of the gradient is calculated
            and returned.
        """
        dp = numpy.asarray(params) - self.center

        if k >= self.npar:
            raise ValueError("Parameter k must be in range [0, npar-1]!")

        elif k >= 0:
            # linear part
            grad = self.getCoefficient(k)
            # quadratic part
            for i in xrange(0, k+1):
                grad += dp[i] * self.getCoefficient(i, k)
            for i in xrange(k, self.npar):
                grad += dp[i] * self.getCoefficient(k, i)
            # cubic part
            for i in xrange(k, self.npar):
                for j in xrange(i, self.npar):
                    grad += dp[i] * dp[j] * self.getCoefficient(k, i, j)
            for i in xrange(0, k+1):
                for j in xrange(k, self.npar):
                    grad += dp[i] * dp[j] * self.getCoefficient(i, k, j)
            for i in xrange(0, k+1):
                for j in xrange(i, k+1):
                    grad += dp[i] * dp[j] * self.getCoefficient(i, j, k)
            return grad

        else:
            grad = numpy.empty(self.npar)
            for k in xrange(self.npar):
                # linear part
                grad_k = self.getCoefficient(k)

                # quadratic part
                for i in xrange(0, k+1):
                    grad_k += dp[i] * self.getCoefficient(i, k)
                for i in xrange(k, self.npar):
                    grad_k += dp[i] * self.getCoefficient(k, i)

                # cubic part
                for i in xrange(k, self.npar):
                    for j in xrange(i, self.npar):
                        grad_k += dp[i] * dp[j] * self.getCoefficient(k, i, j)
                for i in xrange(0, k+1):
                    for j in xrange(k, self.npar):
                        grad_k += dp[i] * dp[j] * self.getCoefficient(i, k, j)
                for i in xrange(0, k+1):
                    for j in xrange(i, k+1):
                        grad_k += dp[i] * dp[j] * self.getCoefficient(i, j, k)

                grad[k] = grad_k
            return grad


def getInterpolationClass(method, weave):
    """Return class implementing the desired method of interpolation, given an informal name.

    Parameters
    ----------
    method : {'quadratic', 'cubic'}
        The name of the interpolation method. At the moment quadratic and
        cubic polynomial interpolation is supported.
    weave : bool
        If `True` the weave implementations are tried first and the
        pure-Python implementations are returned only as fall backs.
    """
    if weave:
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

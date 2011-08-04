"""
Module defining interpolation mechanisms.
"""

import numpy
import numpy.dual

from professor.tools import log as logging
from professor.tools.decorators import virtualmethod
from professor.tools.errors import InterpolationError, InterpolationFailedError, ParameterError
from professor.histo import Bin

class GenericBinInterpolation(object):
    """Generic class for bin-wise interpolation of the MC response function.

    Tailored for polynomial interpolations. The matrix of interpolation
    coefficients is stored. And a method to compute the *extended* parameter
    vector is available.

    A new interpolation is created from a :class:`BinDistribution` instance
    with the standard constructor :meth:`__init__`. 
    This method calculates the matrix of coefficients.

    .. note::
        The constructor can be called only with the "order=..." argument, 
        e.g. to calculate the number of minimum MC-runs with the created instance.

    """

    def __init__(self, bd=None, center=None, order=None):
        """ Creates an interpolation object.
        
        At least 'order' needs to be specified for object creation.
        Data can be provided optional in form of a bin distribution.
        
        Parameters
        ----------
        bd : BinDistribution, optional
            The distribution of the MC response function. 
        center : ParameterPoint, optional
            The center of the interpolation. If `None`the center of the
            hyper cube spanned by the anchor points is used.
        order : int, str
            Interpolation order. 
            Given either by word ("linear, quadratic",...) or polyN with
            N being the order of the polynom used for interpolation.
        """
        
        if not order:
            raise ValueError("No input for bin interpolation - cannot build object.")
        
        try: 
            self.order = filter(lambda x: x[1] == order, enumerate(("linear", "quadratic", "cubic", "quartic")))[0][0]+1
        except IndexError:
            try:
                if not order.startswith("poly"):
                    raise ValueError("No interpolation order specified. (%s)" % str(order))
                self.order = int(order[4:])
            except ValueError:
                raise ValueError("No interpolation order specified. (%s)" % str(order))

        if self.order < 1:
            raise ValueError("Constant interpolation as well as negative exponents not supported.")
        
        if bd:
            self.fillFromBinDistribution(bd=bd, center=center)
            return
    
    def fillFromBinDistribution(self, bd=None, center=None):
        """Fill an empty interpolation from a bin distribution.
        Will overwrite previous bin data!

        This calculates the interpolation coefficients.

        Parameters
        ----------
        bd : BinDistribution
            The distribution of the MC response function.
        center : ParameterPoint, optional
            The center of the interpolation. If `None` the center of the
            hyper cube spanned by the anchor points is used.
        """
        if center is None:
            center = bd.getRanges().center
        # a simple short cut
        dim = bd.dim

        # prepare class
        self.npar = dim
        self.numOfCoeffs = self.numOfCoefficients(dim)

        # check the arguments
        if bd.paramnames != center.names:
            raise ParameterError("Parameter names of bin distribution and"
                                 " interpolation center mismatch!")
        if bd.numberOfRuns() < self.minNumOfRuns(dim):
            raise ValueError("Not enough runs for this interpolation!")

        # NOTE: The parameter names are not needed here. By converting all
        # parameter points to plain arrays, no copying of the parameter
        # names during vector operations takes place. This results in a
        # factor 3 speed-up during the construction of the interpolation
        # coefficients with prof-interpolate and a factor 6 during tuning.

        center = numpy.asarray(center)

        DP = numpy.ones(( bd.numberOfRuns(),
                          self.numOfCoeffs ))
        MC = numpy.zeros(bd.numberOfRuns())
        for i, (params, bin) in enumerate(bd):
            MC[i] = bin.getVal()

            dp = numpy.asarray(params) - center

            DP[i] = self.getLongVector(dp)


        DP_inv = numpy.dual.pinv(DP)
        coeffs = numpy.dot(DP_inv, MC)

        self.binid = bd.binid
        self.binrange = bd.binrange

        if not numpy.isfinite(coeffs).any():
            raise InterpolationFailedError("Some coefficients are not finite"
                                           " for bin %s!" % (binid), binid)
        self.coeffs = coeffs

        if not numpy.isfinite(center).any():
            raise InterpolationError("Center contains non finite elements"
                                     "for bin %s!" % (binid), binid)
        self.center = center
        self.medianmcerr = bd.getMedianMCError()
        return self

    def getLongVector(self, p):
        """Make an extended parameter vector.
        
        Polynomials are split into parts of same order.
        Generating functions (lambda) for these parts are created once per order
        and stored in a dict.
        In case the same class/object is used multiple times the stored functions
        will be used.
        
        TODO: Maybe a numpy-equivalent can be found for the by-order-creation task
        which would speed-up the pure-python implementation.
        (Anyway this might not be used because of the C-implementation).

        Parameters
        ----------
        p : numpy.ndarray
        """
        
        if self.order < 0:
            return
        npar = len(p)

        def getOrder(p,n):
            if n == 0:
                return (1,)
            return eval("lambda x:(%s for x0 in xrange(%d) %s)" % (
                "*".join("x[x%d]"%j for j in xrange(n)),
                npar,
                " ".join("for x%d in xrange(x%d,%d)" % (k,l,npar) for (l,k) in zip(xrange(n-1),xrange(1,n)))
                ))(p)
        
        from itertools import chain
        return numpy.fromiter(chain(*(getOrder(p, n) for n in xrange(self.order+1))),float,count=self.numOfCoefficients(npar))

    def numOfCoefficients(self, dim):
        """The number of coefficients for a `dim` dimensional space.

        Parameters
        ----------
        dim : int
        """
        def binomial(n,k):
            # taken from http://www.velocityreviews.com/forums/t502438-combination-function-in-python.html
            ntok = 1
            for t in xrange(min(k,n-k)):
                ntok = ntok*(n-t)//(t+1)
            return ntok
        self.numOfCoeffs = binomial(dim+self.order,self.order)
        return self.numOfCoeffs

    def minNumOfRuns(self, dim):
        """Get the minimal number of runs necessary.

        Parameters
        ----------
        dim : int
        """
        return self.numOfCoefficients(dim)

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
                   val=self.getValue(p), errplus=0.0, errminus=0.0)

    def getBinCenter(self):
        return self.binrange[0] + 0.5*(self.binrange[1] - self.binrange[0])
    
    def getCoefficient(self, comb):
        """Get coefficient to specific parameter combination given by comb.
        
        As a side-effect self.coeffs is provided, which is an ordered list of all possible
        combinations (o1,o2,o3,...) with ox's being the order of the x-th parameter
        characterizing a term in the polynomial.
        
        Parameters
        ----------
        comb: Tuple, containing order of parameters in this combination.
            E.g. with 3 parameters: (2,1,4) means coefficient to x^2*y*z^4
            in a polynomial with (at least) order 7.
            Constraints: every element in comb > 0, sum(comb) <= self.order
        """
        
        if sum(comb) > self.order or len(comb) != self.npar: 
            # higher order with zero coefficient
            return 0
        if filter(lambda x: x<0 or type(x) != int, comb): 
            # no int or negative order somewhere in comb
            return 0
        
        try:
            """If it's not the first call, we can get the answer from memory."""
            return self.coeffs[int((self.combs==numpy.array(comb)).prod(1).nonzero()[0])]
        except IndexError: # improper combination
            return 0
        except AttributeError:
            """First call: Create the list of all possible combinations."""
            from itertools import product, chain, repeat

            def combinations_with_replacement(iterable, r):
                # from python documentation: 
                # replacement for function only available in >=2.7 
                pool = tuple(iterable)
                n = len(pool)
                for indices in product(range(n), repeat=r):
                    if sorted(indices) == list(indices):
                        yield tuple(pool[i] for i in indices)

            self.combs = numpy.vstack(
                numpy.fromiter(
                    (len(filter(lambda y: y == n, x)) for n in xrange(1,self.npar+1)), int, count=self.npar)
                for o in xrange(self.order+1)
                for x in combinations_with_replacement(xrange(1,self.npar+1),o)
            )
        
        try:
            return self.coeffs[int((self.combs==numpy.array(comb)).prod(1).nonzero()[0])]
        except IndexError: #improper combination
            return 0
        except:
            # we newly created the list and did NOT found the correct term 
            # should be really strange but not impossible
            raise ValueError("""An error occured! 
                Something went very wrong in obtaining polynomial coefficients""")
            return 0

    def getGradient(self, params, k=-1):
        """Return gradient of polynomial characterized by coefficients (memory)
        for given 'params'. If given dimension 'k' only the k-th component is
        computed.
        
        Parameters
        ----------
        params: array-like
        k:  positive integer
        """
        npar = len(params)
        # let create, if needed
        self.getCoefficient(tuple(0 for i in xrange(npar)))
        
        params = params - self.center
        
        if k >= 0 and k < npar: # one component
            ks = (k,)
        else: # all components
            ks = xrange(npar)
        
        if npar == 1:
            ret = sum(self.coeffs[i+1]*params**i*(i+1) for i in xrange(self.order))
            
        else:
            ret = numpy.fromiter(( # some numpy-slicing-and-python-list-comprehension-magic
                sum(
                    (params**numpy.hstack((z[:k],z[k:(k+1)]-1,z[(k+1):]))).prod()*z[k]*self.coeffs[i]
                    for (i,z) in filter(lambda x: x[1][k] != 0, zip(xrange(len(self.combs)),self.combs)))
                for k in ks), float, count=len(ks))
        return ret

###### Backward compatibility section ######
class BaseBinInterpolation(object):
    order = "poly0"
    def convert_to_generic(self):
        try:
            import interpolationweave
            IpolCls = interpolationweave.GenericWeaveBinInterpolation
        except ImportError:
            IpolCls = GenericBinInterpolation
        ipol = IpolCls(order=self.order)
        ipol.__dict__.update(self.__dict__)
        ipol.numOfCoeffs = ipol.numOfCoefficients(self.npar)
        return ipol

class QuadraticBinInterpolation(BaseBinInterpolation):
    order = "quadratic"

class CubicBinInterpolation(QuadraticBinInterpolation):
    order = "cubic"

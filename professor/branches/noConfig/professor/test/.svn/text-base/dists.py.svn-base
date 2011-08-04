"""dists.py

Library with fake distributions to test the interpolation.
"""

from professor.tools.config import Config
from professor.tools.decorators import virtualmethod, deprecated
from professor.histo import Bin
# from professor.interpolation.interpolation import QuadraticInterpolation

_log = Config().getLogger('test')

import numpy


class FakeDistribution(object):
    """Baseclass for our fake bin distributions.

    Stores an object for the y- and error-distribution.
    """
    def __init__(self, obs, binrange, ydist=None, errdist=None):
        self._obs = obs
        self._binrange = binrange
        self._ydist = ydist
        self._errdist = errdist
        self._errorwanted = True

    def getObs(self):
        return self._obs

    def getBinrange(self):
        return self._binrange

    def setError(self, errorwanted = True):
        self._errorwanted = errorwanted

    def getError(self):
        return self._errorwanted

    def __str__(self):
        return ("<FakeDistribution for obs '%s' bin %s:"
                " ydist=%s, errdist=%s>"%(self._obs, self._binrange,
                                          self._ydist, self._errdist))

    def __call__(self, ppoint):
        yval = self._ydist(ppoint.getScaled())

        if self._errorwanted != True or self._errdist is None:
            errestimate = .0
        else:
            yval += self._errdist.error(ppoint.getScaled())
            errestimate = self._errdist.estimate(ppoint.getScaled())

        return Bin(self._binrange[0], self._binrange[1], yval, errestimate)

    def chi2Compare(self, interp, testpoints, error='fake dist'):
        """Return the chi2 between interpolation and this distribution.

        For the calculation the error is switched off.

        @param interp: the Interpolation instance we want to compare with
            this fake distribution.
        @param testpoints: generator/list/iterator of test points
        @type testpoints: something which can stand in a C{for} statement.
        @param error: keyword to set the error used. 'fake dist'(default) or
            'interpolation'.
        """
        chi2 = .0

        if error == 'fake dist':
            olderr = self.getError()
            self.setError(False)

            for tp in testpoints:
                chi2 += ( (self(tp).getYVal() - interp.getValue(tp))
                          / self._errdist.estimate(tp) )**2

            self.setError(olderr)

        elif error == 'interpolation':
            for tp in testpoints:
                chi2 += ( (self(tp).getYVal() - interp.getValue(tp))
                          / interp.getError(tp) )**2

        else:
            raise ValueError("argument error must be 'fake dist' or"
                    " 'interpolation' but is '%s'!"%(error))

        return chi2

    @deprecated(chi2Compare)
    def compare():
        pass

    def pullCompare(self, interp, testpoints, error='fake dist'):
        """Return a numpy.array with the pulls between interpolation and
        this distribution.

        For the calculation the error is switched off.

        @param interp: the Interpolation instance we want to compare with
            this fake distribution.
        @param testpoints: generator/list/iterator of test points where the
            pulls are calculated.
        @type testpoints: something which can stand in a C{for} statement.
        @param error: keyword to set the error used. 'fake dist'(default) or
            'interpolation'.
        """
        pulls = []

        if error == 'fake dist':
            olderr = self.getError()
            self.setError(False)

            for tp in testpoints:
                pulls.append( (self(tp).getYVal() - interp.getValue(tp))
                              / self._errdist.estimate(tp) )
            self.setError(olderr)

        elif error == 'interpolation':
            for tp in testpoints:
                pulls.append( (self(tp).getYVal() - interp.getValue(tp))
                              / interp.getError(tp) )
        else:
            raise ValueError("argument error must be 'fake dist' or"
                    " 'interpolation' but is '%s'!"%(error))

        return numpy.array(pulls)


class YDist(object):
    """Base class for y distributions.

    Description of the interface:
        - __init__ set initial coefficients for the distribution.
        - __call__(self, p) return the value of the distribution.
        - The class should also have a name attribute.
    """
    name="YDist"
    def __init__(self, p_shape):
        assert len(p_shape) == 1
        self._pshape = p_shape
        _log.debug('created dist %s'%(self.name))

    def getPShape(self):
        return self._pshape

    @virtualmethod
    def __call__(self, p):
        """Return the y value at given parameter point.

        @type p: C{numpy.ndarray}
        """
        pass


class ErrorDist(object):
    """Base class for error distributions.

    Description of the interface:
        - __init__ set initial coefficients for the distribution.
        - L{error} return an error that should be added to a y value.
        - L{estimate} return an error estimate.
    The only relevant methods are the __init__, error, and estimate methods.
    """
    @virtualmethod
    def error(self, p):
        """Return an error value for the given point in parameter space.

        This will mostly return some random values.

        @type p: C{numpy.ndarray}
        """
        pass

    @virtualmethod
    def estimate(self, p):
        """Return the error estimate/sigma at the given point in parameter space.
        This is intended to be used in chi^2 calculations.

        @type p: C{numpy.ndarray}
        """
        pass


class Paraboloid(YDist):
    name = 'Paraboloid'
    def __init__(self, center, scale=1., offset=0.):
        super(Paraboloid, self).__init__(center.shape)

        self._center = center
        self._scale = scale
        self._offset = offset

    def __call__(self, p):
        assert p.shape == self.getPShape()
        return (numpy.dot(p-self._center, p-self._center)*self._scale
                + self._offset)

    def __str__(self):
        return ('<Paraboloid: center=%s, scale=%s,'
                ' offset=%f>'%(str(self._center).replace('\n', ''),
                               str(self._scale).replace('\n', ''),
                               self._offset))


class TwoMinima(YDist):
    name = 'TwoMinima'
    def __init__(self, min1, min2, linscale=None):
        """
        min1, min2, linscale must be numpy arrays

        linscale makes sure that the function is not symmetric between the
        two minima, it should not be too big, e.g. around 1.e-4
        """
        super(TwoMinima, self).__init__(min1.shape)

        self._m1 = min1

        assert self.getPShape() == min2.shape
        self._m2 = min2

        if linscale is None:
            linscale = numpy.zeros(self.getPShape())
        assert self.getPShape() == linscale.shape
        self._ls = linscale

    def __call__(self, p):
        assert self.getPShape() == p.shape
        return (numpy.dot(p-self._m1, p-self._m1)
                * numpy.dot(p-self._m2, p-self._m2)
                + numpy.dot(self._ls, p))

    def __str__(self):
        return ('<TwoMinima: min1=%s , min2=%s,'
                ' linear scale=%s>'%(
                    str(self._m1).replace('\n', ''),
                    str(self._m2).replace('\n', ''),
                    str(self._ls).replace('\n', '')))


class Quadratic(YDist):
    name = "Quadratic"
    def __init__(self, cmat, cvec, offset):
        """
        @param cmat: quadratic matrix with the 2. order coefficients
        @param cvec: vector with the 1. order coefficients
        @param offset: offset
        """
        super(Quadratic, self).__init__(cvec.shape)

        dim = self.getPShape()[0]
        assert cmat.shape == (dim, dim)

        self._cmat = cmat
        self._cvec = cvec
        self._offs = offset

    def __call__(self, p):
        assert p.shape == self.getPShape()
        # function call abbreviation
        ndot = numpy.dot
        return (ndot(p, ndot(self._cmat, p))
                + ndot(self._cvec, p)
                + self._offs)

    def __str__(self):
        return "<Quadratic: dim=%i>"%(self.getPShape()[0])


class Cubic(Quadratic):
    def __init__(self, cubmat, cubvec, quadmat, quadvec, quadoff):
        super(Cubic, self).__init__(quadmat, quadvec, quadoff)

        assert cubvec.shape == self.getPShape()
        dim = self.getPShape()[0]
        assert cubmat.shape == (dim, dim)

        self._cubvec = cubvec
        self._cubmat = cubmat

    def __call__(self, p):
        assert p.shape == self.getPShape()
        return ( numpy.dot(self._cubvec, p**3)
                 + numpy.dot(p**2, numpy.dot(self._cubmat, p))
                 + super(Cubic, self).__call__(p)
                )

    def __str__(self):
        return "<Cubic: dim=%i>"%(self.getPShape()[0])


class AbsoluteGaussianError(ErrorDist):
    def __init__(self, sigma):
        self._sigma = sigma

    def error(self, p_unused):
        return numpy.random.normal(.0, self._sigma)

    def estimate(self, p_unused):
        """Return the error estimate at the given point."""
        return self._sigma

    def __str__(self):
        return "<AbsoluteGaussianError: sigma=%f>"%(self._sigma)

#!/usr/bin/env python
# vim:fileencoding=utf-8
"""testBase.py

Base functions for the test code.
"""

import numpy, types, logging
#import random
from professor import histo
from professor.interpolation.analytic_interpolation import InterpolationError, BinDistribution


TestBinXRange = (.0, .1)


#def randomPoint(dim):
    #"""Returns a randomly filled numpy.ndarray length dim."""
    #print "Use numpy.random.rand(...) instead!"
    #r = numpy.zeros(dim)
    #for i in xrange(dim):
        #r[i] = random.random()
    #return r


class Distribution:
    def __init__(self, sm_sigma, binxrange=(.0, 1.)):
        self._smear_sigma = sm_sigma
        self._smeared = True
        self._binXRange = binxrange

    def getXRange(self):
        return self._binXRange

    def getSigma(self):
        return self._smear_sigma

    def getSmeared(self):
        return self._smeared

    def setSmeared(self, smeared):
        self._smeared = smeared

    def getValue(self, point):
        if type(point) == types.FloatType:
            point = numpy.array((point,))

        if self.getSmeared():
            v = self.function(point) + numpy.random.normal(.0, self._smear_sigma)
        else:
            v = self.function(point)
        return histo.Bin(self._binXRange[0], self._binXRange[1],
                v, self.getSmeared()*self._smear_sigma)

    def __call__(self, point):
        self.getValue(point)



class QuadraticDist(Distribution):
    def __init__(self, center = None, parabola_coeffs = None,
            dim = None, sigma = .2, binxrange=(.0, 1.)):
        Distribution.__init__(self, sigma)
        if center == None and dim == None:
            raise ValueError("center and dim must not be None at the same time!")
        elif center != None:
            self._center = center
        else:
            self._center = .5*numpy.ones(dim)

        #nd = len(self._center)
        np = BinDistribution.s_numberOfCoefficients(len(self._center))
        if parabola_coeffs != None:
            if np != len(parabola_coeffs):
                raise ValueError("Given dimension (%i) and number"%(nd) +
                        " of parameters (%i) don't match!"%(np))
            self._coeffs = parabola_coeffs
        else:
            self._coeffs = numpy.zeros(np)

            dim = len(self._center)
            horindex = dim + 1
            for j in xrange(dim):
                for k in xrange(j, dim):
                    if j == k:
                        #print j, '-->', horindex
                        self._coeffs[horindex] = 1.
                    horindex += 1

    def _check_parameters(self, parameters, errormessage="Given parameters have wrong length!"):
        """Check length of given parameters against len(self._parameter_names).

        @raise InterpolationError:
        """
        if len(parameters) != len(self._center):
            raise InterpolationError(errormessage)

    def getCenter(self):
        return self._center

    def function(self, point):
       lp = BinDistribution.s_longParameterVector(point - self._center)
       return numpy.dot(self._coeffs, lp)

    def __str__(self):
        return ("%i-dim QuadraticDist instance:" +
                "    center : %s"%(self._center) +
                "    sigma = %f"%(self._smear_sigma) +
                "    coeffs : %s"%(self._coeffs) )


class CubicDist(QuadraticDist):
    def __init__(self, center = None, cubic_coeffs = None,
            parabola_coeffs = None,
            dim = None, sigma = .2, binxrange=(.0, 1.)):
        QuadraticDist.__init__(self, center, parabola_coeffs, dim, sigma)

        if cubic_coeffs != None:
            if len(cubic_coeffs) != len(self.getCenter()):
                raise ValueError("# of cubic_coeffs (%i) and"%(len(cubic_coeffs)) +
                        " dimension (%i) must match!"%(len(self.getCenter())))

            self._cubic_coeffs = cubic_coeffs
        else:
            self._cubic_coeffs = numpy.ones(len(self.getCenter()))

    def function(self, point):
        return ( QuadraticDist(self).function(point)
                 + self._cubic_coeffs*(point - self._center)**3 )



def Quadratic(point, smeared=True, sigma=.2, scaling=1.):
    center = .5 * numpy.ones(len(point))
    r = .0
    for i, x in enumerate(point):
        r += scaling**2 * (center[i] - x)**2
    if smeared:
        r += numpy.random.normal(.0, sigma)
    return histo.Bin(TestBinXRange[0], TestBinXRange[1], r, sigma)


def Cubic(point, smeared=True, sigma=.2, scaling=1.):
    center = .2 * numpy.ones(len(point))
    r = .0
    for i, x in enumerate(point):
        r += scaling**3 * ( (center[i] - x)**3 + 1.8 )
    if smeared:
        r += numpy.random.normal(.0, sigma)

    return histo.Bin(TestBinXRange[0], TestBinXRange[1], r, sigma)


class PointGenerator:
    """Generates random n-dim points where the projections on the axes keep a
    minimal distance.

    Usage:
        >>> pg = PointGenerator(2)
        >>> pg.nextPoint()
    """
    def __init__(self, dimensions, old_points = None):
        self.dim = dimensions
        if old_points == None:
            self.points = []
        else:
            self.points = old_points[:]

    def getMinDistance(self):
        return 1./(len(self.points)+1)**2

    def nextPoint(self):
        newpoint = numpy.random.rand(self.dim)
        while not self.testDistance(newpoint):
            logging.info("Point %s failed (not a serious problem)!"%(newpoint))
            newpoint = numpy.random.rand(self.dim)
            #newpoint = randomPoint(self.dim)
        self.points.append(newpoint)
        return newpoint

    def testDistance(self, point):
        "Returns True if point fulfills the minimal distance to other points criterion."
        for p in self.points:
            dp = abs(p - point)
            if dp.min() <= self.getMinDistance():
                return False
        return True

    def getParamNames(self):
        return ['param_%i' for i in range(self.dim)]

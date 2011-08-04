#!/usr/bin/env python
# vim:fileencoding=utf-8
"""testInfluenceOfCenter.py

Tests the influence of the chosen center on the SVD algorithm/the interpolation.

Result: the center has no influence.
"""

import functools, numpy, pylab
from professor.interpolation.testBase import *
from professor.interpolation.analytic_interpolation import BinDistribution


class TestBinDistribution(BinDistribution):
    """Class for testing the L{Bin_Distribution} implementation.

    Testing is done on the unit cube in arbitrary dimensions.
    """
    def __init__(self, dimensions, distribution, checkpoints,
            smeared_checkpoints):
        """Store/create test bins and create work bins.

        @param dimensions:
        @param distribution: A callable object describing the distribution
            against which the test is performed. Must map a vector to a
            dictionary. The dictionary must have the keys `content`,
            `higherror`, and `lowerror`.
            It should have a keyword argument `smeared` defaulting to `True`
            which triggers wether the output is smeared with some kind of
            statistic.

            It is used to calculate the work- an test-bin contents.
            See L{Quadratic}.
        @param checkpoints: The number of desired checkpoints or the locations
            of the checkpoints itself.
        @type  checkpoints: list or int
        @param smeared_checkpoints: Triggers if the bin content of test bins
            should be smeared, too.
        @type  smeared_checkpoints: bool
        """
        # initialise with dummy parameter names
        BinDistribution.__init__(self, "test observable", 0,
                ["Param%04i"%(i) for i in xrange(dimensions)])

        self.dim = dimensions
        self.distribution = distribution
        self.test_bins = []

        # store/create test bins
        if type(checkpoints) == types.IntType:
            for i in xrange(checkpoints):
                point = self.randomPoint()
                bindata = self.distribution(point, smeared = smeared_checkpoints)
                self.addTestRun(bindata, point)
        else:
            for point in checkpoints:
                bindata = self.distribution(point, smeared = smeared_checkpoints)
                self.addTestRun(bindata, point)

        # create work bins
        for i in xrange(self.requiredRuns()):
            self.addRun()

    def addRun(self, *args):
        """Adds a (bin content, point) pair to the work bins.

        If a bin content point pair is given, these values are added.
        Otherwise a random point is created and the bin is calculated and both
        are added to the work bin list.

        @param *args: Empty or a bin content point pair.
        """
        if len(args) == 0:
            point = self.randomPoint()
            bin = self.distribution(point, smeared = True)
            BinDistribution.addRun(self, bin, point)
        elif len(args) == 2:
            BinDistribution.addRun(self, args[0], args[1])
        else:
            raise TypeError("AddRun() takes exactly 0 or 2 arguments.")

    def addTestRun(self, bin, parameters):
        self.test_bins.append((bin, parameters))

    def randomPoint(self):
        # return randomPoint(self.dim)
        return numpy.random.rand(self.dim)

    def simpleTestChi2(self):
        """Returns a simple chi2 value calculated with the TEST bins.

        M{ chi^2 = sum_i (x_i - MC(p_i))^2 / dx_i^2 }

        If there are bins with no associated error, a warning is raised and
        these bins are not used for calculation.

        @return: simple chi2 value
        @rtype: C{float}
        """
        chi2 = .0
        for bin, parameters in self.test_bins:

            if bin.getYErr() == None:
                w = InterpolationWarning("Encountered bin with no" +
                    " associated error:" +
                    " parameters: %s bin data: %s"%(parameters, bindata))
                warnings.warn(w)
                continue

            d = bin.getYVal() - self.calcValue(parameters)
            chi2 += d**2 / bin.getYErr()**2

        return chi2


def testInfluenceOfCenter(dim, seed):

    nrofcheckpoints = 15
    nrofcenters = 10

    sigma = .015
    scale = 1.

    dist = functools.partial(Cubic, sigma=sigma, scaling=scale)

    print "----- Seed = '%s' -----"%(seed)

    # generate bin distributions with one seed
    # random.seed(seed)
    numpy.random.seed(seed)
    test = TestBinDistribution(dim, dist, nrofcenters, True)

    xr = numpy.linspace(.0, 1., 1000)

    for i in xrange(nrofcenters):
        #print "==== %i ===="%(i+1)

        center = test.randomPoint()
        test.setCenter(center)
        test.calcInterpolationCoefficients()

        print "p_0 = %s   chi2 = %f   coeff = %s"%(test.center, test.simpleTestChi2(), test.coefficients)

        # plot the interpolation and the center
        if dim == 1:
            y = []
            for x in xr:
                y.append(test.calcValue([x]))
            pylab.plot(xr, y, label="_nolegend_")
            pylab.plot(center, [.1], 'o', label="_nolegend_")

    if dim == 1:
        # plot unsmeared function
        y = []
        xr = numpy.linspace(0., 1., 100)
        for t in xr:
            y.append(dist([t], smeared=False).getYVal())
        pylab.plot(xr, y, lw="2", label="ideal distribution" )
        pylab.legend()
        pylab.title("Seed = '%s'"%(seed))


if __name__ == "__main__":
    print __doc__
    dim = 1

    if dim == 1: pylab.subplot(311)
    testInfluenceOfCenter(dim, 100)

    if dim == 1: pylab.subplot(312)
    testInfluenceOfCenter(dim, 180)

    if dim == 1: pylab.subplot(313)
    testInfluenceOfCenter(dim, "hello world")

    if dim == 1: pylab.show()

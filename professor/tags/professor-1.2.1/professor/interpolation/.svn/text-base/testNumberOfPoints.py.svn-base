"""testNumberOfPoints.py

Tests the influence of the number of data points on the quality of the
interpolation.

Result: for numbers of additional runs (3D ~30) the simpleChi2 result and the
external chi2 calculation seem to converge, at least they seem to become
constant.
"""

import numpy, pylab, functools
from professor.interpolation.analytic_interpolation import BinDistribution
from professor.interpolation.testBase import *

class Tester:
    def __init__(self, distribution, dimension, nr_chi2points, max_additional_bins=10):
        self.dist = distribution
        self.chi2points = None
        self.dim = dimension
        self.parameternames = ["param%i"%(i) for i in xrange(self.dim)]
        self.pointgen = PointGenerator(dimension)

        self.bins = []
        self.max_additional_bins = max_additional_bins
        self.added_bins = -1

        # fill initial bins
        minbins = BinDistribution('TESTOBS', 'TESTBIN',
                self.parameternames).requiredRuns()
        for i in xrange(minbins-1):
            self.generateBin()

        self.initTestPoints(nr_chi2points)

    def initTestPoints(self, nr_testpoints):
        self.chi2points = []
        for i in xrange(nr_testpoints):
            #self.chi2points.append(randomPoint(self.dim))
            self.chi2points.append(numpy.random.rand(self.dim))

    def __iter__(self):
        return self

    def generateBin(self):
        p = self.pointgen.nextPoint()
        data = self.dist(p)
        self.bins.append( (data, p) )

    def next(self):
        """Returns (BinDistribution instance, external chi2) pairs."""
        if self.added_bins >= self.max_additional_bins:
            raise StopIteration

        self.generateBin()
        self.added_bins += 1
        bd = BinDistribution("testObs", self.bins[-1][0].getXRange(),
                self.parameternames, bins = self.bins[:])
        bd.setCenter(.5 * numpy.ones(self.dim))
        bd.calcInterpolationCoefficients()

        yinterp = numpy.zeros(len(self.chi2points))
        yerr = numpy.zeros(len(self.chi2points))
        yideal = numpy.zeros(len(self.chi2points))
        for i, p in enumerate(self.chi2points):
            yinterp[i], yerr[i] = bd.calcValue(p, True)
            yideal[i] = self.dist(p, smeared=False).getYVal()

        external_chi2 = numpy.sum( (yinterp - yideal)**2 / yerr**2 )

        return bd, external_chi2


def testChi2Methods():
    seed = 1
    numpy.random.seed(seed)
    tester = Tester( functools.partial(Quadratic, sigma=.2, scaling=1.),
                     2,         # dimension
                     1000,      # #of points for the external chi2 calculation
                     35)        # #of additional bins
    x = []
    y_ext = [] # for external chi2 calculation done in Tester
    y_int = [] # for BinDistribution-builtin chi2 calculation
    for bd, chi2_ext in tester:
        added_data = bd.numberOfRuns() - bd.requiredRuns()
        x.append(added_data)
        y_ext.append(chi2_ext)
        y_int.append(bd.simpleChi2())

        #print  add_data, bd.simpleChi2(), chi2_ext
        #bd.calcCovMatrix()
        #print bd
        #print bd.numberOfRuns(), bd.covariance

    pylab.semilogy(x, y_ext, "o", label="ext. Chi^2")
    pylab.semilogy(x, y_int, "x", label="int. Chi^2")
    pylab.title(("Comparison of interpolation-quality measurements" +
            " (dim = %i)")%(tester.dim))
    #pylab.text(.9, .7, "dimensions = %i\nunderlying distribution: %s"%(

    pylab.xlabel("# additional points")
    pylab.ylabel('"Chi^2"')
    #pylab.legend()
    pylab.show()


def testNumberOfPoints():
    """Tests the influence of the number of data points on the quality of the
    interpolation.
    """
    dim = 1  # constant!
    columns = 2
    maxadditionalbins = 5
    parameternames = ["param%i"%(i) for i in xrange(dim)]
    #bindistribs = []
    sigma = .02
    dist = functools.partial(Cubic, sigma=sigma, scaling=2.)
    pg = PointGenerator(dim)

    minbins = BinDistribution('TESTOBS', 'TESTBIN', parameternames).requiredRuns()
    center = .5 * numpy.ones(dim)
    bins = []
    for i in xrange(minbins):
        point = pg.nextPoint()
        data = dist(point)
        bins.append( (data, point) )

    # stuff for drawing the real distribution
    xideal = numpy.linspace(.0, 1., 1000)
    yideal = numpy.zeros(1000)
    xtube, ytube = [], []
    for i, t in enumerate(xideal):
        y = dist([t], smeared=False).getYVal()
        yideal[i] = y
        xtube.append(t)
        ytube.append(y - sigma)
    for t in reversed(xideal):
        y = dist([t], smeared=False).getYVal()
        xtube.append(t)
        ytube.append(y + sigma)

    for add in xrange(maxadditionalbins + 1):
        pylab.subplot((maxadditionalbins + 1)/columns, columns, add + 1)

        bd = BinDistribution("testobs", "testbin", parameternames, bins=bins)
        bd.setCenter(center)
        bd.calcInterpolationCoefficients()

        # plot ideal distribution
        #pylab.plot(xideal, yideal, label="ideal distribution")
        pylab.fill(xtube, ytube, label="1-sigma tube", alpha=.1)

        # plot bins
        xbins = [b[1][0] for b in bins]
        ybins = [b[0].getYVal() for b in bins]
        ybinserr = [b[0].getYErr() for b in bins]
        pylab.errorbar(xbins, ybins, ybinserr, fmt="ro", ls="", label="used bins")

        # plot interpolation
        yinterp = numpy.zeros(1000)
        for i, t in enumerate(xideal):
            yinterp[i] = bd.calcValue([t])
        pylab.plot(xideal, yinterp, label="interpolation")

        # calculate chi2
        chi2 = numpy.sum((yinterp - yideal)**2/sigma**2)

        pylab.xlabel('parameter')
        pylab.ylabel('y')
        pylab.title("#bins %i, chi2 = %e" % (len(bins), chi2))

        # add new data point
        point = pg.nextPoint()
        data = dist(point)
        bins.append( (data, point) )
    pylab.show()


if __name__ == "__main__":
    print __doc__
    testChi2Methods()
    #testNumberOfPoints()

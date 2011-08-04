"""testipol.py

This module holds basic code to verify that the quadratic interpolation works.

useful functions:
 - testQuadraticInterpolation:
   Checks if the interpolation of a quadratic function result in the
   coefficients of this function.

 - testInterpolationStoring:
   Checks if the storing/loading of interpolation sets to/from xml-files is
   working. This is done by comparing the coefficients of interpolations
   with those coefficients of interpolations which are the result of storing
   and re-reading the first interpolations.
"""

import tempfile
import os
import numpy
from professor.histo import Bin
from professor.tools.parameter import Scaler, ppFromList, ParameterPoint
from professor.interpolation import (BinDistribution, InterpolationSet,
                                     getInterpolationClass)

class PointGenerator(object):
    def __init__(self, npar=None, scaler=None):
        if scaler is not None:
            self.scaler = scaler
            self.npar = self.scaler.dim()
        elif npar is not None:
            self.npar = npar
            self.scaler = Scaler(["param%i"%(i) for i in xrange(npar)])
        else:
            ValueError("Either npar or scaler must not be None!")

    def nextPoint(self):
        return ppFromList(numpy.random.rand(self.npar), self.scaler,
                          scaled=True)


class BinGenerator(object):
    def __init__(self, obsname, binrange, ydist, errdist=None):
        self.obsname = obsname
        self.binrange = binrange
        self.ydist = ydist
        self.errdist = errdist
        self.errorwanted = True

    def generate(self, ppoint):
        yval = self.ydist(ppoint)
        yerr = .0
        # if self.errdist is not None and self.errorwanted:
        if self.errorwanted:
            yval += self.errdist.error(ppoint)
            yerr = self.errdist.estimate(ppoint)
        return Bin(self.binrange[0], self.binrange[1], yval, yerr)

    def compareWithInterpolation(self, ipol, testpoints, relerrlim=1e-10):
        for tp in testpoints:
            y_ipol = ipol.getValue(tp.getScaled())
            y_dist = self.ydist(tp)
            if abs((y_ipol-y_dist)/y_dist) > relerrlim:
                print "Interpolation failed: %g (ipol) != %g (dist)"%(y_ipol,
                        y_dist)
                print "  at point:", tp
        print "finished comparsion with %i test points"%(len(testpoints))


class QuadraticDistribution(object):
    def __init__(self, **kwargs):
        """Takes either the dimension as kwarg, or quadratic, linear and
        absolute coefficients.
        """
        if kwargs.has_key("quadc"):
            self.quadc = kwargs["quadc"]
            self.linc = kwargs["linc"]
            self.absol = kwargs["absol"]
        else:
            npar = kwargs["npar"]
            self.quadc = 2*(numpy.random.rand(npar, npar) - .5)
            self.linc = 2*(numpy.random.rand(npar) - .5)
            self.absol = 2*(numpy.random.rand() - .5)

    def __call__(self, ppoint):
        psc = ppoint.getScaled()
        return (numpy.dot(psc, numpy.dot(self.quadc, psc))
                + numpy.dot(self.linc, psc) + self.absol)


class AbsoluteGaussianError(object):
    def __init__(self, width):
        self.width = width

    def error(self, par_unused):
        return numpy.random.normal(.0, self.width)

    def estimate(self, par_unused):
        return self.width


def testQuadraticInterpolation(npar, maxruns):
    """Test if the interpolation works at all, i.e. cross check
    interpolation coefficients with the coefficients of the generating
    distribution.
    """
    obsname = "Test/DummyObs"
    binrange = (0., 1.)
    binid = obsname + ":1"
    ntestpoints = 1000

    scalerdict = {}
    for i in xrange(npar):
        rvec = numpy.random.rand(2)
        rvec.sort()
        scalerdict["param%02i"%(i)] = rvec
    pg = PointGenerator(scaler=Scaler(scalerdict))
    testpoints = []
    for i in xrange(ntestpoints):
        testpoints.append(pg.nextPoint())

    qdist = QuadraticDistribution(npar=npar)
    bg = BinGenerator(obsname, binrange, qdist)
    bg.errorwanted = False
    bindist = BinDistribution(pg.scaler.getKeys(), binid)
    runs = []
    for i in xrange(max(maxruns, getInterpolationClass().minNumOfRuns(npar))):
        pp = pg.nextPoint()
        bin = bg.generate(pp)
        bindist.addRun(pp, bin)
        runs.append("%03i"%(i))
    runs = ':'.join(runs)

    print "== Testing quadratic interpolation:"
    print
    print "== used scaler for generating points:", pg.scaler
    print "== number of MC runs:", bindist.numberOfRuns()

    ipolcenter = ppFromList(numpy.zeros(npar), pg.scaler, scaled=True)
    ipolset = InterpolationSet.fromBinDists([bindist,], ipolcenter, runs)
    ipol = ipolset[binid]
    compare_coefficients(qdist, ipol, ipolcenter.getScaled())
    print

    print "comparing with test points:"
    bg.compareWithInterpolation(ipol, testpoints)

    # This is a code snippet that shows, how we can compare coefficients
    # with an interpolation centered at [0 , 0 , ...]
    # print "Comparing Coefficients: index: ipol (expected) [ , ... ]:"
    # print " center of interpolation: %s"%(ipolcenter.getScaled())
    # print
    # print "absol: %g (%g)"%(ipol.getCoefficient(None), qdist.absol)
    # print

    # lincomp = []
    # for i in xrange(npar):
        # lincomp.append("%i %g (%g)"%(i, ipol.getCoefficient(i), qdist.linc[i]))
    # print "linear:"
    # print " , ".join(lincomp)
    # print

    # quadcomp = []
    # for i in xrange(npar):
        # quadcomp.append("%i%i %g (%g)"%(i ,i, ipol.getCoefficient(i, i),
                                        # qdist.quadc[i,i]))
        # for j in xrange(i + 1, npar):
            # quadcomp.append("%i%i %g (%g)"%(i, j, ipol.getCoefficient(i, j),
                                        # qdist.quadc[i,j] + qdist.quadc[j,i]))
    # print "quadratic:"
    # print " , ".join(quadcomp)


    # now with a real center
    ipolcenter = ppFromList(numpy.random.rand(npar), pg.scaler, scaled=True)
    ipolset = InterpolationSet.fromBinDists([bindist,], ipolcenter, runs)
    ipol = ipolset[binid]

    compare_coefficients(qdist, ipol, ipolcenter.getScaled(), True)
    print
    print "comparing with test points:"
    bg.compareWithInterpolation(ipol, testpoints)

def compare_coefficients(qdist, ipol, ipolcenter, verbose=True):
    """Compare the coefficients of a QuadraticDistribution with an
    QuadraticBinInterpolation.

    This is used to test if the quadratic interpolation (i.e. the taylor
    expansion up to 2. order) yields the coefficients used to generate the
    data in the first place.

    The quadratic coefficients of the interpolation are converted from the
    coefficient vector of the interpolation to a matrix A:

        A_ii = a^2_ii and A_ij = A_ji = 0.5 * a^2_ij for i < j

    @param qdist: a quadratic distribution
    @param ipol: the quadratic bin interpolation
    @param ipolcenter: the scaled interpolation center as numpy.array
    """
    abscoefferr = 1e-6
    npar = len(ipolcenter)
    a = numpy.zeros(npar)
    for i in xrange(npar):
        a[i] = ipol.getCoefficient(i)
    A = numpy.zeros((npar, npar))
    for i in xrange(npar):
        A[i,i] = ipol.getCoefficient(i, i)
        for j in xrange(i+1, npar):
            A[i, j] = A[j, i] = .5 * ipol.getCoefficient(i, j)
    if verbose:
        print "Comparing Coefficients: index: ipol (expected) [ , ... ]:"
        print " center of interpolation: %s"%(ipolcenter)
        print
    b0 = (ipol.getCoefficient(None) - numpy.dot(a, ipolcenter)
          + numpy.dot(ipolcenter, numpy.dot(A, ipolcenter)))
    if verbose:
        print "absol: %g (%g)"%(b0 , qdist.absol)
        print

    lincomp = []
    failed = []
    for i in xrange(npar):
        # the coefficient in the generator's distribution
        a1_i = qdist.linc[i]
        # the interpolation coefficient
        b1_i = a[i] - 2*numpy.dot(A, ipolcenter)[i]
        lincomp.append("%i %g (%g)"%(i, b1_i, qdist.linc[i]))
        if abs(b1_i-a1_i) > abscoefferr:
            failed.append("%i %g != %g"%(i, b1_i, a1_i))
    if verbose:
        print "linear:"
        print " , ".join(lincomp)
        print
    if failed:
        print "linear coefficients differ:"
        print "\n".join(failed)

    quadcomp = []
    failed = []
    for i in xrange(npar):
        quadcomp.append("%i%i %g (%g)"%(i ,i, ipol.getCoefficient(i, i),
                                        qdist.quadc[i,i]))
        if abs(ipol.getCoefficient(i, i)-qdist.quadc[i,i]) > abscoefferr:
            failed.append("%i%i %g != %g"%(i, i, ipol.getCoefficient(i, i),
                                           qdist.quadc[i,i]))
        for j in xrange(i + 1, npar):
            a2_ij = qdist.quadc[i,j] + qdist.quadc[j,i]
            b2_ij = ipol.getCoefficient(i, j)
            quadcomp.append("%i%i %g (%g)"%(i, j, b2_ij, a2_ij))
            if abs(a2_ij-b2_ij) > abscoefferr:
                failed.append("%i%i %g != %g"%(i, j, b2_ij, a2_ij))
    if verbose:
        print "quadratic:"
        print " , ".join(quadcomp)
    if failed:
        print "quadcomp coefficients differ:"
        print "\n".join(failed)


def testInterpolationStoring(npar, maxruns, relerr=1.e-12):
    """Checks if the storing/loading of interpolation sets to/from xml-files
    is working. This is done by comparing the coefficients of interpolations
    with those coefficients of interpolations which are the result of
    storing and re-reading the first interpolations.
    """
    nbins = 10
    bdlist = []
    temppath = tempfile.mkstemp(prefix = "proftest")[1]

    obsname = "Test/DummyObs"
    scalerdict = {}
    for i in xrange(npar):
        rvec = numpy.random.rand(2)
        rvec.sort()
        scalerdict["param%02i"%(i)] = rvec
    pg = PointGenerator(scaler=Scaler(scalerdict))

    for i in xrange(nbins):
        binrange = (i, i+1)
        binid = "%s:%i"%(obsname, i)

        qdist = QuadraticDistribution(npar=npar)
        gaussianerr = AbsoluteGaussianError(width=.2)
        bg = BinGenerator(obsname, binrange, qdist, gaussianerr)
        bg.errorwanted = True

        bindist = BinDistribution(pg.scaler.getKeys(), binid)
        runs = []
        for i in xrange(max(maxruns,
                            getInterpolationClass().minNumOfRuns(npar))):
            pp = pg.nextPoint()
            bin = bg.generate(pp)
            bindist.addRun(pp, bin)
            runs.append("%03i"%(i))
        runs = ':'.join(runs)
        bdlist.append(bindist)

    ipolcenter = ppFromList(numpy.zeros(npar), pg.scaler, scaled=True)
    ipolset_orig = InterpolationSet.fromBinDists(bdlist, ipolcenter, runs)

    print "== Testing storing of interpolation coefficients in %iD"%(npar)

    ipolset_orig.write(temppath)
    ipolset_read = InterpolationSet.fromXML(temppath)
    for binid in ipolset_orig.iterkeys():
        corig = ipolset_orig[binid].coeffs
        cread = ipolset_read[binid].coeffs
        # print corig
        # print cread
        # print (corig - cread)/corig

        if (corig == cread).all():
            print "%s: coeffs match exactly"%(binid)

        elif (abs(((corig - cread)/corig)) <= relerr).any():
            print "%s: passed relative error test"%(binid)
        else:
            print "%s: failed, coeffs differ to stark!"%(binid)
    print "== tested all %i bins with rel. error %e"%(nbins, relerr)
    os.remove(temppath)


def testInterpolationWithData(td):
    """This function interpolates the data in the given TuningData object
    with the minimal number of needed MC runs. And then checks the value of
    the interpolation against the used MC data. The resulting number should
    be 0.0.

    2008-05-16: Works with 2008-03-18-pythia6413-4D-p21p41p81p82 .
    """
    npar = td.numberOfParams()
    IpolCls = getInterpolationClass()
    noruns = IpolCls.minNumOfRuns(npar)
    runs = td.getRunNums()[:noruns]
    print "Building single tune data ..."
    std = td.getTuneData(use_runnums = runs)
    print "  ... done."
    print "Checking interpolation:"
    for run in runs:
        mychi2 = 0.0
        pp = ParameterPoint(td.getParams(run), std.scaler, scaled=False)
        for bp in std.filteredValues():
            mychi2 += (bp.mcdict[run].getYVal() - bp.ipol.getBin(pp.getScaled()).getYVal())**2
        print "  ", run, mychi2

if __name__ == "__main__":
    # testQuadraticInterpolation(2, 0)
    testInterpolationStoring(2, 0)
    # testInterpolationStoring(5, 0)
    # testInterpolationStoring(7, 0)

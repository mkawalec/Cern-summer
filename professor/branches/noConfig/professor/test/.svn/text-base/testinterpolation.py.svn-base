"""testinterpolation.py

"""

import unittest
import numpy

from professor.histo import Bin
from professor.tools.parameter import Scaler, ppFromList
from professor.interpolation import getInterpolationClass, BinDistribution
from professor.tools.decorators import virtualmethod


class TestQuadraticPython(unittest.TestCase):
    """Unittests for the quadratic interpolation with Python."""
    """Baseclass for unit tests for the interpolation code."""
    obsname = "Test/DummyObs"
    binrange = (0.0, 1.0)
    binid = obsname + ":1"
    maxdim = 12

    ipolclass = getInterpolationClass("quadratic", weave=False)

    def InterpolateAndCompare(self, dim, addanchorpoints = 0):
        # create DUMMY scaler
        scaler = Scaler(["param%02i" % (i) for i in xrange(dim)])
        center = numpy.random.rand(dim)
        numcoeffs = self.ipolclass.numOfCoefficients(dim)
        gencoeffs = numpy.random.rand(numcoeffs)

        bd = BinDistribution(scaler.getKeys(), self.binid, self.binrange)
        for i in xrange(numcoeffs + addanchorpoints):
            vec = numpy.random.rand(dim)
            yval = numpy.dot(gencoeffs,
                    self.ipolclass.getLongVector(vec - center))
            pp = ppFromList(vec, scaler)
            bd.addRun(pp, Bin(self.binrange[0], self.binrange[1], yval, 0.0))
        ipol = self.ipolclass.fromBindist(ppFromList(center, scaler), bd)
        for i in xrange(numcoeffs):
            # self.assertEqual(gencoeffs[i], ipol.coeffs[i])
            self.assertAlmostEqual(gencoeffs[i], ipol.coeffs[i], 10)

    def testLongVectorMethod(self):
        # A) with static vector
        vec = numpy.array([3.0, 2.0, 1.5])
        res = self.ipolclass.getLongVector(vec)
        self.assertEqual(1.0, res[0])

        self.assertEqual(3.0, res[1])
        self.assertEqual(2.0, res[2])
        self.assertEqual(1.5, res[3])

        self.assertEqual(3.0 * 3.0, res[4])
        self.assertEqual(3.0 * 2.0, res[5])
        self.assertEqual(3.0 * 1.5, res[6])
        self.assertEqual(2.0 * 2.0, res[7])
        self.assertEqual(2.0 * 1.5, res[8])
        self.assertEqual(1.5 * 1.5, res[9])

        # B) with random vectors
        for dim in xrange(self.maxdim + 1):
            vec = numpy.random.rand(dim)
            res = self.ipolclass.getLongVector(vec)
            self.assertEqual(1.0, res[0])
            ind = 1 + dim
            for i in xrange(dim):
                self.assertEqual(vec[i], res[i + 1])
                for j in xrange(i, dim):
                    self.assertEqual(vec[i]*vec[j], res[ind])
                    ind += 1

    def testInterpolation(self):
        for dim in xrange(self.maxdim + 1):
            self.InterpolateAndCompare(dim, 0)
            self.InterpolateAndCompare(dim, 1)
            self.InterpolateAndCompare(dim, 2)


class TestQuadraticWeave(TestQuadraticPython):
    """Unittests for the quadratic interpolation with weave."""
    ipolclass = getInterpolationClass("quadratic", weave=True)

class TestCubicPython(TestQuadraticPython):
    ipolclass = getInterpolationClass("cubic", weave=False)
    def testLongVectorMethod(self):
        # A) with static vector
        vec = numpy.array([3.0, 2.0, 1.5])
        res = self.ipolclass.getLongVector(vec)
        self.assertEqual(1.0, res[0])

        self.assertEqual(3.0, res[1])
        self.assertEqual(2.0, res[2])
        self.assertEqual(1.5, res[3])

        self.assertEqual(3.0 * 3.0, res[4])
        self.assertEqual(3.0 * 3.0 * 3.0, res[10])
        self.assertEqual(3.0 * 3.0 * 2.0, res[11])
        self.assertEqual(3.0 * 3.0 * 1.5, res[12])
        self.assertEqual(3.0 * 2.0, res[5])
        self.assertEqual(3.0 * 2.0 * 2.0, res[13])
        self.assertEqual(3.0 * 2.0 * 1.5, res[14])
        self.assertEqual(3.0 * 1.5, res[6])
        self.assertEqual(3.0 * 1.5 * 1.5, res[15])
        self.assertEqual(2.0 * 2.0, res[7])
        self.assertEqual(2.0 * 2.0 * 2.0, res[16])
        self.assertEqual(2.0 * 2.0 * 1.5, res[17])
        self.assertEqual(2.0 * 1.5, res[8])
        self.assertEqual(2.0 * 1.5 * 1.5, res[18])
        self.assertEqual(1.5 * 1.5, res[9])
        self.assertEqual(1.5 * 1.5 * 1.5, res[19])

class TestCubicWeave(TestQuadraticPython):
    ipolclass = getInterpolationClass("cubic", weave=True)


if __name__ == "__main__":
    unittest.main()

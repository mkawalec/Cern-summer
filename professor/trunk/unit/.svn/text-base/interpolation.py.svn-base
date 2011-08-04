"""interpolation.py

Unit tests for the calculation of bin interpolation coefficients.
"""

import unittest
import numpy

from professor.histo import Bin
from professor.params import ParameterPoint
from professor.interpolation import BinDistribution
from professor.interpolation.interpolation import GenericBinInterpolation
from professor.interpolation.interpolationweave import GenericWeaveBinInterpolation


class TestQuadraticPython(unittest.TestCase):
    """Unittests for the quadratic bin interpolation with Python.

    Use this as base class for tests of other interpolation classes (e.g.
    cubic, weave-versions). Change the `ipolclass` class-attribute to the
    appropriate class object.

    Attributes
    ---------
    obsname : str
        The observable name.
    Binrange : tuple of floats
        The bin range of the interpolated bin.
    maxdim : int
        The maximal dimension of the parameter space that is interpolated
        over.
    ipolclass: type
        The interpolation class that is used to calculate interpolation
        coefficients.
    """
    obsname = "Test/DummyObs"
    binrange = (0.0, 1.0)
    binid = obsname + ":1"
    # maxdim = 12
    maxdim = 3
    maxaddanchorpoints = 5

    ipolclass = GenericBinInterpolation
    order = 2
    ipol = ipolclass(order="poly%d"%order)

    def InterpolateAndCompareCoeffs(self, dim, addanchorpoints = 0):
        """Helper function to create an interpolation and compare the
        interpolation coefficients.

        The input data for the interpolation is computed by generating a
        random vector for the coefficients, use the self.ipolclass's
        getLongVector() to compute the values at the anchorpoints by
        numpy.dot'ting the long parameter vectors with the coefficients.
        Then compare the interpolation's coefficients with the generated
        coefficients with assertAlmostEqual(. , . , 10) (i.e. on 10
        decimals)
        """
        params = ["param%02i" % (i) for i in xrange(dim)]
        center = ParameterPoint(params, numpy.random.rand(dim))
        numcoeffs = self.ipol.numOfCoefficients(dim)
        gencoeffs = numpy.random.rand(numcoeffs)

        bd = BinDistribution(params, self.binid, self.binrange)
        for i in xrange(numcoeffs + addanchorpoints):
            pp = ParameterPoint(params, numpy.random.rand(dim))
            yval = numpy.dot(gencoeffs,
                    self.ipol.getLongVector(pp - center))
            bd.addRun(pp, Bin(self.binrange[0], self.binrange[1], yval, 0.0))
        ipol = self.ipolclass(bd=bd, center=center, order="poly%d"%self.order)
        for i in xrange(numcoeffs):
            # self.assertEqual(gencoeffs[i], ipol.coeffs[i])
            self.assertAlmostEqual(gencoeffs[i], ipol.coeffs[i], 10)


    def InterpolateAndCompareValues(self, dim, addanchorpoints=0):
        params = ["param%02i" % (i) for i in xrange(dim)]
        center = ParameterPoint(params, numpy.random.rand(dim))
        numcoeffs = self.ipol.numOfCoefficients(dim)

        c_lin = numpy.random.rand(dim)
        c_quad = numpy.random.rand(dim,dim)

        bd = BinDistribution(params, self.binid, self.binrange)
        for i in xrange(numcoeffs + addanchorpoints):
            pp = numpy.random.rand(dim)
            yval = numpy.dot(c_lin, pp)
            yval += numpy.dot(pp, numpy.dot(c_quad, pp))
            pp = ParameterPoint(params, pp)
            bd.addRun(pp, Bin(self.binrange[0], self.binrange[1], yval, 0.0))
        ipol = self.ipolclass(bd=bd, center=center, order="poly%d"%self.order)

        for i in xrange(100):
            pp = numpy.random.rand(dim)
            yval = numpy.dot(c_lin, pp)
            yval += numpy.dot(pp, numpy.dot(c_quad, pp))
            pp = ParameterPoint(params, pp)

            ipolval = ipol.getValue(pp)
            self.assertAlmostEqual(yval, ipolval, 10)


    def testLongVectorMethod(self):
        """Test the long vector method with assertEqual.

        A) with a static 3D vector and by-hand computed results
        B) with randomly generated vectors dim = 1,...,self.maxdim
           and a hard-coded version of the long-vector algorithm
        """
        self.ipol.order = self.order
        # A) with static vector
        vec = numpy.array([3.0, 2.0, 1.5])
        res = self.ipol.getLongVector(vec)
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
        for dim in xrange(1, self.maxdim + 1):
            vec = numpy.random.rand(dim)
            res = self.ipol.getLongVector(vec)
            self.assertEqual(1.0, res[0])
            ind = 1 + dim
            for i in xrange(dim):
                self.assertEqual(vec[i], res[i + 1])
                for j in xrange(i, dim):
                    self.assertEqual(vec[i]*vec[j], res[ind])
                    ind += 1


    def testInterpolation(self):
        """Test the interpolation for dim = 1, .. , self.maxdim with 0, 1, 2
        additional anchor points.
        """
        self.ipol.order = self.order
        for dim in xrange(1, self.maxdim + 1):
            for addanchorpoints in xrange(self.maxaddanchorpoints + 1):
                self.InterpolateAndCompareCoeffs(dim, addanchorpoints)
                self.InterpolateAndCompareValues(dim, addanchorpoints)


    def InterpolateAndGetGradient(self, dim):
        params = ["param%02i" % (i) for i in xrange(dim)]
        center = ParameterPoint(params, numpy.random.rand(dim))
        # Dice random coefficients (make sure the quad. coeffs matrix is
        # symmetric).
        c_lin = numpy.random.rand(dim)
        c_quad = numpy.random.rand(dim, dim)
        # c_quad = c_quad + c_quad.T - numpy.diag(c_quad.diagonal())
        c_quad = 0.5*(c_quad + c_quad.T)

        bd = BinDistribution(params, self.binid, self.binrange)
        for i in xrange(self.ipol.minNumOfRuns(dim)):
            p = numpy.random.rand(dim)
            yval = numpy.dot(c_lin, p)
            yval += numpy.dot(p, numpy.dot(c_quad, p))
            p = ParameterPoint(params, p)
            bd.addRun(p, Bin(self.binrange[0], self.binrange[1], yval, 0.0))
        ipol = self.ipolclass(bd=bd, center=center,order="poly%d"%self.order)

        p = numpy.random.rand(dim)

        grad = ipol.getGradient(p)
        for k in xrange(dim):
            grad_k = c_lin[k]
            grad_k += 2*numpy.dot(c_quad[k], p)

            self.assertAlmostEqual(grad[k], grad_k, 10)

        # Test that the optional `k` parameter is working.
        for k in xrange(dim):
            grad_k = ipol.getGradient(p, k)
            self.assertEqual(grad[k], grad_k)


    def testGradient(self):
        self.ipol.order = self.order
        for dim in xrange(1, self.maxdim + 1):
            self.InterpolateAndGetGradient(dim)


    def testGradientByHand2D(self):
        self.ipol.order = self.order
        numpy.random.seed(10)
        dim = 2
        params = ["param%02i" % (i) for i in xrange(dim)]
        center = ParameterPoint(params, numpy.random.rand(dim))

        c_lin = numpy.asarray([1., 2.])
        c_quad = numpy.asarray([[4., 1.],
                                [1., 2.]])
        dx = lambda p: 8*p[0] + 2*p[1] + 1
        dy = lambda p: 2*p[0] + 4*p[1] + 2
        
        bd = BinDistribution(params, self.binid, self.binrange)
        for i in xrange(self.ipol.minNumOfRuns(dim)):
            p = numpy.random.rand(dim)
            yval = numpy.dot(c_lin, p)
            yval += numpy.dot(numpy.dot(c_quad, p), p)
            p = ParameterPoint(params, p)
            bd.addRun(p, Bin(self.binrange[0], self.binrange[1], yval, 0.0))
        ipol = self.ipolclass(bd=bd, center=center,order="poly%d"%self.order)

        for i in xrange(10):
            p = numpy.random.rand(dim)
            self.assertAlmostEqual(ipol.getGradient(p, 0), dx(p), 10)
            self.assertAlmostEqual(ipol.getGradient(p, 1), dy(p), 10)

            # Test the way the gradient is automatically calculated.
            grad_x = c_lin[0] +  2*numpy.dot(c_quad[0], p)
            grad_y = c_lin[1] + 2*numpy.dot(c_quad[1], p)
            self.assertEqual(grad_x, dx(p))
            self.assertEqual(grad_y, dy(p))

        p = numpy.random.rand(dim)
        for k in xrange(dim):
            grad_k = c_lin[k] + 2*numpy.dot(c_quad[k], p)

            self.assertAlmostEqual(ipol.getGradient(p, k), grad_k, 10)

        p = numpy.random.rand(dim)
        # Test the optional `k` parameter.
        grad = ipol.getGradient(p)
        for k in xrange(dim):
            grad_k = ipol.getGradient(p, k)
            self.assertEqual(grad[k], grad_k)



class TestQuadraticWeave(TestQuadraticPython):
    """Unittests for the quadratic interpolation with weave."""
    ipolclass = GenericWeaveBinInterpolation



class TestCubicPython(TestQuadraticPython):
    ipolclass = GenericBinInterpolation
    order = 3
    ipol = ipolclass(order="poly3")

    def testLongVectorMethod(self):
        """Test the long vector method with assertEqual.

        A) with a static 3D vector and by-hand computed results
        """
        # A) with static vector
        vec = numpy.array([3.0, 2.0, 1.5])
        res = self.ipol.getLongVector(vec)
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


    def InterpolateAndCompareValues(self, dim, addanchorpoints=0):
        params = ["param%02i" % (i) for i in xrange(dim)]
        center = ParameterPoint(params, numpy.random.rand(dim))
        numcoeffs = self.ipol.numOfCoefficients(dim)

        c_lin = numpy.random.rand(dim)
        c_quad = numpy.random.rand(dim,dim)
        c_cube = numpy.random.rand(dim, dim, dim)

        bd = BinDistribution(params, self.binid, self.binrange)
        for i in xrange(numcoeffs + addanchorpoints):
            pp = numpy.random.rand(dim)
            yval = numpy.dot(c_lin, pp)
            yval += numpy.dot(numpy.dot(c_quad, pp), pp)
            yval += numpy.dot(numpy.dot(numpy.dot(c_cube, pp), pp), pp)
            pp = ParameterPoint(params, pp)
            bd.addRun(pp, Bin(self.binrange[0], self.binrange[1], yval, 0.0))
        ipol = self.ipol.fillFromBinDistribution(bd, center)

        for i in xrange(100):
            pp = numpy.random.rand(dim)
            yval = numpy.dot(c_lin, pp)
            yval += numpy.dot(numpy.dot(c_quad, pp), pp)
            yval += numpy.dot(numpy.dot(numpy.dot(c_cube, pp), pp), pp)
            pp = ParameterPoint(params, pp)

            ipolval = ipol.getValue(pp)
            self.assertAlmostEqual(yval, ipolval, 10)


    def InterpolateAndGetGradient(self, dim):
        params = ["param%02i" % (i) for i in xrange(dim)]
        center = ParameterPoint(params, numpy.random.rand(dim))
        numcoeffs = self.ipol.numOfCoefficients(dim)

        c_lin = numpy.random.rand(dim)
        # Dice random coefficients (make sure the quad. and cubic coeffs
        # matrices are symmetric).
        c_quad = numpy.random.rand(dim,dim)
        c_quad = 0.5*(c_quad + c_quad.T)

        c_cube = numpy.random.rand(dim, dim, dim)
        # Could be done with itertools.permutations(range(3), 3), but this
        # is only avaible from Python2.6 on.
        permuts = ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1),
                   (2, 1, 0))
        t = numpy.zeros((dim, dim, dim))
        for p in permuts:
            t += c_cube.transpose(p)
        c_cube = t/float(len(permuts))

        bd = BinDistribution(params, self.binid, self.binrange)
        for i in xrange(numcoeffs):
            pp = numpy.random.rand(dim)
            yval = numpy.dot(c_lin, pp)
            yval += numpy.dot(numpy.dot(c_quad, pp), pp)
            yval += numpy.dot(numpy.dot(numpy.dot(c_cube, pp), pp), pp)
            pp = ParameterPoint(params, pp)
            bd.addRun(pp, Bin(self.binrange[0], self.binrange[1], yval, 0.0))
        ipol = self.ipolclass(bd=bd, center=center,order="poly%d"%self.order)

        p = numpy.random.rand(dim)

        # Check that c_cube is symmetric.
        for k in xrange(dim):
            r0 = numpy.dot(numpy.dot(c_cube[k], p), p)
            r1 = numpy.dot(numpy.dot(c_cube[:,k], p), p)
            r2 = numpy.dot(numpy.dot(c_cube[:,:,k], p), p)
            self.assertTrue((abs(r0 - r1) < 1e-15).all())
            self.assertTrue((abs(r0 - r2) < 1e-15).all())

        grad = ipol.getGradient(p)
        for k in xrange(dim):
            grad_k = c_lin[k]
            grad_k += 2*numpy.dot(c_quad[k], p)
            grad_k += 3*numpy.dot(numpy.dot(c_cube[k], p), p)

            self.assertAlmostEqual(grad[k], grad_k, 10)


    def testGradientByHand1D(self):
        dim = 1
        params = ["param%02i" % (i) for i in xrange(dim)]
        center = ParameterPoint(params, numpy.random.rand(dim))

        poly = lambda p: 2*p[0]**3
        dx = lambda p: 6*p[0]**2

        bd = BinDistribution(params, self.binid, self.binrange)
        for i in xrange(self.ipol.minNumOfRuns(dim)):
            p = numpy.random.rand(dim)
            yval = poly(p)
            p = ParameterPoint(params, p)
            bd.addRun(p, Bin(self.binrange[0], self.binrange[1], yval, 0.0))
        ipol = self.ipol.fillFromBinDistribution(bd, center)

        for i in xrange(10):
            p = numpy.random.rand(dim)
            self.assertAlmostEqual(ipol.getGradient(p, 0), dx(p), 10)



class TestCubicWeave(TestCubicPython):
    ipolclass = GenericWeaveBinInterpolation


if __name__ == "__main__":
    unittest.main()

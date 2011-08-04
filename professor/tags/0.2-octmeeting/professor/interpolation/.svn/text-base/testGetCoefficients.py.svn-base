#!/usr/bin/env python
# vim:fileencoding=utf-8
"""testGetCoefficients.py

Test code for the BinDistribution.getCoefficient(...) method.

Runs the interpolation on a non-smeared paraboloid and compares the return
values of getCoefficient(...) with parameters which were calculated.
Comparsion is done by printing out by-hand-calculated value vs. the return
value of getCoefficient(...).

Result: method works ;)
"""

import numpy, pylab
from professor.interpolation.analytic_interpolation import BinDistribution
from professor.histo import Bin
#from professor.interpolation.testBase import randomPoint


def test_getCoefficient(dim, f, a):
    """Tests the BinDistribution.getCoefficient(...) method.

    Runs the interpolation on a non-smeared paraboloid and compares the return
    values of getCoefficient(...) with parameters which were calculated.
    Comparsion is done by printing out by-hand-calculated value vs. the return
    value of getCoefficient(...).

    @param dim: the number of dimensions
    @type  dim: C{int}
    @param f: the function for the paraboloid
    @param a: list with the parameters calculated by hand stored in sublists,
        the indices must fit the parameters, e.g.
        a^2_23 -> a[1][1][2]
    @type  a: C{list}
    """

    parameternames = ["param%i"%(i) for i in xrange(dim)]
    bd = BinDistribution('obs', [.0, .1], parameternames)
    bd.setCenter(numpy.zeros(dim))

    arr = []
    for i in xrange(bd.requiredRuns()):
        # p = randomPoint(dim)
        p = numpy.random.rand(dim)
        v = Bin(.0, .1, yval=f(p))
        bd.addRun(v, p)
        arr.append((p[0],p[1],p[2], f(p)))
        # pylab.plot(f(p))
        # print p[0], f(p)
        # pylab.subplot(312)
        # pylab.plot(p[1], f(p))
        # pylab.subplot(313)
        # pylab.plot(p[2], f(p))
    X = numpy.array(arr)
    pylab.subplot(311)
    pylab.plot(X[:,0], X[:,3]/max(abs(X[:,3])), 'rx')
    pylab.subplot(312)
    pylab.plot(X[:,1], X[:,3], 'rx')
    pylab.subplot(313)
    pylab.plot(X[:,2], X[:,3], 'rx')
    pylab.show()
    bd.calcInterpolationCoefficients()
    #print bd.coefficients
    #print
    print "a^0_0   %f    (%f expected)"%(bd.getCoefficient(), a[0][0])
    for i1 in xrange(dim):
        print "a^1_%i  %f    (%f expected)"%(i1+1, bd.getCoefficient(i1), a[1][i1])
    for i1 in xrange(dim):
        for i2 in xrange(i1, dim):
            print "a^2_%i%i  %f    (%f expected)"%(i1+1, i2+1,
                            bd.getCoefficient(i1, i2), a[2][i1][i2])


def MCAnswer(par, bin):
    pass


if __name__ == "__main__":
    print __doc__

    dim = 3

    def f(x_):
        x, y, z = x_[0], x_[1], x_[2]
        return (2.*x - .5)**2 + (3.*y - .2)**2 + (z - .9)**2 + 5*x*y + 13*x*z

    # the parameters, calculated by hand for a concrete f(x_)
    a = [ [1.1],
          [-2, -1.2, -1.8],
          [ [4., 5., 13.],
            [None, 9., 0.],
            [None, None, 1.] ]
        ]

    test_getCoefficient(dim, f, a)

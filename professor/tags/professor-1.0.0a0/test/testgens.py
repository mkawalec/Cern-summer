"""testgens.py

"""

import numpy
from professor.tools.parameter import Scaler
from professor.test.generator import *
from professor.test.dists import *

import pylab


def testBinGenerator(dim):
    sc = Scaler(["param%i"%(i) for i in xrange(dim)])
    print sc
    dist = Paraboloid(numpy.random.rand(dim))
    gen = BinGenerator(sc)
    gen.setDist(dist=dist)
    for i in xrange(10):
        pp, bin = gen.next()
        print i
        print pp
        print

def testMinDistGenerator(dim):
    sc = Scaler(["param%i"%(i) for i in xrange(dim)])
    # print sc
    dist = Paraboloid(numpy.random.rand(dim))
    gen = MinDistanceGenerator(sc)
    gen.setDist(dist=dist)
    nop = 6

    ps = -1. * numpy.ones((nop, dim))

    for i,(pp, bin) in enumerate(gen(nop)):
        print i
        print pp
        ps[i,:] = pp.getUnscaled()
        print
    print ps

    for y in xrange(dim):
        pylab.plot(ps[:,y], y*numpy.ones(nop), 'o')
    pylab.show()

testMinDistGenerator(3)

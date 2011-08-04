"""test.py

tests if the new algorithm for creating long parameter vectors works the
same way the old one did.

"""

from professor.interpolation.interpolation import QuadraticInterpolation

def old(nop):
    retvec = range(QuadraticInterpolation.numberOfCoefficients(nop))
    hor_index = 1

    for j in xrange(nop):
        retvec[hor_index] = "p%i"%(j)
        hor_index += 1

    for j in xrange(nop):
        for k in xrange(j, nop):
            retvec[hor_index] = "p%i*p%i"%(j, k)
            hor_index += 1

    return retvec

def new(nop):
    retvec = range(QuadraticInterpolation.numberOfCoefficients(nop))
    ind1, ind2 = 1, nop + 1
    for j in xrange(nop):
        retvec[ind1] = 'p%i'%(j)
        ind1 += 1
        for k in xrange(j, nop):
            retvec[ind2] = "p%i*p%i"%(j, k)
            ind2 += 1

    return retvec


for dim in xrange(0, 10):
    print "="*10, dim, "="*10
    o = old(dim)
    n = new(dim)
    print o == n
    # print old(dim)
    # print new(dim)
    print

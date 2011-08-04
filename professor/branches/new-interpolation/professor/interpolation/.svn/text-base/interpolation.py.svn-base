"""interpolation.py

"""

from professor.tools.config import Config
from professor.tools.decorators import virtualmethod

import warnings, numpy, numpy.dual

_logger = Config().getLogger('interpolation')


class InterpolationError(Exception):
    pass


class BaseBinInterpolation(object):
    #@cvar method: string used to identify the interpolation method
    method = None
    @classmethod
    def fromXML(cls, center, elem):
        binid = elem.get("binid")
        coeffs = []
        for pel in sorted(elem.findall("Coefficient"), key=lambda i: int(i.get("index"))):
            assert len(coeffs) == int(pel.get("index"))
            coeffs.append(float(pel.get("value")))
        return cls(binid, coeffs, center)

    def asXMLElement(self):
        ret = ET.Element("Interpolation", {"method": self.method,
                                           "binid" : self.binid})
        for i, c in enumerate(self.coeffs):
            ET.SubElement(ret, "Coefficient", {"index":"%i"%(i),
                                               "value":"%g"%(c)})
        return ret

    @virtualmethod
    @classmethod
    def fromBindist(cls, center, bd):
        pass

    @virtualmethod
    @staticmethod
    def getLongVector(p):
        pass

    def __init__(self, binid, coeffs, center):
        self.binid = binid
        if type(coeffs) != numpy.ndarray:
            coeffs = numpy.array(coeffs)
        self.coeffs = coeffs
        self.center = center

    def getValue(self, p):
        """Returns the interpolation value for an already scaled parameter
        vector.

        @param p: the parameter vector from the normed hypercube.
        @type p: numpy.ndarray
        """
        DP = self.getLongVector(p - self.center)
        return numpy.dot(DP, self.coeffs)

    def getCoefficient(self, i1=None, i2=None):
        """Returns an interpolation coefficient.

        Return values are::
            a^0_0          if i1 == None
            a^1_i1         if i1 != None and i2 == None
            a^2_(i1,i2)    if i1 != None and i2 != None

        Indices run from 0 to n-1 , where n is the number of parameters!

        @raise InterpolationError: if i1 > i2 or i1, i2 > dim.
        """
        if i1 is None and i2 is None:
            ind = 0
        elif i1 is not None and i2 is None:
            # we want a linear coefficient
            if i1 > self.getBD().dim():
                raise InterpolationError("Index i1 must not be greater than"
                                         " dimension")
            ind = i1 + 1
        else:
            # now we want a quadratic coefficient TODO dim!
            if i1 > self.getBD().dim():
                raise InterpolationError("Index i1 must not be greater than"
                                         " dimension")
            if i2 > self.getBD().dim():
                raise InterpolationError("Index i2 must not be greater than"
                                         " dimension")
            ind = 1 + len(self.getBD())

            if i1 > i2:
                raise InterpolationError("Index i1 must not be greater" +
                        " than i2!")
                # make i1 <= i2
                #i1, i2 = i2, i1

            for n in xrange(i1):
                ind += len(self.getBD()) - n

            ind += i2 - i1

        #print i1, i2, ind
        return self.coeffs[ind]

    @virtualmethod
    @staticmethod
    def numOfCoefficients(dim):
        pass

    @virtualmethod
    def minNumOfRuns(dim):
        pass


class QuadraticBinInterpolation(BaseBinInterpolation):
    method = "quadratic"
    @classmethod
    def fromBindist(cls, center, bd):
        dim = bd.dim()
        if bd.numberOfRuns() < cls.minNumOfRuns(dim):
            raise ValueError("Not enough runs for this interpolation!")

        DP = numpy.ones(( bd.numberOfRuns(),
                          cls.numOfCoefficients(dim) ))
        MC = numpy.zeros(bd.numberOfRuns())
        for i, (params, bin) in enumerate(bd):
            center.goodPartner(params)
            MC[i] = bin.getYVal()

            dp = params.getScaled() - center.getScaled()

            DP[i] = cls.getLongVector(dp)

        DP_inv = numpy.dual.pinv(DP)
        coeffs = numpy.dot(DP_inv, MC)
        binid = bd.binid
        return cls(binid, coeffs, center.getScaled())

    @staticmethod
    def getLongVector(p):
        """Return a row vector with relevant combinations of the parameter
        values.

        Used for computing both the interpolation coefficients and the
        results of the interpolation.

        @type  p: C{numpy.ndarray} instance.
        @rtype: C{numpy.ndarray}
        """
        # stores the long row vector, entries are:
        # ( 1. , p_1 , ... , p_n , 
        #     p_1*p_1 , p_1*p_2 , ... , p_1*p_n ,
        #     p_2*p_2 , p_2*p_3 , ... , p_2*p_n ,
        #                      ...
        #                                   p_n*p_n )
        nop = len(p)
        retvec = numpy.ones(QuadraticBinInterpolation.numOfCoefficients(nop))

        ind1 = 1
        ind2 = nop + 1

        for j in xrange(nop):
            retvec[ind1] = p[j]
            ind1 += 1
            for k in xrange(j, nop):
                retvec[ind2] = p[j]*p[k]
                ind2 += 1

        return retvec

    @staticmethod
    def numOfCoefficients(dim):
        return 1 + dim + dim*(dim+1)/2
    minNumOfRuns = numOfCoefficients


def getInterpolationClass(method=None):
    if method is None:
        method = Config().getOption('interpolation', 'method')

    if method == "quadratic":
        return QuadraticBinInterpolation

    raise ValueError("Unknown interpolation method '%s'!"%(method))


"""interpolationweave.py

The Quadratic and cubic interpolations from interpolation.py but using
inlined C++ code to fill long parameter vectors. Speed-ups by about
factor 5!

To use the weave version, use the "--use-weave" command line option or set
the "use weave" configuration option, defaults to "False" by the moment.

Put in a separate file to allow plain Python interpolations in case
weave/SciPy is not available.
"""

import numpy
from scipy import weave
from interpolation import QuadraticBinInterpolation, CubicBinInterpolation


class QuadraticBinInterpolationWeave(QuadraticBinInterpolation):
    @classmethod
    def getLongVector(cls, p):
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
        retvec = numpy.ones(cls.numOfCoefficients(nop))

        code = """
            int ind1 = 1;
            int ind2 = 1 + nop;

            for (int i = 0; i < nop; i++) {
                retvec[ind1] = p[i];
                ind1++;
                for (int j = i; j < nop; j++) {
                    retvec[ind2] = p[i] * p[j];
                    ind2++;
                }
            }
            """
        weave.inline(code, ["retvec", "p", "nop"])
        return retvec


class CubicBinInterpolationWeave(CubicBinInterpolation):
    @classmethod
    def getLongVector(cls, p):
        nop = len(p)
        retvec = numpy.ones(CubicBinInterpolation.numOfCoefficients(nop))
        #
        # # For testing fill the parameter with NaN's
        # retvec = numpy.zeros(cls.numOfCoefficients(nop)) * numpy.NaN
        # retvec[0] = 1.0
        code = """
            int ind1 = 1;
            int ind2 = 1 + nop;
            int ind3 = 1 + nop + nop*(nop+1)/2;
            for (int i = 0; i < nop; i++) {
                retvec[ind1] = p[i];
                ind1++;
                for (int j = i; j < nop; j++) {
                    retvec[ind2] = p[i]*p[j];
                    ind2++;
                    for (int k = j; k < nop; k++) {
                        retvec[ind3] = p[i]*p[j]*p[k];
                        ind3++;
                    }
                }
            }
            """
        weave.inline(code, ["retvec", "p", "nop"])
            #, type_converters=weave.converters.blitz, compiler="gcc") 
        return retvec

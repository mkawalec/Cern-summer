# encoding: utf8
"""interpolationweave.py

The Quadratic and cubic interpolations from interpolation.py but using
inlined C++ code to fill long parameter vectors. Speed-ups by about
factor 5!

To use the weave version, use the "--use-weave" command line option or set
the "use weave" configuration option, defaults to "True" by the moment.

Put in a separate file to allow plain Python interpolations in case
weave/SciPy is not available.
"""

import numpy
from scipy import weave
from interpolation import *

class GenericWeaveBinInterpolation(GenericBinInterpolation):
    """Extending 'GenericBinInterpolation' with inline C-code
    execution for speed.
    
    See superclasses documentation for details.
    
    """
    __init__ = GenericBinInterpolation.__init__
    
    def getLongVector(self, p):
        """
        Creates C source code from class configuration 
        (number of params, order of polynomial) and stores this.
        
        If cls.code available, run with weave.inline.
        """
        def numOfCoefficients(dim, order):
            """The number of coefficients for a `dim` dimensional space.

            Parameters
            ----------
            dim : int
            """
            def binomial(n,k):
                ntok = 1
                for t in xrange(min(k,n-k)):
                    ntok = ntok*(n-t)//(t+1)
                return ntok
            return binomial(dim+order,order)
            
        nop = len(p)
        noc = self.numOfCoeffs #numOfCoefficients(nop,self.order)
        retvec = numpy.empty(noc)
        retvec[0] = 1
        
        try:
            code = cls.code[(noc,nop)]
        except:
            code_init = "\n".join("int ind%d = %d;" % (i+1, numOfCoefficients(nop, i)) for i in xrange(self.order))

            code_for0 = """for (int i1 = 0; i1 < nop; i1++) {
                retvec[ind1] = (double) p[i1];
                ind1++; """
            code_forj = """for (int i%d = i%d; i%d < nop; i%d++) {
                retvec[ind%d] = %s;
                ind%d++; """
            code_for = "\n".join(code_forj % (j+1, j, j+1, j+1, j+1, "*".join("(double) p[i%d]" % (i+1) for i in xrange(j+1)), j+1) for j in xrange(1,self.order))

            code = "\n".join((
                code_init, 
                code_for0, 
                code_for,
                "\n}"*int(self.order)
                ))
            try:
                self.code[(noc,nop)] = code
            except AttributeError:
                self.code = {(noc,nop): code}
        weave.inline(code, ['retvec', 'p', 'nop'])
        return retvec

##### Backward compatibiliy section #####

class QuadraticBinInterpolationWeave(QuadraticBinInterpolation):
    pass
class CubicBinInterpolationWeave(CubicBinInterpolation):
    pass
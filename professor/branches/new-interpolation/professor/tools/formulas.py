"""formulas.py

"""

import numpy, scipy

# statistical formulas
def rms(alist):
    """ calculates the rms from a list """
    if len(alist) > 1:
        return numpy.sqrt(sum([(i - numpy.mean(alist))**2
            for i in alist])/(len(alist)-1.))
    else:
       raise StandardError('more than one item needed to calculate rms')

def noverk(n,k):
    """ calculate the binomial coefficent of n over k """
    return  scipy.factorial(n)/(scipy.factorial(k)*scipy.factorial(n-k))

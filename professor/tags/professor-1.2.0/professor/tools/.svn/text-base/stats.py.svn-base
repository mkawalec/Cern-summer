"""
Functions for statistical measures and correlations.
"""

import numpy, scipy
from professor.tools import log as logging


def rms(alist):
    """
    Compute the RMS of a number list.
    """
    if len(alist) > 1:
        listsum = sum((i - numpy.mean(alist))**2 for i in alist)
        return numpy.sqrt(listsum/(len(alist) - 1.0))
    else:
       logging.warning("More than one item needed to calculate RMS, thus returning 0")
       return 0.


def weightedMean(tuplelist):
    """
    Compute weighted mean of a tuple list, e.g. [(x0, sigma x0), (x1, sigma x1), ...]
    """
    A = sum([value/sigma**2 for value, sigma in tuplelist])
    B = sum([1./sigma**2 for value, sigma in tuplelist])
    return A/B, 1./numpy.sqrt(B)


def gauss(x, mu=0, sigma=1):
    """
    Calculate value of a Gaussian at x.
    """
    exppart = numpy.exp(-(x-mu)**2/(2*sigma**2))
    norm = numpy.sqrt(2*numpy.pi)*sigma
    return exppart/norm


def n_choose_k(n, k):
    """
    Calculate the binomial coefficent of n over k

    Deprecated: this is an unsafe implementation, use prof.tools.permut.nCr instead.

    TODO: remove!
    """
    return scipy.factorial(n)/(scipy.factorial(k)*scipy.factorial(n-k))


def getCorrelation(covmat, par1, par2):
    """
    Returns the correlation of two parameters using the covariance matrix.

    covmat has to be a dictionary with keys as such: (par_i, par_j)
    e.g. as stored in MinimizationResult.covariance
    """
    return covmat[(par1, par2)]/(
            numpy.sqrt(covmat[(par1, par1)])*numpy.sqrt(covmat[(par2, par2)]))


def getCovMatFromSample(sample):
    """
    sample is a dict {PARAM:[values...] ...}
    """
    covmat={}
    means = {}
    for k, v in sample.iteritems():
        means[k] = numpy.mean(v)
    def cov_xy(x,y):
        cov = 0
        for i in xrange(len(sample[x])):
            cov += (sample[x][i] - means[x])*(sample[y][i] - means[y])
        return cov/(len(sample[x]) - 1.)
    for x in sample.keys():
        for y in sample.keys():
            covmat[(x,y)] = cov_xy(x,y)
    return covmat


def convertCovMatToArray(covmat, names=None):
    """
    This converts a dict-type correlation or covariance matrix
    into an array-type matrix, suitable for e.g. the eigenDecomposition.
    """

    if names is None:
        names = list(set(numpy.array(covmat.keys())[:,0]))
    else:
        if len(names) == int(numpy.sqrt(len(covmat.keys()))):
            pass
        else:
            raise ValueError("Number of names unequal to matrix dimension!")
    V = numpy.diag(numpy.zeros(len(names)))
    for m, x in enumerate(names):
        for n, y in enumerate(names):
            V[m][n] = covmat[(x,y)]
    return V, names


def convertCovMatToCorrMat(covmat):
    """
    This converts the dict-type covariance matrix into a dict-type
    correlation matrix.
    """
    C = {}
    for k, v in covmat.iteritems():
        C[k] = getCorrelation(covmat, k[0], k[1])
    return C


## Cluster search
def checkForClustering(plist, K, param):
    a = numpy.array([[i] for i in plist])
    for i in xrange(1, len(plist) + 1):
        clusters, labels = scipy.cluster.vq.kmeans2(a,i)
        nrofcls = []
        for j in xrange(i):
            if not list(labels).count(j) == 0:
                nrofcls.append(list(labels).count(j))
        if len(nrofcls) == i:
            logging.info('At K=%i for param %s the results seem to cluster into %i regions' % (K, param, i))

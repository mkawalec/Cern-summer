"""formulas.py

"""

import numpy, scipy, re
from scipy import cluster, linalg, matrix
# statistical formulas
def rms(alist):
    """ calculates the rms from a list """
    if len(alist) > 1:
        return numpy.sqrt(sum([(i - numpy.mean(alist))**2
            for i in alist])/(len(alist)-1.))
    else:
       print 'Warning, more than one item needed to calculate rms, thus returning 0'
       return 0.

def weightedMean(tuplelist):
    """ tuplelist: [(x0, sigma x0), (x1, sigma x1), ...] """
    A = sum([value/sigma**2 for value, sigma in tuplelist])
    B = sum([1./sigma**2 for value, sigma in tuplelist])
    return A/B, 1./numpy.sqrt(B)


def noverk(n,k):
    """ calculate the binomial coefficent of n over k """
    return  scipy.factorial(n)/(scipy.factorial(k)*scipy.factorial(n-k))


def getCorrelation(covmat, par1, par2):
    """ this returns the correlation of two parameters using the covariance
        matrix
        covmat has to be a dictionary with keys as such: (par_i, par_j)
        e.g. as stored in MinimizationResult.covariance
    """
    return covmat[(par1, par2)]/(
            numpy.sqrt(covmat[(par1, par1)])*numpy.sqrt(covmat[(par2, par2)]))


def eigenDecomposition(mat):
    """ given, that M is a symmetric,real NxN matrix, an eigen decomposition is
        always possible, such that M can be written as
        M = T_transp * S * T   (orthogonal transformation)
        with T_transp * T = 1_N and S being a diagonal matrix with the
        eigenvalues of M on the diagonal.
        The return values are:\n
                T_transp, S, T
        T and T_trans are scipy matrices, S is a list of real eigenvalues
    """
    A = matrix(mat)
    #!scipy.linalg.eig returns the transposed matrix of eigenvectors
    eigenvalues, T_trans = linalg.eig(A)
    return matrix(T_trans), map(float, map(numpy.real, eigenvalues)
            ), matrix(T_trans).transpose()


def getExtremalDirection(covmat, direction='shallow'):
    """Calculate an extremal direction (of a MinimizationResult) based on a
    diagonalised covariance matrix.
    """
    T_transp, S, T = eigenDecomposition(covmat)
    #
    # create unit vector in the rotated system (where covmat is diagonal),
    # that points in the direction of the largest diagonalised covariance
    # matrix's element
    w = list(numpy.zeros(len(S)))
    S_abs = map(abs, S)
    # use most 'extreme' eigenvalue 
    if direction=='shallow':
        ## use the, according to amount, largest eigenvalue
        w[S_abs.index(max(S_abs))] = 1.
    elif direction=='steep':
        ## use the, according to amount, smallest eigenvalue
        w[S_abs.index(min(S_abs))] = 1.
    else:
        raise StandardError("direction '%s' not supported, use 'shallow' or 'steep'")%direction
    # rotate this vector back into the original system
    return T*(matrix(w).transpose())

# helper function(s) for nicer sorting

def cmpByInt(sa, sb):
    """ compare integers found in strings
    """
    pattern = re.compile(r'[0-9]+')
    if int(pattern.findall(sa)[0]) < int(pattern.findall(sb)[0]):
        return -1
    else:
        return 1

# cluster search
def checkForClustering(plist, K, param):
    a = numpy.array([[i] for i in plist])
    for i in xrange(1, len(plist) + 1):
        clusters, labels = cluster.vq.kmeans2(a,i)
        nrofcls = []
        for j in xrange(i):
            if not list(labels).count(j) == 0:
                nrofcls.append(list(labels).count(j))
        if len(nrofcls) == i:
            print 'at K=%i for param %s the results seem to cluster into %i regions'%(K,param,i)

"""
Functions for handling eigen-decompositions of covariance matrices and the
like. Mostly kept general in terms of NumPY/SciPy data objects, although some
specifics to MinimizationResult may also occur until there's an obvious better
place to put them.
"""

import numpy
from numpy import matrix
from scipy import linalg

from decorators import deprecated
from professor.params import ParameterPoint, ParameterMatrix


def eigenDecomposition(mat):
    """
    Given a symmetric, real NxN matrix, M, an eigen decomposition is always
    possible, such that M can be written as M = T_transp * S * T (orthogonal
    transformation) with T_transp * T = 1_N and S being a diagonal matrix with
    the eigenvalues of M on the diagonal.

    Returns
    -------
    T_trans : numpy.matrix
    S : numpy.ndarray
        The real eigen values.
    T : numpy.matrix
    """
    A = matrix(mat)
    ## scipy.linalg.eig returns the transposed matrix of eigenvectors:
    S, T_trans = linalg.eig(A)
    if numpy.iscomplex(S).any():
        raise ValueError("Given matrix `mat` has complex eigenvalues!")

    return matrix(T_trans), S.real, matrix(T_trans).transpose()


def getExtremalDirections(covmat):
    """Calculate an extremal direction (of a MinimizationResult) based on a
    diagonalised covariance matrix.

    If `covmat` is a ParameterMatrix object, ParameterPoint objects are
    returned.

    Parameters
    ----------
    covmat : array_like, ParameterMatrix
        The (non-diagonal) covariance matrix.

    Returns
    -------
    shallow : numpy.ndarray, ParameterPoint
        The direction along the largest eigenvalue.
    steep : numpy.ndarray, ParameterPoint
        The direction along the smallest eigenvalue.
    """
    T_transp, S, T = eigenDecomposition(covmat)

    ishallow = S.argmax()
    isteep = S.argmin()

    # transform into plain arrays before indexing to get rid of extra
    # dimensions.
    vshallow = numpy.asarray(T_transp)[:,ishallow]
    vsteep = numpy.asarray(T_transp)[:,isteep]

    if type(covmat) == ParameterMatrix and type(vshallow) != ParameterPoint:
        vshallow = ParameterPoint(covmat.names, vshallow)

    if type(covmat) == ParameterMatrix and type(vsteep) != ParameterPoint:
        vsteep = ParameterPoint(covmat.names, vsteep)

    return vshallow, vsteep


# TODO: is this used by any one?
@deprecated("getExtremalDirections(...)[0/1]")
def getPrincipalDirections(covmat):
    T_transp, S, T = eigenDecomposition(covmat)
    ## Create unit vectors in the rotated system (where covmat is diagonal)
    s_vec = []
    for i, s in enumerate(S):
        w = list(numpy.zeros(len(S)))
        w[i] = 1.0
        ## Rotate this vector back into the original system
        ## TODO: would be better to return these vectors with same alignment as in MR, i.e. transposed again.
        vec = T * matrix(w).transpose()
        ## Correct alignment and convert to an array rather than matrix
        vec = vec.transpose()
        arr = numpy.array(vec.tolist()[0])
        ## Store as a list of (eigenvalue, eigenvec) data
        s_vec.append( (S[i], arr) )
    return sorted(s_vec, reverse=True, cmp=lambda x,y: cmp(abs(x[0]), abs(y[0])) )


# TODO: is this used by any one?
@deprecated("getExtremalDirections(...)[0/1]")
def getExtremalDirection(covmat, direction='shallow'):
    """
    Calculate an extremal direction (of a MinimizationResult) based on a
    diagonalised covariance matrix.
    """

    s_vec_list = getPrincipalDirections(covmat)

    ## Use most 'extreme' eigenvalues
    if direction == 'shallow':
        ## Use the largest eigenvalue
        return s_vec_list[0][1]
    elif direction == 'steep':
        ## Use the smallest eigenvalue
        return s_vec_list[-1][1]
    else:
        raise ValueError("direction '%s' not supported, use 'shallow' or"
                         " 'steep'" % (direction))


def transformParameter(parameter, T_transp):
    """
    This transforms a parameter into the space where a certain
    covariance matrix is diagonal.

    parameter has to be a list
    """
    return T_transp * matrix(parameter).transpose()

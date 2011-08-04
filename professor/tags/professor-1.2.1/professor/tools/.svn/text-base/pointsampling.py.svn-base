"""
Random generator tools for sampling points in a space.
"""

import numpy

from professor.tools import eigen
from professor.tools import log as logging

from professor.params import ParameterPoint, ParameterRange


class RandomPointGenerator(object):
    """Generate random parameter points.

    The numpy RNG is used.

    Attributes
    ----------
    _range : ParameterRange
        The range from which to sample.
    """
    def __init__(self, range_):
        self._range = range_

    def newPoint(self):
        """Get a new random point."""
        ran = numpy.random.rand(self._range.dim)
        return self._range.getRelativePoint(ran)

    # TODO: Is this working in parallel,i.e. two generators from one
    # PointGenerator instance?
    def generate(self, num):
        """Return a Python generator with new points.

        Parameters
        ----------
        num : int
            The number of points.
        """
        i = 0
        while i < num:
            yield self.newPoint()
            i += 1

    @staticmethod
    def seed(*args, **kwargs):
        """Pass-through to numpy.random.seed."""
        numpy.random.seed(*args, **kwargs)


class ScanPointGenerator(RandomPointGenerator):
    """Generate line scan parameter points.

    Different modes of line generation are available through factory
    functions:

    `mkDiagonal`
        sample along the diagonal of the given hyper cube
    `mkSteep`, `mkShallow`
        sample along the a line through a point of tuned values in
        the direction of the extremal uncertainties. The directions are
        calculated from the covariance matrix estimated by the minimizer.

    Attributes
    ----------
    _range : Parameterrange
        The endpoints of the line.
    """
    def newPoint(self, t):
        """Get a new point along the line.

        Parameters
        ----------
        t : float
            The position along the line.
        """
        return self._range.getRelativePoint(t)

    def generate(self, num):
        """Return a Python generator with new points.

        Parameters
        ----------
        num : int
            The number of points.
        """
        ts = numpy.linspace(0.0, 1.0, num, endpoint=True)
        for t in ts:
            yield self.newPoint(t)

    @classmethod
    def mkDiagonal(cls, range_, pivot=None, symmetric=False):
        """Return a point generator along the diagonal of `range_`."""
        return cls(range_)

    @classmethod
    def mkSubRangeDiagonal(cls, range_, center):
        """Return a point generator along the diagonal of the maximal
        sub-hypercube of `range_` centered at `center`.

        The direction is parallel to the diagonal of range_.

        Parameters
        ----------
        center : ParameterPoint
            A point, defining the center of the sub-range.
        """
        # create a dummy direction vector
        direction = ParameterPoint(range_.names, numpy.ones(range_.dim))
        endpts = cls._getEndPoints(range_, center, direction, True)
        return cls(endpts)

    @classmethod
    def mkShallow(cls, range_, result, symmetric=False):
        """Return a point generator along the 'shallow' direction of the
        covariance matrix from `result`.

        Parameters
        ----------
        range_ : ParameterRange
            The extremal parameter values that are allowed.
        result : MinimisationResult
        symmetric : bool
            Make the line symmetric around `result`.
        """
        grad = cls._getGradient(result, "shallow")
        endpoints = cls._getEndPoints(range_, result.values, grad, symmetric)
        return cls(endpoints)

    @classmethod
    def mkSteep(cls, range_, result, symmetric=False):
        """Return a point generator along the 'steep' direction of the
        covariance matrix from `result`.

        Parameters
        ----------
        range_ : ParameterRange
            The extremal parameter values that are allowed.
        result : MinimisationResult
        symmetric : bool
            Make the line symmetric around `result`.
        """
        grad = cls._getGradient(result, "steep")
        endpoints = cls._getEndPoints(range_, result.values, grad, symmetric)
        return cls(endpoints)


    # TODO: put this somewhere else?
    @staticmethod
    def _getGradient(result, direction):
        """Return the 'steep'/'shallow' direction vector for `result`.

        Parameters that were fixed during minimization have a gradient
        component of 0.

        Parameters
        ----------
        result : MinimizationResult
        direction : ('steep' | 'shallow')

        Returns
        -------
        grad : ParameterPoint
            The normalized direction vector.
        """
        # make `direction` into an index for the return tuple of
        # eigen.getExtremalGradient
        try:
            direction = ["shallow", "steep"].index(direction)
        except ValueError:
            raise ValueError("Argument direction must be 'shallow' or 'steep'")

        grad = eigen.getExtremalDirections(result.covariance)[direction]

        # If no parameters were fixed, were done an can return the
        # direction.
        if len(result.fixedparameters) == 0:
            return grad
        # If parameters were fixed grad does not contain any information
        # about them. So add some zeros in this case.
        # initialize with zeros this way we only need to set 
        grad2 = ParameterPoint(result.names, numpy.zeros(result.dim))
        for name in grad.names:
            grad2[name] = grad[name]
        return grad2

    # TODO check that this works!
    @staticmethod
    def _getEndPoints(range_, center, direction, symmetric):
        """Get end points for a scan line.

        Get the points where a line from point `center` in `direction`
        first hits the boundaries in `range_`.

        The endpoints are the intersection points of the line with the
        surrounding hypercube. The line goes through the given
        MinimizationResult.

        If the hypercube is centered around the MinimizationResult this
        points should be symmetric around the center of the hypercube.

        Parameters
        ----------
        range_ : ParameterRange
        center : ParameterPoint
        direction : ParameterPoint
            It must not necessarily be normalized.
        symmetric : bool
            Make the line symmetric around `center`.

        Returns
        -------
        endpoints : ParameterRange
        """
        if not range_.isInside(center):
            raise ValueError("center not in range_")

        # this might give INFs if direction contains 0.0
        t_low = (range_.low - center)/direction
        t_high = (range_.high - center)/direction

        logging.trace("l:" + str(t_low))
        logging.trace("h:" + str(t_high))

        ts = numpy.concatenate((t_low, t_high))
        # remove INFs
        ts = ts[numpy.negative(numpy.isinf(ts))]

        # Now we need the smallest and second-smallest abs(t-values) with
        # opposite signs.
        i1 = numpy.argmin(abs(ts))
        t1 = ts[i1]
        # t2 is minimum of all t-values with opposite sign of t1
        if t1 < 0.0:
            t2 = (ts[ts > 0.0]).min()
        else:
            t2 = (ts[ts < 0.0]).max()

        if symmetric:
            logging.info("Making line end points symmetric around given center")
            if abs(t1) > abs(t2):
                t1 = -t2
            else:
                t2 = -t1

        low = center + t1*direction
        high = center + t2*direction

        # print "1[%s]  2[%s]" % (t1, t2)
        # print low
        # print "=="
        # print high
        # print "=="
        endpoints = ParameterRange(low.names, zip(low, high))

        # This should never raise.
        if (not range_.isInside(endpoints.low)
                or not range_.isInside(endpoints.high)):
            raise ValueError("Calculated endpoints outside of original range!")

        return endpoints

    # make seed() not work here
    @staticmethod
    def seed(*args, **kwargs):
        raise RuntimeError("ScanPointGenerator.seed should never be called!")

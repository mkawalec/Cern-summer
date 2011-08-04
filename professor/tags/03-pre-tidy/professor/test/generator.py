"""generator.py

Holds a fake generator for bin distributions.

Intended to be used for testing the interpolation/minimization.
"""

from professor.histo import Bin
from professor.tools.parameter import ppFromList
from professor.tools.config import Config

import numpy.random

_log = Config().getLogger('test')

class PointGenerator(object):
    def __init__(self, scaler):
        self._scaler = scaler
        self._remainingruns = 0

    def __call__(self, runs):
        self._remainingruns = runs
        return self

    def __iter__(self):
        return self

    def nextRawPoint(self):
        return numpy.random.rand(len(self._scaler))

    def next(self):
        """Returns the next (ParameterPoint, Bin) pair."""
        if self._remainingruns <= 0:
            raise StopIteration
        self._remainingruns -= 1

        praw = self.nextRawPoint()
        ppoint = ppFromList(praw, self._scaler)
        return ppoint

    def getScaler(self):
        return self._scaler

    def dim(self):
        return self._scaler.dim()


class MinDistanceGenerator(PointGenerator):
    """
    minimal distance is calculated after:
    M{1/(1 + dim)^2}
    """
    def __init__(self, scaler, binrange=None):
        super(MinDistanceGenerator, self).__init__(scaler, binrange)
        self._oldpoints = []
        self._mindist = 1./(1 + len(self.getScaler()))**2

    #TODO: finish criterion method
    def isGoodPoint(self, cand):
        mindist = 1. # something to catch the case when we test the first
                     # point
        for p in self._oldpoints:
            mindist = min(mindist, min(abs(cand-p)))
            if mindist <= self._mindist:
                return False
        return True

    def nextPoint(self):
        dim = len(self._scaler)

        # while True:
        for i in xrange(1000):
            cand = numpy.random.rand(dim)
            if self.isGoodPoint(cand):
                self._oldpoints.append(cand)
                _log.info('point candidate %s passed criterion'%(cand))
                return cand
            _log.info('point candidate %s failed criterion'%(cand))
        _log.error('no usefull point after 1000 tried!')


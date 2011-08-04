"""bindistribution.py

"""

# for epydoc
__docformat__ = "epytext"


import numpy
from professor.tools.parameter import FixedSortedKeys


class BinDistribution(FixedSortedKeys):
    """Container class for (parameter, bin) pairs.
    usage should be:

        >>> bindist = BinDistribution(['dummy-par1', 'dummy-par2'], 'dummy-obs',
                  dummy_bin.getXRange())
        >>> ...
        >>> bindist.addRun(param, bin)
        >>> ...
        >>> for param, bin in bindist:
        >>>     # do whatever you need here
        >>>     pass
    """

    def __init__(self, paramnames, binid, binrange, data=None):
        """
        @param paramnames: C{list} with the parameter names
        @param obs: the observable name
        @param binrange: this bin's x range as in the L{Bin} class
        @param data: optional, a list with initial data
        """
        super(BinDistribution, self).__init__(paramnames)
        self.binid = binid
        self.binrange = binrange
        self._runs = []
        if data is not None:
            for par, bin in data:
                self.addRun(par, bin)

    def getScaler(self):
        if len(self._runs):
            return self._runs[0][0].getScaler()
        else:
            raise RuntimeError("No run added, therefore scaler does not exist.")

    def getMedianMCError(self):
        mcerrors = numpy.array([run[1].getYErr() for run in self._runs])
        return  numpy.median(mcerrors)

    def getName(self):
        return self.binid

    def addRun(self, params, bin):
        self.goodPartner(params)

        self._runs.append((params, bin))

    def __iter__(self):
        return iter(self._runs)

    def numberOfRuns(self):
        return len(self._runs)

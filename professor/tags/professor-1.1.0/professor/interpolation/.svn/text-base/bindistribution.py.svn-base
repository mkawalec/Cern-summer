import numpy
from professor.tools.errors import ParameterError
from professor.params import ParameterRange


class BinDistribution(list):
    """Container class for the distribution of MC bin contents.

    This class stores the distribution of the MC response of *one* bin for
    varying MC model parameters.

    Examples
    --------
    >>> bindist = prof.BinDistribution(['dummy-par1', 'dummy-par2'], 'dummy-obs',
    ...                                dummy_bin.getXRange())
    >>> # populate the distribution...
    >>> bindist.addRun(param, bin)
    >>> for param, bin in bindist:
    >>>     # do whatever you need here
    """

    def __init__(self, paramnames, binid, binrange, data=None):
        """Create a new BinDistribution.

        Parameters
        ----------
        paramnames : list of str
            The parameter names.
        binid : str
            The bin id, i.e. /Histo/Path:BinIndex.
        binrange : tuple of floats
            The x-range of the bin.
        data : list of (ParameterPoint, Bin) tuples, optional
            Initialise the new instance with this values.
        """
        self.paramnames = tuple(sorted(paramnames))
        self.dim = len(self.paramnames)
        self.binid = binid
        self.binrange = binrange
        if data is not None:
            for par, bin in data:
                self.addRun(par, bin)


    def getMedianMCError(self):
        """Calculate the median error of the MC data."""
        mcerrors = numpy.array([run[1].getYErr() for run in self])
        return  numpy.median(mcerrors)


    def getName(self):
        """Get the bin id."""
        return self.binid


    def addRun(self, params, bin):
        """Add a MC run to the distribution.

        Parameters
        ----------
        params : ParameterPoint
            The model parameters used in this run.
        bin : Bin
            The MC prediction in this bin.

        Raises
        ------
        ParameterError
            If `params` does not match the previously added parameters
            points.
        """
        ## Check that parameter names and scaler match the previously added
        ## parameter points.
        if self.paramnames != params.names:
            raise ParameterError("Parameter names mismatch!")

        self.append((params, bin))


    def numberOfRuns(self):
        return len(self)


    def getRanges(self):
        """Get the parameter ranges spanned by the stored runs."""
        points = [run[0] for run in self]
        cube = ParameterRange.mkFromPoints(points)
        return cube


    def __str__(self):
        return "<BinDistribution for bin %s and params %s with %i runs>" % (
                self.binid, self.paramnames, len(self))

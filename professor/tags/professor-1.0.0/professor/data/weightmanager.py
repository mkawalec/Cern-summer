"""
System for managing weight-like quantities -- e.g. observable weights, extra
error ("epsilon") factors, etc. -- which can need to be specified on a
per-observable or per-range basis.
"""

import re
import numpy

from professor.tools.errors import WeightError
from professor.tools import log as logging

from professor.tools.decorators import deprecated


class Weight(dict):
    """A simple object that holds a dict with binrange:weight pairs."""
    def __init__(self, obs):
        self.obs = obs

    def binRangeIsOk(self, binrange):
        if binrange in self.keys():
            raise WeightError("Weight already set for %s:%s" % (
                              self.obs, binrange,))
        else:
            low  = float(binrange[0])
            high = float(binrange[1])

            if low > high:
                raise WeightError("Lower edge of bin range large than upper"
                                  " edge: %s:%s" % (self.obs, binrange,))

            for br in self.keys():
                if low < float(br[1]):
                    raise WeightError("Low edge of binrange %s conflicts with"
                                      " binrange %s:%s" % (
                                      self.obs, binrange, br))
                #if high > float(br[0]):
                    #raise WeightError("Upper edge of binrange %s conflicts with binrange %s:%s"%(self.obs, binrange, br))

    def __setitem__(self, binrange, weight):
        self.binRangeIsOk(binrange)
        super(Weight, self).__setitem__(binrange, weight)

    def getWeight(self, bincenter):
        """ Evaluate the weight for bincenter by iterating over
            binrange:Weight definitions
            If the bincenter is outside the ranges, return 0
        """
        for k, v in self.iteritems():
            if float(k[0]) <= bincenter and bincenter <= float(k[1]):
                return v
        return 0.0


class WeightManager(object):
    """
    This simple object loads Weight/Epsilon files and stores a dictionary
    with observable:Weight pairs
    """
    linere = re.compile(r"([^#\s]+)\s*([-0-9e\.]+)?(?:\s*#\s*(.*)\s*)?")

    def __init__(self):
        self._weightdict = {}


    @classmethod
    @deprecated("WeightManager.mkFromFile")
    def fromFile(cls, path):
        return cls.mkFromFile(path)


    @classmethod
    def mkFromFile(cls, path):
        new = cls()
        new.loadWeightsFile(path)
        return new


    def loadWeightsFile(self, wfile):
        f = open(wfile, 'r')

        for rawline in f:
            ## Strip leading/trailing white spaces, e.g. newline
            line = rawline.strip()
            if len(line) == 0 or line.startswith('#'):
                continue
            try:
                groups = self.linere.search(line).groups()
            except Exception, e:
                logging.error("Could not parse line '%s' from observable"
                              " file '%s'" % (line, wfile))
                raise e

            name = groups[0]

            weight = groups[1]
            if weight is None:
                weight = 1.0
            else:
                weight = float(weight)

            ## Look for bin definitions
            low, high = "", ""
            try:
                path, low, high = name.split(":")
            except:
                logging.debug("No bin definition given for  `%s'" % (name))
                path = name
            if low == "":
                low = -numpy.inf
            if high == "":
                high = numpy.inf
            self.addBinRangeWeight(path, (low, high), weight)


    def addBinRangeWeight(self, observable, binrange=(-numpy.inf, numpy.inf), weight=1.0):
        """Set the weights for bins of 'observable' in 'binrange'.

        Parameters
        ----------
            observable : str
                Path of the observable.
            binrange : tuple of floats
                The x-value bin range.
            weight : float
                Weight for the bins.
        """
        if not self._weightdict.has_key(observable):
            self._weightdict[observable] = Weight(observable)
        self._weightdict[observable][binrange] = weight


    """
    Accessor for sorted list of observables, including those with zero weight.
    """
    observables = property(lambda self: sorted(self._weightdict.keys()))


    @property
    def posWeightObservables(self):
        "Return the observables that have at least one non-zero weighted bin."
        return [obs for obs, weight in self._weightdict.items()
                if max(weight.values()) > 0.0]


    """
    Indexing operator for weight lookup. Also useable as `wm["obsname"]`.
    """
    def getWeights(self, obs):
        ## TODO: how does this deal with bin-range weights?
        return self._weightdict[obs]

    __getitem__ = getWeights



    ## TODO: Provide wm.getValue("/path/to/MYHIST:42")


    def __str__(self):
        wstring = "Observables/Weights:\n"
        for obs in sorted(self.observables):
            v = self.getWeights(obs)
            wstring += "%s %s\n" % (obs, v)
        return wstring

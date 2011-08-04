"""
New interpolation architecture:

 - BinDistribution (not changed)
   stores ParameterPoint, Bin pairs

 - Interpolation
   Stores the interpolation coefficients and calculates results.
   Can be saved as Python pickle object.
   All data is stored in scaled values.

 - InterpolationSet
   Stores a scaler and a list of (ref-bin, Interpolation) pairs.
"""

from professor import histo
from professor.tools.parameter import Scaler, ParameterPoint
from professor.interpolation.interpolation import getInterpolationClass
from professor.tools.persistency import pickle


## TODO: move to tools.persistency
def loadIpol(path):
    """Load ipolset from a pickle file."""
    f = open(path, 'r')
    ipolset = pickle.load(f)
    f.close()
    return ipolset


class InterpolationSet(dict):
    @classmethod
    def fromBinDists(cls, bindists, center, runskey, ipolmethod):
        """Build an InterpolationSet from a list BinDistributions."""
        ipols = {}
        for bd in bindists:
            ipols[bd.binid] = ipolmethod.fromBindist(center, bd)
        return cls(center, runskey, ipolmethod, ipols)

    @classmethod
    def fromPickle(cls, path):
        f = open(path, "r")
        ipolset = pickle.load(f)
        f.close()
        if type(ipolset) != cls:
            raise IOError("Given file contains wrong data type: %s" % (path))
        return ipolset

    def write(self, path):
        """
        Dump IpolSet to file via pickle.
        """
        f = open(path, 'w')
        pickle.dump(self, f)
        f.close()

    def __init__(self, center, runskey, ipolmethod, ipols=None):
        """Should not be called directly: use fromBinDists or unpickle it!

        @param ipols: dict with binid - interpolation pairs
        """
        self.ipolmethod = ipolmethod
        self.center = center
        self.scaler = center.getScaler()
        self.runskey = runskey
        self._writeflag = False

        if ipols is None:
            super(InterpolationSet, self).__init__()
        else:
            super(InterpolationSet, self).__init__(ipols)

    def __repr__(self):
        return ("<InterpolationSet (method %s  runs %s) with"
                " %i interpolations>" % (
                    self.ipolmethod.__name__, self.runskey, len(self)))

    def getHistogramNames(self):
        """Return the histogram names as list.

        Returns a list with the names of all histograms for which at least
        one bin-interpolation is stored.
        """
        names = set([binid.split(":")[0] for binid in self.iterkeys()])
        return list(names)

    def setWriteFlag(self):
        self._writeflag = True

    def getWriteFlag(self):
        return self._writeflag

    def __setitem__(self, binid, ipol):
        if self.has_key(binid):
            raise ValueError("Interpolation '%s' already stored!"%(binid))
        if type(ipol) != self.ipolmethod:
            raise TypeError("Given interpolation %s of wrong type %s."
                    " Type %s expected!" % (ipol, type(ipol), self.ipolmethod))
        super(InterpolationSet, self).__setitem__(binid, ipol)

    def addInterpolation(self, ipol):
        if (ipol.center != self.center.getScaled()).any():
            raise ValueError("Given interpolation uses different center!")
        if type(ipol) != self.ipolmethod:
            raise ValueError("Given interpolation used different method!")
        self[ipol.binid] = ipol

    def addBindistribution(self, bd):
        self[bd.binid] = self.ipolmethod.fromBindist(self.center, bd)

    def sortedBinIDs(self):
        """Return a list of the sorted bin ids."""
        return sorted(self.iterkeys(), cmp=self.binIDCmp)

    @staticmethod
    def binIDCmp(idA, idB):
        """Compare bin ids first by observable name, then by numeric bin number."""
        histA, binA = idA.split(":")
        histB, binB = idB.split(":")
        ret = cmp(histA, histB)
        if ret == 0:
            return cmp(int(binA), int(binB))
        else:
            return ret

    def getObservableBins(self, observable):
        """Return an InterpolationSet with the ipols for observable."""
        new = InterpolationSet(self.center, self.runskey, self.ipolmethod)
        for binid, ipol in self.iteritems():
            if binid.split(":")[0] == observable:
                new[binid] = ipol
        return new

    def getParameterNames(self):
        return self.scaler.getKeys()

    def getInterpolationHisto(self, observable, parampoint, title=" "):
        """ Return a Histo object of an observable derived
            from the interpolation at a certain parameter point
            @param parampoint: Must be a dict, e.g. read via
            professor.tools.parameter.readParameterFile
        """
        if not observable in self.getHistogramNames():
            raise ValueError("Observable %s not amongst these:"%observable)
        obsbins = self.getObservableBins(observable)

        pointsarray = ParameterPoint(parampoint, self.scaler).getScaled()

        h = histo.Histo()
        obsBinIDs = obsbins.sortedBinIDs()
        for binID in obsBinIDs:
            h.addBin(obsbins[binID].getBin(pointsarray))
        h.name = observable
        h.title = title
        return h

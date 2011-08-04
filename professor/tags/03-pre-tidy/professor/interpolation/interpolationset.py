"""interpolationlist.py

new interpolation architecture:
 - BinDistribution (not changed)
   stores ParameterPoint, Bin pairs

 - Interpolation
   Stores the interpolation coefficients and calculates results.
   Can be saved as a xml element.
   All data is stored in scaled values.
 - InterpolationSet
   Stores a scaler and
          a list of ref-bin, Interpolation pairs.
"""
from professor import histo
from professor.tools.elementtree import ET
from professor.tools.parameter import Scaler, ParameterPoint

from interpolation import getInterpolationClass

try:
    import cPickle as pickle
except ImportError:
    print "module 'cPickle' not available, loading slower 'pickle' instead"
    import pickle

def loadIpol(path):
    """ load ipolset from a pickle file """
    f=open(path, 'r')
    ipolset=pickle.load(f)
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
    def fromXML(cls, tree):
        """build an InterpolationSet from an xml tree or file."""
        if type(tree) in (str, unicode):
            tree = ET.parse(tree)
        root = tree.getroot()
        runskey = root.get("runsKey")

        # build scaler and center
        scalerdict = {}
        centerdict = {}
        for elem in tree.findall("paramInfo"):
            scalerdict[elem.get("name")] = (float(elem.get("scalerLow")),
                                            float(elem.get("scalerHigh")))
            centerdict[elem.get("name")] = float(elem.get("center"))
        scaler = Scaler(scalerdict)
        center = ParameterPoint(centerdict, scaler)

        # build the interpolations
        ipols = {}
        for elem in tree.findall("interpolation"):
            ipolcls = getInterpolationClass(elem.get("method"))
            ipol = ipolcls.fromXML(center, elem)
            ipols[ipol.binid] = ipol

        if len(ipols) == 0:
            raise ValueError("Given xml-file or -tree does not contain"
                             " any data!")

        return cls(center, runskey, ipols)

    @classmethod
    def fromPickle(cls, path):
        f = open(path, "r")
        ipolset = pickle.load(f)
        f.close()
        if type(ipolset) != cls:
            raise IOError("Given file contains wrong data type: %s" % (path))
        return ipolset

    def asXMLElement(self):
        """Return an ElementTree.Element object with all data."""
        rootelem = ET.Element("interpolationSet", {"runsKey" : self.runskey})
        for pname in self.scaler.getKeys():
            index = self.scaler.getIndex(pname)
            ET.SubElement(rootelem, "paramInfo",
                          {"name" : pname
                          ,"index" : "%i"%(index)
                          ,"scalerLow" : "%.12g"%(self.scaler.getMinVal(pname))
                          ,"scalerHigh" : "%.12g"%(self.scaler.getMaxVal(pname))
                          ,"center" : "%.12g"%(self.center.getUnscaled()[index])
                          })
        for ipol in self.itervalues():
            rootelem.append(ipol.asXMLElement())
        return rootelem

    def write(self, path):
        """ dump IpolSet to file via pickle """
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
        h.setName(observable)
        h.setTitle(title)
        return h

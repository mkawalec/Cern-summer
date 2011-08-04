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
    def fromBinDists(cls, bindists, center, runskey, ipolcls):
        """Build an InterpolationSet from a list BinDistributions."""
        ipols = {}
        for bd in bindists:
            ipols[bd.binid] = ipolcls.fromBindist(center, bd)
        return cls(center, runskey, ipols)

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
        f=open(path, 'w')
        pickle.dump(self, f)
        f.close()

    def __init__(self, center, runskey, ipols=None):
        """Should not be called directly: use fromBinDists, fromXML!

        @param ipols: dict with binid - interpolation pairs
        """
        if ipols is None:
            super(InterpolationSet, self).__init__()
        else:
            super(InterpolationSet, self).__init__(ipols)

        self.center = center
        self.scaler = center.getScaler()
        self.runskey = runskey
        self._writeflag = False

    def setWriteFlag(self):
        self._writeflag = True

    def getWriteFlag(self):
        return self._writeflag

    def __setitem__(self, binid, ipol):
        if self.has_key(binid):
            raise ValueError("Interpolation '%s' already stored!"%(binid))
        super(InterpolationSet, self).__setitem__(binid, ipol)

    def addInterpolation(self, ipol):
        if (ipol.center != self.center.getScaled()).any():
            raise ValueError("Given interpolation uses different center!")
        self[ipol.binid] = ipol

    def addBindistribution(self, bd, ipolcls):
        self[bd.binid] = ipolcls.fromBindist(self.center, bd)

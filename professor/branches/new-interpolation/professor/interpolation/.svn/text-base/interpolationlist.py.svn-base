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


class InterpolationSet(dict):
    @classmethod
    def fromBinDists(cls, bindists, center, runskey):
        """Build an InterpolationSet from a list BinDistributions."""
        # use the configured interpolation class
        IpolClass = getInterpolationClass()
        ipols = {}
        for bd in bindists:
            ipols[bd.binid] = IpolClass.fromBindist(center, bd)
        return cls(center, runskey, ipols)

    @classmethod
    def fromXML(cls, tree):
        """build an InterpolationSet from an xml file"""
        if type(tree) in (str, unicode):
            tree = ET.parse(tree)

        runskey = tree.get("runskey")

        # build scaler and center
        scalerdict = {}
        centerdict = {}
        for elem in tree.findall("paraminfo"):
            scalerdict[elem.get("name")] = (float(elem.get("scalerlow")),
                                            float(elem.get("scalerhigh")))
            centerdict[elem.get("name")] = float(elem.get("center"))
        scaler = Scaler(scalerdict)
        center = ParameterPoint(centerdict, scaler)


        # build the interpolations
        ipols = {}
        for elem in tree.findall("interpolation"):
            ipolcls = getInterpolationClass(elem.get("method"))
            ipol = ipolcls.fromXML(center, elem)
            ipols[ipol.binid] = ipol

        return cls(center, runskey, ipols)

    def asXMLElement(self):
        """Return an ElementTree.Element object with all data."""
        rootelem = ET.Element("InterpolationSet", {"runskey" : self.runskey})
        for pname in self.scaler.getKeys():
            index = self.scaler.getIndex(pname)
            ET.Subelement(rootelem, "paraminfo",
                          {"name" : pname
                          ,"index" : "%i"%(index)
                          ,"scalerlow" : "%f"%(self.scaler.getMin(pname))
                          ,"scalerhigh" : "%f"%(self.scaler.getMax(pname))
                          ,"center" : "%f"%(self.center.getUnscaled()[index])
                          })
        for ipol in self.itervalues():
            rootelem.append(ipol.asXMLElement())
        return rootelem

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

    def __setitem__(self, binid, ipol):
        if self.has_key(binid):
            raise ValueError("Interpolation '%s' already stored!"%(binid))
        super(InterpolationSet, self).__setitem__(binid, ipol)

    def addInterpolation(self, ipol):
        if (ipol.center != self.center.getScaled()).any():
            raise ValueError("Given interpolation uses different center!")
        self[ipol.binid] = ipol

    def addBindistribution(self, bd):
        self[bd.binid] = getInterpolationClass().fromBindist(
                                    self.center, bd)

"""
New interpolation architecture:

 - BinDistribution (not changed)
   stores ParameterPoint, Bin pairs

 - Interpolation
   Stores the interpolation coefficients and calculates results.
   Can be saved as Python pickle object.

 - InterpolationSet
   Stores a list of (ref-bin, Interpolation) pairs.
"""

from professor import histo
from professor.params import ParameterPoint
from professor.tools.persistency import pickle
from professor.tools.sorting import cmpBinID
from professor.tools.decorators import deprecated


class InterpolationSet(dict):
    """Container for all bin-wise interpolations for *one* set of anchor
    points. Used for persistency.

    The object is an extended dict. Keys are bin identifiers, values bin
    interpolations.

    The following factory functions are available:
    * :meth:`mkFromBinDists`
    * :meth:`mkFromPickle`

    Attributes
    ----------
    ranges : ParameterRanges
        The parameter ranges spanned by the runs.
    runskey : str
        The identifiers of the used MC runs, sorted and joined by colons,
        e.g. '000:001:002:004:005'.
    ipolmethod : class
        The interpolation method that is used.
    center : ParameterPoint
    """
    @classmethod
    def mkFromBinDists(cls, bindists, runskey, ipolmethod, center=None):
        """Build an InterpolationSet from a list of BinDistributions.

        Parameters
        ----------
        bindists : list of BinDistribution objects
            A list of BinDistributions, one BinDistribution for each bin
            that should be interpolated.
        runskey : str
            The identifiers of the used MC runs, sorted and joined by
            colons, e.g. '000:001:002:004:005'.
        ipolmethod : class
            The interpolation method that is used given as a class.
        center : ParameterPoint, optional
            The center for polynomial interpolation. If `None` the center of
            the hypercube is used.
        """
        ipols = {}
        ranges = bindists[0].getRanges()
        if center is None:
            center = ranges.center
        elif center.name != ranges.name:
            raise ValueError("Parameter names of center and ranges differ!")

        for bd in bindists:
            ipols[bd.binid] = ipolmethod(bd=db, center=center, order=ipolmethod.method)
        return cls(ranges, runskey, ipolmethod, ipols)

    @classmethod
    def mkFromPickle(cls, path):
        """Load an InterpolationSet from a pickle file.

        Parameters
        ----------
        path : str
            The path of the pickle file.
        """
        f = open(path, "r")
        ipolset = pickle.load(f)
        f.close()
        if type(ipolset) != cls:
            raise IOError("Given file contains wrong data type: %s" % (path))
        
        # following should maintain backward compatibility by converting to generic interpolation
        if not "Generic" in str(ipolset.values()[0].__class__):
            generic_ipols = dict((bin, ipol.convert_to_generic()) for (bin,ipol) in ipolset.iteritems())
            ipolset.update(generic_ipols)
        return ipolset

    @classmethod
    @deprecated("InterpolationSet.mkFromPickle")
    def fromPickle(cls, path):
        return cls.mkFromPickle(path)

    def write(self, path):
        """Dump InterpolationSet to file via pickle.

        Parameters
        ----------
        path : str
            The path of the pickle file.
        """
        f = open(path, 'w')
        pickle.dump(self, f)
        f.close()

    def __init__(self, ranges, runskey, ipolmethod, ipols=None):
        """
        Should not be called directly: use `mkFromBinDists` or `fromPickle`!

        Parameters
        ----------
        ranges : ParameterRanges
            The parameter ranges spanned by the runs.
        runskey : str
            The identifiers of the used MC runs, sorted and joined by
            colons, e.g. '000:001:002:004:005'.
        ipolmethod : class
            The interpolation method that is used.
        ipols : dict, optional
            dict with binid - interpolation pairs
        """
        self.ipolmethod = ipolmethod
        self.ranges = ranges
        self.runskey = runskey

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

        Returns
        -------
        names : list
            The names of all histograms for which at least one
            bin-interpolation is stored.
        """
        names = set([binid.split(":")[0] for binid in self.iterkeys()])
        return list(names)

    @property
    def center(self):
        """Get the center of of interpolations.

        Returns the center of the first interpolation. If no interpolations
        are yet stored the center of the sampling hyper cube is returned.

        Returns
        -------
        center : ParameterPoint
        """
        if len(self):
            ipol = self.itervalues().next()
            return ipol.center
            return self.values()[0]
        else:
            return self.ranges.center

    def __setitem__(self, binid, ipol):
        if self.has_key(binid):
            raise ValueError("Interpolation '%s' already stored!" % (binid))
#        if ipol.method != self.ipolmethod.method:
#            raise TypeError("Given interpolation %s of wrong type %s."
#                " Type %s expected!" % (ipol, type(ipol), self.ipolmethod))
        # TODO: Is this necessary?
        # Assert that all interpolations use the same interpolation center.
        if (ipol.center != self.center).any():
            raise ValueError("Bad center of interpolation!")
        super(InterpolationSet, self).__setitem__(binid, ipol)

    def addInterpolation(self, ipol):
        self[ipol.binid] = ipol

    def addBinDistribution(self, bd):
        self[bd.binid] = self.ipolmethod(bd=bd,order=self.ipolmethod.method)

    def sortedBinIDs(self):
        """Return a list of the sorted bin ids."""
        return sorted(self.iterkeys(), cmp=cmpBinID)

    def getObservableBins(self, observable):
        """Return an InterpolationSet with the ipols for observable."""
        new = InterpolationSet(self.ranges, self.runskey, self.ipolmethod)
        for binid, ipol in self.iteritems():
            if binid.split(":")[0] == observable:
                new[binid] = ipol
        return new

    def getParameterNames(self):
        return self.ranges.names

    def getInterpolationHisto(self, observable, parampoint, title=""):
        """Create an interpolated histogram.

        Parameters
        ----------
        observable : str
            The path of the observable, i.e. of the form
            '/Analysis/Observable'.
        parampoint : ParameterPoint, dict
            The parameter values where the interpolations are evaluated.
        title : str, optional
            A human-readable title for the histogram.

        Returns
        -------
        histo : Histo
            The histogram as predicted by the interpolations.
        """
        if not observable in self.getHistogramNames():
            raise ValueError("Observable %s not amongst these: %s" % (observable, self.getHistogramNames()))
        obsbins = self.getObservableBins(observable)

        if type(parampoint) == dict:
            parampoint = ParameterPoint.mkFromDict(parampoint)

        h = histo.Histo()
        obsBinIDs = obsbins.sortedBinIDs()
        for binID in obsBinIDs:
            h.addBin(obsbins[binID].getBin(parampoint))
        h.name = observable
        h.title = title
        return h


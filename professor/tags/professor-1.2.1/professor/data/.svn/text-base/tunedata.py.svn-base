import itertools
import numpy
import posixpath

from professor import histo

from professor.params import ParameterPoint
from professor.minimize.result import MinimizationResult
from professor.tools.errors import DataProxyError, ArgumentError
from professor.tools.sorting import cmpBinID
import professor.tools.log as logging


class TuneData(dict):
    """Container for data for one choice of runs.

    The bin ids (e.g. /Path/To/Obs:index) are mapped on `BinProps` instances.

    Attributes
    ----------
    runnums : list
        Sorted list run identifiers.
    hasref, hasmc, hasipol : bool
        Flags that are `True` if the object contains that type of data.
    paramranges : ParameterRange, None
        The range of parameters spanned by the used MC runs. Only available
        if MC or ipol data was included.
    """

    def __init__(self, dataproxy, withref=True, withmc=None,
                 useipol=None, useruns=None, useobs=None):
        """Make a TuneData object with the desired data.

        The kind of data that is given to TuneData can be steered via the
        (optional) flags. Depending on the kind of computation (calculating
        interpolation coefficients/minimising/...) different kinds of data
        must be turned on.

        This is the central data preparation function.

        Raises
        ------
        ArgumentError
            If run numbers (if needed) or observables are not specified and
            cannot be guessed.

        Parameters
        ----------
        withref
            Equip TuneData with reference data.
        withmc : str, optional
            Equip TuneData with mc data of the given type, e.g. 'sample'.
            Use ``None`` to disable storing MC data. This is the default.
        useipol : class, optional
            The interpolation method given by the class or ``None`` (=> no
            interpolation data is loaded). ``None`` is the default.
        useruns : list of str
            List of MC run numbers to use or ``None`` (=> use all runs from
            mc data given with `withmc`).
        useobs : list of str
            List of observables to use or ``None`` (=> use all observables from
            mc data given with `withmc`).
        """
        if not useruns:
            if withmc:
                useruns = dataproxy.getMCData(withmc).availableruns
            elif useipol:
                raise ArgumentError("Interpolations reqested but useruns"
                                    " and withmc not given!")
        else:
            useruns = sorted(useruns)
        self.runnums = useruns

        if not useobs:
            if withmc is None:
                raise ArgumentError("Arguments useobs and withmc not specified!")
            useobs = dataproxy.getMCData(withmc).availablehistos
        else:
            useobs = sorted(useobs)

        self.hasref = False
        self.hasmc = False
        self.hasipol = False

        refbins = dict()
        mcbins = dict()
        binipols = dict()
        # binids is a helper for the final loop where we fill this TuneData
        # dict structure
        binids = None

        if withref:
            self.hasref = True
            for obs in useobs:
                try:
                    hist = dataproxy.getRefHisto(obs)
                except KeyError:
                    raise DataProxyError("No reference histogram found:"
                                         " %s" % (obs))
                for i in range(hist.numBins()):
                    binid = dataproxy.getBinID(hist, i)
                    refbins[binid] = hist.getBin(i)
            binids = sorted(refbins.iterkeys())

        self.paramranges = None

        if withmc:
            self.hasmc = True
            mcdata = dataproxy.getMCData(withmc)
            self.parameters = mcdata.getParameterBounds(useruns)
            for run in useruns:
                mcdata.loadRun(run)
            for obs in useobs:
                dummyhisto = mcdata.getRunHistos(useruns[0])[obs]
                for i in range(dummyhisto.numBins()):
                    binid = dataproxy.getBinID(dummyhisto, i)
                    bindict = dict()
                    for run in useruns:
                        bindict[run] = mcdata.getRunHistos(run)[obs].getBin(i)
                    mcbins[binid] = bindict
            if binids is None:
                binids = sorted(mcbins.iterkeys())
            else:
                if sorted(mcbins.iterkeys()) != binids:
                    raise DataProxyError("Bad MC bin IDs!")

        if useipol:
            self.hasipol = True
            binipols = dataproxy.getInterpolationSet(useipol, useruns)

            if binids is None:
                binids = sorted(binipols.iterkeys())
            else:
            # TODO: raise a more useful error/warning
                ipolbins = binipols.keys()
                for binid in binids:
                    assert binid in ipolbins

            if self.paramranges is None:
                self.paramranges = binipols.ranges
            # TODO: raise a more useful error
            else:
                assert self.paramranges == binipols.ranges

        # Fill the dict structure with BinProps. Use get to have None in
        # place where we didn't load the data.
        for binid in binids:
            self[binid] = BinProps(refbins.get(binid),
                                   mcbins.get(binid),
                                   binipols.get(binid))

    def numParams(self):
        if self.paramranges is None:
            raise DataProxyError("No run parameter informatinon available"
                                 " in this TuneData instance!")
        return self.paramranges.dim

    def getBinProps(self, obs):
        """List of all BinProps for observable `obs'."""
        return [bp for bid, bp in self.iteritems() if bid.startswith(obs)]

    def getBinIDs(self, obs):
        """List of all binIDs for observable `obs'."""
        return [bid for bid in self.iterkeys() if bid.startswith(obs)]

    def filteredValues(self):
        """Return an iterator with the bin properties without vetoed,
        zero-weighted.
        """
        return itertools.ifilterfalse(
                lambda bp: bp.veto or bp.weight <= 0.0, self.itervalues())

    def applyObservableWeightDict(self, weightmanager):
        """Set the bin weights.

        Parameters
        ----------
        weightmanager : WeightManager
        """
        for binid, binprop in self.iteritems():
            obsname = binid.split(':')[0]
            bincenter = binprop.getBinCenter()
            w = weightmanager.getWeights(obsname).getWeight(bincenter)
            logging.debug("weighting bin %s with %g"%(binid, w))
            binprop.weight = w

    def getObservables(self):
        obs = map(lambda s: s.split(":")[0], self.keys())

        # make the list unique
        obs = set(obs)

        return list(obs)

    observables = property(getObservables)


    @property
    def ipolmethod(self):
        """The interpolation method.

        Returns the interpolation method of the first bin. It is assumed
        that all bin properties use the same interpolation method.

        Raises
        ------
        DataProxyError
            If no interpolations were stored.
        """
        if not self.hasipol:
            raise DataProxyError("TuneData lacks interpolation data.")
        return type(self.values()[0].ipol)


    def getInterpolationHisto(self, observable, params):
        """Interpolation-prediction for observable at params.

        Parameters
        ----------
        observable : str
            Path of the observable.
        params : MinimizationResult, ParameterPoint, dict
            The values of MC model parameters where the interpolation is
            evaluated.

        Returns
        -------
        histogram : lighthisto.Histo
            Interpolated histogram.
        """
        if not self.hasipol:
            raise RuntimeError("TuneData instance was built without interpolations!")
        if observable not in self.observables:
            raise ValueError("Observable '%s' not available!" % (observable))

        if isinstance(params, MinimizationResult):
            params = params.values
        elif type(params) == dict:
            params = ParameterPoint.mkFromDict(params)
        elif not isinstance(params, ParameterPoint):
            raise TypeError("Argument parampoint must be of types"
                            " MinimizationResult, ParameterPoint, or dict!")
        if (self.paramranges is not None and
                self.paramranges.names != params.names):
            raise ValueError("params has wrong parameter names!")

        h = histo.Histo()
        binids = sorted(self.getBinIDs(observable), cmp=cmpBinID)
        # binids = sorted(binids, key = lambda bid: int(bid.split(":")[-1]))

        for bid in binids:
            ipol = self[bid].ipol
            if ipol is not None:
                h.addBin(ipol.getBin(params))
            else:
                logging.warn("Adding zero bin for uninterpolated bin %s" % (bid))
                if self[bid].refbin is not None:
                    xlow, xhigh = self[bid].refbin.getXRange()
                elif self[bid].mcdict is not None:
                    xlow, xhigh = self[bid].mcdict.values()[0].getXRange()
                else:
                    logging.warn("Unable to add uninterpolated bin %s" % (bid))
                    continue

                h.addBin(histo.Bin(xlow, xhigh))
        h.name = posixpath.basename(observable)
        h.path = posixpath.dirname(observable)
        return h

    def vetoEmptyErrors(self):
        """Veto bins with zero reference error."""
        for bp in self.itervalues():
            # if bp.refbin.getYErr() == 0 or bp.refbin.getYVal() == 0:
            if bp.refbin.getYErr() <= 0.0:
                bp.veto = True


class BinProps(object):
    """Container for all data related to a bin needed to do a minimisation.

    A container for all the variants on a distribution bin: its weight, its
    reference value and errors, a collection of its simulated equivalents from a
    set of MC runs, and an interpolation function for that bin, based on
    optimising the fit to a sampling of MC points in the parameter space.

    At the moment the following is stored:
    Attributes
    ----------
    refbin: lighthisto.Bin
        The refernce bin.
    mcdict : dict {str => lighthisto.Bin}
        Map for run numbers on MC bins.
    ipol
        The interpolation for this bin.
    veto : bool
        Flag for vetoing this bin in the GoF calculation.
    weight : float
    sqrtweight : float
        The weight of this bin in GoF calculation.
    binid : str
        The bin ID of this bin of the form '/Analysis/Observable:BinIndex'.
    """
    __slots__ = ["refbin", "mcdict", "ipol", "veto",
                 "__weight", "weight",
                 "__sqrtweight", "sqrtweight",
                 "binid"]
    def __init__(self, refbin, mcdict, ipol):
        self.refbin = refbin
        self.mcdict = mcdict
        self.ipol = ipol

        self.veto = False
        self.__weight = 1.0
        self.__sqrtweight = 1.0

    def __cmp__(self, other):
        """ This allows for sorting BinProps by binids """
        selfid = int(self.binid.split(':')[-1])
        otherid = int(other.binid.split(':')[-1])
        return cmp(selfid, otherid)

    def setWeight(self, w):
        self.__weight = w
        self.__sqrtweight = numpy.sqrt(w)

    def setSqrtWeight(self, sw):
        self.__weight = sw**2
        self.__sqrtweight = sw

    def getBinCenter(self):
        return self.refbin.getBinCenter()

    weight = property(lambda s: s.__weight, setWeight)
    sqrtweight = property(lambda s: s.__sqrtweight, setSqrtWeight)
    binid = property(lambda s: s.ipol.binid)

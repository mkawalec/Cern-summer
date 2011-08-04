import itertools
import numpy

from professor import histo

from professor.tools.parameter import ParameterPoint
from professor.minimize.result import MinimizationResult
from professor.tools.errors import DataProxyError
import professor.tools.log as logging


class TuneData(dict):
    """Container for data for one choice of runs."""
    def __init__(self, dataproxy, withref=True, withmc=None, useipol=None,
                    useruns=None, useobs=None):
        """Return a TuneData object with the desired data.

        The kind of data that is given to TuneData can be steered via the
        (optional) flags. Depending on the kind of computation (calculating
        interpolation coefficients/minimising/...) different kinds of data
        must be turned on.

        This is the central data preparation function.

        withref  -- equip TuneData with reference data
        withmc   -- equip TuneData with mc data data
        useipol  -- the interpolation method given by the class or
                    None (=> no interpolation data is loaded)
        useruns  -- list of run numbers to use or
                    None (=> use all valid run directories from sample mc)
        useobs   -- list of observables to use or
                    None (=> use all observables from sample mc)
        """
        if useruns is None:
            useruns = dataproxy.getMCData(withmc).availableruns
        else:
            useruns = sorted(useruns)
        self.runnums = useruns

        if useobs is None:
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
            binids = refbins.iterkeys()

        if withmc is not None:
            self.hasmc = True
            mcdata = dataproxy.getMCData(withmc)
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
                binids = mcbins.iterkeys()

        # Load interpolation and get a Scaler:
        # Use Scaler from interpolations by default and fall back to setting
        # the scaler to None, since without interpolations there should be
        # no need for a Scaler at all.
        if useipol is not None:
            self.hasipol = True
            binipols = dataproxy.getInterpolationSet(useipol, useruns)
            self.scaler = binipols.scaler
            if binids is None:
                binids = binipols.iterkeys()
        else:
            binipols = dict()
            self.scaler = None
            # short cut for MC data
            # mcd = dataproxy.getMCData(withmc)
            # from professor.tools.parameter import Scaler
            # self.scaler = Scaler(mcd.getParameterBounds(useruns))

        # Fill the dict structure with BinProps. Use get to have None in
        # place where we didn't load the data.
        for binid in binids:
            self[binid] = BinProps(refbins.get(binid),
                                   mcbins.get(binid),
                                   binipols.get(binid))

    def numParams(self):
        return self.scaler.dim()

    def getBinProps(self, obs):
        """List of all BinProps for observable `obs'."""
        return [bp for bid, bp in self.iteritems() if bid.startswith(obs)]

    def getBinIDs(self, obs):
        """List of all binIDs for observable `obs'."""
        return [bid for bid in self.iterkeys() if bid.startswith(obs)]

    def filteredValues(self):
        """Return an iterator with the bin properties without vetoed,
        zero-weighted or zero referror bins.
        """
        return itertools.ifilterfalse(
                lambda bp: bp.veto or bp.weight <= 0.0, self.itervalues())

    def applyObservableWeightDict(self, weightmanager):
        """
        Make sure the keys fit the observable names in the bin ID in this
        instance! Weights has to be a dict with observable names as keys
        and 3-tuples as values: weights[observ] = (weight, low, high)
        where weight is the actual weight and low and high are x-values
        that define an allowed region; bincenters not in this range will
        result in a veto of the according binprop.
        """
        for binid, binprop in self.iteritems():
            if binprop.ipol is None:
                raise DataProxyError("No interpolation found for bin"
                                     " '%s'" % (binid))
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

    # TODO: accept dictionaries
    def getInterpolationHisto(self, observable, parampoint):
        """Interpolation-prediction for observable at parampoint.

        Parameters
        ----------
            observable : str
                AIDA path of the observable.
            parampoint : MinimizationResult, ParameterPoint, dict
                The values of MC model parameters where the interpolation is
                evaluated.

        Returns
        -------
            histogram : lighthisto.Histo
                Interpolated histogram.
        """
        if not self.hasipol:
            raise RuntimeError("TuneData instance was built without"
                               " interpolations!")
        if observable not in self.observables:
            raise ValueError("Observable '%s' not available!" % (observable))

        if isinstance(parampoint, MinimizationResult):
            pointasarray = parampoint.parscaled
        elif isinstance(parampoint, ParameterPoint):
            pointasarray = parampoint.getScaled()
        elif type(parampoint) == dict:
            pointasarray = ParameterPoint(parampoint, self.scaler).getScaled()
        else:
            raise TypeError("Argument parampoint must be of types"
                            " MinimizationResult, ParameterPoint, or dict!")

        h = histo.Histo()
        binids = self.getBinIDs(observable)
        binids = sorted(binids, key = lambda bid: int(bid.split(":")[-1]))

        for bid in binids:
            ipol = self[bid].ipol
            if ipol is not None:
                h.addBin(ipol.getBin(pointasarray))
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
        h.name = observable
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
     - refbin: a Bin instance with the reference bin
     - mcdict: a run number -> MC Bin dictionary
     - ipol: a QuadraticBinInterpolation instance
     - veto: a flag for vetoing this bin in the GoF calculation
     - weight/sqrtweight: weights for the GoF calculation
    """
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

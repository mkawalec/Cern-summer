import numpy as np

from professor.interpolation.interpolationset import InterpolationSet
from professor.params import ParameterPoint
from professor.tools.decorators import addmethodattribute
from professor.tools import log

# keep this for later reference

class _OLD_SensCalculator(InterpolationSet):
    """Sensitivity calculator built on top of an InterpolationSet

    Several sensitivtiy definitions are implemented. For more information
    about the implemented definitions or to use different definitions see
    the setSensitivityDefinition method.

    The basic method to get sensitivity information is arraySensitivity()
    that returns an 2D array of sensitivities of one observable to one
    parameter.

    extremalSensitivity() is a convenience method to get signed extremal
    sensitivities for one observable to one parameter.
    """
    def __init__(self, ipolset, deltaP, tundat=None, penalty=0.5):
        """
        Parameters
        ----------
        ipolset : InterpolationSet
        deltaP : float, ParameterPoint
            The $\\delta \\vec p$ that is used for the numeric derivatives. If it is a
            float the fraction of the body diagonal of the parameter range
            stored in `ipolset` is used.
        tundata : TuneData, optional
            A TuneData with reference data included.
        """
        super(SensCalculator, self).__init__(ipolset.ranges,
                        ipolset.runskey, ipolset.ipolmethod, ipolset)
        if isinstance(deltaP, float):
            self.deltaP = deltaP * self.ranges.getRelativePoint(deltaP)
        else:
            self.deltaP = deltaP.copy()

        # init parameterpoint with center of spanned hyper cube
        self.parampoint = self.ranges.center
        # initialize bin sensitivity definition
        self.binSensitivity = self._oldSensitivity

        if tundat is not None and not tundat.hasref:
            # tune data 
            raise ValueError("Argument tundat must have reference data!")
        self._tundat = tundat
        self.penalty = penalty

    def setSensitivityDefinition(self, definition):
        if definition == "slope":
            self.binSensitivity = self._slopeSensitivity
        elif definition == "relslope":
            self.binSensitivity = self._relSlopeSensitivity
        elif definition == "old":
            self.binSensitivity = self._oldSensitivity
        elif definition == "original":
            self.binSensitivity = self._originalSensitivity
        else:
            raise ValueError("Unknown sensitivity definition: %s!" % (definition))

    def getSensitivityDefinition(self):
        return self.binSensitivity.definition

    def setParampoint(self, params):
        """Set the default parameter values for sensitivity calculation.

        These values are used for the location in parameter space when the
        sensitivities are calculated for one parameter.

        Parameters
        ----------
        params : ParameterPoint
            The default parameter values.
        """
        if type(params) != prof.ParameterPoint:
            raise TypeError("Argument `params` must be a ParameterPoint!")
        self.parampoint = params

    # TODO: parameter values of the other parameters
    def arraySensitivity(self, observable, param, parbincenters):
        """Return sensitivity of observable to param as 2D array.

        The return value is a 2D numpy array:
            axis 0 -> observable bin index
            axis 1 -> parameter bin index
        e.g.
            >>> ret = sc.sensitivityArray(...)
            >>> # get the sensitivity of obs-bin #3 at parameter location #5
            >>> ret[3,5]

        Parameters
        ----------
        observable : str
            The observable name.
        param : str
            The parameter name.
        parbincenters : array_like, optional
            The parameter values for `param` to calculate sensitivities at.
            Default is to guess the bin centers from the parameter ranges
            stored in the interpolation set.

        Returns
        -------
        sensitivity : numpy.ndarray
            2D array with the sensitiviy values.
        """
        # subset containing only the bins of this observable
        subset = self.getObservableBins(observable)

        prof.log.debug("Calculating sensitivity of obs %s (%i bins) to param %s at"
                       " p = %s." % (observable, len(subset), param, parbincenters))
        prof.log.debug("Using sensitivity definition: %s." % (
                       self.binSensitivity.definition))
        # check that the width of the parameter bins is greater than our
        # deltaP[param] for sensitivitiy calculation
        if len(parbincenters) > 1:
            w = parbincenters[1] - parbincenters[0]
            if w < self.deltaP[param]:
                prof.log.warn("Width of parameter bins %s is smaller"
                              " than deltaP: %s for sensitivitiy"
                              " calculation!" % ( w, self.deltaP[param]))
                prof.log.warn("Continuing anyway...")

        ret = numpy.zeros((len(subset), len(parbincenters)))
        for i, binid in enumerate(subset.sortedBinIDs()):
            binipol = self[binid]
            for j, par in enumerate(parbincenters):
                # make a copy to assure that self.parampoint is not changed
                ppoint = self.parampoint.copy()
                ppoint[param] = par

                sens = self.binSensitivity(binipol, param, ppoint)
                if self._tundat is not None:
                    if self._tundat[binid].refbin.yval <= 0.0:
                        sens = 0.0
                        prof.log.debug("Sensitivity set to 0 for bin %s"
                                       " (refval=0)" % (binid))
                    else:
                        relreferr = (self._tundat[binid].refbin.yerr /
                                     self._tundat[binid].refbin.yval)
                        if relreferr > self.penalty:
                            sens = 0.0
                            msg = ("Sensitivity set to 0 for bin %s "
                                   " (referror/refval=%f < %s)" % (
                                       binid, relreferr, self.penalty))
                            print msg
                            prof.log.debug(msg)
                            del msg
                ret[i,j] = sens
        return ret


    def getParameterBins(self, observable, param, nbins=0):
        """Get parameter bin centers and edges.

        Parameters
        ----------
        observable : str
        param : str
        nbins : int, optional
            The number of parameter bins. Default: number of observable
            bins, but at least 10.

        Returns
        -------
        bincenters : numpy.ndarray
            1D array of length `npar`
        binedges : numpy.ndarray
            1D array of length `npar` + 1
        """
        # subset containing only the bins of this observable
        subset = self.getObservableBins(observable)
        if nbins <= 0:
            nbins = max(10, len(subset))
        x = numpy.linspace(0.0, 1.0, nbins + 1, endpoint=True)
        # create a line stretching from end-to-end
        binedges = self.ranges.getRelativePoint(x[:,numpy.newaxis],
                                                plainarray = True)
        print binedges
        # we only need the centers for one param
        pindex = self.ranges.getIndex(param)
        binedges = binedges[:,pindex]
        w = binedges[1] - binedges[0]
        bincenters = binedges[1:] + 0.5 * w
        return (bincenters, binedges)


    def extremalSensitivity(self, observable, param, parbincenters,
                            retstd=False):
        """Return extremal sensitivity of observable to param.

        Sensitivities are first calculated by arraySensitivity and then the
        array is reduced to a 1D-array with the signed extremal values.

        If retstd is True a second array with the standard deviation values
        of the sensitivity samples for each bin.

        The return value is a 1D numpy array:
            axis 0 -> observable bin index

        observable  -- The observable name.
        param       -- The parameter name.
        parbincenters  -- The parameter points to calculate sensitivities
                    at.
        retstd      -- Additionaly return the standard deviation of the
                    sensitivitiy samples.
        """
        a = self.arraySensitivity(observable, param, parbincenters)
        mins = a.min(1)
        maxs = a.max(1)
        extremals = numpy.zeros(len(mins))
        for i in xrange(len(mins)):
            if abs(mins[i]) > abs(maxs[i]):
                extremals[i] = mins[i]
            else:
                extremals[i] = maxs[i]
        if retstd == True:
            return extremals, a.std(1, ddof=1)
        else:
            return extremals


    # Sensitivity is defined as
    # { \delta(MC)/MC }/{ \delta(P_i)/P_i }
    @addmethodattribute("definition", "original")
    def _originalSensitivity(self, binipol, param, ppoint):
        """Calculate the sensitivity to param of binipol at ppoint.

        Sensitivity is defined as:
            { \delta(MC)/MC } / { \delta(P_i)/P_i }
        This means that with constant slope dMC/dp the sensitivity is not
        constant but proportional to p/MC !
        """
        pindex = ppoint.getIndex(param)
        dp = self.deltaP[pindex]
        dpvec = numpy.zeros(ppoint.dim)
        dpvec[pindex] = dp
        MC_0 = binipol.getValue(ppoint)
        MC_plus = binipol.getValue(ppoint + dpvec)
        return (MC_plus-MC_0)*ppoint[pindex]/(MC_0 * dp)

    # Sensitivity is defined as
    # { \delta(MC)/MC }/{ (P_i + \delta(P_i))/P_i }
    @addmethodattribute("definition", "old")
    def _oldSensitivity(self, binipol, param, ppoint):
        """Calculate the sensitivity to param of binipol at ppoint.

        Sensitivity is defined as:
            { \delta(MC)/MC } / { (P_i + \delta(P_i))/P_i }
        This is the definition we used in the old sensistivity code.
        """
        pindex = ppoint.getIndex(param)
        dp = self.deltaP[pindex]
        dpvec = numpy.zeros(ppoint.dim)
        dpvec[pindex] = dp
        MC_0 = binipol.getValue(ppoint)
        MC_plus = binipol.getValue(ppoint + dpvec)
        return ( (MC_plus-MC_0)*ppoint[pindex]
                / (MC_0 * (ppoint[pindex] + dp)) )

    # Sensitivity is defined as
    # { \delta(MC)/MC } / \delta(P_i)
    @addmethodattribute("definition", "relslope")
    def _relSlopeSensitivity(self, binipol, param, ppoint):
        """Calculate the sensitivity to param of binipol at ppoint.

        Sensitivity is defined as:
            { \delta(MC)/MC } / \delta(p_i)
        This means that with constant slope dMC/dp the sensitivity is not
        constant but proportional to 1/MC !
        """
        pindex = ppoint.getIndex(param)
        dp = self.deltaP[pindex]
        dpvec = numpy.zeros(ppoint.dim)
        dpvec[pindex] = dp
        MC_0 = binipol.getValue(ppoint)
        MC_plus = binipol.getValue(ppoint + dpvec)
        return (MC_plus-MC_0)/(MC_0 * dp)

    # Sensitivity is defined as
    # \delta(MC) / \delta(P_i)
    # i.e. the slope
    @addmethodattribute("definition", "slope")
    def _slopeSensitivity(self, binipol, param, ppoint):
        """Calculate the sensitivity to param of binipol at ppoint.

        Sensitivity is defined as:
            \delta(MC) / \delta(P_i)
        i.e. the slope.
        """
        pindex = ppoint.getIndex(param)
        dp = self.deltaP[pindex]
        dpvec = numpy.zeros(ppoint.dim)
        dpvec[pindex] = dp
        MC_0 = binipol.getValue(ppoint)
        MC_plus = binipol.getValue(ppoint + dpvec)
        return (MC_plus-MC_0) / dp

    def getSensFormulaSign(self):
        d = self.getSensitivityDefinition()
        if d == "slope":
            return "S^\mathrm{slope}_i"
        if d == "relslope":
            return "S^\mathrm{rel}_i"
        return d


class Sensitivity(InterpolationSet):
    """Sensitivity calculator built on top of an InterpolationSet

    The sensitivity is calculated based on the interpolation of the MC
    response function.

    The basic method to get sensitivity information is `arraySensitivity`
    that returns an 2D array of sensitivities of one observable to one
    parameter. The values of the other, unvaried parameters are taken from
    the values of `parampoint`

    `extremalSensitivity` is a convenience method to get signed extremal
    sensitivities for one observable to one parameter.

    Several sensitivtiy definitions are implemented. For more information
    about the implemented definitions or to use different definitions see
    the `setSensitivityDefinition` method.

    Attributes
    ----------
    parampoint : ParameterPoint
        The parameter point used as center for the N-dim cross for for
        :meth:`arraySensitivity` and :meth:`extremalSensitivity` and to
        estimate the typical parmeter and MC scale of each bin to scale the
        sensitivities.
    """
    def __init__(self, ipolset, deltaP, tundat=None, penalty=0.5,
                 epsilonfactor=1e-3):
        """
        Parameters
        ----------
        ipolset : InterpolationSet
        deltaP : float, ParameterPoint
            The :math:`\\delta \\vec p` that is used for the numeric derivatives.
            If it is a float the fraction of the body diagonal of the
            parameter range stored in `ipolset` is used.
        tundata : TuneData, optional
            A TuneData with reference data included.
        penalty : float, optional
            Bins with a relative error of the reference data larger than
            `penalty` will be excluded from the sensitivity calculation and
            the respective sensitivity will be set to 0.0. [default: 0.5]
        epsilonfactor : float, optional
            Scale used to calculate the *small* epsilons used in some
            sensitivitiy definitions. The default is 1e-3
        """
        super(Sensitivity, self).__init__(ipolset.ranges,
                        ipolset.runskey, ipolset.ipolmethod, ipolset)
        if isinstance(deltaP, float):
            self.deltaP = self.ranges.getRelativePoint(deltaP) - self.ranges.low
        else:
            self.deltaP = deltaP.copy()

        # init parameterpoint with center of spanned hyper cube
        self.parampoint = self.ranges.center
        # initialize bin sensitivity definition
        self.binSensitivity = self._newSensitivity

        if tundat is not None and not tundat.hasref:
            raise ValueError("Argument tundat must have reference data!")

        self._tundat = tundat
        self.penalty = penalty
        self.epsilonfactor = epsilonfactor

        # list of parameter points
        self._rndpoints = None
        self._rndgen = None


    def setSensitivityDefinition(self, definition):
        if definition == "slope":
            self.binSensitivity = self._slopeSensitivity
        elif definition == "relslope":
            self.binSensitivity = self._relSlopeSensitivity
        elif definition == "old":
            self.binSensitivity = self._oldSensitivity
        elif definition == "original":
            self.binSensitivity = self._originalSensitivity
        elif definition == "new":
            self.binSensitivity = self._newSensitivity
        else:
            raise ValueError("Unknown sensitivity definition: %s!" % (definition))


    def getSensitivityDefinition(self):
        return self.binSensitivity.definition


    def setParamPoint(self, params):
        """Set the default parameter values for sensitivity calculation.

        These values are used for the location in parameter space when the
        sensitivities are calculated for one parameter.

        Parameters
        ----------
        params : ParameterPoint
            The default parameter values.
        """
        if type(params) != ParameterPoint:
            raise TypeError("Argument `params` must be a ParameterPoint!")
        self._parampoint = params

    def getParamPoint(self):
        return self._parampoint

    parampoint = property(getParamPoint, setParamPoint,
                          doc = "The values of the unvaried parameters used"
                                " during the sensitivity calculation.")


    def arraySensitivity(self, observable, param, parbincenters):
        """Return sensitivity of `observable` to `param` as 2D array.

        For the calculation parameters `param` is set to the values in
        `parbincenters`. The values of the other parameters are set to the
        values of `parampoint`.

        The return value is a 2D numpy array:
            axis 0 -> observable bin index
            axis 1 -> parameter bin index
        e.g.
            >>> ret = sc.sensitivityArray("/Analysis/Observable", "PAR 1", [0.5, 1.5, 2.5, 3.5, 4.5, 5.5])
            >>> # get the sensitivity of obs-bin #3 at parameter location #5
            >>> ret[3,5]

        Parameters
        ----------
        observable : str
            The observable name.
        param : str
            The parameter name.
        parbincenters : array_like, optional
            The parameter values for `param` to calculate sensitivities at.
            Default is to guess the bin centers from the parameter ranges
            stored in the interpolation set.

        Returns
        -------
        sensitivity : numpy.ndarray
            2D array with the sensitiviy values.
        """
        # subset containing only the bins of this observable
        subset = self.getObservableBins(observable)

        log.debug("Calculating sensitivity of obs %s (%i bins) to param %s at"
                       " p = %s." % (observable, len(subset), param, parbincenters))
        log.debug("Using sensitivity definition: %s." % (
                       self.binSensitivity.definition))
        # check that the width of the parameter bins is greater than our
        # deltaP[param] for sensitivitiy calculation
        if len(parbincenters) > 1:
            w = parbincenters[1] - parbincenters[0]
            if w < self.deltaP[param]:
                log.warn("Width of parameter bins %s is smaller"
                              " than deltaP: %s for sensitivitiy"
                              " calculation!" % ( w, self.deltaP[param]))
                log.warn("Continuing anyway...")

        ret = np.zeros((len(subset), len(parbincenters)))
        for i, binid in enumerate(subset.sortedBinIDs()):
            binipol = self[binid]

            if not self._enough_statistics(binid):
                continue

            # print 40*"+"
            # print "next bin:", binid, "(", param, ")"
            # print "initial parampoint:"
            # print self.parampoint
            # print "bins:", parbincenters
            # print 40*"+"

            for j, par in enumerate(parbincenters):
                # make a copy to assure that self.parampoint is not changed
                ppoint = self.parampoint.copy()
                ppoint[param] = par
                # print "--"
                # print ppoint
                sens = self.binSensitivity(binipol, param, ppoint)
                if np.isnan(sens):
                    ret[i,j] = 0.0
                    log.debug("Encountered nan sensitivity for param %s at for bin %s ... return 0.0"%(param, binid))
                else:
                    ret[i,j] = sens
        return ret


    def _enough_statistics(self, binid):
        """Test that the ref bin has enough statistics.

        The criterion is that the rel. error must be less than :attr:`penalty`.

        `True` is returned if the above criterion is fulfilled.
        """
        if self.penalty <= 0.0:
            return True
        if self._tundat is None:
            log.debug("Cannot test ref. stats: no reference data ->"
                      " Returning True")
            return True
        try:
            refbin = self._tundat[binid].refbin
        except:
            # Here we have a problem. Some observables look for binids in the ref histos
            # that do not exist in interpolations, strange!
            return False

        if refbin.yval == 0.0:
            log.debug("refbin content ==0.0!")
            return False

        if refbin.yerr == 0.0:
            log.warning("refbin error == 0.0  for binid %s!"%binid)
            return False

        # yerr = (yerrplus + yerrminus)/2
        relerr = abs(refbin.yerr/refbin.yval)
        if relerr > self.penalty:
            msg = ("Sensitivity set to 0 for bin %s (referror/refval=%f"
                   " > %s)" % ( binid, relerr, self.penalty))
            log.debug(msg)
            return False

        return True


    def getParameterBins(self, observable, param, nbins=0):
        """Get parameter bin centers and edges for sensitivity calculations.

        Parameters
        ----------
        observable : str
        param : str
        nbins : int, optional
            The number of parameter bins. Default: number of observable
            bins, but at least 10.

        Returns
        -------
        bincenters : numpy.ndarray
            1D array of length `npar`
        binedges : numpy.ndarray
            1D array of length `npar` + 1
        """
        # subset containing only the bins of this observable
        subset = self.getObservableBins(observable)
        if nbins <= 0:
            nbins = max(10, len(subset))
        x = np.linspace(0.0, 1.0, nbins + 1, endpoint=True)
        # create a line stretching from end-to-end
        binedges = self.ranges.getRelativePoint(x[:,np.newaxis],
                                                plainarray = True)
        # we only need the centers for one param
        pindex = self.ranges.getIndex(param)
        binedges = binedges[:,pindex]
        w = binedges[1] - binedges[0]
        bincenters = binedges[1:] + 0.5 * w
        return (bincenters, binedges)


    def extremalSensitivity(self, observable, param, parbincenters,
                            retstd=False):
        """Return extremal array sensitivity of observable to param.

        Sensitivities are first calculated by :meth:`arraySensitivity` and
        then the array is reduced to a 1D-array with the signed extremal
        values in each observable bin.

        If `retstd` is `True` a second array with the standard deviation values
        of the sensitivity samples for each bin.

        The return value is a 1D numpy array::

            axis 0 -> observable bin index

        Parameters
        ----------
        observable : str
            The observable name.
        param : str
            The parameter name.
        parbincenters : array_like
            The parameter points to calculate sensitivities at.
        retstd : bool, optional
            Additionaly return the standard deviation of the sensitivitiy
            samples. The default is to return only the sensitivitiy values.

        Returns
        -------
        extremals : numpy.ndarray
            The extremal sensitivity values.
        stddev: numpy.ndarray, optional
            The standard deviation of the sampled sensitivity values.
        """
        a = self.arraySensitivity(observable, param, parbincenters)
        mins = a.min(1)
        maxs = a.max(1)
        extremals = np.zeros(len(mins))
        for i in xrange(len(mins)):
            if abs(mins[i]) > abs(maxs[i]):
                extremals[i] = mins[i]
            else:
                extremals[i] = maxs[i]
        if retstd == True:
            return extremals, a.std(1, ddof=1)
        else:
            return extremals


    def setRandomPointGen(self, rndgen):
        self._rndpoints = None
        self._rndgen = rndgen

    def getRandomPointGen(self):
        if self._rndgen is None:
            from professor.tools.pointsampling import RandomPointGenerator
            self._rndgen = RandomPointGenerator(self.ranges)
            self._rndgen.seed()
        return self._rndgen

    rndpointgen = property(getRandomPointGen, setRandomPointGen)


    def extremalSensitivityRandom(self, observable, param, numpoints=1000,
                                  retstd=False):
        """Return extremal sensitivity of observable to param.

        The sensitivities are calculated at randomly located points and the
        data is then reduced to a 1D-array with the signed extremal values
        in each observable bin.

        The generator that is used to sample the points can be set with
        :attr:`rndpointgen`. By default points are sampled from the
        hyper-cube spanned by the anchor points of the interpolation.

        If `retstd` is `True` a second array with the standard deviation values
        of the sensitivity samples for each bin.

        The return value is a 1D numpy array:
            axis 0 -> observable bin index

        Parameters
        ----------
        observable : str
            The observable name.
        param : str
            The parameter name.
        numpoints : int, optional
            The number of random parameter points to calculate sensitivities
            at. The points are sampled only the first time
            `extremalSensitivityRandom` is called.
        retstd : bool, optional
            Additionaly return the standard deviation of the sensitivitiy
            samples. The default is to return only the sensitivitiy values.

        Returns
        -------
        extremals : numpy.ndarray
            The extremal sensitivity values.
        stddev: numpy.ndarray, optional
            The standard deviation of the sampled sensitivity values.
        """
        if self._rndpoints == None or len(self._rndpoints) != numpoints:
            self._rndpoints = [p for p in self.rndpointgen.generate(numpoints)]
            log.debug("(Re-)Generated list of random points for sens."
                      " calculation.")

        # subset containing only the bins of this observable
        subset = self.getObservableBins(observable)
        sens = np.zeros((len(subset), len(self._rndpoints)))
        for i, binid in enumerate(subset.sortedBinIDs()):
            if not self._enough_statistics(binid):
                continue
            binipol = self[binid]
            for j, point in enumerate(self._rndpoints):
                sens[i,j] = self.binSensitivity(binipol, param, point)

        mins = sens.min(1)
        maxs = sens.max(1)
        extremals = np.empty_like(mins)
        for i in xrange(len(mins)):
            if abs(mins[i]) > abs(maxs[i]):
                extremals[i] = mins[i]
            else:
                extremals[i] = maxs[i]
        if retstd == True:
            return extremals, sens.std(1, ddof=1)
        else:
            return extremals


    # Sensitivity is defined as
    # { \delta(MC)/MC }/{ \delta(P_i)/P_i }
    @addmethodattribute("definition", "original")
    def _originalSensitivity(self, binipol, param, ppoint):
        """Calculate the sensitivity to param of binipol at ppoint.

        Sensitivity is defined as:
            { \delta(MC)/MC } / { \delta(P_i)/P_i }
        This means that with constant slope dMC/dp the sensitivity is not
        constant but proportional to p/MC !
        """
        pindex = ppoint.getIndex(param)
        # dpvec = np.zeros(ppoint.dim)
        # dpvec[pindex] = dp
        dp, dpvec = self._get_dp_dpvec(param)
        MC_0 = binipol.getValue(ppoint)
        MC_plus = binipol.getValue(ppoint + dpvec)
        return (MC_plus-MC_0)*ppoint[pindex]/(MC_0 * dp)


    # Sensitivity is defined as
    # { \delta(MC)/MC }/{ (P_i + \delta(P_i))/P_i }
    @addmethodattribute("definition", "old")
    def _oldSensitivity(self, binipol, param, ppoint):
        """Calculate the sensitivity to param of binipol at ppoint.

        Sensitivity is defined as:
            { \delta(MC)/MC } / { (P_i + \delta(P_i))/P_i }
        This is the definition we used in the old sensistivity code.
        """
        pindex = ppoint.getIndex(param)
        dp = self.deltaP[pindex]
        dpvec = np.zeros(ppoint.dim)
        dpvec[pindex] = dp
        MC_0 = binipol.getValue(ppoint)
        MC_plus = binipol.getValue(ppoint + dpvec)
        return ( (MC_plus-MC_0)*ppoint[pindex]
                / (MC_0 * (ppoint[pindex] + dp)) )


    # Sensitivity is defined as
    # { \delta(MC)/MC } / \delta(P_i)
    @addmethodattribute("definition", "relslope")
    def _relSlopeSensitivity(self, binipol, param, ppoint):
        """Calculate the sensitivity to param of binipol at ppoint.

        Sensitivity is defined as:
            { \delta(MC)/MC } / \delta(p_i)
        This means that with constant slope dMC/dp the sensitivity is not
        constant but proportional to 1/MC !
        """
        pindex = ppoint.getIndex(param)
        dp = self.deltaP[pindex]
        dpvec = np.zeros(ppoint.dim)
        dpvec[pindex] = dp
        MC_cent = binipol.getValue(self.parampoint)
        MC_0 = binipol.getValue(ppoint)
        MC_plus = binipol.getValue(ppoint + dpvec)
        # return (MC_plus-MC_0)/(MC_0 * dp)
        return (MC_plus-MC_0)/(MC_cent * dp)


    # Sensitivity is defined as
    # \delta(MC) / \delta(P_i)
    # i.e. the slope
    @addmethodattribute("definition", "slope")
    def _slopeSensitivity(self, binipol, param, ppoint):
        """Calculate the sensitivity to param of binipol at ppoint.

        Sensitivity is defined as:
            \delta(MC) / \delta(P_i)
        i.e. the slope.
        """
        pindex = ppoint.getIndex(param)
        dp = self.deltaP[pindex]
        dpvec = np.zeros(ppoint.dim)
        dpvec[pindex] = dp
        MC_0 = binipol.getValue(ppoint)
        MC_plus = binipol.getValue(ppoint + dpvec)
        return (MC_plus-MC_0) / dp

    @addmethodattribute("definition", "analytic-slope")
    def _analyticSlopeSens(self, binipol, param, ppoint):
        pindex = ppoint.getIndex(param)
        return binipol.getGradient(ppoint, pindex)


    @addmethodattribute("definition", "new")
    def _newSensitivity(self, binipol, param, ppoint):
        dp, dpvec = self._get_dp_dpvec(param)
        MC_0 = binipol.getValue(ppoint)
        MC_plus = binipol.getValue(ppoint + dpvec)

        # Calculate parameter and MC spread over the parameter sampling
        # range.
        # Do not use the edges but use a 10% offset to make sure that the
        # interpolations are reliable.
        pidx = self.ranges.getIndex(param)
        pmin = self.ranges.low[pidx]
        pmax = self.ranges.high[pidx]
        # the relative width of the offest of min/max parameter values
        reloff = 0.1
        pwidth = pmax - pmin
        # This should always be true because of the way the parameter ranges
        # are stored in interpolation sets are created.
        assert pwidth > 0.0
        offset = np.zeros(ppoint.dim)
        offset[pidx] = reloff*pwidth
        # update the width
        pwidth = (1 - 2*reloff) * pwidth
        pmin = self.ranges.low + offset
        pmax = self.ranges.high - offset

        MCwidth = abs(binipol.getValue(pmax) - binipol.getValue(pmin))

        MC_scale = binipol.getValue(self.parampoint)
        # MC_scale = MC_0
        p_scale = self.parampoint[pidx]
        # p_scale = ppoint[pidx]

        eps_MC = self.epsilonfactor * MCwidth
        eps_par = self.epsilonfactor * pwidth

        # pval = self.parampoint[pidx]
        # pval = ppoint[pidx]

        sens =  (MC_plus - MC_0) * (abs(p_scale) + eps_par) / ((abs(MC_scale) + eps_MC) * dp)
        # sens =  (MC_plus - MC_0) * pwidth / (MCwidth * dp)
        # print sens
        # sens =  (MC_plus - MC_0) * (pval + eps_par) / ((MC_0 + eps_MC) * dp)
        # print "pwidth:", pwidth
        # print "MCwidth:", MCwidth
        # print "%f = [(%f - %f) / (%f + %f)] / [%f / (%f + %f)]" % (
                # sens, MC_plus, MC_0, MC_0, eps_MC, dp, pval, eps_par)
        return sens


    def _get_dp_dpvec(self, param):
        """
        Returns
        -------
        dp : float
            The $\delta p$ value in direction `param`.
        dpvec : numpy.ndarray
            A vector in direction `param` with length `dp`.
        """
        pidx = self.deltaP.getIndex(param)
        dp = self.deltaP[pidx]
        dpvec = np.zeros(self.deltaP.dim)
        dpvec[pidx] = dp
        return dp, dpvec


    def getSensFormulaSign(self):
        d = self.getSensitivityDefinition()
        if d == "slope":
            return "S^\mathrm{slope}_i"
        if d == "relslope":
            return "S^\mathrm{rel}_i"
        return d


# Test methods for calculating extremal sensitivities:
# 1) from a N-dim cross: extremalSensitivity
# 2) from random points: extremalSensitivityRandom
if __name__ == "__main__":

    from professor.user import *
    from professor.tools.pointsampling import RandomPointGenerator
    from professor.controlplots import Sensitivity

    def testSens(binfunc, parranges):
        """Compare N-dim-cross and random-point extremal sensitivities.

        Builds bin interpolations from fake bin data. `binfunc` is used to
        calculate the bin contents. 5 bins are filled each with an
        individual scaling factor::

            cont = scale * binfunc(params)

        to check that the calculated sensitivitiy is not dependent on the
        scaling of the bin content.

        A quadratic polynomial is used for interpolation and a oversampling
        factor of 1.5 .

        Parameters
        ----------
        binfunc : function
            Function to calculate bin values.

        parranges : ParameterRange
            The range to sample the anchor points from.
        """
        # Set up the point sampling and some identifiers stubs.
        IC = getInterpolationClass("cubic", True)
        OBS = "/My/Obs"

        sampler = RandomPointGenerator(parranges)
        sampler.seed(1)
        points = [p for p in
                    sampler.generate(int(IC.minNumOfRuns(parranges.dim) * 1.5))]
        RUNSKEY = ":".join("%03i" % (i) for i in range(len(points)))

        bdlist = []
        for i in range(5):
            scale = 10**(i)
            binid = "%s:%i" % (OBS, i)
            binranges = (i * 1.0, (i+1) * 1.0)
            bd = BinDistribution(ranges.names, binid, binranges)
            # generate enough points for 1.5 over-sampling ratio
            for p in points:
                b = Bin(binranges[0], binranges[1], scale*binval(p))
                bd.addRun(p, b)
            bdlist.append(bd)

        iset = InterpolationSet.mkFromBinDists(bdlist, RUNSKEY, IC)
        sens = Sensitivity(iset, 0.01)
        sens.setSensitivityDefinition("slope")
        sens.parampoint = parranges.center
        print "definition:", sens.getSensitivityDefinition()
        print "ranges:"
        print iset.ranges
        print "dP:"
        print sens.deltaP

        # parbincenters, step = np.linspace(0, 1, 10, endpoint=False, retstep=True)
        # parbincenters += 0.5*step
        # del step

        for p in ranges.names:
            parbincenters = sens.getParameterBins(OBS, p)[0]
            print "------"
            print p
            # print sens.arraySensitivity(OBS, p, parbincenters)
            S, E = sens.extremalSensitivity(OBS, p, parbincenters, retstd=True)
            print "cross:", S
            print "  err:", E
            S, E = sens.extremalSensitivityRandom(OBS, p, 1000, retstd=True)
            print "random:", S
            print "   err:", E

    # Create bin distributions with the "same" sensitivity to PAR1 and inverse
    # sensitivity to PAR2 but bin contents varying by orders of magnitude.


    print 9*"+", "Next test", 40*"+"
    print "+ The following should yield sens(PAR1) == -2/3*sens(PAR2)"
    print "+ and cross == random"
    print "+ and sens(PAR3) == 0"
    print 60*"+"
    ranges = ParameterRange.mkFromDict({"PAR1" : [0, 4],
                                        "PAR2" : [0.1e-8, 4e-3],
                                        "PAR3" : [0.1, 1]})
    def binval(p):
        A = 4
        B = -6e3
        return A*p["PAR1"] + B*p["PAR2"]
    # testSens(binval, ranges)
    del ranges, binval

    print
    print 9*"+", "Next test", 40*"+"
    print "+ The following should yield cross == random"
    print "+ and sens(PAR3) == 0 if cubic interpolations are used."
    print 60*"+"
    def binval(p):
        A = 4
        B = -6e3
        return A*p["PAR1"]**3 + B*p["PAR2"]**2
    ranges = ParameterRange.mkFromDict({"PAR1" : [0, 1],
                                        "PAR2" : [0.1e-8, 4e-3],
                                        "PAR3" : [0.1, 1]})
    # testSens(binval, ranges)
    del ranges, binval

    print
    print 9*"+", "Next test", 40*"+"
    print "+ The following should yield cross != random"
    print "+ and sens(PAR3) == 0"
    print 60*"+"
    def binval(p):
        A = 1
        B = -10
        C = 15.
        return A*p["PAR1"]**2 + B*p["PAR2"]**2 + C*p["PAR1"]*p["PAR2"]
    ranges = ParameterRange.mkFromDict({"PAR1" : [0, 1],
                                        "PAR2" : [0.1, 1],
                                        "PAR3" : [0.1, 1]})
    testSens(binval, ranges)
    del ranges, binval

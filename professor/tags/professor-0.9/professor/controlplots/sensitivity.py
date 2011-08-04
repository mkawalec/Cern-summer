"""sensitivity.py\n
calculates the sensitivity of an observable to certain parameters
only input is a TuningData - object
"""
import numpy, professor, pylab, matplotlib.cm, time, os
from professor.tools import parameter, translate, resolution, formulas, histotools as hito
from professor import interpolation

# try:
    # from IPython.Shell import IPShellEmbed
    # ipshell = IPShellEmbed([])
# except:
    # print "Ipython shell not available."

class Sensitivity(object):
    ipolclass = interpolation.getInterpolationClass("quadratic", True) #the True is for weave

    def __init__(self, tuningdata, use_runnums=None, use_obs=None, use_veto=False):
        """ @param tuningdata: a TuningData - object """
        self._td = tuningdata
        self._tundat = tuningdata.getTuneData(self.ipolclass ,use_runnums, use_obs)
        self._use_veto=use_veto

        self._observables = use_obs
        self._runs = self.getRunNums(use_runnums)
        self._dim = self._tundat.numParams()
        self._scaler = self._tundat.scaler
        self._params = self._scaler.getKeys()
        self._thepoints = self.getParameterPoints()
        self._screensize = resolution.getScreenSize()

    def getTuningData(self):
       """ return TuningData-object """
       return self._td

    def getRunNums(self, use_runnums):
        """ determine runnums to be used """
        if type(use_runnums) == list:
            return use_runnums
        elif use_runnums is None:
            return self._td.getRunNums()
        else:
            raise ValueError('use_runnums has to be a list of strings or None')

    def getParameterPoints(self):
        """ returns a dictionary of ParameterPoint - objects generated from
        the parameter points found in the TuningData-object
        """
        return  dict([(run, parameter.ParameterPoint(
            self._td.getParams(run), self._scaler))
            for run in self._runs])

    def getYBins(self, use_obs, nrofparbins='same', low=0., high=1.,
            unscaled=False, paramindex=False):
        """ returns a numpy.array of the bincenters to be used for the
            binning of the parameter, by default, the same number of bins
            is used for the parameter as for the observable
            @param use_obs: the observable (much mor its binning) to be
                considered
            @param nrofparbins: if it is not set to 'same', an integer is
                required, otherwise the parameter will be binned using the
                same number of bins as was used for the observable
            @param low: the lower edge of the linear parameter-space
            @param high: the upper edge of the linear parameter-space
        """
        if nrofparbins == 'same':
            # number of bins of use_obs in first run found
            N = len(self._td.getMCHistos(use_obs)[self._runs[0]].getBins())
        elif type(nrofparbins) == int and nrofparbins > 0:
            N = nrofparbins
        else:
            raise StandardError('Number of parameterbins invalid!')

        ## some aesthetical improvements
        if N <10:
            N=11
        if numpy.mod(N,2) == 0:
            N = N + 1

        ## this generates the y-bins
        temp = numpy.linspace(low, high, N+1)
        if N == 1:
            temp = [.5]

        if unscaled:
            return numpy.array([self._scaler.descale(i)[paramindex]
                for i in temp])
        else:
            return temp

    def centSensitivity(self, p, binprob, param):
        """
        this calculates an observables sensitivity to one parameter in one bin
        by setting all other parametervalues to a default value, e.g. the
        center value of the interpolation (default)

        @param bindist: a BinDistribution-object
        @param param: parametername not to be set to default
        @param default: all the prametervalues to be changed will be set to
        this value
        """

        def set(point, paramindex, newval):
            """ sets the 'paramindex-th' value in point to newval """
            point[paramindex] = newval
            return point

        def fromValue(binprob, point, paramindex, p0, p, f=00.1):
            """ this is the actual sensitivity calculation for one bin """
            #dP = p +f*p0
            dP = p + f # should be more convenient than the line above
            MC_0 = binprob.ipol.getValue(set(point, paramindex, p), error=False)
            MC_plus = binprob.ipol.getValue(set(point, paramindex, dP), error=False)
            dMC = MC_plus - MC_0
            return (dMC/MC_0)*(p/dP)


        ## definition of point p0 w.r.t. whom the sensitivity is being
        ## calculated
        center = binprob.ipol.center
        paramindex = self._scaler.getIndex(param)
        p0 = center[paramindex]
        ## definition of point p where the sensitivity is to be calculated
        ## based again on the interpolation center
        point = list(center)
        point[paramindex] = p # assign the value p to the parameter param

        ## this returns a single float
        return fromValue(binprob, point, paramindex, p0, p)

    def getSens(self, runnums, use_obs, param, nrofparbins='same', intcenter=.5, errorlimit=30.,
            mode='ref'):
        # a list of use_obs's histo.BinProbs - objects
        binprob_list = self._tundat.getBinProps(use_obs)
        # list of bin numbers that matches bin content criterion
        goodbins = self.getGoodBins(use_obs, errorlimit, mode)
        # list of parameter bins --default is the same number as for x-bins
        parbins = self.getYBins(use_obs, nrofparbins)
        badbins = []

        senslist = []
        for binprob in binprob_list:
            # iterates over all param values set in parbins
            binnum = int(binprob.binid.split(':')[-1])
            if binnum in goodbins:
                temp = numpy.array([self.centSensitivity(
                        p, binprob, param) for p in parbins])
            else:
                temp =  numpy.zeros(len(parbins))
                badbins.append(binnum)
            senslist.append(temp)

        return senslist, badbins

    def getIpolSens(self, use_obs, param):
        """ Use the interpolation coefficents directly, the 2nd derivative (ii)
            is the curvature of the parabola in param direction ii and should
            hold as a measure of sensitivity directly
        """
        # Get the observables bin representation (incl. ipols) first
        binprob_list = self._tundat.getBinProps(use_obs)
        badbins = []

        paramindex = self._scaler.getIndex(param)
        senslist = []
        for binprob in binprob_list:
            binnum = int(binprob.binid.split(':')[-1])
            senslist.append([binprob.ipol.getCoefficient(paramindex, paramindex)])

        return senslist, badbins

    def getGoodBins(self, use_obs, R, mode):
        """ return a list of bin numbers that match certain criterion
            NOTE: if use_veto evaluates to True, all other settings will
            be overridden
        """
        if not self._use_veto:
            # here we choose whether to use the mc- or ref-histos for the error
            # flag/penalty
            if mode == 'mc':
                goodbins = hito.compareAllMC(use_obs, R)
            elif mode == 'ref':
                goodbins = hito.getBinsWithNotMoreThanErrorR(
                        self._td.getRefHisto(use_obs), R)
            else:
                raise StandardError('mode is neither mc nor ref: %s'%mode)
        else:
            goodbins = [int(binprob.binid.split(':')[-1]) for binprob in
                    self._tundat.getBinProps(use_obs)]
            goodbins.sort() # not sure if this is important :)
        return goodbins

    def getSensAvg_wrt_p(self, senslist, absolute=False):
        """ returns a list of tuples: (simple mean, rms) of list of
            sensitivities (arrays)
            if abs is set to True, the mean of absolute values is
            computed
        """
        if absolute:
            return numpy.array([(numpy.mean(abs(i)), formulas.rms(i))
                for i in senslist])
        else:
            return numpy.array([(numpy.mean(i), formulas.rms(i))
                for i in senslist])

    def getSensMax_wrt_p(self, senslist):
        """ returns a list of tuples: (simple mean, rms) of list of
            sensitivities (arrays)
            if abs is set to True, the mean of absolute values is
            computed
        """
        temp = []
        #return numpy.array([(numpy.mean(abs(i)), formulas.rms(i))
            #for i in senslist])
        for s_pbin in senslist:
            maxabsindex = map(abs, s_pbin).index(max(map(abs, s_pbin)))
            temp.append((s_pbin[maxabsindex],0))
            #temp.append((numpy.median(s_pbin),0))
        return temp


    ## everything from is not yet recoded...
    def getColorBoundaries(self, cscale, Z, sens):
        if cscale=='single':
            return self.getVminVmax(Z)
        elif cscale=='all':
            return self.getGlobalVminVmax(sens)
        else:
            raise StandardError('cscale not set: cscale = '+cscale)

    def getVminVmax(self, array):
        """ return vmin, vmax for pcolor by parsing sensitivity-array for max()
            and max(abs()) values and comparison of both
        """
        Smaxabs = max([max(abs(numpy.array(subarray))) for subarray in array])
        return (-1.*Smaxabs, Smaxabs)

    def getGlobalVminVmax(self, alist):
        gmax = max([self.getVminVmax(array)[1] for array in alist])
        return (-1.*gmax, gmax)


class CubicSensitivity(Sensitivity):
    ipolclass = interpolation.getInterpolationClass("cubic", True) #the True is for weave
    def __init__(self, tuningdata, use_runnums=None, use_obs=None, use_veto=False):
        super(CubicSensitivity, self).__init__(tuningdata, use_runnums=None, use_obs=None, use_veto=False)

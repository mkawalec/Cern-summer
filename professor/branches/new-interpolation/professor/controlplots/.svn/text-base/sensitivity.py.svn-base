"""sensitivity.py\n
calculates the sensitivity of an observable to certain parameters
only input is a TuningData - object
"""
import numpy, professor, pylab, matplotlib.cm, time, os
from professor.tools import parameter, translate, resolution, formulas
from professor.controlplots import checkbins as cb
matplotlib.rc('text', usetex=True)

class Sensitivity:

    def __init__(self, tuningdata):
        """ @param tuningdata: a TuningData - object """
        self._td = tuningdata
        self._observables = tuningdata.getMCHistoNames()
        self._runs = tuningdata.getRunNums()
        self._dim = len(tuningdata._params[self._td.getRunNums()[0]])
        self._scaler = professor.histo.TuningData.getScaler(self._td)
        self._params = self._scaler.getKeys()
        self._thepoints = self.getParameterPoints()
        self._screensize = resolution.getScreenSize()
        ## for testing purposes only
        self._interp_list = {}
        self._sensitivities = {}

    def getTuningData(self):
       """ return TuningData-object """
       return self._td

    def getParameterPoints(self):
        """ returns a dictionary of ParameterPoint - objects generated from
        the parameter points found in the TuningData-object
        """
        return  dict([(run, parameter.ParameterPoint(
            self.getTuningData().getParams(run), self._scaler))
            for run in self.getTuningData().getRunNums()])

    def getBinCenter(self, bin):
        """ determine the bins center using its lower and upper edge
        @param bin: either a histo.Bin or a interpolation.bindistribution.
        BinDistribution object
        """
        if isinstance(bin,
                professor.interpolation.bindistribution.BinDistribution):
            low, up = bin.getBinrange()
        elif isinstance(bin, professor.histo.Bin):
            low, up = bin.getXRange()
        else:
            raise StandardError('bin is neither from histo.Bin'+
                    'nor interpolation.bindistribution.BinDistribution')
        return low + .5*(up - low)

    def getXBins(self, use_obs, for_cmap=True):
        """ return a list of bin-centers of the ref-histo of observable use_obs
        """
        #temp = numpy.array([self.getBinCenter(bin) for bin in
        #        self.getTuningData().getRefHisto(use_obs).getBins()])
        temp = cb.getPrintRange(self._td, use_obs, for_cmap)
        return temp

    def getYBins(self, use_obs, nrofparbins='same', low=0., high=1., unscaled=False, paramindex=False):
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
        temp = numpy.linspace(low, high, N+1)
        if unscaled:
            return numpy.array([self._scaler.descale(i)[paramindex]
                for i in temp])# use map()???
        else:
            return temp

    def centeredSensitivity(self, p, bindist, param, newcenter=False, use_grad=False):
        """
        this calculates an observables sensitivity to one parameter in one bin
        by setting all other parametervalues to a default value, e.g. the
        center value of the interpolation (default)

        @param bindist: a BinDistribution-object
        @param param: parametername not to be set to default
        @param default: all the prametervalues to be changed will be set to
        this value
        """
        center = bindist.getCenter()
        paramindex = center.getIndex(param)

        if type(newcenter) == float:
            p0 = newcenter
            # setting all parameter values to newcenter
            point = newcenter*numpy.ones(len(self._params))
            # now assign the value p to the desired parameter param
            point[paramindex] = p
        else:
            # here we use the interpolationcenter as defaults
            p0 = center._scaled[paramindex]
            point = list(center._scaled)
            # and again assign the value p to the desired parameter param
            point[paramindex] = p

        return self.getSensitivity(bindist,
                point, paramindex, p0, p, use_grad=use_grad)

    def projectedSensitivity(self, p, bindist, param, absolute=False, use_grad=False):
        """ calculates an averaged sensitivity using the anchor-points of all
        runs instead of (just one) interpolation center
        """
        # some zeros, to use the += statement with arrays
        # projections = numpy.zeros(bindist.getBD().dim())
        projections = 0#numpy.zeros(bindist.getBD().dim())
        # iterate over all parameterpoints (all runs)
        for ppoint in self.getParameterPoints().values():
           # using parameterpointvalues
           paramindex = ppoint.getIndex(param)
           p0 = ppoint._scaled[paramindex]
           temp = ppoint._scaled
           # assign the value p to the desired parameter param
           # TODO use list?
           temp[paramindex] = p
           if absolute:
               projections += abs(self.getSensitivity(bindist, temp,
                   paramindex, p0, p, use_grad=use_grad))
           else:
               projections += self.getSensitivity(bindist, temp, paramindex,
                   p0, p, use_grad=use_grad)
        # simple mean
        return projections/len(self.getParameterPoints())

    def getSensitivity(self, bindist, point, paramindex, p0, p, use_grad=False):
        """ actually calculates the Sensitivity Value of one bin to one
        parameter value p
        @param bindist: InterpolationObject representing one Bin
        @param point: the ParameterPoint we want to use for the calculation
        @type point: list
        @param paramindex: the index of the desired parameter in
                ParameterPoint._scaled
        @param p0: a p0 float
        @param p: float
        """
        def fromGrad(bindist, point, paramindex):
            if bindist.getValueFromScaled(point) != 0:# here we exclude division by 0
                return p*(bindist.getGradientFromScaled(point)[paramindex]
                    /bindist.getValueFromScaled(point))
            else:
                return 0.

        def fromValue(bindist, point, paramindex, p0, p):
            MC_0 = bindist.getValueFromScaled(set(point, paramindex, p0))
            MC_x = bindist.getValueFromScaled(set(point, paramindex, p))
            if MC_x != 0 and p != p0:
                return ((MC_x - MC_0)*p)/((p - p0)*MC_x)
            else:
                return 0.

        def set(point, paramindex, newval):
            point[paramindex] = newval
            return point

        #interpvalue = bindist.getValueFromScaled(point)
        #if interpvalue != 0 and p!=p0:# here we exclude division by 0
            #return p*(bindist.getGradientFromScaled(
            #    point)[paramindex]/interpvalue)
        if use_grad:
            return fromGrad(bindist, point, paramindex)
        else:
            return fromValue(bindist, point, paramindex, p0, p)
        #else: #TODO logger, if temp=0
        #    return 0

    def calcSensForSingleObservable(self, runnums, use_obs, nrofparbins='same',
            method='centered', intcenter=.5, newcenter=False, errorlimit=30.,
            mode='ref', absolute=False):
        """ sensitivity calculation for one observable
        @param runnums: the set of runnumbers used for the interpolation
        @param use_obs: the observable
        @param use_run: if None, an average sensitivity is calculated,
        otherwise runnumber use_run is used meaning that only one point in
        parameterspace will be used for the calculation
        @param R: threshold criterion for bin content

        return value is a dictionary {runnumber : list of calculated
        sensitivities}
        """
        # list of interpolations (one for each bin)
        interp_list = numpy.array(self.getTuningData().buildBinDistList(runnums
            , use_obs, intcenter=intcenter))[:,1]

        # list of bin numbers that matches bin content criterion
        goodbins = self.getGoodBins(use_obs, errorlimit, mode)
        badbins = []
        # for testing purposes only
        # self._interp_list[use_obs] = interp_list

        # list of parameter bins
        parbins = self.getYBins(use_obs, nrofparbins)

        # actual calculation over runs and bins
        sensitivity={}
            # iterate over all params
        for param in self._params:
            asd = []
            # iterates over all params
            for binnum, interp in enumerate(interp_list):
                # iterates over all param values of the current param
                if binnum in goodbins:
                    if method =='centered':
                        temp = numpy.array([self.centeredSensitivity(
                            p, interp, param, newcenter=newcenter)
                            for p in parbins])
                    elif method =='projected':
                        temp = numpy.array([self.projectedSensitivity(
                            p, interp, param, absolute=absolute)
                            for p in parbins])
                    else:
                        raise StandardError('method is not valid: %s'%method)
                else:
                    temp =  numpy.zeros(len(parbins))
                    badbins.append(binnum)
                asd.append(temp)
            sensitivity[param] = numpy.array(asd)

        return sensitivity, badbins

    def doTheCalculationForAllBins(self, interp_list, runpoint,
            method='center'):
        """this calculates dMC/MC for all BinDistributions found in interp_list
        @param interp_list: a list of BinDistribution-objects
        @param runpoint: a ParameterPoint - object
        """
        temp = []
        for i, interp in enumerate(interp_list):
            if not interp.getValue(runpoint) ==0:
                temp.append(interp.getGradient(
                    runpoint)/interp.getValue(runpoint))
            else:
                temp.append(numpy.zeros(self._dim))
        return numpy.array(temp)

    def getBinsWithNotMoreThanErrorR(self, histo, R):
        """ return a list of bin-numbers that match relative error threshold
        criterion
        """
        if R < 0:
            raise StandardError('relative error cannot be negative!')
        else:
            return [i for i, bin in enumerate(histo) if bin.getYVal() !=0 and bin.getYErr()/bin.getYVal() <= R/100.]

    def compareAllMC(self, use_obs, R):
        """ return a list of bin-numbers that match threshold criterion in all
            MCHistos
            @param use_obs: the observable
            @param R: threshold, only Bins whose content is >= R are accepted
        """
        allbins = numpy.arange(len(self._td.getRefHisto(use_obs)))
        alllists = [self.getBinsWithNotMoreThanErrorR(
            histo, R) for histo in self._td.getMCHistos(use_obs).values()]
        return [item for item in allbins if self.itemIsInAllLists(
            item, alllists)]

    def itemIsInAllLists(self, item, lists):
        """ check whether a certain item is in contained in all of several
            lists
            @param item: the item to check for
            @param lists: a list of lists
        """
        for i in lists:
            if item in i:
                continue
            else:
                return False
        return True

    def getGoodBins(self, use_obs, R, mode):
        """ return a list of bin numbers that match certain criterion """
        if mode == 'mc':
            goodbins = self.compareAllMC(use_obs, R)
        elif mode == 'ref':
            goodbins = self.getBinsWithNotMoreThanErrorR(
                    self._td.getRefHisto(use_obs), R)
        else:
            raise StandardError('mode is neither mc nor ref: %s'%mode)
        return goodbins

    def getBadBins(self, use_obs, errorlimit, mode):
        return []


    def plotOverview(self, use_obs, intcenter=.5, newcenter=.5,
            nrofparbins = 'same', cmap=matplotlib.cm.RdYlBu, errorlimit=30.,
            mode='ref', method='centered', cscale='single', logscale=(True,
                False), printshow='show'):
        #TODO: docstring
        """ docstring
        """
        methods = {'centered':('interpolation center', newcenter), 'projected':(True, False)}

        x = self.getXBins(use_obs)
        y = self.getYBins(use_obs)
        X, Y = numpy.meshgrid(x,y)
        fig = pylab.figure(facecolor='w')
        # fig.set_size_inches(self._screensize)

        # this creates the title
        self.createTitleLegend(use_obs, method, mode, errorlimit, intcenter, newcenter)

        nrows = len(self._params)
        ncols = len(methods[method])

        for i, meth in enumerate(methods[method]):
            # here we say, that we want to include all runs for the calculation
            # and what minimum bin content we want to accept
            if method == 'projected':
                sens = self.calcSensForSingleObservable(self._runs, use_obs,
                        nrofparbins, method=method, absolute=meth,
                        intcenter=intcenter,
                        errorlimit=errorlimit, mode=mode, )
                self._temp=sens

            elif method == 'centered':
                sens = self.calcSensForSingleObservable(self._runs, use_obs,
                        nrofparbins, method=method, newcenter=meth,
                        intcenter=intcenter,
                        errorlimit=errorlimit, mode=mode, )
                self._temp=sens

            # handles arrangement of subplots
            for j, param in enumerate(self._params):
                Z = sens[param]
                if cscale=='single':
                    vmin, vmax = self.getVminVmax(Z)
                elif cscale=='all':
                    vmin, vmax = self.getGlobalVminVmax(sens)
                else:
                    raise StandardError('cscale not set: cscale = '+cscale)
                sp = fig.add_subplot(nrows, ncols, ncols*j + i + 1)
                coll = sp.pcolormesh(X, Y, Z.transpose(),
                        cmap=cmap, vmin=vmin, vmax=vmax)
                if j == nrows -1: # have xlabel only once in a column 
                    sp.set_xlabel('\\small Observable')
                if i == 0: # have ylabel only once in a row
                    sp.set_ylabel('\\Large %s'%translate.translate(param))
                pylab.xlim((x[0], x[-1]))
                ## colorbar settings
                cbar = fig.colorbar(coll)
                cbar.set_label('\\small Sensitivity')
        ## either print to file or show in gtk mainloop
        if printshow == 'print':
            pylab.savefig(self.createFilename(method, use_obs, intcenter,
                newcenter, errorlimit, mode), dpi=100, orientation='landscape',
                format='png')
            pylab.close(fig)

    def plotOverview2(self, use_obs, intcenter=.5, nrofparbins = 'same',
            cmap=matplotlib.cm.RdYlBu, errorlimit=30., mode='ref',
            method='centered', cscale='single', printshow='show'):
        #TODO: docstring
        """ docstring
        """
        methods = {'centered':('interpolation center','dummy'), 'projected':(True, False)}

        x = self.getXBins(use_obs)
        self._x=x

        nrows = len(self._params)
        ncols = len(methods[method])

        if method == 'centered':
            sens, badbins = self.calcSensForSingleObservable(self._runs, use_obs,
                    nrofparbins, method=method, newcenter=methods[method],
                    intcenter=intcenter, errorlimit=errorlimit, mode=mode)
        elif method == 'projected':
            sens, badbins = self.calcSensForSingleObservable(self._runs, use_obs,
                    nrofparbins, method=method, absolute=False,
                   intcenter=intcenter, errorlimit=errorlimit, mode=mode)
        ## this is for our averaged sensitivity
        vmin_g, vmax_g = self.getGlobalVminVmax(sens)
        # handles arrangement of subplots
        fig = pylab.figure(facecolor='w')
        fig.set_size_inches(self._screensize)
        for j, param in enumerate(self._params):
            y = self.getYBins(use_obs, nrofparbins=nrofparbins,
                    unscaled=True, paramindex=j)
            self._y=y
            X, Y = numpy.meshgrid(x,y)
            Z = sens[param]
            ## Colormap, left hand plot
            sp_1 = fig.add_subplot(nrows, ncols, ncols*j + 1)
            vmin, vmax = self.getColorBoundaries(cscale, Z, sens)
            coll = sp_1.pcolormesh(X, Y, Z.transpose(), cmap=cmap, vmin=vmin, vmax=vmax)
            pylab.xlim((x[0], x[-1]))
            cbar = fig.colorbar(coll)
            ## Averaged Sensitivitiy (1D), right hand plot
            sp_2 = fig.add_subplot(nrows, ncols, ncols*j + 2)
            pylab.axhline(y=0, color='k', ls='--' )
            A = self.getSensAvg_wrt_p(sens, param)
            avg_x = self.getXBins(use_obs, for_cmap=False)
            for i, V in enumerate(A):
                if i in badbins:
                    pylab.errorbar(avg_x[i], V[0], V[1], fmt='kx')
                else:
                    pylab.errorbar(avg_x[i], V[0], V[1], fmt='rx')
            pylab.xlim((x[0], x[-1]))
            #pylab.errorbar(self.getXBins(use_obs, for_cmap=False), A[:,0], A[:,1], fmt='rx')
            #pylab.errorbar(self.getXBins(use_obs, for_cmap=False)[-4], A[:,0][-4], A[:,1][-4], fmt='ko')
            ## subplot labels
            if j == nrows -1: # have xlabels only once in a column 
                sp_1.set_xlabel(translate.observables[use_obs][1])#'\\small Observable')
                sp_2.set_xlabel(translate.observables[use_obs][1])#'\\small Observable')
            cbar.set_label('\\small Sensitivity')
            sp_1.set_ylabel('\\Large %s'%translate.translate(param))
            sp_2.set_ylabel('\\small avg. Sensitivity')
            pylab.ylim(vmin_g, vmax_g)
        ## this creates the title
        self.createTitleLegend2(use_obs, method, mode, errorlimit, intcenter, badbins)

        ## either print to file or show in gtk mainloop
        if printshow == 'print':
            pylab.savefig(self.createFilename(method, use_obs, intcenter,
                errorlimit, mode), dpi=75, orientation='landscape',
                format='png')
            pylab.close(fig)

    def getSensAvg_wrt_p(self, sensdict, param):
        """ returns a simple mean of th"""
        return numpy.array([(numpy.mean(i), formulas.rms(i))
            for i in sensdict[param]])

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
        Smaxabs = max([max(abs(subarray)) for subarray in array])
        return (-1.*Smaxabs, Smaxabs)

    def getGlobalVminVmax(self, adict):
        gmax = max([self.getVminVmax(array)[1] for array in adict.values()])
        return (-1.*gmax, gmax)

    def createTitleLegend(self, use_obs, method, mode, errorlimit, intcenter, newcenter):
        # this creates the title
        title = '\\Large \\underline{%s} sensitivity of \\quad \\bf{%s}\\quad\\small{\\tt{(%s)}}'%(method,
                self._td.getTitle(use_obs).replace('_', '\\_').replace(
                    '^', '\\^'), use_obs.replace('_', '\\_') )
        params = 'to params:'
        for i in self._params:
            params += '\\quad \\Large{%s} \\normalsize{\\tt{(%s)}} '%(
                    translate.translate(i), i)

        # create legend
        legend = 'upper limit of relative errors set to %.1f percent with respect to '%errorlimit
        if mode == 'ref':
            legend += 'the Reference Histo'
        elif mode == 'mc':
            legend += 'all MC Histos'
        if method == 'centered':
            legend += '\\\\interpolation center (left plot) = %.2f, right hand center = %.2f'%(intcenter, newcenter)
        elif method == 'projected':
            legend += '\\\\interpolation center (all plots) = %.2f, left: absolute values, right: values'%intcenter

        pylab.figtext(.5,.96, title,ha='center')
        pylab.figtext(.5,.92, params,ha='center')
        pylab.figtext(.5,.01, legend,ha='center')

    def createTitleLegend2(self, use_obs, method, mode, errorlimit, intcenter, badbins):
        # this creates the title
        title = '\\Large \\underline{%s} sensitivity of \\quad \\bf{%s}\\quad\\small{\\tt{(%s)}}'%(method,
                self._td.getTitle(use_obs).replace('_', '\\_').replace(
                    '^', '\\^'), use_obs.replace('_', '\\_') )
        params = 'to params:'
        for i in self._params:
            params += '\\quad \\Large{%s} \\normalsize{\\tt{(%s)}} '%(
                    translate.translate(i), i)
        # create legend
        legend = 'rel. errors $\\leq$ %.1f pct. w.r.t. '%errorlimit
        if mode == 'ref':
            legend += 'the Reference Histo;'
        elif mode == 'mc':
            legend += 'all MC Histos;'
        legend += '\\quad interp. center  = %.2f $\\forall$ coord.'%intcenter
        legend += '\\quad Nr. of bins omitted: %i'%len(badbins)


        pylab.figtext(.5,.96, title,ha='center')
        pylab.figtext(.5,.92, params,ha='center')
        pylab.figtext(.5,.01, legend,ha='center')

    def createFilename(self, method, use_obs, intcenter, errorlimit,
            mode):
        # create timestamp
        year, month, day = map(str, time.localtime()[0:3])
        date = year + '-' + month + '-' + day
        # create some subdirectories
        subfolders = ['pics', date]#, use_obs.replace('/', '_')]
        prefix = ''
        for i in subfolders:
            prefix += i + '/'
            if not os.path.exists(prefix):
                os.system('mkdir ' + prefix)
                print 'new folder created: ', prefix
        # single filename
        fname = use_obs + '_' + method + '_sens_interp_at_' + str(intcenter)
        fname += 'rel_error_leq_' + str(errorlimit) + '_pct_of_' + mode
        return prefix +  (fname.replace('.', 'point')).replace('/','_')

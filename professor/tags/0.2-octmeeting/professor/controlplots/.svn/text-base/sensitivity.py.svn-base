#!/usr/bin/python
# vim:fileencoding=utf-8
"""sensitivity.py\n
    this provides methods to calculate the sensitivity of an observable
    to parameterchanges in AIDA-format from a TuningData-object.
"""
import numpy, random, time
from professor.interpolation.analytic_interpolation import BinDistribution
from professor.histo import Bin
from professor.interpolation.testBase import randomPoint

class Sensitivity:

    def __init__(self, tuningdata):
        self._td = tuningdata
        self._observables = tuningdata.getMCHistoNames()
        self._runs = self.getRuns()
        self._params = self.setParameters()
        self._mcsets = self.determineMCSets()

    def getRuns(self):
        """ this returns the run-idenificators. this worls only, if
            all observables in the tuningdata share the same runs
        """
        firstkey = self._td._mchistos.keys()[0]
        d = {}
        return d.fromkeys(self._td._mchistos[firstkey])

    def setParameters(self):
        """ returns a dictionary of all parameters and their values in all runs
        """
        pars = {}
        for key in self._runs.iterkeys():
            pars[key] = self._td.getParams(key)
        return pars

    def getParDim(self, run):
        """ obsolete now, returns the number of parameters varied in run
            @param run: a dictionary key
        """
        return len(self._params[run].keys())

    def determineMCSets(self):
        """ returns a list of the different sets of parameters varied in all
            runs
        """
        mcsets = []
        for k, v in self._params.iteritems():
            if not v.keys() in mcsets:
                mcsets.append(v.keys())
        return mcsets

    def getYVals(self, observable, mcset):
        """ obsolete now, returns dictionary of the actual bin-entries of an
            observable in a mcset
            @param observable: a key that names the observable
            @param mcset: one of the sets of varied parameters returned by L:{determineMCSets()}
        """
        yvals = {}
        for run, v in self._params.iteritems():
            if v.keys() == mcset:
                yvals[run] = numpy.array( [bin.getYVal() for bin in self._td.getMCHistos(observable)[run].getBins()] )
        return yvals

    def getDeltaP(self, mcset, p0run):
        """ return a dictionary of all (p_i - p_0)
            @param mcset: one of the sets of varied parameters returned by
                L:{determineMCSets()}
            @param p0run: a key from L:{getRuns()} to identify the run to which
                differences are calculated against
        """
        diff = lambda key: numpy.array(map(float,self._params[key].values())
                )- numpy.array(map(float,self._params[p0run].values()))
        deltap = {}
        for k, v in self._params.iteritems():
            if v.keys() == mcset:
                deltap[k] = diff(k)
        return deltap

    def getParWeight(self, run, par, mcset, p0run):
        """ returns (p_i - p_0)/p_i
        """
        paridx = mcset.index(par)
        return self.getDeltaP(mcset, p0run)[run][paridx]/float(self._params[run][par])

    def selectInterpolationParams(self, pardict, observable):
        """ in future, this should include a feature that ensures clever
            selection of parameters, since they are now chosen randomly
            @param pardict: a dictionary that holds the names of parameters
                as keys
        """
        bd = BinDistribution(observable, 1, pardict.keys())
        bd.setCenter(numpy.zeros(len(pardict.keys())))

        intplparams = []
        runkeys = pardict[pardict.keys()[0]].keys()
        print 'run | parameters to be used for analytic interpolation'
        for i in xrange(bd.requiredRuns()):
            run = runkeys[random.randint(0, len(runkeys)-1)]
            p = [pardict[par][run] for par in pardict.keys()]
            print run, '#', p
            runkeys.remove(run)
            intplparams.append(p)

        return intplparams

    def interpolate(self, observable, mcset):
        """ this does the interpolation for all bins in the mcsetand returns
            a list that contains all the binditribution-objects of a specific
            observable
        """
        t0 = time.time()
        params = {}
        for i, par in enumerate(mcset):
            params[par] = dict([(k,map(float, v.values())[i]) for k,v in
                self._params.iteritems() if v.keys() == mcset])

        intplparams = self.selectInterpolationParams(params, observable)

        bdists = []
        runkeys = params[params.keys()[0]].keys()
        for bin in self._td._mchistos[observable][runkeys[0]].getBins():
            bd = BinDistribution(observable, bin.getXRange(), params.keys())
            bd.setCenter(numpy.zeros(len(params.keys())))
            for i in xrange(bd.requiredRuns()):
                bd.addBin(bin, intplparams[i])
            bd.calcInterpolationCoefficients()
            bdists.append(bd)
        # print 'intpl: time spent: %.2f seconds'%(time.time() - t0)
        return bdists

    def getEasedIntplCoeffs(self, bd, mcset):
        """ returns the interpolation-coefficients in a well shaped form:
            - the (so far obolete) scalar 'offset'
            - the vector of linear interpolation-coefficients
            - the matrix of quadratic interpolation coeffs (its not really
              a matrix, only the diagonal and the upper-off-diagonal-elements
              are non zero, the real matrix in our model of a parabolic
              interpolation should be symmetric
            @param bd: this is a BinDistributio object
        """
        # linear interpolation coefficients
        lin = []
        for i1 in xrange(len(mcset)):
            lin.append(bd.getCoefficient(i1))

        # create a 'matrix' of quadratic interpolation coefficients
        t=[]
        z=numpy.zeros(len(mcset))
        for i in xrange(0, len(mcset)):
            t.append(z)
        qc=numpy.array(t)

        for i1 in xrange(len(mcset)):
            for i2 in xrange(i1, len(mcset)):
                # print 'i,j=',i1, i2
                qc[i1][i2] = bd.getCoefficient(i1, i2)
                # print qc[i1][i2],'#'
        return (bd.getCoefficient(), lin, qc)

    def getDMC(self,observable, bd, par, mcset, p0): # called bin-wise
        """ return list of a bins MC-answer-deviations relative to MC(p0),
            using interpolation-coefficients\n
            k ... parameters\n
            r ... runs\n
            n ... total number of parameters
            @param par: String that names the parameter, needs to be one of
                        mcset entries
            dmc=dp_[k]*(
                        a_[k] + sum_{i=1}^{k}(a_[ik]*dp_[i])
                              + sum_{i=k}^{n}(a_[ki]*dp_[i])
                       )
        """
        p0run = p0
        alldmc = {}
        coeff = self.getEasedIntplCoeffs(bd, mcset)
        mcruns = [k for k, v in self._params.iteritems() if v.keys() == mcset]
        paridx = mcset.index(par)

        for run in mcruns:
            dmc = 0
            # exclude p0
            if run != p0run:
                sumall =[]
                sum1= [coeff[2][i][paridx]*self.getDeltaP(mcset, p0run
                    )[run][i] for i in xrange(0, paridx + 1)]
                sum2 = [coeff[2][paridx][j]*self.getDeltaP(mcset, p0run
                    )[run][j] for j in xrange(paridx, len(mcset))]
                dmc = self.getDeltaP(mcset, p0run)[run][paridx]*(
                        coeff[1][paridx] + sum(sum1) + sum(sum2))
            alldmc[run] = dmc
        return alldmc

    def getYValue(self, observable, run, binname):
        """ return a specific bin-entry
        """
        t0 = time.time()
        yval = [bin.getYVal() for bin in self._td._mchistos[observable][run
            ].getBins() if bin.getXRange() == binname]
        return yval[0]

    def getSensitivity(self,observable, bd, par, mcset, p0='000'):
        """ this calculates and returns the sensitivity
        """
        p0run = p0
        mcruns = [k for k, v in self._params.iteritems() if v.keys() == mcset]
        DMC =  self.getDMC(observable, bd, par, mcset, p0run)
        sens = {}
        for run in mcruns:
            if run != p0run:
                sens[run] = (DMC[run]/self.getYValue(observable, run,
                    bd.getBinname()))/self.getParWeight(run, par, mcset,p0run)
        return sens

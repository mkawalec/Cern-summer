"""fit.py

"""

import numpy, pylab, sys, random, pickle
from professor import histo
from professor.controlplots import envelope
from professor.interpolation import *
from scipy import optimize
# from scipy.optimize import leastsq
from professor.interpolation.testBase import PointGenerator
import matplotlib.axes3d as p3


class PointSelector(PointGenerator):
    def __init__(self, dimensions, available_points):
        self.dim = dimensions
        self.points = []
        self._avbpts = available_points

    def nextPoint(self, quiet=True):
        i = 0
        if self.points == []:
            newpoint = self._avbpts[0]
        else:
            newpoint = self.points[-1]
        while not self.testDistance(newpoint.values()[0]):# and len(self.points) < len(self._avbpts):
            if not quiet:
                print newpoint, "failed"
            newpoint = self._avbpts[i]
            i=i+1
        self.points.append(newpoint)
        return newpoint

    def testDistance(self, point):
        "Returns True if point fulfills the minimal distance to other points criterion."
        for p in self.points:
            dp = abs(p.values()[0] - point)
            if dp.min() <= self.getMinDistance():
                return False
        return True

class DistributorError(StandardError):
    pass

class Distributor:
    def __init__(self, td):
        self._td = td
        self._obs = td.getMCHistoNames()
        self._mcsets = self.determineMCSets()
        self._nrofruns = -1
        self._bdists = {}

    def getRunkeys(self):
        """ returns a list of the runkeys if they are equal for all observables
        """
        temp = [self._td.getMCHistos(obs).keys() for obs in self._obs]
        for i in xrange(len(temp)):
            if cmp(temp[0], temp[i])==0:
                pass
            else:
                raise DistributorError('something went wrong with the runkeys,'+
                        'they are not equal!')
        return temp[0]

    def determineMCSets(self):
        """ returns a list of the different sets of parameters varied in all
            runs
        """
        mcsets = []
        for k in self.getRunkeys():
           if not self._td.getParams(k).keys() in mcsets:
               mcsets.append(self._td.getParams(k).keys())
        return mcsets

    def getAvailablePoints(self, mcset):
        """ the parameter values of a certain mcset """
        newkeys = [run for run in self.getRunkeys() if self._td.getParams(
            run).keys() == mcset]
        points = []
        for run in newkeys:
            temp = {run:numpy.array([float(self._td.getParams(run)[par])  for par in mcset])}
            points.append(temp)
        return points

    def getMinNrOfRuns(self, mcset):
        bd = analytic_interpolation.BinDistribution('dummy', [0, 1], mcset)
        return bd.requiredRuns()

    def setNrOfRuns(self, mcset, nr):
        if nr < self.getMinNrOfRuns(mcset) or nr > len(self.getRunkeys()):
            raise DistributorError('number of runs bad, should be between'+
                    ' %i and %i!'%(self.getMinNrOfRuns(mcset), len(
                        self.getRunkeys())))
        else:
            self._nrofruns = nr

    def getNrOfRuns(self):
        return self._nrofruns

    def getBins(self, obs):
        temp = []
        for histo in self._td.getMCHistos(obs).values():
            temp.append([bin.getXRange() for bin in histo.getBins()])

        for i in xrange(len(temp)):
            if cmp(temp[0], temp[i]) == 0:
                pass
            else:
                raise DistributorError('the binning is not equal in all runs!')
        return temp[0]

    def getPointsForInterpol(self, mcset, avbpts, Runs):
        ps = PointSelector(len(mcset), avbpts)
        points = []
        while len(ps.points) < Runs:
            points.append(ps.nextPoint())
        return points


    def getBinDistributions(self, obs, mcset, recreate=False):
        if self._bdists.has_key(obs) and recreate is False:
            return self._bdists[obs]
        else:
            temp=[]
            usedpoints = []
            i=0
            if self._nrofruns == -1:
                print 'nrofruns not set, using minimum number instead'
                Runs = self.getMinNrOfRuns(mcset)
            else:
                Runs = self._nrofruns

            avbpts = self.getAvailablePoints(mcset)
            points = self.getPointsForInterpol(mcset, avbpts, Runs)
            for i, bin in enumerate(self.getBins(obs)):
               bd = analytic_interpolation.BinDistribution(obs, [bin[0], bin[1]], mcset)
               bd.setCenter(numpy.zeros(len(mcset)))
               # ps = PointSelector(len(mcset), avbpts)
               # while len(ps.points) < Runs:
               for pt in points:
                   # pt, key = ps.nextPoint()
                   v = histo.Bin(bin[0], bin[1], self._td.getMCHistos(obs)[pt.keys()[0]][i].getYVal() )
                   # v = histo.Bin(bin[0], bin[1], self._td.getMCHistos(obs)[pt.keys()[0]][i].getYVal() )
                   bd.addRun(v, pt.values()[0])
                   # usedpoints.append(key)
               bd.calcInterpolationCoefficients()
               temp.append(bd)
            self._bdists[obs] = temp
            self._nrofruns = Runs
            return temp, points

class FitTester:
    def __init__(self, dtr, obs, mcset):
        """ @ param dtr: Distributor object"""
        self._dtr = dtr
        self._obs = obs
        self._mcset = mcset
        self._params = [[float(par) for par in dtr._td.getParams(k).values(
                ) if dtr._td.getParams(k).keys(
                    ) == mcset] for k in dtr._td._params.iterkeys()]
        bds, usdpts = dtr.getBinDistributions(obs, mcset)
        self._bdists = bds
        self._usedpoints = usdpts

    def addRuns(self, howmany=1):
        if howmany + self._dtr.getNrOfRuns() < len(self._dtr.getRunkeys()):
            self.regenerateBD(howmany+self._dtr.getNrOfRuns())
        else:
            raise StandardError('invalid number of runs')

    def regenerateBD(self, howmany):
        self._dtr.setNrOfRuns(self._mcset, howmany)
        bds, usdpts = self._dtr.getBinDistributions(self._obs, self._mcset, recreate=True)
        self._bdists = bds
        self._usedpoints = usdpts

    def reset(self):
        self.regenerateBD(self._dtr.getMinNrOfRuns(self._mcset))

    def printTheory(self, points=100):
        xmin = min(self._params)
        xmax = max(self._params)
        print xmin, xmax
        R = numpy.linspace(xmin[0], xmax[0], points)
        allpoints = [[(p, bd.calcValue([p])) for p in  R]
                for bd in self._bdists]

        B = numpy.arange(len(self._bdists))
        X, Y = numpy.meshgrid(R, B)
        Z = numpy.zeros((len(Y), len(X)), 'Float32')
        for i, bin in enumerate(allpoints):
            for j, point in enumerate(bin):
                ix = int((allpoints[i][j][0])*numpy.floor(points/xmax[0]))
                Z[i,ix] = allpoints[i][j][1]
        fig = pylab.figure()
        string = ''
        for pt in self._usedpoints:
            string = string + str(pt.values()[0]) +'\n'
        pylab.figtext(0.5,0.95,'Observable: '+str(self._obs) + ' - using '
                + str(len(self._usedpoints)) + ' points for the interpolation'
                , horizontalalignment='center')
        pylab.figtext(0.8,0.25,'Points:'+ string, horizontalalignment= 'right')
        ax = p3.Axes3D(fig)
        ax.plot_wireframe(X,Y,Z)
        ax.set_xlabel('parameter')
        ax.set_ylabel('bin')
        ax.set_zlabel('interpol')

    def printAllTheories(self, start, stop, step):
        self.printTheory()
        for i in xrange(start, stop, step):
            self.addRuns(step)
            self.printTheory()

    def fitfunc(self, p, refhist, switch='noerr', pos='all'):
        """ definintion of functions to fit """
        errexp = lambda ans, ref: (ans-ref)**2/float(ref)

        _interpol = numpy.array([bd.calcValue(p) for bd in self._bdists])
        _reference = numpy.array([(bin.getYVal(), bin.getYErr()
            ) for bin in refhist.getBins()])
        if switch == 'noerr':
           chiq = [(_interpol[i] - _reference[i][0])**2 for i in xrange(len(
               _interpol)) ]
        else:
           raise StandardError('Feature not yet implemented.')

        if pos == 'all':
           return sum(chiq)
        else:
           return chiq[pos]

    def printChiq(self, xmin, xmax, points, switch = 'noerr', pos = 'all'
            , refrun = '000'):
        refhist = self._dtr._td.getMCHistos(self._obs)[refrun]
        temp = []
        ans= []
        for num, i in enumerate(numpy.linspace(xmin, xmax, points)):
            temp.append(( i, self.fitfunc([i], refhist, switch, pos)))
        X= numpy.array(temp)
        pylab.figtext(.5,.95, 'Chi**2 for Observable %s'%(self._obs),
                horizontalalignment='center')
        pylab.plot(X[:,0], X[:,1], '+', label=refrun)
        pylab.legend(loc=0)

    def doFit(self, p0=[0], refrun = '000'):
        ref = self._dtr._td.getMCHistos(self._obs)[refrun]
        pbest = optimize.fmin_powell(self.fitfunc, p0, args=(ref, 'noerr'),
                disp = 0)
        return pbest

    def testIncreasePoints(self, start, stop, step=1, refrun='000'):
        print 'value(s) to be found: ', self._dtr._td.getParams(refrun)
        print '##### %i points in interpolation ####'%(len(
            self._usedpoints))
        for pt in self._usedpoints:
            print 'start points: ',pt.values()[0], 'pbest = ',self.doFit(
                    pt.values()[0], refrun)
        for i in xrange(start, stop, step):
            self.addRuns(step)
            print '##### %i points in interpolation ####'%(len(
                self._usedpoints))
            for pt in self._usedpoints:
                print 'start points: ',pt.values()[0], 'pbest = ',self.doFit(
                        pt.values()[0], refrun)


#print 'opening pickle'
#afile = open('td','r')
#td = pickle.load(afile)
#afile.close()

#ds = Distributor(td)

## usage example
#ft = FitTester(ds, ds._obs[0], ds._mcsets[0])
#ft.printChiq(0, 20, 100)
#pylab.show()

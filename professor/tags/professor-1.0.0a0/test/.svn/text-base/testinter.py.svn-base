"""testinter.py

contains:
Class GenDataBase
Allows to run interpolation tests with fake distributions for varying number
of MC runs and dimensions. Builds PointGenerators and FakeDistributions.
Configuration key is 'testinter'.

filesystem layout::
    /basedir/${ydistribution}/${dim}D/${mcruns}MC.dat

example::
    /tmp/paraboloid/1D/4MC.dat
                      /5MC.dat
                      ...
                   /2D/7MC.dat
                      /8MC.dat
                      ...
                   ...

previous data will be overwritten!
"""

import os
import threading
import numpy

from professor.tools.config import Config
from professor.tools.decorators import virtualmethod
from professor.test import buildSimplePG, dists
from professor.interpolation.interpolation import QuadraticInterpolation


logger = Config().initModule('testinter',
        { 'logfiles' : '-'                      # change
        , 'loglevel' : 'debug'
        , 'start dim': '1'
        , 'stop dim' : '2'                      # change
        # '-1' to start with the minimal needed number of mc runs
        , 'mc run min' : '-1'
        , 'add mc runs' : '5'
        , 'mc run step' : '2'
        , 'basedir' : '/tmp'                     # change
        , 'y distribution' : 'twominima'
        # the maximal relative error
        , 'relative error' : '.05'
        })

class GenDataBase(object):
    """Base class for data generation on a per dimension base.

    Runs the code in runPerDim for configured dimension values.
    """
    def __init__(self):
        self.workdir = os.path.join(self._getopt('basedir'),
                                    self._getopt('y distribution'))
        self.mindim = self._getopt('start dim', int)
        self.maxdim = self._getopt('stop dim', int)

        self.addmc = self._getopt('add mc runs', int)
        self.mcstep = self._getopt('mc run step', int)
        self.mcmin = self._getopt('mc run min', int)

        self.setFakeDistFactory()

        logger.debug('creating work directory: %s'%(self.workdir))
        try:
            os.mkdir(self.workdir)
        except OSError, e:
            logger.warning("Could not create working directory '%s': %s"%(
                           self.workdir, e))

    def setFakeDistFactory(self):
        ydistname = self._getopt('y distribution').lower()
        maxrelerr= self._getopt('relative error', float)
        # shortcut for function call
        nrand = numpy.random.rand
        if ydistname == 'paraboloid':
            # use dim*0.5*0.5 to estimate the maximal y value of the
            # paraboloid
            def h(dim):
                return dists.FakeDistribution('fake obs', (0., 1.),
                        dists.Paraboloid(nrand(dim)),
                        dists.AbsoluteGaussianError( .25 * dim * maxrelerr))

        elif ydistname == 'twominima':
            # multiply the linscale factors, so that they remain small for
            # higher dimensions
            #
            # use dim*0.5*0.5 * dim*0.5*0.5 to estimate the maximal y value
            # of the two minima distribution
            def h(dim):
                return dists.FakeDistribution('fake obs', (0., 1.),
                            dists.TwoMinima(
                                    min1 = nrand(dim),
                                    min2 = nrand(dim),
                                    linscale = (nrand(dim)
                                                *1.e-4*.09**(dim-1.)/dim)
                                    ),
                            dists.AbsoluteGaussianError(
                                    .0625 * dim**2 * maxrelerr)
                            )

        elif ydistname == 'quadratic':
            def h(dim):
                quaddist = dists.Quadratic(nrand(dim, dim)*2. - 1.,
                                     nrand(dim)*2. - 1.,
                                     nrand(1)[0]*2. - 1.)
                # estimate the maximal y value
                pg = buildSimplePG(dim)
                ymax = 0.
                for pp in pg(100):
                    ymax = max(ymax, abs(quaddist(pp.getScaled())))
                ymax *= 1.5
                logger.info("Estimated maximal y value for quadratic function: %e ." % ymax)

                return dists.FakeDistribution('fake obs', (0., 1.), quaddist,
                            dists.AbsoluteGaussianError(maxrelerr*ymax))

        elif ydistname == 'cubic':
            def h(dim):
                cubicdist = dists.Cubic(nrand(dim, dim)*2. - 1.,
                                        nrand(dim)*2. - 1.,
                                        nrand(dim, dim)*2. -1.,
                                        nrand(dim)*2. - 1.,
                                        nrand(1)[0]*2. - 1.)
                # estimate the maximal y value
                pg = buildSimplePG(dim)
                ymax = 0.
                for pp in pg(100):
                    ymax = max(ymax, abs(cubicdist(pp.getScaled())))
                ymax *= 1.5
                logger.info("Estimated maximal y value for cubic function: %e ." % ymax)

                return dists.FakeDistribution('fake obs', (0., 1.), cubicdist,
                                              dists.AbsoluteGaussianError(maxrelerr*ymax))

        else:
            logger.error("bad config value 'y distribution': %s"%(ydistname))
        self.getFD = h

    def _getopt(self, opt, conv=None):
        return Config().getOption('testinter', opt, conv)

    def getDimDir(self, dim):
        return os.path.join(self.workdir, '%sD'%(dim))

    def makeDimDir(self, dim):
        logger.debug('creating dim directory: %s'%(self.workdir))
        try:
            path = self.getDimDir(dim)
            os.mkdir(path)
        except OSError, e:
            logger.warning("Could not create dim directory '%s': %s"%(
                           path, e))
        return path

    def getSaveFile(self, dim, mc, add=None):
        if add is None:
            filename = "%iMC.dat"%(mc)
        else:
            filename = "%iMC_%s.dat"%(mc, add)

        logger.debug("Opening save file '%s'"%(filename))

        path = os.path.join(self.getDimDir(dim), filename)
        return open(path, 'w')

    def startOneThread(self, dim, mc, target, args, add=None):
        if add is None:
            name = "%sD_%sMC"%(dim, mc)
        else:
            name = "%sD_%sMC_%s"%(dim, mc, add)
        th = threading.Thread(name=name, target=target, args=args)
        th.setDaemon(False)
        th.start()
        logger.info("started thread '%s'"%(name))

    def run(self):
        print self
        for dim in xrange(self.mindim, self.maxdim+1):
            self.makeDimDir(dim)
            self.runPerDim(dim)
        logger.info("Waiting for threads to finish...")

    @virtualmethod
    def runPerDim(self, dim):
        pass


def corners(dim):
    """Generator for the corners of a hypercube.

    Used to test the error estimates in GenDataBase.setFakeDiskFactory.

    usage::
    >>> for c in corners(3):
    >>>     print c
    [...]

    @param dim: dimension of the hypercube
    """
    if dim > 1:
        for x in (0., 1.):
            t = numpy.zeros(dim)
            t[0] = x
            for c in corners(dim-1):
                t[1:] = c
                yield t
    else:
        for x in (0., 1.):
            yield x*numpy.ones(1)


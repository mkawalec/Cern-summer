#!/usr/bin/env python2.5
"""genpulldata.py

Generates pull data for different dimensions and MC runs.

usage::
    genpulldata.py CONFIGFILE
"""

import sys
import numpy

from professor.tools.config import Config
from professor.tools.parameter import ppFromList
from professor.test.testinter import GenDataBase
from professor.test import buildSimplePG, generator
from professor.interpolation import getInterpolationClass, BinDistribution

logger = Config().initModule('genpulldata',
        { 'logfiles' : '-'
        , 'loglevel' : 'debug'
        # '-1' to use the anchor points
        , 'number of test points' : '10'
        , 'number of pull sets' : '4'
        , 'use error for comparison' : 'fake dist'
        })

class GenPullData(GenDataBase):
    def __init__(self):
        super(GenPullData, self).__init__()
        self.notestp = Config().getOption('genpulldata',
                'number of test points', int)
        self.nopullsets = Config().getOption('genpulldata',
                'number of pull sets', int)
        self.useerror = Config().getOption('genpulldata',
                'use error for comparison')

    def MCThread(self, dim, mc, scaler, testp):
        """
        @param testp: list with the points where the pulls are calculated.
            Or None, then the anchor points are used.
        """
        for pullset in xrange(self.nopullsets):
            pullset += 1
            fd = self.getFD(dim)
            savefile = self.getSaveFile(dim, mc, pullset)
            savefile.write('# pulls\n'
                           '# used fake distribution: %s\n'
                           '# line layout:\n'
                           '# pull value\n'
                           '# ...\n'%(fd))
            logger.info("Starting pull calculation number %i for %i dim,"
                        " %i MC runs and fake distribution %s" %
                        (pullset, dim, mc, fd))

            pg = generator.PointGenerator(scaler)
            fd.setError(True)

            bd = BinDistribution(scaler.getKeys(), fd.getObs(),
                                 fd.getBinrange())
            [bd.addRun(p, fd(p)) for p in pg(mc)]
            ip = getInterpolationClass()(bd)
            ip.setCenter(ppFromList(.5 * numpy.ones(scaler.dim()), scaler,
                                    scaled=True))
            ip.interpolate()

            if testp is None:
                testp = [p for p,b in bd]

            for pull in fd.pullCompare(ip, testp, error=self.useerror):
                savefile.write("%e\n" % pull)

            savefile.close()
            logger.info("Finished pull calculation number %i for %i dim,"
                        " %i MC runs and fake distribution %s"%(
                        pullset, dim, mc, fd))

    def runPerDim(self, dim):
        pg = buildSimplePG(dim)

        if self.notestp == -1:
            testp = None
        else:
            testp = [tp for tp in pg(self.notestp)]

        if self.mcmin == -1:
            minmc = getInterpolationClass().minNrOfRuns(dim)
        else:
            minmc = self.mcmin

        for mc in xrange(minmc, minmc + self.addmc + 1, self.mcstep):
            self.startOneThread(dim, mc, self.MCThread,
                                (dim, mc, pg.getScaler(), testp))


if __name__ == '__main__':
    try:
        Config(sys.argv[1])
    except IndexError, e:
        logger.error(__doc__)
        logger.error("Need config file on command line!")
        sys.exit(1)

    GenPullData().run()

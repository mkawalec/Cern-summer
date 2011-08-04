#!/usr/bin/env python2.5
"""gencenterdata.py

Generates chi^2 vs. interpolation center  data.

usage::
    gencenterdata.py CONFIGFILE
"""

import sys
import numpy

from professor.tools.parameter import ppFromList
from professor.interpolation import getInterpolationClass, BinDistribution
from professor.test.testinter import GenDataBase, Config
from professor.test import buildSimplePG, generator

logger = Config().initModule('gencenterdata',
        { 'logfiles' : '-'
        , 'loglevel' : 'debug'
        , 'number of test points' : '10'
        , 'number of centers' : '100'
        , 'number of interpolations' : '10'
        , 'use error for comparison' : 'fake dist'
        })

class GenCenterData(GenDataBase):
    def __init__(self):
        super(GenCenterData, self).__init__()
        self.notestp = Config().getOption('gencenterdata',
                                          'number of test points', int)
        self.nocenters = Config().getOption('gencenterdata',
                                            'number of centers', int)
        self.noint = Config().getOption('gencenterdata',
                                        'number of interpolations', int)
        self.useerror = Config().getOption('gencenterdata',
                                           'use error for comparison')

    def MCThread(self, dim, mc, scaler, testp):
        logger.info("Starting %i different interpolation with %i different"
                    " centers each."%(self.noint, self.nocenters))
        for add in xrange(1, self.noint + 1):
            fd = self.getFD(dim)
            savefile = self.getSaveFile(dim, mc, add)
            savefile.write("# chi2-vs-center of interpolation\n"
                           "# used fake distribution: %s\n"
                           "# number of test points for chi2 calc: %i\n"
                           "# line layout:\n"
                           "# chi2 ; center point\n"%(fd, self.notestp))


            pg = generator.PointGenerator(scaler)
            # build and fill the bin distribution
            fd.setError(True)
            bd = BinDistribution(scaler.getKeys(), fd.getObs(),
                                 fd.getBinrange())
            [bd.addRun(p, fd(p)) for p in pg(mc)]

            def calcandsave(center):
                ip = getInterpolationClass()(bd)
                ip.setCenter(center)
                ip.interpolate()
                chi2 = fd.chi2Compare(ip, testp, error=self.useerror)
                savefile.write("%e ; " % chi2
                   + " ".join("%e" % scval for scval in center.getScaled())
                   + '\n')

            # calculate the chi2 value for the center of the hyper cube
            calcandsave(ppFromList(.5*numpy.ones(scaler.dim()), scaler, True))
            for c in pg(self.nocenters):
                calcandsave(c)
            savefile.close()

        logger.info("Finished %i different interpolation with %i different"
                    " centers each."%(self.noint, self.nocenters))



    def runPerDim(self, dim):
        pg = buildSimplePG(dim)
        # test points for chi2 calculation
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

    GenCenterData().run()

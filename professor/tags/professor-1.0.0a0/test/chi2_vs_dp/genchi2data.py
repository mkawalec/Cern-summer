#!/usr/bin/env python2.5

"""genchi2data.py

Generates data which allow to compare chi^2 values with the distribution of
the anchor points used for interpolation.

usage::
    genchi2data.py CONFIGFILE
"""

import sys
import numpy

from professor.tools.config import Config
from professor.tools.parameter import ppFromList
from professor.test.testinter import GenDataBase
from professor.test import buildSimplePG, generator
from professor.interpolation import getInterpolationClass, BinDistribution

logger = Config().initModule('genchi2data',
        { 'logfiles' : '-'                      # change
        , 'loglevel' : 'debug'
        , 'number of test points' : '10'
        , 'number of interpolations' : '100'
        , 'use error for comparison' : 'fake dist'
        })

class GenChi2Data(GenDataBase):
    def __init__(self):
        super(GenChi2Data, self).__init__()
        self.notestp = Config().getOption('genchi2data',
                'number of test points', int)
        self.noint = Config().getOption('genchi2data',
                'number of interpolations', int)
        self.useerror = Config().getOption('genchi2data',
                'use error for comparison')

    def MCThread(self, dim, mc, scaler, testp):
        fd = self.getFD(dim)
        savefile = self.getSaveFile(dim, mc)
        savefile.write(('# chi-vs-dp\n'
                        '# used fake distribution: %s\n'
                        '# number of test points: %i\n'
                        '# line layout:\n'
                        '# chi2 ; point1 ; point2 ; ... ; point%i\n')%(
                            fd, self.notestp, mc))

        logger.info('Starting %i interpolations for %i MC runs and fake'
                ' distribution %s'%(self.noint, mc, fd))
        pg = generator.PointGenerator(scaler)
        for i in xrange(self.noint):
            fd.setError(True)
            # build and fill the bin distribution
            bd = BinDistribution(scaler.getKeys(), fd.getObs(),
                                 fd.getBinrange())
            [bd.addRun(p, fd(p)) for p in pg(mc)]

            ip = getInterpolationClass()(bd)
            ip.setCenter(ppFromList(.5*numpy.ones(scaler.dim()), scaler,
                                    scaled=True))
            ip.interpolate()
            chi2 = fd.chi2Compare(ip, testp, error=self.useerror)
            line = "%e" % chi2
            for p, unusedbin in bd:
                line += " ; "
                line += " ".join(["%e" % scval for scval in p.getScaled()])
            savefile.write(line + "\n")
        savefile.close()
        logger.info('Finished %i interpolations for %i MC runs and fake'
                ' distribution %s'%(self.noint, mc, fd))

    def runPerDim(self, dim):
        pg = buildSimplePG(dim)
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
        print __doc__
        print "Need config file on command line!"
        sys.exit(1)

    GenChi2Data().run()

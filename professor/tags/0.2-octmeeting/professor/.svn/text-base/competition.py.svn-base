#!/usr/bin/python
# vim:fileencoding=utf-8
"""competition.py

"""

from professor.rivetreader import getTuningData
from professor.permut import xuniqueCombinations
from professor.interpolation.analytic_interpolation import BinDistribution
import professor.histo as histo

import numpy, pylab
from scipy import optimize

class Competition:
    def __init__(self, refdir, outdir):
        self._td = getTuningData(refdir, outdir)
        self._td.isValid()
        # store the results of all minimizations in a dict:
        # { list of used run numbers: result }
        # in bad results 
        self._results = []

        self._badresults = []

    def getTuningData(self):
        return self._td

    def calculateResult(self, runnums):
        """
        Resulting parameter set is denormalized!
        """
        data_list = self.getTuningData().buildBinDistList(runnums)
        p0 = .5 * numpy.ones(self.getTuningData().numberOfParams())

        def chi2(p):
            r = .0
            for ref, bd in data_list:
                r += (ref.getYVal() - bd.calcValue(p))**2
            return r

        guess = optimize.fmin_powell(chi2, p0)
        # a bug in optimize.fmin_powell
        # returns 0-dim array!
        if guess.shape == ():
            print "Found bug?"
            guess = numpy.array([guess+0])
        # print '   p0 = %s --> %s, '%(p0, guess)
        # print "%s vs %s"%(numpy.ones(1), guess)
        # print "%s vs %s"%(type(numpy.ones(1)), type(guess))
        # print "%s vs %s"%(numpy.ones(1).shape, guess.shape)

        # denormalize result
        pmins, pmaxs = self.getTuningData().getParameterBoundaries(runnums)
        r = []
        for v, min_, max_ in zip(guess, pmins, pmaxs):
            r.append(v*(max_ - min_) + min_)

        print 'min: %s  max: %s'%(pmins, pmaxs)
        print 'normalized: %s  denormalized: %s'%(guess, r)

        return r

    def guess(self, runnums):
        print "guessing %s ..."%(runnums)
        guess = self.calculateResult(runnums)
        if self.goodRunnums(runnums):
            self._results.append( (runnums, guess) )
            print "   -> %s"%(guess)
        else:
            self._badresults.append( (runnums, guess) )
            print "   -> %s bad run numbers!"%(guess)
        return guess

    def goodRunnums(self, runnums):
        mindist = 1./(len(runnums) + 1.)**2
        pmins, pmaxs = self.getTuningData().getParameterBoundaries(runnums)

        for i, n1 in enumerate(runnums):
            p1 = histo.normalizeParameterDict(self.getTuningData().getParams(n1), pmins, pmaxs)
            p1 = numpy.array(p1)

            for n2 in runnums[i+1:]:
                # print runnums, n1, n2
                p2 = histo.normalizeParameterDict(self.getTuningData().getParams(n2), pmins, pmaxs)
                p2 = numpy.array(p2)
                dp = abs(p1 - p2)
                if dp.min() <= mindist:
                    print "Entry of %s -%s = %s <= %f!"%(p1, p2, dp, mindist)
                    return False


        return True


    def runAllGuesses(self, minnrofpoints=None, maxnrofpoints=None, maxiter=None):
        if minnrofpoints == None:
            minnrofpoints = BinDistribution.s_requiredRuns(
                    self.getTuningData().numberOfParams())

        if maxnrofpoints == None:
            maxnrofpoints = minnrofpoints

        print minnrofpoints, '...', maxnrofpoints

        i = 0
        for n in xrange(minnrofpoints, maxnrofpoints + 1):
            for runnums in xuniqueCombinations(
                    self.getTuningData().getRunNums(), n):
                # t = ['%3i'%i for i in runnums]
                self.guess(runnums)
                i += 1
                if maxiter != None and i >= maxiter:
                    print "reached maxiter(%i)!"%(maxiter)
                    print "   returning"
                    return

    def plotEachParameter(self):
        parameternames = self.getTuningData().paramsNames()
        plot_data = {}
        for name in parameternames:
            plot_data[name] = {'x':[], 'y':[]}

        # fill plot data
        # for runnums, guessed in self._results().iteritems():
        for runnums, guessed in self._results:
            x = len(runnums)
            print guessed
            for i, name in enumerate(parameternames):
                print '   ', i, name
                plot_data[name]['x'].append(x)
                plot_data[name]['y'].append(guessed[i])

        i = 1
        for name, data in plot_data.iteritems():
            sp = pylab.subplot(len(parameternames), 1, i)
            sp.plot(data['x'], data['y'], '.')
            print data['x']
            print data['y']
            sp.set_title(name)
            sp.set_xlabel('# of used runs')
            sp.set_ylabel('result')
            i += 1
        pylab.show()

class CompetitionFileWriter(Competition):
    def __init__(self, refdir, outdir, savepath):
        Competition.__init__(self, refdir, outdir)
        self._refdir = refdir
        self._outdir = outdir
        self._savepath = savepath
        self._goodfile = None
        self._badfile = None
        self._separator = ','

    def setSeparator(self, sep):
        if len(sep) != 1:
            raise ValueError('sep must be of length 1!')
        self._separator = sep

    def getSeparator(self):
        return self._separator

    def guess(self, runnums):
        guess = self.calculateResult(runnums)
        line = ''
        for num in runnums:
            line += '%s%s'%(num, self.getSeparator())
        line = line[:-1] + '\t%i\t'%(len(runnums))
        for v in guess:
            line += '%f\t'%(v)
        self.writeLine(line[:-1], self.goodRunnums(runnums))

    def writeLine(self, line, good):
        if good:
            self._goodfile.write(line + '\n')
        else:
            self._badfile.write(line + '\n')

    def openFile(self):
        if self._goodfile != None or self._badfile != None:
            raise StandardError('save file already opened!')

        pmins, pmaxs = self.getTuningData().getParameterBoundaries()
        pnames = self.getTuningData().paramsNames()

        self._goodfile = open(self._savepath, 'w')
        self._badfile = open(self._savepath + '_bad', 'w')

        for isgood in (True, False):

            self.writeLine('# used directories:', isgood)
            self.writeLine('#   refdir: %s'%(self._refdir), isgood)
            self.writeLine('#   outdir: %s'%(self._outdir), isgood)
            self.writeLine('#', isgood)

            self.writeLine('#           \tname\tmin\tmax', isgood)
            for name, min_, max_ in zip(pnames, pmins, pmaxs):
                self.writeLine('# parameter:\t%s\t%f\t%f'%(name, min_, max_), isgood)
            self.writeLine('#', isgood)

            l = '# used runnums\t#runs\t'
            for name in self.getTuningData().paramsNames():
                l += '%s\t'%(name)
            self.writeLine(l[:-1], isgood)

    def closeFile(self):
        self._goodfile.close()
        self._badfile.close()


if __name__ == '__main__':
    cp = Competition('/home/eike/uni/professor/trunk/testdata/2d/testref1a/',
                     '/home/eike/uni/professor/trunk/testdata/2d/out')
    cp.runAllGuesses(minnrofpoints=19, maxnrofpoints=20)
    # cp.plotEachParameter()


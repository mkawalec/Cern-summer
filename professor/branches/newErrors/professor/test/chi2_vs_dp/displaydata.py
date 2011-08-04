#!/usr/bin/env python2.5
"""displaydata.py

usage::
    displaydata.py DATAFILE

    Then use the opened IPython shell. Data is stored in an OneSet instance
    named os. Example:
    >>> x, y, z, zerr = os.get3Ddata(10, 100, dpProjMin, True, 10000)
    >>> plot(x, y, z)
    >>> pylab.show()
"""

import itertools
import numpy
import sys, os, re
import pylab, matplotlib.cm


class OneSet(object):
    def __init__(self, path):
        self._p = path

        # a 1D array with the chi2/ndf values of the interpolations
        self.chi2s = None
        self._del = ' ; '
        self.notestp = None

        # a 3D array with the used parameter values
        # axes: 1. interpolation index
        #       2. MC run number
        #       3. dimension
        # so:
        # >>> self._points[3:4:2]
        # should return the value of the 3. component of the 5. MC run point
        # of the 4. interpolation run (counting started with 1)
        self.points = None
        self.__parseFile()

        self.dims = None
        self.nomc = None
        try:
            regexp = re.compile(r'(?P<DIM>[0-9]*)D/(?P<MC>[0-9]*)MC')
            d = regexp.search(os.path.abspath(self._p)).groupdict()
            self.dims = d['DIM']
            self.nomc = d['MC']
        except StandardError, e:
            print e
            print 'continuing...'
        # norm the chi2 to the ndf, i.e. the number of test points
        self.chi2s = self.chi2s/self.notestp

    def __parseFile(self):
        t = []
        f = open(self._p, 'r')
        for line in f:
            if line.startswith('#'):
                # parse # of test points
                if line.startswith('# number of test points:'):
                    self.notestp = int(line.split()[-1])
                continue
            t.append(float(line.split(' ; ')[0]))
        self.chi2s = numpy.array(t)
        noint = len(self.chi2s)
        # examine last line to get the dimension and the # of mc runs
        nomc = len(line.split(self._del)) - 1
        t = line.split(self._del)[-1]
        dim = len(t.split())
        del t

        self.points = -1. * numpy.ones((noint, nomc, dim))
        f.seek(0)
        inti = 0
        for line in f:
            if line.startswith('#'):
                continue
            for mci, pstring in enumerate(line.split(self._del)[1:]):
                params = numpy.array([float(t) for t in pstring.split()])
                self.points[inti, mci] = params
            inti += 1

    def get3Ddata(self, dpbins, chi2bins, dpanalysis, maxchi2=None,
            logchi2=False):
        """Fill the chi2/ndf values in a 2D histogram.

        Normed histograms are calculated so that the projection on the dp
        axis gives 1 for all dp bins (or 0 if there is not a single entry).
        This is to take into account, that small dp values occure more often
        than great ones.

        @param dpbins: # of dp bins
        @param chi2bins: # of chi2 bins
        @param dpanalysis: function returning a list of dp values. Gets self
            as only argument.
        @param maxchi2: cut for the chi2 values, e.g. 10000
        @returns: returns tuple of numpy.ndarrays:
            chi2 bin edges, dp bin edges, histogram entries,
            normed histogram entries, normed histogram errors
        """
        dps = dpanalysis(self)
        assert dps.shape == self.chi2s.shape

        minchi2 = min(self.chi2s)
        ext_maxchi2 = True
        if maxchi2 is None:
            maxchi2 = max(self.chi2s)
            ext_maxchi2 = False

        if logchi2:
            logminchi2 = numpy.floor(numpy.log10(minchi2))
            logmaxchi2 = numpy.floor(numpy.log10(maxchi2)) + 1

            logchi2borders, logchi2step = numpy.linspace(logminchi2,
                    logmaxchi2, chi2bins + 1, endpoint=True, retstep=True)
            chi2borders = 10**logchi2borders
            # print logchi2borders, logchi2step
            # print chi2borders
        else:
            chi2borders, chi2step = numpy.linspace(minchi2, maxchi2,
                    chi2bins + 1, endpoint=True, retstep=True)

        mindp = min(dps)
        maxdp = max(dps)
        dpborders, dpstep = numpy.linspace(mindp, maxdp, dpbins + 1,
                endpoint=True, retstep=True)

        # Build function to determine the chi2 index for 
        # log scale and lin scale
        if logchi2:
            chi2Index = lambda chi2: int((numpy.log10(chi2)-logminchi2)/logchi2step)
            # for testing:
            def chi2Index_TESTING(chi2):
                ind = int((numpy.log10(chi2)-logminchi2)/logchi2step)
                # print ind, repr(chi2), repr(chi2borders[ind])
                # print chi2borders[ind] - chi2
                assert chi2borders[ind] <= chi2
                try:
                    assert chi2 <= chi2borders[ind+1]
                except IndexError:
                    pass
                return ind
        else:
            chi2Index = lambda chi2: int((chi2-minchi2)/chi2step)

        z = numpy.zeros((dpbins, chi2bins))
        # TODO make this faster with numpy, ufuncs:
        # i_dps = int((dps-mindp)/dpstep)

        # for chi2, dp in itertools.izip(self.chi2s, dps):
        # itertools.izip is not faster
        for chi2, dp in zip(self.chi2s, dps):
            # print chi2, dp
            # calculate indices
            i_chi2 = chi2Index(chi2)
            i_dp = int((dp-mindp)/dpstep)
            # take care of max values
            # don't put them in the overflow bin, i.e. neglect them
            if i_chi2 == chi2bins and chi2 == maxchi2:
                i_chi2 = chi2bins - 1
                print "found max chi2"
            elif chi2 > maxchi2:
                # print "found chi2(%f) > chi2_max(%f) ... omitting"%(chi2,
                        # maxchi2)
                continue

            if i_dp == dpbins and dp == maxdp:
                i_dp = dpbins - 1
                print "found max dp"

            z[i_dp, i_chi2] += 1

        if ext_maxchi2:
            print "external chi^2_max:"
            print ("  dropped %i chi^2 values;"
                   " left %i chi^2 values in histogramm")%(
                           len(self.chi2s) - z.sum(), z.sum())

        # the normed values
        # initiated with obviously wrong values
        zn = numpy.ones(z.shape)
        zerrn = numpy.ones(z.shape)

        sums = z.sum(axis=1)
        for i, s in enumerate(sums):
                if s == 0:
                    zn[i] = 0.
                    zerrn[i] = 0.
                else:
                    zn[i] = z[i]/s
                    # Poissonian error for the bin content, normed
                    zerrn[i] = numpy.sqrt(z[i])/s

        return dpborders, chi2borders, z, zn, zerrn


def distCart(p1, p2):
    return numpy.sqrt(numpy.inner(p1 - p2, p1 - p2))

def distProj(p1, p2):
    return abs(p1 - p2)

def dpCartAvg(os):
    """Return an array with the average cartesian distance for each interpolation run."""
    points = os.points
    noint, nomc, dim = points.shape

    ret = -1. * numpy.ones(noint)
    for inti in xrange(noint):
        dp_cumulative = .0
        for p1 in points[inti]:
            for p2 in points[inti]:
                dp_cumulative += distCart(p1, p2)

        # store the average distance:
        # 1/(# MC) * sum_{i=0}^{# MC}  1/(# MC -1) * sum_{j!=i} |p_i - p_j|
        ret[inti] = dp_cumulative/(nomc*(nomc-1))
    return ret

def dpCartMin(os):
    """Return an array with the minimalcartesian distance for each interpolation run."""
    points = os.points
    noint, nomc, dim = points.shape

    ret = -1. * numpy.ones(noint)
    for inti in xrange(noint):
        dp = 1.e18

        for mci, p1 in enumerate(points[inti]):
            for p2 in points[inti, mci+1:]:
                dp = min(dp, distCart(p1, p2))
        ret[inti] = dp

    return ret

def dpProjAvg(os):
    """Return an array with the average projection distance for each
    interpolation run.
    """
    points = os.points
    noint, nomc, dim = points.shape

    ret = -1. * numpy.ones(noint)
    for inti in xrange(noint):
        dp_cumulative = numpy.zeros(dim)
        for p1 in points[inti]:
            for p2 in points[inti]:
                dp_cumulative += distProj(p1, p2)
        ret[inti] = dp_cumulative.sum()/(nomc*(nomc-1)*dim)
    return ret

def dpProjMin(os):
    """Return an array with the minimal projection distance for each
    interpolation run."""
    points = os.points
    noint, nomc, dim = points.shape

    ret = -1. * numpy.ones(noint)
    for inti in xrange(noint):
        dp = 1.e18
        for mci, p1 in enumerate(points[inti]):
            for p2 in points[inti,mci+1:]:
                dp = min(dp, min(distProj(p1, p2)))
        ret[inti] = dp
    return ret


dpanalyses = (('min dp_proj', dpProjMin),
               ('avg dp_proj', dpProjAvg),
               ('min dp_cart', dpCartMin),
               ('avg dp_cart', dpCartAvg))


def createBigFigure(oset, dpbins, chi2bins, chi2cut=None, logchi2=False):
    """Returns (figure, possible file name)."""
    title = '%s D; %s MC'%(oset.dims, oset.nomc)
    fname = '%sD_%sMC'%(oset.dims, oset.nomc)
    if chi2cut is not None:
        title += '; chi^2 cut = %s; # entries %i'%(chi2cut, noentries)
        fname += '_cut%s'%(chi2cut)

    fig = pylab.figure()
    # TODO: adjust wspace 
    # put in batchplot.py using matplotlib.rc

    nrows = len(dpanalyses)
    ncols = 3

    for i, (name, meth) in enumerate(dpanalyses):
        x, y, zunnormed, znormed, zerrnormed = oset.get3Ddata(dpbins,
                                    chi2bins, meth, chi2cut,
                                    logchi2=logchi2)
        X, Y = pylab.meshgrid(x, y)
        sp = fig.add_subplot(nrows, ncols, ncols*i + 1)
        coll = sp.pcolor(X, Y, znormed.transpose(), cmap=matplotlib.cm.hot)
        sp.set_xlabel(name)
        sp.set_ylabel('chi2/ndf')
        if logchi2:
            sp.set_yscale('log')
        fig.colorbar(coll).set_label('normed entries')

        sp = fig.add_subplot(nrows, ncols, ncols*i + 2)
        coll = sp.pcolor(X, Y, zerrnormed.transpose(), cmap=matplotlib.cm.gray_r)
        sp.set_xlabel(name)
        sp.set_ylabel('chi2/ndf')
        if logchi2:
            sp.set_yscale('log')
        fig.colorbar(coll).set_label('normed error')

        sp = fig.add_subplot(nrows, ncols, ncols*i + 3)
        coll = sp.pcolor(X, Y, zunnormed.transpose(), cmap=matplotlib.cm.autumn)
        sp.set_xlabel(name)
        sp.set_ylabel('chi2/ndf')
        if logchi2:
            sp.set_yscale('log')
        fig.colorbar(coll).set_label('unnormed entries')

        print 'finished', name

    fig.text(.5, .98, title, ha='center', va='top')
    return fig, fname

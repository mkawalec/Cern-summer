#!/usr/bin/python
# vim:fileencoding=utf-8
"""envelope.py\n
    this is for plotting an envelope of all datapoints in several histograms of
    equal and equidistant binning.
"""
import numpy, matplotlib
from pylab import *
# matplotlib.rc('text', usetex=True)

class EnvelopeError(StandardError):
    pass

class Envelope:
    """ This a class that provides Envelope-Plotting of histogramms in AIDA-file-format.
    """

    def __init__(self, histdata, show=True, mc =True):
        """ @param histdata: histdata is considered to be a
            getHistolist-instance from histo.py
        """
        self._obs = histdata[1]      # observable...
        self._histdata = numpy.array(histdata[0]) # list, contains histos
        self._mc = mc
        self.plotAll()
        if show:
            self.Show()

    def plotAll(self):
        self.plotEnvelope(self.getTube())
        self.plotErrorbars(self.getAll(), self.getSmallestStep())
        self.plotPolygon(self.getAll(), self.getSmallestStep())


    def getObservable(self):
        """ returns a string of the observables name
        """
        return self._obs

    def getXRange(self):
        """ returns the 'worlds'-xrange of all histogramms as a bituple
        """
        Xmin = []
        Xmax = []
        for i in xrange(0, len(self._histdata), 1):
            for j in self._histdata[i].getBins():
                Xmin.append(min(j.getXRange()))
                Xmax.append(max(j.getXRange()))
        return (min(Xmin), max(Xmax))

    def getSmallestStep(self):
        """ considered to return the binwidth.
            this is also used to catch non constant binning.
        """
        Xsteps = []
        for i in xrange(0, len(self._histdata), 1):
            for j in self._histdata[i].getBins():
                Xsteps.append(j.getXRange()[1] - j.getXRange()[0])
        #if not min(Xsteps) == max(Xsteps):
        #    print 'min:', min(Xsteps), 'max:', max(Xsteps), 'all:', Xsteps
        #    raise EnvelopeError('non equidistant binnning!')
        else:
            return min(Xsteps)

    def getAll(self):
        """ reads all histogram-data into array.\n
            returns array of i arrays of histos of j bins:\n
            every bin: binedges|YValue|YError(might be None)|binfocus(might be
            None)\n
            btw, nonetype appears to be no problem to errorbarplots
        """
        self._alldata = []
        # over all histos
        for i in xrange(0, len(self._histdata), 1):
            temp =[]
            # over all bins
            for j in xrange(0,len(self._histdata[i].getBins()),1):
                temp.append( (self._histdata[i].getBins()[j].getXRange(),\
                        self._histdata[i].getBins()[j].getYVal(),\
                        self._histdata[i].getBins()[j].getYErr(),\
                        self._histdata[i].getBins()[j].getFocus())  )
            self._alldata.append(temp)
        return self._alldata

    def getTube(self):
        """ assuming equal binnning, this returns points of a closed polygon
            that wraps all datapoints, using both binedges, and can be used
            with the matplotlib.fill()-method.\n
            if bin is empty in all histograms, then the tube is filed with 0.
        """
        Ymin =[]
        Ymax =[]
        # append the min/max-YValues for all bins
        # iterate over 'worlds'-xrange-bins, using lower bin-edges
        #for i in numpy.arange(self.getXRange()[0], self.getXRange()[1], \
        #        self.getSmallestStep()):
        binrange = numpy.arange(self.getXRange()[0], self.getXRange()[1], self.getSmallestStep())
        if self._mc:
            if not (len(binrange) == len(self._histdata[0].getBins())):
                binrange = binrange[:len(self._histdata[0].getBins())]
        for i ,item in enumerate(binrange):
            temp = [] # called binwise, is filled with YValues, if histo
                      # has bin in worlds xrange
            # iterate over all 'histo-files'
            for j in xrange(0, len(self._histdata)):
                if not self._mc == True:
                    # iterate over all bins of the j'th histo
                    for k in xrange(0, len(self._histdata[j].getBins()) ):
                        # check if j'th histo has bin i
                        if self._histdata[j].getBins()[k].getXRange() == (i, i + self.getSmallestStep() ):
                            temp.append(self._histdata[j].getBins()[k].getYVal())  # *
                else:
                    temp.append(self._histdata[j].getBins()[i].getYVal())  # *
            # only in case i'th bin is empty in all histos[j].getYErr
            # print len(temp), max(temp), temp.index(max(temp)), i
            if len(temp) == 0: # empty bins     # *
                # temp.append(None) # nonetype
                # temp.append(0) # nonetype
                Ymax.append( ((item, item + self.getSmallestStep() ), 0. )) # *
                Ymin.append( ((item, item + self.getSmallestStep() ), 0. )) # *
            else:
                # append min/max datapoints
                Ymax.append( ((item, item + self.getSmallestStep() ), max(temp) ))
                Ymin.append( ((item, item + self.getSmallestStep() ), min(temp) ))
        # creating the polygon, 'clockwise' filling->starting with max-Yvalues
        tube = []
        for i in xrange(0, len(Ymax), 1):
            # if not (Ymax[i][1] is None): # see below...
            # if not (Ymax[i][1] == 0): # if nonetype is filled in tube above..
            tube.append((Ymax[i][0][0], Ymax[i][1]))
            tube.append((Ymax[i][0][1], Ymax[i][1]))

        # closing the polygon, filling tube with reversed minimum yvalues
        Ymin.reverse()
        for i in xrange(0, len(Ymin), 1):
            # if not (Ymin[i][1] is None): if you dont want empty bins to be
            # put in envelope
            # if not (Ymin[i][1] == 0): # same...
            tube.append((Ymin[i][0][1], Ymin[i][1]))
            tube.append((Ymin[i][0][0], Ymin[i][1]))
        return tube

    def plotEnvelope(self, tube):
        """ plot the Envelope using matplotlib.fill
            @param tube: list, that contains extremal bincontents,
                considered to be a L{getTube()}-object
        """
        TB = array(tube) # easier to handle
        fill(TB[:,0], TB[:,1], 'b', alpha = .05, label = 'Envelope')

    def plotErrorbars(self, data, step):
        """ add xy-errorbars for all bins; for plotting I use:\n
            x:        binfocus or center of bin if latter is None\n
            y:        Yvalue Bin.getYval()\n
            Yerr:     Bin.getYErr() or minimum length from focus to edge\n
            Xerr:     half the bin-width (half of step)\n
            @param data: list that contains all histograms, it is considered
                to be a L{getAll()}-object
            @param step: float, that gives the smallest binwidth found, it
                should be a L{getSmallestStep()}-object
        """
        for i in xrange(0, len(data)):
            for j in xrange(0, len(data[i])):
                # this is for determing the binfocus
                if not (data[i][j][3] is None):
                    errorbar(data[i][j][3],\
                            data[i][j][1], data[i][j][2],\
                            min([abs(data[i][j][0][0]-data[i][j][3]),\
                            abs(data[i][j][0][1]-data[i][j][3])]), capsize=3,\
                            barsabove=False, ls=' ', label='_nolegend_') \

                else:
                    errorbar(data[i][j][0][0] + .5*step,\
                            data[i][j][1], data[i][j][2], .5*step, capsize=3,\
                            barsabove=False, ls=' ', label='_nolegend_') \
                        # mid of bin, y, yerr, xerr==half bin width,options

    def plotPolygon(self, data, step, which='all', plotstyle=':'):
        """ plots a single or all datasets as polygons
            @param data: list that contains all histograms, it is considered
                to be a L{getAll()}-object
            @param which: integer in range of len(data), that toggles between
                printing all or a single polygon
            @param step: float, that gives the smallest binwidth found, it
                should be a L{getSmallestStep()}-object
            @param plotstyle: string, that can be any valid matplotlib-plot-
                option (*kwarg)
        """
        if which == 'all':
            start = 0
            stop = len(data)
        else:
            start = which
            stop = which + 1

        for i in xrange(start, stop):
            temp = []
            for j in xrange(0, len(data[i])):
                # this is for determing the binfocus
                if not (data[i][j][3] is None):
                    temp.append((data[i][j][3], data[i][j][1]))
                else:
                    temp.append((data[i][j][0][0] + .5*step, data[i][j][1]))
                X= array(temp)
            plot(X[:,0], X[:,1],plotstyle, label = 'Run '+str(self._histdata[i].getRunnr())) # x(bincenter), y,optns.

    def Show(self):
        """ show everything that was plotted before
        """
        legend()
        #xlim(self.getXRange()[0]-1.,self.getXRange()[1]+1.)
        #ylim(0)
        title('Observable: %s'%(self.getObservable()))
        # ylabel('\\Large \\#')
        xlabel('\\Large $\\mathrm{a.u.}$')
        figtext(.05,.5,'\\Large \\#', horizontalalignment='center',verticalalignment='center')
        show()


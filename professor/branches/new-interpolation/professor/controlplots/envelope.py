"""envelope.py\n
The Envelope class allows to generate envelope plots out of a TuningData object
also, the reference data is being plotted as well as the individual runs, the
latter as a dotted polygon
"""
import numpy, pylab
from professor.tools import translate
pylab.matplotlib.rc('text', usetex=True) # causes problems on some machines

class EnvelopeError(StandardError):
    pass

class Envelope:
    """ In this class all the methods are to be found needed for generating an
        envelope plot. For each envelope plot, representing Histos of a certain
        observable, a new Envelope object has to be created.

        By default, the Envelope plot will be of the first observable found in
        the TuningData object. This behavier can be altered by passing the
        Observables name or its position in the TuningData object to the
        constructor.
    """

    def __init__(self, td, observable=-1, plotwhat=(True, True, False),
            show=True, logscale=(False, False)):
        """ @param td: this is considered to be a TuningData object
            @param observable: this is to select one of the observables stored
            in the TuningData object to plot the envelope for. This can either
            be a string out of the list given by the
            TuningData.getMCHistoNames()-function or an integer representing
            the observables position in this list (this is good for envelope-
            plotting of all observables)
            @param show: here one can switch whether the result shall be
            shown or not
        """
        self._td = td
        self._logscale=logscale
        self._params = [i for i in self._td._params.values()[0].keys()]
        self._params.sort()
        if not observable==-1 and observable in self._td.getMCHistoNames():
            self._obs = observable
        elif type(observable)==int and int(observable) in xrange(len(
            self._td.getMCHistoNames())):
            self._obs = self._td.getMCHistoNames()[int(observable)]
        else:
            print 'invalid input using first Observable found'
            self._obs = self._td.getMCHistoNames()[0]
        print 'now processing %s'%self._obs
        self._histdata = [run for run in self._td.getMCHistos(
            self._obs).values()]

        if True in plotwhat:
            fig = pylab.figure(facecolor='w')
            self._sp = fig.add_subplot(1, 1, 1)
            self.plotAll(plotwhat)
            if show:
                self.Show()
        else:
            print 'nothing was chosen to plot'
        # to ease log axes selection

        #if logscale[0]:
        #    self._sp.set_xscale('log')
        #if logscale[1]:
        #    self._sp.set_yscale('log')

    def getRange(self, bins):
        """ returns the minimum and maximum of the bins xranges of one histo
            @param bins: this is a list of Bin objects given by Histo.getBins()
        """
        temp = [bin.getXRange() for bin in bins]
        return temp, min(temp), max(temp)

    def getTotalXRange(self):
        """ returns the minimum and the maximum of the bins xranges of all
            histos found in the TuningData object to the Observable stored in
            Envelope._obs
        """
        mins = [self.getRange(histo.getBins())[1] for histo in self._td.getMCHistos(self._obs).values()]
        maxs = [self.getRange(histo.getBins())[2] for histo in self._td.getMCHistos(self._obs).values()]
        return min(mins), max(maxs)

    def arrayEntriesAreEqual(self, arr):
        """ this is to compare arrays and to return True and to proceed only if
            the arrays are equal. It is used to check whether the binning
            of the histos belonging to the same observable but different runs
            differs.
            @param arr: this a list of numpy.arrays
        """
        for i in xrange(len(arr)):
            if (arr[0] == arr[i]).all():
                continue
            else:
                raise EnvelopeError('binning seems to differ from run to run'+
                        ' problem occured while processing run %i'%i)
        return True

    def getTube(self):
        """ assuming that the binning doesnt't differ from run to run, this
            returns points of a closed polygon that wraps all datapoints and
            that can be used with the pylab.fill()-method.\n
            if a bin is empty in all histograms (all runs), then the tube is
            filed with a 0.
        """
        binranges = numpy.array([self.getRange(histo.getBins())[0]
            for histo in self._td.getMCHistos(self._obs).values()])
        if self.arrayEntriesAreEqual(binranges) :
            binrange = binranges[0]
        else:
            raise EnvelopeError('binning seems to differ from run to run')

        Temp ={}
        # this will create a dictionary that has Bin.getXRange() returnvalues
        # as keys and all the corresponding Bin.getYVal()returnvalues as values
        for i, item in enumerate(binrange):
            temp = [[bin.getYVal() for bin in histo.getBins()
                if bin.getXRange() == tuple(item)][0]
                for histo in  self._td.getMCHistos(self._obs).values()]
            Temp[tuple(item)] = temp

        # now we only want to have the minimal and maximal values of Temp....
        Ymin = dict([(key, min(value)) for key, value in Temp.iteritems()])
        Ymax = dict([(key, max(value)) for key, value in Temp.iteritems()])

        # now we start the counterclockwise filling of a list with datapoints,
        # starting with the maximum values
        tube = []
        oldrightbinedge=-999999999
        for i, bin in enumerate(binrange):
            if bin[0] == oldrightbinedge or i==0:
                tube.append((bin[0], Ymax[tuple(bin)]))
                tube.append((bin[1], Ymax[tuple(bin)]))
            else:
                tube.append((oldrightbinedge, .0))
                tube.append((bin[0], .0))
                tube.append((bin[0], Ymax[tuple(bin)]))
                tube.append((bin[1], Ymax[tuple(bin)]))
            oldrightbinedge = bin[1]

        # now filling minimal datapoints in reversed binrange order
        oldleftbinedge = 999999999
        for i, bin in enumerate(binrange[::-1]): # this reverses the binrange
           if bin[1] == oldleftbinedge or i==0:
               tube.append((bin[1], Ymin[tuple(bin)]))
               tube.append((bin[0], Ymin[tuple(bin)]))
           else:
               tube.append((oldleftbinedge, .0))
               tube.append((bin[1], .0))
               tube.append((bin[1], Ymax[tuple(bin)]))
               tube.append((bin[0], Ymax[tuple(bin)]))
           oldleftbinedge = bin[0]
        return tube

    def plotEnvelope(self, tube):
        """ plot the Envelope using matplotlib.fill
            @param tube: list, that contains extremal bincontents,
                considered to be a L{getTube()}-object
        """
        TB = numpy.array(tube) # easier to handle
        self._sp.fill(TB[:,0], TB[:,1], 'b', alpha = .05, label = '\\scriptsize Envelope')

    def plotRefData(self, plotstyle='bo'):
        temp = numpy.array([(bin.getXRange()[0] + .5*(bin.getXRange()[1] -bin.getXRange()[0]), bin.getYVal()) for bin in self._td.getRefHisto(self._obs).getBins()])
        # pylab.plot(temp[:,0], temp[:,1], 'bo', label='\\scriptsize ReferenceData')
        self._sp.plot(temp[:,0], temp[:,1], 'bo', label='\\scriptsize ReferenceData')

    def plotPolygon(self, plotstyle=':'):
        """ plots the runs as polygons
            @param plotstyle: this can be any valid matplotlib-plot-expression
            by default one gets dotted lines
        """
        for key, run in self._td.getMCHistos(self._obs).iteritems():
            temp = numpy.array([(bin.getXRange()[0] + .5*(bin.getXRange()[1]-bin.getXRange()[0]), bin.getYVal()) for bin in run.getBins()])
            self._sp.plot(temp[:,0], temp[:,1], ':', label='\\tiny Run\\#%s'%key)

    def plotAll(self, plotwhat=(True, True, False)):
        """ this will draw everything """
        if plotwhat[0]:
            self.plotEnvelope(self.getTube())
        if plotwhat[1]:
            self.plotRefData()
        if plotwhat[2]:
            self.plotPolygon()

    def Show(self):
        """ show everything that was plotted before, create title, labels and
            legends
        """
        pylab.legend(loc=0)
        a, b = self.getTotalXRange()[0][0], self.getTotalXRange()[1][1]
        pylab.xlim(a - .1*(b-a), b + .1*(b-a))
        pylab.ylim(0)
        ## create title
        title = '\\Large \\bf{%s}\\quad\\small{\\tt{(%s)}}'%(
                self._td.getTitle(self._obs).replace('_', '\\_').replace(
                    '^', '\\^'), self._obs.replace('_', '\\_') )
        params = 'params varied:'
        for i in self._params:
            params += '\\quad \\Large{%s} \\normalsize{\\tt{(%s)}} '%(
                    translate.translate(i), i)
        ## display title
        pylab.figtext(.5,.96, title,ha='center')
        pylab.figtext(.5,.92, params,ha='center')
        # pylab.title(title)
        # pylab.title('Observable: \\begin{verbatim}  %s \\end{verbatim}'%self._td.getTitle(self._obs))
        # pylab.title('\\Large envelope plot of observable %s'%(self._obs.replace('_','\\_')))
        pylab.xlabel('Observable')
        pylab.figtext(.05,.5,'Entries', ha='center',va='center', rotation='vertical')
        pylab.grid(True)

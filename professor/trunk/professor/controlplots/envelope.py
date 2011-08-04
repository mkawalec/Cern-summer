import itertools
import numpy
from professor.data import MCData, DataProxy
from professor.tools import log as logging
from professor.tools.errors import DataProxyError
from professor.histo import Bin, Histo



class EnvelopeHisto(Histo):
    defaultcolor = "blue!40!"
    @classmethod
    def mkFromHisto(cls, other):
        """Create an envelope histogram with preset meta-data."""
        new = cls()
        new.path = other.path
        new.name = other.name
        new.title = other.title
        new.xlabel = other.xlabel
        new.ylabel = other.ylabel
        return new

    def __init__(self):
        super(EnvelopeHisto, self).__init__()
        self.confidencelevel = -1.0
        # the color of the band (default: light blue)
        self.color = self.defaultcolor

    def fullPath(self):
        fullaidapath = super(EnvelopeHisto, self).fullPath()
        ## TODO: Use something safer than %f?
        return "Envel-%f-%s" % (self.confidencelevel, fullaidapath)

    def asFlat(self):
        out = "# BEGIN HISTOGRAM %s\n" % self.fullPath()
        if self.confidencelevel > 0.0:
            out += "Title=Envelope (CL %.1f \\%%)\n" % (round(self.confidencelevel, 1))
        elif self.title:
            out += "Title=Envelope %s\n" % self.title
        if self.xlabel:
            out += "XLabel=%s\n" % self.xlabel
        if self.ylabel:
            out += "YLabel=%s\n" % self.ylabel

        out += "ErrorBands=1\n"
        out += "ErrorBandColor=%s\n" % (self.color)
        out += "ErrorBandOpacity=0.45\n"

        out += "LineStyle=none\n"

        out += "## xlow  \txhigh   \tval    \terrminus\terrplus\n"
        out += "\n".join([b.asFlat() for b in self.getBins()])
        out += "\n# END HISTOGRAM"
        return out

    def asAIDA(self):
        raise NotImplementedError("%s is not implemented in %s" % (__name__,
                                  self.__class__))

    def asGnuplot(self):
        raise NotImplementedError("%s is not implemented in %s" % (__name__,
                                  self.__class__))

class TuneHisto(Histo):
    defaultmarker = "pentagon"
    markercycle = itertools.cycle(["o", "+", "x", "asterisk", "square",
                                   "triangle"])
    @classmethod
    def fromAIDA(cls, path):
        runhistos = super(TuneHisto, cls).fromAIDA(path)
        marker = cls.markercycle.next()
        for h in runhistos.values():
            h.polymarker = marker
        return runhistos

    @classmethod
    def fromFlat(cls, stringbuf):
        runhistos = super(TuneHisto, cls).fromFlat(path)
        marker = cls.markercycle.next()
        for h in runhistos.values():
            h.polymarker = marker
        return runhistos

    def __init__(self):
        super(TuneHisto, self).__init__()
        self.polymarker = self.defaultmarker

    def fullPath(self):
        return "Tune-%s" % self.title.replace(" ", "_")

    def asFlat(self):
        out = "# BEGIN HISTOGRAM %s\n" % self.fullPath()
        out += "Title=%s\n" % self.title
        if self.xlabel:
            out += "XLabel=%s\n" % self.xlabel
        if self.ylabel:
            out += "YLabel=%s\n" % self.ylabel

        out += "PolyMarker=%s\n" % self.polymarker
        out += "ErrorBands=0\n"

        out += "LineStyle=none\n"

        out += "## xlow  \txhigh   \tval    \terrminus\terrplus\n"
        out += "\n".join([b.asFlat() for b in self.getBins()])
        out += "\n# END HISTOGRAM"
        return out


class EnvelopeGetter(object):
    """Get envelope data from MCData objects and create envelope plots.

    Main method is getEnvelopeHisto().

    The colors of envelopes for different confidence levels can be adjusted
    using the `envelopecolors' attribute. The colors are applied from high
    to low confidence levels.

    Example
    -------
    To calculate a 95 percent central envelope of observable `OBS' of the MC
    data in mcdata do:
    >>> envelopegetter = EnvelopeGetter(mcdata)
    >>> envelopehisto = envelopegetter.getEnvelopeHisto("OBS", 95.0)

    To create plots with an EnvelopeGetter with data from a DataProxy
    instance:
    >>> envelopegetter = EnvelopeGetter(dataproxy)
    >>> envelopegetter.plotparser = prof.PlotParser()
    >>> envelopegetter.obs = "OBS"
    >>> envelopegetter.addConfidenceLevel(69.0)
    >>> envelopegetter.addConfidenceLevel(95.0)
    >>> makeplots = envelopegetter.plotMakePlots()
    """

    # Colors for envelopes as pstricks colors for make-plots.
    envelopecolors = ["blue!40!", "red!40!yellow", "blue!80!", "red!80!"]

    def __init__(self, data):
        """
        Parameters
        ----------
        data : MCData, DataProxy
            The data to compute the envelopes from. If it's a DataProxy the
            "sample" MC data type is used for envelope calculations.
        """
        self._dataproxy = None
        self._mcdata = None
        self.setData(data)
        self.plotparser = None
        # list of {histo-path => histogram}
        self.tunes = []


    def setData(self, data):
        if isinstance(data, MCData):
            self._mcdata = data
        elif isinstance(data, DataProxy):
            self._dataproxy = data

    def getMCData(self):
        if self._mcdata is not None:
            return self._mcdata
        return self._dataproxy.getMCData("sample")
    mcdata = property(getMCData)


    def addConfidenceLevel(self, cl, realcl=False):
        """Create an envelope plot with confidence level.

        The observable must be set previously via the obs property.

        See
        ---
        getEnvelopeHisto
        """
        if self.obs is None:
            raise RuntimeError("The observable to plot is not set. Use"
                               " 'setObs()' or the 'obs' property.")

        envhisto = self.getEnvelopeHisto(self.obs, cl, realcl)
        self._envelopes.append(envhisto)


    def setObs(self, obs):
        """Set the observable to plot."""
        self.refhisto = None    # reference histogram
        self._envelopes = []    # list of EnvelopeHisto's

        self._obs = obs

    obs = property(lambda self: self._obs, setObs,
                   doc="Create plots for this observable.")


    def getEnvelopeHisto(self, obs, cl=100.0, realcl=False):
        """Get an envelope histogram.

        MC errors are ignored!

        Parameters
        ----------
        obs : str
            Path of the observable.
        cl : float, optional
            The targeted confidence level in percent [default: 100].
        realcl : bool, optional
            Store the actual confidence in the returned envelope histogram
            [default: False].

        Returns
        -------
        out : EnvelopeHisto
            An EnvelopeHisto histogram with y-value +- y-error spanning over
            the band of the given confidence level. The `confidencelevel'
            property is set to the targeted or real confidence level.
        """
        if cl > 100.0 or cl < 0.0:
            raise ValueError("Argument cl must be in [0.0, 100.0]!")

        # Get the bin content of all bins from all runs.
        # Index order: [bin, run]
        values = self._getBinValues(obs)

        # Sort along run index axis ...
        values.sort(axis=1)
        # ... and cut (1-CL)/2 fraction of sorted values from top and
        # bottom.
        nruns = len(self.mcdata.availableruns)
        ncuts = int(round((100.0-cl)*nruns*0.5/100.0))
        realcl = (nruns - 2.0*ncuts)/nruns * 100.0
        # Log a warning if real and targetted confidence level differ more
        # than 5%.
        if abs(realcl-cl)/cl > 0.05:
            logging.warn("Real (%f) and targeted (%f) confidence level differ "
                         "by more than 5%%" % (realcl, cl))
        logging.debug("Requested a CL of %f: Rounding gives that %i top and "
                      "bottom runs (of %i runs total) are stripped => "
                      "real CL = %f" % (cl, ncuts, nruns, realcl))
        if ncuts > 0:
            values = values[:, ncuts:-ncuts]

        valmin = values.min(axis=1)
        valmax = values.max(axis=1)

        valerr = 0.5*(valmax - valmin)
        valmean = valmin + valerr

        # copy meta-data from run0 histogram to our output histogram
        run0 = self.mcdata.getRunHistos(self.mcdata.availableruns[0])
        histo0 = run0[obs]
        out = EnvelopeHisto.mkFromHisto(histo0)
        if realcl:
            out.confidencelevel = realcl
        else:
            out.confidencelevel = cl    # default

        for ibin, bin0 in enumerate(histo0):
            xlow, xhigh = bin0.getXRange()
            out.addBin(Bin(xlow, xhigh,
                           val = valmean[ibin],
                           errplus = valerr[ibin],
                           errminus = valerr[ibin]))

        return out

    def _getBinValues(self, obs):
        """Helper function. Returns a 2D array with the bin contents of obs.

        Parameters
        ----------
        obs : str
            Path of the observable.

        Returns
        -------
        values : numpy.ndarray
            2D numpy array with the contents of all bins and all runs.
            Array index order is [bin, run].
        """
        nruns = len(self.mcdata.availableruns)
        run0 = self.mcdata.getRunHistos(self.mcdata.availableruns[0])
        nbins = run0[obs].numBins()

        # index order [bin, run]
        values = numpy.zeros((nbins, nruns))
        for irun, run in enumerate(self.mcdata.availableruns):
            histo = self.mcdata.getRunHistos(run)[obs]
            for ibin, bin in enumerate(histo):
                values[ibin, irun] = bin.getVal()
        return values

    def plotMakePlots(self, noratio=False):
        if len(self._envelopes) == 0:
            raise RuntimeError("No envelope plots available. Call addConfidenceLevel() first!")

        # Use a heuristic for logging levels: If no dataproxy was given
        # (self._dataproxy is None) we log with WARN priority. If a
        # dataproxy was set, we assume the user wanted reference data to be
        # available and we log with ERROR priority.
        try:
            refhisto = self._dataproxy.getRefHisto(self.obs)
            logging.debug("Reference data for envelope available for histo '%s'" % self.obs)
        except AttributeError, err:
            logging.warn("No reference data available in envelopes for histo '%s'" % self.obs)
            refhisto = None
        except Exception, err:
            logging.error("Observable '%s' is missing in reference data!" % self.obs)
            refhisto = None

        tunehistos = []
        for tune in self.tunes:
            try:
                tunehistos.append(tune[self.obs])
            except KeyError:
                logging.warn("Observable '%s' is not available in one of the tunes!" % self.obs)

        # Sort envelopes by their confidence level, from high to low.
        self._envelopes = sorted(self._envelopes,
                                 key=lambda eh: eh.confidencelevel,
                                 reverse=True)

        # Write PLOT header. The order is important to see the tunes/ref
        # data plot them *after* the envelopes.
        out = "# BEGIN PLOT\n"
        out += "DrawOnly="
        out += " ".join([eh.fullPath() for eh in self._envelopes])
        out += " "
        out += " ".join([th.fullPath() for th in tunehistos])
        out += " "

        # Plot the reference histo if it exists
        if refhisto is not None:
            # Some Title mangling
            expt = refhisto.fullpath.split("/")[2].split("_")[0]
            refhisto.title = "%s data" % expt
            out += refhisto.fullPath()
        out += "\n"

        # Try to add the ratio plot in case there is a refhisto
        if refhisto and not noratio:
            out += "RatioPlot=1\n"
            out += "RatioPlotReference=%s\n"%refhisto.fullPath()
        else:
            out += "RatioPlot=0\n"

        if self.plotparser is not None:
            try:
                headdict = self.plotparser.getHeaders(self.obs)
                for k, v in headdict.iteritems():
                    out += "%s=%s\n" % (k, v)
                #
            except:
                headdict = None

        out += "Legend=1\n"

        # Set LogY=1 by default
        if headdict:
            if "LogY" in headdict.keys():
                out += "LogY=%s\n"%headdict["LogY"]
            else:
                out += "LogY=1\n"
        else:
            out += "LogY=1\n"


        out += "# END PLOT\n\n"
        if refhisto is not None:
            out += refhisto.asFlat()

        if tunehistos:
            out += "\n\n"
            out += "\n\n".join([th.asFlat() for th in tunehistos])

        # Set different colors for the envelopes.
        colcycle = itertools.cycle(self.envelopecolors)
        for eh in self._envelopes:
            eh.color = colcycle.next()
            out += "\n\n" + eh.asFlat()
        return out

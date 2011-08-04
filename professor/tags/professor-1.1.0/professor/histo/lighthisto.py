# Use posixpath instead of os.path for AIDA path handling to be platform
# independent, i.e. always use "/" as path delimiter.
import posixpath
import os
import re

from professor.tools import log as logging
from professor.tools.elementtree import ET

__all__= ['Histo', 'Bin', 'PlotParser']


from htmlentitydefs import codepoint2name
unichr2entity = {}
for code, name in codepoint2name.iteritems():
    # exclude "&"
    if code != 38:
        unichr2entity[unichr(code)] = u"&%s;" % (name)


# Using mutable types as (dict, list) as default arguments can have nasty
# side effects.
def htmlescape(text, d=None):
    if d is None:
        d = unichr2entity
    if u"&" in text:
        text = text.replace(u"&", u"&amp;")
    for key, value in d.iteritems():
        if key in text:
            text = text.replace(key, value)
    return text


# Histo and Bin classes were copied from aida2flat

class Histo(object):
    """Simple container for histograms storing a list of :class:`Bin` instances.

    Histogram trees can be read in from AIDA and flat format files with
    :meth:`~Histo.fromAIDA` and :meth:`~histo.fromFlat`. These methods
    produce dictionaries mapping histogram paths to histograms. For string
    representations for AIDA and flat output :meth:`~Histo.asFlat` and
    :meth:`~Histo.asAIDA` can be used.

    Two different paths for histograms exist:

    :attr:`histopath`
        The path of the histogram.

    :attr:`fullpath`
        The full path of the histogram including "/REF" for reference histograms.

    Looping over the bins in a histogram can be simply done by::

        >>> for b in myhisto:
        ...     # do stuff with Bin b

    """
    aidaindent = "  "
    def __init__(self):
        self._bins = []
        # the leading AIDA path (including /REF) but not the observable name
        self.path = None
        # the observable name, e.g. d01-x02-y01
        self.name = None
        # the histogram title
        self.title = ''
        self.xlabel = ''
        self.ylabel = ''
        self._sorted = False

    def __cmp__(self, other):
        """Sort by $path/$name string"""
        return self.fullPath() > other.fullPath()

    def __str__(self):
        out = "Histogram '%s' with %d bins\n" % (self.fullPath(), self.numBins())
        out += "Title: %s\n" % self.title
        out += "XLabel: %s\n" % self.xlabel
        out += "YLabel: %s\n" % self.ylabel
        out += "\n".join([str(b) for b in self.getBins()])
        return out

    def fullPath(self):
        return posixpath.join(self.path, self.name)
    fullpath = property(fullPath,
            doc="Full AIDA path including leading '/REF' and histogram name")

    def histoPath(self):
        if self.path.startswith("/REF"):
            return self.fullpath[4:]
        else:
            return self.fullpath
    histopath = property(histoPath,
            doc="AIDA path but without a leading '/REF'")

    def header(self):
        out = "# BEGIN PLOT\n"
        out += "LogY=1\n"
        out += "Title=%s\n" % self.title
        out += "XLabel=%s\n" % self.xlabel
        out += "YLabel=%s\n" % self.ylabel
        out += "# END PLOT\n"
        return out

    def asFlat(self):
        out = "# BEGIN HISTOGRAM %s\n" % self.fullPath()
        out += "AidaPath=%s\n" % self.fullPath()
        out += "Title=%s\n" % self.title
        if self.xlabel:
            out += "XLabel=%s\n" % self.xlabel
        if self.ylabel:
            out += "YLabel=%s\n" % self.ylabel
        if self.fullPath().startswith('/REF'):
            out += "PolyMarker=*\n"
            out += "ErrorBars=1\n"
        out += "## Area: %e\n" % self.area()
        out += "## Num bins: %d\n" % self.numBins()
        out += "## xlow  \txhigh   \tyval    \tyerrminus\tyerrplus\n"
        out += "\n".join([b.asFlat() for b in self.getBins()])
        out += "\n# END HISTOGRAM"
        return out

    def asGnuplot(self):
        out  = "## HISTOGRAM: %s\n" % self.fullPath()
        out += "## Title: %s\n" % self.title
        if (self.xlabel!=''):
            out += "## XLabel: %s\n" % self.xlabel
        if (self.ylabel!=''):
            out += "## YLabel: %s\n" % self.ylabel
        out += "## Area: %s\n" % self.area()
        out += "## Num bins: %d\n" % self.numBins()
        out += "## xval  \tyval    \txlow    \txhigh    \tylow     \tyhigh\n"
        out += "\n".join([b.asGnuplot() for b in self.getBins()])
        out += "\n# END HISTOGRAM"
        return out

    def asAIDA(self):
        ind = self.aidaindent
        r = ind + '<dataPointSet name="%s" dimension="2"\n' % (
                self.name)
        if self.title is not None:
            r += ind + '    path="%s" title="%s">\n' % (
                    self.path, htmlescape(self.title))
        else:
            r += ind + '    path="%s" title="">\n' % (
                    self.path)
        if (self.xlabel!=''):
            r += ind + '  <dimenstion dim="0" title="%s"/>\n' % (
                    htmlescape(self.xlabel))
        if (self.ylabel!=''):
            r += ind + '  <dimenstion dim="1" title="%s"/>\n' % (
                    htmlescape(self.ylabel))
        r += ind + "  <annotation>\n"
        if (self.title!=''):
            r += ind + '    <item key="Title" value="%s" sticky="true"/>\n' % (
                    htmlescape(self.title))
        else:
            r += ind + '    <item key="Title" value="" sticky="true"/>\n'
        r += ind + '    <item key="AidaPath" value="%s" sticky="true"/>\n' % (
                self.fullPath())
        # TODO: FullPath annotation item?
        # r += ind + '    <item key="FullPath" value
        r += ind + "  </annotation>\n"
        for b in self:
            r += b.asAIDA()
        r += ind + "</dataPointSet>\n"
        return r

    def numBins(self):
        return len(self._bins)

    def getBins(self):
        if not self._sorted:
            self._bins.sort()
            self._sorted = True
        return self._bins

    def setBins(self, bins):
        self._bins = bins
        self._sorted = False
        return self

    def addBin(self, bin):
        self._bins.append(bin)
        self._sorted = False
        return self

    def getBin(self, index):
        if not self._sorted:
            self._bins.sort()
            self._sorted = True
        return self.getBins()[index]

    bins = property(getBins, setBins)

    def area(self):
        return sum([bin.area() for bin in self.bins])
    getArea = area

    def __iter__(self):
        return iter(self.getBins())

    def __len__(self):
        return len(self._bins)

    def __getitem__(self, index):
        return self.getBin(index)

    def chop(self, *xranges):
        """Return a chopped histogram.

        The kept bins are defined by (xstart, xstop) pairs. The first xstart
        and last xstop can be None meaning that all is included from the
        first or up to the last bin respectively.
        Example:
            >>> hist.chop((2.5, 5.5), (7.5, None))
        """
        if len(xranges) == 0:
            raise ValueError("At least one (xstart, xstop) range is needed!")
        # check that xranges is
        laststop = xranges[0][1]
        for xr in xranges[1:]:
            if laststop >= xr[0]:
                raise ValueError("(xstart, xstop) ranges must be in numerical order!")
            laststop = xr[1]

        new = Histo()
        new.path = self.path
        new.name = self.name
        new.title = self.title
        new.xlabel = self.xlabel
        new.ylabel = self.ylabel

        irange = 0
        curran = xranges[irange]
        for b in self:
            #lowok = False
            #highok = False
            br = b.getXRange()
            # update the current range used if we exceed the current upper
            # limit
            while (curran[1] is not None and
                    irange < len(xranges) - 1 and
                    br[0] > curran[1]):
                irange += 1
                curran = xranges[irange]

            if ((curran[0] is None or curran[0] <= br[0] or
                        br[0] <= curran[0] <= br[1]) and

                (curran[1] is None or curran[1] >= br[1] or
                        br[0] <= curran[1] <= br[1])):
                new.addBin(b)
            else:
                logging.debug("Chopping bin %s: %e" % (self.fullPath(), b.getBinCenter()))
        return new

    def renormalise(self, newarea):
        """ Renormalise histo to newarea """
        # Construc new histo
        new = Histo()
        # Use the same metadata
        new.path = self.path
        new.name = self.name
        new.title = self.title
        new.xlabel = self.xlabel
        new.ylabel = self.ylabel

        # The current histogram area
        oldarea = self.getArea()

        # Iterate over all bins
        for b in self:
            # Rescale YValue, YErr+, YErr-
            newy = b.yval * float(newarea) / oldarea
            newyerrplus = b.yerrplus * float(newarea) / oldarea
            newyerrminus = b.yerrminus * float(newarea) / oldarea
            newbin = Bin(b.xlow, b.xhigh, newy, newyerrplus, newyerrminus, b.focus)
            new.addBin(newbin)

        return new

    ## decorators are only available since Python 2.4
    def fromDPS(cls, dps):
        """Build a histogram from a xml dataPointSet."""
        new = cls()
        new.name = dps.get("name")
        new.title = dps.get("title")
        new.path = dps.get("path")
        # # strip /REF from path
        # if new.path.startswith("/REF"):
            # new.path = new.path[4:]
        axes = dps.findall("dimension")
        if (len(axes)==2):
            for a in axes:
                if (a.get("dim")=="0"):
                    new.xlabel = a.get("title")
                elif (a.get("dim")=="1"):
                    new.ylabel = a.get("title")
        points = dps.findall("dataPoint")
        #numbins = len(points)
        for binnum, point in enumerate(points):
            bin = Bin()
            for d, m in enumerate(point.findall("measurement")):
                val  = float(m.get("value"))
                down = float(m.get("errorMinus"))
                up = float(m.get("errorPlus"))
                if d == 0:
                    low  = val - down
                    high = val + up
                    bin.setXRange(low, high)
                elif d == 1:
                    bin.yval = val
                    bin.yerrplus = up
                    bin.yerrminus = down
            new.addBin(bin)
        return new
    fromDPS = classmethod(fromDPS)

    def fromFlat(cls, stringbuf):
        """Build a histogram from a string buffer containing flat-format."""
        desc = {}
        new = cls()
        for line in stringbuf:
            line = line.rstrip()
            if "=" in line:
                linearray = line.split("=", 0)
                desc[linearray[0]] = linearray[1]
            else:
                linearray = line.split()
                if len(linearray) == 4:
                    new.addBin(Bin(float(linearray[0]), float(linearray[1]),
                                   float(linearray[2]),
                                   float(linearray[3]), float(linearray[3])))
                elif len(linearray) == 5:
                    new.addBin(Bin(float(linearray[0]), float(linearray[1]),
                                   float(linearray[2]),
                                   float(linearray[3]), float(linearray[4])))
                else:
                    logging.error("Unknown line format in '%s'" % (line))
        new.path, new.name = posixpath.split(desc["AidaPath"])
        if desc.has_key("Title"):
            new.title = desc["Title"]
        if desc.has_key("XLabel"):
            new.title = desc["XLabel"]
        if desc.has_key("YLabel"):
            new.title = desc["YLabel"]
        return new
    fromFlat = classmethod(fromFlat)

    def fromAIDA(cls, path):
        """Load all histograms in file 'path' into a histo-path=>histo dict.

        The keys of the dictionary are the full paths of the histogram, i.e.
        AnaylsisID/HistoID, a leading "/REF" is stripped from the keys.
        """
        runhistos = dict()
        tree = ET.parse(path)
        for dps in tree.findall("dataPointSet"):
            fullpath = posixpath.join(dps.get("path"), dps.get("name"))
            if fullpath.startswith("/REF"):
                fullpath = fullpath[4:]
            runhistos[fullpath] = cls.fromDPS(dps)
        return runhistos
    fromAIDA = classmethod(fromAIDA)


class Bin(object):
    """A simple container for a binned value with an error."""
    aidaindent = "    "
    __slots__ = ["xlow", "xhigh", "yval", "yerrplus", "yerrminus", "focus"]
    def __init__(self, xlow=None, xhigh=None, yval=0, yerrplus=0, yerrminus=0, focus=None):
        def _float(f):
            if f is None:
                return None
            return float(f)
        self.xlow = _float(xlow)
        self.xhigh= _float(xhigh)
        self.yval = _float(yval)
        self.yerrplus = _float(yerrplus)
        self.yerrminus = _float(yerrminus)
        self.focus= _float(focus)

    def __str__(self):
        out = "%e to %e: %e +%e-%e" % (self.xlow, self.xhigh,
                self.yval, self.yerrplus, self.yerrminus)
        return out

    def asFlat(self):
        out = "%e\t%e\t%e\t%e\t%e" % (self.xlow, self.xhigh, self.yval, self.yerrminus, self.yerrplus)
        return out

    def asGnuplot(self):
        out = "%e\t%e\t%e\t%e\t%e\t%e" % (self.getBinCenter(), self.yval,
                self.xlow, self.xhigh, self.yval-self.yerrminus,
                self.yval+self.yerrplus)
        return out

    def asAIDA(self):
        "Return this bin as AIDA formatted string."
        ind = self.aidaindent
        return (ind + "<dataPoint>\n"
            + ind
            + '  <measurement errorPlus="%e" value="%e" errorMinus="%e"/>\n' % (
                self.getXErrPlus(), self.getBinCenter(), self.getXErrMinus())
            + ind
            + '  <measurement errorPlus="%e" value="%e" errorMinus="%e"/>\n' % (
                self.yerrplus, self.yval, self.yerrminus)
            + ind + "</dataPoint>\n")

    def __cmp__(self, other):
        """Sort by mean x value (yeah, I know...)"""
        return (self.xlow + self.xhigh) > (other.xlow + other.xhigh)

    def getXRange(self):
        return (self.xlow, self.xhigh)

    def setXRange(self, xlow, xhigh):
        self.xlow = xlow
        self.xhigh = xhigh
        return self

    def getBinCenter(self):
        """Geometric middle of the bin range."""
        return float(self.xlow + .5*(self.xhigh - self.xlow))

    def getXErrPlus(self):
        return self.xhigh - self.getBinCenter()

    def getXErrMinus(self):
        return self.getBinCenter() - self.xlow

    def getFocus(self):
        """Mean x-value of the bin."""
        if self.focus is not None:
            return (self.xlow + self.xhigh)/2.0
        else:
            return self.focus

    def getYVal(self):
        """Y-value of the bin."""
        return self.yval

    def area(self):
        return self.yval * (self.xhigh - self.xlow)
    getArea = area

    def getYErr(self):
        """Get mean of +ve and -ve y-errors."""
        return (self.yerrplus + self.yerrminus)/2.0

    def setYErr(self, yerr):
        """Set both +ve and -ve y-errors simultaneously."""
        self.yerrplus = yerr
        self.yerrminus = yerr
        return self

    yerr = property(getYErr, setYErr)


class PlotParser(object):
    """Parser for rivet's .plot plotinfo files."""
    pat_begin_block = re.compile('^# BEGIN ([A-Z0-9_]+) ?(\S+)?')
    # temporarily allow several hashes before END for YODA
    pat_end_block =   re.compile('^#+ END ([A-Z0-9_]+)')
    pat_comment = re.compile('^#|^\s*$')
    pat_property = re.compile('^(\w+?)=(.*)$')
    pat_path_property  = re.compile('^(\S+?)::(\w+?)=(.*)$')

    def __init__(self, plotpaths=None):
        """
        Parameters
        ----------
        plotpaths : list of str, optional
            The directories to search for .plot files.
            The default is to call :command:`rivet-config --datadir` to get
            the directory where the .plot files can be found.

        Raises
        ------
        ValueError
            If `plotpaths` is not specified and calling
            :command:`rivet-config` fails.
        """
        if plotpaths is None:
            plotpaths = []
        self.plotpaths = plotpaths

        if len(self.plotpaths) == 0:
            try:
                # Use old os.popen to be Python 2.3 compatible.
                path = os.popen("rivet-config --datadir", "r").readline()
                path = path.strip()
                if not path:
                    raise ValueError("Path is empty!")
                self.plotpaths.append(path)
            except Exception:
                raise ValueError("No plotpaths given and rivet-config call failed!")

    def getSection(self, section, hpath):
        """Get a section for a histogram from a .plot file.

        Parameters
        ----------
        section : ('PLOT'|'SPECIAL'|'HISTOGRAM')
            The section that should be extracted.
        hpath : str
            The histogram path, i.e. /AnaylsisID/HistogramID .

        Todo
        ----
        Caching
            At the moment the result of the lookup is not cache so every
            call requires a file to be opened.
        """
        if section not in ['PLOT', 'SPECIAL', 'HISTOGRAM']:
            raise ValueError("Can't parse section \'%s\'" %section)

        parts = hpath.split("/")
        if len(parts) != 3:
            raise ValueError("hpath has wrong number of parts (%i)" % (len(parts)))
        base = parts[1] + ".plot"
        ret = {'PLOT': {}, 'SPECIAL': None, 'HISTOGRAM': {}}
        for pidir in self.plotpaths:
            if os.access(os.path.join(pidir, base), os.R_OK):
                plotfile = os.path.join(pidir, base)
                startreading = False
                f = open(plotfile)
                for line in f:
                    m = self.pat_begin_block.match(line)
                    if m:
                        tag, pathpat = m.group(1,2)
                        # pathpat could be a regex
                        if tag == section and re.match(pathpat,hpath):
                            startreading=True
                            if section in ['SPECIAL']:
                                ret[section] = ''
                            continue
                    if not startreading:
                        continue
                    if self.isEndMarker(line, section):
                        startreading=False
                        continue
                    elif self.isComment(line):
                        continue
                    if section in ['PLOT', 'HISTOGRAM']:
                        vm = self.pat_property.match(line)
                        if vm:
                            prop, value = vm.group(1,2)
                            ret[section][prop] = value
                    elif section in ['SPECIAL']:
                        ret[section] += line
                f.close()
        return ret[section]


    def getHeaders(self, hpath):
        """Get the plot headers for histogram hpath.

        This returns the PLOT section.

        Parameters
        ----------
        hpath : str
            The histogram path, i.e. /AnaylsisID/HistogramID .

        Returns
        -------
        plot_section : dict
            The dictionary usually contains the 'Title', 'XLabel' and
            'YLabel' properties of the respective plot.

        See also
        --------
        :meth:`getSection`
        """
        return self.getSection('PLOT', hpath)

    def getSpecial(self, hpath):
        """Get a SPECIAL section for histogram hpath.

        The SPECIAL section is only available in a few analyses.

        Parameters
        ----------
        hpath : str
            Histogram path. Must have the form /AnalysisID/HistogramID .

        See also
        --------
        :meth:`getSection`
        """
        return self.getSection('SPECIAL', hpath)

    def getHistogramOptions(self, hpath):
        """Get a HISTOGRAM section for histogram hpath.

        The HISTOGRAM section is only available in a few analyses.

        Parameters
        ----------
        hpath : str
            Histogram path. Must have the form /AnalysisID/HistogramID .

        See also
        --------
        :meth:`getSection`
        """
        return self.getSection('HISTOGRAM', hpath)

    def isEndMarker(self, line, blockname):
        m = self.pat_end_block.match(line)
        return m and m.group(1) == blockname

    def isComment(self, line):
        return self.pat_comment.match(line) is not None

    def updateHistoHeaders(self, hist):
        headers = self.getHeaders(hist.histopath)
        if headers.has_key("Title"):
            hist.title = headers["Title"]
        if headers.has_key("XLabel"):
            hist.xlabel = headers["XLabel"]
        if headers.has_key("YLabel"):
            hist.ylabel = headers["YLabel"]

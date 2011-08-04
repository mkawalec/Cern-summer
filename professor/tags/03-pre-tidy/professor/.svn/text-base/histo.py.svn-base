import os.path

class Histo(object):
    def __init__(self):
        self._bins = []
        self._issorted = False
        self._name = None
        self._path = None
        self._title = None

    def __str__(self):
        out = "Histogram with %d bins:" % self.numBins()
        for b in self.getBins():
            out += "\n" + str(b)
        return out

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name
        return self
    name = property(getName, setName)

    def getTitle(self):
        return self._title

    def setTitle(self, title):
        self._title = title
        return self
    title = property(getTitle, setTitle)

    def setPath(self, path):
        self._path = path
    path = property(lambda s: s._path, setPath)
    fullname = property(lambda s: os.path.join(s.path, s.name))

    def numBins(self):
        return len(self._bins)

    def getBins(self):
        if not self._issorted:
            self._bins.sort()
            self._issorted = True
        return self._bins

    def setBins(self, bins):
        self._bins = bins
        self._issorted = False
        return self

    def addBin(self, bin):
        self._bins.append(bin)
        self._issorted = False
        return self

    def getBin(self, index):
        return self.getBins()[index]

    def __iter__(self):
        return iter(self.getBins())

    def __len__(self):
        return len(self._bins)

    def __getitem__(self, index):
        return self.getBin(index)

    def getHistoArea(self):
        return sum([bin.getArea() for bin in self.getBins()])

    def asFlat(self):
        out = "# BEGIN HISTOGRAM %s\n" % self.getName()
        out += "AidaPath=%s\n" % self.getName()
        out += "Title=%s\n" % self.getTitle()
        out += "## Area: %s\n" % self.getHistoArea()
        out += "## Num bins: %d\n" % self.numBins()
        #if opts.GNUPLOT:
            #out += "## xval  \tyval    \txlow    \txhigh    \tylow     \tyhigh\n"
        #else:
            #out += "## xlow  \txhigh   \tyval    \tyerrminus\tyerrplus\n"
        out += "## xlow  \txhigh   \tyval    \tyerrminus\tyerrplus\n"
        out += "\n".join([bin.asFlat() for bin in self.getBins()])
	out += "\n# END HISTOGRAM"
        return out


class Bin(object):
    """A simple container for a binned value with an error.\n
        TODO: * asymmetric errors
    """
    def __init__(self, xlow=None, xhigh=None, yval=0, yerr=0, focus=0):
        self._xlow = xlow
        self._xhigh= xhigh
        self._yval = yval
        self._yerr = yerr
        self._focus= focus

    def __str__(self):
        out = "%f to %f: %f +- %f" % (self._xlow, self._xhigh, self._yval, self._yerr)
        return out

    def __cmp__(self, other):
        """Sort by mean x value (yeah, I know...)"""
        return (self._xlow + self._xhigh) > (other._xlow + other._xhigh)

    def getXRange(self):
        return (self._xlow, self._xhigh)

    def setXRange(self, xlow, xhigh):
        self._xlow = xlow
        self._xhigh = xhigh
        return self

    def getBinCenter(self):
        """Geometric middle of the bin range."""
        return self._xlow + .5*(self._xhigh - self._xlow)

    def getFocus(self):
        """Mean x-value of the bin."""
        return self._focus

    def getYVal(self):
        return self._yval

    def setYVal(self, yval):
        self._yval = yval
        return self

    def getYErr(self):
        return self._yerr

    def setYErr(self, yerr):
        self._yerr = yerr
        return self

    def getArea(self):
        low, high = self.getXRange()
        return self.getYVal()*(high - low)

    def asFlat(self):
        low, high = self.getXRange()
        return "%e\t%e\t%e\t%e\t%e" % (low, high, self.getYVal(), self.getYErr(), self.getYErr())

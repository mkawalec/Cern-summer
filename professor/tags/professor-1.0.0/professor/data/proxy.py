import os
import itertools

from professor import histo
## TODO: hide that MD5 is used for hash implementation?
from professor.tools.hashes import md5

from professor.tools.decorators import deprecated

from mcdata import MCData
from tunedata import TuneData

from professor.interpolation.interpolationset import InterpolationSet
from professor.tools.errors import DataProxyError, IOTestFailed
from professor.tools import io
import professor.tools.log as logging



class DataProxy(object):
    """Central object for loading data from the file system.

    Three types of data are handled:

    Reference data :
        TODO

    MC data :
        Different types of MC data can be stored. The MC data is stored in a
        `dict` ``{type-ID => MCData}`` . type-IDs are for example 'sample'
        or 'scan'.

    Interpolations :
        TODO

    See Also
    --------
    MCData : Abstraction of a MC data subdirectory.
    """

    def __init__(self):
        self._refpath = None
        self._ipolpath = None
        self._mcpaths = dict()

        # { histo path => Histo }
        self._refdata = None
        # { data type => MCData }
        self._mcdata = dict()
        # Do not cache InterpolationSets: this is probably too memory-intensive
        # self._ipoldata = None

    def __str__(self):
        """
        Mildly informative string representation.
        """
        s = "<%s ref(%s)" % (self.__class__.__name__, self._refpath)
        for typeid, mcdata in self._mcdata.items():
            s += " mc-%s(%s)" % (typeid, mcdata.basepath)
        s += " ipol(%s)>" % self._ipolpath
        return s


    @staticmethod
    def getPathsFromCLOptions(opts):
        """Return a dict with the data paths specified on command line.

        The dictionary has the following 4 keys:

            * mc
            * ref
            * scan
            * ipol

        Each value can contain `None` meaning that the respective
        command-line option is not available or that a value could not be
        constructed from e.g. DATADIR/mc .

        Arguments
        ---------
        opts : optparse.Values
        """
        datadir = opts.DATADIR
        paths = {"mc":None, "ref":None, "scan":None, "ipol":None}
        try:
            if opts.MCDIR is not None:
                paths["mc"] = opts.MCDIR
            elif datadir is not None:
                paths["mc"] = os.path.join(datadir, "mc")
            else:
                logging.warn("Command-line option defined for `mcdir` but"
                             " no value could be build. Continue and hope"
                             " for the best...")
        except AttributeError, err:
            logging.debug("mcdir not found in CL options: %s" % (err))
            ## No opts.MCDIR defined in OptionParser that produced opts

        try:
            if opts.REFDIR is not None:
                paths["ref"] = opts.REFDIR
            elif datadir is not None:
                paths["ref"] = os.path.join(datadir, "ref")
            else:
                logging.warn("Command-line option defined for `refdir` but"
                             " no value could be build. Continue and hope"
                             " for the best...")
        except AttributeError, err:
            logging.debug("refdir not found in CL options: %s" % (err))
            ## No opts.REFDIR defined in OptionParser that produced opts

        try:
            if opts.SCANDIR is not None:
                paths["scan"] = opts.SCANDIR
            elif datadir is not None:
                paths["scan"] = os.path.join(datadir, "scan")
            else:
                logging.warn("Command-line option defined for `scandir` but"
                             " no value could be build. Continue and hope"
                             " for the best...")
        except AttributeError, err:
            logging.debug("scandir not found in CL options: %s" % (err))
            ## No opts.SCANDIR defined in OptionParser that produced opts

        try:
            if opts.IPOLDIR is not None:
                paths["ipol"] = opts.IPOLDIR
            elif datadir is not None:
                paths["ipol"] = os.path.join(datadir, "ipol")
            else:
                logging.warn("Command-line option defined for `ipoldir` but"
                             " no value could be build. Continue and hope"
                             " for the best...")
        except AttributeError, err:
            logging.debug("ipoldir not found in CL options: %s" % (err))
            ## No opts.IPOLDIR defined in OptionParser that produced opts

        return paths


    @classmethod
    def mkFromCLOptions(cls, opts, checkAIDA=True):
        """Build DataProxy from CL-options that were prepared with
        addDataCLOptions.

        Only the paths are set in the returned DataProxy for which the
        parser has an according option.

        See Also
        --------
        addDataCLOptions : Add a data location command-line option group to
            an `OptionParser`.
        getPathsFromCLOptions : Get a `dict` of data-location paths from
            command line options.
        """
        # Try to create more comfortable RivetDataProxy. Do this here so we
        # don't need to modify all prof-* scripts.
        # Use the refdir as specified if it is given explicitly on the command line
        if cls != RivetDataProxy and hasattr(opts, "REFDIR") and opts.REFDIR is None:
            try:
                logging.debug("Trying to create RivetDataProxy")
                return RivetDataProxy.mkFromCLOptions(opts)
            except Exception, err:
                logging.warning("Could not create RivetDataProxy: %s" % err)
        else:
            logging.debug("Not creating RivetDataProxy")

        proxy = cls()
        paths = cls.getPathsFromCLOptions(opts)

        if paths["ref"] is not None:
            proxy.refpath = paths["ref"]
        if paths["ipol"] is not None:
            proxy.ipolpath = paths["ipol"]

        if paths["mc"] is not None:
            proxy.setMCPath(paths["mc"], "sample", checkAIDA=checkAIDA)
        if paths["scan"] is not None:
            proxy.setMCPath(paths["scan"], "linescan", checkAIDA=checkAIDA)

        return proxy

    @classmethod
    @deprecated("mkFromCLOptions")
    def fromCLOptions(cls, opts):
        return cls.mkFromCLOptions(opts)

    #END Command-line I/O


    def setDataPath(self, base):
        """Set data location paths rooted at `base`.

        Sets the data location paths for reference data (`base/ref`),
        MC sample (`base/mc`) and interpolation storage (`base/ipol/`).

        Parameters
        ----------
        base : str
            Base path for data locations.
        """
        temp = os.path.join(base, "ref")
        if os.path.isdir(temp):
            self.setRefPath(temp)

        temp = os.path.join(base, "mc")
        if os.path.isdir(temp):
            self.setMCPath(temp, "sample")

        temp = os.path.join(base, "ipol")
        if os.path.isdir(temp):
            self.setIpolPath(temp)


    def setRefPath(self, path):
        self._refdata = None
        io.testReadDir(path)
        self._refpath = path


    def getRefPath(self):
        if self._refpath is None:
            raise DataProxyError("No reference data path set!")
        return self._refpath

    refpath = property(getRefPath, setRefPath,
                       doc="base directory for reference data .aida files")


    def _loadRefData(self, force=False):
        """Load all reference data if not done before.

        Raises
        ------
        DataProxyError
            If `self.refpath` is not set.
        """
        if not force and self._refdata is not None:
            return

        # Call this before self._refdata is initialised to check that
        # refpath is set. If it's not set an DataProxyError is raised.
        refdircontent = os.listdir(self.refpath)

        self._refdata = dict()

        for reffile in refdircontent:
            ## TODO: generalise file type: move AIDA-specifics into histo.aida
            if not reffile.endswith(".aida"):
                continue
            reffilepath = os.path.join(self.refpath, reffile)
            if not os.path.isfile(reffilepath):
                logging.warn("Could not read reference file: " + reffilepath)
            self._refdata.update(histo.Histo.fromAIDA(reffilepath))


    def getRefHisto(self, histopath):
        """Get a reference histogram.

        Parameters
        ----------
        histopath : str
            A histogram path of the form '/Analysis/HistoID'.

        Raises
        ------
        DataProxyError
            If `self.refpath` is not set.
        KeyError
            If `histopath` is not available.


        Returns
        -------
        histogram : histo.Histo
            The reference histogram.
        """
        self._loadRefData()
        return self._refdata[histopath]


    def getRefData(self):
        """Get the dictionary of all loaded reference histograms, indexed
        by histogram path.

        Returns
        -------
        refhistos : dict(path => histo.Histo)
            The reference histograms.
        """
        self._loadRefData()
        return self._refdata


    def setMCPath(self, path, datatype="sample", checkAIDA=True):
        """Add MC data of given type rooted at `path`.

        Parameters
        ----------
        path : str
            Base directory of the MC data.
        datatype : str, optional
            The type identifier of the MC data, e.g. `'sample'` or
            `'linescan'`. The default is `'sample'`.

        Raises
        ------
        IOTestFailed
            If `path` is not a readable directory.
        """
        io.testReadDir(path)
        if self._mcdata.has_key(datatype):
            del self._mcdata[datatype]
        self._mcdata[datatype] = MCData(path, checkAIDA=checkAIDA)


    def addMCData(self, mcdata, datatype):
        """Add MC data of given data type.

        Add a MC data interface to the internal storage dictionary. If an
        entry for `datatype` already exists it will be overwritten!

        Parameters
        ----------
        mcdata : MCData (or subclass)
            The MC data to add.
        datatype : str
            The MC data type, e.g. `'sample'` or `'scan'` or `'tunes'`.

        Raises
        ------
        TypeError
            If mcdata has wrong type.
        """
        if not isinstance(mcdata, MCData):
            raise TypeError("Argument mcdata must be a MCData (or subclass)"
                            " instance. But type is %s" % (type(mcdata)))
        self._mcdata[datatype] = mcdata

    def getMCData(self, datatype="sample", checkAIDA=True):
        """Get MC data of the given type.

        Parameters
        ----------
        datatype : str, optional
            The MC data type, e.g. `'sample'` or `'scan'` (default is
            `'sample'`.

        Raises
        ------
        DataProxyError
            If no MC data of type `datatype` is available.

        Returns
        -------
        mcdata : MCData
            The `datatype` MC data.
        """
        if not self._mcdata.has_key(datatype):
            raise DataProxyError("MC data type '%s' not set!" % (datatype))
        return self._mcdata[datatype]


    def setIpolPath(self, path):
        io.testReadDir(path)
        self._ipolpath = path

    def getIpolPath(self):
        if self._ipolpath is None:
            raise DataProxyError("No interpolation base path set!")
        return self._ipolpath

    ipolpath = property(getIpolPath, setIpolPath,
                        doc="base directory for InterpolationSet files")


    def getIpolFilePath(self, ipolcls, runs):
        """Return the canonical path for an interpolation pickle.

        Parameters
        ----------
        ipolcls : class
            The interpolation method class. Must have a 'method' attribute.
        runs : list, str
            The runs that are used as anchor points for the interpolation.
            Can be a list of strings or a single string of colon-separated
            run keys.
        """
        if type(runs) in [list, tuple]:
            runs = ":".join(sorted(runs))
        return os.path.join(self.ipolpath,
                            "profipol_%s_%s.pkl" % (ipolcls.method,
                                                    md5(runs).hexdigest()))


    # TODO: raise meaningful error
    def getInterpolationSet(self, ipolcls, runs):
        """Get an InterpolationSet.

        This is loaded from disk on-the-fly.

        Parameters
        ----------
        ipolcls : class
            The interpolation method class.
        runs : list, str
            The runs that are used as anchor points for the interpolation.
            Can be a list of strings or a single string of colon-separated
            run keys.
        """
        path = self.getIpolFilePath(ipolcls, runs)
        return InterpolationSet.mkFromPickle(path)


    # TODO: is this necessary?
    # TODO: filter for max info ipol
    def listInterpolationSets(self):
        """Return a list of *all* InterpolationSets in the ipol directory.

        Raises
        ------
        DataProxyError
            If `self.ipolpath` is not set.
        """
        l = []
        for f in os.listdir(self.ipolpath):
            if not f.endswith(".pkl"):
                continue
            p = os.path.join(self.ipolpath, f)
            l.append(InterpolationSet.mkFromPickle(p))
        return l


    # TODO: add method that gets a ipolcls and a list of runcombs and
    # checks, that all files exist


    def getTuneData(self, withref=True, withmc=None,
                    useipol=None, useruns=None, useobs=None):
        """Return a TuneData object with the desired data.

        The kind of data that is given to TuneData can be steered via the
        (optional) flags. Depending on the kind of computation (calculating
        interpolation coefficients/minimising/...) different kinds of data
        must be turned on.

        This is the central data preparation function.

        Parameters
        ----------
        withref : bool, optional
            Equip `TuneData` with reference data (the default is `True`).
        withmc : {str, `None`}, optional
            If not `None`, the type of MC data that is stored in the
            `TuneData`, e.g. `'sample'`. The default is `None`.
        useipol : {interpolation_class, `None`}, optional
            If not `None`, the interpolation method class used for the
            per-bin interpolations. Only the
            :attr:`~BinInterpolation.method` attribute is important because
            this is used to construct the file name of the pickle file.
        useruns : {list of str, `None`}, optional
            The run numbers used for interpolation. Can be `None` if
            `withmc` is given. In this case, all available MC runs are used.
        useobs : {list of str, `None`}, optional
            The observables to use. Can be `None` if `withmc` is given. In
            this case, all available observables in the MC data are used.
        """
        return TuneData(self, withref, withmc, useipol, useruns, useobs)


    @staticmethod
    def getBinID(histo, ibin):
        """Get a canonical bin id of the form Analysis/HistoID:BinIdx .

        Parameters
        ----------
        histo : Histo
            Histogram.
        ibin : int
            Bin index.
        """
        return "%s:%i" % (histo.histopath, ibin)


    @staticmethod
    def getBinIndex(binid):
        """Get the bin index from a canonical bin ID.

        Parameters
        ----------
        binid : str
            The bin ID.
        Returns
        -------
        index : int
        """
        return DataProxy.splitBinID(binid)[1]

    @staticmethod
    def splitBinID(binid):
        """Split a bin ID in observable and bin index.

        Parameters
        ----------
        binid : str
            The bin ID.
        Returns
        -------
        observable : str
        index : int
        """
        obs, idx = binid.split(":")
        return obs, int(idx)



class RivetDataProxy(DataProxy):
    """Data proxy that loads the reference data from the files distributed
    with rivet.

    """
    def __init__(self):
        import rivet
        super(RivetDataProxy, self).__init__()

        self._refdirs = rivet.getAnalysisRefPaths()


    def getRefHisto(self, histopath):
        """Get a reference histogram.

        Parameters
        ----------
        histopath : str
            A histogram path of the form '/Analysis/HistoID'.

        Raises
        ------
        KeyError
            If `histopath` is not available.

        Returns
        -------
        histogram : histo.Histo
            The reference histogram.
        """
        if self._refdata is None or not self._refdata.has_key(histopath):
            self._loadRefData(histopath)
        return self._refdata[histopath]


    def _loadRefData(self, histopath):
        ana = histopath[1:].split("/")[0]

        rp = None

        try:
            rd = itertools.chain([self.refpath], self._refdirs)
            logging.debug("Using %s and %s for ref data search." % (
                            self.refpath, self._refdirs))

        except DataProxyError:
            rd = self._refdirs
            logging.debug("refpath not set. Using only %s for ref data"
                          "  search." % self._refdirs)

        for rd in self._refdirs:
            rp = os.path.join(rd, ana + ".aida")
            try:
                io.testReadFile(rp)
                logging.debug("Found ref data file for analysis %s: %s" % (
                                ana, rp))
                break
            except IOTestFailed:
                rp = None

        if rp is None:
            # No file matching the analysis name found. (Re-)Load all ref
            # data in refpath.
            super(RivetDataProxy, self)._loadRefData(True)
            logging.debug("(Re-)Loaded reference data from %s" % (self.refpath))

        else:
            if self._refdata is None:
                self._refdata = dict()

            logging.debug("Loading histograms from %s" % (rp))
            self._refdata.update(histo.Histo.fromAIDA(rp))


    def getRefData(self):
        if self._refdata is None:
            raise DataProxyError("No reference data loaded!")
        return self._refdata


    @classmethod
    def mkFromCLOptions(cls, opts, checkAIDA=True):
        """Build DataProxy from CL-options that were prepared with
        addDataCLOptions.

        Only the paths are set in the returned DataProxy for which the
        parser has an according option.

        See Also
        --------
        addDataCLOptions : Add a data location command-line option group to
            an `OptionParser`.
        getPathsFromCLOptions : Get a `dict` of data-location paths from
            command line options.
        """
        proxy = cls()
        paths = cls.getPathsFromCLOptions(opts)

        if paths["ref"] is not None:
            try:
                proxy.refpath = paths["ref"]
            except IOTestFailed, err:
                logging.debug("Reference directory does not exist: %s (this"
                              " is not fatal for RivetDataProxy)" % (err))
        if paths["ipol"] is not None:
            proxy.ipolpath = paths["ipol"]

        if paths["mc"] is not None:
            proxy.setMCPath(paths["mc"], "sample", checkAIDA=checkAIDA)
        if paths["scan"] is not None:
            proxy.setMCPath(paths["scan"], "linescan", checkAIDA=checkAIDA)

        return proxy

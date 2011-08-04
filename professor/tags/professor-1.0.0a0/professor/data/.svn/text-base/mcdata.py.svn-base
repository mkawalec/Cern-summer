import os

from professor import histo

from professor.tools.parameter import readParameterFile
from professor.tools.errors import ArgumentError, DataProxyError
import professor.tools.log as logging


class MCData(object):
    """Interface for a directory with MC generated data.

    `MCData` abstracts a directory with MC generated data with a layout
    following::

        base/run1
             run2
             ...

    Data is read from the filesystem only if necesarry.
    """

    def __init__(self, base):
        self.basepath = base

        # {run => parameter dict}
        self._params = dict()

        # {run => scan parameter}
        self._scanparam = dict()

        # {run => {histoname => histo}}
        self._histos = dict()

        self.availableruns = tuple(sorted(filter(self.isValidRunDir,
                                          os.listdir(self.basepath))))
        if not self.availableruns:
            raise DataProxyError("No valid runs found in '%s'!" % (
                                 self.basepath))

    # TODO: make requirement for out.aida option optional
    def isValidRunDir(self, runid=None, runpath=None):
        """Check that the run directory is valid.

        Checks for an ``out.aida`` file and an ``used_params`` file.

        The run can be specified by `runid` or `runpath`.

        Parameters
        ----------
        runid : str
            The ID of the run, i.e. the subdirectory name.
        runpath : str
            The full path to the rundirectory. This is used in the
            ManualMCData class.
        """
        if runid is not None and runpath is not None:
            raise ArgumentError("runid and runpath given: Don't know what to do!")
        if runid is None and runpath is None:
            raise ArgumentError("runid and runpath not given!")

        if runid is not None:
            path = os.path.join(self.basepath, runid)
        else:
            path = runpath

        if not os.path.isdir(path):
            return False

        temp = os.path.join(path, "used_params")
        if not os.path.isfile(temp):
            return False

        temp = os.path.join(path, "out.aida")
        if not os.path.isfile(temp):
            return False

        return True


    ## TODO: add switch to ignore used_params files
    ## TODO: rm AIDA-specifics
    def loadRun(self, run, loadhistos=True):
        """Load data for a run.

        Parameters
        ----------
        run : str
            The run identifier to load.
        loadhistos : bool, optional
            Turn loading histogram data on (default) or off.
        """
        ## Load run only if necessary
        if ((not loadhistos or self._histos.has_key(run)) and
             self._params.has_key(run)):
            return

        d = os.path.join(self.basepath, run)
        if not os.path.isdir(d):
            raise DataProxyError("Run '%s' not found in base directory"
                                 " '%s'!" % (run, self.basepath))

        temp = os.path.join(d, "used_params")
        if not os.path.isfile(temp):
            raise DataProxyError("Run '%s': no file 'used_params'"
                                 " found!" % (run))
        pardict = readParameterFile(temp)
        ## Take care of special PROF_SCAN_PARAM
        if pardict.has_key("PROF_SCAN_PARAM"):
            self._scanparam[run] = pardict["PROF_SCAN_PARAM"]
            del pardict["PROF_SCAN_PARAM"]
        self._params[run] = pardict

        if loadhistos:
            temp = os.path.join(d, "out.aida")
            if not os.path.isfile(temp):
                raise DataProxyError("Run '%s': no file 'out.aida'"
                                     " found!" % (run))
            histodict = histo.Histo.fromAIDA(temp)
            self._histos[run] = histodict


    # TODO: try threading to speed things up => To no avail, blast you GIL!
    def loadAllRuns(self, loadhistos=True):
        """Load the data for all available runs.

        Parameters
        ----------
        loadhistos : bool, optional
            Turn loading histogram data on (default) or off.

        See Also
        --------
        loadRun : Load a single run.
        loadAllThreaded : Load all runs threaded, useful if IO lags are
            huge, e.g. with network file storage.
        """
        for run in self.availableruns:
            try:
                self.loadRun(run, loadhistos=loadhistos)
            except DataProxyError:
                logging.error("Could not load data from run directory"
                              " '%s'!" % (run))

    def loadAllThreaded(self, loadhistos=True, numthreads=8):
        """Load the data for all available runs (multi-threaded).

        This is only useful if IO lags are huge. Otherwise the Python thread
        overhead makes this more time-consuming than `loadAll`.

        Parameters
        ----------
        loadhistos : bool, optional
            Turn loading histogram data on (default) or off.
        numthreads : int, optional
            Number of threads (default: 8).

        See Also
        --------
        loadRun : Load a single run.
        loadAll : Load all runs sequentially.
        """
        import threading
        import Queue
        # Code copied from Python documentation.
        # I think the threads idle after all runs were read. But I'm not
        # sure if it's a problem...
        q = Queue.Queue()
        def worker(idx):
            logging.debug("Starting IO worker thread")
            while True:
                # print "T%i: Trying to get a run..." % (idx)
                run = q.get()
                # print "T%i: loading run %s" % (idx, run)
                self.loadRun(run, loadhistos=loadhistos)
                # print "T%i: loaded  run %s" % (idx, run)
                # time.sleep(1)
                q.task_done()
        # fill Queue and start the IO
        for run in self.availableruns:
            q.put(run)
            # print "added run", run, "to queue"

        # create #(availableruns) worker threads
        for i in range(numthreads):
            t = threading.Thread(target=worker, args=(i,))
            t.setDaemon(True)
            t.start()
        # print "waiting for threads"
        q.join()

    def getRunHistos(self, run):
        """Return the {obsname => Histo} dict for given run.

        Returns
        -------
        histograms : dict
            Dictionary that map histogram paths to `Histo` instances.
        """
        self.loadRun(run)
        return self._histos[run]

    def getRunParams(self, run):
        """Get the run parameters.

        Parameters
        ----------
        run : str
            Run ID.

        Returns
        -------
        parametes : dict
            Dictionary that maps parameter names to values.
        """
        self.loadRun(run, loadhistos=False)
        return self._params[run]

    def getParameterBounds(self, runs=None):
        """Get the extremal parameter bounds of runs."""
        # load parameter files
        if not runs:
            runs = self.availableruns
        bounds = {}
        init = self.getRunParams(runs[0])
        for name, value in init.items():
            bounds[name] = [value, value]

        for run in runs[1:]:
            for name, value in self.getRunParams(run).items():
                bounds[name][0] = min(bounds[name][0], value)
                bounds[name][1] = max(bounds[name][1], value)
        return bounds

    def getParameterNames(self):
        return self.getRunParams(self.availableruns[0]).keys()

    def getScanParam(self, run):
        self.loadRun(run)
        return self._scanparam[run]

    def getAvailableObservables(self):
        """Get a sorted list with the available observables.

        The observables are taken from the first available MC run data.
        """
        if len(self._histos) == 0:
            self.loadRun(self.availableruns[0])
        return sorted(self._histos.values()[0].keys())

    availablehistos = property(getAvailableObservables,
                               doc="The available histogram names (sorted).")
    loadedruns = property(lambda s: sorted(s._histos.keys()),
                          doc="The currently loaded run numbers (sorted).")


class ManualMCData(MCData):
    def __init__(self, runpathmap=None):

        # {run => parameter dict}
        self._params = dict()

        # {run => scan parameter}
        self._scanparam = dict()

        # {run => {histoname => histo}}
        self._histos = dict()

        self._runpaths = {}
        if runpathmap is not None:
            for runid, path in runpathmap.items():
                self.addRunPath(runid, path)

    # overwrite MCData.availableruns variable
    availableruns = property(lambda self: self._runpaths.keys())

    def addRunPath(self, runid, path):
        if not self.isValidRunDir(runpath = path):
            raise DataProxyError("Path '%s' is not a valid MC run"
                                 " directory!" % (path))
        if self._runpaths.has_key(runid):
            raise DataProxyError("MC run '%s' already exists!" % (runid))
        self._runpaths[runid] = path

    def loadRun(self, runid, loadhistos=True):
        """Load data for `run`."""
        ## Load run only if necessary
        if ((not loadhistos or self._histos.has_key(runid)) and
             self._params.has_key(runid)):
            return

        d = self._runpaths[runid]

        if not os.path.isdir(d):
            raise DataProxyError("Run '%s' not found in base directory"
                                 " '%s'!" % (runid, self.basepath))

        temp = os.path.join(d, "used_params")
        if not os.path.isfile(temp):
            raise DataProxyError("Run '%s': no file 'used_params'"
                                 " found!" % (runid))
        pardict = readParameterFile(temp)
        ## Take care of special PROF_SCAN_PARAM
        if pardict.has_key("PROF_SCAN_PARAM"):
            self._scanparam[runid] = pardict["PROF_SCAN_PARAM"]
            del pardict["PROF_SCAN_PARAM"]
        self._params[runid] = pardict

        if loadhistos:
            temp = os.path.join(d, "out.aida")
            if not os.path.isfile(temp):
                raise DataProxyError("Run '%s': no file 'out.aida'"
                                     " found!" % (runid))
            histodict = histo.Histo.fromAIDA(temp)
            self._histos[runid] = histodict



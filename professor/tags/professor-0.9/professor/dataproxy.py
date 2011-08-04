import os
import logging
import itertools
import threading
import Queue
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

from professor import lighthisto
from professor.tools.elementtree import ET
from professor.tools.parameter import readParameterFile
from professor.interpolation import InterpolationSet
from professor.interpolation.interpolationset import InterpolationSet


class DataProxyError(Exception):
    pass


class MCData(object):
    "Abstraction of directory with MC generated data (sample or line scan)."
    def __init__(self, path):
        self.basepath = path

        # {run => parameter dict}
        self._params = dict()

        # {run => scan parameter}
        self._scanparam = dict()

        # {run => {histoname => histo}}
        self._histos = dict()

        self.availableruns = tuple(sorted(filter(self.isValidRunDir,
                                          os.listdir(self.basepath))))
        if not self.availableruns:
            raise DataProxyError("No valid runs found in '%s'!" % (self.basepath))

    def isValidRunDir(self, run):
        path = os.path.join(self.basepath, run)
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
        ## Load run only if necessary
        if ((not loadhistos or self._histos.has_key(run)) and
             self._params.has_key(run)):
            print run, "already loaded!"
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
            self._histos[run] = self.readAIDA(temp)


    ## TODO: Move AIDA-specifics elsewhere
    @staticmethod
    def readAIDA(path):
        """Get {histo path=>Histo} dict for AIDA file at path."""
        runhistos = dict()
        tree = ET.parse(path)
        for dps in tree.findall("dataPointSet"):
            dpsname = dps.get("path") + "/" + dps.get("name")
            runhistos[dpsname] = lighthisto.Histo.fromDPS(dps)
        return runhistos


    # TODO: try threading to speed things up
    def loadAllRuns(self):
        for run in self.availableruns:
            run = os.path.join(self.basepath, run)
            try:
                self.loadRun(run)
            except DataProxyError, err:
                logging.error("Could not load data from run directory"
                              " '%s'!" % (run))


    def loadAllThreaded(self, numthreads=8):
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
                self.loadRun(run)
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
        """Return the obsname-Histo dict for given run."""
        self.loadRun(run)
        return self._histos[run]

    def getRunParams(self, run):
        self.loadRun(run, loadhistos=False)
        return self._params[run]

    def getParameterBounds(self, runs):
        """Get the parameter bounds of runs."""
        # load parameter files
        bounds = {}
        init = self.getRunParams(runs[0])
        for name, value in init.items():
            bounds[name] = (value, value)

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
        """Get a list with the available observables."""
        if len(self._histos) == 0:
            self.loadRun(self.availableruns[0])
        return sorted(self._histos.values()[0].keys())

    availablehistos = property(getAvailableObservables,
                               doc="the available histogram names")
    loadedruns = property(lambda s: sorted(s._histos.keys()),
                          doc="the currently loaded run numbers")


class DataProxy(object):
    """
    MC data
    =======
    Different types of MC data can be stored. The MC data is stored in a
    dict {type-ID => MCData} . type-IDs are for example "sample" or "scan".

    ideas:
    ======
    * set paths via properties (clear previously loaded data)
    * load data on-the-fly via properties
    """
    def __init__(self):
        self._refpath = None
        self._ipolpath = None
        self._mcpaths = dict()

        self._refdata = None
        # { data type => MCData }
        self._mcdata = dict()
        # do not cache InterpolationSets this is probably too memory
        # intensive
        # self._ipoldata = None

    def setDataPath(self, path):
        temp = os.path.join(path, "ref")
        if os.path.isdir(temp):
            self.setRefPath(temp)

        temp = os.path.join(path, "mc")
        if os.path.isdir(temp):
            self.setMCPath(temp, "sample")

        temp = os.path.join(path, "ipol")
        if os.path.isdir(temp):
            self.setIpolPath(tmp)


    def setRefPath(self, path):
        self._refdata = None
        self._refpath = path

    def getRefPath(self):
        if self._refpath is None:
            raise DataProxyError("No reference data path set!")
        return self._refpath

    refpath = property(getRefPath, setRefPath,
                       doc="base directory for reference data .aida files")

    def loadRefData(self):
        """Load all reference data if not done before."""
        if self._refdata is not None:
            return

        self._refdata = dict()

        for reffile in os.listdir(self.refpath):
            ## TODO: generalise file type
            if not reffile.endswith(".aida"):
                continue
            reffilepath = os.path.join(self.refpath, reffile)
            if not os.path.isfile(reffilepath):
                logging.warn("Could not read reference file: " + reffilepath)
            tree = ET.parse(reffilepath)
            for dps in tree.findall("dataPointSet"):
                dpsname = os.path.join(dps.get("path"), dps.get("name"))
                if dpsname.startswith("/REF"):
                    dpsname = dpsname[4:]
                self._refdata[dpsname] = lighthisto.Histo.fromDPS(dps)

    def getRefHisto(self, histoname):
        self.loadRefData()
        return self._refdata[histoname]


    def setMCPath(self, path, datatype="sample"):
        """
        data type  -- the type of MC data (e.g. "sample" or "linescan")
        """
        if self._mcdata.has_key(datatype):
            del self._mcdata[datatype]
        self._mcdata[datatype] = MCData(path)

    def getMCData(self, datatype):
        if not self._mcdata.has_key(datatype):
            raise DataProxyError("MC data type '%s' not set!" % (datatype))
        return self._mcdata[datatype]


    def setIpolPath(self, path):
        self._ipolpath = path

    def getIpolPath(self):
        if self._ipolpath is None:
            raise DataProxyError("No interpolation base path set!")
        return self._ipolpath

    ipolpath = property(getIpolPath, setIpolPath,
                        doc="base directory for InterpolationSet files")

    def getIpolFilePath(self, ipolcls, runs):
        """Return the canonical path for an interpolation pickle.

        ipolcls -- The interpolation method class.
        runs    -- The runs that are used. Can be a list of strings or the usual
                   colon separated sorted list of run keys.
        """
        if type(runs) == list:
            runs = ":".join(sorted(runs))
        return os.path.join(self.ipolpath, "profipol_%s_%s.pkl" % (ipolcls.method,
                            md5(runs).hexdigest()))

    ## TODO: Need to know ipol class?
    def getInterpolationSet(self, ipolcls, runs):
        """Get an InterpolationSet.

        This is loaded from disk on-the-fly.
        """
        path = self.getIpolPath(ipolcls, runs)
        return InterpolationSet.fromPickle(ipolpath)

    def listInterpolationSets(self):
        """Return a list of *all* InterpolationSets in the ipol directory."""
        l = []
        for f in os.listdir(self.ipolpath):
            if not f.endswith(".pkl"):
                continue
            p = os.path.join(self.ipolpath, f)
            l.append(InterpolationSet.fromPickle(p))
        return l


    def getTuneData(self, withref=True, withmc=False, useipol=None,
                    useruns=None, useobs=None):
        """Return a TuneData object with the desired data.

        The kind of data that is given to TuneData can be steered via the
        (optional) flags. Depending on the kind of computation (calculating
        interpolation coefficients/minimising/...) different kinds of data
        must be turned on.

        This is the central data preparation function.

        withref  -- equip TuneData with reference data
        withmc   -- equip TuneData with mc data data
        useipol  -- the interpolation method given by the class or
                    None (=> no interpolation data is loaded)
        useruns  -- list of run numbers to use or
                    None (=> use all valid run directories from sample mc)
        useobs   -- list of observables to use or
                    None (=> use all observables from sample mc)
        """
        if useruns is None:
            useruns = self.getMCData("sample").availableruns
        else:
            useruns = sorted(use_runnums)

        if useobs is None:
            useobs = self.getMCData("sample").availablehistos
        else:
            useobs = sorted(useobs)

        refbins = None
        mcbins = None
        binipols = None

        if useipol is not None:
            binipols = self.getInterpolationSet(useipol, useruns)

        if withref:
            refbins = dict()
            for obs in useobs:
                hist = self.getRefHisto(obs)
                for i in range(hist.numBins()):
                    binid = self.getBinID(hist, i)
                    refbins[binid] = hist.getBin(i)

        if withmc:
            mcbins = dict()
            mcdata = self.getMCData("sample")
            for run in useruns:
                mcdata.loadRun(run)
            for obs in useobs:
                dummyhisto = mcdata.getRunHistos(useruns[0])[obs]
                for i in range(dummyhisto.numBins()):
                    binid = self.getBinID(dummyhisto, i)
                    bindict = dict()
                    for run in useruns:
                        bindict[run] = mcdata.getRunHistos(run)[obs].getBin(i)
                    mcbins[binid] = bindict

        return TuneData(refbins, mcbins, binipols)

    @staticmethod
    def getBinID(histo, ibin):
        return "%s:%i"%(histo.histopath, ibin)


class TuneData(dict):
    """Container for data for one choice of runs."""
    def __init__(self, dataproxy, withref=True, withmc=False, useipol=None,
                    useruns=None, useobs=None):
        """Return a TuneData object with the desired data.

        The kind of data that is given to TuneData can be steered via the
        (optional) flags. Depending on the kind of computation (calculating
        interpolation coefficients/minimising/...) different kinds of data
        must be turned on.

        This is the central data preparation function.

        withref  -- equip TuneData with reference data
        withmc   -- equip TuneData with mc data data
        useipol  -- the interpolation method given by the class or
                    None (=> no interpolation data is loaded)
        useruns  -- list of run numbers to use or
                    None (=> use all valid run directories from sample mc)
        useobs   -- list of observables to use or
                    None (=> use all observables from sample mc)
        """
        if useruns is None:
            useruns = dataproxy.getMCData("sample").availableruns
        else:
            useruns = sorted(use_runnums)
        self.runnums = useruns

        if useobs is None:
            useobs = dataproxy.getMCData("sample").availablehistos
        else:
            useobs = sorted(useobs)

        self.hasref = False
        self.hasmc = False
        self.hasipol = False

        refbins = dict()
        mcbins = dict()
        binipols = dict()
        # binids is a helper for the final loop where we fill this TuneData
        # dict structure
        binids = None

        if withref:
            self.hasref = True
            for obs in useobs:
                hist = dataproxy.getRefHisto(obs)
                for i in range(hist.numBins()):
                    binid = dataproxy.getBinID(hist, i)
                    refbins[binid] = hist.getBin(i)
            binids = refbins.iterkeys()

        if withmc:
            self.hasmc = True
            mcdata = dataproxy.getMCData("sample")
            for run in useruns:
                mcdata.loadRun(run)
            for obs in useobs:
                dummyhisto = mcdata.getRunHistos(useruns[0])[obs]
                for i in range(dummyhisto.numBins()):
                    binid = dataproxy.getBinID(dummyhisto, i)
                    bindict = dict()
                    for run in useruns:
                        bindict[run] = mcdata.getRunHistos(run)[obs].getBin(i)
                    mcbins[binid] = bindict
            if binids is None:
                binids = mcbins.iterkeys()

        # Load interpolation and get a Scaler:
        # Use Scaler from interpolations by default and fall back to a
        # scaler based on MC run parameters.
        if useipol is not None:
            self.hasipol = True
            binipols = dataproxy.getInterpolationSet(useipol, useruns)
            self.scaler = binipols.scaler
            if binids is None:
                binids = binipols.iterkeys()
        else:
            # short cut for MC data
            mcd = dataproxy.getMCData("sample")
            self.scaler = Scaler(mcd.getParameterBounds(useruns))

        # Fill the dict structure with BinProps. Use get to have None in
        # place where we didn't load the data.
        for binid in binids:
            self[binid] = BinProps(refbins.get(binid),
                                   mcbins.get(binid),
                                   ipolset.get(binid))

    def numParams(self):
        return self.scaler.dim()

    def getBinProps(self, obs):
        """List of all BinProps for observable `obs'."""
        return [bp for bid, bp in self.iteritems() if bid.startswith(obs)]

    def filteredValues(self):
        """Return an iterator with the bin properties without vetoed or
        zero-weighted bins.
        """
        return itertools.ifilterfalse(lambda bp: bp.veto or bp.weight <= 0.0,
                                      self.itervalues())

    def applyObservableWeightDict(self, weights):
        """
        Make sure the keys fit the observable names in the bin ID in this
        instance! Weights has to be a dict with observable names as keys
        and 3-tuples as values: weights[observ] = (weight, low, high)
        where weight is the actual weight and low and high are x-values
        that define an allowed region; bincenters not in this range will
        result in a veto of the according binprop.
        """
        for binid, binprop in self.iteritems():
            obsname = binid.split(':')[0]
            bincenter = binprop.getBinCenter()
            w, low, high = weights[obsname]
            logging.debug("weighting bin %s with %g"%(binid, w))
            binprop.weight = w
            if low and high:
                if bincenter < low or bincenter > high:
                    binprop.veto = True
                    logging.debug("vetoing bin %s (x=%.3f)"%(binid, bincenter))
            elif low and not high:
                if bincenter < low:
                    binprop.veto = True
                    logging.debug("vetoing bin %s (x=%.3f)"%(binid, bincenter))
            elif not low and high:
                if bincenter > high:
                    binprop.veto = True
                    logging.debug("vetoing bin %s (x=%.3f)"%(binid, bincenter))

    def getObservables(self):
        obs = map(lambda s: s.split(":")[0], self.keys())

        # make the list unique
        obs = set(obs)

        return list(obs)

    observables = property(getObservables)

    def getInterpolationHisto(self, observable, params):
        """Interpolation-prediction for `observable' at `params'"""
        if observable not in self.observables:
            raise ValueError("Observable '%s' not available!" % (observable))

        if isinstance(parampoint, MinimizationResult):
            pointasarray = parampoint.parscaled
        elif isinstance(parampoint, ParameterPoint):
            pointasarray = parampoint.getScaled()
        elif type(parampoint) == dict:
            pointasarray = ParameterPoint(parampoint, self.scaler).getScaled()
        else:
            raise TypeError("Argument parampoint must be of types"
                            " MinimizationResult, ParameterPoint, or dict!")

        h = lighthist.Histo()
        binprobs = self.getBinProps(observable)
        binprobs.sort()
        for i in binprobs:
            h.addBin(i.ipol.getBin(pointasarray))
        h.name = observable
        h.title = title
        return h

    def vetoEmptyErrors(self):
        """Veto bins with zero reference error."""
        for bp in self.itervalues():
            # if bp.refbin.getYErr() == 0 or bp.refbin.getYVal() == 0:
            if bp.refbin.getYErr() <= 0.0:
                bp.veto = True


class BinProps(object):
    """Container for all data related to a bin needed to do a minimisation.

    A container for all the variants on a distribution bin: its weight, its
    reference value and errors, a collection of its simulated equivalents from a
    set of MC runs, and an interpolation function for that bin, based on
    optimising the fit to a sampling of MC points in the parameter space.

    At the moment the following is stored:
     - refbin: a Bin instance with the reference bin
     - mcdict: a run number -> MC Bin dictionary
     - ipol: a QuadraticBinInterpolation instance
     - veto: a flag for vetoing this bin in the GoF calculation
     - weight/sqrtweight: weights for the GoF calculation
    """
    def __init__(self, refbin, mcdict, ipol):
        self.refbin = refbin
        self.mcdict = mcdict
        self.ipol = ipol

        self.veto = False
        self.__weight = 1.0
        self.__sqrtweight = 1.0

    def __cmp__(self, other):
        """ This allows for sorting BinProps by binids """
        return cmp(int(self.binid.split(':')[-1]),
                int(other.binid.split(':')[-1]))

    def setWeight(self, w):
        self.__weight = w
        self.__sqrtweight = numpy.sqrt(w)

    def setSqrtWeight(self, sw):
        self.__weight = sw**2
        self.__sqrtweight = sw

    def getBinCenter(self):
        return self.refbin.getBinCenter()

    weight = property(lambda s: s.__weight, setWeight)
    sqrtweight = property(lambda s: s.__sqrtweight, setSqrtWeight)
    binid = property(lambda s: s.ipol.binid)


#############################

## GoF calculators


## TODO: remove inheritance from list
## TODO: make BaseGoF a pure interface and add BaseChi2
class BaseGoF(list):
    """Interface definition of GoF calculators and simple chi2/Ndf GoF
    calculator.

    Take this as documenting by example ;)
    """
    def __init__(self, tunedata, params, scaled=False):
        if type(params) == dict:
            self.params = ParameterPoint(params, tunedata.scaler, scaled)
        elif type(params) == list:
            self.params = ParameterPoint.fromList(params, tunedata.scaler, scaled)
        else:
            TypeError("Unsupported type for argument `params': '%s'!" % (type(params)))

        self.usereferror = True
        self.usesimerror = True

        for bp in tunedata.filteredValues():
            ref = bp.refbin
            sim = bp.ipol.getBin(self.params.getScaled())
            self.append((ref, sim, bp.weight))

    def calcGoF(self):
        return self.calcChi2()/self.calcNdof()

    # ** end of interface ;) **
    def calcChi2(self):
        re = self.usereferror
        se = self.usesimerror
        chi2 = 0.0
        for ref, sim, w in self:
            err2 = 0.0
            if re:
                err2 += (ref.getYErr())**2
            if se:
                err2 += (sim.getYErr())**2
            chi2 += w * (ref.getYVal() - sim.getYVal())**2 / err2
        return chi2

    def calcNdof(self):
        sumw = sum(map(operator.itemgetter(2), self))
        return sumw - self.params.dim()


## A more instructive name
SimpleIpolChi2 = BaseGoF


class SimpleMCChi2(SimpleIpolChi2):
    """Chi2 between MC data from `run' and ref data."""
    def __init__(self, tunedata, run):
        self.usereferror = True
        self.usesimerror = True

        for bp in tunedata.filteredValues():
            ref = bp.refbin
            sim = bp.mcdict[run]
            self.append((ref, sim, bp.weight))


class RelativeIpolChi2(SimpleIpolChi2):
    def calcNdof(self):
        return 1.0

    def calcChi2(self):
        relchi2 = 0.0
        for ref, sim, w in self:
            relchi2 += w * (ref.getYVal() - sim.getYVal())**2/ref.getYVal()**2
        return relchi2


class RelativeMCChi2(RelativeIpolChi2):
    def __init__(self, tunedata, run):
        for bp in tunedata.filteredValues():
            ref = bp.refbin
            sim = bp.mcdict[run]
            self.append((ref, sim, bp.weight))

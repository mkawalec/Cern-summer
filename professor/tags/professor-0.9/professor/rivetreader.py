import os, sys, re
import subprocess
import logging
import optparse
# work around python 2.4 on SL 5
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

from professor import lighthisto
from professor import tuningdata

from professor.tools.progressbar import ForLoopProgressBar as flpb
from professor.tools.elementtree import ET
from professor.tools.parameter import readParameterFile
from professor.interpolation import InterpolationSet
from professor.interpolation.interpolationset import InterpolationSet


def addDataCLOptions(parser):
    """Add common data location options to the given parser.

    Use together with getConfiguredData or getDataDirectories.
    """
    group = optparse.OptionGroup(parser, "Data locations")
    group.add_option("--datadir",
            help = "directory containing mc, ref and ipol directories")
    group.add_option("--mcdir",
            help = "directory containing random mode MC runs (default: DATADIR/mc)")
    group.add_option("--refdir",
            help = "directory containing reference runs (default: DATADIR/ref)")
    group.add_option("--scandir",
            help = "directory containing scan mode MC runs (default: DATADIR/scan)")
    group.add_option("--ipoldir",
            help = "directory to store/load interpolation sets (default: DATADIR/ipol)")
    group.add_option("--obsfile",
            dest = "observablefile",
            help = "file with observable names (and optional weights)")
    parser.add_option_group(group)

def getDataDirectories(opts):
    """Return data dirs as dictionary from the given command line opts.
    Check if ref, mc or ipol are given explicitly, otherwise construct
    directories from datadir. If datadir and one of the other directories is
    not given None is returned as value.
    Format is:
        {"ref":refdir, "mc":mcdir, "ipol":ipoldir, "scan":scandir}
    """
    ref = opts.refdir
    mc = opts.mcdir
    ipol = opts.ipoldir
    scan = opts.scandir
    if ref is None:
        if opts.datadir is None:
            ref = None
        else:
            ref = os.path.join(opts.datadir, "ref")
    if mc is None:
        if opts.datadir is None:
            mc = None
        else:
            mc = os.path.join(opts.datadir, "mc")
    if ipol is None:
        if opts.datadir is None:
            ipol = None
        else:
            ipol = os.path.join(opts.datadir, "ipol")
    if scan is None:
        if opts.datadir is None:
            scan = None
        else:
            scan = os.path.join(opts.datadir, "scan")

    return {"ref":ref, "mc":mc, "ipol":ipol, "scan":scan}

def getIpolFilename(ipolcls, runs):
    """Return the canonical file name for an interpolation pickle.

    ipolcls -- The interpolation method class.
    runs    -- The runs that are used. Can be a list of strings or the usual
               colon separated sorted list of run keys.
    """
    # convert to a runskey string
    if type(runs) == list:
        runs = ":".join(sorted(runs))
    return "profipol_%s_%s.pkl" % (ipolcls.method,
            md5(runs).hexdigest())

def readObservableFile(path, gettitles=False):
    """Read an observable file.

    File structure is:

        observable_name  [weight  [# comment]]

    Lines starting with # are regarded as comments.
    """
    try:
        obsfile = open(path, 'r')
    except Exception, e:
        logging.error("Could not open observable file '%s'!"%(path))
        logging.error("re-raising intercepted error...")
        raise e

    weightdict = {}
    linere = re.compile(r"([^# ]+)\s*([-0-9e\.]+)?(?:\s*#\s*(.*)\s*)?")
    for rawline in obsfile:
        # strip leading/trailing white spaces, e.g. newline
        line = rawline.strip()
        if len(line) == 0 or line.startswith('#'):
            continue

        try:
            groups = linere.search(line).groups()
        except Exception, e:
            logging.error("Could not parse line '%s' from observable file '%s'" % (
                line, path))
            raise e

        name = groups[0]

        weight = groups[1]
        if weight is None:
            weight = 1.0
        else:
            weight = float(weight)

        # Look for bin definitions
        low, high = "", ""
        try:
            path, low, high = name.split(":")
        except:
            logging.debug("No bin definition given for  `%s'" % (name))
            path = name
        if low == "":
            low = None
        else:
            low = float(low)
        if high == "":
            high = None
        else:
            high = float(high)

        if gettitles:
            title = groups[2]
            if title is None:
                title = path
            weightdict[path] = (weight, low, high, title)
        else:
            weightdict[path] = (weight, low, high)

    return weightdict

def getHistosInfo(histolist):
    """Get histogram information for all given histograms.

    The return value is a nested dict:
        { histopath => { property => value }}
    """
    logging.debug("getHistosInfo(...): calling rivet-config")
    datadir = subprocess.Popen(["rivet-config", "--datadir"],
                               stdout=subprocess.PIPE).communicate()[0]
    datadir = datadir[:-1]
    info = {}
    analist = set([os.path.split(histopath)[0] for histopath in histolist])
    for a in analist:
        info.update(getSingleAnalysisInfo(a, datadir))
    return info

def getSingleAnalysisInfo(analysis, datadir=None):
    """Get analysis information from Rivet's *.plot files as nested dict.

    The return value is a nested dict:
        { histopath => { property => value }}

    No errors are catched! Possible error classes are:
        IOError if the plot-file isn't found
        OSError if rivet-config isn't found
    """
    if datadir is None:
        datadir = subprocess.Popen(["rivet-config", "--datadir"],
                                   stdout=subprocess.PIPE).communicate()[0]
        datadir = datadir[:-1]
    # Strip leading / from analysis name. Otherwise path.join gets confused.
    if analysis[0] == "/":
        analysis = analysis[1:]

    plotfile = open(os.path.join(datadir, analysis + ".plot"))
    logging.debug("opened .plot file: %s" % (plotfile.name))

    anainfo = {}
    inplotblock = False
    histopath = None
    histoinfo = None
    for line in plotfile:
        line = line.strip()
        if len(line) == 0:
            continue

        if not inplotblock and line.startswith("# BEGIN PLOT"):
            histoinfo = {}
            histopath = line.split()[-1]
            inplotblock = True
        elif inplotblock and line.startswith("# END PLOT"):
            anainfo[histopath] = histoinfo
            inplotblock = False
        elif inplotblock and not line.startswith("#"):
            try:
                name, value = line.split("=", 1)
                # Replace \text by \mathrm because matplotlib cannot handle
                # it.
                histoinfo[name] = value.replace(r"\text", r"\mathrm")
            except ValueError, err:
                logging.warn("Could not parse line '%s': %s" % (line, err))
    return anainfo

def getTitle(dps):
    """ Try to read plot title from dps or .plot file if it exists in
        any $PATH/share/Rivet.
    """
    # This is the histo title, a la "Charged Multiplicity"
    histoname = dps.get("title")
    if histoname == "":
        # This is the analysis name a la /UA5_1989_S1..
        analysis = dps.get("path")
        obspath = os.path.join(analysis, dps.get("name"))
        try:
            histoname = getSingleAnalysisInfo(analysis)[obspath]["Title"]
        except (IOError, ValueError, KeyError, OSError), err:
            logging.warn("Could not get title for histo %s: %s" % (
                         obspath, err))
            histoname = obspath

    return histoname

def getRefHistos(refdir):
    '''Get a dictionary of reference histograms indexed by name.'''

    ## Initialize the return values
    refhistos = {}

    refdir = os.path.abspath(refdir)
    for reffile in os.listdir(refdir):
        if not re.match(r'.*\.aida$', reffile): continue
        refname = re.sub(r'(.*)\.aida$', r'\1', reffile)
        logging.debug("File -> name: " + reffile + " -> " + refname)

        reffilepath = os.path.abspath(os.path.join(refdir, reffile))
        if not os.path.isfile(reffilepath):
            logging.warn("Could not read reference file: " + reffilepath)
            continue

        tree = ET.parse(reffilepath)
        for dps in tree.findall("dataPointSet"):
            ## Get this histogram's path name, stripped of the "/REF" prefix
            dpsname = os.path.join(dps.get("path"), dps.get("name"))
            if dpsname[:4] == "/REF":
                dpsname = dpsname[4:]

            ## Make a histogram and add it to the return dictionary
            refhistos[dpsname] = lighthisto.Histo.fromDPS(dps)
    ## Return collection of ref histos
    return refhistos

def getMCHistosAndParams(mcdir, obslist=None, getparamsonly=False):
    '''Get the generated MC histograms by iterating over all the MC runs
    in the top-level output directory.'''

    ## Initialize the return values
    mcparams, mchistos, titles = {}, {}, {}
    scanparams = {}

    nrofruns = len(os.listdir(mcdir))
    bar = flpb(0, nrofruns, 30, 'reading histos and params ')
    mcdir = os.path.abspath(mcdir)
    for i, run in enumerate(os.listdir(mcdir)):
        bar.update(i)
        mchistos[run] = {}
        runoutdir = os.path.join(mcdir, str(run))
        runoutdir = os.path.abspath(runoutdir)
        if not os.path.isdir(runoutdir):
            continue

        ## allow for both filenames to be recognized
        outhistofile = os.path.join(runoutdir, 'out.aida')
        if not os.path.exists(outhistofile):
            outhistofile = os.path.join(runoutdir, 'histos.aida')

        outparamsfile = os.path.join(runoutdir, 'used_params')
        if not os.access(outhistofile, os.R_OK) and os.access(outparamsfile, os.R_OK) and getparamsonly:
            pass
        elif not os.access(outhistofile, os.R_OK) or not os.access(outparamsfile, os.R_OK):
            logging.warn("Can't read histo or params files for run %s... skipping" % str(run))
            continue

        ## Store the run params and scanparams if a scan param is found
        temp = readParameterFile(outparamsfile)
        if temp.has_key("PROF_SCAN_PARAM"):
            scanparams[str(run)] = temp["PROF_SCAN_PARAM"]
            del temp["PROF_SCAN_PARAM"]

        mcparams[str(run)] = temp

        ## Run over all the histograms in all the papers
        if not getparamsonly:
            tree = ET.parse(outhistofile)
            for dps in tree.findall("dataPointSet"):
                dpsname = dps.get("path") + "/" + dps.get("name")
                ## Make a histogram and add it to the return dictionary
                if obslist is None or (obslist and dpsname in obslist):
                    mchistos[run][dpsname] = lighthisto.Histo.fromDPS(dps)
                    ## read histo-titles
                    if not titles.has_key(dpsname):
                        titles[dpsname] = getTitle(dps)
    return mchistos, mcparams, titles, scanparams

def getIpols(ipoldir):
    """Return a list of interpolation sets."""
    ipollist = []

    ipoldir = os.path.abspath(ipoldir)
    for ipolfile in os.listdir(ipoldir):
        if not ipolfile.endswith(".pkl"):
            continue
        ipolpath = os.path.abspath(os.path.join(ipoldir, ipolfile))
        if not (os.path.isfile(ipolpath) or os.access(ipolpath, os.R_OK)):
            logging.warn("Path '%s' is not a file or could not be"
                          " opened!"%(ipolpath))
            continue
        try:
            ipol = InterpolationSet.fromPickle(ipolpath)
            # set a flag if ipolset was loaded successfully so that no
            # duplicate is stored
            ipol.setWriteFlag()
            ipollist.append(ipol)
        except (SyntaxError, ValueError), e:
            logging.warn("Error during reading of file '%s': %s"%(ipolpath, e))
    return ipollist

def getTuningData(refdir, outdir, ipoldir=None, ipolout=None, getparamsonly=False):
    '''A single command which gets the MC histos, MC parameters
    and the reference histograms all in one TuningData object. More
    convenient than the individual methods, but gives less fine-grained
    control of OS exceptions.'''

    ## Data container return value
    data = tuningdata.TuningData()

    ## Get reference data
    if refdir:
        refhistos = getRefHistos(refdir)
    else:
        refhistos = {}
    # refhistos, titles = getRefHistos(refdir)
    for name, hist in refhistos.iteritems():
        data.setRefHisto(name, hist)
    # data.setTitles(titles)

    ## Get MC histos and params for all the available tunings
    mchistos, mcparams, titles, scanparams = getMCHistosAndParams(outdir,
            getparamsonly=getparamsonly)

    if not getparamsonly:
        data.setTitles(titles)
        for run, histos in mchistos.iteritems():
            for name, hist in histos.iteritems():
                data.setMCHisto(name, run, hist)

    for run, params in mcparams.iteritems():
        data.setParams(run, params)
    for run, scanparam in scanparams.iteritems():
        data.setScanParam(run, scanparam)

    ## Return TuningData object
    return data

def getLimitedTuningData(refdir, outdir, obslist, ipoldir=None, ipolout=None, getparamsonly=False):
    '''A single command which gets the MC histos, MC parameters
    and the reference histograms all in one TuningData object. More
    convenient than the individual methods, but gives less fine-grained
    control of OS exceptions. This function loads the observables stored
    in obslist only'''

    ## Data container return value
    data = tuningdata.TuningData()

    ## Get reference data
    refhistos = getRefHistos(refdir)
    for name, hist in refhistos.iteritems():
        if name in obslist:
            data.setRefHisto(name, hist)

    ## Get MC histos and params for all the available tunings
    mchistos, mcparams, titles, scanparams = getMCHistosAndParams(outdir,
            obslist=obslist, getparamsonly=getparamsonly)

    if not getparamsonly:
        data.setTitles(titles)
        for run, histos in mchistos.iteritems():
            for name, hist in histos.iteritems():
                data.setMCHisto(name, run, hist)

    for run, params in mcparams.iteritems():
        data.setParams(run, params)
    for run, scanparam in scanparams.iteritems():
        data.setScanParam(run, scanparam)

    ## Return TuningData object
    return data

def getConfiguredData(data, mc=None, ref=None, ipol=None, ipolout=None):
    if data is None and (mc is None or ref is None):
        raise ValueError("Either datadir or both mcdir and refdir must be"
                " configured either in the config file or on the command"
                " line")

    if mc is None:
        mc = os.path.join(data, "mc")
    if ref is None:
        ref = os.path.join(data, "ref")
    if ipol is None and data is not None:
        ipol = os.path.join(data, "ipol")
    if ipol is not None and not os.path.isdir(ipol):
        logging.warn("Interpolation directory %s does not exist!" % ipol)
        ipol = None

    logging.info("Loading data files from %s (mc), %s (ref), and"
                 " %s (ipol)" % (mc, ref, ipol))
    return getTuningData(ref, mc, ipol, ipolout)

def getConfiguredScanData(data, scan, ref, ipol, getparamsonly=False):
    if data is None and (scan is None or ref is None):
        raise ValueError("Either datadir or both scandir and refdir must be"
                " configured either in the config file or on the command"
                " line")

    if scan is None:
        scan = os.path.join(data, "scan")
    if ref is None:
        ref = os.path.join(data, "ref")
    if ipol is None and data is not None:
        ipol = os.path.join(data, "ipol")
    if ipol is not None and not os.path.isdir(ipol):
        logging.warn("Interpolation directory %s does not exist!"%(ipol))
        ipol = None

    logging.info("Loading XML files from %s (mc-scan), %s (ref), and"
                 " %s (ipol)"%(scan, ref, ipol))
    return getTuningData(ref, scan, ipol, getparamsonly=getparamsonly)

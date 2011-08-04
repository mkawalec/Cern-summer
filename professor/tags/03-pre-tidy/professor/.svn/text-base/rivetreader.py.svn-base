import os, sys, re
import logging
import optparse
from hashlib import md5

from professor import histo
from professor import tuningdata

from professor.tools.progressbar import ForLoopProgressBar as flpb
from professor.tools.elementtree import ET
from professor.interpolation import InterpolationSet
from professor.interpolation.interpolationset import loadIpol


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
        {"ref":refdir, "mc":mcdir, "ipol":ipoldir}
    """
    ref = opts.refdir
    mc = opts.mcdir
    ipol = opts.ipoldir
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
    return {"ref":ref, "mc":mc, "ipol":ipol}

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

        if gettitles:
            title = groups[2]
            if title is None:
                title = name
            weightdict[name] = (weight, title)
        else:
            weightdict[name] = weight

    return weightdict

def getTitleDict(analist, mcpath=None):
    """Return a {AIDA-path => title} dictionary for the given analyses.

    analist  -- a list with the analyses' AIDA paths
    mcpath  -- the MC root directory, e.g. DATADIR/mc

    TODO:
    * use the new plot info files from rivet-trunk (make mcpath optional
      for that)
    """
    # initialize title dictionary as identitity mapping
    titles = dict(zip(analist, analist))

    # open a MC AIDA file
    if mcpath is not None:
        ls = filter(lambda p: os.path.isdir(os.path.join(mcpath, p)),
                    os.listdir(mcpath))
        aida = None
        for subdir in ls:
            tpath = os.path.join(mcpath, subdir, "out.aida")
            if os.path.exists(tpath):
                logging.debug("getTitleDict: checking for AIDA file %s" % (tpath))
                aida = tpath
                break

        if aida is None:
            logging.warn("No valid mc run directory found in %s" % (mcpath))
            logging.warn("Returning identitity mapping.")
            return titles

        # read in titles from AIDA file
        tree = ET.parse(aida)
        for dps in tree.findall("dataPointSet"):
            aidapath = os.path.join(dps.get("path"), dps.get("name"))
            if aidapath in analist:
                title = dps.get("title")
                # titles[aidapath] = title
                # Replace \text by \mathrm because matplotlib cannot handle
                # it
                titles[aidapath] = title.replace(r"\text", r"\mathrm")

    return titles


def mkHistoFromDPS(dps):
    """Make a mini histo representation from an AIDA dataPointSet tag."""
    myhist = histo.Histo()
    myhist.name = dps.get("name")
    path = dps.get("path")
    if path[:4] == "/REF":
        path = path[4:]
    myhist.path = path
    myhist.title = dps.get("title")
    points = dps.findall("dataPoint")
    numbins = len(points)
    for binnum, point in enumerate(points):
        bin = histo.Bin()
        for d, m in enumerate(point.findall("measurement")):
            val  = float(m.get("value"))
            up = float(m.get("errorPlus"))
            down = float(m.get("errorMinus"))
            if d == 0:
                low  = val - down
                high = val + up
                bin.setXRange(low, high)
            elif d == 1:
                bin.setYVal(val)
                bin.setYErr((up + down)/2.0)
        myhist.addBin(bin)
    return myhist

def getTitle(dps):
    """ Try to read plot title from dps or .plot file if it exists in
        any $PATH/share/Rivet.
    """
    # This is the histo title, a la "Charged Multiplicity"
    histoname = dps.get("title")
    if histoname == "":
        # This is the analysis name a la UA5_1989_S1..
        aidapath = dps.get("path").strip("/")
        # This is the histo name a la d01-x03-y01
        rivetname = dps.get("name")
        #
        histoname = getTitleFromDotPlot(aidapath, rivetname)
    return histoname

def getTitleFromDotPlot(aidapath, rivetname, lookfor="Title="):
    # plotfile to look for
    plotfile = aidapath + ".plot"
    # Search for plotfile in $PATH
    paths = os.environ["PATH"].split(":")
    histoname = ""
    for p in paths:
        rivetdir = "/share/Rivet"
        if os.path.exists(p+rivetdir):
            if plotfile in os.listdir(p+rivetdir):
                histoname = readDotPlot(p+rivetdir+"/"+plotfile, rivetname, lookfor=lookfor)
            else:
                logging.debug("Could not find histo title %s "%rivetname +
                        "in %s- returning empty string!"%plotfile)
    return histoname

def readDotPlot(infofile, obs, lookfor="Title="):
    """ Open .plot file and try to read titles and so on."""
    f=open(infofile, "r")
    L = [line for line in f]
    f.close()
    for num, i in enumerate(L):
        if obs in i:
            for k in xrange(1,4):
                if lookfor in  L[num+k]:
                    return L[num+k].split(lookfor)[-1].replace("\n","")
    return ""

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
            refhistos[dpsname] = mkHistoFromDPS(dps)
    ## Return collection of ref histos
    return refhistos

def getMCHistosAndParams(mcdir, getparamsonly=False):
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

        #if scan:
            #scanparamsfile = os.path.join(runoutdir, 'scan_params')
            #if not os.access(outhistofile, os.R_OK) or not os.access(scanparamsfile, os.R_OK):
                #logging.warn("Can't read histo or scan params files for run %s... skipping" % str(run))
                #continue
        #else:
        outparamsfile = os.path.join(runoutdir, 'used_params')
        if not os.access(outhistofile, os.R_OK) and os.access(outparamsfile, os.R_OK) and getparamsonly:
            pass
        elif not os.access(outhistofile, os.R_OK) or not os.access(outparamsfile, os.R_OK):
            logging.warn("Can't read histo or params files for run %s... skipping" % str(run))
            continue

        #if scan:
            ### Get scan params if they exist
            ### TODO: multiple scan params?
            #if os.access(scanparamsfile, os.R_OK):
                #sfile = open(scanparamsfile, "r")
                #for line in sfile:
                    #line = re.sub(r' +', r' ', line) # collapse spaces
                    #line = re.sub(r'\n', r'', line) # remove newline
                    #if len(line) == 0 or line == " ":
                        #continue
                    #tokens = line.split(" ")
                    #if tokens[0] == "PROF_SCAN_PARAM":
                        ##scanparams[str(run)] = float(sfile.readline().replace(r'\n', ''))
                        #scanparams[str(run)] = float(tokens[1])
                #sfile.close()

        #else:
        ## Store the run params and scanparams if a scan param is found
        pfile = open(outparamsfile, "r")
        temp = {}
        for line in pfile:
            line = re.sub(r' +', r' ', line) # collapse spaces
            line = re.sub(r'\n', r'', line) # remove newline
            if len(line) == 0 or line == " ":
                continue
            tokens = line.split(" ")
            if len(tokens) != 2:
                logging.error("Parameter def %s is invalid" % str(tokens))
            else:
                ## check for scan parameter
                if tokens[0].startswith("PROF_SCAN_PARAM"):
                    scanparams[str(run)] = float(tokens[1])
                else:
                    temp[tokens[0]] = float(tokens[1])
        mcparams[str(run)] = temp
        pfile.close()

        ## Run over all the histograms in all the papers
        if not getparamsonly:
            tree = ET.parse(outhistofile)
            for dps in tree.findall("dataPointSet"):
                dpsname = dps.get("path") + "/" + dps.get("name")
                ## Make a histogram and add it to the return dictionary
                mchistos[run][dpsname] = mkHistoFromDPS(dps)
                ## read histo-titles
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
            ipol = loadIpol(ipolpath)
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
    # if ipoldir is None:
        # data = tuningdata.CachingTuningData()
    # elif ipoldir is not None and ipolout is None:
        # data = tuningdata.WriteBackTuningData(ipoldir)
    # elif ipoldir is not None and ipolout is not None:
        # data = tuningdata.WriteBackTuningData(ipolout)

    ## Get reference data
    refhistos = getRefHistos(refdir)
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

    ## Get the interpolations.
    # if ipoldir is not None:
        # ipollist = getIpols(ipoldir)
        # for ipolset in ipollist:
            # data.setInterpolationSet(ipolset)

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
    # c = Config()
    # data = c.getOption("data source", "datadir")
    # scan = c.getOption("data source", "scandir")
    # ref = c.getOption("data source", "refdir")

    # ipol = c.getOption("data source", "ipoldir")

    if data is None and (scan is None or ref is None):
        raise ValueError("Either datadir or both scandir and refdir must be"
                " configured either in the config file or on the command"
                " line")

    if scan is None:
        scan = os.path.join(data, "mc-scan")
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

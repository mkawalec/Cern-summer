import os, sys, re
import professor
from professor import histo

from professor.tools.config import Config
__logger = Config().getLogger()

# try to load faster but non-standard cElementTree module
try:
    import xml.etree.cElementTree as ET
except ImportError:
    __logger.debug("Could not load module xml.etree.cElementTree,"
                   " so we're on a python <=2.5 system."
                   " Trying to load cElementTree...")
    try:
        import cElementTree as ET
    except ImportError:
        __logger.debug("Could not load module cElementTree: "
                       "using slower xml.etree.ElementTree instead!")
        import xml.etree.ElementTree as ET



def mkHistoFromDPS(dps):
    """Make a mini histo representation from an AIDA dataPointSet tag."""
    myhist = histo.Histo()
    myhist.name = dps.get("name")
    myhist.title = dps.get("title")
    points = dps.findall("dataPoint")
    numbins = len(points)
    for binnum, point in enumerate(points):
        bin = histo.Bin()
        for d, m in enumerate(point.findall("measurement")):
            val  = float(m.get("value"))
            low  = val - float(m.get("errorMinus"))
            high = val + float(m.get("errorPlus"))
            if d == 0:
                bin.setXRange(low, high)
            elif d == 1:
                bin.setYVal(val)
                bin.setYErr((high-low)/2.0)
        myhist.addBin(bin)
    return myhist



def getRefHistos(refdir):
    '''Get a dictionary of reference histograms indexed by name.'''

    ## Initialize the return values
    refhistos = {}

    refdir = os.path.abspath(refdir)
    for reffile in os.listdir(refdir):
        if not re.match(r'.*\.aida$', reffile): continue
        refname = re.sub(r'(.*)\.aida$', r'\1', reffile)
        __logger.debug("File -> name: " + reffile + " -> " + refname)

        reffilepath = os.path.abspath(os.path.join(refdir, reffile))
        if not os.path.isfile(reffilepath):
            __logger.warn("Could not read reference file: " + reffilepath)
            continue

        tree = ET.parse(reffilepath)
        for dps in tree.findall("dataPointSet"):
            ## Get this histogram's path name, stripped of the "/HepData" prefix
            dpsname = os.path.join(dps.get("path"), dps.get("name"))
            if dpsname[:8] == "/HepData":
                dpsname = dpsname[8:]

            ## Make a histogram and add it to the return dictionary
            refhistos[dpsname] = mkHistoFromDPS(dps)
    ## Return collection of ref histos
    return refhistos

def getMCHistosAndParams(mcdir):
    '''Get the generated MC histograms by iterating over all the MC runs
    in the top-level output directory.'''

    ## Initialize the return values
    mcparams, mchistos, titles = {}, {}, {}

    #print os.listdir(mcdir)
    mcdir = os.path.abspath(mcdir)
    for run in os.listdir(mcdir):
        #print run
        mchistos[run] = {}
        runoutdir = os.path.join(mcdir, str(run))
        runoutdir = os.path.abspath(runoutdir)
        if not os.path.isdir(runoutdir):
            continue
        outhistofile = os.path.join(runoutdir, 'out.aida')
        outparamsfile = os.path.join(runoutdir, 'used_params')
        scanparamsfile = os.path.join(runoutdir, 'scan_params')
        if not os.access(outhistofile, os.R_OK) or not os.access(outparamsfile, os.R_OK):
            __logger.warn("Can't read histo or params files for run %s... skipping" % str(run))
            continue

        ## Store the run params
        pfile = open(outparamsfile, "r")
        temp = {}
        for line in pfile:
            line = re.sub(r' +', r' ', line) # collapse spaces
            line = re.sub(r'\n', r'', line) # remove newline
            if len(line) == 0 or line == " ":
                continue
            tokens = line.split(" ")
            if len(tokens) != 2:
                __logger.error("Parameter def %s is invalid" % str(tokens))
            else:
                # mcparams[tokens[0]] = tokens[1]
                temp[tokens[0]] = float(tokens[1])
        mcparams[str(run)] = temp
        pfile.close()

        ## Get scan params if they exist
        ## TODO: clean up this treatment of different param classes
        ## TODO: multiple scan params?
        if os.access(scanparamsfile, os.R_OK):
            sfile = open(scanparamsfile, "r")
            scanparam = float(sfile.readline().replace(r'\n', ''))
            mcparams[str(run)]["PROF_SCAN_PARAM"] = scanparam
            sfile.close()

        ## Run over all the histograms in all the papers
        tree = ET.parse(outhistofile)
        for dps in tree.findall("dataPointSet"):
            dpsname = dps.get("path") + "/" + dps.get("name")
            ## Make a histogram and add it to the return dictionary
            mchistos[run][dpsname] = mkHistoFromDPS(dps)
            ## read histo-titles
            titles[dpsname] = dps.get("title")
    return mchistos, mcparams, titles



def getTuningData(refdir, outdir):
    '''A single command which gets the MC histos, MC parameters
    and the reference histograms all in one TuningData object. More
    convenient than the individual methods, but gives less fine-grained
    control of OS exceptions.'''

    ## Data container return value
    data = professor.histo.TuningData()

    ## Get reference data
    refhistos = getRefHistos(refdir)
    # refhistos, titles = getRefHistos(refdir)
    for name, histo in refhistos.iteritems():
        data.setRefHisto(name, histo)
    # data.setTitles(titles)

    ## Get MC histos and params for all the available tunings
    mchistos, mcparams, titles = getMCHistosAndParams(outdir)
    data.setTitles(titles)
    for run, histos in mchistos.iteritems():
        for name, histo in histos.iteritems():
            data.setMCHisto(name, run, histo)
    for run, params in mcparams.iteritems():
        data.setParams(run, params)

    ## Return TuningData object
    return data


def handleTestData(outdir, refrun):
    """Build a TuninData instance and reference parameter dict from Andy's
    test data.

    @param outdir: the path to the 'out' directory
    @type outdir: C{string}
    @param refrun: a subdirectory of outdir defining which run to use as
                   reference data
    @type refrun: C{string}
    @return: (TuningData instance , reference parameter C{dict}) C{tuple}
    """
    data = professor.histo.TuningData()

    mchistos, mcparams = getMCHistosAndParams(outdir)
    for run, histos in mchistos.iteritems():
        if run == refrun:
            #print "ref histo:", run
            for name, histo in histos.iteritems():
                data.setRefHisto(name, histo)
        else:
            #print "mc histo:", run
            for name, histo in histos.iteritems():
                data.setMCHisto(name, run, histo)

    for run, params in mcparams.iteritems():
        if run != refrun:
            data.setParams(run, params)
    #print mcparams

    return data, mcparams[refrun]

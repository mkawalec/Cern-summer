import os, sys, re, logging
import professor
from professor import histo
from paida import IAnalysisFactory


def mkHistoFromDPS(dps):
    """Make a mini histo representation from an AIDA DataPointSet object."""
    # myhist = histo.MCHisto()
    myhist = histo.Histo()
    numbins = dps.size()
    for binnum in range(numbins):
        dp = dps.point(binnum)
        ## X-vals
        dpx = dp.coordinate(0)
        xlow  = dpx.value() - dpx.errorMinus()
        xhigh = dpx.value() + dpx.errorPlus()
        ## Y-vals
        dpy = dp.coordinate(1)
        yval  = dpy.value()
        yerr = (dpy.errorPlus() + dpy.errorMinus())/2.0
        ## Build the bin
        bin = histo.Bin(xlow, xhigh)
        bin.setYVal(yval)
        bin.setYErr(yerr)
        myhist.addBin(bin)
    return myhist


def getRefHistos(refdir):
    '''Get a dictionary of reference histograms indexed by name.'''

    ## AIDA infrastructure
    analysisFactory = IAnalysisFactory.create()
    treeFactory = analysisFactory.createTreeFactory()


    ## Initialize the return value
    refhistos = {}

    refdir = os.path.abspath(refdir)
    for reffile in os.listdir(refdir):
        if not re.match(r'.*\.aida', reffile):
            continue
        refname = re.sub(r'(.*)\.aida', r'\1', reffile)
        #print reffile, refname

        reffilepath = os.path.abspath(os.path.join(refdir, reffile))
        if not os.path.isfile(reffilepath):
            logging.warn("Could not read reference file: " + reffilepath)
            continue
        
        tree = treeFactory.create(reffilepath, 'xml', readOnly=True, createNew=False, options='compress=no')
        if tree.find("HepData") is None:
            logging.warn("Could not read reference data from file: " + reffilepath)
        else:
            tree.cd("HepData")
            for paper in tree.listObjectNames():
                tree.cd(paper)
                for dpsname in tree.listObjectNames():
                    dps = tree.find(dpsname)

                    ## Strip off the "/HepData" prefix
                    #shortdpsname = re.sub(r'^/HepData', '', dpsname)
                    shortdpsname = dpsname[8:]

                    ## Make a mini histo object from the DPS
                    refhisto = mkHistoFromDPS(dps)

                    ## Add the reference histo to the return dictionary
                    refhistos[shortdpsname] = refhisto
    ## Return collection of ref histos
    return refhistos


def getMCHistosAndParams(mcdir):
    '''Get the generated MC histograms by iterating over all the MC runs
    in the top-level output directory.'''

    ## AIDA infrastructure
    analysisFactory = IAnalysisFactory.create()
    treeFactory = analysisFactory.createTreeFactory()

    ## Initialize the return values
    mcparams, mchistos = {}, {}

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
        if not os.access(outhistofile, os.R_OK) or not os.access(outparamsfile, os.R_OK):
            logging.warn("Can't read histo or params files for run %s... skipping" % str(run))
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
                logging.error("Parameter def %s is invalid" % str(tokens))
            else:
                # mcparams[tokens[0]] = tokens[1]
                temp[tokens[0]] = float(tokens[1])
        mcparams[str(run)] = temp

        ## Run over all the histograms in all the papers
        tree = treeFactory.create(outhistofile, 'xml', readOnly=True, createNew=False, options='compress=no')
        for paper in tree.listObjectNames():
            tree.cd(paper)
            for dpsname in tree.listObjectNames():
                #print dpsname
                dps = tree.find(dpsname)

                ## Make histo from AIDA DPS
                mchisto = mkHistoFromDPS(dps)
                #mchisto.setRunnr(str(run))

                ## Put the MC histos into the appropriate run number slot
                mchistos[run][dpsname] = mchisto

    return mchistos, mcparams



def getTuningData(refdir, outdir):
    '''A single command which gets the MC histos, MC parameters
    and the reference histograms all in one TuningData object. More
    convenient than the individual methods, but gives less fine-grained
    control of OS exceptions.'''

    ## Data container return value
    data = professor.histo.TuningData()

    ## Get reference data
    refhistos = getRefHistos(refdir)
    for name, histo in refhistos.iteritems():
        data.setRefHisto(name, histo)

    ## Get MC histos and params for all the available tunings
    mchistos, mcparams = getMCHistosAndParams(outdir)
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

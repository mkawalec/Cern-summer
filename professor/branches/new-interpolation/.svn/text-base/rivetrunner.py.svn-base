#! /usr/bin/env python

usage = """Usage: %prog -p <paramrangefile> [options]\n
Run an event generator a number of times (via rivetgun) to 
generate an output directory in the Professor format, i.e. a 
"ref" subdirectory with an AIDA reference histogram file, and 
an "mc" subdirectory with a number of numerically-named run 
subdirectories, each of which is equivalent to the "ref" 
directory.

This runner can generate runs either by random sampling from
the parameter hypercube, or by treating the parameter ranges 
as defining endpoints of a line in param space to be uniformly
sampled. It can also generate a "fake reference" point 
within a central region of the param hypercube for bootstrap 
testing of Professor when no real reference data is available.

Jobs can currently only be run on the local machine, but the
run speed can be improved by using multiple threads.

TODO: 
 * Job distribution: batch farm / Grid integration
 * Convert actual runner part to be a class in a rivetrunner 
   module in the professor package.
 * Store contents of -P files in output directory
"""


from optparse import OptionParser, OptionGroup
import os, sys, re, logging, commands, glob, shutil, time
import numpy, random
import threading, Queue
#import traceback, unittest
#import professor


## Set up logging
logging.basicConfig(level=20, format="%(message)s")
logging.debug("This is RivetRunner\n")


## Parse command line options
parser = OptionParser(usage=usage)

parser.add_option("-p", "--params", dest="PARAMSFILE",
                  default=None, help="file containing the param names and sample ranges")
parser.add_option("-n", "--num-events", dest="NUM_EVENTS_PER_RUN", type=int,
                  default=5000, help="how many events to generate in each run")
parser.add_option("-N", "--num-runs", dest="NUM_RUNS", type=int,
                  default=1, help="how many parameter space points to run the generator for")
parser.add_option("--first-run", dest="NUM_FIRST_RUN", type=int,
                  default=0, help="number given to the first run")
parser.add_option("-o", "--outdir", dest="OUT_DIR",
                  default="professor-out", help="directory into which to write the generator output")
parser.add_option("-t", "--timestamp", action="store_true", dest="TIMESTAMP",
                  default=False, help="add a timestamp prefix to the output directory name")
parser.add_option("-r", "--run", action="store_true", dest="RUN",
                  default=False, help="actually call Rivet rather than just writing out the command")

scangroup = OptionGroup(parser, "Param line scanning")
scangroup.add_option("-s", "--scan", action="store_true", dest="SCANMODE",
                     default=False, help="rather than scan randomly, treat param ranges as being endpoints " + \
                         "of a straight, uniformly sampled line in param space. Requires at least 2 runs to " + \
                         "work, and more to really make sense. Used to verify MC behaviour around a proposed " + \
                         "optimum and to compare systematically to other tunes.")
scangroup.add_option("--scan-range", dest="SCANRANGE", type=float,
                     default=1.0, help="specify symmetric fraction of the param range from which to sample " + \
                         "the params in scan mode. Internally, the line is specified by a linear parameter t, " + \
                         "with t=0,1 corresponding to the specified param range limits: setting the scan " + \
                         "range param to 1.2 would sample t uniformly from -0.1 to 1.1.")
parser.add_option_group(scangroup)

rivetgroup = OptionGroup(parser, "Rivet control")
rivetgroup.add_option("-g", "--gen", dest="GENERATOR",
                      default="FPythia:6413", help="generator to use (Rivet name convention)")
rivetgroup.add_option("-a", "--analysis", action="append", dest="ANALYSES",
                      help="add a Rivet analysis (can be used multiple times)")
rivetgroup.add_option("-A", "--all-analyses", action="store_true", dest="ALL_ANALYSES",
                      default=False, help="add all Rivet analyses, as for the rivetgun -A option")
rivetgroup.add_option("-P", "--rivet-paramfile", action="append", dest="RIVET_PARAM_FILES",
                      help="specify a Rivet parameter file as passed to rivetgun with '-P' (can be used multiple times)")
parser.add_option_group(rivetgroup)

refgroup = OptionGroup(parser, "Reference data")
refgroup.add_option("-R", "--fake-reference", action="store_true", dest="MKREF",
                    default=False, help="make an extra run as a fake reference point")
refgroup.add_option("--ref-range", dest="REFRANGE", type=float,
                    default=0.5, help="specify central fraction of the param range from which to sample the fake reference")
parser.add_option_group(refgroup)

jobgroup = OptionGroup(parser, "Job distribution")
jobgroup.add_option("-T", "--threads", dest="NUM_THREADS", type=int,
                    default=1, help="max number of threads to be used [1]")
jobgroup.add_option("--nice", dest="NICE", type=int,
                    default=10, help="optional nice level")
# jobgroup.add_option("-b", "--batch", dest="BATCH_SYSTEM",
#                   default=False, help="use a batch submission system. Choose from NO, PBS. NOT IMPLEMENTED!")
parser.add_option_group(jobgroup)

verbgroup = OptionGroup(parser, "Verbosity control")
verbgroup.add_option("-V", "--verbose", action="store_true", dest="VERBOSE", 
                     default=False, help="print status messages")
verbgroup.add_option("-D", "--debug", action="store_true", dest="DEBUG", 
                     default=False, help="print debug (very verbose) messages")
verbgroup.add_option("-Q", "--quiet", action="store_true", dest="QUIET",
                     default=False, help="be very quiet (overrides verbose and debug)")
parser.add_option_group(verbgroup)

(opts, args) = parser.parse_args()


## Provide defaults for analyses and -P options if none were specified
## (optparse defaults can't be used since these are 'append-type' options)
if opts.RIVET_PARAM_FILES is None:
    opts.RIVET_PARAM_FILES = ["lep1.params"]
if opts.ANALYSES is None:
    opts.ANALYSES = ["EXAMPLE", "DELPHI_1996_S3430090"]


## Add timestamp to output dir name
if opts.TIMESTAMP:
    outname = os.path.basename(opts.OUT_DIR)
    outparent = os.path.dirname(opts.OUT_DIR)
    timestamp = time.strftime("%Y-%m-%d")
    opts.OUT_DIR = os.path.join(outparent, timestamp + "-" + outname)


## Build paths to MC and reference output directories
mcoutdir = os.path.join(opts.OUT_DIR, "mc")
refoutdir = os.path.join(opts.OUT_DIR, "ref")


## Base command passed to rivetgun
GEN_CMD = 'rivetgun'
GEN_CMD += ' -g %s' % opts.GENERATOR
GEN_CMD += ' -n %d' % opts.NUM_EVENTS_PER_RUN
for pfile in opts.RIVET_PARAM_FILES:
    GEN_CMD += " -P %s" % pfile
if opts.ALL_ANALYSES:
    GEN_CMD += " -A"
for analysis in opts.ANALYSES:
    GEN_CMD += " -a %s" % analysis
if opts.NICE:
    GEN_CMD = "nice -%d " % opts.NICE + GEN_CMD

## Make the run names
runnames = ["%03d" % i for i in range(opts.NUM_FIRST_RUN, opts.NUM_FIRST_RUN + opts.NUM_RUNS)]


## Get parameter range definitions from a file
if not opts.PARAMSFILE:
    logging.error("Need to specify a parameter file with -p")
    sys.exit(1)
if not os.access(opts.PARAMSFILE, os.R_OK):
    logging.error("Parameter file %s needs to be readable" % opts.PARAMSFILE)
    sys.exit(1)
paramfile = file(opts.PARAMSFILE, "r")


## Read the params file
params = {}
for line in paramfile:
    line = re.sub(r'(^.*?)#.*', r'\1', line) # strip comments
    line = re.sub(r' +', r' ', line) # collapse spaces
    line = re.sub(r'\n', r'', line)
    if len(line) == 0 or line == " ":
        continue
    tokens = line.split(" ")
    if len(tokens) != 3:
        logging.error("Parameter def %s is invalid" % str(tokens))
        sys.exit(1)
    params[tokens[0]] = [float(tokens[1]), float(tokens[2])]
paramfile.close()


## Print out params
if opts.SCANMODE:
    logging.info("Parameter end points:")
else:
    logging.info("Parameter ranges:")
for k, v in sorted(params.iteritems()):
    logging.info("%-10s: %f - %f" % (k, v[0], v[1]))


## Initialize RNG
random.seed()


## Notify re. run conditions
logging.info("\nRunning generator %d times" % opts.NUM_RUNS)
if opts.SCANMODE:
    logging.info("Using linear scan mode: param points will not be randomly distributed!")
if not opts.RUN:
    logging.warn("Not actually running - use '-r' switch for a real run.")


## Make an individual directory for each run
if opts.RUN:
    runoutdir = "UNKNOWN"
    try:
        logging.debug("Making directory " + os.path.abspath(refoutdir))
        os.makedirs(os.path.abspath(refoutdir))
        for run in runnames:
            runoutdir = os.path.abspath(os.path.join(mcoutdir, str(run)))
            logging.debug("Making directory " + runoutdir)
            os.makedirs(runoutdir)
    except Exception, e:
        logging.error("Directory %s already exists... exiting" % runoutdir)
        logging.error(e)
        sys.exit(2)


def chooseRandomParams(runnames, rangefrac=1):
    """Make a random set of parameter values."""
    num = len(runnames)
    sortedrunnames = sorted(runnames)
    paramsets = {}
    for run in range(num):
        paramset = {}
        for k, v in params.iteritems():
            rangewidth = v[1] - v[0]
            rangelow  = v[0] + (1-rangefrac)/2.0 * rangewidth
            rangehigh = v[1] - (1-rangefrac)/2.0 * rangewidth
            randv = random.uniform(rangelow, rangehigh)
            paramset[k] = randv
        paramsets[sortedrunnames[run]] = paramset
    return paramsets


def chooseLineParams(num, rangefrac=1):
    """Make a set of parameter values distributed uniformly along a straight
    line in parameter space."""
    num = len(runnames)
    sortedrunnames = sorted(runnames)
    paramsets = {}
    ## Gradients and offsets defined against a control parameter t in range [0,1]
    gradients = dict()
    offsets = dict()
    for k, v in params.iteritems():
        offsets[k] = v[0]
        gradients[k] = v[1] - v[0]
    tStart = 0 - (rangefrac-1)/2.0
    tEnd = 1 + (rangefrac-1)/2.0
    ts = numpy.linspace(tStart, tEnd, num)
    for run in range(num):
        paramset = {}
        t = ts[run]
        ## Store scan parameter
        paramset["PROF_SCAN_PARAM"] = t
        ## Store generator parameters
        for k in params.keys():
            paramset[k] = offsets[k] + gradients[k] * t
        paramsets[sortedrunnames[run]] = paramset
    return paramsets


## Choose the param-choosing function based on sample/scan mode
chooseParams = chooseRandomParams
if opts.SCANMODE:
    chooseParams = chooseLineParams
    

## Build the generator execution string with random params
def mkruncmd(run, paramset):
    runoutdir = os.path.abspath(os.path.join(mcoutdir, str(run)))
    if run == "ref":
        runoutdir = os.path.abspath(refoutdir)

    ## Build generator command
    gencmd = GEN_CMD
    gencmd += " -H " + os.path.join(runoutdir, "out")

    ## Extract scan parameter, if it exists, and write to file
    if paramset.has_key("PROF_SCAN_PARAM"):
        t = paramset["PROF_SCAN_PARAM"]
        if opts.RUN:
            scanlog = file(os.path.join(runoutdir, "scan_params"), "w")
            scanlog.write(str(t))
            scanlog.close()
        ## Remove the meta-param from the generator param list
        del paramset["PROF_SCAN_PARAM"]

    ## Write out params file
    paramlog = None
    if opts.RUN:
        paramlog = file(os.path.join(runoutdir, "used_params"), "w")
    for k, v in sorted(paramset.iteritems()):
        gencmd += " -p \"%s=%f\"" % (k, v)
        if opts.RUN:
            paramlog.write("%s %f\n" % (k, v))
    if paramlog:
        paramlog.close()

    return gencmd


## Make run commands
runs = Queue.Queue(maxsize=-1)
paramsets = chooseParams(runnames, opts.SCANRANGE)
for runname in runnames:
    runs.put( (runname, mkruncmd(runname, paramsets[runname])) )
if opts.MKREF:
    if opts.SCANMODE:
        logging.info("Fake refs can't be used in scan mode: skipping fake ref command.")
    else:
        paramsets = chooseParams(["ref"], opts.REFRANGE)
        runs.put( ("ref", mkruncmd("ref", paramsets["ref"])) )


## Copy across reference data files
if not opts.MKREF:
    rivetdatadir = commands.getoutput("rivet-config --datadir")
    analysisglobs = opts.ANALYSES
    if opts.ALL_ANALYSES:
        logging.info("I don't know exactly which analyses ran, due to the -A option: copying all ref data to ref area")
        analysisglobs = ["*"]
    for analysis in analysisglobs:
        for aidafile in glob.glob(os.path.join(rivetdatadir, "%s.aida" % analysis)):
            if opts.RUN:
                logging.info("Copying %s to ref area" % aidafile)
                shutil.copy(aidafile, refoutdir)


## A simple class representing a process thread which attempts to
## execute generator runs from the "runs" Queue until empty.
class GenRunThread( threading.Thread ):
    def run(self):
        global runs
        global opts
        global mcoutdir
        global refoutdir
        while True:
            try:
                runpair = runs.get_nowait()
                if runpair is not None:
                    runname = runpair[0]
                    runcmd = runpair[1]
                    runoutdir = os.path.abspath(os.path.join(mcoutdir, str(runname)))
                    if runname == "ref":
                        runoutdir = os.path.abspath(refoutdir)
                    logging.info(runname + ": " + runcmd)
                    if opts.RUN:
                        cmd = runcmd + " > " + os.path.join(runoutdir, "out.log")
                        os.popen(cmd)
            except Queue.Empty, e:
                logging.debug("Thread %s ending." % self.getName())
                break


## Run the generator via threads
logging.info("\nRunning starts now:")
for threadnum in range(opts.NUM_THREADS):
    GenRunThread().start()


## Confirm that it's all over
#if opts.RUN:
#    logging.info("Done")

#! /usr/bin/env python

"""
Run an event generator a number of times with randomly generated parameters
based on ranges defined in an input file.
"""

## TODO
##
##  * Parallelise the runs via threading and Queue
##  * Build all commands before running (reduces sensitivity to changes in params file during runs)
##


from optparse import OptionParser
import os, sys, re, random, logging, commands
#import traceback, unittest
#import professor


## Set up logging
logging.basicConfig(level=20, format="%(message)s")
logging.info("This is RivetRunner")


## Parse command line options
parser = OptionParser()
parser.add_option("-V", "--verbose", action="store_true", dest="VERBOSE",
                  default=False, help="print status messages")
parser.add_option("-D", "--debug", action="store_true", dest="DEBUG",
                  default=False, help="print debug (very verbose) messages")
parser.add_option("-Q", "--quiet", action="store_true", dest="QUIET",
                  default=False, help="be very quiet (overrides verbose and debug)")
parser.add_option("-r", "--run", action="store_true", dest="RUN",
                  default=False, help="actually call Rivet rather than just writing out the command")
parser.add_option("-p", "--params", dest="PARAMSFILE",
                  default=None, help="file containing the param names and sample ranges")
parser.add_option("-n", "--num-events", dest="NUM_EVENTS_PER_RUN", type=int,
                  default=5000, help="how many events to generate in each run")
parser.add_option("-N", "--num-runs", dest="NUM_RUNS", type=int,
                  default=1, help="how many parameter space points to run the generator for")
parser.add_option("--first-run", dest="NUM_FIRST_RUN", type=int,
                  default=0, help="number given to the first run")
parser.add_option("-o", "--outdir", dest="OUT_DIR",
                  default=".", help="directory into which to write the generator output")
parser.add_option("-b", "--batch", dest="BATCH_SYSTEM",
                  default=False, help="use a batch submission system. Choose from NO, PBS. NOT IMPLEMENTED!")
(opts, args) = parser.parse_args()


## Base generator command
GEN_CMD = 'rivetgun -g FPythia6411 -P lep1.params -n %d -a TEST' \
          % opts.NUM_EVENTS_PER_RUN


## Make the run names
runnames = ["%03d" % i for i in range(opts.NUM_FIRST_RUN, opts.NUM_FIRST_RUN + opts.NUM_RUNS)]


## Get parameter range definitions from a file
if not opts.PARAMSFILE:
    raise Exception("Need to specify a parameter file with -p")
if not os.access(opts.PARAMSFILE, os.R_OK):
    raise Exception("Parameter file %s needs to be readable" % opts.PARAMSFILE)
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
logging.info("\nParameter ranges:")
for k, v in params.iteritems():
    logging.info("%-10s: %f - %f" % (k, v[0], v[1]))


## Try firing off generator runs for randomly sampled points in this space
## TODO: Job distribution: batch farm / Grid integration
random.seed()
logging.info("\nRunning generator %d times" % opts.NUM_RUNS)


## Make an individual directory for each run
for run in runnames:
    if opts.RUN:
        runoutdir = os.path.abspath(os.path.join(opts.OUT_DIR, str(run)))
        try:
            logging.info("Making directory " + runoutdir)
            os.makedirs(runoutdir)
        except Exception, e:
            logging.error("Directory %s already exists... exiting" % runoutdir)
            logging.error(e)
            sys.exit(2)


## Build the generator execution string with random params and run it
for run in runnames:
    runoutdir = os.path.abspath(os.path.join(opts.OUT_DIR, str(run)))

    ## Build generator command
    gencmd = GEN_CMD
    gencmd += " -H " + os.path.join(runoutdir, "out")

    ## Write out params file
    paramlog = None
    if opts.RUN:
        paramlog = file(os.path.join(runoutdir, "used_params"), "w")
    for k, v in params.iteritems():
        randv = random.uniform(v[0], v[1])
        gencmd += " -p \"%s=%f\"" % (k, randv)
        if opts.RUN:
            paramlog.write("%s %f\n" % (k, randv))
    if paramlog:
        paramlog.close()

    ## Run the generator command
    logging.info(gencmd)
    if opts.RUN:
        cmd = gencmd + " > " + os.path.join(runoutdir, "out.log")
        os.popen(cmd)

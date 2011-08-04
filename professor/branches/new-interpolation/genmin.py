#!/usr/bin/env python2.5
"""genmin.py

Minimize using the given/configured observable for all possible choices of
runs with one run omitted.


For command line options see:
    genmin.py --help

Some command line options can be set in a config file:
    see conf.initModule call at the top of the script
"""

import sys
import os.path as opa

from professor.tools.config import Config as _C
from professor.rivetreader import getTuningData
from professor.minimize import selectionfunctions, ResultList, ValidationFailed
from professor.observablelist import USE_OBS

conf = _C()
logger = conf.initModule('genmin',
        {'datadir' : ('./', None, True,
                      "directory with the 'mc/' and 'ref/' subdirectories")
        ,'outfile' : ('./results.xml', None, True,
                      "file where the results are stored")
        ,'observables' : ('all', None, True,
                          "a number to select the observable set (see"
                          " observablelist.py) or a comma separated list"
                          " with observable names to use" " for the"
                          " minimization. 'all' to use all observables.")
        ,'minimizer' : ('minuit', None, True,
                        "minimizer to use (scipy|minuit)")
        ,'start points': ('random', None, "spmethods",
                          "comma separated list with the minimization"
                          " starting points")
        ,'validate': (False, conf.convBool, True,
                      "validate the result")
        ,'debug' : (False, conf.convBool, True,
                    "turn debugging on (this will result in doing only a few"
                    " minimizations)")
        })
conf.initOption('genmin', 'dump config', False, conv=conf.convBool,
                cmdline="dump-config",
                help="dump the config to stdout and exit")
conf.initOption('genmin', 'list obs', False, conv=conf.convBool,
                cmdline=True,
                help="choose observables interactivly")
print "PARSING"
conf.parseCommandline()

if conf.getOption('genmin', 'dump config'):
    conf.write(sys.stdout, False)
    sys.exit(0)

# turn debug logging on off
if conf.getOption('genmin', 'debug'):
    logger.info("running in debug mode")
    conf.setOption('global', 'loglevel', 'debug')
else:
    conf.setOption('global', 'loglevel', 'info')

whichmin = conf.getOption('genmin', 'minimizer').lower()
if  whichmin == 'scipy':
    from professor.minimize.scipyminimizer import ScipyMinimizer as Minimizer
elif whichmin == 'minuit':
    from professor.minimize.minuitminimizer import ROOTMinuitMinimizer as Minimizer
else:
    raise ValueError("option genmin.minimizer = '%s' not supported"%(whichmin))
logger.info('using %s as Minimizer'%(Minimizer.__name__))

refdir = opa.join(conf.getOption('genmin', 'datadir'), 'ref')
mcdir = opa.join(conf.getOption('genmin', 'datadir'), 'mc')
outfile = open(conf.getOption('genmin', 'outfile'), 'w')
logger.info('loading XML files from %s and %s'%(mcdir, refdir))
tundat = getTuningData(refdir, mcdir)
tundat.isValid()

# select observables{{{
if conf.getOption('genmin', 'list obs'):
    obsnames = tundat.getRefHistoNames()
    for i, o in enumerate(obsnames):
        print "%2i: %s (%s)"%(i+1, o, tundat.getTitle(o))
    print "select wanted observables via a space separated list of numbers"
    e = raw_input("wanted observables: ")
    idx = map(int, e.split(' '))
    filtered= []
    for i in idx:
        filtered.append(obsnames[i-1])
    conf.setOption('genmin', 'observables', ','.join(filtered), True)
# }}}

minimizer = Minimizer(tundat)
# read observable config
obs = conf.getOption('genmin', 'observables').split(',')
try:
    i = int(obs[0])
    obs = USE_OBS[i]
except:
    if obs == ["all"]:
        obs = None
if obs:
    logger.info("using observables: %s"%(', '.join(obs)))
else:
    logger.info("using observables: all")
# read start point config
spmethods = conf.getOption('genmin', 'start points').split(',')
logger.info("using start point methods: %s"%(', '.join(spmethods)))

selfuncs = [selectionfunctions.OmitEmpty()]
logger.info("using selection functions: %s"%(
    ', '.join(['%s'%(sf) for sf in selfuncs])))


reslist = ResultList()
allruns = tundat.getRunNums()
allruns.sort()
if conf.getOption('genmin', 'debug'):
    leaveoutruns = xrange(3)
else:
    leaveoutruns = xrange(len(allruns))
for i in leaveoutruns:
    # allruns without the i th one
    curruns = allruns[:i] + allruns[i+1:]
    for meth in spmethods:
        logger.info("starting minimization for runs %s and spmethod %s"%(
                                curruns, meth))
        mr = minimizer.guessMinimum(meth, curruns, obs, selfuncs)
        if conf.getOption('genmin', 'validate'):
            try:
                minimizer.validateResult(mr)
            except ValidationFailed, e:
                logger.error("Validation for run #%i left out failed: \n%s"%(i, e))
                logger.error("Result not appended!")
            else:
                reslist.append(mr)
        else:
            reslist.append(mr)
# get result using all available runs
for meth in spmethods:
    logger.info("starting minimization for runs 'all' and spmethod %s"%(meth))
    mr = minimizer.guessMinimum(meth, allruns, obs, selfuncs)
    if conf.getOption('genmin', 'validate'):
        try:
            minimizer.validateResult(mr)
        except ValidationFailed, e:
            logger.error("Validation for run #%i left out failed: \n%s"%(i, e))
            logger.error("Result not appended!")
        else:
            reslist.append(mr)
    else:
        reslist.append(mr)

reslist.write(outfile)

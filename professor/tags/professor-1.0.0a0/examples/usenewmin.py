#!/usr/bin/env python2.5
"""
Example script to show the usage of the different parts.

I don't use 'from ... import ...' statements so everywhere 
in this file it is clear where the original code is located.

Hopefully heavy documented :)
"""

# import non-professor modules
import sys
import os
import numpy

# import our central config/logging module
import professor.tools.config

# import parameter handling tools
import professor.tools.parameter

# import the new minimization code
import professor.minimize

# import rivetreader so we can load data files
import professor.rivetreader

#### 1. Configuration
# get a handle to the Config object
conf = professor.tools.config.Config()

# now init configuration for this script with default values and store
# the returned logger
logger = conf.initModule('example',
        {
            # logging to file '-' means to send all messages to the parent
            # logger
            'logfiles' : '-',

            # the log level can be changed by the commandline. For this we
            # exchange the old string value by a length 4 tuple. The four
            # fields ars:
            # 1. default value
            # 2. a conversion function (e.g. int)
            # 3. string to use for the command line option
            # 4. help for the command line
            'loglevel' : ('debug', None, 'loglvl', "choose log level"),

            # obsoleted by rivetreader.py: getConfiguredData()
            # now the data dir.
            # Here we use 'True' as 3. field value, this results in a
            # standard string for the command line option
            # 'datadir' : ('./data/', None, True,
                         # "directory which contains the mc/ and ref/"
                         # " subdirectories"),

            # add a boolean option, n.b. real "switches" aren't supported
            # yet, to turn this on you have to use --dump-config yes
            # In fact every string whose lower()'ed version is in
            # ('1', 'on', 'yes', 'true') evaluates to True.
            #
            # To handle bool options use the Config.convBool static method.
            'dump config' : (False, conf.convBool, True,
                             "print the contents of the configuration to"
                             " stdout and exit"),
            'shell' : (False, conf.convBool, True,
                       "start a IPython shell after running the script"),
            'validate' :(False, conf.convBool, True,
                         "validate the result after minimization")
        })

# Now parse the commandline.
# If the user gives a config file via --config it is parsed before the
# command line, so command line options still overwrite them
conf.parseCommandline()

if conf.getOption('example', 'dump config'):
    conf.write(sys.stdout, False)
    sys.exit(0)


#### 2. Load data
# build the TuningData object
tundat = professor.rivetreader.getConfiguredData()

logger.debug('checking tuning data')
# this might raise an exception
tundat.isValid()

#### 2. Create Minimizer
# 
# If possible, Minuit is used as Minimizer automatically. Scipy is used as
# fallback.
# If you want to use Scipy, you can use it directly:
# >>> import professor.minimize.scipyminimizer
# >>> minimizer = professor.minimize.scipyminimizer.ScipyMinimizer()
logger.debug("creating minimizer")
minimizer = professor.minimize.Minimizer()
# minimizer = professor.minimize.scipyminimizer.ScipyMinimizer()

#### 3. Set up data selection for tune
# select the observables we want to use for our tune
obsdict = professor.rivetreader.readObservableFile(
                conf.getOption("data source", "obsfile"))
logger.debug("loaded observable file: %s"%(obsdict))

singletunedata = tundat.getTuneData(use_obs = obsdict.keys())
singletunedata.applyObservableWeightDict(obsdict)


#### 4. tune

# use the center of the parameter space as starting point (Minuit is not
# using the start point)
mr = minimizer.guessMinimum(singletunedata, "center")

print "Minimization results in:"
print mr
print
print "Used runs: %s"%(mr.runs)
print "Used observables: %s"%(mr.obs)
print

#### 5. Validating result (as of writing this only works with Minuit)
# this fixes one parameter after another to the values in the result mr
# and checks if the relative chi^2 and parameter deviations are below a
# given value (default 1e-3 for both)
if conf.getOption('example', 'validate'):
    print "Validating results..."
    minimizer.validateResult(mr)
    print "    ...done."
    print
    print "I hope you're happy now :)"

# uncomment this if you want to start a IPython shell at the end
# to examine the created objects
#
if conf.getOption('example', 'shell'):
    from IPython.Shell import IPShellEmbed
    ipshell = IPShellEmbed([])
    ipshell()

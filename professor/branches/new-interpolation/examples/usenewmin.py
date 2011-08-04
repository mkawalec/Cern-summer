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

            # now the data dir.
            # Here we use 'True' as 3. field value, this results in a
            # standard string for the command line option
            'datadir' : ('./data/', None, True,
                         "directory which contains the mc/ and ref/"
                         " subdirectories"),

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

# the data directories
mcdir = os.path.join(conf.getOption('example', 'datadir'), 'mc')
refdir = os.path.join(conf.getOption('example', 'datadir'), 'ref')

#### 2. Load data
# build the TuningData object
logger.info('loading XML files from %s and %s'%(mcdir, refdir))
tundat = professor.rivetreader.getTuningData(refdir, mcdir)

logger.debug('checking tuning data')
# this might raise an exception
tundat.isValid()

#### 2. Create Minimizer
# 
# If possible, Minuit is used as Minimizer automatically. Scipy is used as
# fallback.
# If you want to use Scipy, you can use it directly:
# >>> import professor.minimize.scipyminimizer
# >>> minimizer = professor.minimize.scipyminimizer.ScipyMinimizer(tundat)
logger.debug("creating minimizer")
minimizer = professor.minimize.Minimizer(tundat)

#### 3. Set up data selection for tune
# set up the selection functions
selfuncs = [professor.minimize.selectionfunctions.OmitEmpty(),
            professor.minimize.selectionfunctions.WeightObservable("/DELPHI_1996_S3430090/d35-x01-y01", 3)]

# select the observables we want to use for our tune
## TODO: It would be nice to take these from a config file in the same way as the compare_plots script.
obs = [
   "/DELPHI_1996_S3430090/d11-x01-y01",    # 1-thrust, 1-T (charged)
   #"/DELPHI_1996_S3430090/d28-x01-y01",    # Differential 2-jet rate with Jade algorithm, D_2^Jade (charged)
   #"/DELPHI_1996_S3430090/d30-x01-y01",    # Differential 3-jet rate with Jade algorithm, D_3^Jade (charged)
   #"/DELPHI_1996_S3430090/d32-x01-y01",    # Differential 4-jet rate with Jade algorithm, D_4^Jade (charged)
   "/DELPHI_1996_S3430090/d27-x01-y01",    # Differential 2-jet rate with Durham algorithm, D_2^Durham (charged)
   "/DELPHI_1996_S3430090/d29-x01-y01",    # Differential 3-jet rate with Durham algorithm, D_3^Durham (charged)
   "/DELPHI_1996_S3430090/d31-x01-y01",    # Differential 4-jet rate with Durham algorithm, D_4^Durham (charged)
   #"/DELPHI_1996_S3430090/d15-x01-y01",    # Sphericity, S (charged)
   #"/DELPHI_1996_S3430090/d16-x01-y01",    # Aplanarity, A (charged)
   "/DELPHI_1996_S3430090/d17-x01-y01",    # Planarity, P (charged)
   "/DELPHI_1996_S3430090/d12-x01-y01",    # Thrust major, M (charged)
   "/DELPHI_1996_S3430090/d13-x01-y01",    # Thrust minor, m (charged)
   #"/DELPHI_1996_S3430090/d33-x01-y01",    # Energy-energy correlation, EEC (charged)
   "/DELPHI_1996_S3430090/d35-x01-y01",    # Mean charged multiplicity
   "/DELPHI_1996_S3430090/d01-x01-y01",     # In-plane p_T in GeV w.r.t. thrust axes (charged)
   "/DELPHI_1996_S3430090/d02-x01-y01",     # Out-of-plane p_T in GeV w.r.t. thrust axes (charged)
   #"/DELPHI_1996_S3430090/d03-x01-y01",     # In-plane p_T in GeV w.r.t. sphericity axes (charged)
   #"/DELPHI_1996_S3430090/d04-x01-y01",     # Out-of-plane p_T in GeV w.r.t. sphericity axes (charged)
   #"/DELPHI_1996_S3430090/d05-x01-y01",     # Rapidity w.r.t. thrust axes, y_T (charged)
   #"/DELPHI_1996_S3430090/d06-x01-y01",     # Rapidity w.r.t. sphericity axes, y_S (charged)
   "/DELPHI_1996_S3430090/d07-x01-y01",     # Scaled momentum, x_p = |p|/|p_beam| (charged)
   ]

#### 4. tune
# use the center of the parameter space as starting point (Minuit is not
# using the start point)
mr = minimizer.guessMinimum("center", runs=None, obs=obs, selfuncs=selfuncs)

print "Minimization results in:"
print mr
print
print "Used runs: %s"%(mr.runs)
print "Used observables: %s"%(mr.obs)
print "Used selection functions: %s"%(['%s'%(sf) for sf in mr.selfuncs])
print

#### 5. Validating result (as of writing this only works with Minuit)
# this fixes one parameter after another to the values in the result mr
# and checks if the relative chi^2 and parameter deviations are below a
# given value (default 1e-6 for both)
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

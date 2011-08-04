"""useitall.py

example script to show the usage of the different parts.

I don't use from ... import ... statements so everywhere in this file it is
clear where the original code is located.

Hopefully heavy documented :)
"""

# import non-professor modules
import scipy.optimize, numpy

# import our central config/logging module
import professor.tools.config

# import parameter handling tools
import professor.tools.parameter


# import rivetreader so we can load data files
import professor.rivetreader


# get central config object and load configuration from the given file
conf = professor.tools.config.Config('example.conf')

# we use the module name `example' to store our configuration
# now we init our module with some default values in case the given
# configuration file doesn't contain any values.
# This does not overwrite any settings set before, e.g. during parsing
# example.conf!
logger = conf.initModule('example',
        {
        # a space separated list with filenames for logfiles:
        # `-' or `stderr' result in logging put to stderr
        # here we log to stderr an the file example.log
        'logfiles' : '- example.log',
        'loglevel' : 'debug',
        # the directory where xml files reside
        'mcdir' :  './data/mc',
        'refdir' : './data/ref'
        })

# store some configuration values
mcdir = conf.getOption('example', 'mcdir')
refdir = conf.getOption('example', 'refdir')


logger.info('loading XML files from %s and %s'%(mcdir, refdir))
tundat = professor.rivetreader.getTuningData(refdir, mcdir)

logger.debug('checking tuning data')
# this might raise an exception
tundat.isValid()

# Now build a list of reference bin - interpolation pairs:
#
# The method name comes from the time before the Durham meeting.
# Here we use all bins and all observables and all available runs.
# If you want to change this behaviour, use the `use_runnums' and `use_obs'
# arguments (None means use all).
# For the interpolation the center in the scaled world is taken: [.5, .5,
# ...]
#
# I think this method must be rewritten completely to make it more flexible.
logger.info('building (refbin, interp) list')
data = tundat.buildBinDistList(use_runnums = None, use_obs=["/Test/Thrust", "/Test/TotalChMult"])

# Reduce the data set to bins which are non-zero.
# Do this just once, we'll need it all over the place:
data_reduced = []
for refbin, interp in data:
    if (refbin.getYVal()!=0 and refbin.getYErr()!=0):
        data_reduced.append((refbin, interp))

# Now we want a Scaler instance so we can calculate the real world parameter
# values from the ones out of the scaled interpolation/minimization world.
# This must be given the same `use_runnums' argument as the buildBinDistList
# method.
logger.debug('building scaler')
scaler = tundat.getScaler(use_runnums = None)


# Check the interpolation. This requires ROOT to be installed and thus I
# disable the plots by default.
#
# Making the plots also depend on the scripts at
# http://www.linta.de/~hoeth/d0/make_plot/
# You need histplotter.py to generate the input files for make_plot.py. To
# create .ps or .pdf files call "make_plot.py <file.dat>" (see "make_plot.py
# --help" for options).
#
# To install ROOT, download the latest stable tarball from http://root.cern.ch/
# and do something like this:
#
#   find -type f | xargs sed -i "s@usr/X11R6@usr/X11R7@g"  # If running xorg 7.x
#   ./configure --prefix=/usr/local/root-5.16.00 --etcdir=/etc/root-5.16.00 \\
#               --enable-python --with-python-incdir=/usr/include/python2.5 \\
#               --with-python-libdir=/usr/lib  &&
#               make && make install
#
# Then to let python find the ROOT libraries do
#   export PYTHONPATH=/usr/local/root-5.16.00/lib/root

if False:
    for i, (refbin, interp) in enumerate(data_reduced):
        interp.plotPulls(i)
        interp.plotRatios(i)


# Now we can start minimizing:

# 1. create the chi2 function we want to minimize:
logger.debug('building chi2 funtion')
def chi2(p):
    r = 0.
    for refbin, interp in data_reduced:
        r += ( (refbin.getYVal() - interp.getValueFromScaled(p)) / refbin.getYErr() )**2
    return r

# 2. start minimization

# Use minuit:
if False:
    def fit_func_root(x, params):
        """fit_func_root() defines the prediction function in a way ROOT can
        use for the optimisation. Basically I return a constant value over the
        whole bin width.
        """
        bin=int(x[0])
        refbin, interp = data_reduced[bin]
        return interp.getValueFromScaled(params)
    def optimize_root():
        """optimize_root() uses the ROOT TH1:Fit() for optimisation.
        I define a TH1F histogram with a bin width of 1 and fill all data
        bins into this histogram. Then I fit the function defined in
        fit_func_root() to this histogram.

        NB: I don't set the start values for the fit yet, so minuit does
        everything on its own.
        """
        import ROOT
        npars=tundat.numberOfParams()
        nbins=len(data_reduced)
        # define fit function f:
        f=ROOT.TF1('prediction', fit_func_root, 0, nbins, npars)
        # define data histogram h:
        h=ROOT.TH1F('data_reduced', 'data_reduced', nbins, 0, nbins)
        # fill the histogram:
        for i, (refbin, interp) in enumerate(data_reduced):
            h.SetBinContent(i+1, refbin.getYVal())
            h.SetBinError(i+1, refbin.getYErr())
        # do the fit:
        h.Fit('prediction', 'NME')

        # print the result. FIXME: The error unscaling is ugly.
        guessval_root = []
        guesserr_root = []
        for i in range(npars):
            #print "Parameter %d: %e +- %e " %(i, f.GetParameter(i), f.GetParError(i))
            guessval_root.append(f.GetParameter(i))
            guesserr_root.append(f.GetParameter(i)+f.GetParError(i))
        finalguessval_root = professor.tools.parameter.ppFromList(guessval_root, scaler, scaled=True)
        finalguesserr_root = professor.tools.parameter.ppFromList(guesserr_root, scaler, scaled=True)
        print "Unscaled minimization results using ROOT:"
        for i in range(npars):
            foo = finalguessval_root.getUnscaled()[i]
            bar = finalguesserr_root.getUnscaled()[i]
            print '%s  %e +- %e' %(finalguessval_root.getKeys()[i], foo, bar-foo)
    optimize_root()

# Use the scipy-minimizer:
logger.info('starting the minimization using fmin_powell')
# set the starting point to the center of unit cube
p0 = .5 * numpy.ones(tundat.numberOfParams())
guess = scipy.optimize.fmin_powell(chi2, p0)

# work around scipy bug: in 1D the guess has shape () instead of (1,)
if guess.shape == ():
    guess.reshape(1)

logger.debug('unscaled result: %s'%(guess))

# Turn the guess into a ParameterPoint instance using a factory funtion.
finalguess = professor.tools.parameter.ppFromList(guess, scaler, scaled=True)

# Do some final output
logger.info('minimization result: %s'%(finalguess))
print "Minimization results in:"
print 'parameter names: ' + '\t'.join(finalguess.getKeys())
print 'unscaled values: ' + '\t'.join('%e' % p for p in finalguess.getUnscaled())
print 'scaled values:   ' + '\t'.join('%e' % p for p in finalguess.getScaled())

# uncomment this if you want to start a IPython shell at the end
# to examine the created objects
#
# from IPython.Shell import IPShellEmbed
# ipshell = IPShellEmbed()
# ipshell()

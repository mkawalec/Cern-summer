"""plotdataforandy.py

based on usenewmin.py



Hopefully heavy documented :)
"""

import sys
from optparse import OptionParser
parser = OptionParser()
parser.add_option("--show", action="store_true", dest="SHOW",
                  default=False, help="show plot interactively, rather than saving")
opts, args = parser.parse_args()

NUM_RUNS = 7
if len(args):
    NUM_RUNS = int(args[0])
print "Using %d runs to do the interpolation fit" % NUM_RUNS

# import non-professor modules
import numpy
import pylab
import matplotlib.axes3d

# import our central config/logging module
import professor.tools.config

# import parameter handling tools
import professor.tools.parameter

# import the new minimization code
import professor.minimize
import professor.minimize.selectionfunctions

# import rivetreader so we can load data files
import professor.rivetreader

# import 
import professor.tools.translate

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
        'mcdir' :  './mc',
        'refdir' : './ref'
        })

# store some configuration values
mcdir = conf.getOption('example', 'mcdir')
refdir = conf.getOption('example', 'refdir')


logger.info('loading XML files from %s and %s'%(mcdir, refdir))
tundat = professor.rivetreader.getTuningData(refdir, mcdir)

logger.debug('checking tuning data')
# this might raise an exception
tundat.isValid()

logger.debug("creating minimizer")
minimizer = professor.minimize.Minimizer(tundat)

# set up the selection functions
selfuncs = [professor.minimize.selectionfunctions.OmitEmpty()]
# just use the first observable:
obs = tundat.getMCHistoNames()[0:1]

## Choose the number of runs to use in the interpolation fitting
runs = ["%03i"%(i) for i in xrange(NUM_RUNS)]

mr = minimizer.guessMinimum("minmc", runs=runs, obs=obs, selfuncs=selfuncs)
data = minimizer.getData()
binnr = 0
interp = data[binnr][1]

def showOrSave():
    if opts.SHOW:
        pylab.show()
    else:
        filename = 'interpolation-%d.png' % NUM_RUNS
        print "Saving fig", filename
        pylab.savefig(filename)

def plot1D():
    anchors_x = []
    anchors_y = []
    # don't plot errors since they are not used in the interpolation
    anchors_err = []
    for param, bin in interp.getBD():
        anchors_x.append(param.getUnscaled()[0])
        anchors_y.append(bin.getYVal())
        anchors_err.append(bin.getYErr())

    scaler = mr.getScaler()

    interp_x = []
    interp_y = []
    for x_scaled in numpy.linspace(0, 1, 1000, endpoint=True):
        pp = professor.tools.parameter.ppFromList([x_scaled], scaler,
                                                  scaled=True)
        interp_x.append(pp.getUnscaled())
        interp_y.append(interp.getValue(pp))
    # pylab.plot(anchors_x, anchors_y, 'ro', label="anchor points")
    pylab.errorbar(anchors_x, anchors_y, yerr=anchors_err,
                   fmt='ro', label="anchor points")
    pylab.plot(interp_x, interp_y, 'b', ls='-', label="interpolation")
    pylab.xlabel('parameter %s'%(scaler.getKeys()[0]))
    pylab.ylabel('bin content')
    # pylab.legend(loc='best')
    showOrSave()

def plot2D():
    # data for use with scatter3D
    anchors_x = []
    anchors_y = []
    anchors_z = []

    for param, bin in interp.getBD():
        x, y = param.getUnscaled()
        anchors_x.append(x)
        anchors_y.append(y)
        anchors_z.append(bin.getYVal())

    scaler = minimizer.getScaler()

    mins = scaler.getMinVals()
    maxs = scaler.getMaxVals()
    l = 100
    xr = numpy.linspace(mins[0], maxs[0], l, endpoint=True)
    yr = numpy.linspace(mins[1], maxs[1], l, endpoint=True)
    X, Y = numpy.meshgrid(xr, yr)
    Z = numpy.zeros((l, l), "Float32")
    for i in xrange(l):
        for j in xrange(l):
            pp = professor.tools.parameter.ppFromList([X[i, j], Y[i, j]],
                                                      scaler,
                                                      scaled=False)
            Z[i,j] = interp.getValue(pp)

    fig = pylab.figure()
    ax = matplotlib.axes3d.Axes3D(fig)
    ax.scatter3D(anchors_x, anchors_y, anchors_z)
    ax.plot_wireframe(X, Y, Z)
    ax.set_xlabel("parameter %s"%scaler.getKeys()[0])
    ax.set_ylabel("parameter %s"%scaler.getKeys()[1])
    ax.set_zlabel("bin content")
    showOrSave()


dim = interp.getBD().dim()
if dim == 1:
    plot1D()
elif dim == 2:
    plot2D()
else:
    print "Dim %i not supported!"%(dim)

"""Convenience module which brings the core Professor API classes and functions
into scope with a single import.

The point of professor.user is to provide easy API access to the core Professor
classes to be used for loading MC and ref data; for making, storing, loading and
using ipols and runcombs; and for minimising and GoF computation.

The bulk of official prof scripts should also be written using only these
imports, with a few extra special imports used for the usage messages, banner,
etc.

We recommend that you import professor.user as follows:

  >>> from professor import user as prof

then use like this:

  >>> dp = prof.DataProxy(...)
"""

from professor import __version__ as version

from professor.data import *
from professor.fitfunctions import *

from professor.params import *

from professor.histo import Histo, Bin, PlotParser

from professor.interpolation import InterpolationSet
try:
    from professor.interpolation.interpolationweave import GenericWeaveBinInterpolation as InterpolationClass
except ImportError:
    from professor.interpolation.interpolation import GenericBinInterpolation as InterpolationClass
from professor.interpolation import addIpolCLOptions, BinDistribution

from professor.minimize import getMinimizerClass
from professor.minimize.result import MinimizationResult, ParameterTune, ResultList

from professor.tools.messages import writeGuideLine, writeLogo
from professor.tools import log, io
from professor.tools.log import addLoggingCLOptions
from professor.tools.errors import *

def addOutputCLOptions(parser):
    """ This adds the --outdir CL option to the parser. By default it
        reroutes to $datadir
    """
    parser.add_option("-o", "--outdir",
                 dest = "OUTDIR",
                 default=None,
                 help = "specifies an output directory with data-dir like structure [default: DATADIR]")


def getOutputDirectory(opts, subdir=None):
    """Get the output-tree base from command-line options.

    Alternatively a sub-directory suffix can be automatically be appended.
    """
    if opts.OUTDIR is not None:
        d = opts.OUTDIR
    elif opts.DATADIR is not None:
        d = opts.DATADIR
    else:
        log.error("No output directory given. Use --outdir or --datadir.")
        sys.exit(1)

    if subdir is not None:
        from os.path import join
        return join(d, subdir)

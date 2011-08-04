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

from professor.interpolation import getInterpolationClass, InterpolationSet
from professor.interpolation import addIpolCLOptions, BinDistribution

from professor.minimize import getMinimizerClass
from professor.minimize.result import MinimizationResult, ParameterTune, ResultList

from professor.tools.messages import writeGuideLine, writeLogo
from professor.tools import log, io
from professor.tools.log import addLoggingCLOptions
from professor.tools.errors import *

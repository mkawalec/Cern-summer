"""Professor is a tool for tuning particle physics Monte Carlo event
generator programs to optimally simulate high energy particle collisions, in
terms of their fit to recorded experimental data. It does this by sampling
random points in the generator parameter space, then using an SVD technique to
fit an interpolation function to bins of distributions. Finally, a minimiser is
used to predict the input parameters for which the generator will produce the
best output.

Professor is written as a Python library, which is used by a few installed
scripts to run generators via the Rivet system, and to predict and analyse new
tunings based on the interpolation technique.
"""

## Container package for the Professor parameterisation & tuning system.
## Don't import *anything* here! Use professor.user instead.
## This top-level module tests for a compatible Python version: it will always be executed.
## Don't define __all__: we don't want anyone to be able to do "from professor import *"

__version__ = "1.1.0"

import sys
pyversion = sys.version_info
if sys.version_info[0] < 2 or (sys.version_info[0] == 2 and sys.version_info[1] < 4):
    raise Exception("Professor requires Python 2.4 or greater")
del sys

"""__init__.py

professor/minimize

subpackage holding interfaces to external minimizers and and container
classes for minimization results.

minimizers
==========
For an explanation how to use the minimizer see L{BaseMinimizer}.
Supported external minimizers:
 - SciPy L{ScipyMinimizer}
 - PyMinuit L{PyMinuitMinimizer} (default)

To get the default minimizer use:
>>> from professor.minimize import getMinimizerClass
>>> MinClass = getMinimizerClass()
>>> min = MinClass()
>>> min.guessMinimum(singletunedata, "center")

container classes
=================
 - L{MinimizationResult}: stores minimization result information, e.g
   (un-)scaled parameter values (and errors when available).
 - L{ResultList}: extends a plain C{list} of MinimizationResults, e.g. it
   can be read/written from/to a xml-file for later usage.
"""

__all__ = ['baseminimizer', 'scipyminimizer', 'pyminuitminimizer', 'result']

from baseminimizer import ValidationFailed, MinError
from result import ResultList


def getMinimizerClass(which, useminos=False, printminuit=False):
    """Return the configured minimizer class.

    If import fails we use SciPy as a fallback.
    """
    if which == "pyminuit":
        try:
            import pyminuitminimizer
            # set some options of the minimizer
            # TODO: do this in a better way
            pyminuitminimizer.PyMinuitMinimizer.useminos = useminos
            pyminuitminimizer.PyMinuitMinimizer.printminuit = printminuit
            return pyminuitminimizer.PyMinuitMinimizer
        except ImportError, e:
            logging.error("Failed to load minimizer from pyminuitminimizer: %s", e)
            import scipyminimizer
            return scipyminimizer.ScipyMinimizer

    elif which == "scipy":
        import scipyminimizer
        return scipyminimizer.ScipyMinimizer

    else:
        raise ValueError("Unsupported minimizer chosen: %s"%(which))

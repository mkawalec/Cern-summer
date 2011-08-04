"""\
Introduction
------------

The minimize package defines interfaces to external minimizers, most notably
PyMinuit, and containers for minimization results.

minimizers
^^^^^^^^^^
For an explanation how to use the minimizer see :class:`~baseminimizer.BaseMinimizer`.
Supported minimizers are:

* :class:`~scipyminimizer.ScipyMinimizer`
* :class:`~pyminuitminizer.PyMinuitMinimizer`, which is used by default

A convenience function is available to get a minimizer that is available in
the current Python installation: :func:`getMinimizerClass`.

To get the default minimizer use::

>>> from professor.minimize import getMinimizerClass
>>> MinClass = getMinimizerClass()
>>> min = MinClass()
>>> min.guessMinimum(singletunedata, "center")

container classes
^^^^^^^^^^^^^^^^^

* :class:`MinimizationResult`
    A simple container for all data of one interpolation that is of interest
    for the different *prof-** scripts.
* :class:`ResultList`
    A list of `MinimizationResult`s that are stored in one file on disk.


Documentation
^^^^^^^^^^^^^

.. autofunction:: getMinimizerClass

.. autoclass:: baseminimizer.BaseMinimizer
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: result.MinimizationResult
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: professor.minimize.result.ResultList
   :members:
   :undoc-members:
   :show-inheritance:

"""

__all__ = ['baseminimizer', 'scipyminimizer', 'pyminuitminimizer', 'result']


from professor.tools import log as logging
from professor.tools.errors import MinimizerError, ValidationFailed, ResultError

## TODO: To be removed if commenting hasn't broken anything!
#from result import ResultList


def getMinimizerClass(which, useminos=False, printminuit=0):
    """
    Return the configured minimizer class.

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
        raise ValueError("Unsupported minimizer chosen: %s" % which)

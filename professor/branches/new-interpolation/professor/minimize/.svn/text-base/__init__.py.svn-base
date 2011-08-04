"""__init__.py

professor/minimize

subpackage holding interfaces to external minimizers and and container
classes for minimization results.

minimizers
==========
For an explanation how to use the minimizer see L{BaseMinimizer}.
Supported external minimizers:
 - SciPy L{ScipyMinimizer}
 - Minuit L{MinuitMinimizer} (default)

To get the default minimizer use:
>>> from professor.minimize import Minimizer
>>> min = Minimizer(TuningData_instance)

container classes
=================
 - L{MinimizationResult}: stores minimization result information, e.g
   (un-)scaled parameter values (and errors when available).
 - L{ResultList}: extends a plain C{list} of MinimizationResults, e.g. it
   can be read/written from/to a xml-file for later usage.
"""

__all__ = ['baseminimizer', 'scipyminimizer', 'minuitminimizer',
           'selectionfunctions']

from professor.tools.config import Config as _Config


_logger = _Config().initModule('minimize',
                       {'logfiles' : '-'})
                        # don't set loglevel, use the root logger's instead
                        # 'loglevel' : 'info'})
_logger.debug("using config %r"%(_Config()))

try:
    from minuitminimizer import ROOTMinuitMinimizer as Minimizer
    _logger.info("imported ROOTMinuitMinimizer as Minimizer")
except ImportError, e:
    _logger.warning("failed to import MinuitMinimizer as Minimizer: %s", e)
    from scipyminimizer import ScipyMinimizer as Minimizer
    _logger.info("imported ScipyMinimizer as Minimizer")

from baseminimizer import ValidationFailed
from result import ResultList
import selectionfunctions

_logger.debug('finished minimize/__init__.py')

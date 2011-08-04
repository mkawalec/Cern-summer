"""__init__.py
Subpackage to interpolate the MC behaviour.

TODO!
Contains 2 objects for external usage:

    1. BinDistribution:
       Simple container for MC run data.

    2. getInterpolationClass:
       Function to get a concrete L{Interpolation} subclass based on config
       option 'interpolation.method'.
       At the moment only Quadratic (config: interpolation.method = quadratic)
       is available.

Usage:

    >>> from professor.interpolation import getInterpolationClass
    >>> InterpolationClass = getInterpolationClass()
"""

__all__ = ['interpolationlist', 'interpolation', 'bindistribution']

from professor.tools.config import Config as _C
_logger = _C().initModule('interpolation',
                         {'logfiles' : '-',
                          'loglevel' : 'warning',
                          'method' : 'quadratic'})

from bindistribution import BinDistribution
from interpolationlist import InterpolationSet
from interpolation import getInterpolationClass

_logger.debug('finished interpolation/__init__.py')

"""__init__.py
Subpackage to interpolate the MC behaviour.

TODO!
Contains 2 objects for external usage:

    1. BinDistribution:
       Simple container for MC run data.

    2. getInterpolationClass:
       Function to get a concrete L{Interpolation} subclass based on config
       option 'interpolation.method'. Current allowed values are 'quadratic' and 'cubic'.

Usage:

    >>> from professor.interpolation import getInterpolationClass
    >>> InterpolationClass = getInterpolationClass("quadratic", True)
"""

__all__ = ['interpolationset', 'interpolation', 'bindistribution']


from bindistribution import BinDistribution
from interpolationset import InterpolationSet
from interpolation import getInterpolationClass


def addIpolCLOptions(optparser):
    from optparse import OptionGroup
    optgroup = OptionGroup(optparser, "Interpolation")

    optgroup.add_option("--ipol-method",
            dest = "ipolmethod",
            type = "choice",
            choices = ("quadratic", "cubic"),
            help = "the interpolation method (quadratic|cubic) (default: %default)")

    optgroup.add_option("--weave",
            dest="useweave",
            action = "store_true",
            help = "use the weave implementation of the interpolation (default: %default)")

    optgroup.add_option("--noweave",
            dest="useweave",
            action = "store_false",
            help = "use the Python implementation of the interpolation")

    optparser.add_option_group(optgroup)
    optparser.set_defaults(
            ipolmethod = "quadratic",
            useweave = True)


## I think this is not used anymore, and can be safely removed
from professor.tools.decorators import deprecated
addCLOptions = deprecated("interpolation.addIpolCLOptions")(addIpolCLOptions)

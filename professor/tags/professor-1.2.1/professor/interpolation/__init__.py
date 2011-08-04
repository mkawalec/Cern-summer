"""\
Introduction
------------

The interpolation sub-package contains the data structures for the
bin-wise parameterization of the MC response function. Four objects are
designed for external usage and are available in :mod:`professor.user`:

:func:`addIpolCLOptions`
    Add an :class:`OptionGroup` with common options to an command line
    parser.

:func:`getInterpolationClass`
    Function to get a :class:`BaseBinInterpolation` subclass for
    interpolation.

:class:`BinDistribution`
    A simple container for the MC run data of a single bin.

:class:`InterpolationSet`
    Container for all bin-wise interpolations for one set of anchor points.
    Used for persistency.

Examples
^^^^^^^^

Get the quadratic polynomial interpolation class that uses weave:

    >>> ipolcls = prof.getInterpolationClass("quadratic", True)

Load an interpolation set from a file.

    >>> ipolset = prof.InterpolationSet.fromPickle("path/to/file.pkl")

Documentation
^^^^^^^^^^^^^

.. autofunction:: addIpolCLOptions

.. autofunction:: getInterpolationClass

.. autoclass:: BinDistribution
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: InterpolationSet
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: professor.interpolation.interpolation.BaseBinInterpolation
   :members:
   :undoc-members:
   :show-inheritance:

"""

__all__ = ['interpolationset', 'interpolation', 'bindistribution']


from bindistribution import BinDistribution
from interpolationset import InterpolationSet
from interpolation import getInterpolationClass


def addIpolCLOptions(optparser, weaveswitch=False):
    """Add an OptionGroup with common options to an command line parser."""
    from optparse import OptionGroup
    optgroup = OptionGroup(optparser, "Interpolation")

    optgroup.add_option("--ipol", "--ipol-method",
                        dest = "IPOLMETHOD",
                        type = "choice",
                        choices = ("quadratic", "cubic"),
                        default = "cubic",
                        help = "the interpolation method (quadratic|cubic)"
                        " [default: %default]")
    if weaveswitch:
        optgroup.add_option("--weave",
                            dest="USEWEAVE",
                            action = "store_true",
                            help = "use the weave implementation of the interpolation"
                            " [default]")
        optgroup.add_option("--noweave",
                            dest="USEWEAVE",
                            action = "store_false",
                            help = "use the Python implementation of the interpolation")
        optparser.set_default("USEWEAVE", True)

    optparser.add_option_group(optgroup)

"""This sub-package contains the classes used for loading data from disk and to
re-structure them for tuning.

The loading of files from disk is done in :class:`DataProxy` (or
:class:`~professor.data.proxy.RivetDataProxy`). Files are only read if necessary
and then cached. A :class:`TuneData` object holds all information necessary for
a single tune or for comparing MC data (held in :class:`MCData`) with reference
data.  Basically, `TuneData` is just a list of :class:`BinProps` objects, one
object for each bin that is in the requested observables.

The data flow looks like this::

    +-----+   +------+  +----+
    | ref |   | ipol |  | mc |  (files on disk)
    +-----+   +------+  +----+
       |       |          |
       |    +---------+ +--------+
       |    | IpolSet | | MCData |
       |    +---------+ +--------+
       |       |          |
    +-----------+         |
    | DataProxy |---------+
    +-----------+
       |
    +----------+
    | TuneData |      (list of BinProps)
    +----------+
       |
    +------------+
    | GoF object |    (this compares MC/interpolation with reference)
    +------------+


.. autoclass:: DataProxy
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: professor.data.proxy.RivetDataProxy
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: MCData
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: ManualMCData
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: TuneData
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: BinProps
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: WeightManager
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: Weight
    :members:
    :undoc-members:
    :show-inheritance:

"""

from proxy import DataProxy
from mcdata import MCData, ManualMCData
from tunedata import TuneData, BinProps

from weightmanager import WeightManager, Weight
from runcombmanager import RunCombManager


## Command-line I/O
def addDataCLOptions(parser, ref=False, mc=False, ipol=False, scan=False):
    """
    Add data location options to command-line option parser.

    Use the flags ref, mc, ... to include data locations as needed. Set
    only those flags to True that are actually needed by a script to
    keep the CL interface clean.

    See Also
    --------
    DataProxy.fromCLOptions : Build a `DataProxy` instance from command line options.
    DataProxy.getPathsFromCLOptions : Get a `dict` of data-location paths from command line options.
    addRunCombsCLOptions : Add the standard CL option for loading lists of run combinations.
    """
    from optparse import OptionGroup
    g = OptionGroup(parser, "Data locations")
    g.add_option("--datadir",
                 metavar = "DATADIR",
                 dest = "DATADIR",
                 help = "directory containing mc, ref and ipol directories")

    if mc:
        g.add_option("--mcdir",
                     dest = "MCDIR",
                     help = "directory containing random mode MC runs"
                     " [default: DATADIR/mc]")

    if ref:
        g.add_option("--refdir",
                     dest = "REFDIR",
                     help = "directory containing reference runs"
                     " [default: DATADIR/ref]")

    if scan:
        g.add_option("--scandir",
                     dest = "SCANDIR",
                     help = "directory containing scan mode MC runs"
                     " [default: DATADIR/scan]")

    # TODO: Add an --outdir opt which defaults to --datadir, for ipols, ipolhistos, etc.

    if ipol:
        g.add_option("--ipoldir",
                     dest = "IPOLDIR",
                     help = "directory to store/load interpolation sets"
                     " [default: DATADIR/ipol]")

    ## Dual-purpose option: prof-interpolate doesn't care about weight values
    g.add_option("--weights", "--obs", "--obsfile",
                 metavar = "WEIGHTS",
                 dest = "OBSERVABLEFILE",
                 help = "file with observable weight definitions")

    parser.add_option_group(g)


def addRunCombsCLOptions(parser):
    """
    Add run combination options to command-line option parser.

    See Also
    --------
    addDataCLOptions : Add standard CL options for data, MC, ipol, etc. directories.
    """
    parser.add_option("--runs", "--runsfile", "--runcombs",
                      dest="RUNSFILE",
                      default=None,
                      help="specify a file of run combinations to use (space-separated, "
                      "one combination per line) [default: %default]")

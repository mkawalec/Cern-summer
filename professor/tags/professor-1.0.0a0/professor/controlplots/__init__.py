"""Sub-package for control plots.

Each of the modules contains a class that takes a (usually) a DataProxy or MCData
instance, extracts/computes the information that should be displayed and
methods for plotting with matplotlib or make-plots.

In addition the StyleGenerator helper class is located in this sub-package.
"""

from stylegen import StyleGenerator
from linescan import LineScanPlotter
from parameterscatter import ParameterScatterPlotter
from envelope import EnvelopeGetter

"""elementtree.py

Use this module to get the best ElementTree implementation

Usage:

    >>> from professor.tools.elementtree import ET

"""

from professor.tools.config import Config as _C

_logger = _C().getLogger()

# try to load faster but non-standard cElementTree module
try:
    import xml.etree.cElementTree as ET
except ImportError:
    _logger.info("Could not load module xml.etree.cElementTree,"
                   " so we're on a python < 2.5 system."
                   " Trying to load cElementTree...")
    try:
        import cElementTree as ET
    except ImportError:
        _logger.warn("Could not load module cElementTree: "
                       "using slower xml.etree.ElementTree instead!")
        import xml.etree.ElementTree as ET



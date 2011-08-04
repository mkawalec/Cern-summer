"""elementtree.py

Use this module to get the best ElementTree implementation

Usage:

    >>> from professor.tools.elementtree import ET

"""

import logging

# try to load faster but non-standard cElementTree module
try:
    import xml.etree.cElementTree as ET
except ImportError:
    logging.info("Could not load module xml.etree.cElementTree,"
                 " so we're on a python < 2.5 system."
                 " Trying to load cElementTree...")
    try:
        import cElementTree as ET
    except ImportError:
        logging.warning("Could not load module cElementTree:"
                        " using slower xml.etree.ElementTree instead!")
        import xml.etree.ElementTree as ET



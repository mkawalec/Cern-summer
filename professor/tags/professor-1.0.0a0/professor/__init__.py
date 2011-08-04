"""Container package for the Professor parameterisation & tuning system.

Don't import *anything* here! Use professor.user instead.

This top-level module tests for a compatible Python version: it will always be executed.
"""

__all__ = ['histo', 'interpolation', 'tools', 'minimize', 'dataproxy']

import sys
pyversion = sys.version_info
if sys.version_info[0] < 2 or (sys.version_info[0] == 2 and sys.version_info[1] < 4):
    raise Exception("Professor requires Python 2.4 or greater")
del sys

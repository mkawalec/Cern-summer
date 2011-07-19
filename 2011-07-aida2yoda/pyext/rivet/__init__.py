"Python interface to the Rivet MC validation system"

## Change dlopen status to GLOBAL for Rivet lib
import sys
try:
    import ctypes
    sys.setdlopenflags(sys.getdlopenflags() | ctypes.RTLD_GLOBAL)
    del ctypes
except:
    import dl
    sys.setdlopenflags(sys.getdlopenflags() | dl.RTLD_GLOBAL)
    del dl
del sys

## Import SWIG-generated wrapper core
from rivetwrap import *

## Provide an extra Python-only function used to enforce the Rivet scripts' minimal Python version
def check_python_version():
    import sys
    req_version = (2,4,0)
    if sys.version_info[:3] < req_version:
        sys.stderr.write( "rivet scripts require Python version >= %s... exiting\n" % ".".join(req_version) )
        sys.exit(1)

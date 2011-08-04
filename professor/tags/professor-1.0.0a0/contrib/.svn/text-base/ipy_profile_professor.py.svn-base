import IPython.ipapi

from IPython.Extensions import ipy_profile_scipy

ip = IPython.ipapi.get()
try:
    ip.ex("from professor.user import *")
    ip.ex("from professor.controlplots import *")
except ImportError, err:
    print "Unable to start professor profile, is professor installed?"


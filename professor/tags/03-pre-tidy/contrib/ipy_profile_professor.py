import IPython.ipapi

from IPython.Extensions import ipy_profile_scipy

ip = IPython.ipapi.get()
try:
    ip.ex("from professor import *")
    ip.ex("from professor.rivetreader import *")
    ip.ex("from professor.interpolation import *")
    ip.ex("from professor.minimize import *")
except ImportError:
    print "Unable to start professor profile, is professor installed?"


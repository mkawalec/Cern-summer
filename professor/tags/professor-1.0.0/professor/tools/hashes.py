"""Super-minimal convenience wrapper for getting the MD5 hash function, since
the module name changed between versions of Python in use on SL5 and more recent
OSes.
"""

## Work around python 2.4 on SL 5
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

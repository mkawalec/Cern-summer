#!/usr/bin/env python2.5
"""testcenterdata.py

simple script that tests if the chi^2 value stored in the chi^2 vs.
interpolation center files does not change.

usage::
    testcenterdata.py FILE1 [...]
"""

import sys

class MismatchError(Exception):
    pass

def testfile(path):
    f = open(path)
    # search the first data line
    for line in f:
        if not line.startswith("#"):
            break
    chi2 = line.split(";")[0]

    for line in f:
        t = line.split(";")[0]
        if chi2 != t:
            raise MismatchError("chi^2 values differ in file '%s':"
                    " %s != %s!"%(path, chi2, t))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print __doc__
        sys.exit(1)

    total = len(sys.argv[1:])
    successes = 0
    for p in sys.argv[1:]:
        try:
            testfile(p)
            successes += 1
        except MismatchError, e:
            print e

    print "Successes: %i/%i"%(successes, total)

#! /usr/bin/env python

import sys
from yoda import *

def testmatch(name, v1, v2, tolerance=1e-3):
    fracdiff = 2*abs(v1 - v2)/(v1 + v2)
    match = (fracdiff < 1e-3)
    passfail = "PASS" if match else "FAIL"
    print "Testing %s: %f vs. %f => %e deviation. %s" % (name, v1, v2, fracdiff, passfail)
    return match

h1 = Histo1D(5, 0.0, 100.0)
h1.fill(10,-200)
h1.fill(20,1)
h1.fill(30,0.2)
h1.fill(10,+200)

h2 = Histo1D(5, 0.0, 100.0)
h2.fill(20,1)
h2.fill(30,0.2)

meanmatch   = testmatch("means",    h1.mean(),   h2.mean())
stddevmatch = testmatch("std devs", h1.stdDev(), h2.stdDev())
ok = (stddevmatch and meanmatch)

p1 = Profile1D(5, 0.0, 100.0)
p1.fill(10, 10, -200)
p1.fill(10, 10, +200)
p1.fill(20, 20, 1)
p1.fill(25, 40, 4)
p1.fill(70, 70, 0.2)

p2 = Profile1D(5, 0.0, 100.0)
p2.fill(20, 20, 1)
p2.fill(25, 40, 4)
p2.fill(70, 70, 0.2)

for i, j in zip(p1.bins(), p2.bins()):
    if i.numEntries() > 1 and j.numEntries() > 1:
        meanmatch   = testmatch("y means",    i.mean(),   j.mean())
        stddevmatch = testmatch("y std errs", i.stdErr(), j.stdErr())
        ok = ok and stddevmatch and meanmatch

if not ok:
    sys.exit(1)

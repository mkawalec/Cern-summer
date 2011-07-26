#! /usr/bin/env python

from yoda import *
NUM_SAMPLES = 1000

h = Histo1D("/foo", "Title", 50, 0.0, 100.0)

for i in range(NUM_SAMPLES):
    exp = - (i-NUM_SAMPLES/2)**2 / float(NUM_SAMPLES/4)
    val = 2.718 ** exp
    h.fill(val);

print h.mean(), "+-", h.stdDev()

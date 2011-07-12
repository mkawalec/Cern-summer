#! /usr/env/python

import os
from subprocess import Popen
import time

null = open('/dev/null', 'w')

# Make fifos

subprocesses = []

for n in xrange(3):
    print "Spawning process %d" % n
    pipe = "/tmp/dmallows/privet-%02d.fifo" % n
    aida = "privet-%02d.aida" % n

    try:
        os.mkfifo(pipe)
    except OSError, e:
        print e

    agile=Popen("agile-runmc Pythia6:425 --beams=LHC:7000 -n 2000 -o %s" % pipe, shell=True)
    agile.poll()

    time.sleep(5)

    rivet=Popen("rivet -a MC_GENERIC -H %s %s" % (aida,pipe), shell=True)
    rivet.poll()

    subprocesses.append((agile, rivet))

while subprocesses:
    time.sleep(1)
    print subprocesses
    for n, (a, r) in enumerate(subprocesses):
        s = a.poll(), r.poll()
        print s

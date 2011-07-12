#! /usr/env/python

import os
from subprocess import Popen
import time

null = open('/dev/null', 'w')

# Make fifos

pipes = []
subprocesses = []

pipe_fn = lambda n: "/tmp/dmallows/privet-%02d.fifo" % n
aida_fn = lambda n: "privet-%02d.aida" % n

try:
    for n in xrange(1):
        pipe = pipe_fn(n)
        aida = aida_fn(n)

        try:
            pipes.append(pipe)
            os.mkfifo(pipe)
        except OSError, e:
            print e

        agile=Popen(['agile-runmc','Pythia6:425','--beams=LHC:7000', '-n',
                    '2000', '-o', pipe], stdout=null, stderr=null)
        agile.poll()

        rivet=Popen(['rivet','-a','MC_GENERIC','-H', aida, pipe],stdout=null,stderr=null)
        rivet.poll()

        subprocesses.append((n, agile, rivet))

    state = 0
    finished = []

    while subprocesses:
        time.sleep(1)
        for i, (n, a, r) in enumerate(subprocesses):
            aState, rState = a.poll(), r.poll()
            print n, aState, rState
            if rState is not None:
                try:
                    if aState is None:
                        a.kill()
                finally:
                    finished.append((n, aState, rState))
                    subprocesses.pop(i)

    print finished

finally:
    print "Cleaning the pipes..."
    for f in pipes:
        os.unlink(f)

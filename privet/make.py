#! /usr/bin/env python2

""" 
This is supposed to be a small script for running and compiling 
an analysis for Rivet. It has an overgrowth of features, precisely
to boost my line count at github.
"""

import sys
import hashlib
import os
import subprocess
import time

if sys.version_info[:3] < (2, 4, 0):
    print 'This script requires at least python 2.5. Go get it now!!11!!'
    sys.exit(1)

# Try importing rivet
try:
    import rivet
    rivet.check_python_version()
except Exception, e:
    sys.stderr.write(PROGNAME + " requires the 'rivet' Python module\n")
    sys.stderr.write(str(e)+'\n')
    sys.exit(1)

# Regexps here?
def md5sum(fileName, excludeLine='#'):
    """Compute md5 hash of the specified file"""
    m = hashlib.md5()
    with open(filename, 'rb') as file:
        for line in file:
            if excludeLine and line.startswith(excludeLine) or line == '':
                continue
            m.update(eachLine)
        return m.hexdigest()

def build_plugin(name, verbose=False):
    so_name = 'Rivet%sAnalysis.so' % name
    ana_name = '%s.cc' % name
    output = subprocess.check_output(['rivet-buildplugin', so_name, ana_name])
    if verbose: 
        print(output)

# Parsing command line options:
from optparse import OptionParser
parser = OptionParser(usage=__doc__, version='1')

parser.add_option('-m', '--make', dest='make', action='store_true',
        default=None,
        help='Make analysis plugins before running rivet')
parser.add_option('-b', '--beams', dest='beams', default='LHC:7000',
        help='Specify beam parameters for AGILe')
parser.add_option('-g', '--generator', dest='generator', default='Pythia:423',
        help='Generator to use. Default: Pythia:423.')
parser.add_option('-n', '--number', dest='number', type='int', default=1000,
        help='Number of events to generate. Default: 2000.')
parser.add_option('-j', '--threads', dest='threads', type='int', default=1,
        help='Number of processes to fork. Default: 1')
parser.add_option('-p', '--options', dest='options', default='',
        help='Options string for Pythia.')
parser.add_option('-P', dest='options2', default='',
        help='additional options for Pythia')
parser.add_option('-t', '--options', dest='tempdir', default='/dev/shm',
        help='Directory to create pipes in. Defaults to /dev/shm')
parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
        default=False, help='make the program verbose')

(opts,args) = parser.parse_args()

print opts, args

# Now we check if the file should be built automatically
analyses = args
all_analyses = rivet.AnalysisLoader.analysisNames()

# Build a dictionary of files -> md5
with file as open('.makerc', 'r'):
    md5s = dict(line.split() for line in file)

# Get analyses with cc on the end. We wish to preserve the order.

filter(analyses, is_cc_file)

for i, filename in enumerate(cc_analyses):
    if not filename.endswith('.cc'): 
        continue

    # Strip filename of its extension
    name = filename[:-3]
    analyses[i] = name

    newsum = md5sum(file)
    oldsum = md5s[file]

    if oldsum == newsum:
        continue
        print('Found')
    else:
        build_plugin(name)
        md5s[ccfile] = newsum

# Some moving around of the files to be sure we have what we need in the file
# Great! :)

with open('.makerc.swp', 'w') as out:
    lines = ' '.join(i) for i in md5.iteritems()
    out.write('\n'.join(lines))

# Changing this to os.rename, simple reason that...
# "If successful, the renaming will be an atomic operation
# (this is a POSIX requirement"
os.rename('.makerc.swp', '.makerc')

# Now, let's add the stuff to look for analysis
# Did I write that?

devnull = open('/dev/null', 'w')

# Make fifos
pipes = []
subprocesses = []

def run_rivet():

rivet_args = []
agile_args = lambda pipe:
                ['agile-runmc', generator, '--beams=%s' % beams, '-n',
                number, '-o', pipe, '-p', 'MSEL=6', '-P',
                 'fpythia-Wenumunu.params','--randomize-seed' ]

pipe_fn = lambda n: '/tmp/dmallows/privet-%02d.fifo' % n
aida_fn = lambda n: 'privet-%02d.aida' % n

try:
    for n in xrange(10):
        pipe = pipe_fn(n)
        aida = aida_fn(n)

        try:
            pipes.append(pipe)
            os.mkfifo(pipe)
        except OSError, e:
            print e

        agile=Popen(agile_args(pipe), stdout=devnull, stderr=devnull)
        agile.poll()

        rivet=Popen(['rivet','-a','MC_TTBAR2','-H', aida, pipe])
        rivet.poll()

        subprocesses.append((n, agile, rivet))

    state = 0
    finished = []

    while subprocesses:
        time.sleep(1)
        for i, (n, a, r) in enumerate(subprocesses):
            aState, rState = a.poll(), r.poll()
            if rState is not None:
                try:
                    a.kill()
                except Exception, e:
                    pass
                finally:
                    finished.append((n, aState, rState))
                    subprocesses.pop(i)

finally:
    print 'Cleaning the pipes...'
    for f in pipes:
        os.unlink(f)
"""

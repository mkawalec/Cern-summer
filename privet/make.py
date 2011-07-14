#! /usr/bin/env python2

""" 
This is supposed to be a small script for running and compiling 
an analysis for Rivet. It has an overgrowth of features, precisely
to boost my line count at github.
"""
# Hack to be removed - breaks cross-platform (windows - is that a problem?)
devnull = open('/dev/null', 'w')

import sys
import hashlib
import os
from subprocess import Popen, PIPE
import time
import logging

os.putenv('RIVET_ANALYSIS_PATH',os.getcwd())
print os.getenv('RIVET_ANALYSIS_PATH')
print "foo", os.getcwd()

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

def md5sum(fileName, excludeLine='#'):
    """Compute md5 hash of the specified file"""
    m = hashlib.md5()
    with open(filename, 'rb') as file:
        for line in file:
            if excludeLine and line.startswith(excludeLine) or line == '':
                continue
            m.update(line)
        return m.hexdigest()

def build_plugin(name, verbose=True):
    so_name = 'Rivet%sAnalysis.so' % name
    ana_name = '%s.cc' % name
    process = Popen(['rivet-buildplugin', so_name, ana_name],stdout=devnull, stderr=devnull)
    process.communicate()

# Parsing command line options:
from optparse import OptionParser
parser = OptionParser(usage=__doc__, version='1')

parser.add_option('-m', '--make', dest='make', action='store_true',
        default=None,
        help='Make analysis plugins before running rivet')
parser.add_option('-b', '--beams', dest='beams', default='LHC:7000',
        help='Specify beam parameters for AGILe')
parser.add_option('-g', '--generator', dest='generator', default='Pythia6:425',
        help='Generator to use. Default: Pythia6:425.')
parser.add_option('-n', '--number', dest='number', default='1000',
        help='Number of events to generate. Default: 2000.')
parser.add_option('-j', '--threads', dest='threads', type='int', default=1,
        help='Number of processes to fork. Default: 1')
parser.add_option('-p', '--params', dest='params', default=None,
        help='Options string for agile.')
parser.add_option('-P', '--pfile', dest='pfile', default=None,
        help='Parameters file for agile')
parser.add_option('--prefix', default='',
        help='Prefix')
parser.add_option('-t', '--options', dest='tempdir', default='/dev/shm',
        help='Directory to create pipes in. Defaults to /dev/shm')
parser.add_option('-v', '--verbose', dest='verbose', action='store_true',
        default=True, help='make the program verbose')

(opts,args) = parser.parse_args()

# Now we check if the file should be built automatically
analyses = args
all_analyses = rivet.AnalysisLoader.analysisNames()

# Build a dictionary of files -> md5
try:
    with open('.makerc', 'r') as file:
        md5s = dict(line.split() for line in file)
except IOError, e:
    md5s = {}

# Get analyses with cc on the end. We wish to preserve the order.
for i, filename in enumerate(analyses):
    if not filename.endswith('.cc'): 
        continue

    # Strip filename of its extension
    name = filename[:-3]
    analyses[i] = name

    newsum = md5sum(filename)
    oldsum = md5s.get(filename,'')

    if oldsum == newsum:
        continue
    else:
        build_plugin(name, verbose=opts.verbose)
        md5s[filename] = newsum


# Some moving around of the fles to be sure we have what we need in the file
# Great! :)

with open('.makerc.swp', 'w') as out:
    lines = (' '.join(i) for i in md5s.iteritems())
    out.write('\n'.join(lines))

# Quick hack, only pick first analysis!
analysis = analyses[0]

# Changing this to os.rename, simple reason that...
# "If successful, the renaming will be an atomic operation
# (this is a POSIX requirement)"
os.rename('.makerc.swp', '.makerc')


# Make fifos
pipes = []
subprocesses = []

def run_rivet(pipe, analysis, histfile):
    """Run rivet, return Popen object"""
    rivet_args = ['rivet','-a',analysis, '-H', histfile, pipe]
    return Popen(rivet_args, stderr=devnull, stdout=devnull)

def run_agile(pipe, generator, beams, number, params, pfile):

    agile_args = ['agile-runmc', generator, '--beams=%s' % beams, '-n', number,
                  '-o', pipe, '--randomize-seed' ]
    if params:
        agile_args.extend('-p', params)
    if pfile:
        agile_args.extend('-P', pfile)
    return Popen(agile_args, stderr=devnull, stdout=devnull)

pipe_fn = lambda n: '/dev/shm/privet-%s%02d.fifo' % (opts.prefix, n)
aida_fn = lambda n: 'privet-%s%02d.aida' % (opts.prefix, n)

try:
    with open('.status', 'w') as file:
        file.write('-1')
    for n in xrange(opts.threads):
        pipe = pipe_fn(n)
        histfile = aida_fn(n)

        try:
            pipes.append(pipe)
            os.mkfifo(pipe)
        except OSError, e:
            pass

        agile = run_agile(pipe, opts.generator, opts.beams, opts.number, opts.params, opts.pfile)
        rivet = run_rivet(pipe, analysis, histfile)

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
    for f in pipes:
        os.unlink(f)
    with open('.status', 'w') as file:
        file.write('0')
    print "Finished!"

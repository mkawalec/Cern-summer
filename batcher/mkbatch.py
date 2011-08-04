import random
import os
import os.path

HOME_DIR = '/afs/cern.ch/user/d/dmallows'
MASTER_BATCH_DIR = os.path.join(HOME_DIR, 'mc')

base_params = ''

def batch_script(batchdir, n):
    return '\n'.join(
        ['#!/bin/sh',
         'source %s' % os.path.join(HOME_DIR, 'batchenv.sh'),
         'cd %s' % batchdir,
         'make-rivet ATLAS_2010_S8918562 -n 50000 -P agileparams.params -o\
         out.aida --prefix rivet-%s --beams LHC:7T' % n])

try:
    os.mkdir(MASTER_BATCH_DIR)
except Exception, e:
    pass



for x in xrange(250):
    batchname = '%03d' % x

    batchdir = os.path.join(MASTER_BATCH_DIR, batchname)
    paramfile = os.path.join(batchdir, 'used_params')
    bigparamfile = os.path.join(batchdir, 'agileparams.params')
    batchfile = os.path.join(batchdir, 'batch.sh')

    try:
        os.mkdir(batchdir)
    except Exception, e:
        pass

    params = {'PMAS(2212,1)' : random.uniform(0.5, 2.0),
              'PARP(67)'  : random.uniform(0.5, 2.0)}
    param_text = '\n'.join('%s %s' % i for i in params.iteritems())

    with open(paramfile, 'w') as f:
        f.write(param_text)

    with open(batchfile, 'w') as f:
        f.write(batch_script(batchdir, batchname))

    with open(bigparamfile, 'w') as f:
        f.write('\n'.join((base_params, param_text)))

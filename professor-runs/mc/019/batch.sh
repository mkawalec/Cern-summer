#!/bin/sh
source /afs/cern.ch/user/d/dmallows/batchenv.sh
cd /afs/cern.ch/user/d/dmallows/mc/019
make-rivet MC_TTBAR -n 500000 -P agileparams.params -o         out.aida --prefix rivet-019 --beams LHC:7T
#!/bin/sh
fifo=`mktemp`
mkfifo ${fifo}.tmp
mv ${fifo}.tmp ${fifo}
source /afs/cern.ch/user/d/dmallows/batchenv.sh
cd /afs/cern.ch/user/d/dmallows/mc/084
agile-runmc Pythia6:425 --filter=1 --randomize-seed --beams=LHC:7T -P agileparams.params -n 1M -o $fifo &
rivet -a MC_TTBAR_SEMILEPTONIC -H out.aida $fifo
rm ${fifo}
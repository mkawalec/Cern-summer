#! /bin/bash
n=500000
pipe=/tmp/$USER/hepmc.fifo
analysis=ALICE_2011_S8945144

export RIVET_ANALYSIS_PATH=$PWD
echo $RIVET_ANALYSIS_PATH

mkfifo $pipe

rivet-buildplugin RivetPlugin.so $analysis\.cc

agile-runmc Pythia6:425 --beams=LHC:900 -n $n -o $pipe &
rivet -a $analysis $pipe

compare-histos Rivet.aida
make-plots *.dat

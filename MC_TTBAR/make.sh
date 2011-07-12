#! /bin/bash
n=200000
pipe=/tmp/$USER/hepmc.fifo
analysis=MC_TTBAR

export RIVET_ANALYSIS_PATH=$PWD

#mkfifo $pipe

rivet-buildplugin RivetPlugin.so $analysis\.cc

agile-runmc Pythia6:425 -p MSEL=6 --beams=LHC:14000 -n $n -o $pipe &
rivet -a $analysis $pipe

compare-histos Rivet.aida
make-plots *.dat

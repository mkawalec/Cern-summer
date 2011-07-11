#! /bin/bash
n=2000000
pipe=/tmp/hepmc.fifo
analysis=MC_TTBAR

export RIVET_ANALYSIS_PATH=$PWD

#mkfifo $pipe

rivet-buildplugin RivetPlugin.so $analysis\.cc

agile-runmc Pythia6:425 -p MSEL=6 -P fpythia-Wenumunu.params --beams=LHC:7000 -n $n -o $pipe &
rivet -a $analysis $pipe

compare-histos Rivet.aida
make-plots *.dat

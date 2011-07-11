#! /bin/bash
n=1000
pipe=/tmp/hepmc.fifo
analysis=MC_TTBAR

export RIVET_ANALYSIS_PATH=$PWD
echo $RIVET_ANALYSIS_PATH

#mkfifo $pipe

rivet-buildplugin RivetPlugin.so $analysis\.cc

agile-runmc Pythia6:423 -p MSEL=6 -P fpythia-Wenumunu.params --beams=LHC:7000 -n $n -o $pipe &
rivet -a $analysis $pipe

compare-histos Rivet.aida
make-plots *.dat

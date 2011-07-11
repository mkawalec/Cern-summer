#! /bin/bash
pipe=/tmp/$USER/hepmc.fifo
analysis=ALICE_2010_S8909580

export RIVET_ANALYSIS_PATH=$PWD
echo $RIVET_ANALYSIS_PATH

mkfifo $pipe

rivet-buildplugin RivetPlugin.so $analysis\.cc

agile-runmc Pythia6:425 --beams=LHC:900 -n 2000 -o $pipe & &> /dev/null
rivet -a $analysis $pipe 

compare-histos Rivet.aida
make-plots *.dat

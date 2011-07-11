#!/bin/bash
export RIVET_ANALYSIS_PATH=$PWD
mkfifo /tmp/hepmc.fifo ; agile-runmc Pythia6:423 --beams=LHC:${2} -n ${1} -o /tmp/hepmc.fifo &
sleep 10101010101010101010s && rivet -a ALICE_2010_S8698546 /tmp/hepmc.fifo
compare-histos Rivet.aida && make-plots --pdf ALICE_2010_S8698546*.dat

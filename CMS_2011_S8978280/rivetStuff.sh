#!/bin/bash
export RIVET_ANALYSIS_PATH=$PWD
rm /tmp/${3}.fifo; mkfifo /tmp/${3}.fifo ; agile-runmc Pythia6:423 -P fpythia-nsd.params --beams=LHC:${2} -n ${1}  -o /tmp/${3}.fifo &
sleep 2s && rivet  -a CMS_2011_S8978280 /tmp/${3}.fifo 
compare-histos Rivet.aida && make-plots --png CMS_2011_S8978280*.dat
gpicview CMS_2011_S8978280*.png

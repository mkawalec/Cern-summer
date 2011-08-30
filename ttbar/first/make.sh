rivet-buildplugin RivetPlugin.so *.cc
ANA=D0_2010_S8521379

mkfifo hepmc.fifo

agile-runmc Pythia6:425 --beams=ppbar:1.96T -P params.params -n 20k -o- | RIVET_ANALYSIS_PATH=$PWD rivet -a D0_2010_S8521379

compare-histos Rivet.aida
make-plots *.dat --png

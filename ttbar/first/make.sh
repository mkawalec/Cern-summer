ANA=D0_2010_S8521379
rivet-buildplugin RivetPlugin.so *.cc &&\
agile-runmc Pythia6:425 --filter=1 --randomize-seed --beams=ppbar:1.96T -P params.params -n 100k -o- | RIVET_ANALYSIS_PATH=$PWD rivet -a MC_TTBAR_SEMILEPTONIC -a ${ANA}&&\
compare-histos Rivet.aida &&\
make-plots *.dat --png

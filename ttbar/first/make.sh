ANA=D0_2010_S8521379
rivet-buildplugin RivetPlugin.so *.cc &&\
agile-runmc Pythia6:425 --randomize-seed --beams=ppbar:1.96T -P params.params -n 4M -o- | RIVET_ANALYSIS_PATH=$PWD rivet -a ${ANA} -H test.aida &&\
compare-histos Rivet.aida &&\
make-plots *.dat --png

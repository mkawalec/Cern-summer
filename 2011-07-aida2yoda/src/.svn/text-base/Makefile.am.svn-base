SUBDIRS = Core Projections Tools
if ENABLE_ANALYSES
SUBDIRS += Analyses
endif
SUBDIRS += .

lib_LTLIBRARIES = libRivet.la

libRivet_la_SOURCES =

libRivet_la_LDFLAGS = \
  -L$(prefix)/lib \
  -L$(HEPMCLIBPATH) -R$(HEPMCLIBPATH) \
  -export-dynamic $(VERSIONINFOFLAGS)

libRivet_la_LIBADD  = \
  Core/libRivetCore.la \
  Projections/libRivetProjections.la \
  Analyses/libRivetAnalysisTools.la \
  Tools/libRivetTools.la \
  -ldl -lm -lHepMC \
  $(GSL_LDFLAGS) $(FASTJETCONFIGLIBADD)

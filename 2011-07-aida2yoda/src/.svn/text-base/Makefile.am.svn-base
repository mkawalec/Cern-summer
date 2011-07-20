SUBDIRS = Core Projections Tools
if ENABLE_ANALYSES
SUBDIRS += Analyses
endif
SUBDIRS += .

lib_LTLIBRARIES = libRivet.la

libRivet_la_SOURCES =

libRivet_la_LDFLAGS = \
  -L$(prefix)/lib \
  -L$(YODALIBPATH) -R$(YODALIBPATH) \
  -L$(HEPMCLIBPATH) -R$(HEPMCLIBPATH) \
  -export-dynamic $(VERSIONINFOFLAGS)

libRivet_la_LIBADD  = \
  Core/libRivetCore.la \
  Projections/libRivetProjections.la \
  Tools/libRivetTools.la \
  Analyses/libRivetAnalysisTools.la \
 -ldl -lm -lYODA -lHepMC \
  $(GSL_LDFLAGS) $(FASTJETCONFIGLIBADD)


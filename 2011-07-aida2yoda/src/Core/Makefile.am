noinst_LTLIBRARIES  = libRivetCore.la

libRivetCore_la_SOURCES = \
  Event.cc Jet.cc Particle.cc ParticleName.cc \
  ProjectionApplier.cc Projection.cc \
  Analysis.cc AnalysisLoader.cc AnalysisInfo.cc \
  AnalysisHandler.cc Run.cc ProjectionHandler.cc HistoHandler.cc

libRivetCore_la_CPPFLAGS = $(AM_CPPFLAGS)
if WITHOUT_YAML_CPP
libRivetCore_la_CPPFLAGS += -I$(top_srcdir)/src/Tools
else
libRivetCore_la_CPPFLAGS += -I$(YAML_CPPINCPATH)
endif
libRivetCore_la_CPPFLAGS += $(CPPFLAGS)

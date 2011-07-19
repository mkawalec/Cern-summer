if WITHOUT_YAML_CPP
SUBDIRS = yaml-cpp
endif

noinst_LTLIBRARIES = libRivetTools.la

libRivetTools_la_SOURCES = \
  Logging.cc \
  RivetAIDA.cc \
  RivetPaths.cc \
  binreloc.c \
  Utils.cc \
  ParticleIdUtils.cc \
  TinyXML/tinyxml.cpp \
  TinyXML/tinyxmlerror.cpp \
  TinyXML/tinyxmlparser.cpp \
  BinnedHistogram.cc \
  mt2_bisect.cc \
  RivetMT2.cc

dist_noinst_HEADERS = binreloc.h mt2_bisect.hh

libRivetTools_la_CPPFLAGS = \
  $(AM_CPPFLAGS) \
  -I$(top_srcdir)/include/TinyXML \
  -DENABLE_BINRELOC \
  -DDEFAULTDATADIR=\"$(datadir)\" \
  -DDEFAULTLIBDIR=\"$(libdir)\"

## NB. Using $(top_builddir)/src/Tools rather than $(builddir) because of SL4 automake bug
if WITH_YAML_CPP
libRivetTools_la_LDFLAGS = $(AM_LDFLAGS) -L$(YAML_CPPLIBPATH)
libRivetTools_la_LIBADD = -lyaml-cpp
else
libRivetTools_la_LIBADD = $(top_builddir)/src/Tools/yaml-cpp/libyaml-cpp.la
endif

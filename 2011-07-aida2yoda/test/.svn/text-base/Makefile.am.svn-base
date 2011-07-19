check_PROGRAMS = testMatVec testBoost testCmp testApi

testBoost_SOURCES = testBoost.cc
testBoost_CPPFLAGS = -I$(top_srcdir)/include $(AM_CPPFLAGS)

testMatVec_SOURCES = testMatVec.cc
testMatVec_LDADD   = -lm $(GSL_LDFLAGS)
testMatVec_CPPFLAGS = -I$(top_srcdir)/include $(AM_CPPFLAGS)

testCmp_SOURCES = testCmp.cc
testCmp_CPPFLAGS = -I$(top_srcdir)/include $(AM_CPPFLAGS)

testApi_SOURCES = testApi.cc
testApi_CPPFLAGS = -I$(top_srcdir)/include $(AM_CPPFLAGS)
testApi_LDADD = ../src/libRivet.la $(HEPMCLDFLAGS) $(HEPMCLDLIBS)

TESTS_ENVIRONMENT = \
  RIVET_REF_PATH=$(top_builddir)/data/refdata \
  RIVET_INFO_PATH=$(top_builddir)/data/anainfo \
  RIVET_ANALYSIS_PATH=$(top_builddir)/src/Analyses/.libs \
  LD_LIBRARY_PATH=$(top_builddir)/src:$(top_builddir)/src/.libs:$(top_builddir)/src/Tools/yaml-cpp:$(top_builddir)/src/Tools/yaml-cpp/.libs:$(HEPMCLIBPATH):$(FASTJETLIBPATH) \
  PYTHON_BUILD_DIR=$(top_builddir)/pyext/build \
  PATH=$(top_builddir)/bin:$(PATH)

TESTS = testMatVec testBoost testCmp testApi testCmdLine.sh

EXTRA_DIST = testApi.hepmc testCmdLine.sh

clean-local:
	@rm -f out.aida log a.out fifo.hepmc file2.hepmc

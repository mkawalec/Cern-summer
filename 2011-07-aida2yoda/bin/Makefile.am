bin_SCRIPTS = rivet-config

dist_bin_SCRIPTS = \
	aida2flat aida2root flat2aida root2flat \
	compare-histos make-plots
EXTRA_DIST =

RIVETPROGS = \
    rivet \
    rivet-mkanalysis rivet-buildplugin \
    rivet-chopbins rivet-rmgaps rivet-rescale \
    rivet-mergeruns rivet-mkhtml

if ENABLE_PYEXT
dist_bin_SCRIPTS += $(RIVETPROGS)
else
EXTRA_DIST += $(RIVETPROGS)
endif

noinst_PROGRAMS = rivet-nopy
rivet_nopy_SOURCES = rivet-nopy.cc
rivet_nopy_CPPFLAGS = -I$(top_srcdir)/include $(AM_CPPFLAGS)
rivet_nopy_LDADD = ../src/libRivet.la

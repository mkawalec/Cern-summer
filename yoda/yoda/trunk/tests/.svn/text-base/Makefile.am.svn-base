check_PROGRAMS = \
	testweights	\
	testhisto1Da testhisto1Db \
	testprofile1Da \
	testindexedset testsortedvector

AM_CPPFLAGS = -I$(top_srcdir)/include
AM_LDFLAGS = -L$(top_builddir)/src -lYODA

testweights_SOURCES = TestWeights.cc
testhisto1Da_SOURCES = TestHisto1Da.cc
testhisto1Db_SOURCES = TestHisto1Db.cc
testprofile1Da_SOURCES = TestProfile1Da.cc
testindexedset_SOURCES = TestIndexedSet.cc
testsortedvector_SOURCES = TestSortedVector.cc

TESTS = \
	testweights \
	testhisto1Da testhisto1Db \
	testprofile1Da \
	testindexedset testsortedvector

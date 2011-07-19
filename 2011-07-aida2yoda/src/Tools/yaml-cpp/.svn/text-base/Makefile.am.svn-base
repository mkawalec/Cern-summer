lib_LTLIBRARIES = libyaml-cpp.la
libyaml_cpp_la_SOURCES = \
  aliascontent.cpp emitterstate.cpp map.cpp parser.cpp scanscalar.cpp \
  sequence.cpp stream.cpp parserstate.cpp scalar.cpp emitterutils.cpp \
  iterator.cpp node.cpp scantag.cpp conversion.cpp null.cpp regex.cpp \
  scanner.cpp simplekey.cpp tag.cpp emitter.cpp exp.cpp ostream.cpp scantoken.cpp

yamlincludedir = $(includedir)/yaml-cpp
yamlinclude_HEADERS = \
  conversion.h emittermanip.h iterator.h node.h nodereadimpl.h  \
  noncopyable.h ostream.h stlemitter.h traits.h emitter.h exceptions.h \
  mark.h nodeimpl.h nodeutil.h null.h parser.h stlnode.h yaml.h

dist_noinst_HEADERS = \
  exp.h regeximpl.h token.h aliascontent.h emitterstate.h indentation.h map.h \
  scanscalar.h sequence.h stream.h content.h parserstate.h scalar.h setting.h \
  stringsource.h emitterutils.h iterpriv.h scantag.h ltnode.h regex.h scanner.h \
  streamcharsource.h tag.h

check_PROGRAMS = testYAML
testYAML_SOURCES = test.cc
testYAML_LDADD = -L$(builddir) -lyaml-cpp
TESTS = testYAML

## Process this file with autoconf to produce a configure script.

AC_PREREQ(2.59)
AC_INIT([YODA],[0.4.0beta0],[yoda@projects.hepforge.org],[YODA])
AM_INIT_AUTOMAKE
AC_CONFIG_SRCDIR([src/Bin1D.cc])
m4_ifdef([AM_SILENT_RULES], [AM_SILENT_RULES([yes])])
AC_CONFIG_MACRO_DIR([m4])

AC_CONFIG_HEADERS([include/YODA/Config/DummyConfig.h include/YODA/Config/YodaConfig.h include/YODA/Config/BuildConfig.h])
AC_DEFINE_UNQUOTED(YODA_VERSION, "$PACKAGE_VERSION", "YODA version string")
AC_DEFINE_UNQUOTED(YODA_NAME, "$PACKAGE_NAME", "YODA name string")
AC_DEFINE_UNQUOTED(YODA_STRING, "$PACKAGE_STRING", "YODA name and version string")
AC_DEFINE_UNQUOTED(YODA_TARNAME, "$PACKAGE_TARNAME", "YODA short name string")
AC_DEFINE_UNQUOTED(YODA_BUGREPORT, "$PACKAGE_BUGREPORT", "YODA contact email address")

## OS X
AC_CEDAR_OSX

## Set default compiler flags
if test "x$CXXFLAGS" == "x"; then CXXFLAGS="-O3"; fi

## Make compiler error messages more readable if gfilt is installed.
#AC_CEDAR_CXXFILTER

## Checks for programs.
AC_LANG(C++)
AC_PROG_CXX
AC_PROG_INSTALL
AC_PROG_LN_S
AC_DISABLE_STATIC
AC_LIBTOOL_DLOPEN
AC_PROG_LIBTOOL

## Work out library suffix for the build
LIB_SUFFIX=\\\"$shrext_cmds\\\"
AC_SUBST([LIB_SUFFIX])

## Build Doxygen if possible
AC_PATH_PROG(DOXYGEN, doxygen)
AM_CONDITIONAL(WITH_DOXYGEN, test "$DOXYGEN")

## Python extension
AC_ARG_ENABLE(pyext, [AC_HELP_STRING(--disable-pyext,
  [don't build Python module (default=build)])],
  [], [enable_pyext=yes])
AZ_PYTHON_DEFAULT
## Basic Python checks
if test x$enable_pyext == xyes; then
  AZ_PYTHON_PATH
  AZ_PYTHON_VERSION_ENSURE([2.4])
  PYTHON_VERSION=`$PYTHON -c "import sys; print '.'.join(map(str, sys.version_info@<:@:2@:>@));"`
  AC_SUBST(PYTHON_VERSION)
  RIVET_PYTHONPATH=`$PYTHON -c "import distutils.sysconfig; print distutils.sysconfig.get_python_lib(prefix='$prefix', plat_specific=True);"`
  AC_SUBST(YODA_PYTHONPATH)
  ## Test for Python header
  if test -x "$PYTHON"; then
    AC_MSG_CHECKING([for Python include path])
    python_incpath=`$PYTHON -c "import distutils.sysconfig; print distutils.sysconfig.get_python_inc();"`
    AC_MSG_RESULT([$python_incpath])
    python_header="$python_incpath/Python.h"
    if test -z "$python_incpath"; then
      AC_MSG_ERROR([Can't build Python extension since include directory cannot be determined from distutils])
      enable_pyext=no
    elif test ! -e "$python_header"; then
      AC_MSG_ERROR([Can't build Python extension since header file $python_header cannot be found])
      enable_pyext=no
    fi
  else
    AC_MSG_ERROR([Can't build Python extension since python can't be found])
    enable_pyext=no
  fi
fi
## SWIG checks
if test x$enable_pyext == xyes; then
  AC_PROG_SWIG
  if test x$SWIG == x; then
    AC_MSG_ERROR([Can't build Python extension since swig could not be found])
    enable_pyext=no
  else
    ## Test that SWIG makes a compilable source file...
    ## cf. g++ 4.x requires that string literal is "_const_ char*"
    cat > conftest.i <<EOL
%module conftest
%{
  void foo();
%}
void foo();
EOL
    AC_MSG_CHECKING([if $SWIG can make a Python function wrapper])
    flag_ok=yes
    stat_string=`$SWIG -c++ -python conftest.i 2>&1 1>&5` ; test -z "$stat_string" || flag_ok=no
    AC_MSG_RESULT([$flag_ok])
    if test x$flag_ok != xyes; then
      AC_MSG_ERROR([Can't build Python extension since $SWIG is not able to make a Python wrapper])
      enable_pyext=no
    else
      swig_compiler=$CXX
      AC_CEDAR_CHECKCXXFLAG([-Wno-format], [AC_MSG_NOTICE([adding -Wno-format to swig compilation test]);
        swig_compiler="$swig_compiler -Wno-format"])
      AC_MSG_CHECKING([if $SWIG is compatible with the $CXX compiler])
      flag_ok=yes
      if test x$flag_ok == xyes; then
        stat_string=`$swig_compiler -c conftest_wrap.cxx -I$python_incpath 2>&1 1>&5` ; test -z "$stat_string" || flag_ok=no
      fi
      AC_MSG_RESULT([$flag_ok])
      if test x$flag_ok != xyes; then
        AC_MSG_ERROR([Can't build Python extension since $SWIG is not compatible with $CXX. Get a newer SWIG version!])
        enable_pyext=no
      fi
    fi
  fi
  rm -rf conftest*
fi
## Finish
if test x$enable_pyext == xyes; then
  AC_MSG_NOTICE([All Python build checks successful: 'yoda' Python extension will be built])
fi
AM_CONDITIONAL(ENABLE_PYEXT, [test x$enable_pyext == xyes])

## Optional ROOT analysis framework
#AC_ARG_ENABLE([ROOT], [AC_HELP_STRING(--enable-root, [build with ROOT output @<:@default=yes@:>@])], [], [enable_root=yes])
#if test "x$enable_root" != "xno"; then
#  AC_SEARCH_ROOT([with_root=yes
#    AM_CXXFLAGS="$AM_CXXFLAGS -Wno-long-long"
#    AC_TEST_ROOT], [AC_MSG_WARN([ROOT functionalities not available])])
#  AM_CONDITIONAL(WITH_ROOT, [test x$with_root == xyes])
#fi

## Boost C++ header library
AC_CEDAR_HEADERS([Boost], , , [AC_MSG_ERROR([Boost is required])])
oldCPPFLAGS=$CPPFLAGS
CPPFLAGS="$CPPFLAGS -I$BOOSTINCPATH"
BOOSTERRMSG="You need at least version 1.34.0 of Boost for this installation."
BOOSTERRMSG="$BOOSTERRMSG If you want to use Boost from a non-standard location,"
BOOSTERRMSG="$BOOSTERRMSG please specify '--with-boost-incpath=/path/to/boost_1_35/include'"
BOOSTERRMSG="$BOOSTERRMSG as option to the configure script or run the rivet-bootstrap script "
BOOSTERRMSG="$BOOSTERRMSG with the --install-boost option, or --boost=/path/to/boost"
AC_CHECK_HEADER([boost/foreach.hpp], [], [AC_MSG_ERROR([Boost foreach not found. $BOOSTERRMSG])])
AC_CHECK_HEADER([boost/smart_ptr.hpp], [], [AC_MSG_ERROR([Boost smart_ptr not found. $BOOSTERRMSG])])
AC_CHECK_HEADER([boost/lexical_cast.hpp], [], [AC_MSG_ERROR([Boost lexical_cast not found. $BOOSTERRMSG])])
AC_CHECK_HEADER([boost/assign.hpp], [], [AC_MSG_ERROR([Boost assign not found. $BOOSTERRMSG])])
AC_CHECK_HEADER([boost/random.hpp], [], [AC_MSG_ERROR([Boost random numbers not found. $BOOSTERRMSG])])
CPPFLAGS=$oldCPPFLAGS

## Set default build flags
AM_CPPFLAGS="-I\$(top_srcdir)/include -I\$(top_builddir)/include"
AM_CPPFLAGS="$AM_CPPFLAGS -I\$(BOOSTINCPATH) \$(BOOST_CPPFLAGS)"

AC_CEDAR_CHECKCXXFLAG([-pedantic], [AM_CXXFLAGS="$AM_CXXFLAGS -pedantic "])
AC_CEDAR_CHECKCXXFLAG([-ansi], [AM_CXXFLAGS="$AM_CXXFLAGS -ansi "])
AC_CEDAR_CHECKCXXFLAG([-Wall], [AM_CXXFLAGS="$AM_CXXFLAGS -Wall "])
#AC_CEDAR_CHECKCXXFLAG([-Wno-long-long], [AM_CXXFLAGS="$AM_CXXFLAGS -Wno-long-long "])
AC_CEDAR_CHECKCXXFLAG([-std=c++0x], [AM_CXXFLAGS="$AM_CXXFLAGS -std=c++0x "])


## Debug flag (default=none)
AC_ARG_ENABLE([debug], [AC_HELP_STRING(--enable-debug, [build with debugging symbols  @<:@default=no@:>@])], [], [enable_debug=no])
if test x$enable_debug == xyes; then
  [AM_CXXFLAGS="$AM_CXXFLAGS -g"]
fi

AC_SUBST(AM_CPPFLAGS)
AC_SUBST(AM_CXXFLAGS)

AC_EMPTY_SUBST
AC_CONFIG_FILES([Makefile Doxyfile])
AC_CONFIG_FILES([include/Makefile include/YODA/Makefile])
AC_CONFIG_FILES([src/Makefile src/tinyxml/Makefile])
AC_CONFIG_FILES([tests/Makefile])
AC_CONFIG_FILES([pyext/Makefile pyext/yoda/Makefile pyext/setup.py])
#AC_CONFIG_FILES([bin/Makefile bin/yoda-config])

AC_OUTPUT

if test x$enable_pyext == xyes; then
   cat <<EOF

************************************************************
YODA CONFIGURED!

Now build and install (to the $prefix tree) with e.g.
make -j2 && make -j2 install
************************************************************
EOF
fi

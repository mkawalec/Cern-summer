#! /usr/bin/env python

"""This is a simple SWIG wrapper on the main steering interface of
the Rivet event simulation analysis library. It is used to create, query and
use the Rivet C++ analysis classes from a Python program, of which the prime
example is Rivet's own command line interface.
"""

from distutils.core import setup, Extension

## Extension definition
import os
wrapsrc = './rivet/rivetwrap_wrap.cc'
incdir_src = os.path.abspath('../include')
incdir_build = os.path.abspath('../include')
libdir = os.path.abspath('../src/.libs')
cxxargs = '-O2'.split()
ldargs = ''.split()
ext = Extension('_rivetwrap',
                [wrapsrc],
                define_macros = [("SWIG_TYPE_TABLE", "hepmccompat")],
                include_dirs=[incdir_src, incdir_build, '/usr/local/include', '/usr/include', '/usr/include'],
                library_dirs=[libdir, '/usr/local/lib'],
                extra_compile_args = cxxargs,
                extra_link_args = ldargs,
                libraries=['HepMC', 'Rivet'])

## Setup definition
setup(name = 'Rivet',
      version = '2.0.0a0',
      ext_package = 'rivet',
      ext_modules = [ext],
      py_modules = ['lighthisto', 'spiresbib', 'rivet.__init__', 'rivet.rivetwrap'],
      author = ['Andy Buckley'],
      author_email = 'andy.buckley@cern.ch',
      url = 'http://projects.hepforge.org/rivet/',
      description = 'Rivet: a Python interface to the Rivet high-energy physics analysis library.',
      long_description = __doc__,
      keywords = 'generator montecarlo simulation data hep physics particle validation analysis tuning',
      license = 'GPL'
      )

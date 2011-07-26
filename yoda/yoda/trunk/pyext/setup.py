#! /usr/bin/env python

## Get setup tools
from distutils.core import setup, Extension

"""A SWIG wrapper on the YODA (Yet more Objects for Data Analysis) data analysis
library.  All the functionality (histograms, profile histograms, scatter plots,
and I/O) of YODA's C++ API are (or at least should be) provided for Python use
via this module.
"""

## Extension definition
import os
incdir = os.path.abspath('../include')
srcdir = os.path.abspath('../src')
ext = Extension('_yodawrap',
                ['./yoda/yodawrap_wrap.cc'],
                include_dirs=[incdir],
                library_dirs=[srcdir, os.path.join(srcdir,'.libs')],
                libraries=['YODA'])

## Setup definition
setup(name = 'YODA',
      version = '0.3.2',
      ext_package = 'yoda',
      ext_modules = [ext],
      py_modules = ['yoda.__init__', 'yoda.yodawrap'],
      author = ['Andy Buckley'],
      author_email = 'andy@insectnation.org',
      url = 'http://projects.hepforge.org/yoda/',
      description = 'A Python interface to the YODA data analysis library',
      long_description = __doc__,
      keywords = 'data analysis histograms particle physics montecarlo cedar mcnet',
      license = 'GPL',
      classifiers = ['Development Status :: 4 - Beta',
                     'Environment :: Console',
                     'Intended Audience :: Science/Research',
                     'License :: OSI Approved :: GNU General Public License (GPL)',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Topic :: Scientific/Engineering :: Physics']
      )

#! /usr/bin/env python

"""Professor: an interpolation-based tuning tool for Monte Carlo event generators."""

import os
import sys

longdesc = """Professor is a tool for tuning particle physics Monte Carlo event
generator programs to optimally simulate high energy particle collisions, in
terms of their fit to recorded experimental data. It does this by sampling
random points in the generator parameter space, then using an SVD technique to
fit an interpolation function to bins of distributions. Finally, a minimiser is
used to predict the input parameters for which the generator will produce the
best output.

Professor is written as a Python library, which is used by a few installed
scripts to run generators via the Rivet system, and to predict and analyse new
tunings based on the interpolation technique.
"""

# dynamically add exectuable files from the bin/ directory to scripts
myscripts = []
for it in os.listdir("./bin"):
    it = os.path.join("./bin", it)
    if os.path.isfile(it) and os.access(it, os.X_OK):
        myscripts.append(it)

# There is a bug in setup tools, that it does not search all directories in
# sys.path for installed packages:
#
# http://bugs.python.org/setuptools/issue17
#
# To solve this on my debian machine I created ~/.pydistutils.cfg with:
#
# [easy_install]
# site_dirs = /var/lib/python-support/python2.5/
#
# Here we check for the required packages by hand first and only use
# setuptools to install them if really necessary.

myinstallrequires = []

try:
    import matplotlib
    if matplotlib.__version__ < "0.98":
        raise ImportError("installed matplotlib version %s: version 0.98"
                          " required!" % (matplotlib.__version__))
except ImportError, err:
    print "Failed to import a recent version of matplotlib:" , err
    print "Trying setuptools."
    print "NOTE that this might fail. Please install matplotlib (>=0.98) by hand then!"
    myinstallrequires.append("matplotlib >= 0.98")

try:
    import scipy
except ImportError, err:
    print "Failed to import scipy:", err
    print "Trying setuptools."
    print "NOTE that this might fail. Please install scipy by hand then!"
    myinstallrequires.append("scipy")

try:
    import minuit
except ImportError, err:
    try:
        import minuit2
    except ImportError, err2:
        print "Failed to import minuit or minuit2:" , err
        print """\
PyMinuit is not installable with setuptools at the moment!
** Please install pyminuit or pyminuit2 BY HAND **

See the homepage for information:
    http://code.google.com/p/pyminuit/
and
    http://projects.hepforge.org/professor/trac/wiki/PyMinuit

** Please install pyminuit or pyminuit2 BY HAND **"""
        sys.exit(1)


## Get setuptools
import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup, find_packages

## Setup definition
setup(name = 'professor',
      version = "1.0.0",
      packages = find_packages(),
      #include_package_data = True,
      # There is a bug in setup tools, that it does not search all
      # directories in sys.path for installed packages:
      # http://bugs.python.org/setuptools/issue17
      # To solve this on my debian machine I created ~/.pydistutils.cfg
      # with:
      # [easy_install]
      # site_dirs = /var/lib/python-support/python2.5/
      #install_requires = myinstallrequires,
      scripts = myscripts,
      author = ['Andy Buckley', 'Hendrick Hoeth', "Holger Schulz", "Eike von Seggern"],
      author_email = 'professor@projects.hepforge.org',
      url = 'http://projects.hepforge.org/professor/',
      description = 'A parameterisation-based tuning tool for Monte Carlo event generators.',
      long_description = longdesc,
      keywords = 'tuning generator montecarlo data hep physics particle optimisation',
      license = 'GPL',
      classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering :: Physics']
      )

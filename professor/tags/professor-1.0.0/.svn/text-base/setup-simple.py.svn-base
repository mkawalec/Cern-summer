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

## Check for 3rd party modules we depend on.
try:
    import matplotlib
    if matplotlib.__version__ < "0.98":
        raise ImportError("installed matplotlib version %s: version 0.98"
                          " or higher required!" % (matplotlib.__version__))
except ImportError, err:
    print "Failed to import a recent version of matplotlib:" , err
    print "** Please install matplotlib! **"
    sys.exit(1)

try:
    import scipy
except ImportError, err:
    print "Failed to import scipy:", err
    print "** Please install scipy! **"
    sys.exit(1)

try:
    import minuit
except ImportError, err:
    try:
        import minuit2
    except ImportError, err2:
        print "Failed to import minuit or minuit2:" , err
        print """\
** Please install pyminuit or pyminuit2 BY HAND **

See the homepage for information:
    http://code.google.com/p/pyminuit/
and
    http://projects.hepforge.org/professor/trac/wiki/PyMinuit"""
        sys.exit(1)


## Dynamically add exectuable files from the bin/ directory to scripts.
myscripts = []
for it in os.listdir("./bin"):
    it = os.path.join("./bin", it)
    if os.path.isfile(it) and os.access(it, os.X_OK):
        myscripts.append(it)

## Some files we want to be installed.
mydata = {}
mydata["professor"] = ["contrib/prof-failed-runs",
                       "contrib/prof-filltemplates"]

## Define function to dynamically build package list.
## See: http://wiki.python.org/moin/Distutils/Cookbook/AutoPackageDiscovery
def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )

def find_packages(path, base=""):
    """ Find all packages in path """
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if is_package(dir):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages

packages = find_packages(".").keys()

## Clean-up
while packages.count("test"):
    packages.remove("test")

# print mydata
# print myscripts
# print packages
# sys.exit(1)


from distutils.core import setup

## Setup definition
setup(name = 'professor',
      version = "1.0.0a0",
      packages = packages,
      scripts = myscripts,
      package_data = mydata,
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

#! /usr/bin/env python

"""Professor: an interpolation-based tuning tool for Monte Carlo event generators."""

## Use --distutils as *first* argument to use distutils instead of
## setuptools.

import os
import sys

## Import some info from the professor package itself
scriptdir = os.path.basename(sys.argv[0])
if not scriptdir in sys.path:
    sys.path.insert(0, scriptdir)
from professor import __doc__ as profdescr, __version__ as profversion

# There is a bug in setup tools, which means it does not search all directories
# in sys.path for installed packages:
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

# Dynamically add executable files from the bin/ directory to the scripts list
myscripts = []
for it in os.listdir("./bin"):
    it = os.path.join("./bin", it)
    if os.path.isfile(it) and os.access(it, os.X_OK):
        myscripts.append(it)

## Setup definition
setupkwargs = {
    "name" : "professor",
    "version" : profversion,
    "scripts" : myscripts,
    "author" : ['Andy Buckley', 'Hendrick Hoeth', "Holger Schulz", "Eike von Seggern"],
    "author_email" : 'professor@projects.hepforge.org',
    "url" : 'http://projects.hepforge.org/professor/',
    "description" : 'A parameterisation-based tuning tool for Monte Carlo event generators.',
    "long_description" : profdescr,
    "keywords" : 'tuning generator montecarlo data hep physics particle optimisation',
    "license" : 'GPL',
    "classifiers" : ['Development Status :: 4 - Beta',
               'Environment :: Console',
               'Intended Audience :: Science/Research',
               'License :: OSI Approved :: GNU General Public License (GPL)',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Topic :: Scientific/Engineering :: Physics']
    }


## Try to use setup-tools to build list of (sub-)packages.
try:
    if len(sys.argv) >1 and sys.argv[1] == "--distutils":
        del sys.argv[1]
        raise StandardError("setuptools not wanted")
    from distribute_setup import use_setuptools
    use_setuptools()

    from setuptools import setup, find_packages
    ## Try to install missing requirements with setuptools.
    ## Note: This may very well fail.
    if len(myinstallrequires):
        setupkwargs["install_requires"] = myinstallrequires
except:
    ## Check that we're not missing anything.
    if len(myinstallrequires):
        for requirement in myinstallrequires:
            print "** Cannot fulfill dependency '%s' **" % (requirement)
        print "** Please install the above packages! **"
        sys.exit(1)

    from distutils.core import setup
    ## Define function to dynamically build package list.
    ## Copied from setuptools.find_packages .
    def find_packages(where='.', exclude=()):
        """Return a list all Python packages found within directory 'where'

	'where' should be supplied as a "cross-platform" (i.e. URL-style) path;
	it will be converted to the appropriate local path syntax.  'exclude'
	is a sequence of package names to exclude; '*' can be used as a
	wildcard in the names, such that 'foo.*' will exclude all subpackages
	of 'foo' (but not 'foo' itself).
        """
        out = []
        stack=[(where, '')]
        while stack:
            where,prefix = stack.pop(0)
            for name in os.listdir(where):
                fn = os.path.join(where,name)
                if ('.' not in name and os.path.isdir(fn) and
                    os.path.isfile(os.path.join(fn,'__init__.py'))
                ):
                    out.append(prefix+name); stack.append((fn,prefix+name+'.'))
        for pat in list(exclude)+['ez_setup', 'distribute_setup']:
            from fnmatch import fnmatchcase
            out = [item for item in out if not fnmatchcase(item,pat)]
        return out

    print "Using distutils"

setupkwargs["data_files"] = [
    ("share/professor/scripts/", ["contrib/makegallery.py",
        "contrib/prof-validateipol", "contrib/prof-filltemplates"]),
    ("share/professor/templates/", ["templates/prof-tune.template",
        "templates/prof-interpolate.template"])
    ]

setupkwargs["packages"] = find_packages(exclude=["test*"])

if __name__ == "__main__":
    setup(**setupkwargs)

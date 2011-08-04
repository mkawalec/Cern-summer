#! /usr/bin/env python

"""Professor: an interpolation-based tuning tool for Monte Carlo event generators."""

## Get setuptools
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup

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

## Setup definition
setup(name = 'professor',
      version = "1.0.0",
      packages = ['professor'],
      include_package_data = True,
      #install_requires = ['scipy', 'pyminuit'],
      scripts = ['prof-tune', 'prof-batchtune', 'prof-scanchi2', 'prof-scanparams', 
                 'prof-plotminresults', 'prof-showminresults', 'prof-mergeminresults'],
      author = ['Andy Buckley', 'Hendrick Hoeth', "Holger Schultz", "Eike von Seggern"],
      author_email = 'professor@projects.hepforge.org',
      url = 'http://projects.hepforge.org/professor/',
      description = 'An interpolation-based tuning tool for Monte Carlo event generators.',
      long_description = longdesc,
      keywords = 'tuning generator montecarlo data hep physics particle',
      license = 'GPL',
      classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Console',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering :: Physics']
      )

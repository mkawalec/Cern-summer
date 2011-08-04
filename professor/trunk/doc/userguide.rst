**********
User guide
**********

This section contains documentation of the scripts distributed with
professor. The scripts are listed in the order of a typical work cycle.

Note that there may be scripts which are not documented here: at the time of
writing the :program:`prof-envelopes` and :program:`prof-plotcorrelations`
scripts fall into this category. However, all the Professor scripts have names
starting with `prof-`, and so typing this and using your shell's tab completion
facility is a handy way to get a list of all available programs. All of the
Professor scripts have built-in documentation via the :option:`--help` flag.


Main programs
=============

.. toctree::
    :maxdepth: 1

    scripts/prof-sampleparams.rst
    scripts/prof-runcombs.rst
    scripts/prof-lsobs.rst
    scripts/prof-envelopes.rst
    scripts/prof-interpolate.rst
    scripts/prof-ipolhistos.rst
    scripts/prof-I.rst
    scripts/prof-tune.rst
    scripts/prof-plotresultscatter.rst
    scripts/prof-plotcorrelations.rst
    scripts/prof-sensitivities.rst
    scripts/prof-compare-tunes.rst
    scripts/prof-scanchi2.rst


.. toctree::
    :maxdepth: 1

    scripts/options-paths.rst


Helper programs
===============

.. toctree::
    :maxdepth: 1

    scripts/prof-showipol.rst
    scripts/prof-batchtune.rst
    scripts/prof-mergeminresults.rst

File formats
============

.. toctree::
    :maxdepth: 1

    runcomb_syntax.rst
    weights_syntax.rst

Interactive usage
=================

.. todo::

    Give instructions and examples how to setup the Professor mode for
    IPython and how to do stuff interactively with Professor. E.g.
    filtering result lists.

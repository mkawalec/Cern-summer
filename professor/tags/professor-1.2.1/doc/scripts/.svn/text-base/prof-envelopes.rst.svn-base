Plotting MC envelope histograms -- :program:`prof-envelopes`
------------------------------------------------------------

.. create some short-cuts to link to other documents
.. |prof-runcombs| replace:: :doc:`prof-runcombs <prof-runcombs>`

.. program:: prof-envelopes

:program:`prof-envelopes` makes histograms showing the range of variation
available on observable histograms from the MC runs available in the
:file:`MCDIR` directory (or a subset, specified with the :option:`--runsfile`
`RUNSFILE` option). This is an important tool for ascertaining whether the
sampled MC parameter space is *ever* going to be capable of describing certain
observables: some tuning problems lie in the models or the param sampling
ranges.

The :option:`--datadir` `DATADIR` and related options are used as normal to
specify the reference data, MC runs, and interpolation objects: see the
:doc:`path options <options-paths>` page.

By default all the MC runs found in the MCDIR will be used, and all the
observables in those runs. The :option:`--runsfile` `RUNSFILE` option may be
used to obtain envelope plots for specified subsets of the available runs, and
the :option:`--obsfile` `OBSFILE` can be used to restrict the observables to be
plotted. The formats of these files are the usual ones: one space-separated run
combination, or observable path per line.

By default the complete envelope of all runs is used; this may be adapted to
e.g. the 68% central band of the runs, by using e.g. :option:`--cl` `68`.

The output format of the envelope histograms is in the Rivet
:program:`make-plots` script's `.dat` format and can be plotted with that
script.


Example
^^^^^^^

Simple example: plot the fully-inclusive MC envelopes for all-runs, and for all
available observables::

    prof-envelopes --data /my/data


Command-line options
^^^^^^^^^^^^^^^^^^^^

The :option:`--datadir` `DATADIR` and related options are used as normal to
specify the reference data, MC runs, and interpolation objects: see the :doc:`path
options <options-paths>` page.


.. cmdoption:: --runs RUNSFILE, --runsfile RUNSFILE

    A file listing the runs to be used to calculate the envelopes.

.. cmdoption:: --obsfile OBSFILE

    A file listing the observables for which envelope plots should be generated.

.. cmdoption:: --cl CL

    Specify the central coverage interval to be displayed, as a percentage. Defaults to 100%.

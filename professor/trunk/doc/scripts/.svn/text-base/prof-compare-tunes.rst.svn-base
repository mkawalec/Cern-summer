Comparing tune performance -- :program:`prof-compare-tunes`
-----------------------------------------------------------

.. create some short-cuts to link to other documents
.. |prof-tune| replace:: :doc:`prof-tune <prof-tune>`

.. program:: prof-compare-tunes

:program:`prof-compare-tunes` makes histograms comparing the goodness of fit of
multiple tunes. The name "tune" in this context really means a run: the input
data is read in the format of an input MC scan directory from `MCDIR`, i.e. a
`used_params` file and an `out.aida` file. Such directories can be created from
tune interpolations by using the :program:`prof-tune` or
:program:`prof-ipolhistos` programs.

The :option:`--datadir` `DATADIR` and related options are used as normal to
specify the reference data: see the :doc:`path options <options-paths>` page.

The output format of the histograms is in the Rivet :program:`make-plots`
script's `.dat` format and can be plotted with that script.


Example
^^^^^^^

Simple example: plot the goodness of fit for a single tune/run, located in the
:file:`tune1` directory::

    prof-compare-tunes --refdir datahistos --weights my.weights tune1/:"very good tune"


Command-line options
^^^^^^^^^^^^^^^^^^^^

The :option:`--datadir` `DATADIR` and related options are used as normal to
specify the reference data, MC runs, and interpolation objects: see the :doc:`path
options <options-paths>` page.


.. cmdoption:: --weights WEIGHTSFILE

    A file listing the observables and weights for the goodness of fit calculation.

.. cmdoption:: --no-weights

    Ignore the weights in the weights file, instead using all listed observables
    with a weight of 1.0 per bin.

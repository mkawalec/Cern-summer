Plotting parameter correlations -- :program:`prof-plotcorrelations`
-------------------------------------------------------------------

.. create some short-cuts to link to other documents
.. |prof-interpolate| replace:: :doc:`prof-interpolate <prof-interpolate>`
.. |prof-tune| replace:: :doc:`prof-tune <prof-tune>`

.. program:: prof-plotcorrelations

:program:`prof-plotcorrelations` makes 2D matrix histograms showing the degree
of correlation between each parameter in a tune, around the tune parameter
point. These correlations are calculated using the parameterisations built by
|prof-tune|, so that script must have been run first.

The :option:`--datadir` `DATADIR` and related options are used as normal to
specify the reference data, MC runs, and interpolation objects: see the :doc:`path
options <options-paths>` page.


Example
^^^^^^^

Simple example: make :file:`.dat` histogram source files for the given tune
object, and make PDF files from them using the :program:`make-plots` command::

    prof-plotcorrelations --data /my/data /my/data/tune-myweights-000/tune-myweights-000.pkl
    make-plots *.dat


Command-line options
^^^^^^^^^^^^^^^^^^^^

The :option:`--datadir` `DATADIR` and related options are used as normal to
specify the reference data, MC runs, and interpolation objects: see the :doc:`path
options <options-paths>` page.

Plotting parameterised histograms -- :program:`prof-ipolhistos`
---------------------------------------------------------------

.. create some short-cuts to link to other documents
.. |prof-interpolate| replace:: :doc:`prof-interpolate <prof-interpolate>`
.. |prof-runcombs| replace:: :doc:`prof-runcombs <prof-runcombs>`

.. program:: prof-ipolhistos

:program:`prof-ipolhistos` makes parameterised histograms for a parameter point,
using the parameterisations built by |prof-interpolate|. It writes out one AIDA
histogram file, plottable with the usual Rivet tools (see
e.g. :program:`prof-tune`) for each run combination (i.e. each parameterisation).

As for |prof-interpolate|, is necessary to specify a file with the observables
to be plotted, using :option:`--obsfile` `OBSFILE`. Also, the run combinations
can be given with :option:`--runsfile` `RUNSFILE` and the type of
parameterisation with :option:`--ipol` `IPOLMETHOD`: the default set of runs
will be all those found in the `MCDIR`, if available.

The :option:`--datadir` `DATADIR` and related options are used as normal to
specify the input data, MC runs, and interpolation objects.

The parameter point(s) at which the parameterisations are to be evaluated may be
supplied in several ways: as a list of `NAME=VALUE` pairs on the command line
with the :option:`--params` option, or as a parameter file or set of files with
the :option:`--paramsfile` or :option:`--paramsdir` options.

The :option:`--subdirs` option flag is useful for producing a collection of AIDA
files in the format of a Professor input `mc` directory, i.e. fake Rivet runs.


Example
^^^^^^^

Simple example: make a single AIDA file using the all-runs cubic interpolation, and
for all available observables, at the given param point::

    prof-ipolhistos --data /my/data --ipol cubic --params PAR1=1.5,PAR2=42


Command-line options
^^^^^^^^^^^^^^^^^^^^

Output
""""""

.. cmdoption:: --outdir OUTDIR, -o OUTDIR

    Specify a `DATADIR`-like directory into which the :file:`ipolhistos` and
    directory and its contents will be written. Defaults to `DATADIR`.


Input
"""""
.. cmdoption:: --runs RUNSFILE, --runcombs RUNSFILE

    A file with run combinations that are used as anchor points. One set
    of polynomial coefficients is calculated for each run combination.
    [default: :file:`runcombs.dat`]

.. cmdoption:: --ipol IPOLMETHOD

    The interpolation method. At the moment the order of the polynomial:
    ``quadratic`` or ``cubic``. [default: ``quadratic``]

.. cmdoption:: --datadir DATADIR

    The directory containing the :file:`ref/` and :file:`ipol/`
    directories.

.. cmdoption:: --refdir REFDIR

    The directory containing the reference data.
    [default: :file:`{DATADIR}/ref/`]


.. cmdoption:: --ipoldir IPOLDIR

    The directory containing the parameterization data.
    [default: :file:`{DATADIR}/ipol/`]

.. cmdoption:: --weights WEIGHTS, --obsfile WEIGHTS

    A file listing the observables and their weights which are used in
    the GoF.

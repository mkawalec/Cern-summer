Sample parameter points -- :program:`prof-sampleparams`
-------------------------------------------------------

.. create some short-cuts to link to other documents
.. |prof-scanchi2| replace:: :doc:`prof-scanchi2 <prof-scanchi2>`
.. |prof-interpolate| replace:: :doc:`prof-interpolate <prof-interpolate>`

.. program:: prof-sampleparams

:program:`prof-sampleparams` samples parameter points either randomly
to use them as anchor points for MC data production or along straight
lines for line-scan validation with |prof-scanchi2|.

Random mode
^^^^^^^^^^^

In the random mode (default) the points are sampled randomly from a
hyper-cube. The path to the range file must be given as first argument.
Alternatively, two arguments are accepted with files containing the
lower and upper parameter bounds. The number of points is controlled
with :option:`-N` `NUMRUNS`. The parameter points are written to files
in numbered directories under `OUTDIR` (see :option:`-o`)::

    OUTDIR/000/used_params
           001/used_params
           ...

The first run number can be set with :option:`--first-run`
`NUMFIRSTRUN`. See :ref:`oversampling-ratio` for some comments on how
many runs one should generate.

.. _prof-sampleparams-line_scan_mode:

Line scan mode
^^^^^^^^^^^^^^

Line scan mode can be activated with :option:`-s`. In line scan mode
equally distant points are generated along a straight line.
|prof-scanchi2| compares the MC data at this points with the prediction
of polynomial parameterisations.

The points are only sampled from the ranges given by the first argument.
These ranges should be the same that were used for the polynomials with
|prof-interpolate|, or smaller, because otherwise the polynomials are
evaluated in regions of extrapolation. Alternatively, the ranges can be
specified by two parameter point files.

The location and orientation of the line in parameter space is
controlled with :option:`--scancenter` and the orientation with
:option:`--direction`.

Examples
^^^^^^^^

Sample 100 points randomly from the ranges in :file:`generator.ranges`
and create the files under :file:`mcruns/`::

    prof-sampleparams -N 100 -o mcruns generator.ranges

Sample 10 points along a straight line in the ranges of
:file:`generator.ranges`. The line is rooted at the parameter values of
the first tune in the results file :file:`results.pkl` and is oriented
in the direction of the largest uncertainty::

    prof-sampleparams -s -N 10 -o linescan --scancenter results.pkl,0 --direction shallow generator.ranges


Command-line options
^^^^^^^^^^^^^^^^^^^^

.. cmdoption:: -N NUMRUNS, --num-runs NUMRUNS

    Number of generated points.

.. cmdoption:: --first-run NUMFIRSTRUN

    The number of the first run.


.. cmdoption:: -o OUTDIR, --outdir OUTDIR

    Base directory for run directories. [default: professor-out]

.. cmdoption:: -t, --timestamp

    Prepend the OUTDIR with the current date.

.. cmdoption:: -T TEMPLATE, --template TEMPLATE

    Replace variable in the given template files. Can be given Multiple
    times.

Line scan mode
""""""""""""""

.. cmdoption:: -s, --scan

    Turn line scan sampling on.

.. cmdoption:: --scancenter SCANCENTER

    The base point of the line. Can be either a parameter file or a
    results file. In the second case the index of the minimization
    result must be appended to the file name, separated by a comma,
    e.g::

        --scancenter results.pkl,10

.. cmdoption:: --direction DIRECTION

    The direction of the line scan. Three values are supported:

    diagonal
        The line is parallel to the body diagonal.

    steep, shallow
        Only allowed if `SCANCENTER` is a result file. The line is
        oriented in the direction of the smallest (steep) or largest
        (shallow) uncertainty as was estimated during the minimization.

        To make the lines symmetric around `SCANCENTER` ``:sym`` can be
        appended.

Finding optimal parameter values -- :program:`prof-tune`
--------------------------------------------------------

.. create some short-cuts to link to other documents
.. |prof-interpolate| replace:: :doc:`prof-interpolate <prof-interpolate>`
.. |prof-runcombs| replace:: :doc:`prof-runcombs <prof-runcombs>`
.. |prof-batchtune| replace:: :doc:`prof-batchtune <prof-batchtune>`
.. |prof-mergeminresults| replace:: :doc:`prof-mergeminresults <prof-mergeminresults>`

.. program:: prof-tune

:program:`prof-tune` optimizes the goodnes of fit (GoF) measure between
the MC response function and the experimental reference data by varying
the model parameters.

It is necessary to specify a file with the observables that are included
in the GoF function and their respective weights with
:option:`--weights` `WEIGHTS`. Also, the run combinations must be given
with :option:`-R` `RUNSFILE` and the type of parameterisation with
:option:`--ipol-method` `IPOLMETHOD`.

With :option:`--datadir` `DATADIR` the location of the reference data
and parameterization files must be specified. It is assumed that
reference data are in :file:`{DATADIR}/ref/` and the parameterization
files in :file:`{DATADIR}/ipol/`. These assumptions can be overridden
with :option:`--refdir` `REFDIR` and :option:`--ipoldir` `IPOLDIR`.

The results are stored in a file (see :option:`--outfile` `OUTFILE`).
For each run combination and initial point (see below) one result is
produced and stored in `OUTDIR/tunes/OUTFILE`. Each result contains the optimal
parameter values and additionally the MC runs and observables used and,
if the used minimizer supports this, the errors on the parameters and
the parameter-parameter covariance matrix. In addition, the
parameterization is evaluated at the optimal parameter values and the
resulting histograms are saved in an AIDA file, :file:`histo-{xxx}.aida`.
These files are created in `OUTDIR/ipolhistos`.
The production of these histograms can be turned off with :option:`--no-ipolhistos`.
The histograms in these AIDA files may be plotted and compared with reference
data and other tunes using the Rivet :program:`compare-histos` and :program:`make-plots`
scripts.

Parameters can be fixed with :option:`--fixed-parameters`. To check
against a dependency on the initial point of the minimizer, different
methods to select the initial point are available (see
:option:`--spmethods`). Additionally, parameters can be constrained to
intervals (:option:`--limits`) but this is not recommended. Usually a
diverging parameter is a hint for bad sampling ranges of the anchor
points or a problem in the model.

.. note::

    For all observables in `WEIGHTS` and run combinations in `RUNSFILE`
    the parameterizations of the MC response function must have been
    pre-built with |prof-interpolate| using the parameterisation method
    `IPOLMETHOD` (currently the order of the polynomial). An easy way to
    achieve this is to use the same weights file and run combinations
    file for both :program:`prof-interpolate` and :program:`prof-tune`.

.. note::

    Due to limitations of the Python interpreter (especially the global
    interpreter lock, GIL). This cannot be done in parallel in one
    process. To make use of multiple CPU cores you can split the run
    combinations file in several files and start :program:`prof-tune`
    for each of this "sub-files" (but make sure that each prof-tune call
    has its own result file). Alternatively you can use |prof-batchtune|
    to produce shell scripts for this purpose. These scripts can also be
    fed to a batch system. In both cases you can use
    |prof-mergeminresults| to create a single result file.

Example
^^^^^^^

Simple example: run the minimizer once with the center of the sampling
hyper-cube as initial point::

    prof-tune --data /my/data --weights my.weights --runs mycombinations

Complex example::

    prof-tune --data /my/data --ipoldir /my/ipol/storage --weights my.weights --runsfile mycombinations --fixed-parameters Par1=3.5 --spmethods random,random,center

This loads reference and interpolation data from different directories
(:samp:`{REFDIR}={DATADIR}/ref/=/my/data/ref/`,
:samp:`{IPOLDIR}=/my/ipol/storage`), fixes parameter ``Par1`` to 3.5 and
performs 3 minimizations per run combination (``random,random,center``).

Command-line options
^^^^^^^^^^^^^^^^^^^^

Output
""""""

.. cmdoption:: --outdir OUTDIR, -o OUTDIR

    Specify a `DATADIR`-like directory into which the :file:`tune` and
    :file:`ipolhistos` directories will be written. Defaults to `DATADIR`.

.. cmdoption:: --outfile OUTFILE

    Store results in `OUTDIR/tunes/OUTFILE`. [default: :file:`results.pkl`]

.. cmdoption:: -I, --no-ipolhistos

    Do not store the parameterization histograms at the optimal
    parameter points. [default: store histograms]

.. cmdoption:: --snapshot

    Save snapshots of the result file every 10 results in
    :file:`results-snap.pkl`. [default is off]

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

Minimizer
"""""""""

.. cmdoption:: --minimizer MINIMIZER

    Select the minimizer to use for minimization: ``pyminuit`` or
    ``scipy``. ``pyminuit`` is the default. It includes error and
    parameter-parameter correlation estimation.

.. cmdoption:: --migrad, --minos

    Use the MIGRAD (default) or MINOS error estimation code of MINUIT.

.. cmdoption:: --limits LIMITS

    A file with parameter limits passed to the minimizer. Only supported
    by ``pyminuit``. *Not recommended!*

.. cmdoption:: --spmethods STARTPOINTMETHODS, --start-points STARTPOINTMETHODS

    Select the way how the initial parameter point of the minimizer is
    chosen. Multiple methods can be separated by comma and each method
    can be specified several times (only useful with the ``random``
    method).

    Supported methods are:

    ``center``
        Use the center of the parameter hyper-cube that is spanned by
        the anchor points used for the parameterisations.

    ``random``
        Use a random parameter point hyper-cube that is spanned by the
        anchor points used for the parameterisations.

    ``manual``
        Use the parameter values given by :option:`--manual-sp`.

    .. rubric:: Example

    Run the minimizer four times for each parameterization (i.e. each
    run combination), three times with a random initial point and one
    time with the center as initial point::

        --spmethods random,random,random,center

.. cmdoption:: --manual-sp MANUALSTARTPOINT, --manual-startpoint MANUALSTARTPOINT

    The parameter values used as initial point with the ``manual``
    method. `MANUALSTARTPOINT` must have the form::

        Par1=Val1,Par2=Val2

    A value for every parameter must given!

.. cmdoption:: --fixed-parameters FIXEDPARAMETERS

    These parameters are fixed to the specified values during the
    optimization. `FIXEDPARAMETERS` must have the form::

        Par1=Val1,Par2=Val2

Finding optimal parameter values -- :program:`prof-tune`
--------------------------------------------------------

.. create some short-cuts to link to other documents
.. |prof-interpolate| replace:: :doc:`prof-interpolate <prof-interpolate>`
.. |prof-runcombs| replace:: :doc:`prof-runcombs <prof-runcombs>`
.. |prof-batchtune| replace:: :doc:`prof-batchtune <prof-batchtune>`
.. |prof-mergeminresults| replace:: :doc:`prof-mergeminresults <prof-mergeminresults>`

.. program:: prof-tune

:program:`prof-tune` optimizes the goodness of fit (GoF) measure between
the MC response function and the experimental reference data by varying
the model parameters.

It is advised to specify a file with the observables that are included
in the GoF function and their respective weights with
:option:`--weights` `WEIGHTS`. Also, the run combinations must be given
with :option:`--runsfile` `RUNSFILE` and the type of parameterisation with
:option:`--ipol` `IPOLMETHOD`.

With :option:`--datadir` `DATADIR` the location of the reference data
and parameterization files must be specified. It is assumed that
reference data are in :file:`{DATADIR}/ref/` and the parameterization
files in :file:`{DATADIR}/ipol/`. These assumptions can be overridden
with :option:`--refdir` `REFDIR` and :option:`--ipoldir` `IPOLDIR`.

Each tune's details are stored in a "pickle" file in `OUTDIR/tunes`, as well as
the whole collection of tune results in `OUTDIR/tunes/results.pkl`. Each result
contains the optimal parameter values and additionally the MC runs and
observables used. Also, if the used minimizer supports it, the result object
will contain the errors on the parameters and the parameter-parameter covariance
matrix... but take these errors with a pinch of salt: eigentunes are a better
way to obtain tune errors. In addition, the parameterization is evaluated at the
optimal parameter values and the resulting histograms are saved in an AIDA file,
:file:`histo-{xxx}.aida`.  These files are created in `OUTDIR/tunes/ipolhistos`.
The production of these histograms can be turned off with
:option:`--no-ipolhistos`.  The histograms in these AIDA files may be plotted
and compared with reference data and other tunes using the Rivet
:program:`compare-histos` and :program:`make-plots` scripts (or, alternatively,
the single :program:`rivet-mkhtml` script).

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
    interpreter lock, GIL), tunes cannot be made in parallel in a single
    process. To make use of multiple CPU cores you can split the run
    combinations file in several files and start :program:`prof-tune`
    for each of this "sub-files" (but make sure that each prof-tune call
    has its own result file). Alternatively you can use |prof-batchtune|
    to produce shell scripts for this purpose. These scripts can also be
    fed to a batch system. In both cases you can use
    |prof-mergeminresults| to create a single result file.


Error tunes
^^^^^^^^^^^

|prof-tune| can also produce a set of deviation tunes, representing a good set
of correlated systematic errors on a given best tune. These "eigentunes" are
created by using the covariance matrix in the region of the best tune (supplied
by the minimiser) to define correlated, maximally independent principle
directions in the parameter space. The eigentunes themselves are then created by
walking out from the best tune point to find the points with a given GoF
deviation from the best tune. If the chi2 measure is exactly chi2-distributed
(NB. this is *not* guaranteed!) then a GoF increase of +1 will represent a 1
sigma deviation from the best tune.

To make a set of *2p* eigentunes (two for each principle direction, of which
there are as many as there are parameters), just pass the :option:`--eigentunes`
to |prof-tune|. This will write out extra params files and ipol histo files for
each of the eigentunes. The default GoF increase which defines the eigentune
deviation is 1, but you can change this by also supplying the
:option:`--eigentunes-dgof=NUM` option.


Example
^^^^^^^
Simple example: run the minimizer once with the center of the sampling
hyper-cube as initial point::

    prof-tune --data /my/data --weights my.weights --runs mycombinations

Complex example::

    prof-tune --data /my/data --ipoldir /my/ipol/storage --weights my.weights --runsfile mycombinations --fixed-parameters PAR1=3.5 --spmethods random,random,center

This loads reference and interpolation data from different directories
(:samp:`{REFDIR}={DATADIR}/ref/=/my/data/ref/`,
:samp:`{IPOLDIR}=/my/ipol/storage`), fixes parameter ``PAR1`` to 3.5 and
performs 3 minimizations per run combination (``random,random,center``).


Command-line options
^^^^^^^^^^^^^^^^^^^^

Output
""""""

.. cmdoption:: --outdir OUTDIR, -o OUTDIR

    Specify a `DATADIR`-like directory into which the :file:`tunes` and
    directory and its contents will be written. Defaults to `DATADIR`.

.. cmdoption:: --no-ipolhistos

    Do not store the parameterization histograms at the optimal
    parameter points. [default: store histograms]


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
    the GoF. A weight of 0 will lead to the observable being included in
    any resulting ipol histos, but they will not have any influence on
    the fit to reference data.


Minimizer
"""""""""

.. cmdoption:: --minimizer MINIMIZER

    Select the minimizer to use for minimization: ``pyminuit`` or
    ``scipy``. ``pyminuit`` is the default. It includes error and
    parameter-parameter correlation estimation.

.. cmdoption:: --minos

    Use the MINOS error estimation code of MINUIT, as opposed to the default MIGRAD method.

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

        PAR1=val1,PAR2=val2

    A value must be given for every parameter!

.. cmdoption:: --fixed-parameters FIXEDPARAMETERS

    These parameters are fixed to the specified values during the
    optimization. `FIXEDPARAMETERS` must have the form::

        PAR1=val1,PAR2=val2

.. cmdoption:: --eigentunes

    Construct a set of eigentunes surrounding the best tune point. The eigentunes will
    be constructed from the minimiser-supplied parameter covariance matrix in the
    vicinity of the best tune point, and are explictly solved to get a fixed increase
    in the GoF function. By default the change in the GoF is 1, assuming a true
    chi2-distributed GoF function, but this can be changed using the next option.

.. cmdoption:: --eigentunes-dgof DGOF

    Define the GoF increase which defines the eigentunes. The default deviation is 1,
    but you can change this by supplying this option. You can either supply an absolute
    deviation as a number, e.g.

        --eigentunes-dgof=2

    or as a multiple or percentage of the best tune GoF value, e.g.

        --eigentunes-dgof=1.5x

    or

        --eigentunes-dgof=150%

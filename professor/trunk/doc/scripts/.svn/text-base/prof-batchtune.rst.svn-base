Parallelize computations -- :program:`prof-batchtune`
-----------------------------------------------------

.. create some short-cuts to link to other documents
.. |prof-tune| replace:: :doc:`prof-tune <prof-tune>`
.. |prof-interpolate| replace:: :doc:`prof-interpolate <prof-interpolate>`

.. program:: prof-batchtune

:program:`prof-batchtune` assists you to run |prof-interpolate| or
|prof-tune| in parallel, e.g. on a batch cluster, by filling job-script
template files. This is done by splitting the MC run combinations into
smaller sets. These sets can then be processed in parallel.

The data locations must be given on the command line (e.g.
:option:`--datadir` or :option:`--weights`), and the MC, reference and
interpolation directories must all exist. The paths are converted to
absolute paths. The number of scripts that are produced is controlled
with :option:`-N` `NUMSCRIPTS`. Additional arguments can be passed
through to the called professor script with :option:`-o`
`ADDITIONALOPTIONS`. Paths in `ADDITIONALOPTIONS` must be absolute.

The output of the scripts is stored in numbered directories under
`JOBBASEOUTDIR` given by :option:`-j`

A simple algorithm is used to distribute the number of run combinations
equally over the job scripts. If the number of scripts is not a divisor
of the number of run combinations, the last script will contain less
than the other scripts. In some cases less than `NUMSCRIPTS` scripts
will be created.

.. note:: At the moment the `Cheetah <http://www.cheetahtemplate.org>`_
    templating library is required.

Templates
^^^^^^^^^

Template files are distributed together with the professor source code:

:file:`templates/prof-interpolate.template`
    Template for :program:`prof-interpolate` job scripts. The scripts
    will put the coefficient files in the same directory given by
    `IPOLDIR` (see: :option:`--datadir`, :option:`--ipoldir`).
    `JOBBASEOUTDIR` contains only the log files.

:file:`templates/prof-tune.template`
    Template for :program:`prof-tune` job scripts. The result files and
    interpolated histograms will be stored in output directories under
    `JOBBASEOUTDIR`::

        jobout/000/results.pkl
                   professor.log
                   params/params-tune{xxx}/...
                   ipolhistos/histos-tune{xxx}/...
              001/...
              ...

Examples
^^^^^^^^

Create 20 job scripts for :program:`prof-interpolate` to compute the
coefficients of the polynomial parameterization. Use cubic polynomials::

    prof-batchtune  -N 20  --weights weights  --datadir .  -R runs-cubic  -o "--ipol-method=cubic"  /PATH/TO/PROFESSOR/SOURCE/templates/prof-interpolate.template

The scripts are created in :file:`scripts_interpolate_weights/`. The output
directory for the coefficient files (:file:`./ipol/`) must exist!

Create 10 job scripts for :program:`prof-tune` using quadratic polynomials and
the default initial point method::

    prof-batchtune  -N 10  --weights my.weights  -R my.combinations  --datadir my/data  /PATH/TO/PROFESSOR/SOURCE/templates/prof-tune.template

The scripts are created in :file:`scripts_tune_my.weights/`. The result files
will be put in :samp:`jobout/{xxx}/results.pkl`.

Create 20 job scripts for :program:`prof-tune` with a fixed parameter and three
initial points per run combination using cubic polynomials::

    prof-batchtune -N 20 --weights weights --datadir . -R runs.cubic -o "--ipol-method=cubic --spmethods='random,random,center' --fixed-params='Par1=3.1'"  /PATH/TO/PROFESSOR/SOURCE/templates/prof-tune.template


Command-line options
^^^^^^^^^^^^^^^^^^^^

.. cmdoption:: -N NUMSCRIPTS

    The number of scripts that should be created. By default one script
    for each run combination is created, which usually means a lot of
    scripts.

.. cmdoption:: -o ADDITIONALOPTIONS, --options ADDITIONALOPTIONS

    Options that are passed to the called :program:`prof-*` program,
    e.g. the order of the polynomial.

.. cmdoption:: -s SCRIPTDIR, --script-outdir SCRIPTDIR

    The job scripts will be placed in `SCRIPTDIR`. By default the
    directory name will be constructed from the name of the template and
    the weights file.

.. cmdoption:: -j JOBBASEOUTDIR, --outdir=JOBBASEOUTDIR

    Base directory for the output of the job scripts, e.g. where the
    results files are stored. [default: ./jobout]

Input data
""""""""""

.. cmdoption:: -R RUNSFILE, --runsfile RUNSFILE, --runcombs RUNSFILE

    A file with run combinations that are used as anchor points. One set
    of polynomial coefficients is calculated for each run combination.
    [default: :file:`runcombs.dat`]

.. cmdoption:: --datadir DATADIR

    The directory containing the :file:`mc/` and :file:`ipol/`
    directories.

.. cmdoption:: --mcdir MCDIR, optional

    The directory containing the MC run data. [default:
    :file:`{DATADIR}/mc/`]

.. cmdoption:: --ipoldir IPOLDIR, optional

    The directory where the parameterization data are stored.
    [default: :file:`{DATADIR}/ipol/`]

.. cmdoption:: --weights WEIGHTS, --obsfile WEIGHTS

    Parameterization coefficients for all observables in :file:`WEIGHTS`
    kre calculated.

Creating run combination files -- :program:`prof-runcombs`
----------------------------------------------------------

.. program:: prof-runcombs

The :program:`prof-runcombs` script assists you with the creation of
MC-run-combinations, i.e. the MC runs that are used as anchor points for
the polynomial parameterization of the MC response function and with the
extraction of (a subset of) the run combinations from a result list
file. The mode of operation is given as first argument ``create`` or
``extract``. If no mode is given ``create`` mode is assumed.

In ``create`` mode the location of the MC runs can be specified by
:option:`--mcdir` `MCDIR` or :option:`--datadir` `DATADIR`, as for the main
:program:`prof-interpolate` and :program:`prof-tune` scripts. The combinatorics
of the run combinations can be chosen with (multiple) :option:`-c`
`COMBINATION`.

In ``extract`` mode the file to extract run combinations from must be
given as second argument.

Runs can be excluded in both modes by two different ways:

    1. With :option:`-x` `EXCLUDE` runs can be excluded explicitely by
       their run ID (which is the name of the run directory, e.g.
       :file:`042`).

    2. A parameter range can be given with :option:`-r` `RANGEFILE` and
       only runs within this range are accepted.

In ``create`` mode only the runs that fulfil the above criteria, i.e.
are not excluded and are within the parameter range (if both options are
used), are used to sample the run combinations from. In ``extract`` mode
only those run combinations that do not contain any run that is excluded
are extracted. If :option:`-r` `RANGEFILE` is used to exclude runs in
``extract`` mode, the location of the MC runs must be given by
:option:`--mcdir` `MCDIR`.

.. _oversampling-ratio:

Oversampling ratio
^^^^^^^^^^^^^^^^^^

.. todo:: Put this section into a more general user guide?

The coefficients of the polynomial interpolations are calculated by
solving a system of linear equations. The minimial number of runs is
given by the number of parameters that are tuned and the order of
the polynomial that is used for the interpolations:

====================  ============  ===========
\                     Number of coefficients
--------------------  -------------------------
Number of parameters  second order  third order
====================  ============  ===========
           1                3             4
           2                6            10
           3               10            20
           4               15            35
           5               21            56
           6               28            84
           7               36           120
           8               45           165
           9               55           220
          10               66           286
====================  ============  ===========


As discussed in our paper
(`arxiv:0907.2973 <http://arxiv.org/abs/0907.2973>`_) It is in principle
possible to use the minimal number of anchor points. But this would tie
the interpolation strictly to the anchor points and we know that the MC
response function in each bin is more complex than the polynomials we
use. To take the incapabilities of the polynomials into account we
advise to use a higher number of anchor points. That is the ratio of the
number of runs over the minimal number is larger than 1,

.. math::
    R = \frac{N_\mathrm{runs}}{N_\mathrm{min}} > 1 .

Professor then uses a singular value decomposition to calculate the
coefficients resulting in a least squares fit. In fact we found that an
oversampling ration of 2 is advisable while values above 3.5 do not
necessarily lead to better results.

Second, it is important to check that the results one gets with
Professor do not depend on the specific choice of anchor points i.e. the
results should be robust against using different sets of anchor points.
The way to do this with Professor is to create different subsets of
anchor points that are used for the interpolations. Usually we use 100
such subsets.

Idealy, these subsets are disjunct. This is not feasable due to the high
number of minimal anchor points one usually needs. Instead a certain
level of overlapping between these subsets is accepted and in conclusion
one has to find a compromise between the level of overlap between the
subsets and a reasonable oversampling ratio. A good rule of thumb is to
generate

.. math::
    N = \frac{2}{3} \cdot 2 \cdot N_\mathrm{min}

runs.

.. todo:: Calculate overlap probability.

Examples
^^^^^^^^

::

    prof-runcombs create -m mc/ -c 0:1 -c 30:100 -o mycombinations

This will create a file :file:`mycombinations`. 101 run combinations are
generated. One run combination will contain all runs, and 100
combinations will contain ``#(all runs) - 30``.

::

    prof-runcombs extract -m mc/ -r narrow.ranges -o mynarrowcombinations

This will create :file:`mynarrowcombinations` that will consist of all
the run combinations from :file:`mycombinations` that use only MC runs
within the ranges given in :file:`narrow.ranges`.

Command-line options
^^^^^^^^^^^^^^^^^^^^

.. cmdoption:: -o OUTFILE, --outfile OUTFILE

    The file name of the run combinations file. Any existing OUTFILE will be
    overwritten.

.. cmdoption:: --datadir DATADIR, --mcdir MCDIR

   Specifying the data or specifically MC runs directory from which combinations
   will be picked.

.. cmdoption:: -r RANGEFILE, --range RANGEFILE

    Accept only runs that are in the ranges of `RANGEFILE`. For this the
    location of the MC runs must be given with :option:`-m` `MCDIR`.
    Default is to exclude no runs.

.. cmdoption:: -x EXCLUDE, --exclude EXCLUDE

    Comma-separated list of MC run IDs that are excluded from the run
    combinations.

    This can be used to exclude faulty runs, if completely removing is
    not an option.

.. cmdoption:: -c COMBINATION, --comb COMBINATION

    The number of runs left out and the number of combinations to
    produce, separated by a comma. Multiple definitions can be given.

    For the above example (`-c 0:1 -c 30:100`)::

        +-- leave out 0 runs,       +-- leave out 30 runs,
        |   i.e. use all            |   i.e. use all
        v                           v

        0:1                        30:100

          ^                            ^
          |                            |
          +-> generate one run         +-> generate 100 run
              combination with             combinations with
              0 runs left out              30 runs left out

    The default is to generate only one run combination that includes
    all available MC runs.


Run combination file format
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The run combination files are stored as simple text files -- one
run-combination per line::

    Run_ID_1 Run_ID_2 Run_ID_3 Run_ID_4 ...
    Run_ID_1 Run_ID_4 Run_ID_5 RUN_ID_10 ...
    ...

The :samp:`Run_ID_{x}` are the directory names of the MC run directories
in the :file:`mc/` directory, usually simple numbers::

    mc/000
       001
       002
       ...

thus::

    000 001 002 003 ...
    000 003 004 009 ...
    ...


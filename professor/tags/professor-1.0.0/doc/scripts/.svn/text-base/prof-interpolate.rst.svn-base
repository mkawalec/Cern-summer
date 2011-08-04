Creating response function parameterizations -- :program:`prof-interpolate`
---------------------------------------------------------------------------

.. create some short-cuts to link to other documents
.. |prof-tune| replace:: :doc:`prof-tune <prof-tune>`
.. |prof-runcombs| replace:: :doc:`prof-runcombs <prof-runcombs>`
.. |prof-batchtune| replace:: :doc:`prof-batchtune <prof-batchtune>`

.. program:: prof-interpolate

The polynomial coefficients for the parameterization of the MC response
function are calculated by :program:`prof-interpolate`. This must be
done before |prof-tune| is called to find optimal
parameter values.

A file with the run combinations that are used for the parameterizations
can be specified via :option:`-R` `RUNSFILE`. This file can be prepared
with |prof-runcombs|. If no file is given :file:`runcombs.dat`
is assumed.

The parameterization of the MC response function is calculated for all
observables which are listed in the file given by the
:option:`--weights`.

With :option:`--datadir` `DATADIR` the location of the MC run data and
the parameterization files must be specified. It is assumed that MC data
are in :file:`{DATADIR}/mc/` and the parameterization files are created
in :file:`{DATADIR}/ipol/`. These assumptions can be overridden with
:option:`--mcdir` `MCDIR` and :option:`--ipoldir` `IPOLDIR`.

For each run combination in `RUNSFILE` a file is created under
`IPOLDIR`. The file name follows the scheme
:file:`profipol_{METHOD}_{HASH}.pkl`. *METHOD* specifies the method of
the parameterization, usually the order of the polynomial, and *HASH* is
a md5-hash of the run combinations.

.. note::

    Due to limitations of the Python interpreter (especially the global
    interpreter lock, GIL). This cannot be done in parallel in one
    process. To make use of multiple CPU cores you can split the run
    combinations file in multiple separate and start
    :program:`prof-interpolate` for each of this "sub-files".
    Alternatively you can use |prof-batchtune| to produce shell scripts
    for this purpose. These scripts can also be fed to a batch system.

Examples
^^^^^^^^

Have MC and parameterization data located in the same directory
(:file:`/my/data/`)::

    prof-interpolate --weights my.weights --runsfile mycombinations --data /my/data/

MC and parameterization data in different directories::

    prof-interpolate --weights my.weights --runsfile mycombinations --mcdata /my/data/mc/ --ipoldir /my/tmp/ipol/

Command-line options
^^^^^^^^^^^^^^^^^^^^

.. cmdoption:: -R RUNSFILE, --runsfile RUNSFILE, --runcombs RUNSFILE

    A file with run combinations that are used as anchor points. One set
    of polynomial coefficients is calculated for each run combination.
    [default: :file:`runcombs.dat`]

.. cmdoption:: --ipol-method IPOLMETHOD

    The interpolation method. At the moment the order of the polynomial:
    ``quadratic`` or ``cubic``. [default: ``quadratic``]

.. cmdoption:: --weave, --noweave

    Use an optimized implementation of the parameterization code. This
    code uses C code, that is compiled on-the-fly, and is ~5 times faster
    than the pure-Python code. If the compilation fails you can use
    :option:`--noweave` to use the pure-Python code. [default: use
    weave]

.. cmdoption:: --datadir DATADIR

    The directory containing the :file:`mc/` and :file:`ipol/`
    directories.

.. cmdoption:: --mcdir MCDIR, optional

    The directory containing the MC run data. [default:
    :file:`{DATADIR}/mc/`]

.. cmdoption:: --ipoldir IPOLDIR, optional

    The directory where the parameterization data are stored. If the
    directory does not exist it is created.
    [default: :file:`{DATADIR}/ipol/`]

.. cmdoption:: --weights WEIGHTS, --obsfile WEIGHTS

    Parameterization coefficients for all observables in :file:`WEIGHTS`
    kre calculated.

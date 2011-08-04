Standard Professor script command-line options
----------------------------------------------

The path structure expected by Professor is the same for all scripts, so we
document that and the standard script options which define it, on this common
page.

Professor will by default read from and write to a directory structure all
contained within a single directory which we refer to as `DATADIR`. This
directory contains a directory containing a list of MC sample point directories
(each of which contains a :file:`used_params` file and an :file:`out.aida`
file): this container directory is referred to as `MCDIR`: a new `MCDIR` can be
populated with :file:`used_params` files ready for MC sampling production using
the :program:`prof-sampleparams` script. A second directory in `DATADIR`,
referred to as `REFDIR`, should contain a set of AIDA reference data files for
all of the analyses being tuned to.

It is assumed by default that MC data points are in :file:`{DATADIR}/mc/`,
reference data are in :file:`{DATADIR}/ref/` and the parameterization files in
:file:`{DATADIR}/ipol/`. These assumptions can be overridden with
:option:`--mcdir` `MCDIR`, :option:`--refdir` `REFDIR` and :option:`--ipoldir`
`IPOLDIR`.

Interpolation objects (with :program:`prof-interpolation`) and tune/plot outputs
will be written into a similar structure to `DATADIR`, specified via the
:option:`--outdir` `OUTDIR` option and defaulting to `DATADIR` itself. If
interpolation objects have previously been generated elsewhere than in the
datadir, this location can be specified with the :option:`--ipoldir` `IPOLDIR`
option.


Input
"""""
.. cmdoption:: --datadir DATADIR

    The directory containing the :file:`mc/`, :file:`ref/` and :file:`ipol/`
    directories.

.. cmdoption:: --refdir REFDIR

    The directory containing the reference data.
    [default: :file:`{DATADIR}/ref/`]

.. cmdoption:: --mcdir MCDIR

    The directory containing the parameterization data.
    [default: :file:`{DATADIR}/mc/`]

.. cmdoption:: --ipoldir IPOLDIR

    The directory containing the parameterization data.
    [default: :file:`{DATADIR}/ipol/`]


Output
""""""

.. cmdoption:: --outdir OUTDIR, -o OUTDIR

    Specify a `DATADIR`-like directory into which the :file:`ipolhistos` and
    directory and its contents will be written. Defaults to `DATADIR` or 
    if `DATADIR` is not given the current working directory.

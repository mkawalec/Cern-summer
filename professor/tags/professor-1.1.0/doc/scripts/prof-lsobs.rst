Creating observable weight files -- :program:`prof-lsobs`
----------------------------------------------------------

.. program:: prof-lsobs

The :program:`prof-lsobs` script is a very simple one to help with creation of
observable (and observable weight) files. For convenience, it accepts the same
command line options for data directory specification as do
:program:`prof-interpolate` and :program:`prof-tune`, which are the main users
of the weights output.

Examples
^^^^^^^^

::

    prof-lsobs --datadir=mydata
    prof-lsobs --mcdir=mydata/mc

These will write out the available observables in the MC runs found in the
specified data directories. They are written out to standard output.

::

    prof-lsobs --datadir=mydata --weight=2.5

This will write out the available observables as before, but this time in the
more general format for observable weight files with an observable weight of 2.5
applied to all observables. Of course, a uniform weight like this is no
different from the default uniform weight of 1.0, but it can be used to give a
convenient starting place for a weights file which you will then edit.

::

    prof-lsobs --datadir=mydata --weight=1.0 > myweights
    prof-lsobs --datadir=mydata --weight=1.0 -o myweights

These will create a new weights file, :file:`myweights` with an explicit weight
of 1.0 for all observables.


Command-line options
^^^^^^^^^^^^^^^^^^^^

.. cmdoption:: -o OUTFILE, --outfile OUTFILE

    The file name of the run combinations file.

.. cmdoption:: --weight W

    Explicitly apply an observable weight *W* to all available observables.

.. cmdoption:: --datadir DATADIR, --mcdir MCDIR

    The usual flags for specifying the Professor data locations.

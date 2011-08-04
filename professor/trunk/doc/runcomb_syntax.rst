.. _runcombsyntax:

***************************
Run combination file format
***************************

Combinations of MC runs are used at several points by Professor: to decide on
the input MC runs to use in building an interpolation (or a set of
interpolations), to decide which interpolation to use for tuning or other
comparison, to plot run-combination tune scatter plots, etc. By default the
Professor scripts will use all the available MC runs (or the interpolation
corresponding to them), but if a more select subset (or subsets) is required,
then they must be specified as a text file.

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

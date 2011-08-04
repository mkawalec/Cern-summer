Merge minimisation results in one file -- :program:`prof-mergeminresults`
-------------------------------------------------------------------------

.. create some short-cuts to link to other documents
.. |prof-batchtune| replace:: :doc:`prof-batchtune <prof-batchtune>`
.. |prof-tune| replace:: :doc:`prof-tune <prof-tune>`

.. program:: prof-mergeminresults

:program:`prof-mergeminresults` merges multiple minimization result
files into a single file. If |prof-batchtune| is used to run |prof-tune|
on a batch system, this is needed to merge the result files from the
individual batch scripts into one file.

The :option:`--datadir` `DATADIR` and related options are used as normal to
specify the reference data, MC runs, and interpolation objects: see the :doc:`path
options <options-paths>` page.

With :option:`-o` the name of the merged results file can be given. To
recursively merge all files from a directory use :option:`--fromdir`.

Examples
^^^^^^^^

Merge files produced by batch scripts from :program:`prof-batchtune`::

    prof-batchtune jobout/*/results.pkl

Do the same with :option:`--fromdir`::

    prof-batchtune --fromdir jobout


Command-line options
^^^^^^^^^^^^^^^^^^^^

The :option:`--datadir` `DATADIR` and related options are used as normal to
specify the reference data, MC runs, and interpolation objects: see the :doc:`path
options <options-paths>` page.

.. cmdoption:: --fromdir

    Interprete first argument as directory and recursively merge all
    :file:`*.pkl` files in this directory.

Visualize the scatter of minimization results -- :program:`prof-plotresultscatter`
---------------------------------------------------------------------------------

.. create some short-cuts to link to other documents
.. |prof-tune| replace:: :doc:`prof-tune <prof-tune>`

.. program:: prof-plotresultscatter

After the goodness of fit function was minimized with |prof-tune|,
:program:`prof-plotresultscatter` can be used to visualize the scatter
of the minimization results obtained with different sets of anchor
points. This is necessary to check that the minimizer does not get
caught in local minima and that the goodness of fit (GoF) does not
depend strongly on the combination of anchor points/MC runs. The plots
produced show the scatter of the results in the GoF-parameter plane. For
each parameter one plot is produced.

For a good tuning one expects that the minimization results cluster
around the minimization result that was obtained with all MC runs as
anchor points.

If more than one cluster appears professor can be used interactively to
extract the cluster around the all-MC-runs result by imposing simple
cuts on the parameter values of the minimization results (see:
:meth:`professor.minimize.result.ResultList.filtered`).

Possible reasons for a wide spread of the minimization results in one
ore more parameters are

    * the observables are not sensitive to this parameter
    * the parameter ranges are too wide and, thus, the polynomials
      strongly depend on the used anchor points
    * the model is incapable of describing the observables accurately

The original sampling ranges can be plotted using
:option:`--ranges` `RANGEFILE` to check that the results are not in
regions of extrapolation. The styles of the points changes by default
with the number of anchor points used for the polynomial approximations,
e.g. results obtained from 10 anchor points are displayed in a different
style than results from 20 anchor points. A second criterion that
changes the display style is if parameters were limitted during the
minimization or not. A third, optional criterion is to discriminate the
results by the method that was used to assign the initial point for the
minimization, e.g. center or random.

The location for the output files can be chosen with
:option:`--outdir` `DIRECTORY`. For each parameter that was tuned one
file is created. The file names are constructed from the parameter
names. In addition :option:`--suffix` can be used to add an individual
tag to the file names. The results that are plotted are taken from the
result files that are given as arguments to the scripts. If multiple
result files are given, the results from these files are concatenated.
By default PDF files are created using matplotlib.
:option:`--make-plots` can be used to produce dat files for
:program:`make-plots` instead.

Example
^^^^^^^

Simply plot the scatter of results from :file:`myresults.pkl` and draw
lines at the parameter boundaries in :file:`sample.ranges`::

    prof-plotresultscatter --ranges sample.ranges myresults.pkl


Command-line options
^^^^^^^^^^^^^^^^^^^^
.. cmdoption:: --liny, --logy

    Use a linear (default) or logarithmic scale for the GoF axis.

.. cmdoption:: --ndof, --no-ndof

    Plot :math:`\chi^2/N_{df}` (default) or :math:`\chi^2` as GoF.

.. cmdoption:: --make-plots

    Produce dat files suitable for :program:`make-plots` instead of PDF
    files.

.. cmdoption:: -m, --maxruns-value

    Add a text with the parameter values of the minimization results
    with the maximal number of anchor points used. If more than one
    result with this number of anchor points exists in the input files
    the text is only drawn if the results match up to numerical
    differences. Otherwise a warning is logged.

.. cmdoption:: --outdir DIRECTORY

    The directory were the output files are saved. It is created
    together with parent directories if necessary.

.. cmdoption:: --suffix SUFFIX

    An arbitrary tag that is appended to each file name. This can be
    used to have plots for more than one set of results in the same
    directory, e.g. to create html-galleries easily.

.. cmdoption:: --ranges RANGEFILE

    The parameter ranges that were used for the sampling of the anchor
    points.

Display style changes
"""""""""""""""""""""

.. cmdoption:: -r, --runs

    Change the display style for results with different numbers of
    anchor points used [default].

.. cmdoption:: -R, --no-runs

    Don't change the display style for results with different numbers of
    anchor points used [default].

.. cmdoption:: -s, --startpoints

    Change the display style for results with different methods of
    setting the initial point of the minimization [default].

.. cmdoption:: -S, --no-startpoints

    Don't change the display style for results with different methods of
    setting the initial point of the minimization [default].

.. cmdoption:: -l, --limits

    Change the display style for results if limits were imposed or not
    during the minimization [default].

.. cmdoption:: -L, --no-limits

    Don't change the display style for results if limits were imposed or
    not during the minimization [default].

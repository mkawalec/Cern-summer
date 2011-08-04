Line scan verification -- :program:`prof-scanchi2`
--------------------------------------------------

.. create some short-cuts to link to other documents
.. |prof-interpolate| replace:: :doc:`prof-interpolate <prof-interpolate>`
.. |prof-tune| replace:: :doc:`prof-tune <prof-tune>`
.. |prof-plotresultscatter| replace:: :doc:`prof-plotresultscatter <prof-plotresultscatter>`
.. |prof-runcombs| replace:: :doc:`prof-runcombs <prof-runcombs>`
.. |prof-sampleparams| replace:: :doc:`prof-sampleparams <prof-sampleparams>`

.. |prof-scanchi2| replace:: :program:`prof-scanchi2`
.. program:: prof-scanchi2

To verify that an optimal set of parameter values, that was found by
running |prof-tune| and inspecting the scatter of the results (kebab
plots) with |prof-plotresultscatter|, the Professor tool chain provides
|prof-scanchi2|. At certain points in parameter space, |prof-scanchi2|
compares the goodness of fit (GoF) between the "true" MC data and the
reference data with the GoF between the interpolation and the reference
data. The latter is the GoF that was used in the optimization procedure
in |prof-tune|, the first is the GoF that is really to be minimized.

The points are usually sampled along a straight line with
|prof-sampleparams| using the
:ref:`line scan mode <prof-sampleparams-line_scan_mode>`.

Depending on the given arguments |prof-scanchi2| plots only the "true"
MC-reference data GoF or the interpolation-reference data GoF.

The :option:`--datadir` `DATADIR` and related options are used as normal to
specify the reference data, MC runs, and interpolation objects: see the :doc:`path
options <options-paths>` page.
To plot the "true" MC-reference data GoF the location of the scan MC
data must be specified using :option:`--scandir` `SCANDIR`. By default
:file:`{DATADIR}/scandir/` is assumed (see :option:`--datadir` below).

To plot the interpolation-reference data GoF the location of the
interpolation files and a list of run combinations must be given. The
location of the interpolation files can be passed by :option:`--ipoldir`
`IPOLDIR` (default: :file:`{DATADIR}/ipoldir/`). Run combinations can
be passed either by :option:`--runcombs` `RUNSFILE:IPOLMETHOD` or they
are taken from minimization results files passed by :option:`--results`
`RESULTS`.

.. note::

    If no MC scan directory exists, |prof-scanchi2| will fail unless
    :option:`--no-scandata` is specified and the end points of the line
    are passed by :option:`--endpoints` `ENDPOINTS`.

By default the x-axis represents the location along the line. Using
:option:`--params` `PARAM1[,...]` the x-axis will represent the
projected position on the respective parameter axis.

Interpretation
^^^^^^^^^^^^^^

A good agreement between the two GoF definitions shows that the initial
assumption to approximate the per-bin response function by the
interpolation is valid. If the comparison shows a difference, it is
advisable to resize the initial parameter space (i.e. in- or excluding
some regions of parameter space) and repeat the full procedure of MC
sampling, interpolating and GoF optimization. If time is critical, the
``extract`` mode of |prof-runcombs| can be used to limit the used MC
sample data to narrower parameter ranges.

Examples
^^^^^^^^

Plot the "true" MC-reference GoF of the MC runs in :file:`my-scan-data/`.
The end points of the line are taken from the :file:`used_params` files
and the observables/weights for the GoF are taken from
:file:`my-weights`::

    prof-scanchi2 --scandir my-scan-data --weights my-weights

Plot the interpolation-reference GoF along a straight line between the
two points given by :file:`endpoints.params` (no MC scan data is plotted).
The interpolations are taken from :file:`my-ipol/`, the observables/weights
are taken from :file:`my-weights`, and the run combinations are taken from
:file:`my-runs`. Quadratic polynomials are used for interpolation::

    prof-scanchi2 --ipoldir my-ipol --weights my-weights --runcombs my-runs:quadratic --no-scandata --endpoints endpoints.params

Combine the above two examples and directly compare "true" MC-reference
GoF and interpolation-reference GoF::

    prof-scanchi2 --scandir my-scan-data --weights my-weights --ipoldir my-ipol --runcombs my-runs:quadratic


Command-line options
^^^^^^^^^^^^^^^^^^^^

The :option:`--datadir` `DATADIR` and related options are used as normal to
specify the reference data, MC runs, and interpolation objects: see the :doc:`path
options <options-paths>` page.

.. cmdoption:: --tag TAG

    Specify a tag that is appended to the generated file name.

.. cmdoption:: --results RESULTS

    Use the run combinations and interpolations methods from the
    minimization results in `RESULTS`. Additionally the distribution of
    the projection of the minimization results on the scan line is shown
    in a histogram in the upper panel (this can be turned off with
    :option:`--no-hist`).

.. cmdoption:: --runcombs RUNSFILE:METHOD[,...]

    Files with run combinations that are used for GoF estimation from
    interpolations. The interpolation method must be given as well
    separated by a ':' and different files must be separated by a ','.
    E.g. 'myruncombs.dat:quadratic,mycubecombs.dat:cubic'

.. cmdoption:: <+--OPTION+> <+METAVAR+>

    <+DESCRIPTION+>

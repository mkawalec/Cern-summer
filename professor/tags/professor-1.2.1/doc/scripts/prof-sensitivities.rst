Observable sensitivities -- :program:`prof-sensitivities`
---------------------------------------------------------

.. create some short-cuts to link to other documents
.. |prof-tune| replace:: :doc:`prof-tune <prof-tune>`
.. |prof-interpolate| replace:: :doc:`prof-interpolate <prof-interpolate>`
.. |prof-I| replace:: :doc:`prof-I <prof-I>`

.. program:: prof-sensitivities

A crucial decision at the beginning of every tuning effort is to decide
which observables should be included in the tune, i.e. included in the
goodness of fit function that is optimized with |prof-tune|. To assist
you with this decision :program:`prof-sensitivities` calculates the
sensitivity of a data bin to the model parameters. However, this does
not replace a good knowlegde of the model that is tuned. Rather, the
sensitivity can help you to identify parameters that are less important
and might be excluded in a tune and to identify observables that can be
used to constrain parameters. To make the calculation of the sensitivity
fast the polynomial interpolation of the MC response is used for this.

The :option:`--datadir` `DATADIR` and related options are used as normal to
specify the reference data, MC runs, and interpolation objects: see the :doc:`path
options <options-paths>` page.

:program:`prof-sensitivities` can create color map plots and 2D plots
visualizing the extremal sensitivity. The type of plot can be chosen
with :option:`--plotmode`. The accepted values are described below under
:ref:`plot-modes`. The sensitivity definition can be selected with
:option:`--definition`. The different definitions are discussed under
:ref:`sensitivity-definitions`. The location where the plot files are
created can be given by :option:`-o` `OUTDIR`.

:program:`prof-sensitivities` expects that the observables for which the
sensitivities are calculated are specified in the file given by
:option:`--weights` `WEIGHTS`. The file `WEIGHTS` can be in the usual
format used to specify observable weights or a simple list of
observables, one per line. The location of the interpolation coefficient
cache files (created with |prof-interpolate|) and optionally the
reference data must be given by the data-location options, e.g.
:option:`--datadir` or :option:`--ipoldir` and :option:`--refdir`.

The order of the polynomial used for interpolation can be specified by
:option:`--ipol-method` and the run combination is taken to be the first
one in the file given by :option:`-R` `RUNSFILE`.


Example
^^^^^^^

Create extremal sensitivities derived from sampling along a cross in
parameter space using the default definition and plot style::

    prof-sensitivities --datadir my/data/ -R myruncombinations --weights sensitivity.observables

The above will produce one plot for each observable in
:file:`sensitivity.observables` in the default output directory
:file:`sensitivities`.


.. _plot-modes:

Plot modes
^^^^^^^^^^

Basically two different types of plots can be produced: color maps and
2D plots showing only the extremal sensitivity for each parameter. The
color maps show the sensitivity for each parameter and observable in a
separate plot, i.e. one ends up with
:math:`N = N_\mathrm{obs} \cdot N_\mathrm{params}`
plots. When the sensitivity of observable `O` on parameter `P1` is
calculated the remaining parameters are not varied, i.e. the sensitivity
is calculated along a cross in parameter space::

    p_2  ^
         |
         |           x  ==> Sensitivity for parameter p_2
         |           "
         |           x
         |           "
         |           x
         |           "
         |  =x=x=x=x=o=x=x=x=x=x=x=x   ==> Sensitivity for parameter p_1
         |           "
         |           x
         |           "
         |           x
         |
         +----------------------------->
                                      p_1

The center of the cross (``o`` in the above) can be set using
:option:`--paramsfile` or :option:`--paramsvector`. By default the
center of the parameter hyper cube used for interpolation is used.

The accepted color map plot modes are:

colormap
    Create a color map for each observable-parameter combination. Each
    plot has its own scale for the z-axis data.

colormaplim
    Same as colormap. But all plots have the same scale for the z-axis
    data.

colormapobslim
    Same as colormap. But all plots for the same observable have the same
    scale for the z-axis data.

The accepted extremal plot modes are:

extremal
    Produce one plot per observable. Only the extremal sensitivity value
    found on axes of the cross is plotted.

extrandom
    Same as extremal. But instead of calculating the sensitivities along
    the axes of a cross, the sensitivity is calculated at points sampled
    randomly from the parameter space and only the extremal value for
    each parameter is kepts. The range from which the points are sampled
    can be specified with :option:`--paramsrange`. It defaults to the
    range of the anchor points used for the interpolation.


.. _sensitivity-definitions:

Sensitivity definitions
^^^^^^^^^^^^^^^^^^^^^^^

Several different ways how to calculate the sensitivity are implemented
which are more or less robust for some borderline cases. The sensitivity
definition should take into account that both parameters and the bin
values have different scales. Consider, for example, two parameters with
physical meaningful ranges of

.. |p1| replace:: :math:`p_1`
.. |p2| replace:: :math:`p_2`
.. |b1| replace:: :math:`b_1`
.. |b2| replace:: :math:`b_2`

.. math::

    0.1 < p_1 < 0.4 , \quad 1.0 < p_2 < 10.0 ,

and two bins, |b1| and |b2|, where the first is typically of order 10
and the other of order 1000.

If, now, changing |p1| or |p2| by 0.1 changes |b1| by 1 unit we say that
|b1| is more sensitive to |p2| than to |p1| because to gain a change of
1 unit in |b1| we have to move our |p1| value by ~30% but the |p2| value
only ~1% of the expected range. If, on the other hand, changing |p2| by
0.1 changes |b1| and |b2| by 1 unit we say that |b1| is more sensitive
to |p2| than |b2| because change of a bin with content of 1000 (|b2|) by
1 is not as exciting as the same change in a bin with a content of 10
(|b1|).

So what we are looking for is something like a relative derivative as

.. math::

    S_i = \frac{\partial \ln MC(p)}{\partial \ln p_i}
    = \frac{\partial MC(p)/MC(p)}{\partial p_i/p_i}

i.e. to norm the differential by the values they are taken at.

However, this is not working for either :math:`MC = 0` or
:math:`p_i = 0`. To work around this, we use a slighly modified
definition:

.. math::

    S_i = \frac{\partial MC(p)}{|MC(p_0)| + \epsilon \, w_{MC}}
          \frac{|p_{0,i}| + \epsilon \, w_{p_i}}{\partial p_i}

where :math:`p_0` is assumed to be a typical set of parameter values
(set by :option:`--paramsfile`, :option:`--paramsvector` or the center
of :option:`--paramsrange`) and the :math:`\epsilon` terms are
introduced to work around the borderline cases :math:`MC, p_i = 0`.
:math:`w_{p_i}` corresponds to 80% of the original sampling range and
:math:`w_{MC}` is constructed from this.

.. todo::

    List the available sensitivity definition.


Command-line options
^^^^^^^^^^^^^^^^^^^^

The :option:`--datadir` `DATADIR` and related options are used as normal to
specify the reference data, MC runs, and interpolation objects: see the :doc:`path
options <options-paths>` page.

Output/Plot style
"""""""""""""""""

.. cmdoption:: --plotmode PLOTMODE

    The type of plots to produce, see :ref:`plot-modes`.
    [default: extremal]

.. cmdoption:: --definition DEFINITION

    The sensitivity definition to use, see
    :ref:`sensitivity-definitions`.

.. cmdoption:: --table TABLEFILE

    Create a LaTeX table stub in `TABLEFILE` for all one-bin observables
    in extremal plot modes. By default no such file is created.

.. cmdoption:: --splines, --no-splines

    Do/do not connect data points with splines in the extremal plot
    modes. Default is to draw the splines.

.. cmdoption:: --legend, --no-legend

    Put/don't put a legend on every plot in extremal plot modes. Default
    is to draw a legend.

.. cmdoption:: --logy

    Use a logarithmic scale for the sensitivity axis in extremal plot
    modes. Default is to use a linear scale.

.. cmdoption:: --make-plots

    Create output files suitable for :program:`make-plots` when
    producing color map plots. Default is to use matplotlib for
    plotting.

Input
"""""

.. cmdoption:: --paramsfile PARAMETERFILE,  --pf PARAMETERFILE

    File with parameter values used as center of the parameter cross.

.. cmdoption:: --paramsvector PARAMETERSTRING, --pv PARAMETERSTRING

    String specifying the parameter values used as center of the
    parameter cross. E.g. `PAR1=42.0,PAR2=0.23`.

.. cmdoption::  --paramsrange RANGEFILE, --pr RANGEFILE

    File with parameter sampling range for `extrandom` plot method.

.. cmdoption:: -R RUNSFILE, --runsfile RUNSFILE, --runcombs RUNSFILE

    A file with the run combination that is used for the interpolation.
    Only the first run combination in this file is used.
    [default: :file:`runcombs.dat`]

.. cmdoption:: --ipol-method IPOLMETHOD

    The interpolation method. At the moment the order of the polynomial:
    ``quadratic`` or ``cubic``. [default: ``quadratic``]

.. cmdoption:: --weights WEIGHTS, --obsfile WEIGHTS

    A file listing the observables and their weights which are used in
    the GoF.

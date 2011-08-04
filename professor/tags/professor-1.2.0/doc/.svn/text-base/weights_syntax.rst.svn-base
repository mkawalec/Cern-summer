.. _weightssyntax:

*******************
Weights File Syntax
*******************

.. create some short-cuts to link to other documents
.. |prof-interpolate| replace:: :doc:`prof-interpolate <scripts/prof-interpolate>`
.. |prof-ipolhistos| replace:: :doc:`prof-ipolhistos <scripts/prof-ipolhistos>`
.. |prof-envelopes| replace:: :doc:`prof-envelopes <scripts/prof-envelopes>`
.. |prof-tune| replace:: :doc:`prof-tune <scripts/prof-tune>`
.. |prof-compare-tunes| replace:: :doc:`prof-compare-tunes <scripts/prof-compare-tunes>`


Weights files are used for different purposes by professor:

* Simply list the observables for plotting with e.g. |prof-ipolhistos|,
  |prof-envelopes| or for interpolation with |prof-interpolate|.

* Define the per-bin weights used in the goodness-of-fit function used
  by |prof-tune| or |prof-compare-tunes|.

The syntax of weights file is line-oriented: Each line defines the
weight for a set of bins of an observable. The weight definitions have
the form::

    /AnalysisID/Observable:startValue:endValue weight # comment

This defines a weight for the bins with a center value within the
interval [`startValue`, `endValue`] for observable
`/PATH_TO/OBSERVABLE`. `startValue` and `endValue` can be omitted
meaning to include all bins from the start or all bins to the end,
respectively. E.g::

    /DELPHI_1996_S3430090/d11-x01-y01::0.14 2.0
    /DELPHI_1996_S3430090/d11-x01-y01:0.14: 1.0

defines a weight of 2.0 for the bins with a bin center below 0.14 and a
weight of 1.0 for bins with a bin center above 0.14 for the 1-Thrust
observable of this DELPHI analysis.

Everything after a `#` is treated as a comment and ignored as well are
empty lines.

The `weight` can be omitted. In this case the weight is taken to be
1.0 .

To set the same weight for all bins of an observable the bin-range
definition can be omitted completely::

    /AnalysisID/Observable2 2.3

The above defines a weight of 2.3 for all bins in
`/AnalysisID/Observable2`.

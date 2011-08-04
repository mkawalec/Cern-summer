"""\
Introduction
------------

This package contains container classes for parameter related data, e.g.
parameter points. All classes are child-classes of
:class:`~professor.params.base.ParameterBase`, which itself inherits from
numpy's ndarray. Methods exist for IO to/from :class:`dict` and text files:
    * :meth:`~professor.params.base.ParameterBase.mkFromFile`,
      :meth:`~professor.params.base.ParameterBase.forFile` and
      :meth:`~professor.params.base.ParameterBase.writeParamFile`
    * :meth:`~professor.params.base.ParameterBase.mkFromDict` and
      :meth:`~professor.params.base.ParameterBase.asDict`

The following classes are implemented:

    :class:`ParameterPoint`
        Container for name-value data, e.g. locations or directions in
        parameter space.

    :class:`ParameterRange`
        Container for name-val1-val2 data, e.g. parameter ranges for
        sampling anchor points or line-scan points.

    :class:`ParameterErrors`
        Container for errors of tuned parameter values.

    :class:`ParameterMatrix`
        Container for parameter-parameter matrix data, e.g. the correlation
        matrix.


Documentation
^^^^^^^^^^^^^

.. autoclass:: professor.params.base.ParameterBase
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: ParameterPoint
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: ParameterRange
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: ParameterErrors
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: ParameterMatrix
    :members:
    :undoc-members:
    :show-inheritance:
"""
from base import ParameterPoint, ParameterRange, ParameterErrors, ParameterMatrix, ParameterBase

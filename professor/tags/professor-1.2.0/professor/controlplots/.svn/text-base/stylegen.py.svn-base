"""Little helper for plot style generation.

See documentation for class StyleGenerator
"""

class StyleGenerator(object):
    """Little helper for plot style generation.

    Keyword arguments are accepted that connect matplotlib plot kwargs with
    objects that have a next() method. Each StyleGenerator.next() call
    returns a dictionary that contains the initial kwargs keys paired with
    the outcome of the respective next() calls.

    The itertools builtin module contains useful generators: cycle, repeat, ...

    Example:

        >>> mystylegen = StyleGenerator(
        ... color = itertools.cycle(["r", "k", "b", "g"]),
        ... linestyle = itertools.repeat("solid"),
        ... linewidth = itertools.cycle(numpy.arange(2.0, 0.3, -0.6)))
        ...
        >>> mystylegen.next()
        {'color': 'r', 'linestyle': 'solid', 'linewidth': 2.0}
        >>> mystylegen.next()
        {'color': 'k', 'linestyle': 'solid', 'linewidth': 1.3999999999999999}
    """
    def __init__(self, **kwcycles):
        self._kwcycles = kwcycles

    def next(self):
        r = {}
        for k, cyc in self._kwcycles.items():
            r[k] = cyc.next()
        return r

    def __str__(self):
        return ("<StyleGenerator object for ['" +
                "', '".join(self._kwcycles.keys()) + "']>")

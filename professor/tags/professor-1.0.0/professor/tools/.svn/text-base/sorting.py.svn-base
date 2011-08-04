"""
Helpers for collection sorting.
"""



def cmpByInt(sa, sb):
    """Compare two strings by numbers found in them.

    If one or both lack a number usual string-comparision is performed.

    Used to sort Pythia's PARJ(<NUM>) parameters.
    """
    import re
    pattern = re.compile(r'[0-9]+')
    try:
        numa = int(pattern.findall(sa)[0])
        numb = int(pattern.findall(sb)[0])
        return cmp(numa, numb)
    except IndexError:
        ## Failed to find a number
        return cmp(sa, sb)


def cmpBinID(idA, idB):
    """Compare bin ids first by observable name, then by numeric bin number."""
    histA, binA = idA.split(":")
    histB, binB = idB.split(":")
    ret = cmp(histA, histB)
    if ret == 0:
        return cmp(int(binA), int(binB))
    else:
        return ret


class ParameterCmp(object):
    """Comparison to sort parameter names in a specified order.

    This is intendet to be used as `cmp_` argument to
    :meth:`ParameterBase.format` or :meth:`ParameterBase.writeParamFile`.
    """
    def __init__(self, names):
        self._names = names

    @classmethod
    def mkFromFile(cls, path):
        from professor.params import ParameterBase
        names = ParameterBase._parselines(open(path))[0]
        return cls(names)

    def __call__(self, sa, sb):
        ia = self._names.index(sa)
        ib = self._names.index(sb)
        return cmp(ia, ib)


if __name__ == "__main__":
    import professor.user as prof

    names = ["Par B", "Par  a", "Par 1", "Par 20"]
    values = [1., 3., 0., 4.]

    pp = prof.ParameterPoint(names, values)
    cmp_ = ParameterCmp(names)

    print "cmp_ = None"
    print pp.forFile(cmp_=None)
    print "cmp_ = cmpByInt"
    print pp.forFile(cmp_=cmpByInt)
    print "cmp_ = ParameterCmp(...)"
    print pp.forFile(cmp_=cmp_)

"""parameter.py

This file contains 3 classes which allow us to handle parameters in a
controlled way:
    - class L{FixedSortedKeys}:
        Stores an alphabetically sorted list of key names, normally the
        parameter names.
        It's the base class for classes dealing with parameter vectors.

    - class L{Scaler}:
        Stores upper and lower boundaries for parameter scaling.

    - class L{ParameterPoint}:
        Stores scaled and unscaled versions of the given parameter
        point.

"""

# for epydoc
__docformat__ = "epytext"


import numpy

from types import ListType, DictType



class FixedSortedKeysError(Exception):
    pass

class ParameterError(Exception):
    pass


class FixedSortedKeys(object):
    """Stores given keys in a sorted list."""
    def __init__(self, indices):
        """
        @param indices: list with unique keys.
        @type indices: C{list}
        @raise TypeError: If indices is not a list.
        @raise ValueError: If indices are not unique.
        """
        if type(indices) != ListType:
            raise TypeError("argument indices must be a list!")

        if len(set(indices)) != len(indices):
            raise ValueError("indices must be unique!")
        self._keys = indices[:]
        self._keys.sort()

    def getIndex(self, key):
        """Return the index of given key."""
        return self._keys.index(key)

    def getKeys(self):
        """Return the stored keys."""
        return self._keys

    def goodPartner(self, candidate):
        """Check if self and candidate have the same keys."""
        if not self.getKeys() == candidate.getKeys():
            raise FixedSortedKeysError("keys differ: %s != %s !"%(self, candidate))
        return True

    def __str__(self):
        return "FixedSortedKeys:\n    %s\n"%(self._keys)

    def __len__(self):
        """Return the number of keys.

        For subclasses like ParameterPoint or BinDistribution it returns the
        number of parameters aka the dimension of the tuning.
        """
        return len(self._keys)

    dim = __len__


class Scaler(FixedSortedKeys):
    def __init__(self, data):
        """
        @param data: A C{list} with the parameter names, this Scaler
            instance should handle. If it's a C{dict}, it must contain
            C{{"param name" : (min, max)}} pairs.
            If it's a C{list} lower boundaries are set to 0 upper to 1. So
            NO scaling takes place.
        @type data: C{dict} or C{list}
        @raise TypeError: If data is of wrong type.
        """
        if type(data) == ListType:
            super(Scaler, self).__init__(data)
            self._min = numpy.zeros(len(self))
            self._max = numpy.ones(len(self))

        elif type(data) == DictType:
            super(Scaler, self).__init__(data.keys())
            self._min = numpy.zeros(len(self))
            self._max = numpy.zeros(len(self))
            for i, name in enumerate(self.getKeys()):
                self._min[i] = data[name][0]
                self._max[i] = data[name][1]

        else:
            raise TypeError("data must be a list or dict!")

    def setVal(self, name, min=None, max=None):
        """Set a new minimal and/or maximal value.

        @param name: the parameter name.
        @param min: the new lower boundary
        @param max: the new upper boundary
        """
        i = self.getIndex(name)
        if min is not None:
            self._min[i] = min
        if max is not None:
            self._max[i] = max

    def getMinVals(self):
        return self._min

    def getMaxVals(self):
        return self._max

    def getMinVal(self, name):
        return self._min[self.getIndex(name)]

    def getMaxVal(self, name):
        return self._max[self.getIndex(name)]

    def scale(self, vec):
        return (vec - self._min)/(self._max - self._min)

    def descale(self, vec):
        return vec*(self._max - self._min) + self._min

    def __str__(self):
        r = "Scaler:\n"
        r += "    param   lower  upper\n"
        for key in self.getKeys():
            r += "    %s   %f  %f\n"%(key, self.getMinVal(key), self.getMaxVal(key))
        return r[:-1]

# Keep old code working
Normalizer = Scaler


class ParameterPoint(FixedSortedKeys):
    def __init__(self, data, scaler, scaled=False):
        """
        Parameter data is stored scaled AND unscaled! But the unscaled
        values are regarded as constant whereas the scaled values can
        changed, e.g. when new scaling boundaries are chosen.

        @param data: C{dict} with parmeter name - value pairs.
        @param scaler: L{Scaler} instanced, used to scale this
            parameter point.
        @param scaled: Flag indicating if the given data is scaled.
        @raise ValueError: If give data and scaler don't have the same
            keys.
        """
        super(ParameterPoint, self).__init__(data.keys())

        if not super(ParameterPoint, self).goodPartner(scaler):
            raise ValueError("given scaler is not valid, e.g."
                    " different index names")
        self._scaler = scaler

        # t = numpy.zeros(len(self))
        t = numpy.zeros(self.dim())
        for i, name in enumerate(self.getKeys()):
            t[i] = data[name]

        if scaled:
            self._scaled = t
            self._unscaled = self._scaler.descale(t)
        else:
            self._scaled = self._scaler.scale(t)
            self._unscaled = t

    def getScaler(self):
        return self._scaler

    def getScaled(self):
        return self._scaled

    def getUnscaled(self):
        return self._unscaled

    # Keep old code working
    getNormalized = getScaled
    getUnnormalized = getUnscaled

    def rescale(self):
        """Recalculate the scaled values.

        Use this if scaling boundaries change.
        """
        self._scaled = self._scaler.scale(self._unscaled)

    def __str__(self):
        r = "%s:\n"%(self.__class__.__name__)
        r += "    param   unscaled  scaled\n"
        for i, name in enumerate(self.getKeys()):
            r += "    %s   %f  %f\n"%(name, self._unscaled[i],
                    self._scaled[i])
        return r[:-1]

    def goodPartner(self, candidate):
        """Checks if self and candidate have the same keys and scalers.

        @type candidate: ParameterPoint
        """
        super(ParameterPoint, self).goodPartner(candidate)
        if not self._scaler is candidate._scaler:
            raise ParameterError("scalers differ: no good partner!")
        return True


# Factory function form ParameterPoints
def ppFromList(plist, scaler, scaled=False):
    """Build a ParameterPoint instance from a list with parameter values.

    Uses the given scaler to get the parameter names.

    @see: ParameterPoint

    @param plist: C{list}-like object with the parameter values.
    """
    d = {}
    for i, pname in enumerate(scaler.getKeys()):
        d[pname] = plist[i]
    return ParameterPoint(d, scaler, scaled)

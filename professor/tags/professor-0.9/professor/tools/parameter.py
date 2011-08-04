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


import numpy, re


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
        if type(indices) != list:
            raise TypeError("argument indices must be a list!")

        if len(set(indices)) != len(indices):
            raise ValueError("indices must be unique!")
        self._keys = indices[:]
        self._keys.sort()

    def getIndex(self, key):
        """Return the index of given key."""
        return self.getKeys().index(key)

    def getKeys(self):
        """Return the stored keys."""
        return self._keys

    def goodPartner(self, candidate):
        """Check if self and candidate have the same keys."""
        if not self.getKeys() == candidate.getKeys():
            raise FixedSortedKeysError("keys differ: %s != %s !" % (
                    self.getKeys(), candidate.getKeys()))
        return True

    def __str__(self):
        return "FixedSortedKeys:\n    %s\n"%(self._keys)

    def __len__(self):
        """Return the number of keys.

        For subclasses like ParameterPoint or BinDistribution it returns the
        number of parameters aka the dimension of the tuning.
        """
        return len(self.getKeys())

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
        if type(data) == list:
            super(Scaler, self).__init__(data)
            self._min = numpy.zeros(len(self))
            self._max = numpy.ones(len(self))

        elif type(data) == dict:
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

    def scaleComponent(self, scaledval, paramid):
        """Descale the given scaled parameter value.

        paramid can be an int (=> parameter index)
        or a string (=> parameter name).
        """
        if type(paramid) != int:
            paramid = self.getIndex(paramid)
        return (scaledval - self._min[paramid])/(self._max[paramid] - self._min[paramid])

    def descale(self, vec):
        return vec*(self._max - self._min) + self._min

    def descaleComponent(self, scaledval, paramid):
        """Descale the given scaled parameter value.

        paramid can be an int (=> parameter index)
        or a string (=> parameter name).
        """
        if type(paramid) != int:
            paramid = self.getIndex(paramid)
        return scaledval*(self._max[paramid] - self._min[paramid]) + self._min[paramid]

    def __str__(self):
        r = "Scaler:\n"
        r += "    param   lower  upper\n"
        for key in self.getKeys():
            r += "    %s   %f  %f\n"%(key, self.getMinVal(key), self.getMaxVal(key))
        return r[:-1]

# Keep old code working
Normalizer = Scaler


class ParameterPoint(FixedSortedKeys):
    @classmethod
    def fromList(cls, plist, scaler, scaled=False):
        """Build a ParameterPoint instance from a list with parameter values.

        Uses the given scaler to get the parameter names.

        @param plist: C{list}-like object with the parameter values.
        """
        d = {}
        for i, pname in enumerate(scaler.getKeys()):
            d[pname] = plist[i]
        return cls(d, scaler, scaled)

    @classmethod
    def fromFile(cls, paramfile, ranges, scaled=False):
        """Load parameters from a file.

        ranges  -- Can be a Scaler instance or a dictionary with range
            definitions or the name of the file that contains range definitions.
        """
        params = readParameterFile(parampath)
        if type(ranges) != Scaler:
            if type(ranges) == str:
                ranges = readParameterFile(ranges)
            elif type(ranges) != dict:
                raise TypeError("Argument ranges has wrong type: '%s' of"
                                " type %s" % (ranges, type(ranges)))
            scaler = Scaler(ranges)
        return cls(params, scaler, scaled)

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

        # Check if I and the given scaler share the same parameter names.
        FixedSortedKeys.goodPartner(self, scaler)
        self._scaler = scaler

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
        return self._scaled.copy()

    def getUnscaled(self):
        return self._unscaled.copy()

    # Keep old code working
    getNormalized = getScaled
    getUnnormalized = getUnscaled

    def rescale(self):
        """Recalculate the scaled values.

        Use this if scaling boundaries change.
        """
        self._scaled = self._scaler.scale(self._unscaled)

    def __str__(self):
        if hasattr(self, "_scaled") and hasattr(self, "_unscaled"):
            jwidth = max(map(len, self.getKeys()))
            r = "%s:\n"%(self.__class__.__name__)
            r += "    param   unscaled  scaled\n"
            for i, name in enumerate(self.getKeys()):
                r += "    %s   %f  %f\n" % (name.ljust(jwidth),
                                            self._unscaled[i],
                                            self._scaled[i])
            return r[:-1]
        else:
            return "<Partly initialised ParameterPoint instance>"

    def goodPartner(self, candidate):
        """Checks if self and candidate have the same keys and scalers.

        @type candidate: ParameterPoint
        """
        super(ParameterPoint, self).goodPartner(candidate)
        if not self._scaler is candidate._scaler:
            raise ParameterError("scalers differ: no good partner!")
        return True

    def asDict(self, scaled=True):
        """ return parameter point as simple dictionary """
        temp = dict.fromkeys(self.getKeys())
        for param in self.getKeys():
            if scaled:
                temp[param] = self.getScaled()[self.getIndex(param)]
            else:
                temp[param] = self.getUnscaled()[self.getIndex(param)]
        return temp

    def distanceToP0(self, p0, scaled=False):
        if not scaled:
            dist = self._unscaled - p0._unscaled
        else:
            dist = self._scaled - p0._scaled
        return numpy.sqrt(numpy.dot(dist, dist))


class ParameterRange(FixedSortedKeys):
    def __init__(self, rangedict):
        super(ParameterRange, self).__init__(rangedict.keys())
        self._data = rangedict.copy()
        self.keys = self.getKeys

    def __getitem__(self, paramname):
        return self._data[paramname]

    def getLowerBound(self, paramname):
        return self._data[paramname][0]

    def getUpperBound(self, paramname):
        return self._data[paramname][1]

    def __str__(self):
        jwidth = max(map(len, self.keys()))
        s = ""
        for name in self.keys():
            s += "%s  %f  %f\n" % (name.ljust(jwidth), self.getLowerBound(name), self.getUpperBound(name))
        s = s[:-1]
        return s


def prettyPrintParameter(arg):
    """Pretty multiline formatted string version of arg.

    arg can be
    * a dict containing a parameter point/parameter ranges
    * a ParameterPoint instance
    * ...
    """
    if type(arg) == dict:
        s = ""
        # length of longes parameter name
        jwidth = max(map(len, arg.keys()))
        for name in sorted(arg.keys()):
            s += name.ljust(jwidth)
            val = arg[name]
            try:
                for v in val:
                    s += "  %f" % (v)
                s += "\n"
            except TypeError:
                s += "  %f\n" % (val)
        # strip last newline
        s = s[:-1]
        return s
    return str(arg)


# Factory function for ParameterPoints
def ppFromList(plist, scaler, scaled=False):
    """Build a ParameterPoint instance from a list with parameter values.

    Uses the given scaler to get the parameter names.

    @see: ParameterPoint

    @param plist: C{list}-like object with the parameter values.
    """
    return ParameterPoint.fromList(plist, scaler, scaled)

def ppFromFile(parampath, rangefile, scaled=False):
    """ Create and return a ParameterPoint object from a file that holds
        coordinates for one point only and a param range file (or a param
        range file dict).
    """
    return ParameterPoint.fromFile(parampath, rangefile, scaled)

def readParameterFile(path, checklog=False):
    """Read a parameter file and return the according dictionary """
    try:
        pfile = open(path, 'r')
    except:
        raise Exception("Cannot open file %s" % (path))

    params = {}
    logs = []
    for line in pfile:
        line = re.sub(r'(^.*?)#.*', r'\1', line) # strip comments
        line = re.sub(r'=+', r' ', line) # collapse equal signs
        line = re.sub(r' +', r' ', line) # collapse spaces
        line = re.sub(r'\n', r'', line) # remove newline
        if len(line) == 0 or line == " ":
            continue
        tokens = line.split()
        if len(tokens) == 2:
            params[tokens[0]] = float(tokens[1])
        elif len(tokens) ==3:
            params[tokens[0]] = numpy.array([float(tokens[1]), float(tokens[2])])
        elif len(tokens) ==4:
            if checklog and tokens[3] in ["L","l","log","LOG"]:
                params[tokens[0]] = numpy.array([float(tokens[1]), float(tokens[2])])
                logs.append(tokens[0])
            else:
                params[tokens[0]] = numpy.array([float(tokens[1]), float(tokens[2]), float(tokens[3])])
    ## consistency check:
    for k, v in params.iteritems():
        if not type(params[params.keys()[0]]) == type(v):
            raise Exception("Parameter file faulty in param %s!" % (k))
    pfile.close()
    if checklog:
        return params, logs
    else:
        return params
